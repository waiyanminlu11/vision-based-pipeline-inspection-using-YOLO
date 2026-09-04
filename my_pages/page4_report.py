# ============================================================
# page4_report.py — Report Export Page
# Pipeline Inspection System
# ============================================================

import streamlit as st
import json
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
import numpy as np
from PIL import Image as PILImage
from reportlab.platypus import Image as RLImage
from config import CLASS_COLORS, CLASS_ICONS, PROJECT_NAME


def get_severity(counts):
    if counts.get("Hole", 0) > 0:
        return "CRITICAL", "#FF453A"
    elif counts.get("Crack", 0) > 0:
        return "HIGH RISK", "#FF4B4B"
    elif counts.get("Corrosion", 0) > 0:
        return "MONITOR", "#FFD700"
    return "OK", "#30D158"


def generate_pdf(detections, result_image=None):
    """PDF Report generate လုပ်တယ်"""

    buffer   = BytesIO()
    doc      = SimpleDocTemplate(
        buffer,
        pagesize     = A4,
        rightMargin  = 2*cm,
        leftMargin   = 2*cm,
        topMargin    = 2*cm,
        bottomMargin = 2*cm
    )

    styles   = getSampleStyleSheet()
    elements = []

    # Colors
    DARK_BG  = colors.HexColor("#0A0E1A")
    BLUE     = colors.HexColor("#0A84FF")
    TEAL     = colors.HexColor("#30D5C8")
    LIGHT    = colors.HexColor("#F0F4FF")
    DIM      = colors.HexColor("#8899AA")
    RED      = colors.HexColor("#FF4B4B")
    ORANGE   = colors.HexColor("#FFA500")
    GOLD     = colors.HexColor("#FFD700")
    GREEN    = colors.HexColor("#30D158")

    # Custom Styles
    title_style = ParagraphStyle(
        'Title',
        parent    = styles['Title'],
        fontSize  = 22,
        textColor = BLUE,
        alignment = TA_CENTER,
        spaceAfter= 6,
        fontName  = 'Helvetica-Bold',
    )
    sub_style = ParagraphStyle(
        'Sub',
        parent    = styles['Normal'],
        fontSize  = 10,
        textColor = DIM,
        alignment = TA_CENTER,
        spaceAfter= 4,
    )
    section_style = ParagraphStyle(
        'Section',
        parent    = styles['Normal'],
        fontSize  = 13,
        textColor = BLUE,
        fontName  = 'Helvetica-Bold',
        spaceAfter= 8,
        spaceBefore=12,
    )
    normal_style = ParagraphStyle(
        'Normal2',
        parent    = styles['Normal'],
        fontSize  = 10,
        textColor = colors.HexColor("#333333"),
        spaceAfter= 4,
    )

    # =============================================
    # HEADER
    # =============================================
    elements.append(Paragraph(
        "🔧 PIPELINE INSPECTION REPORT", title_style
    ))
    elements.append(Paragraph(
        "AI-Powered Defect Detection System | YOLOv8n",
        sub_style
    ))
    elements.append(Spacer(1, 0.3*cm))
    elements.append(HRFlowable(
        width="100%", thickness=2,
        color=BLUE, spaceAfter=12
    ))

    # =============================================
    # REPORT INFO
    # =============================================
    now         = datetime.now()
    report_date = now.strftime("%Y-%m-%d")
    report_time = now.strftime("%H:%M:%S")

    info_data = [
        ["Report Date", report_date,
         "Report Time", report_time],
        ["System",      "Pipeline Inspection AI",
         "Model",       "YOLOv8n"],
        ["Total Defects",
         str(len(detections)),
         "Status",
         get_severity({
             "Crack"    : sum(1 for d in detections if d["class"]=="Crack"),
             "Hole"     : sum(1 for d in detections if d["class"]=="Hole"),
             "Corrosion": sum(1 for d in detections if d["class"]=="Corrosion"),
         })[0]
        ],
    ]

    info_table = Table(info_data, colWidths=[4*cm, 5*cm, 4*cm, 5*cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8F9FA")),
        ('TEXTCOLOR',  (0,0), (0,-1), BLUE),
        ('TEXTCOLOR',  (2,0), (2,-1), BLUE),
        ('FONTNAME',   (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME',   (2,0), (2,-1), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,-1), 10),
        ('ROWBACKGROUNDS', (0,0), (-1,-1),
         [colors.HexColor("#F0F4FF"), colors.white]),
        ('GRID',       (0,0), (-1,-1), 0.5,
         colors.HexColor("#DDDDDD")),
        ('PADDING',    (0,0), (-1,-1), 8),
        ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.5*cm))

    # =============================================
    # DEFECT SUMMARY
    # =============================================
    elements.append(Paragraph("📊 Defect Summary", section_style))

    counts = {
        "Crack"     : sum(1 for d in detections if d["class"]=="Crack"),
        "Hole"      : sum(1 for d in detections if d["class"]=="Hole"),
        "Corrosion" : sum(1 for d in detections if d["class"]=="Corrosion"),
    }
    severity_label, _ = get_severity(counts)

    summary_data = [
        ["Defect Type", "Count", "Percentage", "Risk Level"],
        ["🔴 Crack",
         str(counts["Crack"]),
         f"{counts['Crack']/max(len(detections),1)*100:.1f}%",
         "High Risk"],
        ["🟠 Hole",
         str(counts["Hole"]),
         f"{counts['Hole']/max(len(detections),1)*100:.1f}%",
         "Critical"],
        ["🟡 Corrosion",
         str(counts["Corrosion"]),
         f"{counts['Corrosion']/max(len(detections),1)*100:.1f}%",
         "Monitor"],
        ["TOTAL",
         str(len(detections)),
         "100%",
         severity_label],
    ]

    summary_table = Table(
        summary_data,
        colWidths=[5*cm, 3*cm, 4*cm, 6*cm]
    )
    summary_table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0,0), (-1,0), BLUE),
        ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,0), 11),
        ('ALIGN',      (0,0), (-1,0), 'CENTER'),
        # Rows
        ('FONTSIZE',   (0,1), (-1,-1), 10),
        ('ROWBACKGROUNDS', (0,1), (-1,-2),
         [colors.white, colors.HexColor("#F8F9FA")]),
        # Total row
        ('BACKGROUND', (0,-1), (-1,-1),
         colors.HexColor("#E8F4FF")),
        ('FONTNAME',   (0,-1), (-1,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR',  (0,-1), (-1,-1), BLUE),
        # Grid
        ('GRID',       (0,0), (-1,-1), 0.5,
         colors.HexColor("#DDDDDD")),
        ('PADDING',    (0,0), (-1,-1), 8),
        ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN',      (1,0), (-1,-1), 'CENTER'),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.5*cm))

    # =============================================
    # DETECTION IMAGE
    # =============================================
    if result_image is not None:
        elements.append(Paragraph(
            "🖼️ Detection Result Image", section_style
        ))

        # PIL Image → temp save
        img_buffer = BytesIO()
        if hasattr(result_image, 'save'):
            result_image.save(img_buffer, format='PNG')
        else:
            PILImage.fromarray(
                np.array(result_image)
            ).save(img_buffer, format='PNG')

        img_buffer.seek(0)
        rl_img = RLImage(img_buffer, width=14*cm, height=10*cm)
        elements.append(rl_img)
        elements.append(Spacer(1, 0.5*cm))

    # =============================================
    # DETECTION DETAILS
    # =============================================
    if detections:
        elements.append(Paragraph(
            "📋 Detection Details", section_style
        ))

        detail_data = [
            ["#", "Class", "Confidence",
             "Location (x1,y1)", "Location (x2,y2)"]
        ]

        for i, d in enumerate(detections, 1):
            x1, y1, x2, y2 = d["bbox"]
            detail_data.append([
                str(i),
                f"{d['icon']} {d['class']}",
                f"{d['confidence']:.1%}",
                f"({x1}, {y1})",
                f"({x2}, {y2})"
            ])

        detail_table = Table(
            detail_data,
            colWidths=[1.5*cm, 4*cm, 3.5*cm, 4*cm, 4*cm]
        )
        detail_table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A2540")),
            ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
            ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE',   (0,0), (-1,0), 10),
            ('ALIGN',      (0,0), (-1,0), 'CENTER'),
            # Rows
            ('FONTSIZE',   (0,1), (-1,-1), 9),
            ('ROWBACKGROUNDS', (0,1), (-1,-1),
             [colors.white, colors.HexColor("#F8F9FA")]),
            ('GRID',       (0,0), (-1,-1), 0.5,
             colors.HexColor("#DDDDDD")),
            ('PADDING',    (0,0), (-1,-1), 6),
            ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN',      (0,0), (0,-1), 'CENTER'),
            ('ALIGN',      (2,0), (2,-1), 'CENTER'),
        ]))
        elements.append(detail_table)

    elements.append(Spacer(1, 0.5*cm))

    # =============================================
    # RECOMMENDATIONS
    # =============================================
    elements.append(HRFlowable(
        width="100%", thickness=1,
        color=colors.HexColor("#DDDDDD"),
        spaceAfter=12
    ))
    elements.append(Paragraph(
        "💡 Recommendations", section_style
    ))

    recommendations = []
    if counts.get("Hole", 0) > 0:
        recommendations.append(
            "🔴 CRITICAL: Holes detected — Immediate repair required. "
            "Pipeline should be taken offline for inspection."
        )
    if counts.get("Crack", 0) > 0:
        recommendations.append(
            "⚠️  HIGH RISK: Cracks detected — Schedule maintenance within "
            "24-48 hours. Monitor for propagation."
        )
    if counts.get("Corrosion", 0) > 0:
        recommendations.append(
            "🟡 MONITOR: Corrosion detected — Apply anti-corrosion treatment. "
            "Re-inspect within 30 days."
        )
    if not recommendations:
        recommendations.append(
            "✅ Pipeline is in good condition. "
            "Continue routine inspection schedule."
        )

    for rec in recommendations:
        elements.append(Paragraph(f"• {rec}", normal_style))
        elements.append(Spacer(1, 0.2*cm))

    # =============================================
    # FOOTER
    # =============================================
    elements.append(Spacer(1, 0.5*cm))
    elements.append(HRFlowable(
        width="100%", thickness=1,
        color=BLUE, spaceAfter=8
    ))
    elements.append(Paragraph(
        f"Generated by {PROJECT_NAME} | {report_date} {report_time}",
        ParagraphStyle(
            'Footer',
            parent    = styles['Normal'],
            fontSize  = 8,
            textColor = DIM,
            alignment = TA_CENTER,
        )
    ))

    doc.build(elements)
    buffer.seek(0)
    return buffer


