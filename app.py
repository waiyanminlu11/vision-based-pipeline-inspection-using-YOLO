# ============================================================
# app.py — Main Entry Point
# Pipeline Inspection System
# streamlit run app.py
# ============================================================

'''import streamlit as st
from config import CSS, PROJECT_NAME

# =============================================
# Page Config
# =============================================
st.set_page_config(
    page_title = PROJECT_NAME,
    page_icon  = "🔧",
    layout     = "wide",
    initial_sidebar_state = "expanded"
)

# Apply CSS
st.markdown(CSS, unsafe_allow_html=True)

# Session state initialize
if 'detection_done' not in st.session_state:
    st.session_state['detection_done'] = False
if 'detections' not in st.session_state:
    st.session_state['detections']     = []
if 'result_image' not in st.session_state:
    st.session_state['result_image']   = None

# =============================================
# Sidebar Navigation
# =============================================
with st.sidebar:
    st.markdown("""
        <div style='text-align:center; padding:16px 0 8px 0;'>
            <div style='font-size:2.5rem;'>🔧</div>
            <h2 style='
                color:#0A84FF;
                font-family:Rajdhani,sans-serif;
                font-size:1.3rem;
                font-weight:700;
                letter-spacing:1px;
                margin:4px 0;
            '>
                PIPELINE INSPECTION
            </h2>
            <p style='color:#8899AA; font-size:0.75rem;
                      letter-spacing:0.5px;'>
                AI Defect Detection System
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class='custom-divider'></div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        options=[
            "🏠 Home",
            "🔍 Detection",
            "📊 Results",
            "📄 Report",
            "ℹ️ About"
        ],
        label_visibility = "collapsed"
    )

    st.markdown("""
        <div class='custom-divider'></div>
    """, unsafe_allow_html=True)

    # Detection Status
    if st.session_state.get('detection_done'):
        total = len(st.session_state.get('detections', []))
        st.markdown(f"""
            <div style='
                background:rgba(48,209,88,0.1);
                border:1px solid rgba(48,209,88,0.3);
                border-radius:12px; padding:12px;
                text-align:center;
            '>
                <div style='color:#30D158; font-weight:700;'>
                    ✅ Detection Done
                </div>
                <div style='color:#8899AA; font-size:0.85rem;
                            margin-top:4px;'>
                    {total} defect(s) found
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style='
                background:rgba(255,255,255,0.03);
                border:1px solid rgba(255,255,255,0.07);
                border-radius:12px; padding:12px;
                text-align:center;
            '>
                <div style='color:#8899AA; font-size:0.85rem;'>
                    ⏳ No detection yet
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <p style='color:#8899AA; font-size:0.75rem;
                  text-align:center;'>
            v1.0.0 | YOLOv8n
        </p>
    """, unsafe_allow_html=True)


# =============================================
# Page Routing
# =============================================
if page == "🏠 Home":
    from my_pages import page1_home
    page1_home.show()

elif page == "🔍 Detection":
    from my_pages import page2_detection
    page2_detection.show()

elif page == "📊 Results":
    from my_pages import page3_results
    page3_results.show()

elif page == "📄 Report":
    from my_pages import page4_report
    page4_report.show()

elif page == "ℹ️ About":
    from my_pages import page5_about
    page5_about.show()'''
    
    
    
# ============================================================
# app.py — Main Entry Point (Updated Sidebar + Dark/Light Mode)
# Pipeline Inspection System
# streamlit run app.py
# ============================================================

import streamlit as st
from config import PROJECT_NAME

# =============================================
# Page Config
# =============================================
st.set_page_config(
    page_title = PROJECT_NAME,
    page_icon  = "🔧",
    layout     = "wide",
    initial_sidebar_state = "expanded"
)

# =============================================
# Session State Initialize
# =============================================
if 'detection_done' not in st.session_state:
    st.session_state['detection_done'] = False
if 'detections' not in st.session_state:
    st.session_state['detections']     = []
if 'result_image' not in st.session_state:
    st.session_state['result_image']   = None
if 'dark_mode' not in st.session_state:
    st.session_state['dark_mode']      = True

# =============================================
# Theme Colors
# =============================================
dark_theme = {
    "bg"         : "#0A0E1A",
    "bg2"        : "#111827",
    "card"       : "rgba(255,255,255,0.04)",
    "border"     : "rgba(255,255,255,0.08)",
    "text"       : "#F0F4FF",
    "text_dim"   : "#8899AA",
    "primary"    : "#0A84FF",
    "sidebar_bg" : "rgba(10,14,26,0.98)",
    "nav_hover"  : "rgba(10,132,255,0.15)",
    "nav_active" : "rgba(10,132,255,0.25)",
    "nav_border" : "rgba(10,132,255,0.5)",
    "toggle_bg"  : "#1C2333",
}

