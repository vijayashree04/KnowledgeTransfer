import streamlit as st

def show_landing_page():
    """Displays the landing page with hero section, features, and CTAs."""
    
    # Hero Section
    st.markdown("""
    <div style='text-align: center; padding: 4rem 2rem 3rem; background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border-radius: 20px; margin-bottom: 4rem;'>
        <h1 style='font-size: 3.5rem; font-weight: 700; color: #1e293b; margin: 0 0 1rem 0; letter-spacing: -0.02em;'>
            📚 Knowledge Transfer Hub
        </h1>
        <p style='font-size: 1.5rem; color: #475569; margin: 0 0 2.5rem 0; font-weight: 400;'>
            Centralized knowledge transfer for teams made simple
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA Buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Get Started", type="primary", use_container_width=True, key="get_started_btn"):
                st.session_state.current_page = "signup"
                st.rerun()
        with col_btn2:
            if st.button("Login", use_container_width=True, key="login_btn_landing"):
                st.session_state.current_page = "login"
                st.rerun()
    
    st.markdown("""
    <div style='margin-bottom: 4rem;'></div>
    """, unsafe_allow_html=True)
    
    # How It Works Section
    st.markdown("""
    <div style='margin: 4rem 0;'>
        <h2 style='text-align: center; font-size: 2.5rem; color: #1e293b; margin-bottom: 3rem; font-weight: 600;'>
            How It Works
        </h2>
        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin-top: 2rem;'>
            <div style='background: white; padding: 2rem; border-radius: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center; transition: transform 0.3s ease;'>
                <div style='font-size: 3rem; margin-bottom: 1rem;'>👥</div>
                <h3 style='color: #1e293b; font-size: 1.25rem; margin: 0 0 0.75rem 0; font-weight: 600;'>Create or Join Team</h3>
                <p style='color: #64748b; margin: 0; line-height: 1.6;'>Set up your team workspace with a simple access code</p>
            </div>
            <div style='background: white; padding: 2rem; border-radius: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center; transition: transform 0.3s ease;'>
                <div style='font-size: 3rem; margin-bottom: 1rem;'>📤</div>
                <h3 style='color: #1e293b; font-size: 1.25rem; margin: 0 0 0.75rem 0; font-weight: 600;'>Upload Documents</h3>
                <p style='color: #64748b; margin: 0; line-height: 1.6;'>Add your team's knowledge base documents in any format</p>
            </div>
            <div style='background: white; padding: 2rem; border-radius: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center; transition: transform 0.3s ease;'>
                <div style='font-size: 3rem; margin-bottom: 1rem;'>✨</div>
                <h3 style='color: #1e293b; font-size: 1.25rem; margin: 0 0 0.75rem 0; font-weight: 600;'>Auto-Generate Summaries</h3>
                <p style='color: #64748b; margin: 0; line-height: 1.6;'>AI-powered summaries for quick document understanding</p>
            </div>
            <div style='background: white; padding: 2rem; border-radius: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center; transition: transform 0.3s ease;'>
                <div style='font-size: 3rem; margin-bottom: 1rem;'>🤖</div>
                <h3 style='color: #1e293b; font-size: 1.25rem; margin: 0 0 0.75rem 0; font-weight: 600;'>Ask Questions</h3>
                <p style='color: #64748b; margin: 0; line-height: 1.6;'>Get instant answers using our intelligent KT Chatbot</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Why This App Section
    st.markdown("""
    <div style='margin: 4rem 0; padding: 3rem; background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); border-radius: 20px;'>
        <h2 style='text-align: center; font-size: 2.5rem; color: #1e293b; margin-bottom: 2.5rem; font-weight: 600;'>
            Why Knowledge Transfer Hub?
        </h2>
        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem;'>
            <div style='background: white; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #3b82f6;'>
                <h4 style='color: #1e293b; font-size: 1.1rem; margin: 0 0 0.5rem 0; font-weight: 600;'>⚡ Faster Onboarding</h4>
                <p style='color: #64748b; margin: 0; line-height: 1.6; font-size: 0.95rem;'>New team members get up to speed quickly with centralized knowledge</p>
            </div>
            <div style='background: white; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #3b82f6;'>
                <h4 style='color: #1e293b; font-size: 1.1rem; margin: 0 0 0.5rem 0; font-weight: 600;'>📚 Centralized Knowledge</h4>
                <p style='color: #64748b; margin: 0; line-height: 1.6; font-size: 0.95rem;'>All your team's documents in one accessible place</p>
            </div>
            <div style='background: white; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #3b82f6;'>
                <h4 style='color: #1e293b; font-size: 1.1rem; margin: 0 0 0.5rem 0; font-weight: 600;'>🤖 AI-Powered Summaries</h4>
                <p style='color: #64748b; margin: 0; line-height: 1.6; font-size: 0.95rem;'>Automatically generate concise summaries of your documents</p>
            </div>
            <div style='background: white; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #3b82f6;'>
                <h4 style='color: #1e293b; font-size: 1.1rem; margin: 0 0 0.5rem 0; font-weight: 600;'>💬 Instant Answers</h4>
                <p style='color: #64748b; margin: 0; line-height: 1.6; font-size: 0.95rem;'>Get answers to questions instantly via intelligent chatbot</p>
            </div>
            <div style='background: white; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #3b82f6;'>
                <h4 style='color: #1e293b; font-size: 1.1rem; margin: 0 0 0.5rem 0; font-weight: 600;'>👥 Team Independence</h4>
                <p style='color: #64748b; margin: 0; line-height: 1.6; font-size: 0.95rem;'>Reduce dependency on senior members for knowledge sharing</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Contact Section
    st.markdown("""
    <div style='text-align: center; margin: 4rem 0; padding: 3rem; background: white; border-radius: 20px; box-shadow: 0 4px 16px rgba(0,0,0,0.08);'>
        <h2 style='font-size: 2rem; color: #1e293b; margin: 0 0 1.5rem 0; font-weight: 600;'>Get in Touch</h2>
        <p style='color: #64748b; font-size: 1.1rem; margin: 0 0 0.5rem 0;'>Created by <strong style='color: #1e293b;'>Vijaya Shree</strong></p>
        <p style='color: #64748b; font-size: 1rem; margin: 0;'>
            <a href='mailto:vijayashree2k04@gmail.com' style='color: #3b82f6; text-decoration: none; font-weight: 500;'>vijayashree2k04@gmail.com</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

