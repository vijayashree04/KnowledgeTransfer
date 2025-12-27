import os
import json
import hashlib
import re
from datetime import datetime
from typing import Optional, Dict
from supabase_config import supabase
from uuid import uuid4

def hash_password(password: str) -> str:
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email: str) -> bool:
    """Validates an email address format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def _check_supabase():
    """Checks if Supabase is configured."""
    if supabase is None:
        raise ValueError("Supabase is not configured. Please set SUPABASE_URL and SUPABASE_KEY environment variables.")

def create_user(name: str, email: str, password: str, team_id: Optional[str] = None) -> Dict:
    """Creates a new user in Supabase."""
    _check_supabase()
    
    # Validate email
    if not validate_email(email):
        raise ValueError("Invalid email address format.")
    
    # Check if user already exists
    existing_user = get_user_by_email(email)
    if existing_user:
        raise ValueError("A user with this email already exists.")
    
    # Hash password
    password_hash = hash_password(password)
    
    # Generate UUID for user ID
    user_id = str(uuid4())
    
    try:
        result = supabase.table("users").insert({
            "id": user_id,
            "name": name,
            "email": email,
            "password_hash": password_hash,
            "team_id": team_id
        }).execute()
        
        if result.data and len(result.data) > 0:
            user_data = result.data[0]
            return {
                "id": user_data.get("id"),
                "name": user_data.get("name"),
                "email": user_data.get("email"),
                "team_id": user_data.get("team_id"),
                "created_at": user_data.get("created_at", "")
            }
        else:
            raise ValueError("Failed to create user in Supabase.")
    except Exception as e:
        raise ValueError(f"Failed to create user: {str(e)}")

def authenticate_user(email: str, password: str) -> Optional[Dict]:
    """Authenticates a user and returns user data if successful."""
    _check_supabase()
    
    password_hash = hash_password(password)
    
    try:
        result = supabase.table("users").select("*").eq("email", email).execute()
        if result.data and len(result.data) > 0:
            user_data = result.data[0]
            if user_data.get("password_hash") == password_hash:
                return {
                    "id": user_data.get("id"),
                    "name": user_data.get("name"),
                    "email": user_data.get("email"),
                    "team_id": user_data.get("team_id"),
                    "created_at": user_data.get("created_at", "")
                }
        return None
    except Exception as e:
        raise ValueError(f"Failed to authenticate user: {str(e)}")

def get_user_by_email(email: str) -> Optional[Dict]:
    """Gets a user by email address."""
    _check_supabase()
    
    try:
        result = supabase.table("users").select("*").eq("email", email).execute()
        if result.data and len(result.data) > 0:
            user_data = result.data[0]
            return {
                "id": user_data.get("id"),
                "name": user_data.get("name"),
                "email": user_data.get("email"),
                "team_id": user_data.get("team_id"),
                "created_at": user_data.get("created_at", "")
            }
        return None
    except Exception as e:
        raise ValueError(f"Failed to get user: {str(e)}")

def update_user_team(user_id: str, team_id: str) -> bool:
    """Updates a user's team assignment."""
    _check_supabase()
    
    try:
        result = supabase.table("users").update({"team_id": team_id}).eq("id", user_id).execute()
        return result.data is not None and len(result.data) > 0
    except Exception as e:
        raise ValueError(f"Failed to update user team: {str(e)}")

def generate_password_reset_token(email: str) -> Optional[str]:
    """Generates a password reset token for a user."""
    import secrets
    token = secrets.token_urlsafe(32)
    
    # Store token in file (simplified - in production, use Supabase table for tokens)
    tokens_file = "password_reset_tokens.json"
    tokens = {}
    if os.path.exists(tokens_file):
        with open(tokens_file, "r") as f:
            tokens = json.load(f)
    
    tokens[email] = {
        "token": token,
        "created_at": datetime.now().isoformat()
    }
    
    with open(tokens_file, "w") as f:
        json.dump(tokens, f, indent=2)
    
    return token

def verify_password_reset_token(email: str, token: str) -> bool:
    """Verifies a password reset token."""
    tokens_file = "password_reset_tokens.json"
    if not os.path.exists(tokens_file):
        return False
    
    with open(tokens_file, "r") as f:
        tokens = json.load(f)
    
    if email in tokens:
        stored_token = tokens[email].get("token")
        if stored_token == token:
            return True
    return False

def reset_password(email: str, new_password: str) -> bool:
    """Resets a user's password."""
    _check_supabase()
    
    password_hash = hash_password(new_password)
    
    try:
        # Get user by email first
        user = get_user_by_email(email)
        if not user:
            return False
        
        result = supabase.table("users").update({"password_hash": password_hash}).eq("id", user["id"]).execute()
        
        if result.data:
            # Remove token after successful reset
            tokens_file = "password_reset_tokens.json"
            if os.path.exists(tokens_file):
                with open(tokens_file, "r") as f:
                    tokens = json.load(f)
                if email in tokens:
                    del tokens[email]
                    with open(tokens_file, "w") as f:
                        json.dump(tokens, f, indent=2)
            return True
        return False
    except Exception as e:
        raise ValueError(f"Failed to reset password: {str(e)}")
