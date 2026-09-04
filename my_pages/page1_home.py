# ============================================================
# page1_home.py — Home Page
# Pipeline Inspection System
# ============================================================

import streamlit as st
import json
import requests
from streamlit_lottie import st_lottie
from config import CLASS_ICONS, THEME


def load_lottie_url(url: str):
    """Lottie animation URL မှ load လုပ်တယ်"""
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except:
        return None


def load_lottie_file(path: str):
    """Lottie animation file မှ load လုပ်တယ်"""
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except:
        return None


def show():
    """Home Page ပြတဲ့ function"""

    # =============================================
    # Lottie Animations Load
    # =============================================
    # Online မှ load (internet ရှိရင်)
    lottie_robot = load_lottie_url(
        "https://assets5.lottiefiles.com/packages/lf20_qp1q7mct.json"
    )
    lottie_scan = load_lottie_url(
        "https://assets9.lottiefiles.com/packages/lf20_gn0tojjn.json"
    )

    # =============================================
    # Hero Section
    # =============================================
    col_left, col_mid, col_right = st.columns([1, 2, 1])

    with col_mid:
        if lottie_robot:
            st_lottie(lottie_robot, height=200, key="robot_hero")

    st.markdown("""
        <div style='text-align: center; padding: 10px 0 30px 0;'>
            <h1 style='
                font-size: 2.8rem;
                font-weight: 700;
                background: linear-gradient(135deg, #0A84FF, #30D5C8);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 8px;
                font-family: Rajdhani, sans-serif;
                letter-spacing: 2px;
            '>
                VISION-BASED PIPELINE INSPECTION SYSTEM
            </h1>
            <p style='
                color: #8899AA;
                font-size: 1.1rem;
                letter-spacing: 1px;
            '>
                AI-Powered Defect Detection using YOLOv8m-p2
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Divider
    st.markdown("""
        <div class='custom-divider'></div>
    """, unsafe_allow_html=True)

    # =============================================
    # System Overview
    # =============================================
    st.markdown("""
        <div class='glass-card fade-in'>
            <h3 style='color: #0A84FF; margin-bottom: 12px;'>
                📌 System Overview
            </h3>
            <p style='color: #C0CFDF; line-height: 1.8; font-size: 1.05rem;'>
                This system uses <b style='color: #0A84FF;'>YOLOv8m-p2</b> deep learning model
                to automatically detect and classify defects inside Gas Pipelines.
                The system can identify <b style='color: #FF4B4B;'>Cracks</b>,
                <b style='color: #FFA500;'>Holes</b>, and
                <b style='color: #FFD700;'>Corrosion</b> in real-time
                from images or video files.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =============================================
    # Model Info Cards (3 columns)
    # =============================================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
            <div class='metric-card'>
                <div style='font-size: 2.5rem; margin-bottom: 8px;'>🤖</div>
                <div class='metric-value'>YOLOv8m-p2</div>
                <div class='metric-label'>Model Architecture</div>
                <div style='color: #8899AA; font-size: 0.85rem; margin-top: 8px;'>
                    ~25.54M Parameters | ~260 GFLOPs (960*960)
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class='metric-card'>
                <div style='font-size: 2.5rem; margin-bottom: 8px;'>🎯</div>
                <div class='metric-value'>3</div>
                <div class='metric-label'>Defect Classes</div>
                <div style='color: #8899AA; font-size: 0.85rem; margin-top: 8px;'>
                    Crack · Hole · Corrosion
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class='metric-card'>
                <div style='font-size: 2.5rem; margin-bottom: 8px;'>🖼️</div>
                <div class='metric-value'>2700+</div>
                <div class='metric-label'>Training Images</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =============================================
    # Detectable Defects
    # =============================================
    st.markdown("""
        <h3 style='color: #F0F4FF; margin-bottom: 16px;'>
            ⚠️ Detectable Defects
        </h3>
    """, unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown("""
            <div class='glass-card' style='text-align: center; border-color: rgba(255,75,75,0.2);'>
                <div style='font-size: 3rem;'>🔴</div>
                <h3 style='color: #FF4B4B; margin: 10px 0 6px 0;'>Crack</h3>
                <p style='color: #8899AA; font-size: 0.9rem;'>
                    အက်ကြောင်းကွဲများ<br>
                    Linear fractures on pipeline surface
                </p>
                <span class='badge badge-crack'>High Risk</span>
            </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
            <div class='glass-card' style='text-align: center; border-color: rgba(255,165,0,0.2);'>
                <div style='font-size: 3rem;'>🟠</div>
                <h3 style='color: #FFA500; margin: 10px 0 6px 0;'>Hole</h3>
                <p style='color: #8899AA; font-size: 0.9rem;'>
                    အပေါက်များ<br>
                    Circular voids through pipeline wall
                </p>
                <span class='badge badge-hole'>Critical</span>
            </div>
        """, unsafe_allow_html=True)

    with col_c:
        st.markdown("""
            <div class='glass-card' style='text-align: center; border-color: rgba(255,215,0,0.2);'>
                <div style='font-size: 3rem;'>🟡</div>
                <h3 style='color: #FFD700; margin: 10px 0 6px 0;'>Corrosion</h3>
                <p style='color: #8899AA; font-size: 0.9rem;'>
                    သံချေးများ<br>
                    Surface degradation and rust formation
                </p>
                <span class='badge badge-corrosion'>Monitor</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =============================================
    # How to Use
    # =============================================
    st.markdown("""
        <div class='glass-card fade-in'>
            <h3 style='color: #0A84FF; margin-bottom: 16px;'>🚀 How to Use</h3>
            <div style='display: grid; gap: 12px;'>
                <div style='display: flex; align-items: center; gap: 16px;'>
                    <div style='
                        background: rgba(10,132,255,0.15);
                        border: 1px solid rgba(10,132,255,0.3);
                        border-radius: 50%;
                        width: 40px; height: 40px;
                        display: flex; align-items: center;
                        justify-content: center;
                        font-weight: 700; color: #0A84FF;
                        flex-shrink: 0;
                    '>1</div>
                    <div>
                        <b style='color: #F0F4FF;'>Detection Page သွားပါ</b>
                        <p style='color: #8899AA; margin: 2px 0 0 0; font-size: 0.9rem;'>
                            Sidebar မှ 🔍 Detection ကို နှိပ်ပါ
                        </p>
                    </div>
                </div>
                <div style='display: flex; align-items: center; gap: 16px;'>
                    <div style='
                        background: rgba(10,132,255,0.15);
                        border: 1px solid rgba(10,132,255,0.3);
                        border-radius: 50%;
                        width: 40px; height: 40px;
                        display: flex; align-items: center;
                        justify-content: center;
                        font-weight: 700; color: #0A84FF;
                        flex-shrink: 0;
                    '>2</div>
                    <div>
                        <b style='color: #F0F4FF;'>Image သို့မဟုတ် Video Upload လုပ်ပါ</b>
                        <p style='color: #8899AA; margin: 2px 0 0 0; font-size: 0.9rem;'>
                            Pipeline inspection image/video ကို upload လုပ်ပါ
                        </p>
                    </div>
                </div>
                <div style='display: flex; align-items: center; gap: 16px;'>
                    <div style='
                        background: rgba(10,132,255,0.15);
                        border: 1px solid rgba(10,132,255,0.3);
                        border-radius: 50%;
                        width: 40px; height: 40px;
                        display: flex; align-items: center;
                        justify-content: center;
                        font-weight: 700; color: #0A84FF;
                        flex-shrink: 0;
                    '>3</div>
                    <div>
                        <b style='color: #F0F4FF;'>Detect လုပ်ပါ</b>
                        <p style='color: #8899AA; margin: 2px 0 0 0; font-size: 0.9rem;'>
                            "Detect" button နှိပ်ပြီး result ကြည့်ပါ
                        </p>
                    </div>
                </div>
                <div style='display: flex; align-items: center; gap: 16px;'>
                    <div style='
                        background: rgba(10,132,255,0.15);
                        border: 1px solid rgba(10,132,255,0.3);
                        border-radius: 50%;
                        width: 40px; height: 40px;
                        display: flex; align-items: center;
                        justify-content: center;
                        font-weight: 700; color: #0A84FF;
                        flex-shrink: 0;
                    '>4</div>
                    <div>
                        <b style='color: #F0F4FF;'>Report Export လုပ်ပါ</b>
                        <p style='color: #8899AA; margin: 2px 0 0 0; font-size: 0.9rem;'>
                            📄 Report page မှ PDF download လုပ်ပါ
                        </p>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # =============================================
    # Scanning Animation + Start Button
    # =============================================
    col_l, col_c2, col_r = st.columns([1, 2, 1])
    with col_c2:
        if lottie_scan:
            st_lottie(lottie_scan, height=150, key="scan_anim")

        if st.button("🔍 Start Detection", use_container_width=True):
            st.session_state['page'] = "🔍 Detection"
            st.rerun()

    # =============================================
    # Footer
    # =============================================
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div class='custom-divider'></div>
        <p style='text-align: center; color: #8899AA; font-size: 0.8rem;'>
            Pipeline Inspection System v1.0 | YOLOv8n | Streamlit
        </p>

    """, unsafe_allow_html=True)