light_theme = {
    "bg"         : "#F0F4FF",
    "bg2"        : "#E8EEF8",
    "card"       : "rgba(255,255,255,0.9)",
    "border"     : "rgba(0,0,0,0.1)",
    "text"       : "#0A0E1A",
    "text_dim"   : "#4A5568",
    "primary"    : "#0A84FF",
    "sidebar_bg" : "rgba(240,244,255,0.98)",
    "nav_hover"  : "rgba(10,132,255,0.1)",
    "nav_active" : "rgba(10,132,255,0.2)",
    "nav_border" : "rgba(10,132,255,0.6)",
    "toggle_bg"  : "#E2E8F0",
}

T = dark_theme if st.session_state['dark_mode'] else light_theme

# =============================================
# CSS
# =============================================
css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&display=swap');

/* ── App background ── */
.stApp {{
    background: {T['bg']};
    color: {T['text']};
    font-family: 'Rajdhani', sans-serif;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: {T['sidebar_bg']} !important;
    border-right: 1px solid {T['border']};
    backdrop-filter: blur(20px);
}}

[data-testid="stSidebar"] > div:first-child {{
    padding-top: 0 !important;
}}

/* ── Hide default streamlit elements ── */
#MainMenu {{ visibility: hidden; }}
footer    {{ visibility: hidden; }}
header    {{ visibility: hidden; }}

/* ── Navigation button ── */
.nav-btn {{
    display: flex;
    align-items: center;
    gap: 12px;
    width: 100%;
    padding: 14px 18px;
    margin: 4px 0;
    border-radius: 14px;
    border: 1px solid transparent;
    background: transparent;
    color: {T['text_dim']};
    font-family: 'Rajdhani', sans-serif;
    font-size: 16px;
    font-weight: 600;
    letter-spacing: 0.5px;
    cursor: pointer;
    transition: all 0.2s ease;
    text-decoration: none;
}}

.nav-btn:hover {{
    background: {T['nav_hover']};
    color: {T['text']};
    border-color: {T['border']};
}}

.nav-btn.active {{
    background: {T['nav_active']};
    color: {T['primary']};
    border-color: {T['nav_border']};
    box-shadow: 0 2px 12px rgba(10,132,255,0.15);
}}

.nav-icon {{
    font-size: 20px;
    width: 28px;
    text-align: center;
    flex-shrink: 0;
}}

/* ── Status badge ── */
.status-badge {{
    background: rgba(48,209,88,0.12);
    border: 1px solid rgba(48,209,88,0.3);
    border-radius: 20px;
    padding: 6px 14px;
    color: #30D158;
    font-size: 12px;
    font-weight: 600;
    text-align: center;
}}

.status-badge-idle {{
    background: rgba(255,255,255,0.04);
    border: 1px solid {T['border']};
    border-radius: 20px;
    padding: 6px 14px;
    color: {T['text_dim']};
    font-size: 12px;
    text-align: center;
}}

/* ── Toggle button ── */
.stButton > button {{
    background: {T['nav_active']} !important;
    border: 1px solid {T['nav_border']} !important;
    border-radius: 12px !important;
    color: {T['primary']} !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}}

.stButton > button:hover {{
    background: rgba(10,132,255,0.35) !important;
    box-shadow: 0 4px 15px rgba(10,132,255,0.25) !important;
}}

/* ── Divider ── */
.custom-divider {{
    height: 1px;
    background: linear-gradient(90deg,
        transparent 0%,
        {T['border']} 50%,
        transparent 100%);
    margin: 12px 0;
}}

