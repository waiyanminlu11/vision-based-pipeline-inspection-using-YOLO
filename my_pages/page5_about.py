# ============================================================
# page5_about.py — About Page
# Pipeline Inspection System
# ============================================================

import streamlit as st
import json
import os
from streamlit_lottie import st_lottie
from config import (
    PROJECT_NAME, PROJECT_VERSION,
    PROJECT_DESC, AUTHOR, ASSETS_DIR
)


def load_lottie(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except:
        return None


def show():

    lottie_robot = load_lottie(
        os.path.join(ASSETS_DIR, "robot.json")
    )

    # Page Header
    st.markdown("""
        <div style='margin-bottom:24px;'>
            <h2 style='color:#F0F4FF; font-family:Rajdhani,sans-serif;
                       font-size:2rem; font-weight:700; letter-spacing:1px;'>
                ℹ️ About
            </h2>
            <p style='color:#8899AA;'>
                Project အကြောင်း အသေးစိတ် ဖော်ပြချက်
            </p>
        </div>
    """, unsafe_allow_html=True)

    # =============================================
    # Hero
    # =============================================
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        if lottie_robot:
            st_lottie(lottie_robot, height=180, key="about_robot")

    st.markdown(f"""
        <div style='text-align:center; margin-bottom:32px;'>
            <h1 style='
                font-size:2.2rem; font-weight:700;
                background:linear-gradient(135deg, #0A84FF, #30D5C8);
                -webkit-background-clip:text;
                -webkit-text-fill-color:transparent;
                font-family:Rajdhani,sans-serif;
                letter-spacing:2px;
            '>
                {PROJECT_NAME}
            </h1>
            <p style='color:#8899AA; font-size:1rem;'>
                Version {PROJECT_VERSION}
            </p>
            <p style='color:#C0CFDF; font-size:1.05rem;
                      max-width:600px; margin:0 auto;'>
                {PROJECT_DESC}
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class='custom-divider'></div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =============================================
    # Project Overview
    # =============================================
    st.markdown("""
        <h3 style='color:#F0F4FF; margin-bottom:16px;'>
            📌 Project Overview
        </h3>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class='glass-card'>
            <p style='color:#C0CFDF; line-height:1.9; font-size:1.05rem;'>
                This system is designed to detect and classify defects inside
                gas pipelines using computer vision and deep learning.
                The system uses <b style='color:#0A84FF;'>YOLOv8m-p2</b>
                (You Only Look Once) object detection model trained on
                pipeline inspection images to identify three types of defects:
                <b style='color:#FF4B4B;'>Cracks</b>,
                <b style='color:#FFA500;'>Holes</b>, and
                <b style='color:#FFD700;'>Corrosion</b>.
            </p>
            <p style='color:#C0CFDF; line-height:1.9; font-size:1.05rem;
                      margin-top:12px;'>
                The model was trained with online datasets to ensure robust detection under low-light conditions of
                inside pipelines. The system provides real-time detection,
                detailed analysis, and PDF report generation.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =============================================
    # Technical Specs
    # =============================================
    st.markdown("""
        <h3 style='color:#F0F4FF; margin-bottom:16px;'>
            ⚙️ Technical Specifications
        </h3>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        specs_model = [
            ("Model",           "YOLOv8m-p2"),
            ("Parameters",      "~25.54 Million"),
            ("GFLOPs",          "~260 GFLOPs"),
            ("Input Size",      "960 × 960"),
            ("Classes",         "3 (Crack, Hole, Corrosion)"),
            ("Conf Threshold",  "0.10"),
        ]
        st.markdown("""
            <div class='glass-card'>
                <h4 style='color:#0A84FF; margin-bottom:12px;'>
                    🤖 Model Info
                </h4>
        """, unsafe_allow_html=True)
        for key, val in specs_model:
            st.markdown(f"""
                <div style='display:flex; justify-content:space-between;
                            padding:8px 0;
                            border-bottom:1px solid rgba(255,255,255,0.05);'>
                    <span style='color:#8899AA;'>{key}</span>
                    <span style='color:#F0F4FF; font-weight:600;'>{val}</span>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        specs_dataset = [
            ("Original Dataset",  "~3,400 images"),
            ("Augmented Dataset", "~24,000 images(Online Augmentation(On-the-fly Augmentation))"),
            ("Train Split",       "70%"),
            ("Val Split",         "20%"),
            ("Test Split",        "10%"),
            ("Augmentation",      "HSV Color, Rotation, Translate, Scale, Perspective, Mosaic, Mixup"),
        ]
        st.markdown("""
            <div class='glass-card'>
                <h4 style='color:#0A84FF; margin-bottom:12px;'>
                    📁 Dataset Info
                </h4>
        """, unsafe_allow_html=True)
        for key, val in specs_dataset:
            st.markdown(f"""
                <div style='display:flex; justify-content:space-between;
                            padding:8px 0;
                            border-bottom:1px solid rgba(255,255,255,0.05);'>
                    <span style='color:#8899AA;'>{key}</span>
                    <span style='color:#F0F4FF; font-weight:600;'>{val}</span>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =============================================
    # Tech Stack
    # =============================================
    st.markdown("""
        <h3 style='color:#F0F4FF; margin-bottom:16px;'>
            🛠️ Technology Stack
        </h3>
    """, unsafe_allow_html=True)

    tech_stack = [
        ("🤖", "YOLOv8m-p2",  "Object Detection Model",  "#0A84FF"),
        ("🐍", "Python",      "Programming Language",     "#FFD700"),
        ("🎈", "Streamlit",   "Web UI Framework",         "#FF4B4B"),
        ("👁️", "OpenCV",      "Image Processing",         "#30D5C8"),
        ("🔦", "PyTorch",     "Deep Learning Framework",  "#FFA500"),
        ("📊", "Plotly",      "Interactive Charts",       "#30D158"),
        ("📄", "ReportLab",   "PDF Generation",           "#8899AA"),
    ]

    cols = st.columns(4)
    for i, (icon, name, desc, color) in enumerate(tech_stack):
        with cols[i % 4]:
            st.markdown(f"""
                <div class='glass-card' style='
                    text-align:center; padding:16px 12px;
                    border-color:{color}33;
                    margin-bottom:8px;
                '>
                    <div style='font-size:2rem;
                                margin-bottom:6px;'>{icon}</div>
                    <div style='color:{color}; font-weight:700;
                                font-size:1rem;'>{name}</div>
                    <div style='color:#8899AA; font-size:0.78rem;
                                margin-top:4px;'>{desc}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =============================================
    # Defect Classes Detail
    # =============================================
    st.markdown("""
        <h3 style='color:#F0F4FF; margin-bottom:16px;'>
            ⚠️ Defect Classes
        </h3>
    """, unsafe_allow_html=True)

    defects = [
        (
            "🔴", "Crack", "#FF4B4B",
            "Linear fractures on the pipeline inner wall surface. "
            "Cracks can propagate over time due to pressure and "
            "environmental factors, leading to pipeline failure.",
            "High Risk — Schedule maintenance within 24-48 hours."
        ),
        (
            "🟠", "Hole", "#FFA500",
            "Circular or irregular voids through the pipeline wall. "
            "Holes indicate complete material loss and pose immediate "
            "risk of gas leakage and environmental hazard.",
            "Critical — Immediate shutdown and repair required."
        ),
        (
            "🟡", "Corrosion", "#FFD700",
            "Surface degradation due to chemical reactions with "
            "moisture and environmental agents. Corrosion weakens "
            "the pipeline wall and can lead to cracks and holes.",
            "Monitor — Apply anti-corrosion treatment and re-inspect."
        ),
    ]

    for icon, name, color, desc, action in defects:
        st.markdown(f"""
            <div class='glass-card' style='
                margin-bottom:12px;
                border-left:4px solid {color};
            '>
                <div style='display:flex; align-items:flex-start;
                            gap:16px;'>
                    <div style='font-size:2.5rem;'>{icon}</div>
                    <div style='flex:1;'>
                        <h4 style='color:{color}; margin:0 0 8px 0;
                                   font-size:1.2rem;'>{name}</h4>
                        <p style='color:#C0CFDF; margin:0 0 8px 0;
                                  line-height:1.7; font-size:0.95rem;'>
                            {desc}
                        </p>
                        <div style='
                            background:rgba(255,255,255,0.04);
                            border-radius:8px; padding:8px 12px;
                            border:1px solid {color}33;
                        '>
                            <span style='color:#8899AA;
                                         font-size:0.85rem;'>
                                Action: </span>
                            <span style='color:{color};
                                         font-size:0.85rem;
                                         font-weight:600;'>
                                {action}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =============================================
    # Author / Team
    # =============================================
    st.markdown("""<div class='custom-divider'></div>""",
                unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(f"""
        <div class='glass-card' style='text-align:center;'>
            <div style='font-size:3rem; margin-bottom:12px;'>👨‍💻</div>
            <h3 style='color:#F0F4FF; margin-bottom:4px;'>
                {AUTHOR}
            </h3>
            <p style='color:#8899AA;'>
                Pipeline Inspection AI System Developer
            </p>
            <div style='margin-top:16px;'>
                <span style='
                    background:rgba(10,132,255,0.1);
                    border:1px solid rgba(10,132,255,0.3);
                    border-radius:20px;
                    padding:4px 16px;
                    color:#0A84FF;
                    font-size:0.9rem;
                '>
                    🔧 Precision Engineer , Computer Vision , AI , Robotics
                </span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # =============================================
    # Footer
    # =============================================
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
        <p style='text-align:center; color:#8899AA; font-size:0.8rem;'>
            {PROJECT_NAME} v{PROJECT_VERSION} |
            Built with ❤️ using Streamlit & YOLOv8m-p2
        </p>
    """, unsafe_allow_html=True)
