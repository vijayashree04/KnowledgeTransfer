import os
from datetime import datetime
from typing import Optional, Dict
from supabase_config import supabase
from uuid import uuid4

def _check_supabase():
    """Checks if Supabase is configured."""
    if supabase is None:
        raise ValueError("Supabase is not configured. Please set SUPABASE_URL and SUPABASE_KEY environment variables.")

def get_teams() -> list:
    """Retrieves all teams from Supabase."""
    _check_supabase()
    
    try:
        result = supabase.table("teams").select("*").execute()
        if result.data:
            return result.data
        return []
    except Exception as e:
        raise ValueError(f"Failed to get teams: {str(e)}")

def get_team_by_access_code(access_code: str) -> Optional[Dict]:
    """Gets a team by its access code."""
    _check_supabase()
    
    try:
        result = supabase.table("teams").select("*").eq("access_code", access_code).execute()
        if result.data and len(result.data) > 0:
            return result.data[0]
        return None
    except Exception as e:
        raise ValueError(f"Failed to get team by access code: {str(e)}")

def get_team_by_id(team_id: str) -> Optional[Dict]:
    """Gets a team by its ID."""
    _check_supabase()
    
    try:
        result = supabase.table("teams").select("*").eq("id", team_id).execute()
        if result.data and len(result.data) > 0:
            return result.data[0]
        return None
    except Exception as e:
        raise ValueError(f"Failed to get team by ID: {str(e)}")

def create_team(name: str, access_code: str, team_lead_email: Optional[str] = None) -> Dict:
    """Creates a new team in Supabase."""
    _check_supabase()
    
    # Check if access code already exists
    existing_team = get_team_by_access_code(access_code)
    if existing_team:
        raise ValueError(f"Access code '{access_code}' already exists")
    
    # Generate UUID for team ID
    team_id = str(uuid4())
    
    try:
        result = supabase.table("teams").insert({
            "id": team_id,
            "name": name,
            "access_code": access_code,
            "team_lead_email": team_lead_email
        }).execute()
        
        if result.data and len(result.data) > 0:
            return result.data[0]
        else:
            raise ValueError("Failed to create team in Supabase.")
    except Exception as e:
        raise ValueError(f"Failed to create team: {str(e)}")

def validate_access_code(access_code: str) -> Optional[Dict]:
    """Validates an access code and returns the team if valid."""
    return get_team_by_access_code(access_code)

def is_team_lead(team_id: str, user_email: str) -> bool:
    """Checks if a user is the team lead for a given team."""
    _check_supabase()
    
    try:
        result = supabase.table("teams").select("team_lead_email").eq("id", team_id).execute()
        if result.data and len(result.data) > 0:
            team_lead_email = result.data[0].get("team_lead_email")
            return team_lead_email and team_lead_email.lower() == user_email.lower()
        return False
    except Exception as e:
        raise ValueError(f"Failed to check team lead status: {str(e)}")

def update_team_lead(team_id: str, team_lead_email: str) -> bool:
    """Updates the team lead for a team."""
    _check_supabase()
    
    try:
        result = supabase.table("teams").update({"team_lead_email": team_lead_email}).eq("id", team_id).execute()
        return result.data is not None and len(result.data) > 0
    except Exception as e:
        raise ValueError(f"Failed to update team lead: {str(e)}")
