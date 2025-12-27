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
                    # Create user without team (team will be assigned during login)
                    user = user_store.create_user(name, email, password, team_id=None)
                    st.success(f"Account created successfully! Welcome, {name}.")
                    st.info("You can now login with your email and password, and enter your team access code.")
                    st.balloons()
                    # Redirect to login
                    st.session_state.current_page = "login"
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))

def login_page():
    """Displays the login page with modern styling."""
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
