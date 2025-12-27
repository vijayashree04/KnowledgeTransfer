import os
from typing import Optional, List, Dict
import gemini_utils

# Pinecone configuration
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "kt-docs")

# Try to import Pinecone
try:
    from pinecone import Pinecone
    PINECONE_AVAILABLE = True
except ImportError:
    PINECONE_AVAILABLE = False
    print("Warning: pinecone package not installed. Vector search will be disabled.")

# Initialize Pinecone client
pc = None
index = None

if PINECONE_AVAILABLE and PINECONE_API_KEY:
    try:
        pc = Pinecone(api_key=PINECONE_API_KEY)
        index = pc.Index(PINECONE_INDEX_NAME)
    except Exception as e:
        print(f"Warning: Failed to initialize Pinecone: {e}. Vector search will be disabled.")
        pc = None
        index = None

def is_enabled() -> bool:
    """Checks if Pinecone is configured and available."""
    return index is not None and PINECONE_AVAILABLE

def _chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Splits text into overlapping chunks for better vector search granularity."""
    if not text:
        return []
    
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        
        # Move start position with overlap
        start = end - overlap
        
        # Prevent infinite loop
        if start >= text_length:
            break
    
    return chunks

def index_document(
    team_id: str,
    doc_id: str,
    filename: str,
    content: str,
    uploaded_by: str,
    summary: Optional[str] = None,
    team_name: Optional[str] = None,
) -> bool:
    """Indexes a document in Pinecone by chunking it and creating embeddings."""
    if not is_enabled():
        return False
    
    if not content or not content.strip():
        print(f"Warning: No content to index for document {filename}")
        return False
    
    try:
        # Chunk the document content
        chunks = _chunk_text(content)
        
        if not chunks:
            print(f"Warning: No chunks created for document {filename}")
            return False
        
        # Generate embeddings for each chunk and upsert
        vectors_to_upsert = []
        
        for i, chunk in enumerate(chunks):
            try:
                # Generate embedding for this chunk
                embedding = gemini_utils.embed_text(chunk)
                
                if not embedding or len(embedding) == 0:
                    print(f"Warning: Failed to generate embedding for chunk {i} of {filename}")
                    continue
                
                # Create vector ID - use team_name if available for better readability
                if team_name:
                    vector_id = f"{team_name}:{doc_id}:chunk-{i}"
                else:
                    vector_id = f"{team_id}:{doc_id}:chunk-{i}"
                
                # Prepare metadata
                metadata = {
                    "team_id": str(team_id),
                    "doc_id": str(doc_id),
                    "filename": filename,
                    "uploaded_by": uploaded_by,
                    "chunk_index": i,
                    "snippet": chunk[:500],  # Store first 500 chars for context reconstruction
                }
                
                if team_name:
                    metadata["team_name"] = team_name
                
                if summary:
                    metadata["summary"] = summary[:500]  # Limit summary length
                
                vectors_to_upsert.append({
                    "id": vector_id,
                    "values": embedding,
                    "metadata": metadata
                })
                
            except Exception as e:
                print(f"Warning: Failed to process chunk {i} of {filename}: {e}")
                continue
        
        # Upsert all vectors in batches
        if vectors_to_upsert:
            try:
                # Upsert in batches of 100 (Pinecone's recommended batch size)
                batch_size = 100
                for i in range(0, len(vectors_to_upsert), batch_size):
                    batch = vectors_to_upsert[i:i + batch_size]
                    index.upsert(vectors=batch)
                
                print(f"Successfully indexed {len(vectors_to_upsert)} chunks for document {filename}")
                return True
            except Exception as e:
                print(f"Error upserting vectors to Pinecone: {e}")
                return False
        else:
            print(f"Warning: No vectors to upsert for document {filename}")
            return False
            
    except Exception as e:
        print(f"Error indexing document {filename} in Pinecone: {e}")
        return False

def query_similar_documents(
    query_text: str,
    team_id: str,
    team_name: Optional[str] = None,
    top_k: int = 5
) -> List[Dict]:
    """Queries Pinecone for similar documents based on the query text."""
    if not is_enabled():
        return []
    
    if not query_text or not query_text.strip():
        return []
    
    try:
        # Generate embedding for the query
        query_embedding = gemini_utils.embed_text(query_text)
        
        if not query_embedding or len(query_embedding) == 0:
            print("Warning: Failed to generate embedding for query")
            return []
        
        # Build filter for team
        filter_dict = {"team_id": {"$eq": str(team_id)}}
        
        # Query Pinecone
        results = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True,
            filter=filter_dict
        )
        
        # Process results
        matches = []
        if results and hasattr(results, 'matches'):
            for match in results.matches:
                matches.append({
                    "id": match.id,
                    "score": match.score,
                    "metadata": match.metadata if hasattr(match, 'metadata') else {}
                })
        
        return matches
        
    except Exception as e:
        print(f"Error querying Pinecone: {e}")
        return []

def build_context_from_matches(matches: List[Dict]) -> str:
    """Builds a context string from Pinecone query matches."""
    if not matches:
        return ""
    
    context_parts = []
    seen_docs = set()
    
    for match in matches:
        metadata = match.get("metadata", {})
        doc_id = metadata.get("doc_id")
        filename = metadata.get("filename", "Unknown")
        snippet = metadata.get("snippet", "")
        
        # Avoid duplicate documents
        if doc_id and doc_id not in seen_docs:
            seen_docs.add(doc_id)
            context_parts.append(f"From {filename}:\n{snippet}")
    
    return "\n\n".join(context_parts)

def delete_document_vectors(doc_id: str, team_id: str, team_name: Optional[str] = None) -> bool:
    """Deletes all vectors for a document from Pinecone."""
    if not is_enabled():
        return False
    
    try:
        # Build filter to find all chunks for this document
        filter_dict = {
            "team_id": {"$eq": str(team_id)},
            "doc_id": {"$eq": str(doc_id)}
        }
        
        # Get index stats to determine dimension
        try:
            stats = index.describe_index_stats()
            dimension = 768  # Default for Gemini text-embedding-004
            if hasattr(stats, 'dimension'):
                dimension = stats.dimension
            elif isinstance(stats, dict) and 'dimension' in stats:
                dimension = stats['dimension']
        except:
            dimension = 768  # Default fallback
        
        # Query to find all vector IDs for this document
        # Note: Pinecone doesn't have a direct delete by filter, so we need to query first
        # Use a zero vector for the query (we're only using the filter)
        dummy_vector = [0.0] * dimension
        
        results = index.query(
            vector=dummy_vector,
            top_k=10000,  # Large number to get all matches
            include_metadata=True,
            filter=filter_dict
        )
        
        if results and hasattr(results, 'matches'):
            vector_ids = [match.id for match in results.matches]
            if vector_ids:
                # Delete vectors by ID
                index.delete(ids=vector_ids)
                print(f"Deleted {len(vector_ids)} vectors for document {doc_id}")
                return True
        
        return False
        
    except Exception as e:
        print(f"Error deleting document vectors from Pinecone: {e}")
        return False

