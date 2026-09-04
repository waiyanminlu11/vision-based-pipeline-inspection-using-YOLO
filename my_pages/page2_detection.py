# ============================================================
# page2_detection.py — Detection Page
# Pipeline Inspection System (Desktop Version)
# ============================================================

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import json
import time
import os
from streamlit_lottie import st_lottie
import tempfile

from modules.detector import (
    load_model,
    draw_boxes,
    detect_image,
    get_class_counts,
)
from config import (
    MODELS, CONF_THRESHOLD, IOU_THRESHOLD,
    IMG_SIZE, CLASS_COLORS, CLASS_ICONS, ASSETS_DIR
)


def load_lottie(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except:
        return None


def show_detection_summary(detections):
    """Detection result summary ပြတယ်"""

    if not detections:
        st.markdown("""
            <div class='glass-card' style='text-align:center;'>
                <div style='font-size:3rem;'>✅</div>
                <h3 style='color:#30D158;'>No Defects Detected</h3>
                <p style='color:#8899AA;'>Pipeline ကောင်းနေပါတယ်</p>
            </div>
        """, unsafe_allow_html=True)
        return

    counts = get_class_counts(detections)

    # Count cards
    col1, col2, col3 = st.columns(3)
    cards = [
        (col1, "Crack",     "#FF4B4B"),
        (col2, "Hole",      "#FFA500"),
        (col3, "Corrosion", "#FFD700"),
    ]
    for col, cls_name, color in cards:
        with col:
            icon = CLASS_ICONS.get(cls_name, "")
            st.markdown(f"""
                <div class='metric-card'>
                    <div style='font-size:2rem;'>{icon}</div>
                    <div class='metric-value' style='color:{color};'>
                        {counts[cls_name]}
                    </div>
                    <div class='metric-label'>{cls_name}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <h4 style='color:#F0F4FF; margin-bottom:12px;'>
            📋 Detection Details
        </h4>
    """, unsafe_allow_html=True)

    for d in detections:
        color        = CLASS_COLORS.get(d["class"], "#FFFFFF")
        x1,y1,x2,y2 = d["bbox"]

        st.markdown(f"""
            <div class='glass-card' style='
                padding:14px 20px; margin:6px 0;
                border-left:3px solid {color};
            '>
                <div style='display:flex; justify-content:space-between;
                            align-items:center;'>
                    <span style='color:{color}; font-weight:700;
                                 font-size:1.1rem;'>
                        {d['icon']} {d['class']}
                    </span>
                    <span style='
                        background:rgba(255,255,255,0.05);
                        padding:4px 12px; border-radius:20px;
                        color:#30D158; font-weight:600;'>
                        {d['confidence']:.1%}
                    </span>
                </div>
                <div style='color:#8899AA; font-size:0.85rem;
                            margin-top:4px;'>
                    Location: ({x1}, {y1}) → ({x2}, {y2})
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.session_state['detections']     = detections
    st.session_state['detection_done'] = True


def show():

    lottie_scanning = load_lottie(
        os.path.join(ASSETS_DIR, "scanning.json")
    )
    lottie_success = load_lottie(
        os.path.join(ASSETS_DIR, "success.json")
    )

    st.markdown("""
        <div style='margin-bottom:24px;'>
            <h2 style='color:#F0F4FF; font-family:Rajdhani,sans-serif;
                       font-size:2rem; font-weight:700; letter-spacing:1px;'>
                🔍 Pipeline Defect Detection
            </h2>
            <p style='color:#8899AA;'>
                Image သို့မဟုတ် Video upload လုပ်ပြီး
                Defects တွေ Detect လုပ်ပါ
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Settings
    with st.expander("⚙️ Detection Settings", expanded=False):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            selected_model = st.selectbox(
                "Model ရွေးပါ", list(MODELS.keys())
            )
            st.caption(f"📁 {MODELS[selected_model]['desc']}")
        with col_s2:
            conf_thresh = st.slider(
                "Confidence Threshold",
                min_value = 0.10,
                max_value = 0.90,
                value     = CONF_THRESHOLD,
                step      = 0.05,
                format    = "%.2f"
            )

    model_path = MODELS[selected_model]["path"]
    if not os.path.exists(model_path):
        st.warning(f"⚠️ Model file မတွေ့ဘူး: {model_path}")
        st.info("models/ folder ထဲမှာ best.pt ထည့်ပါ")
        return

    model = load_model(model_path)
    if model is None:
        return

    st.markdown("<br>", unsafe_allow_html=True)

    tab_img, tab_vid = st.tabs(["🖼️ Image", "🎥 Video"])

    # IMAGE TAB
    with tab_img:
        uploaded_img = st.file_uploader(
            "Pipeline image upload လုပ်ပါ",
            type             = ["jpg", "jpeg", "png"],
            key              = "img_upload",
            label_visibility = "collapsed"
        )

        if uploaded_img:
            image = Image.open(uploaded_img).convert("RGB")

            col_orig, col_result = st.columns(2)
            with col_orig:
                st.markdown("""
                    <p style='color:#8899AA; font-size:0.9rem;
                    text-align:center;'>Original Image</p>
                """, unsafe_allow_html=True)
                st.image(image, use_column_width=True)

            st.markdown("<br>", unsafe_allow_html=True)
            detect_btn = st.button(
                "🔍 Detect Defects",
                use_container_width=True,
                key="detect_img"
            )

            if detect_btn:
                placeholder = st.empty()
                with placeholder.container():
                    if lottie_scanning:
                        c1, c2, c3 = st.columns([1, 2, 1])
                        with c2:
                            st_lottie(
                                lottie_scanning,
                                height=150,
                                key="scan_run"
                            )
                    else:
                        st.info("🔍 Analyzing pipeline...")

                time.sleep(0.5)

                result_img, detections = detect_image(
                    model, image,
                    conf  = conf_thresh,
                    iou   = IOU_THRESHOLD,
                    imgsz = IMG_SIZE
                )

                placeholder.empty()

                with col_result:
                    st.markdown("""
                        <p style='color:#0A84FF; font-size:0.9rem;
                        text-align:center; font-weight:600;'>
                        Detection Result</p>
                    """, unsafe_allow_html=True)
                    st.image(result_img, use_column_width=True)

                if lottie_success and detections:
                    c1, c2, c3 = st.columns([1, 2, 1])
                    with c2:
                        st_lottie(
                            lottie_success,
                            height=100,
                            key="success_anim",
                            loop=False
                        )

                st.markdown("<br>", unsafe_allow_html=True)
                show_detection_summary(detections)
                st.session_state['result_image'] = result_img

    # VIDEO TAB
    with tab_vid:
        uploaded_vid = st.file_uploader(
            "Pipeline video upload လုပ်ပါ",
            type             = ["mp4", "avi", "mov"],
            key              = "vid_upload",
            label_visibility = "collapsed"
        )

        if uploaded_vid:
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, uploaded_vid.name)
            #temp_path = f"/tmp/{uploaded_vid.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_vid.read())

            st.video(temp_path)

            detect_vid_btn = st.button(
                "🔍 Detect in Video",
                use_container_width=True,
                key="detect_vid"
            )

            if detect_vid_btn:
                cap            = cv2.VideoCapture(temp_path)
                total_frames   = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                all_detections = []
                progress_bar   = st.progress(0)
                frame_display  = st.empty()
                status_text    = st.empty()
                frame_idx      = 0

                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break

                    if frame_idx % 5 == 0:
                        rgb_frame = cv2.cvtColor(
                            frame, cv2.COLOR_BGR2RGB
                        )
                        pil_frame = Image.fromarray(rgb_frame)

                        r_frame, dets = detect_image(
                            model, pil_frame,
                            conf  = conf_thresh,
                            iou   = IOU_THRESHOLD,
                            imgsz = IMG_SIZE
                        )
                        all_detections.extend(dets)
                        frame_display.image(
                            r_frame, use_column_width=True
                        )

                    progress_bar.progress(
                        min((frame_idx+1)/total_frames, 1.0)
                    )
                    status_text.text(
                        f"Frame {frame_idx+1}/{total_frames}"
                    )
                    frame_idx += 1

                cap.release()
                progress_bar.empty()
                status_text.empty()

                st.success("✅ Video detection ပြီးပါပြီ!")
                show_detection_summary(all_detections)
                st.session_state['detections']     = all_detections
                st.session_state['detection_done'] = True

