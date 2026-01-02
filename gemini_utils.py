from google.genai import types
import google.genai as genai
import os
import streamlit as st
from dotenv import load_dotenv
from pathlib import Path
import time
import re

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

def _is_code_file(text: str, filename: str = "") -> bool:
    """Detects if the content is code based on file extension or content patterns."""
    code_extensions = ['.py', '.js', '.java', '.cpp', '.c', '.cs', '.go', '.rs', '.rb', '.php', '.swift', '.kt', '.ts', '.tsx', '.jsx']
    if filename:
        return any(filename.lower().endswith(ext) for ext in code_extensions)
    
    # Check for code patterns
    code_patterns = ['def ', 'function ', 'class ', 'import ', 'from ', 'public class', 'function(', 'const ', 'let ', 'var ']
    lines = text.split('\n')[:50]  # Check first 50 lines
    code_line_count = sum(1 for line in lines if any(pattern in line for pattern in code_patterns))
    return code_line_count > 5  # If more than 5 lines have code patterns, likely code

def _generate_with_fallback_models(client, prompt, primary_model="gemini-2.5-flash"):
    """Generates content with automatic fallback to alternative models if quota is exceeded."""
    # List of models to try in order (primary first, then alternatives)
    models_to_try = [
        primary_model,
        "gemini-2.5-pro",
        "gemini-2.5-flash-lite",
        "gemini-3-pro-preview",
    ]
    
    last_error = None
    
    for i, model_name in enumerate(models_to_try):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            return response.text.strip(), model_name
        except Exception as e:
            error_msg = str(e)
            last_error = e
            
            # Check if it's a quota error (429)
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg or "quota" in error_msg.lower():
                # If not the last model, try the next one
                if i < len(models_to_try) - 1:
                    continue
                else:
                    # All models exhausted - try to extract retry delay and wait
                    retry_match = re.search(r'retry in ([\d.]+)s', error_msg, re.IGNORECASE)
                    if retry_match:
                        retry_seconds = float(retry_match.group(1))
                        time.sleep(min(retry_seconds, 60))
                        # Try the last model one more time after waiting
                        try:
                            response = client.models.generate_content(
                                model=model_name,
                                contents=prompt
                            )
                            return response.text.strip(), model_name
                        except:
                            pass
                    
                    # All models exhausted
                    raise ValueError(f"All Gemini models have exceeded quota. Please wait or upgrade your plan.")
            else:
                # For non-quota errors, raise immediately
                raise
    
    # If we get here, all models failed
    raise last_error if last_error else ValueError("Failed to generate content with any model")

def summarize_document_short(text, filename: str = ""):
    """Generates a short, sweet overview summary (for upload tab)."""
    api_key = get_api_key()
    if not api_key:
        return "Error: API Key not configured. Please set GEMINI_API_KEY in your .env file."
    
    client = get_gemini_model()
    if not client:
        return "Error: Gemini client not initialized. Please check your API key."
    
    is_code = _is_code_file(text, filename)
    
    if is_code:
        prompt = f"""
        Provide a brief, concise overview of what this code does. Keep it short and sweet.
        
        Requirements:
        - Maximum 4-6 bullet points
        - Each bullet point on a new line
        - Focus on: what the code is about, main purpose, key functionality
        - Use bullet format: • or -
        - Be brief and to the point
        - Return ONLY the bullet points, no introductory text
        
        Code Content:
        {text[:30000]}
        
        Return only the bullet points, starting immediately:
        """
    else:
        prompt = f"""
        Provide a brief, concise overview of this document. Keep it short and sweet.
        
        Requirements:
        - Maximum 4-6 bullet points
        - Each bullet point on a new line
        - Cover the main purpose and key points only
        - Use bullet format: • or -
        - Be brief and to the point
        - Return ONLY the bullet points, no introductory text
        
        Document Content:
        {text[:30000]}
        
        Return only the bullet points, starting immediately:
        """
    
    try:
        summary_text, used_model = _generate_with_fallback_models(client, prompt, "gemini-2.5-flash")
        
        # Remove common introductory phrases
        intro_phrases = [
            "here is your summary", "here's your summary", "here is the summary", "here's the summary",
            "summary:", "summary", "document summary:", "document summary",
            "the summary is:", "the summary:", "overview:", "overview"
        ]
        
        for phrase in intro_phrases:
            if summary_text.lower().startswith(phrase.lower()):
                summary_text = summary_text[len(phrase):].strip()
                if summary_text.startswith(':'):
                    summary_text = summary_text[1:].strip()
        
        return summary_text
    except Exception as e:
        error_msg = str(e)
        if "API key" in error_msg or "INVALID_ARGUMENT" in error_msg or "API_KEY" in error_msg:
            return "⚠️ **API Key Error**: Your Gemini API key has expired or is invalid. Please update your `GEMINI_API_KEY` in the `.env` file with a valid key from [Google AI Studio](https://aistudio.google.com/app/apikey)."
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg or "quota" in error_msg.lower():
            return "⚠️ **Quota Exceeded**: All Gemini models have exceeded their daily quota (20 requests/day for free tier). Please wait for the quota to reset or upgrade to a paid plan at [Google AI Studio](https://aistudio.google.com/app/apikey)."
        return f"Error generating summary: {error_msg}"

