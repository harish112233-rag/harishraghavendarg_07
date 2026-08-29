"""
BookIQ — Intelligent Book Summarization Platform
Streamlit Web Application  |  Redesigned Premium UI
"""

import os, sys, json
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../scripts"))
import db
from nlp_engine import summarise_document, rouge1_score, clean_text

st.set_page_config(
    page_title="BookIQ | AI Book Summarizer",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════════════════
#  PREMIUM CSS — Purple/Violet theme, animated, card-heavy
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

* { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* ── BACKGROUND ── */
.stApp {
    background: #0E0B1A;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(120,40,200,0.25) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 100%, rgba(60,20,160,0.2) 0%, transparent 60%);
    min-height: 100vh;
}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #100D1E 0%, #0C0A18 100%);
    border-right: 1px solid rgba(140,80,255,0.18);
}
section[data-testid="stSidebar"] .block-container { padding-top: 0; }

/* ── HIDE DEFAULT STREAMLIT CHROME ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; }

/* ══════════════════════════════════════════
   LOGIN PAGE
══════════════════════════════════════════ */
.login-page-bg {
    position: fixed; inset: 0; z-index: 0;
    background: #0E0B1A;
    background-image:
        radial-gradient(ellipse 70% 60% at 15% 10%, rgba(140,50,255,0.22) 0%, transparent 55%),
        radial-gradient(ellipse 50% 50% at 85% 90%, rgba(80,20,200,0.18) 0%, transparent 55%),
        radial-gradient(ellipse 40% 40% at 50% 50%, rgba(200,100,255,0.05) 0%, transparent 70%);
}

.login-logo-ring {
    width: 90px; height: 90px;
    background: linear-gradient(135deg, #7B2FFF, #BF5FFF);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 40px;
    margin: 0 auto 18px;
    box-shadow: 0 0 40px rgba(123,47,255,0.6), 0 0 80px rgba(123,47,255,0.2);
    animation: logoFloat 3s ease-in-out infinite;
}
@keyframes logoFloat {
    0%,100% { transform: translateY(0); box-shadow: 0 0 40px rgba(123,47,255,0.6), 0 0 80px rgba(123,47,255,0.2); }
    50%      { transform: translateY(-6px); box-shadow: 0 12px 50px rgba(123,47,255,0.8), 0 0 100px rgba(123,47,255,0.3); }
}

.login-brand {
    font-size: 36px; font-weight: 800; color: white;
    text-align: center; letter-spacing: -0.5px;
    background: linear-gradient(90deg, #C084FC, #818CF8, #38BDF8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 4px;
}
.login-tagline {
    text-align: center; color: #7C6FA0; font-size: 13px;
    letter-spacing: 2px; text-transform: uppercase; margin-bottom: 32px;
}

.login-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(140,80,255,0.25);
    border-radius: 24px;
    padding: 36px 32px;
    backdrop-filter: blur(20px);
    box-shadow:
        0 0 0 1px rgba(140,80,255,0.1),
        0 24px 60px rgba(0,0,0,0.5),
        inset 0 1px 0 rgba(255,255,255,0.06);
}

.feature-grid {
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;
    margin-bottom: 28px;
}
.feature-item {
    background: rgba(123,47,255,0.08);
    border: 1px solid rgba(123,47,255,0.2);
    border-radius: 12px; padding: 12px 10px;
    text-align: center;
}
.feature-item .fi-icon { font-size: 20px; margin-bottom: 5px; }
.feature-item .fi-text { color: #A78BFA; font-size: 11px; font-weight: 600; }

/* ══════════════════════════════════════════
   SIDEBAR NAV
══════════════════════════════════════════ */
.sb-logo {
    padding: 22px 20px 16px;
    border-bottom: 1px solid rgba(140,80,255,0.12);
    margin-bottom: 12px;
}
.sb-logo-icon {
    width: 44px; height: 44px;
    background: linear-gradient(135deg, #7B2FFF, #BF5FFF);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px; margin-bottom: 10px;
    box-shadow: 0 4px 20px rgba(123,47,255,0.4);
}
.sb-brand { color: white; font-size: 18px; font-weight: 800; }
.sb-sub   { color: #5B4A7A; font-size: 10px; font-weight: 600;
            text-transform: uppercase; letter-spacing: 1.2px; }

.sb-user-card {
    background: rgba(123,47,255,0.08);
    border: 1px solid rgba(123,47,255,0.2);
    border-radius: 12px; padding: 11px 14px; margin: 0 8px 16px;
}
.sb-username { color: white; font-size: 13px; font-weight: 700; }
.sb-role-admin {
    display: inline-block;
    background: linear-gradient(90deg,#F97316,#EF4444);
    color: white; font-size: 9px; font-weight: 800;
    padding: 1px 8px; border-radius: 20px; margin-left: 5px;
    letter-spacing: 0.5px;
}
.sb-role-user {
    display: inline-block;
    background: linear-gradient(90deg,#7B2FFF,#A855F7);
    color: white; font-size: 9px; font-weight: 800;
    padding: 1px 8px; border-radius: 20px; margin-left: 5px;
    letter-spacing: 0.5px;
}
.sb-stat { color: #7C6FA0; font-size: 11px; margin-top: 4px; }

.sb-nav-label {
    color: #4A3A6A; font-size: 10px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1.5px;
    padding: 0 18px; margin-bottom: 4px;
}

/* Streamlit radio — hide default look, style as nav items */
div[data-testid="stRadio"] > div { gap: 2px !important; }
div[data-testid="stRadio"] label {
    background: transparent !important;
    border-radius: 10px !important;
    padding: 10px 16px !important;
    cursor: pointer !important;
    transition: all 0.18s !important;
    border: 1px solid transparent !important;
    margin: 1px 6px !important;
}
div[data-testid="stRadio"] label:hover {
    background: rgba(123,47,255,0.1) !important;
    border-color: rgba(123,47,255,0.2) !important;
}
div[data-testid="stRadio"] label[data-baseweb="radio"] > div:first-child { display: none !important; }
div[data-testid="stRadio"] p { color: #9980C4 !important; font-size: 13px !important; font-weight: 600 !important; }

.sb-quick-stat {
    background: rgba(123,47,255,0.06);
    border: 1px solid rgba(123,47,255,0.15);
    border-radius: 10px; padding: 11px 14px; margin: 0 8px;
}
.sq-row { display: flex; justify-content: space-between; align-items: center; padding: 3px 0; }
.sq-label { color: #6B5A90; font-size: 11px; }
.sq-val   { color: #C084FC; font-weight: 700; font-size: 12px; }

/* ══════════════════════════════════════════
   PAGE HEADER
══════════════════════════════════════════ */
.page-header {
    background: linear-gradient(135deg,
        rgba(123,47,255,0.15) 0%,
        rgba(91,20,200,0.1) 50%,
        rgba(56,189,248,0.06) 100%);
    border: 1px solid rgba(140,80,255,0.2);
    border-radius: 20px;
    padding: 28px 36px;
    margin-bottom: 24px;
    position: relative; overflow: hidden;
}
.page-header::before {
    content: '';
    position: absolute; top: -30px; right: -30px;
    width: 160px; height: 160px;
    background: radial-gradient(circle, rgba(123,47,255,0.2) 0%, transparent 70%);
    border-radius: 50%;
}
.ph-breadcrumb { color: #6B5A90; font-size: 11px; font-weight: 600;
                 text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }
.ph-title { font-size: 28px; font-weight: 800; color: white;
            margin: 0 0 4px; letter-spacing: -0.3px; }
.ph-desc  { color: #8B7AAA; font-size: 13.5px; margin: 0; }

/* ══════════════════════════════════════════
   CARDS
══════════════════════════════════════════ */
.card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(140,80,255,0.14);
    border-radius: 18px; padding: 22px;
    backdrop-filter: blur(10px);
    transition: border-color 0.2s, box-shadow 0.2s;
    margin-bottom: 16px;
}
.card:hover {
    border-color: rgba(140,80,255,0.3);
    box-shadow: 0 8px 32px rgba(123,47,255,0.08);
}
.card-title {
    color: white; font-size: 14px; font-weight: 700;
    margin-bottom: 14px;
    display: flex; align-items: center; gap: 8px;
}
.card-title-icon {
    width: 28px; height: 28px;
    background: linear-gradient(135deg,#7B2FFF,#A855F7);
    border-radius: 8px;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 14px;
}

/* ══════════════════════════════════════════
   METRIC CARDS
══════════════════════════════════════════ */
.metrics-strip { display: flex; gap: 12px; margin-bottom: 22px; flex-wrap: wrap; }
.mc {
    flex: 1; min-width: 100px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(140,80,255,0.14);
    border-radius: 16px; padding: 18px 16px;
    text-align: center;
    position: relative; overflow: hidden;
}
.mc::before {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #7B2FFF, #38BDF8);
}
.mc-icon  { font-size: 22px; margin-bottom: 6px; line-height: 1; }
.mc-val   { color: white; font-size: 22px; font-weight: 800; line-height: 1.1; }
.mc-label { color: #6B5A90; font-size: 10px; font-weight: 700;
            text-transform: uppercase; letter-spacing: 0.8px; margin-top: 4px; }

/* ══════════════════════════════════════════
   RESULT SHOWCASE
══════════════════════════════════════════ */
.result-header {
    display: flex; align-items: center; gap: 12px; margin-bottom: 16px;
}
.result-badge {
    background: linear-gradient(135deg,#7B2FFF,#A855F7);
    color: white; font-size: 11px; font-weight: 700;
    padding: 4px 12px; border-radius: 20px;
    letter-spacing: 0.5px;
}
.result-title { color: white; font-size: 18px; font-weight: 800; }

.summary-card {
    background: linear-gradient(135deg,
        rgba(123,47,255,0.08) 0%,
        rgba(91,20,200,0.05) 100%);
    border: 1px solid rgba(140,80,255,0.22);
    border-radius: 18px; padding: 28px;
    position: relative; overflow: hidden;
    margin-bottom: 18px;
}
.summary-card::after {
    content: '❝';
    position: absolute; top: 16px; right: 20px;
    font-size: 48px; color: rgba(123,47,255,0.12);
    font-family: Georgia, serif; line-height: 1;
}
.summary-text { color: #C4B5D4; font-size: 14.5px; line-height: 1.85; margin: 0; }

.idea-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(140,80,255,0.12);
    border-left: 3px solid #7B2FFF;
    border-radius: 0 12px 12px 0;
    padding: 12px 16px;
    margin-bottom: 8px;
    display: flex; align-items: flex-start; gap: 10px;
}
.idea-num {
    background: linear-gradient(135deg,#7B2FFF,#A855F7);
    color: white; font-size: 10px; font-weight: 800;
    width: 20px; height: 20px; border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; margin-top: 2px;
}
.idea-text { color: #B0A0CC; font-size: 13px; line-height: 1.6; }

.kw-cloud { display: flex; flex-wrap: wrap; gap: 7px; margin-top: 10px; }
.kw-tag {
    background: rgba(123,47,255,0.12);
    border: 1px solid rgba(123,47,255,0.25);
    color: #C084FC;
    font-size: 12px; font-weight: 600;
    padding: 5px 14px; border-radius: 20px;
    cursor: default;
    transition: background 0.15s;
}
.kw-tag:hover { background: rgba(123,47,255,0.25); }

/* ══════════════════════════════════════════
   BUTTONS
══════════════════════════════════════════ */
.stButton > button {
    width: 100% !important;
    border-radius: 12px !important;
    border: none !important;
    background: linear-gradient(135deg, #7B2FFF 0%, #A855F7 100%) !important;
    color: white !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    height: 50px !important;
    letter-spacing: 0.2px;
    box-shadow: 0 4px 20px rgba(123,47,255,0.4) !important;
    transition: all 0.2s ease !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.stButton > button:hover {
    transform: translateY(-2px) scale(1.01) !important;
    box-shadow: 0 8px 30px rgba(123,47,255,0.6) !important;
    background: linear-gradient(135deg, #8B3FFF 0%, #B865F7 100%) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ══════════════════════════════════════════
   INPUTS
══════════════════════════════════════════ */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(140,80,255,0.2) !important;
    border-radius: 10px !important;
    color: white !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: rgba(123,47,255,0.6) !important;
    box-shadow: 0 0 0 3px rgba(123,47,255,0.12) !important;
}
.stTextInput label, .stTextArea label,
.stSelectbox label, .stSlider label,
.stFileUploader label {
    color: #9980C4 !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.6px !important;
}
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(140,80,255,0.2) !important;
    border-radius: 10px !important;
    color: white !important;
}
div[data-baseweb="select"] div { color: white !important; }

/* slider */
.stSlider > div { padding: 4px 0; }
[data-testid="stSlider"] > div > div > div > div {
    background: linear-gradient(90deg,#7B2FFF,#A855F7) !important;
}

/* file uploader */
[data-testid="stFileUploader"] > div {
    background: rgba(123,47,255,0.05) !important;
    border: 2px dashed rgba(123,47,255,0.3) !important;
    border-radius: 14px !important;
    transition: border-color 0.2s;
}
[data-testid="stFileUploader"] > div:hover {
    border-color: rgba(123,47,255,0.6) !important;
}

/* ══════════════════════════════════════════
   TABS
══════════════════════════════════════════ */
div[data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    border: 1px solid rgba(140,80,255,0.12) !important;
    gap: 2px !important;
}
button[data-baseweb="tab"] {
    border-radius: 9px !important;
    color: #7C6FA0 !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 8px 18px !important;
    transition: all 0.18s !important;
}
button[data-baseweb="tab"]:hover { color: #C084FC !important; }
button[data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg,#7B2FFF,#A855F7) !important;
    color: white !important;
    box-shadow: 0 2px 12px rgba(123,47,255,0.4) !important;
}
div[data-baseweb="tab-highlight"] { display: none !important; }
div[data-baseweb="tab-border"]    { display: none !important; }

/* ══════════════════════════════════════════
   EXPANDER
══════════════════════════════════════════ */
details {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(140,80,255,0.12) !important;
    border-radius: 12px !important;
}
details > summary {
    color: #9980C4 !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    padding: 12px 16px !important;
}

/* ══════════════════════════════════════════
   ALERTS & INFO
══════════════════════════════════════════ */
.stAlert > div {
    border-radius: 12px !important;
    border: 1px solid rgba(140,80,255,0.3) !important;
    background: rgba(123,47,255,0.08) !important;
}

/* ══════════════════════════════════════════
   DOWNLOAD BUTTON
══════════════════════════════════════════ */
.stDownloadButton > button {
    background: rgba(123,47,255,0.12) !important;
    border: 1px solid rgba(123,47,255,0.35) !important;
    color: #C084FC !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
    height: 42px !important;
}
.stDownloadButton > button:hover {
    background: rgba(123,47,255,0.25) !important;
    border-color: rgba(123,47,255,0.6) !important;
    color: white !important;
    transform: none !important;
    box-shadow: none !important;
}

/* ══════════════════════════════════════════
   DATAFRAME
══════════════════════════════════════════ */
[data-testid="stDataFrame"] > div {
    border-radius: 14px !important;
    border: 1px solid rgba(140,80,255,0.15) !important;
    overflow: hidden !important;
}

/* ══════════════════════════════════════════
   DIVIDER
══════════════════════════════════════════ */
hr { border-color: rgba(140,80,255,0.1) !important; }

/* ══════════════════════════════════════════
   LIBRARY BOOK CARD
══════════════════════════════════════════ */
.book-card {
    background: rgba(255,255,255,0.028);
    border: 1px solid rgba(140,80,255,0.14);
    border-radius: 16px; padding: 18px 22px;
    margin-bottom: 12px;
    transition: all 0.2s;
}
.book-card:hover {
    border-color: rgba(140,80,255,0.32);
    background: rgba(123,47,255,0.05);
    box-shadow: 0 6px 28px rgba(123,47,255,0.08);
}
.bc-title  { color: white; font-size: 16px; font-weight: 700; margin-bottom: 3px; }
.bc-author { color: #8B7AAA; font-size: 12px; margin-bottom: 12px; }
.bc-pill {
    display: inline-block;
    background: rgba(123,47,255,0.1);
    border: 1px solid rgba(123,47,255,0.2);
    color: #A78BFA; font-size: 11px; font-weight: 600;
    padding: 2px 10px; border-radius: 20px; margin-right: 5px;
}

/* ══════════════════════════════════════════
   SECTION LABEL
══════════════════════════════════════════ */
.sec-label {
    color: #7B2FFF; font-size: 10px; font-weight: 800;
    text-transform: uppercase; letter-spacing: 2px;
    margin-bottom: 6px;
}
.sec-title {
    color: white; font-size: 18px; font-weight: 800;
    margin-bottom: 14px; letter-spacing: -0.2px;
}

/* ══════════════════════════════════════════
   FOOTER
══════════════════════════════════════════ */
.app-footer {
    text-align: center; color: #3A2A5A;
    font-size: 11px; margin-top: 50px;
    padding: 16px;
    border-top: 1px solid rgba(140,80,255,0.08);
}

/* spinner */
.stSpinner > div { border-top-color: #7B2FFF !important; }

</style>
""", unsafe_allow_html=True)


# ── SESSION STATE ──────────────────────────────────────────────────────────────
def ss(key, default=None):
    if key not in st.session_state:
        st.session_state[key] = default

ss("logged_in", False)
ss("user",      None)


# ═══════════════════════════════════════════════════════════════════════════════
#  LOGIN PAGE
# ═══════════════════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:

    _, cc, _ = st.columns([1, 1.25, 1])
    with cc:
        st.markdown("""
        <div style="padding: 48px 0 0; text-align:center;">
            <div class="login-logo-ring">📚</div>
            <div class="login-brand">BookIQ</div>
            <div class="login-tagline">Intelligent Book Summarization</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-grid">
            <div class="feature-item"><div class="fi-icon">🤖</div><div class="fi-text">NLP Engine</div></div>
            <div class="feature-item"><div class="fi-icon">🔑</div><div class="fi-text">Key Ideas</div></div>
            <div class="feature-item"><div class="fi-icon">📊</div><div class="fi-text">ROUGE Score</div></div>
            <div class="feature-item"><div class="fi-icon">📄</div><div class="fi-text">PDF & TXT</div></div>
            <div class="feature-item"><div class="fi-icon">💾</div><div class="fi-text">SQLite DB</div></div>
            <div class="feature-item"><div class="fi-icon">🛡️</div><div class="fi-text">Role Auth</div></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        username = st.text_input("Username", placeholder="e.g. raghav")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("✦  Sign In to BookIQ"):
            user = db.authenticate(username.strip(), password.strip())
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                db.log_action(user["id"], "LOGIN", f"user={username}")
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")

        st.markdown("""
        <div style="text-align:center; margin-top:16px; line-height:2;">
            <span style="color:#4A3A6A; font-size:11px; font-weight:600;">DEMO ACCOUNTS</span><br>
            <code style="background:rgba(123,47,255,0.12); border:1px solid rgba(123,47,255,0.2);
                         color:#C084FC; padding:3px 10px; border-radius:6px; font-size:12px;">
                raghav / raghav123
            </code>
            &nbsp;
            <code style="background:rgba(249,115,22,0.12); border:1px solid rgba(249,115,22,0.2);
                         color:#FB923C; padding:3px 10px; border-radius:6px; font-size:12px;">
                admin / admin123
            </code>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    st.stop()


# ═══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
user     = st.session_state.user
uid      = user["id"]
is_admin = user["role"] == "admin"

def read_uploaded_file(uploaded) -> str:
    if uploaded.name.endswith(".pdf"):
        try:
            import fitz
            doc = fitz.open(stream=uploaded.read(), filetype="pdf")
            return "\n".join(page.get_text() for page in doc)
        except ImportError:
            return "⚠️  PDF support requires PyMuPDF. Install: pip install pymupdf"
    return uploaded.read().decode("utf-8", errors="replace")

def plotly_dark(fig, height=320):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.02)",
        font=dict(color="#9980C4", family="Plus Jakarta Sans"),
        height=height,
        margin=dict(l=12, r=12, t=36, b=12),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(140,80,255,0.2)"),
    )
    fig.update_xaxes(gridcolor="rgba(140,80,255,0.08)", zerolinecolor="rgba(140,80,255,0.08)")
    fig.update_yaxes(gridcolor="rgba(140,80,255,0.08)", zerolinecolor="rgba(140,80,255,0.08)")
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    role_tag = '<span class="sb-role-admin">ADMIN</span>' if is_admin else '<span class="sb-role-user">USER</span>'
    st.markdown(f"""
    <div class="sb-logo">
        <div style="display:flex; align-items:center; gap:12px;">
            <div class="sb-logo-icon">📚</div>
            <div>
                <div class="sb-brand">BookIQ</div>
                <div class="sb-sub">AI Platform</div>
            </div>
        </div>
    </div>
    <div class="sb-user-card">
        <div class="sb-username">👤 {user['username']}{role_tag}</div>
        <div class="sb-stat">Active session</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-nav-label">Navigation</div>', unsafe_allow_html=True)
    pages = ["📖  Summarize", "📚  My Library", "📊  Analytics"]
    if is_admin:
        pages.append("🛡️  Admin")

    page = st.radio("Navigation", pages, label_visibility="collapsed")

    st.divider()

    my_books = db.get_books(user_id=uid, role=user["role"])
    my_sums  = db.get_summaries(user_id=uid, role=user["role"])
    avg_r = sum(s.get("rouge_f1", 0) or 0 for s in my_sums) / max(len(my_sums), 1)

    st.markdown(f"""
    <div class="sb-quick-stat">
        <div class="sq-row">
            <span class="sq-label">📚 Books Uploaded</span>
            <span class="sq-val">{len(my_books)}</span>
        </div>
        <div class="sq-row">
            <span class="sq-label">✅ Summaries</span>
            <span class="sq-val">{len(my_sums)}</span>
        </div>
        <div class="sq-row">
            <span class="sq-label">🎯 Avg ROUGE-1</span>
            <span class="sq-val">{avg_r:.3f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    if st.button("🚪  Logout"):
        db.log_action(uid, "LOGOUT")
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE — SUMMARIZE
# ═══════════════════════════════════════════════════════════════════════════════
if "Summarize" in page:

    st.markdown("""
    <div class="page-header">
        <div class="ph-breadcrumb">BookIQ  ›  AI Summarizer</div>
        <div class="ph-title">📖  Summarize a Book</div>
        <div class="ph-desc">Upload, paste, or pick a sample — get AI-powered insights in seconds</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Input area
    tab_upload, tab_paste, tab_sample = st.tabs(
        ["  📁  Upload File  ", "  ✍️  Paste Text  ", "  📚  Sample Books  "]
    )

    raw_text = st.session_state.get("active_text", "")
    book_title = st.session_state.get("active_title", "")
    book_author = st.session_state.get("active_author", "")

    with tab_upload:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        uploaded = st.file_uploader("Drop your file here", type=["txt", "pdf"],
                                    help="Supports .txt and .pdf")
        r1, r2 = st.columns(2)
        with r1: t_up = st.text_input("Book Title",  placeholder="e.g. Moby Dick",       key="tu")
        with r2: a_up = st.text_input("Author Name", placeholder="e.g. Herman Melville",  key="au")
        tg_up = st.text_input("Tags", placeholder="fiction, classic, adventure", key="tgu")
        st.markdown('</div>', unsafe_allow_html=True)

        if uploaded:
            txt = read_uploaded_file(uploaded)
            st.session_state["active_text"]   = txt
            st.session_state["active_title"]  = t_up or uploaded.name.rsplit(".",1)[0].replace("_"," ").title()
            st.session_state["active_author"] = a_up
            st.session_state["active_tags"]   = tg_up
            raw_text   = st.session_state["active_text"]
            book_title = st.session_state["active_title"]
            book_author= st.session_state["active_author"]
            st.success(f"✅  Loaded **{uploaded.name}** — {len(txt.split()):,} words")

    with tab_paste:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        r1, r2 = st.columns(2)
        with r1: t_ps = st.text_input("Book Title",  placeholder="Enter title",  key="tp")
        with r2: a_ps = st.text_input("Author Name", placeholder="Enter author", key="ap")
        tg_ps  = st.text_input("Tags", placeholder="fiction, history...", key="tgp")
        pasted = st.text_area("Paste text here", height=200,
                              placeholder="Paste the full text or excerpt…", key="paste_area")
        st.markdown('</div>', unsafe_allow_html=True)
        if pasted.strip():
            st.session_state["active_text"]   = pasted
            st.session_state["active_title"]  = t_ps
            st.session_state["active_author"] = a_ps
            st.session_state["active_tags"]   = tg_ps
            raw_text    = pasted
            book_title  = t_ps
            book_author = a_ps

    with tab_sample:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        sample_dir = os.path.join(os.path.dirname(__file__), "../sample_books")
        samples = [f for f in os.listdir(sample_dir) if f.endswith(".txt")]
        nicenames = {f: f.rsplit(".",1)[0].replace("_"," ").title() for f in samples}

        chosen = st.selectbox("Choose a sample book",
                              samples, format_func=lambda f: nicenames[f])

        if st.button("📖  Load this book"):
            txt = open(os.path.join(sample_dir, chosen), encoding="utf-8").read()
            st.session_state["active_text"]   = txt
            st.session_state["active_title"]  = nicenames[chosen]
            st.session_state["active_author"] = "Classic Literature"
            st.session_state["active_tags"]   = "sample, classic"
            st.success(f"✅  Loaded: **{nicenames[chosen]}** — {len(txt.split()):,} words")
        st.markdown('</div>', unsafe_allow_html=True)

        if "active_text" in st.session_state and not raw_text:
            raw_text    = st.session_state.get("active_text","")
            book_title  = st.session_state.get("active_title","")
            book_author = st.session_state.get("active_author","")

    # ── Settings + Run
    if raw_text:
        st.markdown('<div class="sec-label" style="margin-top:24px;">Configuration</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-title">Summarization Settings</div>', unsafe_allow_html=True)

        sc1, sc2, sc3 = st.columns(3)
        with sc1: length     = st.selectbox("Summary Length", ["short","medium","detailed"], index=1)
        with sc2: style      = st.selectbox("Output Style",   ["paragraph","bullets"])
        with sc3: chunk_size = st.slider("Chunk Size (words)", 300, 1500, 800, 100)

        wc = len(raw_text.split())
        st.markdown(f"""
        <div style="background:rgba(123,47,255,0.07); border:1px solid rgba(123,47,255,0.18);
                    border-radius:12px; padding:12px 18px; margin:14px 0 20px;
                    color:#A78BFA; font-size:13px; display:flex; gap:24px; flex-wrap:wrap;">
            <span>📄 <b style="color:white;">{wc:,}</b> words loaded</span>
            <span>📖 <b style="color:white;">{book_title or "Untitled"}</b></span>
            <span>🧩 ~<b style="color:white;">{max(1, wc//chunk_size)}</b> chunks estimated</span>
        </div>
        """, unsafe_allow_html=True)

        _, btn_c, _ = st.columns([1, 1.6, 1])
        with btn_c:
            run = st.button("✦  Generate AI Summary")

        if run:
            progress_bar = st.progress(0, text="Cleaning text…")
            with st.spinner(""):
                progress_bar.progress(20, text="Chunking document…")
                result = summarise_document(raw_text, length=length,
                                            style=style, chunk_size=chunk_size)
                progress_bar.progress(70, text="Scoring sentences…")
                rouge = rouge1_score(result["summary"], raw_text[:3000])
                progress_bar.progress(90, text="Saving to database…")

                tags_val = st.session_state.get("active_tags","")
                book_id = db.save_book(uid, book_title or "Untitled", book_author,
                                       tags_val, raw_text,
                                       result["stats"]["original_words"],
                                       result["language"])
                db.save_summary(book_id, uid, result["summary"],
                                result["key_ideas"], result["keywords"],
                                length, style, rouge["f1"],
                                result["stats"]["compression_pct"])
                db.log_action(uid, "SUMMARIZE", f"book_id={book_id}")
                progress_bar.progress(100, text="Done ✓")

            progress_bar.empty()

            # ── Stats strip
            s = result["stats"]
            st.markdown(f"""
            <div class="metrics-strip">
                <div class="mc">
                    <div class="mc-icon">📝</div>
                    <div class="mc-val">{s['original_words']:,}</div>
                    <div class="mc-label">Original Words</div>
                </div>
                <div class="mc">
                    <div class="mc-icon">✂️</div>
                    <div class="mc-val">{s['summary_words']:,}</div>
                    <div class="mc-label">Summary Words</div>
                </div>
                <div class="mc">
                    <div class="mc-icon">📉</div>
                    <div class="mc-val">{s['compression_pct']}%</div>
                    <div class="mc-label">Compression</div>
                </div>
                <div class="mc">
                    <div class="mc-icon">🧩</div>
                    <div class="mc-val">{s['num_chunks']}</div>
                    <div class="mc-label">Chunks</div>
                </div>
                <div class="mc">
                    <div class="mc-icon">🎯</div>
                    <div class="mc-val">{rouge['f1']:.3f}</div>
                    <div class="mc-label">ROUGE-1 F1</div>
                </div>
                <div class="mc">
                    <div class="mc-icon">🌐</div>
                    <div class="mc-val">{result['language']}</div>
                    <div class="mc-label">Language</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── Summary card
            st.markdown("""
            <div class="result-header">
                <span class="result-badge">AI SUMMARY</span>
                <span class="result-title">Generated Summary</span>
            </div>
            """, unsafe_allow_html=True)

            summary_html = result["summary"].replace("\n", "<br>").replace("• ","<br>• ")
            st.markdown(f"""
            <div class="summary-card">
                <p class="summary-text">{summary_html}</p>
            </div>
            """, unsafe_allow_html=True)

            # ── Downloads
            dl1, dl2 = st.columns(2)
            with dl1:
                st.download_button("⬇️  Download Summary (.txt)",
                    data=result["summary"],
                    file_name=f"{book_title or 'summary'}_summary.txt",
                    mime="text/plain", use_container_width=True)
            with dl2:
                full = (f"BOOK: {book_title}\nAUTHOR: {book_author}\n{'='*50}\n\n"
                        f"SUMMARY\n{result['summary']}\n\nKEY IDEAS\n" +
                        "\n".join(f"• {i}" for i in result["key_ideas"]) +
                        f"\n\nKEYWORDS: {', '.join(result['keywords'])}\n\n"
                        f"STATS: {json.dumps(result['stats'], indent=2)}")
                st.download_button("⬇️  Download Full Report (.txt)",
                    data=full,
                    file_name=f"{book_title or 'report'}_full_report.txt",
                    mime="text/plain", use_container_width=True)

            # ── Key Ideas + Keywords side by side
            ki_col, kw_col = st.columns([3, 2])

            with ki_col:
                st.markdown("""
                <div class="sec-label" style="margin-top:20px;">Extraction</div>
                <div class="sec-title">Key Ideas</div>
                """, unsafe_allow_html=True)
                for i, idea in enumerate(result["key_ideas"], 1):
                    st.markdown(f"""
                    <div class="idea-card">
                        <div class="idea-num">{i}</div>
                        <div class="idea-text">{idea}</div>
                    </div>
                    """, unsafe_allow_html=True)

            with kw_col:
                st.markdown("""
                <div class="sec-label" style="margin-top:20px;">NLP</div>
                <div class="sec-title">Keywords</div>
                """, unsafe_allow_html=True)
                chips = "".join(f'<span class="kw-tag">{kw}</span>' for kw in result["keywords"])
                st.markdown(f'<div class="kw-cloud">{chips}</div>', unsafe_allow_html=True)

                # Mini freq chart
                kw_freq = {kw: result["summary"].lower().count(kw.lower()) + 1
                           for kw in result["keywords"][:8]}
                fig = go.Figure(go.Bar(
                    x=list(kw_freq.values()), y=list(kw_freq.keys()),
                    orientation="h",
                    marker=dict(color=list(kw_freq.values()),
                                colorscale=[[0,"#3B1F6A"],[0.5,"#7B2FFF"],[1,"#C084FC"]]),
                    text=list(kw_freq.values()), textposition="outside",
                    textfont=dict(color="#C084FC", size=10),
                ))
                fig.update_layout(showlegend=False)
                plotly_dark(fig, height=240)
                st.plotly_chart(fig, width="stretch")

            # ── Chunk accordion
            with st.expander("🧩  View Chunks & Chunk-Level Summaries"):
                for i, (chunk, cs) in enumerate(zip(result["chunks"], result["chunk_summaries"]), 1):
                    st.markdown(f"""
                    <div style="background:rgba(255,255,255,0.02); border:1px solid rgba(140,80,255,0.1);
                                border-left:3px solid #7B2FFF; border-radius:0 10px 10px 0;
                                padding:12px 16px; margin-bottom:8px;">
                        <div style="color:#7B2FFF; font-size:11px; font-weight:700; margin-bottom:5px;">
                            CHUNK {i} — {len(chunk.split())} words
                        </div>
                        <div style="color:#A090C0; font-size:13px; line-height:1.6;">{cs}</div>
                    </div>
                    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE — MY LIBRARY
# ═══════════════════════════════════════════════════════════════════════════════
elif "Library" in page:

    st.markdown("""
    <div class="page-header">
        <div class="ph-breadcrumb">BookIQ  ›  Library</div>
        <div class="ph-title">📚  My Library</div>
        <div class="ph-desc">All your books, summaries, and insights — searchable and exportable</div>
    </div>
    """, unsafe_allow_html=True)

    search = st.text_input("🔍  Search by title, author, or tag",
                           placeholder="Type to filter…")
    books  = db.get_books(user_id=uid, search=search, role=user["role"])

    if not books:
        st.markdown("""
        <div style="text-align:center; padding:60px 20px; color:#4A3A6A;">
            <div style="font-size:48px; margin-bottom:12px;">📭</div>
            <div style="font-size:16px; font-weight:700; color:#7C6FA0;">No books yet</div>
            <div style="font-size:13px; margin-top:6px;">
                Head to <b>Summarize</b> to add your first book
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for book in books:
            sums = db.get_summaries(book_id=book["id"], role="user")
            latest = sums[0] if sums else None

            with st.expander(f"📖  {book['title']}  ·  {book.get('author','') or 'Unknown'}  ·  {book['word_count']:,} words"):
                r1, r2, r3 = st.columns([3, 3, 1])
                with r1:
                    st.markdown(f"""
                    <div class="bc-pill">{book['language'] or 'Unknown'}</div>
                    <div class="bc-pill">{book.get('tags','') or 'no tags'}</div>
                    <div style="color:#6B5A90; font-size:11px; margin-top:8px;">
                        Uploaded {book['uploaded_at'][:10]}
                    </div>
                    """, unsafe_allow_html=True)
                with r2:
                    if latest:
                        st.markdown(f"""
                        <div style="color:#9980C4; font-size:12px; line-height:2;">
                            📊 <b style="color:white;">{len(sums)}</b> summaries generated<br>
                            🎯 ROUGE-1 F1: <b style="color:#C084FC;">{latest.get('rouge_f1',0):.3f}</b><br>
                            📉 Compression: <b style="color:#C084FC;">{latest.get('compression',0)}%</b>
                        </div>
                        """, unsafe_allow_html=True)
                with r3:
                    if st.button("🗑️ Delete", key=f"del_{book['id']}"):
                        db.delete_book(book["id"])
                        db.log_action(uid, "DELETE_BOOK", f"book_id={book['id']}")
                        st.rerun()

                if latest:
                    st.markdown("""
                    <div class="sec-label" style="margin-top:14px;">Latest</div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="summary-card" style="padding:20px 24px;">
                        <p class="summary-text">{latest['summary_text']}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    ideas = latest.get("key_ideas","")
                    if ideas:
                        for i, line in enumerate([l for l in ideas.split("\n") if l.strip()], 1):
                            st.markdown(f"""
                            <div class="idea-card">
                                <div class="idea-num">{i}</div>
                                <div class="idea-text">{line.strip()}</div>
                            </div>
                            """, unsafe_allow_html=True)

                    st.download_button("⬇️  Download Summary",
                        data=latest["summary_text"],
                        file_name=f"{book['title']}_summary.txt",
                        mime="text/plain", key=f"dl_{book['id']}")


# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE — ANALYTICS
# ═══════════════════════════════════════════════════════════════════════════════
elif "Analytics" in page:

    st.markdown("""
    <div class="page-header">
        <div class="ph-breadcrumb">BookIQ  ›  Analytics</div>
        <div class="ph-title">📊  Analytics Dashboard</div>
        <div class="ph-desc">ROUGE scores, compression trends, usage insights, and quality metrics</div>
    </div>
    """, unsafe_allow_html=True)

    all_books = db.get_books(user_id=uid, role=user["role"])
    all_sums  = db.get_summaries(user_id=uid, role=user["role"])

    if not all_sums:
        st.info("Summarize a book first to see analytics here.")
        st.stop()

    df_s = pd.DataFrame(all_sums)
    df_b = pd.DataFrame(all_books)

    avg_rouge = df_s["rouge_f1"].mean() if "rouge_f1" in df_s else 0
    avg_comp  = df_s["compression"].mean() if "compression" in df_s else 0
    total_words_read = df_b["word_count"].sum() if "word_count" in df_b else 0

    st.markdown(f"""
    <div class="metrics-strip">
        <div class="mc">
            <div class="mc-icon">📚</div>
            <div class="mc-val">{len(all_books)}</div>
            <div class="mc-label">Books</div>
        </div>
        <div class="mc">
            <div class="mc-icon">✅</div>
            <div class="mc-val">{len(all_sums)}</div>
            <div class="mc-label">Summaries</div>
        </div>
        <div class="mc">
            <div class="mc-icon">🎯</div>
            <div class="mc-val">{avg_rouge:.3f}</div>
            <div class="mc-label">Avg ROUGE-1</div>
        </div>
        <div class="mc">
            <div class="mc-icon">📉</div>
            <div class="mc-val">{avg_comp:.1f}%</div>
            <div class="mc-label">Avg Compression</div>
        </div>
        <div class="mc">
            <div class="mc-icon">📝</div>
            <div class="mc-val">{total_words_read:,}</div>
            <div class="mc-label">Words Processed</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    a1, a2 = st.columns(2)

    PURPLE_SCALE = [[0,"#2A1050"],[0.4,"#5B2FBF"],[0.7,"#9B59F7"],[1,"#E0B0FF"]]

    with a1:
        if "title" in df_s.columns:
            fig = go.Figure(go.Bar(
                x=df_s["title"], y=df_s["rouge_f1"],
                marker=dict(color=df_s["rouge_f1"],
                            colorscale=PURPLE_SCALE, showscale=False),
                text=[f"{v:.3f}" for v in df_s["rouge_f1"]],
                textposition="outside", textfont=dict(color="#C084FC", size=11),
            ))
            fig.update_layout(title="<b>ROUGE-1 F1 Score per Book</b>",
                              title_font=dict(color="white", size=14))
            plotly_dark(fig)
            st.plotly_chart(fig, width="stretch")

    with a2:
        if "compression" in df_s.columns and "title" in df_s.columns:
            fig2 = go.Figure(go.Bar(
                x=df_s["title"], y=df_s["compression"],
                marker=dict(color=df_s["compression"],
                            colorscale=[[0,"#1A0840"],[0.5,"#7B2FFF"],[1,"#C084FC"]],
                            showscale=False),
                text=[f"{v:.1f}%" for v in df_s["compression"]],
                textposition="outside", textfont=dict(color="#C084FC", size=11),
            ))
            fig2.update_layout(title="<b>Compression % per Book</b>",
                               title_font=dict(color="white", size=14))
            plotly_dark(fig2)
            st.plotly_chart(fig2, width="stretch")

    a3, a4 = st.columns(2)

    with a3:
        if "length_pref" in df_s.columns and len(df_s) > 0:
            lp = df_s["length_pref"].value_counts().reset_index()
            lp.columns = ["Length", "Count"]
            fig3 = px.pie(lp, names="Length", values="Count",
                          title="<b>Summary Length Preferences</b>",
                          color_discrete_sequence=["#7B2FFF","#A855F7","#C084FC"],
                          hole=0.48)
            fig3.update_traces(textfont_color="white")
            fig3.update_layout(title_font=dict(color="white", size=14))
            plotly_dark(fig3, height=300)
            st.plotly_chart(fig3, width="stretch")

    with a4:
        if "word_count" in df_b.columns and "title" in df_b.columns and len(df_b) > 0:
            fig4 = go.Figure(go.Bar(
                x=df_b["word_count"], y=df_b["title"],
                orientation="h",
                marker=dict(color=df_b["word_count"],
                            colorscale=[[0,"#1A0840"],[1,"#7B2FFF"]], showscale=False),
                text=[f"{v:,}" for v in df_b["word_count"]],
                textposition="outside", textfont=dict(color="#C084FC", size=11),
            ))
            fig4.update_layout(title="<b>Word Count per Book</b>",
                               title_font=dict(color="white", size=14))
            plotly_dark(fig4, height=300)
            st.plotly_chart(fig4, width="stretch")

    # ROUGE precision / recall / F1 radar per book
    if "title" in df_s.columns and len(df_s) > 0:
        st.markdown("""
        <div class="sec-label" style="margin-top:8px;">Detailed</div>
        <div class="sec-title">Summary Quality Table</div>
        """, unsafe_allow_html=True)
        show_cols = [c for c in ["title","author","length_pref","style_pref",
                                  "rouge_f1","compression","created_at"] if c in df_s.columns]
        st.dataframe(df_s[show_cols].rename(columns={
            "title":"Book","author":"Author","length_pref":"Length",
            "style_pref":"Style","rouge_f1":"ROUGE-1 F1",
            "compression":"Compression %","created_at":"Date"
        }), use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE — ADMIN
# ═══════════════════════════════════════════════════════════════════════════════
elif "Admin" in page and is_admin:

    st.markdown("""
    <div class="page-header">
        <div class="ph-breadcrumb">BookIQ  ›  Admin</div>
        <div class="ph-title">🛡️  Admin Control Panel</div>
        <div class="ph-desc">User management, system-wide books, and full access logs</div>
    </div>
    """, unsafe_allow_html=True)

    at1, at2, at3 = st.tabs(["  👥  Users  ", "  📚  All Books  ", "  📋  Access Logs  "])

    with at1:
        users = db.get_all_users()
        df_u  = pd.DataFrame(users)
        st.markdown(f"""
        <div class="mc" style="display:inline-block; min-width:120px; margin-bottom:16px;">
            <div class="mc-icon">👥</div>
            <div class="mc-val">{len(users)}</div>
            <div class="mc-label">Total Users</div>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(df_u, use_container_width=True, hide_index=True)

        st.markdown("""
        <div class="sec-label" style="margin-top:20px;">Management</div>
        <div class="sec-title">Add New User</div>
        """, unsafe_allow_html=True)
        n1, n2, n3 = st.columns(3)
        with n1: nu = st.text_input("Username", key="nu")
        with n2: np_ = st.text_input("Password", type="password", key="np")
        with n3: nr = st.selectbox("Role", ["user","admin"], key="nr")
        if st.button("➕  Create User"):
            if db.register_user(nu.strip(), np_.strip(), nr):
                st.success(f"✅  User '{nu}' created.")
                st.rerun()
            else:
                st.error("Username already exists.")

    with at2:
        all_bks = db.get_books(role="admin")
        df_ab   = pd.DataFrame(all_bks)
        if not df_ab.empty:
            cols = [c for c in ["title","author","username","word_count","language","uploaded_at"]
                    if c in df_ab.columns]
            st.dataframe(df_ab[cols], use_container_width=True, hide_index=True)
        else:
            st.info("No books in system yet.")

    with at3:
        logs = db.get_logs(limit=200)
        df_l = pd.DataFrame(logs)
        if not df_l.empty:
            cols = [c for c in ["timestamp","username","action","detail"] if c in df_l.columns]
            st.dataframe(df_l[cols], use_container_width=True, hide_index=True)
        else:
            st.info("No log entries yet.")

elif "Admin" in page and not is_admin:
    st.error("⛔  Access denied. Admin accounts only.")


# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
    BookIQ &nbsp;·&nbsp; Intelligent Book Summarization Platform &nbsp;·&nbsp;
    NLP + TF-IDF &nbsp;·&nbsp; NLTK + SQLite + Streamlit + Plotly
</div>
""", unsafe_allow_html=True)