/* ── Scrollbar ── */
::-webkit-scrollbar       {{ width: 4px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{
    background: rgba(10,132,255,0.3);
    border-radius: 2px;
}}

/* ── Glass card ── */
.glass-card {{
    background: {T['card']};
    backdrop-filter: blur(20px);
    border: 1px solid {T['border']};
    border-radius: 20px;
    padding: 24px;
    margin: 12px 0;
    transition: all 0.3s ease;
}}

/* ── Metric card ── */
.metric-card {{
    background: {T['card']};
    border: 1px solid {T['border']};
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    transition: all 0.3s ease;
}}

.metric-value {{
    font-size: 2.2rem;
    font-weight: 700;
    color: {T['primary']};
    font-family: 'Rajdhani', sans-serif;
    line-height: 1;
}}

.metric-label {{
    font-size: 0.85rem;
    color: {T['text_dim']};
    margin-top: 6px;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

/* ── Badge ── */
.badge-crack      {{ display:inline-block; padding:4px 12px; border-radius:20px; font-size:0.75rem; font-weight:600; background:rgba(255,75,75,0.2); color:#FF4B4B; border:1px solid rgba(255,75,75,0.3); }}
.badge-hole       {{ display:inline-block; padding:4px 12px; border-radius:20px; font-size:0.75rem; font-weight:600; background:rgba(255,165,0,0.2); color:#FFA500; border:1px solid rgba(255,165,0,0.3); }}
.badge-corrosion  {{ display:inline-block; padding:4px 12px; border-radius:20px; font-size:0.75rem; font-weight:600; background:rgba(255,215,0,0.2); color:#FFD700; border:1px solid rgba(255,215,0,0.3); }}

/* ── Custom divider line ── */
.glow-divider {{
    height: 2px;
    background: linear-gradient(90deg, transparent, {T['primary']}, transparent);
    margin: 8px 0 16px 0;
}}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# =============================================
# Navigation Pages
# =============================================
pages = [
    ("🏠", "Home",      "home"),
    ("🔍", "Detection", "detection"),
    ("📊", "Results",   "results"),
    ("📄", "Report",    "report"),
    ("ℹ️",  "About",    "about"),
]

if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "home"

# =============================================
# Sidebar
# =============================================
with st.sidebar:

    # Logo + Title
    st.markdown(f"""
        <div style='padding: 24px 16px 8px 16px; text-align: center;'>
            <div style='font-size: 2.8rem; margin-bottom: 6px;'>🔧</div>
            <div style='
                color: {T['primary']};
                font-family: Rajdhani, sans-serif;
                font-size: 1.1rem;
                font-weight: 700;
                letter-spacing: 2px;
                line-height: 1.2;
            '>PIPELINE<br>INSPECTION</div>
            <div style='
                color: {T['text_dim']};
                font-size: 0.72rem;
                letter-spacing: 0.5px;
                margin-top: 4px;
            '>AI Defect Detection System</div>
        </div>
        <div class='glow-divider'></div>
    """, unsafe_allow_html=True)

    # Navigation Buttons
    st.markdown("<div style='padding: 0 8px;'>", unsafe_allow_html=True)

    for icon, label, key in pages:
        is_active = st.session_state['current_page'] == key
        btn_class = "nav-btn active" if is_active else "nav-btn"

        if st.button(
            f"{icon}  {label}",
            key        = f"nav_{key}",
            use_container_width = True,
        ):
            st.session_state['current_page'] = key
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Divider
    st.markdown("<div class='custom-divider' style='margin: 16px 8px;'></div>",
                unsafe_allow_html=True)

    # Detection Status
    if st.session_state.get('detection_done'):
        total = len(st.session_state.get('detections', []))
        st.markdown(f"""
            <div style='padding: 0 8px;'>
                <div class='status-badge'>
                    ✅ Detection Done — {total} defect(s)
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style='padding: 0 8px;'>
                <div class='status-badge-idle'>
                    ⏳ No detection yet
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Divider
    st.markdown("<div class='custom-divider' style='margin: 16px 8px;'></div>",
                unsafe_allow_html=True)

    # Dark / Light Mode Toggle
    col_icon, col_btn = st.columns([1, 3])
    with col_icon:
        mode_icon = "🌙" if st.session_state['dark_mode'] else "☀️"
        st.markdown(f"""
            <div style='font-size: 1.4rem; padding-top: 6px;
                        text-align: center;'>{mode_icon}</div>
        """, unsafe_allow_html=True)
    with col_btn:
        mode_label = "Light Mode" if st.session_state['dark_mode'] else "Dark Mode"
        if st.button(mode_label, key="theme_toggle",
                     use_container_width=True):
            st.session_state['dark_mode'] = not st.session_state['dark_mode']
            st.rerun()

    # Version footer
    st.markdown(f"""
        <div style='text-align:center; padding: 12px 0 4px 0;'>
            <span style='color:{T['text_dim']}; font-size:0.7rem;'>
                v1.0.0 · YOLOv8
            </span>
        </div>
    """, unsafe_allow_html=True)

# =============================================
# Page Routing
# =============================================
page = st.session_state['current_page']

if page == "home":
    from my_pages import page1_home
    page1_home.show()
elif page == "detection":
    from my_pages import page2_detection
    page2_detection.show()
elif page == "results":
    from my_pages import page3_results
    page3_results.show()
elif page == "report":
    from my_pages import page4_report
    page4_report.show()
elif page == "about":
    from my_pages import page5_about
    page5_about.show()

