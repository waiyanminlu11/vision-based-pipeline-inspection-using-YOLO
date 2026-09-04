# ============================================================
# modules/detector.py
# YOLOv8 Detection Module
# Pipeline Inspection System
# ============================================================

import cv2
import torch
import numpy as np
from PIL import Image
import streamlit as st
from ultralytics import YOLO
from config import (
    CLASSES, CLASS_COLORS, CLASS_ICONS,
    CONF_THRESHOLD, IOU_THRESHOLD, IMG_SIZE
)


@st.cache_resource
def load_model(model_path: str):
    """
    YOLOv8 model load + cache လုပ်တယ်။
    တစ်ခါပဲ load လုပ်ပြီး cache သိမ်းတယ်။
    """
    try:
        model = YOLO(model_path)
        return model
    except Exception as e:
        st.error(f"❌ Model load မရဘူး: {e}")
        return None


def run_detection(model, image, conf=CONF_THRESHOLD,
                  iou=IOU_THRESHOLD, imgsz=IMG_SIZE):
    """
    Image တစ်ပုံကို detect လုပ်တယ်။

    Args:
        model  : YOLO model
        image  : PIL Image
        conf   : Confidence threshold
        iou    : IOU threshold
        imgsz  : Input image size

    Returns:
        results: YOLOv8 raw results
    """
    # PIL Image ဆိုရင် BGR အဖြစ် ပြောင်း
    if isinstance(image, Image.Image):
        img_array = np.array(image)
        img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    else:
        img_bgr = image

    results = model(
        img_bgr,
        conf=conf,
        iou=iou,
        imgsz=imgsz,
        augment=False,
        verbose=False,
        device='0' if torch.cuda.is_available() else 'cpu'
    )
    return results
    


def draw_boxes(image, results, conf_threshold=CONF_THRESHOLD):
    """
    Bounding box တွေ ဆွဲပြီး detection list ပြန်ပေးတယ်။

    Args:
        image          : PIL Image (မူလပုံ)
        results        : YOLOv8 results
        conf_threshold : Confidence threshold

    Returns:
        result_image   : PIL Image (box ပါတဲ့ပုံ)
        detections     : list of detection dicts
    """
    img        = np.array(image).copy()
    detections = []

    color_map = {
        "Crack"     : (255, 75,  75),
        "Hole"      : (255, 165,  0),
        "Corrosion" : (255, 215,  0),
    }

    for result in results:
        for box in result.boxes:
            conf = float(box.conf[0])
            if conf < conf_threshold:
                continue

            cls_id   = int(box.cls[0])
            cls_name = CLASSES.get(cls_id, "Unknown")
            color    = color_map.get(cls_name, (255, 255, 255))

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Bounding box
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

            # Label
            label       = f"{CLASS_ICONS.get(cls_name,'')} {cls_name} {conf:.0%}"
            (tw, th), _ = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
            )
            cv2.rectangle(
                img,
                (x1, y1 - th - 10),
                (x1 + tw + 8, y1),
                color, -1
            )
            cv2.putText(
                img, label, (x1 + 4, y1 - 6),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (0, 0, 0), 2
            )

            detections.append({
                "class"     : cls_name,
                "icon"      : CLASS_ICONS.get(cls_name, ""),
                "confidence": conf,
                "bbox"      : [x1, y1, x2, y2],
                "color"     : CLASS_COLORS.get(cls_name, "#FFFFFF")
            })

    return Image.fromarray(img), detections


def detect_image(model, image,
                 conf=CONF_THRESHOLD,
                 iou=IOU_THRESHOLD,
                 imgsz=IMG_SIZE):
    """
    Image တစ်ပုံ detect လုပ်ပြီး
    result image နဲ့ detections ပြန်ပေးတယ်။

    Args:
        model  : YOLO model
        image  : PIL Image
        conf   : Confidence threshold
        iou    : IOU threshold
        imgsz  : Input image size

    Returns:
        result_image : PIL Image (box ပါတဲ့ပုံ)
        detections   : list of detection dicts
    """
    results      = run_detection(model, image, conf, iou, imgsz)
    result_image, detections = draw_boxes(image, results, conf)
    return result_image, detections


def get_class_counts(detections: list) -> dict:
    """
    Detection list ကနေ class count တွက်တယ်။

    Returns:
        dict: {"Crack": n, "Hole": n, "Corrosion": n}
    """
    counts = {"Crack": 0, "Hole": 0, "Corrosion": 0}
    for d in detections:
        if d["class"] in counts:
            counts[d["class"]] += 1
    return counts


