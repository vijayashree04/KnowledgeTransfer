from google.genai import types
import google.genai as genai
import os
import streamlit as st

# Configure Gemini
# Try to get key from environment, otherwise check session state or user input
api_key = os.getenv("GEMINI_API_KEY") 
# Fallback for the specific key provided in prompt if not in env (For dev purpose only)
if not api_key:
    # This is a fallback. ideally user sets it in secrets.
    # The user explicitly provided this key in the prompt.
    api_key = "AIzaSyD2lZ_tnn39t6ZHEA8rUCi36FII6T_gxKc"

# Initialize the client with the API key
client = genai.Client(api_key=api_key) if api_key else None

def get_gemini_model():
    if not client:
        return None
    return client

def summarize_document(text):
    """Generates a summary for the provided text."""
    if not api_key:
        return "Error: API Key not configured."
    
    client = get_gemini_model()
    if not client:
        return "Error: Gemini client not initialized."
    
    prompt = f"""
    Provide a clear, comprehensive summary of the following document in bullet point format.
    
    Requirements:
    - Maximum 6 bullet points (exactly 6 or fewer)
    - Each bullet point must be on a new line
    - Cover all important information within these 6 points
    - Use bullet format: • or -
    - Be concise but comprehensive
    
    Focus on covering:
    - Main purpose or topic
    - Key information or processes
    - Important details, contacts, or decisions
    - Critical information that should be known
    
    Format: Each bullet point on a separate line. Maximum 6 points total.
    
    Document Content:
    {text[:30000]}  # Limit context window just in case
    
    Summary (exactly 6 bullet points maximum, each on a new line):
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error generating summary: {str(e)}"

def embed_text(text: str) -> list:
    """Generates an embedding for the given text using Gemini's text-embedding-004 model."""
    if not api_key:
        return []
    
    client = get_gemini_model()
    if not client:
        return []
    
    if not text or not text.strip():
        return []
    
    try:
        # Use text-embedding-004 model for embeddings (dimension: 768)
        # The google.genai API accepts contents as a list of strings directly
        response = client.models.embed_content(
            model="text-embedding-004",  # No "models/" prefix needed
            contents=[text]  # Pass list of strings directly
        )
        
        # Extract embedding from response
        # The response should have an embeddings attribute (plural) which is a list
        if response and hasattr(response, 'embeddings'):
            embeddings = response.embeddings
            if embeddings and len(embeddings) > 0:
                # Get the first embedding (since we only passed one text)
                embedding = embeddings[0]
                # Check if embedding has values attribute
                if hasattr(embedding, 'values'):
                    return list(embedding.values)
                # If embedding is directly a list/array
                elif isinstance(embedding, (list, tuple)):
                    return list(embedding)
                # If it's a single value, wrap in list
                else:
                    return [embedding]
        
        # Fallback: check for embedding (singular) attribute
        if response and hasattr(response, 'embedding'):
            embedding = response.embedding
            if hasattr(embedding, 'values'):
                return list(embedding.values)
            elif isinstance(embedding, (list, tuple)):
                return list(embedding)
            else:
                return [embedding]
        
        print(f"Warning: Unexpected embedding response format: {type(response)}")
        if hasattr(response, '__dict__'):
            print(f"Response attributes: {dir(response)}")
        return []
    except Exception as e:
        print(f"Error generating embedding: {e}")
        import traceback
        traceback.print_exc()
        return []

def chat_with_documents(query, context_text, history=[]):
    """Answers a query based on the provided context."""
    if not api_key:
        return "Error: API Key not configured."

    client = get_gemini_model()
    if not client:
        return "Error: Gemini client not initialized."
    
    # Construct prompt with context
    prompt = f"""
    You are a Knowledge Transfer (KT) assistant. Answer the user's question based ONLY on the provided document context.
    
    If the answer is not in the context, say: "This information is not available in the uploaded documents."
    Do not hallucinate facts.

    Context from uploaded documents:
    {context_text[:50000]} # Limit context
    
    User Question: {query}
    """
    
    # In a more advanced version, we would pass history to start_chat
    # For now, single turn with context is robust for RAG-lite
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error answering question: {str(e)}"
