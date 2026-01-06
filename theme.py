"""
Global theme styling for the Knowledge Transfer Hub application.
Applies a calm, modern, light theme with high contrast for accessibility.
"""
import streamlit as st

def apply_global_theme():
    """Applies global CSS theme to the entire Streamlit application."""
    
    st.markdown("""
    <style>
    /* ============================================
       GLOBAL THEME - Light, Calm, Modern, Accessible
       ============================================ */
    
    /* Remove default Streamlit styling */
    .stApp {
        background: #fafbfc !important;
    }
    
    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%) !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        background: transparent !important;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #1e293b !important;
    }
    
    [data-testid="stSidebar"] .stInfo {
        background: #f0f9ff !important;
        border: 1px solid #bfdbfe !important;
        border-radius: 12px !important;
        color: #1e40af !important;
    }
    
    /* Remove black backgrounds */
    .stApp > header {
        background-color: transparent !important;
    }
    
    #MainMenu {
        visibility: hidden;
    }
    
    footer {
        visibility: hidden;
    }
    
    header {
        visibility: hidden;
    }
    
    /* ============================================
       TYPOGRAPHY
       ============================================ */
    
    h1, h2, h3, h4, h5, h6 {
        color: #1e293b !important;
        font-weight: 600 !important;
    }
    
    p, div, span {
        color: #334155 !important;
    }
    
    /* Exception for ClearKT header colors */
    .clearkt-clear-span,
    span.clearkt-clear-span {
        color: #3b82f6 !important;
    }
    .clearkt-kt-span,
    span.clearkt-kt-span {
        color: #000000 !important;
    }
    
    /* ============================================
       BUTTONS - High Contrast, Accessible
       ============================================ */
    
    /* Primary buttons - High contrast blue */
    .stButton > button {
        background: #3b82f6 !important;
        background-color: #3b82f6 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.625rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4) !important;
        background: #2563eb !important;
        background-color: #2563eb !important;
    }
    
    /* Secondary buttons - High contrast outline */
    button[kind="secondary"] {
        background: #ffffff !important;
        background-color: #ffffff !important;
        color: #3b82f6 !important;
        border: 2px solid #3b82f6 !important;
        border-radius: 12px !important;
        padding: 0.625rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    button[kind="secondary"]:hover {
        background: #eff6ff !important;
        background-color: #eff6ff !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2) !important;
    }
    
    /* Form submit buttons - Ensure text visibility */
    .stForm button,
    .stForm .stButton > button,
    button[type="submit"] {
        background: #3b82f6 !important;
        background-color: #3b82f6 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.625rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3) !important;
    }
    
    .stForm button:hover,
    .stForm .stButton > button:hover,
    button[type="submit"]:hover {
        background: #2563eb !important;
        background-color: #2563eb !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Ensure all button text and child elements are visible */
    .stButton > button,
    .stForm button,
    button[type="submit"],
    button[kind="primary"],
    button[kind="secondary"],
    .stButton > button span,
    .stButton > button p,
    .stForm button span,
    .stForm button p {
        color: #ffffff !important;
    }
    
    button[kind="secondary"],
    button[kind="secondary"] span,
    button[kind="secondary"] p {
        color: #3b82f6 !important;
    }
    
    /* ============================================
       FORMS & INPUTS
       ============================================ */
    
    .stTextInput > div > div > input,
    .stTextInput > div > div > input:focus,
    input[type="text"],
    input[type="password"],
    input[type="email"] {
        background: #ffffff !important;
        background-color: #ffffff !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 10px !important;
        padding: 0.75rem 1rem !important;
        color: #1e293b !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    input[type="text"]:focus,
    input[type="password"]:focus,
    input[type="email"]:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
        outline: none !important;
    }
    
    /* Form containers */
    .stForm {
        background: #ffffff !important;
        background-color: #ffffff !important;
        padding: 2rem !important;
        border-radius: 16px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    /* File uploader - Light theme */
    [data-testid="stFileUploader"] {
        border: none !important;
        border-radius: 16px !important;
        padding: 2rem !important;
        background: #ffffff !important;
        background-color: #ffffff !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stFileUploader"]:hover {
        background: #f8fafc !important;
        background-color: #f8fafc !important;
    }
    
    /* File uploader button - High contrast */
    [data-testid="stFileUploader"] button,
    [data-testid="stFileUploader"] .stButton > button,
    [data-testid="stFileUploader"] [role="button"],
    [data-testid="stFileUploader"] button[type="button"] {
        background: #3b82f6 !important;
        background-color: #3b82f6 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.2s !important;
        cursor: pointer !important;
    }
    
    [data-testid="stFileUploader"] button:hover,
    [data-testid="stFileUploader"] .stButton > button:hover,
    [data-testid="stFileUploader"] [role="button"]:hover,
    [data-testid="stFileUploader"] button[type="button"]:hover {
        background: #2563eb !important;
        background-color: #2563eb !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 2px 4px rgba(59, 130, 246, 0.3) !important;
    }
    
    [data-testid="stFileUploader"] button *,
    [data-testid="stFileUploader"] button span,
    [data-testid="stFileUploader"] button p {
        color: #ffffff !important;
    }
    
    /* File uploader text - Light color */
    [data-testid="stFileUploader"] p,
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] div,
    [data-testid="stFileUploader"] label,
    [data-testid="stFileUploader"] * {
        color: #94a3b8 !important;
    }
    
    /* Keep button text white */
    [data-testid="stFileUploader"] button,
    [data-testid="stFileUploader"] button *,
    [data-testid="stFileUploader"] button span,
    [data-testid="stFileUploader"] button p {
        color: #ffffff !important;
    }
    
    /* ============================================
       CARDS & CONTAINERS
       ============================================ */
    
    .stExpander {
        background: #ffffff !important;
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
        margin-bottom: 1rem !important;
    }
    
    .stExpander:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
    }
    
    /* Keep expander background white always */
    .stExpander,
    [data-testid="stExpander"],
    .stExpander summary,
    [data-testid="stExpander"] summary {
        background: #ffffff !important;
        background-color: #ffffff !important;
    }
    
    /* Make expander text and arrow black */
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] summary div,
    [data-testid="stExpander"] summary span,
    [data-testid="stExpander"] summary * {
        color: #000000 !important;
    }
    
    /* Target the expander button/label area - black text */
    [data-testid="stExpander"] > div:first-child,
    [data-testid="stExpander"] > div:first-child p,
    [data-testid="stExpander"] > div:first-child div,
    [data-testid="stExpander"] > div:first-child span,
    [data-testid="stExpander"] > div:first-child * {
        color: #000000 !important;
    }
    
    /* Override any inline color styles to ensure black text */
    [data-testid="stExpander"] [style*="color: rgb(0, 0, 0)"],
    [data-testid="stExpander"] [style*="color:#000"],
    [data-testid="stExpander"] [style*="color: #000"],
    [data-testid="stExpander"] [style*="color:black"],
    [data-testid="stExpander"] [style*="color: black"],
    [data-testid="stExpander"] [style*="color: rgb(255, 255, 255)"],
    [data-testid="stExpander"] [style*="color:#fff"],
    [data-testid="stExpander"] [style*="color: #fff"],
    [data-testid="stExpander"] [style*="color:white"],
    [data-testid="stExpander"] [style*="color: white"] {
        color: #000000 !important;
    }
    
    /* Ensure expander text stays black in all states */
    .stExpander summary[aria-expanded="true"],
    .stExpander summary[aria-expanded="false"],
    [data-testid="stExpander"] summary[aria-expanded="true"],
    [data-testid="stExpander"] summary[aria-expanded="false"] {
        color: #000000 !important;
        background: #ffffff !important;
        background-color: #ffffff !important;
    }
    
    /* General rule for all text in expander headers - black */
    .stExpander summary,
    .stExpander summary *,
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary * {
        color: #000000 !important;
    }
    
    /* Make the expander arrow black */
    [data-testid="stExpander"] summary::marker,
    [data-testid="stExpander"] summary::-webkit-details-marker,
    .stExpander summary::marker,
    .stExpander summary::-webkit-details-marker {
        color: #000000 !important;
    }
    
    /* Info/Success/Error messages */
    .stAlert {
        border-radius: 12px !important;
        border-left: 4px solid !important;
        padding: 1rem 1.5rem !important;
    }
    
    .stSuccess {
        background: #f0fdf4 !important;
        background-color: #f0fdf4 !important;
        border-color: #22c55e !important;
        color: #166534 !important;
    }
    
    .stInfo {
        background: #f0f9ff !important;
        background-color: #f0f9ff !important;
        border-color: #3b82f6 !important;
        color: #1e40af !important;
    }
    
    .stError {
        background: #fef2f2 !important;
        background-color: #fef2f2 !important;
        border-color: #ef4444 !important;
        color: #991b1b !important;
    }
    
    .stWarning {
        background: #fffbeb !important;
        background-color: #fffbeb !important;
        border-color: #f59e0b !important;
        color: #92400e !important;
    }
    
    /* ============================================
       TABS
       ============================================ */
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem !important;
        background: transparent !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #ffffff !important;
        background-color: #ffffff !important;
        border-radius: 10px 10px 0 0 !important;
        padding: 0.75rem 1.5rem !important;
        border: 1px solid #e2e8f0 !important;
        color: #64748b !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: #eff6ff !important;
        background-color: #eff6ff !important;
        color: #3b82f6 !important;
        border-color: #3b82f6 !important;
        border-bottom: 2px solid #3b82f6 !important;
    }
    
    /* ============================================
       CHAT INTERFACE - Light Theme
       ============================================ */
    
    /* Chat messages container */
    .stChatMessage {
        background: #ffffff !important;
        background-color: #ffffff !important;
        border-radius: 16px !important;
        padding: 1rem 1.5rem !important;
        margin-bottom: 1rem !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
    }
    
    /* User messages - Soft accent background */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageUser"]) {
        background: #eff6ff !important;
        background-color: #eff6ff !important;
    }
    
    [data-testid="stChatMessageUser"] {
        background: #eff6ff !important;
        background-color: #eff6ff !important;
    }
    
    /* Assistant messages - White background */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAssistant"]) {
        background: #ffffff !important;
        background-color: #ffffff !important;
    }
    
    [data-testid="stChatMessageAssistant"] {
        background: #ffffff !important;
        background-color: #ffffff !important;
    }
    
    /* Chat input container - Light background */
    .stChatInputContainer,
    [data-testid="stChatInputContainer"],
    [data-testid="stChatInput"],
    div[data-baseweb="input"],
    div[data-baseweb="textarea"],
    div[class*="stChatInput"],
    div[class*="chat-input"],
    div[class*="ChatInput"] {
        background: #ffffff !important;
        background-color: #ffffff !important;
        border-radius: 16px !important;
        border: 2px solid #cbd5e1 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Target BaseWeb input wrapper */
    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div {
        background: transparent !important;
        background-color: transparent !important;
    }
    
    .stChatInputContainer:focus-within,
    [data-testid="stChatInputContainer"]:focus-within,
    [data-testid="stChatInput"]:focus-within,
    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="textarea"]:focus-within {
        border-color: #3b82f6 !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15) !important;
        background: #ffffff !important;
        background-color: #ffffff !important;
    }
    
    /* Chat input text area */
    .stChatInputContainer textarea,
    .stChatInputContainer input[type="text"],
    .stChatInputContainer input,
    [data-testid="stChatInputContainer"] textarea,
    [data-testid="stChatInputContainer"] input,
    [data-testid="stChatInput"] textarea,
    [data-testid="stChatInput"] input,
    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea,
    div[data-baseweb="input"] textarea,
    textarea[placeholder],
    input[placeholder] {
        background: transparent !important;
        background-color: transparent !important;
        color: #1e293b !important;
        border: none !important;
        padding: 1rem 1.25rem !important;
        font-size: 1rem !important;
        line-height: 1.5 !important;
    }
    
    .stChatInputContainer textarea::placeholder,
    .stChatInputContainer input[type="text"]::placeholder,
    .stChatInputContainer input::placeholder,
    [data-testid="stChatInputContainer"] textarea::placeholder,
    [data-testid="stChatInputContainer"] input::placeholder,
    [data-testid="stChatInput"] textarea::placeholder,
    [data-testid="stChatInput"] input::placeholder,
    div[data-baseweb="input"] input::placeholder,
    div[data-baseweb="textarea"] textarea::placeholder,
    textarea[placeholder]::placeholder,
    input[placeholder]::placeholder {
        color: #94a3b8 !important;
    }
    
    .stChatInputContainer textarea:focus,
    .stChatInputContainer input[type="text"]:focus,
    .stChatInputContainer input:focus,
    [data-testid="stChatInputContainer"] textarea:focus,
    [data-testid="stChatInputContainer"] input:focus,
    [data-testid="stChatInput"] textarea:focus,
    [data-testid="stChatInput"] input:focus,
    div[data-baseweb="input"] input:focus,
    div[data-baseweb="textarea"] textarea:focus {
        outline: none !important;
        border: none !important;
        box-shadow: none !important;
        background: transparent !important;
        background-color: transparent !important;
    }
    
    /* Chat input send button - High contrast */
    .stChatInputContainer button,
    [data-testid="stChatInputContainer"] button,
    [data-testid="stChatInput"] button,
    div[data-baseweb="input"] button,
    div[data-baseweb="textarea"] button,
    button[aria-label*="Send"],
    button[aria-label*="send"] {
        background: #3b82f6 !important;
        background-color: #3b82f6 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stChatInputContainer button:hover,
    [data-testid="stChatInputContainer"] button:hover,
    [data-testid="stChatInput"] button:hover,
    div[data-baseweb="input"] button:hover,
    div[data-baseweb="textarea"] button:hover,
    button[aria-label*="Send"]:hover,
    button[aria-label*="send"]:hover {
        background: #2563eb !important;
        background-color: #2563eb !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3) !important;
    }
    
    /* Override any dark backgrounds */
    *[style*="background-color: rgb(30, 41, 59)"],
    *[style*="background-color:#1e293b"],
    *[style*="background-color: #1e293b"],
    *[style*="background: rgb(30, 41, 59)"],
    *[style*="background:#1e293b"],
    *[style*="background: #1e293b"] {
        background: #ffffff !important;
        background-color: #ffffff !important;
    }
    
    /* ============================================
       SPINNER & LOADING
       ============================================ */
    
    .stSpinner > div {
        border-color: #3b82f6 !important;
    }
    
    /* ============================================
       SIDEBAR BUTTONS
       ============================================ */
    
    [data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
        margin-top: 1rem !important;
    }
    
    /* ============================================
       SCROLLBAR STYLING
       ============================================ */
    
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
    
    </style>
    """, unsafe_allow_html=True)

