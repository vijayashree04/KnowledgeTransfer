import streamlit as st
import os
import team_store
import user_store

def check_auth():
    """Checks if the user is logged in."""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    return st.session_state.logged_in

def signup_page():
    """Displays the signup page with modern styling."""
    # Back to home link
    if st.button("← Back to Home", use_container_width=False, key="back_home_signup"):
        st.session_state.current_page = "landing"
        st.rerun()
    
    st.markdown("""
    <div style='text-align: center; margin-bottom: 3rem;'>
        <h1 style='font-size: 2.5rem; color: #1e293b; margin: 0 0 0.5rem 0; font-weight: 700;'>📝 Create Account</h1>
        <p style='color: #64748b; font-size: 1.1rem; margin: 0;'>Join your team and start sharing knowledge</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("signup_form"):
        name = st.text_input("Full Name", placeholder="Enter your full name")
        email = st.text_input("Email", placeholder="Enter your email address")
        password = st.text_input("Password", type="password", placeholder="Choose a password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password")
        submit = st.form_submit_button("Sign Up")

        if submit:
            # Validation
            if not name:
                st.error("Please enter your name.")
            elif not email:
                st.error("Please enter your email address.")
            elif not user_store.validate_email(email):
                st.error("Please enter a valid email address.")
            elif not password:
                st.error("Please enter a password.")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            else:
                try:
                    # Create user without team (team will be assigned during team creation or join)
                    user = user_store.create_user(name, email, password, team_id=None)
                    st.success(f"Account created successfully! Welcome, {name}.")
                    st.balloons()
                    # Store user info temporarily for team choice page
                    st.session_state.pending_user = {
                        "id": user["id"],
                        "name": user["name"],
                        "email": user["email"],
                        "password": password  # Store temporarily for auto-login after team setup
                    }
                    # Redirect to team choice page
                    st.session_state.current_page = "team_choice"
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))

def team_choice_page():
    """Displays the team choice page after signup - Create Team or Join Team."""
    # Back to home link
    if st.button("← Back to Home", use_container_width=False, key="back_home_team_choice"):
        st.session_state.current_page = "landing"
        if "pending_user" in st.session_state:
            del st.session_state.pending_user
        st.rerun()
    
    st.markdown("""
    <div style='text-align: center; margin-bottom: 3rem;'>
        <h1 style='font-size: 2.5rem; color: #1e293b; margin: 0 0 0.5rem 0; font-weight: 700;'>👥 Choose Your Path</h1>
        <p style='color: #64748b; font-size: 1.1rem; margin: 0;'>Create a new team or join an existing one</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if we have a pending user (from signup)
    if "pending_user" not in st.session_state:
        st.warning("No pending signup found. Please sign up first.")
        if st.button("Go to Sign Up"):
            st.session_state.current_page = "signup"
            st.rerun()
        return
    
    pending_user = st.session_state.pending_user
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='border: 2px solid #e2e8f0; border-radius: 12px; padding: 2rem; text-align: center; height: 100%;'>
            <h2 style='color: #1e293b; margin-bottom: 1rem;'>🏢 Create Team</h2>
            <p style='color: #64748b; margin-bottom: 1.5rem;'>Start a new team and become the team lead. You'll create an access code to share with your team members.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Create Team", key="create_team_btn", use_container_width=True, type="primary"):
            st.session_state.current_page = "create_team"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style='border: 2px solid #e2e8f0; border-radius: 12px; padding: 2rem; text-align: center; height: 100%;'>
            <h2 style='color: #1e293b; margin-bottom: 1rem;'>🔗 Join Team</h2>
            <p style='color: #64748b; margin-bottom: 1.5rem;'>Join an existing team using the access code provided by your team lead.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Join Team", key="join_team_btn", use_container_width=True, type="secondary"):
            st.session_state.current_page = "join_team"
            st.rerun()

def create_team_page():
    """Displays the create team page for team leads."""
    # Back button
    if st.button("← Back", use_container_width=False, key="back_create_team"):
        st.session_state.current_page = "team_choice"
        st.rerun()
    
    st.markdown("""
    <div style='text-align: center; margin-bottom: 3rem;'>
        <h1 style='font-size: 2.5rem; color: #1e293b; margin: 0 0 0.5rem 0; font-weight: 700;'>🏢 Create New Team</h1>
        <p style='color: #64748b; font-size: 1.1rem; margin: 0;'>Set up your team and get an access code to share</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if we have a pending user
    if "pending_user" not in st.session_state:
        st.warning("No pending signup found. Please sign up first.")
        if st.button("Go to Sign Up"):
            st.session_state.current_page = "signup"
            st.rerun()
        return
    
    pending_user = st.session_state.pending_user
    
    with st.form("create_team_form"):
        team_name = st.text_input("Team Name", placeholder="Enter your team name (e.g., Engineering Team)")
        access_code = st.text_input("Access Code", placeholder="Create a unique access code (e.g., ENG2024)", help="This code will be used by team members to join your team")
        
        st.info("💡 **Tip**: Choose a memorable access code that's easy to share with your team members. They'll need this code to join your team.")
        
        submit = st.form_submit_button("Create Team", type="primary")
        
        if submit:
            if not team_name:
                st.error("Please enter a team name.")
            elif not access_code:
                st.error("Please enter an access code.")
            elif len(access_code) < 4:
                st.error("Access code must be at least 4 characters long.")
            else:
                try:
                    # Create team with current user as team lead
                    team = team_store.create_team(
                        name=team_name,
                        access_code=access_code,
                        team_lead_email=pending_user["email"]
                    )
                    
                    # Assign user to the team
                    user_store.update_user_team(pending_user["id"], team["id"])
                    
                    # Auto-login the user
                    st.session_state.logged_in = True
                    st.session_state.user_id = pending_user["id"]
                    st.session_state.name = pending_user["name"]
                    st.session_state.email = pending_user["email"]
                    st.session_state.team_id = team["id"]
                    st.session_state.team_name = team["name"]
                    st.session_state.is_team_lead = True
                    st.session_state.access_code = access_code
                    
                    # Clear pending user and current page
                    del st.session_state.pending_user
                    if "current_page" in st.session_state:
                        del st.session_state.current_page
                    
                    st.success(f"✅ Team '{team_name}' created successfully!")
                    st.success(f"🔑 Your team access code is: **{access_code}**")
                    st.info("📋 Share this access code with your team members so they can join your team.")
                    st.balloons()
                    st.rerun()
                    
                except ValueError as e:
                    st.error(str(e))

def join_team_page():
    """Displays the join team page (login with access code)."""
    # Back button
    if st.button("← Back", use_container_width=False, key="back_join_team"):
        st.session_state.current_page = "team_choice"
        st.rerun()
    
    st.markdown("""
    <div style='text-align: center; margin-bottom: 3rem;'>
        <h1 style='font-size: 2.5rem; color: #1e293b; margin: 0 0 0.5rem 0; font-weight: 700;'>🔗 Join Team</h1>
        <p style='color: #64748b; font-size: 1.1rem; margin: 0;'>Enter your credentials and team access code</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if we have a pending user (from signup) or if this is a regular login
    pending_user = st.session_state.get("pending_user")
    
    with st.form("join_team_form"):
        if pending_user:
            # Pre-fill email if from signup
            email = st.text_input("Email", value=pending_user["email"], disabled=True)
            password = st.text_input("Password", type="password", placeholder="Enter your password")
        else:
            email = st.text_input("Email", placeholder="Enter your email address")
            password = st.text_input("Password", type="password")
        
        access_code = st.text_input("Team Access Code", placeholder="Enter your team's access code", help="Get this code from your team lead")
        submit = st.form_submit_button("Join Team", type="primary")

        if submit:
            if not email:
                st.error("Please enter your email address.")
            elif not user_store.validate_email(email):
                st.error("Please enter a valid email address.")
            elif not password:
                st.error("Please enter your password.")
            elif not access_code:
                st.error("Please enter your team access code.")
            else:
                # Validate access code
                team = team_store.validate_access_code(access_code)
                if not team:
                    st.error("Invalid access code. Please contact your team administrator.")
                else:
                    # Authenticate user
                    user = user_store.authenticate_user(email, password)
                    if user:
                        # If user doesn't have a team, assign them to this team
                        if user["team_id"] is None:
                            # Update user's team
                            user_store.update_user_team(user["id"], team["id"])
                            user["team_id"] = team["id"]
                        
                        # Verify user belongs to the team
                        if user["team_id"] != team["id"]:
                            st.error("Your account is not associated with this team.")
                        else:
                            # Check if user is team lead
                            is_team_lead = team_store.is_team_lead(team["id"], user["email"])
                            
                            st.session_state.logged_in = True
                            st.session_state.user_id = user["id"]
                            st.session_state.name = user["name"]
                            st.session_state.email = user["email"]
                            st.session_state.team_id = team["id"]
                            st.session_state.team_name = team["name"]
                            st.session_state.is_team_lead = is_team_lead
                            st.session_state.access_code = access_code
                            
                            # Clear pending user and current page
                            if "pending_user" in st.session_state:
                                del st.session_state.pending_user
                            if "current_page" in st.session_state:
                                del st.session_state.current_page
                            
                            st.success(f"✅ Successfully joined team '{team['name']}'!")
                            st.balloons()
                            st.rerun()
                    else:
                        st.error("Invalid email or password.")

def login_page():
    """Displays the login page with modern styling (for existing users)."""
    # Back to home link
    if st.button("← Back to Home", use_container_width=False, key="back_home_login"):
        st.session_state.current_page = "landing"
        st.rerun()
    
    st.markdown("""
    <div style='text-align: center; margin-bottom: 3rem;'>
        <h1 style='font-size: 2.5rem; color: #1e293b; margin: 0 0 0.5rem 0; font-weight: 700;'>🔐 Welcome Back</h1>
        <p style='color: #64748b; font-size: 1.1rem; margin: 0;'>Enter your credentials to access your team's knowledge base</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs for Login and Sign Up
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="Enter your email address")
            password = st.text_input("Password", type="password")
            access_code = st.text_input("Team Access Code", type="password", help="Enter your team's access code")
            submit = st.form_submit_button("Login", type="primary")

            if submit:
                if not email or not password:
                    st.error("Please enter email and password.")
                elif not user_store.validate_email(email):
                    st.error("Please enter a valid email address.")
                elif not access_code:
                    st.error("Please enter your team access code.")
                else:
                    # Validate access code
                    team = team_store.validate_access_code(access_code)
                    if not team:
                        st.error("Invalid access code. Please contact your team administrator.")
                    else:
                        # Authenticate user
                        user = user_store.authenticate_user(email, password)
                        if user:
                            # If user doesn't have a team, assign them to this team
                            if user["team_id"] is None:
                                # Update user's team
                                user_store.update_user_team(user["id"], team["id"])
                                user["team_id"] = team["id"]
                            
                            # Verify user belongs to the team
                            if user["team_id"] != team["id"]:
                                st.error("Your account is not associated with this team.")
                            else:
                                # Check if user is team lead
                                is_team_lead = team_store.is_team_lead(team["id"], user["email"])
                                
                                st.session_state.logged_in = True
                                st.session_state.user_id = user["id"]
                                st.session_state.name = user["name"]
                                st.session_state.email = user["email"]
                                st.session_state.team_id = team["id"]
                                st.session_state.team_name = team["name"]
                                st.session_state.is_team_lead = is_team_lead
                                st.session_state.access_code = access_code
                                # Clear current_page to show main app
                                if "current_page" in st.session_state:
                                    del st.session_state.current_page
                                st.rerun()
                        else:
                            st.error("Invalid email or password.")
    
    with tab2:
        signup_page()

def logout():
    """Logs the user out."""
    st.session_state.logged_in = False
    st.session_state.current_page = "landing"  # Return to landing page
    if "user_id" in st.session_state:
        del st.session_state.user_id
    if "name" in st.session_state:
        del st.session_state.name
    if "email" in st.session_state:
        del st.session_state.email
    if "team_id" in st.session_state:
        del st.session_state.team_id
    if "team_name" in st.session_state:
        del st.session_state.team_name
    if "is_team_lead" in st.session_state:
        del st.session_state.is_team_lead
    if "access_code" in st.session_state:
        del st.session_state.access_code
    st.rerun()
