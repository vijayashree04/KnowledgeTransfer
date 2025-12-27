import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Now import modules that depend on environment variables
import auth
import document_store
import gemini_utils
import team_store
import user_store
import landing_page
import theme

# Page Config
st.set_page_config(
    page_title="Knowledge Transfer Hub",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="auto"
)

# Apply global theme
theme.apply_global_theme()

# Navigation logic - use session state
if "current_page" not in st.session_state:
    st.session_state.current_page = "landing"

# Check authentication
is_authenticated = auth.check_auth()

# Route to appropriate page
if not is_authenticated:
    if st.session_state.current_page == "signup":
        auth.signup_page()
    elif st.session_state.current_page == "login":
        auth.login_page()
    else:
        landing_page.show_landing_page()
else:
    # Sidebar
    user_name = st.session_state.get("name", st.session_state.get("email", "User"))
    st.sidebar.title(f"Welcome, {user_name}")
    if "team_name" in st.session_state:
        st.sidebar.info(f"🏢 Team: {st.session_state.team_name}")
    if st.sidebar.button("Logout", type="secondary"):
        auth.logout()
    
    # Welcome message banner at the top
    user_name = st.session_state.get("name", st.session_state.get("email", "User"))
    team_name = st.session_state.get("team_name", "your team")
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; border-left: 4px solid #3b82f6;'>
        <h2 style='color: #1e293b; margin: 0 0 0.5rem 0; font-size: 1.75rem; font-weight: 600;'>
            👋 Welcome back, {user_name}!
        </h2>
        <p style='color: #475569; margin: 0; font-size: 1.1rem;'>
            Ready to explore your team's knowledge base? Upload documents, view summaries, or chat with the AI assistant.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Logout button in the main area (top right)
    col_title, col_logout = st.columns([4, 1])
    with col_title:
        st.title("📚 Centralized Knowledge Transfer Hub")
        if "team_name" in st.session_state:
            st.caption(f"Team: {st.session_state.team_name}")
    with col_logout:
        st.markdown("<br>", unsafe_allow_html=True)  # Add some spacing
        if st.button("🚪 Logout", type="secondary", use_container_width=True):
            auth.logout()
    
    # Check if user is team lead
    import team_store
    team_id = st.session_state.get("team_id")
    user_email = st.session_state.get("email", "")
    is_lead = st.session_state.get("is_team_lead", False)
    if not is_lead and team_id:
        is_lead = team_store.is_team_lead(team_id, user_email)
    
    # Tabs - add Team Settings if user is team lead
    if is_lead:
        tab1, tab2, tab3, tab4 = st.tabs(["📤 Upload Documents", "📝 Document Summaries", "🤖 KT Chatbot", "⚙️ Team Settings"])
    else:
        tab1, tab2, tab3 = st.tabs(["📤 Upload Documents", "📝 Document Summaries", "🤖 KT Chatbot"])

    # Tab 1: Upload
    with tab1:
        # Header section
        st.markdown("""
        <div style='margin-bottom: 2.5rem; text-align: center;'>
            <p style='color: #1e293b; margin: 0; font-size: 1.5rem; font-weight: 500; line-height: 1.5;'>Add documents to your team's knowledge base</p>
        </div>
        """, unsafe_allow_html=True)
        
        # File uploader with hidden label
        uploaded_file = st.file_uploader(
            "Upload document",
            type=["txt", "md", "py", "js", "json", "pdf", "docx", "doc"],
            label_visibility="collapsed",
            
        )
        
        # Show file info and format info
        
        # Show file info and process button if file is uploaded
        if uploaded_file is not None:
            st.markdown("<br>", unsafe_allow_html=True)


            
            # Process and Upload button - centered
            col1, col2, col3 = st.columns([1, 2.5, 1])
            with col2:
                if st.button("Process & Upload", type="primary", use_container_width=True):
                    with st.spinner("Uploading and Summarizing..."):
                        # Save File
                        team_id = st.session_state.get("team_id")
                        user_email = st.session_state.get("email", "unknown")
                        team_name = st.session_state.get("team_name")
                        metadata = document_store.save_uploaded_file(uploaded_file, user_email, team_id, team_name)
                        
                        # Success message
                        st.markdown("""
                        <div style='text-align: center; margin: 2rem 0;'>
                            <div style='display: inline-flex; align-items: center; gap: 0.5rem; background: #f0fdf4; padding: 0.75rem 1.5rem; border-radius: 8px; border-left: 4px solid #22c55e;'>
                                <span style='font-size: 1.2rem;'>✅</span>
                                <p style='margin: 0; color: #166534; font-weight: 500;'>Document uploaded successfully</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Generate Summary
                        summary = gemini_utils.summarize_document(metadata["content"])
                        document_store.update_document_summary(uploaded_file.name, summary, team_id)
                        
                        st.markdown("<br><br>", unsafe_allow_html=True)
                        
                        # Display summary - centered
                        st.markdown("""
                        <div style='text-align: center; margin: 2rem 0;'>
                            <h3 style='color: #1e293b; margin-bottom: 1.5rem;'>📋 Document Summary</h3>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if summary.strip():
                            # Format summary as bullet points
                            formatted_summary = summary.strip()
                            lines = formatted_summary.split('\n')
                            bullet_lines = []
                            
                            for line in lines:
                                line = line.strip()
                                if line:
                                    if line.startswith('-') or line.startswith('*') or line.startswith('·'):
                                        line = '•' + line[1:].lstrip()
                                    elif not line.startswith('•'):
                                        line = f"• {line}"
                                    bullet_lines.append(line)
                            
                            # Limit to maximum 6 bullet points
                            bullet_lines = bullet_lines[:6]
                            
                            # Display as markdown in a centered card
                            st.markdown(f"""
                            <div style='display: flex; justify-content: center;'>
                                <div style='background: #ffffff; padding: 2rem; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); text-align: left; max-width: 750px; width: 100%;'>
                                    {'<br>'.join(bullet_lines)}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.info("No summary available.")

    # Tab 2: Summaries
    with tab2:
        st.header("Document Repository")
        docs = document_store.get_documents(team_id)
        
        
        if not docs:
            st.info("No documents uploaded yet for your team.")
        else:
            st.info(f"Showing {len(docs)} document(s) for your team.")
            for doc in docs:
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    with st.expander(f"📄 {doc['filename']} (Uploaded by {doc['uploaded_by']} on {doc['upload_date']})"):
                        st.markdown("### Summary")
                        st.write(doc.get("summary") or "No summary available.")
                        st.markdown("---")
                        st.markdown("### Content Preview")
                        st.text(doc.get("content", "")[:500] + "...")
                
                with col2:
                    if is_lead:
                        if st.button("🗑️ Delete", key=f"delete_{doc['filename']}", type="secondary"):
                            if document_store.delete_document(doc['filename'], team_id):
                                st.success(f"Document '{doc['filename']}' deleted successfully!")
                                st.rerun()
                            else:
                                st.error("Failed to delete document.")

    # Tab 3: Chatbot
    with tab3:
        st.header("Ask the Knowledge Base")
        
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat Input
        if prompt := st.chat_input("Ask any questions related to your project here"):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Generating response..."):
                    team_id = st.session_state.get("team_id")
                    team_name = st.session_state.get("team_name")
                    # Use Pinecone vector search for relevant context
                    context = document_store.get_context_for_query(prompt, team_id, team_name)
                    response = gemini_utils.chat_with_documents(prompt, context)
                    st.markdown(response)
            
            # Add assistant message
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Tab 4: Team Settings (only for team leads)
    if is_lead:
        with tab4:
            st.header("⚙️ Team Settings")
            st.info("👑 As the Team Lead, you can manage team settings here.")
            
            # Get current team info
            team = team_store.get_team_by_id(team_id) if team_id else None
            
            if team:
                st.markdown("### Current Team Information")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Team Name:** {team.get('name', 'N/A')}")
                    st.write(f"**Access Code:** {team.get('access_code', 'N/A')}")
                with col2:
                    current_lead = team.get('team_lead_email', 'Not assigned')
                    st.write(f"**Current Team Lead:** {current_lead}")
                    st.write(f"**Team Created:** {team.get('created_at', 'N/A')}")
                
                st.markdown("---")
                st.markdown("### Update Team Lead")
                st.caption("Assign a new team lead by entering their email address.")
                
                with st.form("update_team_lead_form"):
                    new_lead_email = st.text_input(
                        "New Team Lead Email",
                        placeholder="Enter the email of the new team lead",
                        help="The new team lead must be a member of this team"
                    )
                    submit_update = st.form_submit_button("Update Team Lead", type="primary")
                    
                    if submit_update:
                        if not new_lead_email:
                            st.error("Please enter an email address.")
                        elif not user_store.validate_email(new_lead_email):
                            st.error("Please enter a valid email address.")
                        else:
                            # Check if the email belongs to a user in this team
                            new_lead_user = user_store.get_user_by_email(new_lead_email)
                            if not new_lead_user:
                                st.error(f"No user found with email '{new_lead_email}'. They must sign up first.")
                            elif new_lead_user.get("team_id") != team_id:
                                st.error(f"This user belongs to a different team.")
                            else:
                                # Update team lead
                                if team_store.update_team_lead(team_id, new_lead_email):
                                    st.success(f"Team lead updated successfully! New team lead: {new_lead_email}")
                                    st.info("The new team lead will have full access after they log out and log back in.")
                                    # Update session state if updating to current user
                                    if new_lead_email.lower() == user_email.lower():
                                        st.session_state.is_team_lead = True
                                    else:
                                        st.session_state.is_team_lead = False
                                        st.warning("You are no longer the team lead. Please refresh the page.")
                                    st.rerun()
                                else:
                                    st.error("Failed to update team lead.")
            else:
                st.error("Team information not found.")
