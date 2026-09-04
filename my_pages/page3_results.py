# ============================================================
# page3_results.py — Results & Analysis Page
# Pipeline Inspection System
# ============================================================

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import json
import os
from streamlit_lottie import st_lottie
from config import CLASS_COLORS, CLASS_ICONS, ASSETS_DIR


def load_lottie(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except:
        return None


def get_class_counts(detections):
    """Detection တွေကနေ class count တွက်တယ်"""
    counts = {"Crack": 0, "Hole": 0, "Corrosion": 0}
    for d in detections:
        if d["class"] in counts:
            counts[d["class"]] += 1
    return counts


def get_confidence_stats(detections):
    """Confidence statistics တွက်တယ်"""
    stats = {}
    for cls in ["Crack", "Hole", "Corrosion"]:
        confs = [d["confidence"] for d in detections
                 if d["class"] == cls]
        if confs:
            stats[cls] = {
                "mean" : np.mean(confs),
                "max"  : np.max(confs),
                "min"  : np.min(confs),
                "count": len(confs)
            }
    return stats


def plot_donut_chart(counts):
    """Donut chart — defect distribution"""
    labels = list(counts.keys())
    values = list(counts.values())
    colors = [CLASS_COLORS.get(k, "#FFFFFF") for k in labels]

    fig = go.Figure(data=[go.Pie(
        labels    = labels,
        values    = values,
        hole      = 0.6,
        marker    = dict(colors=colors,
                         line=dict(color='rgba(0,0,0,0)', width=0)),
        textinfo  = 'label+percent',
        textfont  = dict(color='#F0F4FF', size=13),
        hovertemplate = "<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>"
    )])

    fig.update_layout(
        paper_bgcolor = 'rgba(0,0,0,0)',
        plot_bgcolor  = 'rgba(0,0,0,0)',
        font          = dict(color='#F0F4FF'),
        showlegend    = True,
        legend        = dict(
            font      = dict(color='#F0F4FF'),
            bgcolor   = 'rgba(0,0,0,0)',
        ),
        margin        = dict(t=20, b=20, l=20, r=20),
        height        = 320,
        annotations   = [dict(
            text      = f"<b>{sum(values)}</b><br>Total",
            x=0.5, y=0.5,
            font      = dict(size=18, color='#F0F4FF'),
            showarrow = False
        )]
    )
    return fig


def plot_bar_chart(counts):
    """Bar chart — defect count per class"""
    classes = list(counts.keys())
    values  = list(counts.values())
    colors  = [CLASS_COLORS.get(k, "#FFFFFF") for k in classes]

    fig = go.Figure(data=[go.Bar(
        x             = classes,
        y             = values,
        marker_color  = colors,
        marker_line   = dict(width=0),
        text          = values,
        textposition  = 'outside',
        textfont      = dict(color='#F0F4FF', size=14),
        hovertemplate = "<b>%{x}</b><br>Count: %{y}<extra></extra>"
    )])

    fig.update_layout(
        paper_bgcolor = 'rgba(0,0,0,0)',
        plot_bgcolor  = 'rgba(0,0,0,0)',
        font          = dict(color='#F0F4FF'),
        xaxis         = dict(
            showgrid      = False,
            tickfont      = dict(color='#F0F4FF', size=13)
        ),
        yaxis         = dict(
            showgrid      = True,
            gridcolor     = 'rgba(255,255,255,0.05)',
            tickfont      = dict(color='#8899AA')
        ),
        margin        = dict(t=30, b=20, l=20, r=20),
        height        = 280,
    )
    return fig


def plot_confidence_chart(conf_stats):
    """Confidence bar chart per class"""
    if not conf_stats:
        return None

    classes = list(conf_stats.keys())
    means   = [conf_stats[c]["mean"] * 100 for c in classes]
    maxs    = [conf_stats[c]["max"]  * 100 for c in classes]
    colors  = [CLASS_COLORS.get(c, "#FFFFFF") for c in classes]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name         = 'Mean Confidence',
        x            = classes,
        y            = means,
        marker_color = colors,
        opacity      = 0.7,
        text         = [f"{v:.1f}%" for v in means],
        textposition = 'outside',
        textfont     = dict(color='#F0F4FF'),
    ))

    fig.add_trace(go.Bar(
        name         = 'Max Confidence',
        x            = classes,
        y            = maxs,
        marker_color = colors,
        opacity      = 0.4,
        text         = [f"{v:.1f}%" for v in maxs],
        textposition = 'outside',
        textfont     = dict(color='#F0F4FF'),
    ))

    fig.update_layout(
        paper_bgcolor = 'rgba(0,0,0,0)',
        plot_bgcolor  = 'rgba(0,0,0,0)',
        font          = dict(color='#F0F4FF'),
        barmode       = 'group',
        legend        = dict(
            font      = dict(color='#F0F4FF'),
            bgcolor   = 'rgba(0,0,0,0)',
        ),
        xaxis         = dict(
            showgrid  = False,
            tickfont  = dict(color='#F0F4FF')
        ),
        yaxis         = dict(
            showgrid  = True,
            gridcolor = 'rgba(255,255,255,0.05)',
            tickfont  = dict(color='#8899AA'),
            range     = [0, 110],
            ticksuffix= '%'
        ),
        margin        = dict(t=30, b=20, l=20, r=20),
        height        = 280,
    )
    return fig


