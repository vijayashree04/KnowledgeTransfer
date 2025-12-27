"""
Script to check and clean up users from both Supabase and local storage.
"""
import os
import json
from supabase_config import supabase

def check_local_users():
    """Check users in local users.json file"""
    users_file = "users.json"
    if os.path.exists(users_file):
        with open(users_file, "r") as f:
            users = json.load(f)
        print(f"Local users.json: {len(users)} user(s)")
        for user in users:
            print(f"  - {user.get('email', 'No email')} (ID: {user.get('id', 'No ID')})")
        return users
    else:
        print("Local users.json: File does not exist")
        return []

def check_supabase_users():
    """Check users in Supabase"""
    if supabase is None:
        print("Supabase: Not configured")
        return []
    
    try:
        result = supabase.table("users").select("*").execute()
        if result.data:
            print(f"Supabase users: {len(result.data)} user(s)")
            for user in result.data:
                print(f"  - {user.get('email', 'No email')} (ID: {user.get('id', 'No ID')})")
            return result.data
        else:
            print("Supabase users: No users found")
            return []
    except Exception as e:
        print(f"Supabase: Error checking users - {e}")
        return []

def delete_user_by_email(email: str):
    """Delete user by email from both Supabase and local storage"""
    print(f"\nAttempting to delete user: {email}")
    
    # Delete from Supabase
    if supabase is not None:
        try:
            result = supabase.table("users").delete().eq("email", email).execute()
            if result.data:
                print(f"✓ Deleted from Supabase: {email}")
            else:
                print(f"  No user found in Supabase with email: {email}")
        except Exception as e:
            print(f"✗ Error deleting from Supabase: {e}")
    
    # Delete from local storage
    users_file = "users.json"
    if os.path.exists(users_file):
        try:
            with open(users_file, "r") as f:
                users = json.load(f)
            
            original_count = len(users)
            users = [u for u in users if u.get("email") != email]
            
            if len(users) < original_count:
                with open(users_file, "w") as f:
                    json.dump(users, f, indent=2)
                print(f"✓ Deleted from local storage: {email}")
            else:
                print(f"  No user found in local storage with email: {email}")
        except Exception as e:
            print(f"✗ Error deleting from local storage: {e}")

def clear_all_users():
    """Clear all users from both Supabase and local storage"""
    print("\n⚠️  WARNING: This will delete ALL users!")
    response = input("Are you sure? Type 'yes' to confirm: ")
    
    if response.lower() != 'yes':
        print("Cancelled.")
        return
    
    # Clear Supabase
    if supabase is not None:
        try:
            # Get all users first
            result = supabase.table("users").select("id").execute()
            if result.data:
                user_ids = [u["id"] for u in result.data]
                for user_id in user_ids:
                    supabase.table("users").delete().eq("id", user_id).execute()
                print(f"✓ Deleted {len(user_ids)} user(s) from Supabase")
            else:
                print("  No users in Supabase to delete")
        except Exception as e:
            print(f"✗ Error clearing Supabase users: {e}")
    
    # Clear local storage
    users_file = "users.json"
    if os.path.exists(users_file):
        try:
            with open(users_file, "w") as f:
                json.dump([], f)
            print("✓ Cleared local users.json")
        except Exception as e:
            print(f"✗ Error clearing local storage: {e}")

def main():
    print("=" * 60)
    print("User Management - Check and Clean")
    print("=" * 60)
    
    print("\n1. Checking local users...")
    local_users = check_local_users()
    
    print("\n2. Checking Supabase users...")
    supabase_users = check_supabase_users()
    
    print("\n" + "=" * 60)
    print("Options:")
    print("1. Delete a specific user by email")
    print("2. Clear ALL users (from both Supabase and local)")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        email = input("Enter email to delete: ").strip()
        if email:
            delete_user_by_email(email)
    elif choice == "2":
        clear_all_users()
    else:
        print("Exiting...")

if __name__ == "__main__":
    main()

