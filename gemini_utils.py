from google.genai import types
import google.genai as genai
import os
import streamlit as st
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables (in case .env was updated)
# Try to find .env file in current directory or parent directories
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    # Fallback to default behavior
    load_dotenv()

def get_api_key():
    """Get API key from environment variable, reloading .env if needed."""
    # Reload .env each time to ensure we get the latest value
    # Try multiple locations for .env file
    env_locations = [
        Path(__file__).parent / ".env",  # Same directory as this file
        Path.cwd() / ".env",  # Current working directory
        Path.home() / ".env",  # Home directory (fallback)
    ]
    
    for env_path in env_locations:
        if env_path.exists():
            load_dotenv(dotenv_path=env_path, override=True)
            break
    else:
        # If no .env found, try default behavior
        load_dotenv(override=True)
    
    api_key = os.getenv("GEMINI_API_KEY")
    return api_key

def get_gemini_model():
    """Get or create Gemini client with current API key."""
    api_key = get_api_key()
    if not api_key:
        return None
    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")
        return None

def summarize_document(text):
    """Generates a summary for the provided text."""
    api_key = get_api_key()
    if not api_key:
        return "Error: API Key not configured. Please set GEMINI_API_KEY in your .env file."
    
    client = get_gemini_model()
    if not client:
        return "Error: Gemini client not initialized. Please check your API key."
    
    prompt = f"""
    Provide a clear, comprehensive summary of the following document in bullet point format.
    
    Requirements:
    - Maximum 6 bullet points (exactly 6 or fewer)
    - Each bullet point must be on a new line
    - Cover all important information within these 6 points
    - Use bullet format: • or -
    - Be concise but comprehensive
    - Return ONLY the bullet points, no introductory text, no phrases like "here is your summary" or "summary:"
    - Start directly with the first bullet point
    
    Focus on covering:
    - Main purpose or topic
    - Key information or processes
    - Important details, contacts, or decisions
    - Critical information that should be known
    
    Format: Each bullet point on a separate line. Maximum 6 points total.
    
    Document Content:
    {text[:30000]}  # Limit context window just in case
    
    Return only the bullet points, starting immediately with the first bullet point:
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        summary_text = response.text
        
        # Clean up the summary to remove any introductory phrases
        summary_text = summary_text.strip()
        
        # Remove common introductory phrases (case-insensitive)
        intro_phrases = [
            "here is your summary",
            "here's your summary",
            "here is the summary",
            "here's the summary",
            "summary:",
            "summary",
            "document summary:",
            "document summary",
            "the summary is:",
            "the summary:",
        ]
        
        for phrase in intro_phrases:
            # Remove phrase if it appears at the start (case-insensitive)
            if summary_text.lower().startswith(phrase.lower()):
                summary_text = summary_text[len(phrase):].strip()
                # Remove colon if present after the phrase
                if summary_text.startswith(':'):
                    summary_text = summary_text[1:].strip()
        
        return summary_text
    except Exception as e:
        error_msg = str(e)
        # Check for API key errors
        if "API key" in error_msg or "INVALID_ARGUMENT" in error_msg or "API_KEY" in error_msg:
            return "⚠️ **API Key Error**: Your Gemini API key has expired or is invalid. Please update your `GEMINI_API_KEY` in the `.env` file with a valid key from [Google AI Studio](https://aistudio.google.com/app/apikey)."
        return f"Error generating summary: {error_msg}"

def embed_text(text: str) -> list:
    """Generates an embedding for the given text using Gemini's text-embedding-004 model."""
    api_key = get_api_key()
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
        error_msg = str(e)
        # Check for API key errors
        if "API key" in error_msg or "INVALID_ARGUMENT" in error_msg or "API_KEY" in error_msg or "expired" in error_msg.lower():
            api_key = get_api_key()
            if api_key:
                # Key exists but is invalid/expired
                masked_key = f"{api_key[:10]}...{api_key[-4:]}" if len(api_key) > 14 else "***"
                print(f"⚠️ API Key Error: The key {masked_key} has expired or is invalid.")
            else:
                print("⚠️ API Key Error: GEMINI_API_KEY not found in environment.")
            print("   Please update your GEMINI_API_KEY in the .env file with a valid key from:")
            print("   https://aistudio.google.com/app/apikey")
            print(f"   Current working directory: {os.getcwd()}")
            # Don't print full traceback for API key errors
            return []
        else:
            print(f"Error generating embedding: {error_msg}")
            import traceback
            traceback.print_exc()
            return []

def chat_with_documents(query, context_text, history=[]):
    """Answers a query based on the provided context."""
    api_key = get_api_key()
    if not api_key:
        return "Error: API Key not configured. Please set GEMINI_API_KEY in your .env file."

    client = get_gemini_model()
    if not client:
        return "Error: Gemini client not initialized. Please check your API key."
    
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
        error_msg = str(e)
        # Check for API key errors
        if "API key" in error_msg or "INVALID_ARGUMENT" in error_msg or "API_KEY" in error_msg:
            return "⚠️ **API Key Error**: Your Gemini API key has expired or is invalid. Please update your `GEMINI_API_KEY` in the `.env` file with a valid key from [Google AI Studio](https://aistudio.google.com/app/apikey)."
        return f"Error answering question: {error_msg}"