def show():

    lottie_chart = load_lottie(
        os.path.join(ASSETS_DIR, "chart.json")
    )

    # Page Header
    st.markdown("""
        <div style='margin-bottom:24px;'>
            <h2 style='color:#F0F4FF; font-family:Rajdhani,sans-serif;
                       font-size:2rem; font-weight:700; letter-spacing:1px;'>
                📊 Results & Analysis
            </h2>
            <p style='color:#8899AA;'>
                Detection ရလဒ်တွေကို အသေးစိတ် ခွဲခြမ်းစိတ်ဖြာပြတဲ့ page
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Detection မလုပ်ရသေးဘူးဆိုရင်
    if not st.session_state.get('detection_done'):
        st.markdown("""
            <div class='glass-card' style='text-align:center; padding:48px;'>
                <div style='font-size:4rem; margin-bottom:16px;'>🔍</div>
                <h3 style='color:#F0F4FF;'>Detection မလုပ်ရသေးဘူး</h3>
                <p style='color:#8899AA;'>
                    Detection page မှ image/video upload လုပ်ပြီး
                    detect လုပ်ပါ
                </p>
            </div>
        """, unsafe_allow_html=True)

        col_l, col_c, col_r = st.columns([1, 2, 1])
        with col_c:
            if st.button("🔍 Detection Page သွား",
                         use_container_width=True):
                st.session_state['page'] = "🔍 Detection"
                st.rerun()
        return

    # Detection data ယူ
    detections = st.session_state.get('detections', [])
    counts     = get_class_counts(detections)
    conf_stats = get_confidence_stats(detections)

    # =============================================
    # Summary Metrics
    # =============================================
    total    = sum(counts.values())
    severity = "Critical ⚠️" if counts.get("Hole", 0) > 0 \
               else "High Risk 🔴" if counts.get("Crack", 0) > 0 \
               else "Monitor 🟡" if counts.get("Corrosion", 0) > 0 \
               else "OK ✅"

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size:2rem;'>🎯</div>
                <div class='metric-value'>{total}</div>
                <div class='metric-label'>Total Defects</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class='metric-card'
                 style='border-color:rgba(255,75,75,0.2);'>
                <div style='font-size:2rem;'>🔴</div>
                <div class='metric-value' style='color:#FF4B4B;'>
                    {counts.get('Crack', 0)}
                </div>
                <div class='metric-label'>Crack</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class='metric-card'
                 style='border-color:rgba(255,165,0,0.2);'>
                <div style='font-size:2rem;'>🟠</div>
                <div class='metric-value' style='color:#FFA500;'>
                    {counts.get('Hole', 0)}
                </div>
                <div class='metric-label'>Hole</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
            <div class='metric-card'
                 style='border-color:rgba(255,215,0,0.2);'>
                <div style='font-size:2rem;'>🟡</div>
                <div class='metric-value' style='color:#FFD700;'>
                    {counts.get('Corrosion', 0)}
                </div>
                <div class='metric-label'>Corrosion</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Severity
    sev_color = "#FF453A" if "Critical" in severity \
                else "#FF4B4B" if "High" in severity \
                else "#FFD700" if "Monitor" in severity \
                else "#30D158"

    st.markdown(f"""
        <div class='glass-card' style='
            text-align:center;
            border-color:{sev_color}44;
            padding:16px;
        '>
            <span style='color:#8899AA; font-size:0.9rem;'>
                Severity Level
            </span>
            <h3 style='color:{sev_color}; margin:4px 0 0 0;'>
                {severity}
            </h3>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div class='custom-divider'></div>
    """, unsafe_allow_html=True)

    # =============================================
    # Charts
    # =============================================
    if total > 0:
        st.markdown("""
            <h3 style='color:#F0F4FF; margin:16px 0;'>
                📈 Defect Distribution
            </h3>
        """, unsafe_allow_html=True)

        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            st.markdown("""
                <div class='glass-card'>
                    <p style='color:#8899AA; font-size:0.85rem;
                    margin-bottom:8px; text-transform:uppercase;
                    letter-spacing:1px;'>Defect Distribution</p>
            """, unsafe_allow_html=True)
            st.plotly_chart(
                plot_donut_chart(counts),
                use_container_width=True
            )
            st.markdown("</div>", unsafe_allow_html=True)

        with col_chart2:
            st.markdown("""
                <div class='glass-card'>
                    <p style='color:#8899AA; font-size:0.85rem;
                    margin-bottom:8px; text-transform:uppercase;
                    letter-spacing:1px;'>Count per Class</p>
            """, unsafe_allow_html=True)
            st.plotly_chart(
                plot_bar_chart(counts),
                use_container_width=True
            )
            st.markdown("</div>", unsafe_allow_html=True)

        # Confidence Chart
        if conf_stats:
            st.markdown("""
                <h3 style='color:#F0F4FF; margin:16px 0;'>
                    🎯 Confidence Analysis
                </h3>
            """, unsafe_allow_html=True)

            st.markdown("""
                <div class='glass-card'>
                    <p style='color:#8899AA; font-size:0.85rem;
                    margin-bottom:8px; text-transform:uppercase;
                    letter-spacing:1px;'>
                    Mean vs Max Confidence per Class</p>
            """, unsafe_allow_html=True)

            conf_fig = plot_confidence_chart(conf_stats)
            if conf_fig:
                st.plotly_chart(
                    conf_fig, use_container_width=True
                )
            st.markdown("</div>", unsafe_allow_html=True)

            # Confidence Stats Table
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
                <h4 style='color:#F0F4FF; margin-bottom:12px;'>
                    📋 Confidence Statistics
                </h4>
            """, unsafe_allow_html=True)

            for cls, stat in conf_stats.items():
                color = CLASS_COLORS.get(cls, "#FFFFFF")
                icon  = CLASS_ICONS.get(cls, "")
                st.markdown(f"""
                    <div class='glass-card' style='
                        padding:16px 20px; margin:6px 0;
                        border-left:3px solid {color};
                    '>
                        <div style='display:flex;
                                    justify-content:space-between;
                                    align-items:center;
                                    flex-wrap:wrap; gap:12px;'>
                            <span style='color:{color};
                                         font-weight:700;
                                         font-size:1.1rem;'>
                                {icon} {cls}
                            </span>
                            <div style='display:flex; gap:24px;'>
                                <div style='text-align:center;'>
                                    <div style='color:#8899AA;
                                                font-size:0.75rem;'>
                                        COUNT
                                    </div>
                                    <div style='color:#F0F4FF;
                                                font-weight:600;'>
                                        {stat['count']}
                                    </div>
                                </div>
                                <div style='text-align:center;'>
                                    <div style='color:#8899AA;
                                                font-size:0.75rem;'>
                                        MEAN
                                    </div>
                                    <div style='color:#F0F4FF;
                                                font-weight:600;'>
                                        {stat['mean']:.1%}
                                    </div>
                                </div>
                                <div style='text-align:center;'>
                                    <div style='color:#8899AA;
                                                font-size:0.75rem;'>
                                        MAX
                                    </div>
                                    <div style='color:#30D158;
                                                font-weight:600;'>
                                        {stat['max']:.1%}
                                    </div>
                                </div>
                                <div style='text-align:center;'>
                                    <div style='color:#8899AA;
                                                font-size:0.75rem;'>
                                        MIN
                                    </div>
                                    <div style='color:#FF453A;
                                                font-weight:600;'>
                                        {stat['min']:.1%}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    else:
        # No defects
        st.markdown("""
            <div class='glass-card' style='text-align:center;
                                           padding:48px;'>
                <div style='font-size:4rem;'>✅</div>
                <h3 style='color:#30D158;'>No Defects Found</h3>
                <p style='color:#8899AA;'>
                    Pipeline သန့်ရှင်းနေပါတယ်
                </p>
            </div>
        """, unsafe_allow_html=True)

    # =============================================
    # Result Image (Detection page မှ)
    # =============================================
    result_img = st.session_state.get('result_image')
    if result_img:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div class='custom-divider'></div>
            <h3 style='color:#F0F4FF; margin:16px 0;'>
                🖼️ Detection Image
            </h3>
        """, unsafe_allow_html=True)

        col_l, col_c, col_r = st.columns([1, 3, 1])
        with col_c:
            st.image(result_img, use_column_width=True)

    # =============================================
    # Action Buttons
    # =============================================
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<div class='custom-divider'></div>""",
                unsafe_allow_html=True)

    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        if st.button("📄 Report Export လုပ်",
                     use_container_width=True):
            st.session_state['page'] = "📄 Report"
            st.rerun()

    with col_btn2:
        if st.button("🔍 ထပ်ပြီး Detect လုပ်",
                     use_container_width=True):
            # Reset session
            st.session_state['detection_done'] = False
            st.session_state['detections']     = []
            st.session_state['result_image']   = None
            st.session_state['page']           = "🔍 Detection"
            st.rerun()
