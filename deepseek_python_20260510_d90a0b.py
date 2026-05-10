import streamlit as st
import time
import threading
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import database as db
import requests
import os

st.set_page_config(
    page_title="𝐘𝐀𝐌𝐑𝐀𝐉≛𝐃𝐄𝐕 | E2EE HACK SUITE",
    page_icon="💀",
    layout="wide",
    initial_sidebar_state="expanded"
)

custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
    
    /* HACKER THEME */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #0d0d0d 50%, #0a0a0a 100%);
    }
    
    * {
        font-family: 'Share Tech Mono', 'Courier New', monospace;
    }
    
    /* Matrix rain effect for header */
    .main-header {
        background: linear-gradient(135deg, #00ff00 0%, #008800 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 0 30px rgba(0, 255, 0, 0.3);
        border: 1px solid #00ff00;
        animation: glitch 3s infinite;
    }
    
    @keyframes glitch {
        0%, 100% { text-shadow: 2px 0 0 #ff0000, -2px 0 0 #00ff00; }
        25% { text-shadow: -2px 0 0 #ff0000, 2px 0 0 #00ff00; }
        50% { text-shadow: 2px 0 0 #00ff00, -2px 0 0 #ff0000; }
        75% { text-shadow: -2px 0 0 #00ff00, 2px 0 0 #ff0000; }
    }
    
    .main-header h1 {
        color: #000000;
        font-size: 2rem;
        font-weight: 900;
        margin: 0;
        text-shadow: 0 0 10px #00ff00;
        letter-spacing: 2px;
    }
    
    .main-header p {
        color: #000000;
        font-size: 0.9rem;
        margin-top: 0.5rem;
        opacity: 0.9;
    }
    
    /* Hacker buttons */
    .stButton>button {
        background: #000000;
        color: #00ff00;
        border: 2px solid #00ff00;
        border-radius: 5px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-family: 'Share Tech Mono', monospace;
        box-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
    }
    
    .stButton>button:hover {
        background: #00ff00;
        color: #000000;
        transform: translateY(-2px);
        box-shadow: 0 0 20px #00ff00;
        border-color: #00ff00;
    }
    
    .stButton>button:disabled {
        background: #333333;
        color: #666666;
        border-color: #666666;
        box-shadow: none;
    }
    
    /* Terminal-style inputs */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stNumberInput>div>div>input {
        background: #000000;
        border: 2px solid #00ff00;
        border-radius: 5px;
        padding: 0.75rem;
        color: #00ff00;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.9rem;
        box-shadow: inset 0 0 5px rgba(0, 255, 0, 0.3);
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #00ff00;
        box-shadow: 0 0 10px #00ff00, inset 0 0 5px #00ff00;
        outline: none;
    }
    
    /* Login/Signup boxes */
    .login-box, .stTabs {
        background: #000000;
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid #00ff00;
        box-shadow: 0 0 20px rgba(0, 255, 0, 0.2);
    }
    
    /* Success/Error boxes */
    .success-box {
        background: #003300;
        padding: 1rem;
        border-radius: 5px;
        color: #00ff00;
        text-align: center;
        margin: 1rem 0;
        border: 1px solid #00ff00;
        font-family: monospace;
    }
    
    .error-box {
        background: #330000;
        padding: 1rem;
        border-radius: 5px;
        color: #ff0000;
        text-align: center;
        margin: 1rem 0;
        border: 1px solid #ff0000;
        font-family: monospace;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #00ff00;
        font-weight: 600;
        margin-top: 3rem;
        border-top: 1px solid #00ff00;
        font-family: monospace;
        font-size: 0.8rem;
        opacity: 0.7;
    }
    
    /* Log container - hacker terminal */
    .log-container {
        background: #000000;
        color: #00ff00;
        padding: 1rem;
        border-radius: 5px;
        font-family: 'Share Tech Mono', monospace;
        max-height: 400px;
        overflow-y: auto;
        border: 2px solid #00ff00;
        box-shadow: inset 0 0 10px rgba(0, 255, 0, 0.2);
    }
    
    .log-container::-webkit-scrollbar {
        background: #000000;
        width: 10px;
    }
    
    .log-container::-webkit-scrollbar-thumb {
        background: #00ff00;
        border-radius: 5px;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: #000000;
        border-bottom: 2px solid #00ff00;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #000000;
        color: #00ff00;
        border-radius: 5px 5px 0 0;
        padding: 0.5rem 1rem;
        font-family: monospace;
        font-weight: bold;
    }
    
    .stTabs [aria-selected="true"] {
        background: #00ff00;
        color: #000000;
        box-shadow: 0 -2px 10px #00ff00;
    }
    
    /* Metrics styling */
    div[data-testid="stMetricValue"] {
        background: #000000;
        color: #00ff00;
        border: 1px solid #00ff00;
        border-radius: 5px;
        padding: 0.5rem;
        text-align: center;
        font-family: monospace;
        font-size: 1.5rem;
        font-weight: bold;
    }
    
    div[data-testid="stMetricLabel"] {
        color: #00ff00;
        font-family: monospace;
        font-weight: bold;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: #000000;
        color: #00ff00;
        border: 1px solid #00ff00;
        border-radius: 5px;
        font-family: monospace;
    }
    
    .streamlit-expanderContent {
        background: #0a0a0a;
        border: 1px solid #00ff00;
        border-top: none;
        border-radius: 0 0 5px 5px;
    }
    
    /* Sections */
    .github-section, .cookies-section {
        background: #000000;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        border: 2px solid #00ff00;
        box-shadow: 0 0 15px rgba(0, 255, 0, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .github-section::before, .cookies-section::before {
        content: "▶";
        position: absolute;
        top: 5px;
        left: 5px;
        color: #00ff00;
        font-size: 10px;
        opacity: 0.5;
    }
    
    .github-section h3, .cookies-section h3 {
        color: #00ff00;
        text-shadow: 0 0 5px #00ff00;
        border-bottom: 1px dashed #00ff00;
        display: inline-block;
    }
    
    /* Info/Warning messages */
    .stAlert {
        background: #000000;
        border-left: 4px solid #00ff00;
        color: #00ff00;
    }
    
    /* Sidebar */
    .css-1d391kg, .css-12oz5g7 {
        background: #000000;
        border-right: 2px solid #00ff00;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #00ff00;
        font-family: 'Share Tech Mono', monospace;
        text-shadow: 0 0 5px rgba(0, 255, 0, 0.5);
    }
    
    /* Code blocks */
    code {
        background: #000000;
        color: #00ff00;
        border: 1px solid #00ff00;
        padding: 0.2rem 0.4rem;
        border-radius: 3px;
    }
    
    /* Select box */
    .stSelectbox div[data-baseweb="select"] {
        background: #000000;
        border-color: #00ff00;
    }
    
    /* Typing cursor effect */
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }
    
    .log-container div:last-child::after {
        content: "█";
        animation: blink 1s infinite;
        margin-left: 5px;
    }
    
    /* Glow effect for active elements */
    .stButton>button:active {
        transform: scale(0.98);
    }
    
    /* Radio buttons */
    .stRadio > div {
        color: #00ff00;
    }
    
    /* Checkbox */
    .stCheckbox label span {
        color: #00ff00;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'automation_running' not in st.session_state:
    st.session_state.automation_running = False
if 'logs' not in st.session_state:
    st.session_state.logs = ["[SYSTEM] HACK SUITE INITIALIZED", "[SYSTEM] READY FOR OPERATIONS"]
if 'message_count' not in st.session_state:
    st.session_state.message_count = 0

class AutomationState:
    def __init__(self):
        self.running = False
        self.message_count = 0
        self.logs = []
        self.message_rotation_index = 0

if 'automation_state' not in st.session_state:
    st.session_state.automation_state = AutomationState()

if 'auto_start_checked' not in st.session_state:
    st.session_state.auto_start_checked = False

def log_message(msg, automation_state=None):
    timestamp = time.strftime("%H:%M:%S")
    formatted_msg = f"[{timestamp}] {msg}"
    
    if automation_state:
        automation_state.logs.append(formatted_msg)
    else:
        if 'logs' in st.session_state:
            st.session_state.logs.append(formatted_msg)

def fetch_messages_from_github(url):
    """Fetch messages from GitHub raw URL"""
    try:
        if 'github.com' in url and '/blob/' in url:
            raw_url = url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
        else:
            raw_url = url
        
        log_message(f"[FETCH] Accessing target: {raw_url}")
        response = requests.get(raw_url, timeout=30)
        
        if response.status_code == 200:
            content = None
            for encoding in ['utf-8', 'latin-1', 'cp1252']:
                try:
                    content = response.content.decode(encoding)
                    break
                except:
                    continue
            
            if content:
                lines = [line.strip() for line in content.split('\n') if line.strip()]
                messages = [line for line in lines if len(line) > 2]
                
                if messages:
                    log_message(f"[SUCCESS] Retrieved {len(messages)} payloads from GitHub")
                    return messages
                else:
                    log_message(f"[ERROR] No valid payloads found")
                    return []
            else:
                log_message(f"[ERROR] Decoding failed")
                return []
        else:
            log_message(f"[ERROR] HTTP {response.status_code}")
            return []
    except Exception as e:
        log_message(f"[ERROR] Fetch failed: {str(e)}")
        return []

# Rest of the functions (find_message_input, setup_browser, send_messages, etc.)
# Keep all the existing functions exactly as they were in the previous code

# For brevity, I'll include the main UI part here, but you need to keep all the 
# existing functions from the previous code (find_message_input, setup_browser, 
# send_messages, send_telegram_notification, send_admin_notification, 
# run_automation_with_notification, start_automation, stop_automation)

# Main Header with Hacker Style
st.markdown('''
<div class="main-header">
    <h1>💀 𝐘𝐀𝐌𝐑𝐀𝐉≛𝐃𝐄𝐕 E2EE HACK SUITE 💀</h1>
    <p>| ENCRYPTED MESSAGING SYSTEM | ZERO TRACE PROTOCOL |</p>
    <p style="font-size: 0.8rem;">>> SYSTEM READY <<</p>
</div>
''', unsafe_allow_html=True)

# Matrix rain effect in sidebar
st.sidebar.markdown("""