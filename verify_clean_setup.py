"""
Quick script to verify that Supabase and local storage are clean for fresh setup.
"""
import os
import json
from supabase_config import supabase

print("=" * 60)
print("Verifying Clean Setup")
print("=" * 60)

# Check local users.json
print("\n1. Local users.json:")
if os.path.exists("users.json"):
    with open("users.json", "r") as f:
        users = json.load(f)
    if users:
        print(f"   ⚠️  Found {len(users)} user(s) in local storage")
        for user in users:
            print(f"      - {user.get('email', 'No email')}")
    else:
        print("   ✓ Empty (ready for new users)")
else:
    print("   ✓ File does not exist (will be created automatically)")

# Check Supabase users
print("\n2. Supabase users:")
if supabase is None:
    print("   ⚠️  Supabase not configured")
else:
    try:
        result = supabase.table("users").select("email").execute()
        if result.data and len(result.data) > 0:
            print(f"   ⚠️  Found {len(result.data)} user(s) in Supabase")
            for user in result.data:
                print(f"      - {user.get('email', 'No email')}")
        else:
            print("   ✓ No users in Supabase (ready for new users)")
    except Exception as e:
        print(f"   ✗ Error checking Supabase: {e}")

# Check local teams.json
print("\n3. Local teams.json:")
if os.path.exists("teams.json"):
    with open("teams.json", "r") as f:
        teams = json.load(f)
    if teams:
        print(f"   ⚠️  Found {len(teams)} team(s) in local storage")
        for team in teams:
            print(f"      - {team.get('name', 'No name')} (Code: {team.get('access_code', 'No code')})")
    else:
        print("   ✓ Empty (ready for new teams)")
else:
    print("   ✓ File does not exist (will be created automatically)")

# Check Supabase teams
print("\n4. Supabase teams:")
if supabase is None:
    print("   ⚠️  Supabase not configured")
else:
    try:
        result = supabase.table("teams").select("name, access_code").execute()
        if result.data and len(result.data) > 0:
            print(f"   ⚠️  Found {len(result.data)} team(s) in Supabase")
            for team in result.data:
                print(f"      - {team.get('name', 'No name')} (Code: {team.get('access_code', 'No code')})")
        else:
            print("   ✓ No teams in Supabase (ready for new teams)")
    except Exception as e:
        print(f"   ✗ Error checking Supabase: {e}")

print("\n" + "=" * 60)
print("Summary:")
print("If you see any users or teams above, you may need to:")
print("1. Delete them from Supabase dashboard (SQL Editor)")
print("2. Clear local JSON files if needed")
print("=" * 60)