def summarize_document_detailed(text, filename: str = ""):
    """Generates a comprehensive, detailed summary with headings (for document summaries tab)."""
    api_key = get_api_key()
    if not api_key:
        return "Error: API Key not configured. Please set GEMINI_API_KEY in your .env file."
    
    client = get_gemini_model()
    if not client:
        return "Error: Gemini client not initialized. Please check your API key."
    
    is_code = _is_code_file(text, filename)
    
    if is_code:
        prompt = f"""
        Provide a comprehensive, detailed explanation of this code. Use markdown formatting with bold headings.
        
        Requirements:
        - Use **bold headings** for major sections (e.g., **Overview**, **Key Functions**, **Main Logic**, etc.)
        - Cover ALL important aspects: what the code does, how it works, key functions/classes, data flow, important algorithms
        - Explain the code in detail with clear explanations
        - Include an overview section explaining what the code is about
        - Break down complex logic and explain step by step
        - Use bullet points under each heading for clarity
        - Be thorough and comprehensive - cover everything important
        - Return ONLY the formatted content, no introductory text
        
        Code Content:
        {text[:30000]}
        
        Format your response with bold headings and detailed explanations:
        """
    else:
        prompt = f"""
        Provide a comprehensive, detailed summary of this document. Use markdown formatting with bold headings.
        
        Requirements:
        - Use **bold headings** for major topics/sections (e.g., **Main Topic**, **Key Concepts**, **Important Details**, etc.)
        - Cover ALL important information from the entire document
        - Break down into logical sections with clear headings
        - Include all key points, processes, decisions, contacts, dates, and critical information
        - Use bullet points under each heading for clarity
        - Be thorough and comprehensive - cover everything important
        - Return ONLY the formatted content, no introductory text
        
        Document Content:
        {text[:30000]}
        
        Format your response with bold headings and detailed explanations:
        """
    
    try:
        summary_text, used_model = _generate_with_fallback_models(client, prompt, "gemini-2.5-flash")
        
        # Remove common introductory phrases
        intro_phrases = [
            "here is your summary", "here's your summary", "here is the summary", "here's the summary",
            "summary:", "summary", "document summary:", "document summary",
            "the summary is:", "the summary:", "detailed summary:", "detailed summary"
        ]
        
        for phrase in intro_phrases:
            if summary_text.lower().startswith(phrase.lower()):
                summary_text = summary_text[len(phrase):].strip()
                if summary_text.startswith(':'):
                    summary_text = summary_text[1:].strip()
        
        return summary_text
    except Exception as e:
        error_msg = str(e)
        if "API key" in error_msg or "INVALID_ARGUMENT" in error_msg or "API_KEY" in error_msg:
            return "⚠️ **API Key Error**: Your Gemini API key has expired or is invalid. Please update your `GEMINI_API_KEY` in the `.env` file with a valid key from [Google AI Studio](https://aistudio.google.com/app/apikey)."
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg or "quota" in error_msg.lower():
            return "⚠️ **Quota Exceeded**: All Gemini models have exceeded their daily quota (20 requests/day for free tier). Please wait for the quota to reset or upgrade to a paid plan at [Google AI Studio](https://aistudio.google.com/app/apikey)."
        return f"Error generating summary: {error_msg}"

def summarize_document(text):
    """Legacy function - generates a short summary (for backward compatibility)."""
    return summarize_document_short(text)

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
        response_text, used_model = _generate_with_fallback_models(client, prompt, "gemini-2.5-flash")
        return response_text
    except Exception as e:
        error_msg = str(e)
        # Check for API key errors
        if "API key" in error_msg or "INVALID_ARGUMENT" in error_msg or "API_KEY" in error_msg:
            return "⚠️ **API Key Error**: Your Gemini API key has expired or is invalid. Please update your `GEMINI_API_KEY` in the `.env` file with a valid key from [Google AI Studio](https://aistudio.google.com/app/apikey)."
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg or "quota" in error_msg.lower():
            return "⚠️ **Quota Exceeded**: All Gemini models have exceeded their daily quota (20 requests/day for free tier). Please wait for the quota to reset or upgrade to a paid plan at [Google AI Studio](https://aistudio.google.com/app/apikey)."
        return f"Error answering question: {error_msg}"