def get_severity(counts: dict) -> tuple:
    """
    Defect counts အပေါ် မူတည်ပြီး
    severity level ပြန်ပေးတယ်။

    Returns:
        tuple: (severity_label, color_hex)
    """
    if counts.get("Hole", 0) > 0:
        return "CRITICAL ⚠️",  "#FF453A"
    elif counts.get("Crack", 0) > 0:
        return "HIGH RISK 🔴", "#FF4B4B"
    elif counts.get("Corrosion", 0) > 0:
        return "MONITOR 🟡",   "#FFD700"
    return "OK ✅",             "#30D158" 


# ============================================================
# modules/detector.py — Hybrid Detection Module
# Pipeline Inspection System
#
# Stage 1: Traditional CV  → Crack + Hole
# Stage 2: YOLOv8n        → Corrosion + Ambiguous cases
# ============================================================

'''import cv2
import numpy as np
from PIL import Image
import streamlit as st
from ultralytics import YOLO
from config import (
    CLASSES, CLASS_COLORS, CLASS_ICONS,
    CONF_THRESHOLD, IOU_THRESHOLD, IMG_SIZE
)


# ============================================================
# Model Load
# ============================================================

@st.cache_resource
def load_model(model_path: str):
    """YOLOv8 model load + cache"""
    try:
        return YOLO(model_path)
    except Exception as e:
        st.error(f"❌ Model load မရဘူး: {e}")
        return None


# ============================================================
# Stage 1: Traditional CV — Crack Detection
# ============================================================

def detect_crack_cv(gray, clahe_img):
    """
    Canny edge + Morphology + Aspect Ratio နဲ့
    Crack တွေ ရှာတယ်။

    Returns:
        list of (x1, y1, x2, y2, confidence) tuples
    """
    detections = []

    # Gaussian blur — noise လျှော့
    blurred = cv2.GaussianBlur(clahe_img, (5, 5), 0)

    # Canny edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Morphological closing — edge ကြားထဲ gap ပိတ်
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 2))
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    # Contour ရှာ
    contours, _ = cv2.findContours(
        closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    h_img, w_img = gray.shape

    for cnt in contours:
        area = cv2.contourArea(cnt)

        # သေးလွန်းတဲ့ contour ဖယ်
        if area < 100:
            continue

        x, y, w, h = cv2.boundingRect(cnt)

        # Aspect ratio တွက် (ရှည်တယ် = crack)
        aspect_ratio = max(w, h) / (min(w, h) + 1e-5)

        # Solidity တွက်
        hull    = cv2.convexHull(cnt)
        hull_area = cv2.contourArea(hull)
        solidity  = area / (hull_area + 1e-5)

        # Crack criteria —
        # ရှည်တယ် (aspect ratio > 3.0)
        # Solidity နိမ့်တယ် (မပြည့်စုံဘူး)
        # Area သင့်တင့်မျှတယ်
        if aspect_ratio > 3.0 and solidity < 0.6:
            # Confidence estimate (aspect ratio ပေါ် မူတည်)
            conf = min(0.5 + (aspect_ratio - 3.0) * 0.05, 0.85)
            detections.append((x, y, x+w, y+h, conf))

    return detections


# ============================================================
# Stage 1: Traditional CV — Hole Detection
# ============================================================

def detect_hole_cv(gray, original_bgr):
    """
    Circularity + Solidity + Interior darkness နဲ့
    Hole တွေ ရှာတယ်။

    Returns:
        list of (x1, y1, x2, y2, confidence) tuples
    """
    detections = []

    # Threshold — dark region ရှာ
    _, thresh = cv2.threshold(
        gray, 0, 255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    # Morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel)

    # Contour ရှာ
    contours, _ = cv2.findContours(
        cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    h_img, w_img = gray.shape

    for cnt in contours:
        area = cv2.contourArea(cnt)

        # သေးလွန်းတဲ့ contour ဖယ်
        if area < 200:
            continue

        perimeter = cv2.arcLength(cnt, True)
        if perimeter == 0:
            continue

        # Circularity တွက်
        circularity = (4 * np.pi * area) / (perimeter ** 2)

        # Solidity တွက်
        hull      = cv2.convexHull(cnt)
        hull_area = cv2.contourArea(hull)
        solidity  = area / (hull_area + 1e-5)

        # Hole criteria —
        # Circularity > 0.5 (ဝိုင်းတယ်)
        # Solidity > 0.7 (သိပ်သည်းတယ်)
        if circularity > 0.5 and solidity > 0.7:

            x, y, w, h = cv2.boundingRect(cnt)

            # Interior darkness check
            # Hole ဆိုရင် အတွင်းက မှောင်ရမယ်
            mask_interior = np.zeros(gray.shape, dtype=np.uint8)
            cv2.drawContours(mask_interior, [cnt], -1, 255, -1)

            # ROI ပြင်ပ mask
            mask_exterior = np.zeros(gray.shape, dtype=np.uint8)
            ex = max(0, x-10)
            ey = max(0, y-10)
            ew = min(w_img, x+w+10)
            eh = min(h_img, y+h+10)
            mask_exterior[ey:eh, ex:ew] = 255
            mask_exterior = cv2.subtract(mask_exterior, mask_interior)

            interior_mean = cv2.mean(gray, mask=mask_interior)[0]
            exterior_mean = cv2.mean(gray, mask=mask_exterior)[0]

            # Interior က exterior ထက် မှောင်ရမယ်
            if interior_mean < exterior_mean * 0.75:
                conf = min(
                    0.5 + circularity * 0.3 + solidity * 0.2,
                    0.90
                )
                detections.append((x, y, x+w, y+h, conf))

    return detections


# ============================================================
# Stage 2: YOLOv8n — Corrosion + Ambiguous
# ============================================================

def detect_corrosion_yolo(model, image, conf=CONF_THRESHOLD):
    """
    YOLOv8n နဲ့ Corrosion detect လုပ်တယ်။
    Crack နဲ့ Hole ပါလာရင်လည်း
    CV result နဲ့ နှိုင်းယှဉ်ပြီး ထည့်မယ်။

    Returns:
        list of detection dicts
    """
    detections = []

    results = model(
        image,
        conf    = conf,
        iou     = IOU_THRESHOLD,
        imgsz   = IMG_SIZE,
        verbose = False
    )

    for result in results:
        for box in result.boxes:
            cls_id   = int(box.cls[0])
            cls_name = CLASSES.get(cls_id, "Unknown")
            confidence = float(box.conf[0])

            # Corrosion သာ ယူမယ်
            # (Crack/Hole က CV က handle လုပ်ပြီးပြီ)
            if cls_name == "Corrosion":
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                detections.append({
                    "class"     : "Corrosion",
                    "icon"      : CLASS_ICONS.get("Corrosion", "🟡"),
                    "confidence": confidence,
                    "bbox"      : [x1, y1, x2, y2],
                    "color"     : CLASS_COLORS.get("Corrosion", "#FFD700"),
                    "method"    : "YOLOv8n"
                })

    return detections


# ============================================================
# Draw Bounding Boxes
# ============================================================

def draw_boxes_hybrid(image, all_detections):
    """
    CV + YOLO detections အားလုံးကို
    image ပေါ် ဆွဲတယ်။
    """
    img = np.array(image).copy()

    color_map = {
        "Crack"     : (255, 75,  75),
        "Hole"      : (255, 165,  0),
        "Corrosion" : (255, 215,  0),
    }

    for d in all_detections:
        x1, y1, x2, y2 = d["bbox"]
        cls_name        = d["class"]
        conf            = d["confidence"]
        method          = d.get("method", "CV")
        color           = color_map.get(cls_name, (255, 255, 255))

        # Bounding box
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

        # Label
        label       = f"{CLASS_ICONS.get(cls_name,'')} {cls_name} {conf:.0%}"
        (tw, th), _ = cv2.getTextSize(
            label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
        )
        cv2.rectangle(
            img, (x1, y1-th-10), (x1+tw+8, y1), color, -1
        )
        cv2.putText(
            img, label, (x1+4, y1-6),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6, (0, 0, 0), 2
        )

        # Method tag (CV or YOLO)
        method_label = f"[{method}]"
        cv2.putText(
            img, method_label, (x1, y2+15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4, color, 1
        )

    return Image.fromarray(img)


# ============================================================
# Main Hybrid Detection Function
# ============================================================

def detect_image_hybrid(model, image,
                         conf=CONF_THRESHOLD,
                         iou=IOU_THRESHOLD,
                         imgsz=IMG_SIZE):
    """
    Hybrid detection — CV + YOLOv8n

    Stage 1: OpenCV → Crack + Hole
    Stage 2: YOLOv8 → Corrosion

    Args:
        model  : YOLO model
        image  : PIL Image
        conf   : Confidence threshold
        iou    : IOU threshold
        imgsz  : Image size

    Returns:
        result_image : PIL Image (boxes ပါတဲ့ပုံ)
        detections   : list of detection dicts
    """
    # PIL → OpenCV format
    img_bgr  = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    # CLAHE — low-light ကောင်းအောင်
    clahe      = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    img_clahe  = clahe.apply(img_gray)

    all_detections = []

    # =====================
    # Stage 1: CV Detection
    # =====================

    # Crack detection
    crack_boxes = detect_crack_cv(img_gray, img_clahe)
    for (x1, y1, x2, y2, c) in crack_boxes:
        all_detections.append({
            "class"     : "Crack",
            "icon"      : CLASS_ICONS.get("Crack", "🔴"),
            "confidence": c,
            "bbox"      : [x1, y1, x2, y2],
            "color"     : CLASS_COLORS.get("Crack", "#FF4B4B"),
            "method"    : "OpenCV"
        })

    # Hole detection
    hole_boxes = detect_hole_cv(img_clahe, img_bgr)
    for (x1, y1, x2, y2, c) in hole_boxes:
        all_detections.append({
            "class"     : "Hole",
            "icon"      : CLASS_ICONS.get("Hole", "🟠"),
            "confidence": c,
            "bbox"      : [x1, y1, x2, y2],
            "color"     : CLASS_COLORS.get("Hole", "#FFA500"),
            "method"    : "OpenCV"
        })

    # ========================
    # Stage 2: YOLO Detection
    # ========================
    if model is not None:
        corrosion_dets = detect_corrosion_yolo(model, image, conf)
        all_detections.extend(corrosion_dets)

    # NMS — overlapping boxes ဖယ်
    all_detections = apply_nms(all_detections, iou_threshold=0.5)

    # Draw boxes
    result_image = draw_boxes_hybrid(image, all_detections)

    return result_image, all_detections


# ============================================================
# NMS (Non-Maximum Suppression)
# ============================================================

def apply_nms(detections, iou_threshold=0.5):
    """
    Overlapping bounding boxes တွေကို
    IOU နဲ့ စစ်ပြီး ဖယ်တယ်။
    """
    if not detections:
        return detections

    boxes  = np.array([d["bbox"] for d in detections], dtype=np.float32)
    scores = np.array([d["confidence"] for d in detections], dtype=np.float32)

    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    areas = (x2 - x1) * (y2 - y1)
    order = scores.argsort()[::-1]

    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)

        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])

        w   = np.maximum(0.0, xx2 - xx1)
        h   = np.maximum(0.0, yy2 - yy1)
        inter = w * h

        iou = inter / (areas[i] + areas[order[1:]] - inter + 1e-5)
        inds = np.where(iou <= iou_threshold)[0]
        order = order[inds + 1]

    return [detections[i] for i in keep]


# ============================================================
# Helper Functions
# ============================================================

def get_class_counts(detections: list) -> dict:
    """Class count တွက်တယ်"""
    counts = {"Crack": 0, "Hole": 0, "Corrosion": 0}
    for d in detections:
        if d["class"] in counts:
            counts[d["class"]] += 1
    return counts


def get_severity(counts: dict) -> tuple:
    """Severity level ပြန်ပေးတယ်"""
    if counts.get("Hole", 0) > 0:
        return "CRITICAL ⚠️",  "#FF453A"
    elif counts.get("Crack", 0) > 0:
        return "HIGH RISK 🔴", "#FF4B4B"
    elif counts.get("Corrosion", 0) > 0:
        return "MONITOR 🟡",   "#FFD700"
    return "OK ✅",             "#30D158"


# ============================================================
# Backward Compatibility
# (page2_detection.py မှာ detect_image သုံးနေတဲ့အတွက်)
# ============================================================

def detect_image(model, image,
                 conf=CONF_THRESHOLD,
                 iou=IOU_THRESHOLD,
                 imgsz=IMG_SIZE):
    """detect_image_hybrid ကို ခေါ်ပေးတယ်"""
    return detect_image_hybrid(model, image, conf, iou, imgsz)


def draw_boxes(image, results, conf_threshold=CONF_THRESHOLD):
    """Backward compatibility အတွက်"""
    return image, []'''
