# ============================================================  
# config.py — Pipeline Inspection System 
# Settings အားလုံး ဒီမှာ သတ်မှတ်တယ် 
# ============================================================ 
import os 
# ============================================================ 
# Project Info 
# ============================================================
PROJECT_NAME = "Vision-based_Pipeline_Inspection_Robot" 
PROJECT_VERSION = "1.0.0" 
PROJECT_DESC = "AI-Powered Pipeline Defect Detection using YOLOv8m-p2" 
AUTHOR = "Mr. Hlaing Myo" 

# ============================================================ 
# Model Settings 
# ============================================================ 


MODEL_DIR = os.path.join(os.path.dirname(__file__), "models") 

MODELS = {
        "Model": { 
                "path" : os.path.join(MODEL_DIR, "best_real.pt"), 
                "desc" : "Trained on augmented dataset (dark/noise/blur)" 
        } 
} 

# Default model 

DEFAULT_MODEL = "Model" 

# ============================================================ 
# Detection Settings 
# ============================================================ 
 
CONF_THRESHOLD = 0.10 # Confidence threshold 
IOU_THRESHOLD = 0.45 # IOU threshold 
IMG_SIZE = 960 # Input image size 

# Classes 
CLASSES = { 0: "Crack", 1: "Hole", 2: "Corrosion" } 

# Class colors (BGR → RGB) 
 
CLASS_COLORS = { "Crack" : "#FF4B4B", # Red
                 "Hole" : "#FFA500", # Orange 
                 "Corrosion" : "#FFD700", # Gold 
} 

# Class icons 
CLASS_ICONS = { "Crack" : "🔴", "Hole" : "🟠", "Corrosion" : "🟡", } 

# ============================================================ 
# Paths 
# ============================================================ 

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
ASSETS_DIR = os.path.join(BASE_DIR, "assets") 
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs") 
REPORTS_DIR = os.path.join(OUTPUT_DIR, "reports") 

# Lottie Animation Paths 
LOTTIE_ROBOT = os.path.join(ASSETS_DIR, "robot.json") 
LOTTIE_SCANNING = os.path.join(ASSETS_DIR, "scanning.json") 
LOTTIE_SUCCESS = os.path.join(ASSETS_DIR, "success.json") 

# ============================================================ 
# Theme — မိုးပြာ Glass Design 
# ============================================================ 
# 
THEME = {
    "primary" : "#0A84FF", # Apple blue 
    "secondary" : "#30D5C8", # Teal accent 
    "background" : "#0A0E1A", # Deep navy 
    "surface" : "#111827", # Card background 
    "glass" : "rgba(255, 255, 255, 0.05)", # Glass effect 
    "text" : "#F0F4FF", # Light text 
    "text_dim" : "#8899AA", # Dimmed text 
    "success" : "#30D158", # Green 
    "warning" : "#FFD60A", # Yellow 
    "danger" : "#FF453A", # Red 
    "border" : "rgba(255, 255, 255, 0.1)", 
    } 
    
