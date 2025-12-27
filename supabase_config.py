import os
from typing import TYPE_CHECKING, Optional, Any
from dotenv import load_dotenv

load_dotenv()

# Try to import Supabase
if TYPE_CHECKING:
    from supabase import Client

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    Client = None  # type: ignore
    print("Warning: supabase package not installed. Falling back to file-based storage.")

# Get environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
# Ensure URL has trailing slash to avoid storage endpoint warnings
if SUPABASE_URL and not SUPABASE_URL.endswith("/"):
    SUPABASE_URL = SUPABASE_URL + "/"
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# Initialize Supabase client
# Use string annotation to avoid NameError when Client is not available
supabase: Optional["Client"] = None  # type: ignore

if SUPABASE_AVAILABLE and SUPABASE_URL:
    # Prefer SUPABASE_KEY (anon/public key) over service role key for client-side operations
    key = SUPABASE_KEY or SUPABASE_SERVICE_ROLE_KEY
    if key:
        try:
            supabase = create_client(SUPABASE_URL, key)
            if SUPABASE_SERVICE_ROLE_KEY and not SUPABASE_KEY:
                print("Warning: Using SUPABASE_SERVICE_ROLE_KEY for client operations. Consider using SUPABASE_KEY (anon/public key) for better security.")
        except Exception as e:
            print(f"Warning: Failed to initialize Supabase client: {e}. Falling back to file-based storage.")
            supabase = None
    else:
        print("Warning: SUPABASE_URL is set but SUPABASE_KEY is not. Falling back to file-based storage.")
        supabase = None
else:
    if not SUPABASE_AVAILABLE:
        print("Warning: supabase package not available. Using file-based storage.")
    elif not SUPABASE_URL:
        print("Warning: SUPABASE_URL not set. Using file-based storage.")
    supabase = None