def show():

    st.markdown("""
        <div style='margin-bottom:24px;'>
            <h2 style='color:#F0F4FF; font-family:Rajdhani,sans-serif;
                       font-size:2rem; font-weight:700; letter-spacing:1px;'>
                📄 Report Export
            </h2>
            <p style='color:#8899AA;'>
                Detection ရလဒ်တွေကို PDF report အဖြစ် export လုပ်ပါ
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Detection မလုပ်ရသေးဘူး
    if not st.session_state.get('detection_done'):
        st.markdown("""
            <div class='glass-card' style='text-align:center;
                                           padding:48px;'>
                <div style='font-size:4rem;'>📄</div>
                <h3 style='color:#F0F4FF;'>Detection မလုပ်ရသေးဘူး</h3>
                <p style='color:#8899AA;'>
                    Detection page မှ detect လုပ်ပြီးမှ
                    report export လုပ်နိုင်မယ်
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

    detections  = st.session_state.get('detections', [])
    result_img  = st.session_state.get('result_image')
    counts      = {
        "Crack"    : sum(1 for d in detections if d["class"]=="Crack"),
        "Hole"     : sum(1 for d in detections if d["class"]=="Hole"),
        "Corrosion": sum(1 for d in detections if d["class"]=="Corrosion"),
    }
    severity_label, sev_color = get_severity(counts)

    # =============================================
    # Report Preview
    # =============================================
    st.markdown("""
        <h3 style='color:#F0F4FF; margin-bottom:16px;'>
            📋 Report Preview
        </h3>
    """, unsafe_allow_html=True)

    now = datetime.now()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
            <div class='glass-card'>
                <h4 style='color:#0A84FF; margin-bottom:12px;'>
                    📌 Report Info
                </h4>
                <div style='display:flex; flex-direction:column; gap:8px;'>
                    <div style='display:flex; justify-content:space-between;'>
                        <span style='color:#8899AA;'>Date</span>
                        <span style='color:#F0F4FF;'>
                            {now.strftime("%Y-%m-%d")}
                        </span>
                    </div>
                    <div style='display:flex; justify-content:space-between;'>
                        <span style='color:#8899AA;'>Time</span>
                        <span style='color:#F0F4FF;'>
                            {now.strftime("%H:%M:%S")}
                        </span>
                    </div>
                    <div style='display:flex; justify-content:space-between;'>
                        <span style='color:#8899AA;'>Model</span>
                        <span style='color:#F0F4FF;'>YOLOv8n</span>
                    </div>
                    <div style='display:flex; justify-content:space-between;'>
                        <span style='color:#8899AA;'>Total Defects</span>
                        <span style='color:#0A84FF; font-weight:700;'>
                            {len(detections)}
                        </span>
                    </div>
                    <div style='display:flex; justify-content:space-between;'>
                        <span style='color:#8899AA;'>Severity</span>
                        <span style='color:{sev_color}; font-weight:700;'>
                            {severity_label}
                        </span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class='glass-card'>
                <h4 style='color:#0A84FF; margin-bottom:12px;'>
                    📊 Defect Summary
                </h4>
                <div style='display:flex; flex-direction:column; gap:8px;'>
                    <div style='display:flex; justify-content:space-between;
                                align-items:center;'>
                        <span style='color:#FF4B4B;'>🔴 Crack</span>
                        <span style='
                            background:rgba(255,75,75,0.15);
                            padding:2px 12px; border-radius:20px;
                            color:#FF4B4B; font-weight:700;'>
                            {counts['Crack']}
                        </span>
                    </div>
                    <div style='display:flex; justify-content:space-between;
                                align-items:center;'>
                        <span style='color:#FFA500;'>🟠 Hole</span>
                        <span style='
                            background:rgba(255,165,0,0.15);
                            padding:2px 12px; border-radius:20px;
                            color:#FFA500; font-weight:700;'>
                            {counts['Hole']}
                        </span>
                    </div>
                    <div style='display:flex; justify-content:space-between;
                                align-items:center;'>
                        <span style='color:#FFD700;'>🟡 Corrosion</span>
                        <span style='
                            background:rgba(255,215,0,0.15);
                            padding:2px 12px; border-radius:20px;
                            color:#FFD700; font-weight:700;'>
                            {counts['Corrosion']}
                        </span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Recommendations Preview
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <h4 style='color:#F0F4FF; margin-bottom:12px;'>
            💡 Recommendations
        </h4>
    """, unsafe_allow_html=True)

    rec_list = []
    if counts.get("Hole", 0) > 0:
        rec_list.append(("🔴", "#FF453A",
            "CRITICAL: Holes detected — Immediate repair required."))
    if counts.get("Crack", 0) > 0:
        rec_list.append(("⚠️", "#FF4B4B",
            "HIGH RISK: Cracks detected — Schedule maintenance within 24-48 hours."))
    if counts.get("Corrosion", 0) > 0:
        rec_list.append(("🟡", "#FFD700",
            "MONITOR: Corrosion detected — Apply anti-corrosion treatment."))
    if not rec_list:
        rec_list.append(("✅", "#30D158",
            "Pipeline is in good condition. Continue routine inspection."))

    for icon, color, text in rec_list:
        st.markdown(f"""
            <div class='glass-card' style='
                padding:12px 20px; margin:6px 0;
                border-left:3px solid {color};
            '>
                <span style='color:{color};'>{icon} {text}</span>
            </div>
        """, unsafe_allow_html=True)

    # =============================================
    # Export Button
    # =============================================
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<div class='custom-divider'></div>""",
                unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        if st.button("📥 Generate & Download PDF",
                     use_container_width=True):
            with st.spinner("PDF generate လုပ်နေသည်..."):
                pdf_buffer = generate_pdf(detections, result_img)

            filename = f"pipeline_report_{now.strftime('%Y%m%d_%H%M%S')}.pdf"

            st.download_button(
                label     = "⬇️ Download PDF Report",
                data      = pdf_buffer,
                file_name = filename,
                mime      = "application/pdf",
                use_container_width=True
            )

            st.success("✅ PDF Report အဆင်သင့်ဖြစ်ပြီ!")