# ============================================================ 
# CSS — Glass Morphism + iPhone Style 
# ============================================================ 
CSS = f""" 
<style> 
    /* Google Font Import */ 
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;600;700&family=Rajdhani:wght@400;600;700&display=swap'); 
    
    /* Root Variables */ 
    :root {{ 
        --primary : {THEME['primary']}; 
        --secondary : {THEME['secondary']}; 
        --background : {THEME['background']}; 
        --surface : {THEME['surface']}; 
        --glass : {THEME['glass']}; 
        --text : {THEME['text']}; 
        --text-dim : {THEME['text_dim']}; 
        --success : {THEME['success']}; 
        --warning : {THEME['warning']}; 
        --danger : {THEME['danger']}; 
        --border : {THEME['border']}; 
    }} 
    
    /* Main Background */ 
    .stApp {{ 
        background: linear-gradient(135deg, #0A0E1A 0%, #0D1B2A 50%, #0A1628 100%); 
        color: var(--text); 
        font-family: 'Rajdhani', sans-serif; 
    }} 
    
    /* Sidebar */ 
    [data-testid="stSidebar"] {{ 
        background: rgba(10, 14, 26, 0.95) !important; 
        border-right: 1px solid var(--border); 
        backdrop-filter: blur(20px); 
    }} 
    
    /* Glass Card */ 
    .glass-card {{ 
        background: rgba(255, 255, 255, 0.04); 
        backdrop-filter: blur(20px); 
        -webkit-backdrop-filter: blur(20px); 
        border: 1px solid rgba(255, 255, 255, 0.08); 
        border-radius: 20px; 
        padding: 24px; 
        margin: 12px 0; 
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), 
                    inset 0 1px 0 rgba(255, 255, 255, 0.1); 
        transition: all 0.3s ease; 
    }} 
    
    .glass-card:hover {{
        border-color: rgba(10, 132, 255, 0.3); 
        box-shadow: 0 8px 32px rgba(10, 132, 255, 0.15), 
                    inset 0 1px 0 rgba(255, 255, 255, 0.15); 
        transform: translateY(-2px); 
    }} 
    
    /* iPhone Glass Button */ 
    .glass-button {{ 
        background: linear-gradient(135deg, 
            rgba(10, 132, 255, 0.3) 0%, 
            rgba(10, 132, 255, 0.1) 100%); 
        backdrop-filter: blur(10px); 
        border: 1px solid rgba(10, 132, 255, 0.4); 
        border-radius: 14px; color: #ffffff; 
        padding: 12px 28px; 
        font-family: 'Rajdhani', sans-serif; 
        font-size: 16px; 
        font-weight: 600; 
        cursor: pointer; 
        transition: all 0.3s ease; 
        box-shadow: 0 4px 15px rgba(10, 132, 255, 0.2), 
            inset 0 1px 0 rgba(255, 255, 255, 0.2); 
        letter-spacing: 0.5px; 
    }} 
    
    .glass-button:hover {{ 
        background: linear-gradient(135deg, 
            rgba(10, 132, 255, 0.5) 0%, 
            rgba(10, 132, 255, 0.3) 100%); 
        box-shadow: 0 6px 20px rgba(10, 132, 255, 0.4), 
                    inset 0 1px 0 rgba(255, 255, 255, 0.3); 
        transform: translateY(-1px); 
    }} 
    
    /* Streamlit Buttons Override */ 
    .stButton > button {{ 
        background: linear-gradient(135deg, 
            rgba(10, 132, 255, 0.3) 0%, 
            rgba(10, 132, 255, 0.15) 100%) !important; 
        backdrop-filter: blur(10px) !important; 
        border: 1px solid rgba(10, 132, 255, 0.4) !important; 
        border-radius: 14px !important; 
        color: #ffffff !important; 
        font-family: 'Rajdhani', sans-serif !important; 
        font-weight: 600 !important; 
        letter-spacing: 0.5px !important; 
        box-shadow: 0 4px 15px rgba(10, 132, 255, 0.2), 
                    inset 0 1px 0 rgba(255, 255, 255, 0.15) !important; 
        transition: all 0.3s ease !important; 
    }} 
    
    .stButton > button:hover {{ 
        background: linear-gradient(135deg, 
            rgba(10, 132, 255, 0.5) 0%, 
            rgba(10, 132, 255, 0.3) 100%) !important; 
        border-color: rgba(10, 132, 255, 0.7) !important; 
        box-shadow: 0 6px 25px rgba(10, 132, 255, 0.4) !important; 
        transform: translateY(-1px) !important; 
    }} 
    
    /* Metric Cards */ 
    .metric-card {{ 
        background: rgba(255, 255, 255, 0.03); 
        border: 1px solid rgba(255, 255, 255, 0.07); 
        border-radius: 16px; 
        padding: 20px; 
        text-align: center; 
        transition: all 0.3s ease; 
    }} 
    
    .metric-card:hover {{ 
        background: rgba(10, 132, 255, 0.08);
        border-color: rgba(10, 132, 255, 0.3); 
    }} 
    
    .metric-value {{ 
        font-size: 2.2rem; 
        font-weight: 700; 
        color: var(--primary); 
        font-family: 'Rajdhani', sans-serif; 
        line-height: 1; 
    }} 
    
    .metric-label {{ 
        font-size: 0.85rem; 
        color: var(--text-dim); 
        margin-top: 6px; 
        text-transform: uppercase; 
        letter-spacing: 1px; 
    }} 
    
    /* Divider */ 
    .custom-divider {{ 
        height: 1px; 
        background: linear-gradient(90deg, transparent 0%, rgba(10, 132, 255, 0.5) 50%, transparent 100%); 
        margin: 24px 0; 
    }} 
    
    /* Badge */ 
    .badge {{ 
        display: inline-block; 
        padding: 4px 12px; 
        border-radius: 20px; 
        font-size: 0.75rem; 
        font-weight: 600; 
        letter-spacing: 0.5px; 
    }} 
    
    .badge-crack {{ background: rgba(255, 75, 75, 0.2); color: #FF4B4B; border: 1px solid rgba(255,75,75,0.3); }} 
    .badge-hole {{ background: rgba(255, 165, 0, 0.2); color: #FFA500; border: 1px solid rgba(255,165,0,0.3); }} 
    .badge-corrosion {{ background: rgba(255, 215, 0, 0.2); color: #FFD700; border: 1px solid rgba(255,215,0,0.3); }} 
    
    /* Glow effect */ 
    .glow-text {{ 
        color: var(--primary); 
        text-shadow: 0 0 20px rgba(10, 132, 255, 0.5); 
    }} 
    
    /* Hide Streamlit default elements */ 
    #MainMenu {{ visibility: hidden; }} 
    footer {{ visibility: hidden; }} 
    header {{ visibility: hidden; }} 
    
    /* Scrollbar */ 
    ::-webkit-scrollbar {{ width: 6px; }} 
    ::-webkit-scrollbar-track {{ background: rgba(255,255,255,0.02); }} 
    ::-webkit-scrollbar-thumb {{ background: rgba(10, 132, 255, 0.4); border-radius: 3px; }} 
    
    /* Pulse Animation */ 
    @keyframes pulse {{ 
        0% {{ box-shadow: 0 0 0 0 rgba(10, 132, 255, 0.4); }} 
        70% {{ box-shadow: 0 0 0 10px rgba(10, 132, 255, 0); }} 
        100% {{ box-shadow: 0 0 0 0 rgba(10, 132, 255, 0); }} 
    }} 
    
    .pulse {{ animation: pulse 2s infinite; }} 
    
    /* Fade in */ 
    @keyframes fadeIn {{ 
        from {{ opacity: 0; transform: translateY(20px); }} 
        to {{ opacity: 1; transform: translateY(0); }} 
    }} 
    
    .fade-in {{ animation: fadeIn 0.6s ease forwards; }} 
</style> 
"""





