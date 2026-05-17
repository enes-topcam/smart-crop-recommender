import streamlit as st
import numpy as np
import joblib
import os

st.set_page_config(
    page_title="Mahsül Öneri Sistemi",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    .stApp {
        background: linear-gradient(160deg, #f0faf4 0%, #e8f5e9 60%, #f5f0e8 100%);
        font-family: 'Inter', sans-serif;
    }

    #MainMenu, footer { visibility: hidden; }
    header[data-testid="stHeader"],
    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* ── Sidebar toggle butonu (Material Icon font) ──
       KAPALI: sidebar dışındaki buton → koyu yeşil ikon
       AÇIK  : sidebar içindeki buton  → beyaz ikon */

    /* ── Sidebar toggle butonu — KAPALI durum (stExpandSidebarButton, header'da) ── */
    html body button[data-testid="stExpandSidebarButton"] {
        background: #1B4332 !important;
        background-color: #1B4332 !important;
        background-image: none !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 6px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.40) !important;
        visibility: visible !important;
        opacity: 1 !important;
        z-index: 999999 !important;
    }
    html body button[data-testid="stExpandSidebarButton"]:hover,
    html body button[data-testid="stExpandSidebarButton"]:focus,
    html body button[data-testid="stExpandSidebarButton"]:active {
        background: #2D6A4F !important;
        background-color: #2D6A4F !important;
        opacity: 1 !important;
    }
    html body button[data-testid="stExpandSidebarButton"] span,
    html body button[data-testid="stExpandSidebarButton"] span[color],
    html body button[data-testid="stExpandSidebarButton"] [data-testid="stIconMaterial"] {
        color: #ffffff !important;
        opacity: 1 !important;
    }

    /* ── AÇIK durum (sidebar içindeki kapatma butonu) ── */
    html body div[data-testid="stSidebarCollapseButton"] > button,
    html body [data-testid="stSidebar"] button[data-testid="stBaseButton-headerNoPadding"] {
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        opacity: 1 !important;
    }
    html body [data-testid="stSidebar"] button[data-testid="stBaseButton-headerNoPadding"]:hover {
        background: rgba(255,255,255,0.15) !important;
        background-color: rgba(255,255,255,0.15) !important;
    }
    html body div[data-testid="stSidebarCollapseButton"] span,
    html body div[data-testid="stSidebarCollapseButton"] span[color],
    html body div[data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"],
    html body [data-testid="stSidebar"] button[data-testid="stBaseButton-headerNoPadding"] span,
    html body [data-testid="stSidebar"] button[data-testid="stBaseButton-headerNoPadding"] [data-testid="stIconMaterial"] {
        color: #ffffff !important;
        opacity: 1 !important;
    }
    /* Hover'da biraz daha açık yeşil */
    html body div[data-testid="stSidebarCollapseButton"] > button:hover,
    html body div[data-testid="stSidebarCollapseButton"] > button:focus,
    html body div[data-testid="stSidebarCollapsedControl"] > button:hover,
    html body div[data-testid="stSidebarCollapsedControl"] > button:focus,
    html body button[data-testid="stBaseButton-headerNoPadding"]:hover,
    html body button[data-testid="stBaseButton-headerNoPadding"]:focus {
        background: #2D6A4F !important;
        background-color: #2D6A4F !important;
        background-image: none !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    /* İkon her durumda beyaz */
    html body div[data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"],
    html body div[data-testid="stSidebarCollapseButton"] span,
    html body div[data-testid="stSidebarCollapsedControl"] [data-testid="stIconMaterial"],
    html body div[data-testid="stSidebarCollapsedControl"] span {
        color: #ffffff !important;
        opacity: 1 !important;
    }

    /* Kapalı durumda butonu saran tüm olası container'ları da yeşile boya */
    html body [data-testid="stSidebarHeader"],
    html body [data-testid="stSidebarUserContent"],
    html body [data-testid="stSidebarContent"],
    html body [data-testid="stSidebarNav"],
    html body section[data-testid="stSidebar"],
    html body section[data-testid="stSidebar"] > div,
    html body section[data-testid="stSidebar"] > div > div {
        background: #1B4332 !important;
        background-color: #1B4332 !important;
        background-image: none !important;
    }
    /* :has() destekleniyorsa toggle butonunu içeren her parent yeşil olsun */
    html body *:has(> [data-testid="stSidebarCollapseButton"]),
    html body *:has(> [data-testid="stSidebarCollapsedControl"]),
    html body *:has(> button[data-testid="stBaseButton-headerNoPadding"]) {
        background: #1B4332 !important;
        background-color: #1B4332 !important;
    }

    /* ── Genel metin renkleri (açık arka plan üzerinde okunabilir) ── */
    /* Yeşil arka planlı bölgeler (hero, result-card, sidebar-box) hariç tut */
    .stApp [data-testid="stMarkdownContainer"] p,
    .stApp [data-testid="stMarkdownContainer"] li,
    .stApp [data-testid="stMarkdownContainer"] strong,
    .stApp [data-testid="stMarkdownContainer"] span {
        color: #1B4332;
    }
    .hero, .hero *,
    .result-card, .result-card *,
    .sidebar-box, .sidebar-box * {
        color: inherit;
    }
    .hero, .hero h1, .hero .hero-title, .hero .hero-title * { color: #ffffff !important; }
    .hero .hero-sub { color: #95D5B2 !important; }

    /* ── Sidebar (koyu yeşil tema, beyaz yazılar) ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1B4332 0%, #2D6A4F 100%) !important;
    }
    [data-testid="stSidebar"] *,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] td,
    [data-testid="stSidebar"] th,
    [data-testid="stSidebar"] strong,
    [data-testid="stSidebar"] summary,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] * {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"],
    [data-testid="stSidebar"] .stCaption {
        color: rgba(255,255,255,0.75) !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.20) !important;
    }
    [data-testid="stSidebar"] [data-testid="stExpander"] {
        background: rgba(255,255,255,0.06) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
    }
    [data-testid="stSidebar"] [data-testid="stExpander"] svg { fill: #ffffff !important; }

    /* Expander başlıkları (summary) hover/active/focus → gri yerine koyu yeşil */
    [data-testid="stSidebar"] [data-testid="stExpander"] summary,
    [data-testid="stSidebar"] [data-testid="stExpander"] details > summary,
    [data-testid="stSidebar"] details summary {
        background: transparent !important;
        color: #ffffff !important;
        transition: background 0.2s ease !important;
    }
    [data-testid="stSidebar"] [data-testid="stExpander"] summary:hover,
    [data-testid="stSidebar"] [data-testid="stExpander"] summary:active,
    [data-testid="stSidebar"] [data-testid="stExpander"] summary:focus,
    [data-testid="stSidebar"] [data-testid="stExpander"] summary:focus-visible,
    [data-testid="stSidebar"] details > summary:hover,
    [data-testid="stSidebar"] details > summary:active,
    [data-testid="stSidebar"] details > summary:focus {
        background: #1B4332 !important;
        background-color: #1B4332 !important;
        color: #ffffff !important;
        outline: none !important;
        box-shadow: none !important;
    }
    [data-testid="stSidebar"] [data-testid="stExpander"] summary:hover *,
    [data-testid="stSidebar"] [data-testid="stExpander"] summary:focus *,
    [data-testid="stSidebar"] [data-testid="stExpander"] summary:active * {
        color: #ffffff !important;
        background: transparent !important;
    }
    /* Tüm sidebar buton/etkileşim öğeleri için varsayılan gri hover'ı bastır */
    [data-testid="stSidebar"] button:hover,
    [data-testid="stSidebar"] button:focus,
    [data-testid="stSidebar"] button:active {
        background-color: #1B4332 !important;
        color: #ffffff !important;
    }
    .result-card .result-name { color: #FFD700 !important; }
    .result-card .result-en, .result-card .confidence-lbl { color: #95D5B2 !important; }
    .result-card .confidence-val { color: #FFD700 !important; }
    .sidebar-box h4 { color: #95D5B2 !important; }
    .sidebar-box p { color: rgba(255,255,255,0.85) !important; }

    .stApp [data-testid="stCaptionContainer"],
    .stApp .stCaption {
        color: #4B5563 !important;
    }
    /* Number input alanı içindeki yazı + imleç */
    .stNumberInput input,
    div[data-testid="stNumberInput"] input {
        color: #1B4332 !important;
        background: #ffffff !important;
        caret-color: #1B4332 !important;
        -webkit-text-fill-color: #1B4332 !important;
    }
    .stNumberInput input:focus,
    div[data-testid="stNumberInput"] input:focus {
        outline: none !important;
        caret-color: #1B4332 !important;
    }
    /* Input dış kapsayıcısı (baseweb) odaklanınca yeşil kenarlık */
    div[data-testid="stNumberInput"] [data-baseweb="input"] {
        background: #ffffff !important;
        border: 1px solid rgba(45,106,79,0.25) !important;
        border-radius: 8px !important;
    }
    div[data-testid="stNumberInput"] [data-baseweb="input"]:focus-within {
        border-color: #2D6A4F !important;
        box-shadow: 0 0 0 3px rgba(45,106,79,0.15) !important;
    }
    /* Help (?) tooltip metni */
    [data-baseweb="tooltip"], [data-baseweb="tooltip"] * {
        color: #1B4332 !important;
        background: #ffffff !important;
    }
    /* Expander içerikleri */
    .streamlit-expanderHeader, [data-testid="stExpander"] summary,
    [data-testid="stExpander"] p, [data-testid="stExpander"] td,
    [data-testid="stExpander"] th, [data-testid="stExpander"] li {
        color: #1B4332 !important;
    }

    /* ── Hero ── */
    .hero {
        background: linear-gradient(135deg, #1B4332 0%, #2D6A4F 55%, #40916C 100%);
        border-radius: 20px;
        padding: 42px 40px;
        text-align: center;
        margin-bottom: 28px;
        box-shadow: 0 12px 40px rgba(27,67,50,0.30);
        position: relative;
        overflow: hidden;
    }
    .hero::after {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(ellipse at 70% 30%, rgba(255,255,255,0.06) 0%, transparent 65%);
        pointer-events: none;
    }
    .hero-icon  { font-size: 3.4em; display: block; margin-bottom: 12px; }
    .hero-title { font-size: 2.6em; font-weight: 700; color: #fff; margin: 0;
                  text-shadow: 0 2px 12px rgba(0,0,0,0.25); }
    .hero-sub   { font-size: 1.05em; color: #95D5B2; margin-top: 8px; font-weight: 300; }

    /* ── Cards ── */
    .card {
        background: #fff;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        border: 1px solid rgba(45,106,79,0.10);
        margin-bottom: 18px;
        height: 100%;
    }
    .card-header {
        font-size: 1.05em; font-weight: 600; color: #1B4332;
        border-bottom: 2px solid #95D5B2; padding-bottom: 10px; margin-bottom: 14px;
        display: block;
    }

    /* ── Mega result card (modal içinde, YATAY layout) ── */
    .mega-result-card {
        background: linear-gradient(135deg, #1B4332 0%, #2D6A4F 60%, #40916C 100%);
        border-radius: 18px;
        padding: 22px 24px;
        margin: 0;
        box-shadow: 0 14px 42px rgba(27,67,50,0.45);
        animation: slideFadeIn 0.4s ease-out;
        color: #fff;
        display: grid;
        grid-template-columns: 1fr 1.4fr;
        gap: 22px;
        align-items: stretch;
    }
    .mega-hero {
        text-align: center;
        padding: 14px 10px;
        border-right: 1px solid rgba(255,255,255,0.18);
        border-bottom: none !important;
        margin-bottom: 0 !important;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .mega-icon { font-size: 3.0em !important; margin-bottom: 4px !important; }
    .mega-name { font-size: 1.4em !important; letter-spacing: 1.5px !important; }
    .mega-en   { font-size: 0.78em !important; }
    .mega-confidence { margin-top: 12px !important; padding: 6px 16px !important; }
    .mega-conf-val   { font-size: 1.35em !important; }
    .mega-conf-lbl   { font-size: 0.72em !important; }

    .mega-right { display: flex; flex-direction: column; gap: 12px; }
    .mega-right .mega-section { margin-top: 0; }
    .mega-right .mega-section + .mega-section {
        padding-top: 12px;
        border-top: 1px solid rgba(255,255,255,0.18);
    }

    /* Modal genişliği + dış kısım daha koyu yeşil */
    [data-testid="stDialog"] [role="dialog"] {
        background: #0A1F15 !important;
        background-color: #0A1F15 !important;
        border-radius: 18px !important;
        box-shadow: 0 20px 60px rgba(0,0,0,0.55) !important;
        max-width: 820px !important;
        width: 90vw !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
    }
    /* Modal iç alan/wrapper da koyu yeşil */
    [data-testid="stDialog"] [role="dialog"] > div,
    [data-testid="stDialog"] [role="dialog"] [data-testid="stDialogContent"],
    [data-testid="stDialog"] [role="dialog"] [data-testid="stVerticalBlock"] {
        background: transparent !important;
        background-color: transparent !important;
    }
    /* Modal başlığı (üstteki "🌾 Mahsül Önerisi") beyaz */
    [data-testid="stDialog"] [role="dialog"] h1,
    [data-testid="stDialog"] [role="dialog"] h2,
    [data-testid="stDialog"] [role="dialog"] h3,
    [data-testid="stDialog"] [role="dialog"] header,
    [data-testid="stDialog"] [role="dialog"] header * {
        color: #ffffff !important;
        background: transparent !important;
    }
    /* X butonu beyaz */
    [data-testid="stDialog"] [role="dialog"] button[aria-label*="Close" i] svg,
    [data-testid="stDialog"] [role="dialog"] button[aria-label*="close" i] svg,
    [data-testid="stDialog"] [role="dialog"] button[aria-label*="Close" i] svg *,
    [data-testid="stDialog"] [role="dialog"] [data-testid="stDialogCloseButton"] svg,
    [data-testid="stDialog"] [role="dialog"] [data-testid="stDialogCloseButton"] svg * {
        color: #ffffff !important;
        fill: #ffffff !important;
        stroke: #ffffff !important;
    }

    /* Dar ekranda iki kolonu üst üste al */
    @media (max-width: 720px) {
        .mega-result-card {
            grid-template-columns: 1fr;
        }
        .mega-hero {
            border-right: none;
            border-bottom: 1px solid rgba(255,255,255,0.18);
            padding-bottom: 14px;
        }
    }
    .mega-hero {
        text-align: center;
        padding-bottom: 18px;
        border-bottom: 1px solid rgba(255,255,255,0.15);
        margin-bottom: 18px;
    }
    .mega-icon {
        font-size: 3.4em;
        display: block;
        margin-bottom: 6px;
    }
    .mega-name {
        font-size: 1.8em;
        font-weight: 700;
        color: #FFD700 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.30);
    }
    .mega-en {
        color: #95D5B2 !important;
        font-size: 0.85em;
        margin-top: 4px;
    }
    .mega-confidence {
        display: inline-block;
        margin-top: 14px;
        background: rgba(255,255,255,0.12);
        border-radius: 10px;
        padding: 8px 22px;
    }
    .mega-conf-val {
        font-size: 1.6em;
        font-weight: 700;
        color: #FFD700 !important;
        display: block;
        line-height: 1;
    }
    .mega-conf-lbl {
        color: #95D5B2 !important;
        font-size: 0.78em;
    }
    .mega-section {
        margin-top: 16px;
    }
    .mega-section + .mega-section {
        padding-top: 16px;
        border-top: 1px solid rgba(255,255,255,0.15);
    }
    .mega-section-title {
        font-size: 1.0em;
        font-weight: 600;
        color: #95D5B2 !important;
        margin-bottom: 10px;
        letter-spacing: 0.5px;
    }
    .mega-result-card .prob-row { margin: 8px 0; }
    .mega-result-card .prob-meta { color: #fff !important; }

    /* Eski result-card stilini de bırakıyorum (kullanılmıyor ama bozulmasın) */
    .result-card {
        background: linear-gradient(135deg, #1B4332, #2D6A4F);
        border-radius: 20px; padding: 38px;
        text-align: center;
        box-shadow: 0 10px 35px rgba(27,67,50,0.40);
        margin: 22px 0;
        animation: slideFadeIn 0.6s ease-out;
    }
    @keyframes slideFadeIn {
        from { opacity: 0; transform: translateY(30px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .prob-row { animation: slideFadeIn 0.5s ease-out both; }
    html { scroll-behavior: smooth; }
    .result-icon  { font-size: 4.2em; display: block; margin-bottom: 14px; }
    .result-name  { font-size: 2.0em; font-weight: 700; color: #FFD700;
                    text-transform: uppercase; letter-spacing: 3px;
                    text-shadow: 0 2px 10px rgba(0,0,0,0.30); }
    .result-en    { color: #95D5B2; font-size: 0.9em; margin-top: 6px; }
    .confidence-box {
        display: inline-block;
        margin-top: 20px;
        background: rgba(255,255,255,0.12);
        border-radius: 12px; padding: 12px 28px;
    }
    .confidence-val { font-size: 2.0em; font-weight: 700; color: #FFD700; }
    .confidence-lbl { color: #95D5B2; font-size: 0.82em; }

    /* ── Probability bars ── */
    .prob-row { margin: 14px 0; }
    .prob-meta { display: flex; justify-content: space-between;
                 margin-bottom: 5px; font-weight: 500; color: #1B4332; }
    .prob-bg   { background: #e8f5e9; border-radius: 10px; height: 13px; overflow: hidden; }
    .prob-fill { height: 100%; border-radius: 10px;
                 background: linear-gradient(90deg, #2D6A4F, #52B788); }

    /* ── Sidebar info box ── */
    .sidebar-box {
        background: linear-gradient(135deg, #1B4332, #2D6A4F);
        border-radius: 14px; padding: 18px; color: #fff; margin-bottom: 16px;
    }
    .sidebar-box h4 { color: #95D5B2; margin: 0 0 8px 0; }
    .sidebar-box p  { color: rgba(255,255,255,0.80); font-size: 0.88em; margin: 0; }

    /* ── Metrics ── */
    [data-testid="metric-container"] {
        background: #fff; border-radius: 12px; padding: 14px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.05);
        border-left: 4px solid #2D6A4F;
    }

    /* ── Number input labels ── */
    div[data-testid="stNumberInput"] label,
    div[data-testid="stNumberInputContainer"] label,
    .stNumberInput label {
        color: #1B4332 !important;
        font-weight: 600 !important;
        font-size: 0.95em !important;
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
        line-height: 1.2 !important;
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    /* Etiket ile input kutusu arasındaki boşluğu iyice daralt */
    div[data-testid="stNumberInput"] > label,
    .stNumberInput > label {
        margin-bottom: -4px !important;
        padding-bottom: 0 !important;
    }
    div[data-testid="stNumberInput"] [data-testid="stWidgetLabel"],
    .stNumberInput [data-testid="stWidgetLabel"] {
        margin: 0 !important;
        margin-bottom: -4px !important;
        padding: 0 !important;
        min-height: 0 !important;
        gap: 0 !important;
    }
    div[data-testid="stNumberInput"] [data-testid="stWidgetLabel"] p,
    div[data-testid="stNumberInput"] label p {
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1.1 !important;
    }
    /* Inputun üst boşluğunu da kıs */
    div[data-testid="stNumberInput"] > div:nth-child(2),
    div[data-testid="stNumberInput"] [data-baseweb="input"] {
        margin-top: 0 !important;
    }
    /* Inputlar arası dikey aralığı da sıkılaştır */
    div[data-testid="stNumberInput"] {
        margin-bottom: 4px !important;
    }

    /* ── Button ── */
    .stButton > button {
        background: linear-gradient(135deg, #2D6A4F, #40916C) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 30px !important;
        font-size: 1.08em !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 5px 18px rgba(45,106,79,0.40) !important;
        transition: all 0.25s ease !important;
    }
    .stButton > button *,
    .stButton > button p,
    .stButton > button div,
    .stButton > button span {
        background: transparent !important;
        background-color: transparent !important;
        background-image: none !important;
        color: #ffffff !important;
        box-shadow: none !important;
        border: none !important;
    }
    .stButton > button:hover,
    .stButton > button:focus,
    .stButton > button:active {
        color: #ffffff !important;
    }
    .stButton > button:hover *,
    .stButton > button:focus *,
    .stButton > button:active * {
        color: #ffffff !important;
        background: transparent !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 9px 26px rgba(45,106,79,0.50) !important;
    }

    /* ── Section title ── */
    .section-title {
        font-size: 1.25em; font-weight: 600; color: #1B4332; margin-bottom: 14px;
    }

    /* ── pH badge ── */
    .ph-badge {
        display: inline-block; border-radius: 8px; padding: 4px 12px;
        font-size: 0.88em; font-weight: 600;
    }

    /* ── Footer ── */
    .footer {
        text-align: center; color: #6B7280; font-size: 0.82em;
        padding: 14px; margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────────
MODEL_PATH   = "models/best_model.pkl"
SCALER_PATH  = "models/scaler.pkl"
ENCODER_PATH = "models/label_encoder.pkl"
FEATS_PATH   = "models/feature_names.pkl"

CROP_EMOJI = {
    "rice": "🌾", "maize": "🌽", "chickpea": "🫘", "kidneybeans": "🫘",
    "pigeonpeas": "🫘", "mothbeans": "🫘", "mungbean": "🫘", "blackgram": "🫘",
    "lentil": "🫘", "pomegranate": "🍈", "banana": "🍌", "mango": "🥭",
    "grapes": "🍇", "watermelon": "🍉", "muskmelon": "🍈", "apple": "🍎",
    "orange": "🍊", "papaya": "🍑", "coconut": "🥥", "cotton": "🌿",
    "jute": "🌿", "coffee": "☕",
}
CROP_TR = {
    "rice": "Pirinç", "maize": "Mısır", "chickpea": "Nohut",
    "kidneybeans": "Barbunya", "pigeonpeas": "Güvercin Bezelyesi",
    "mothbeans": "Güve Fasulyesi", "mungbean": "Maş Fasulyesi",
    "blackgram": "Kara Mercimek", "lentil": "Mercimek",
    "pomegranate": "Nar", "banana": "Muz", "mango": "Mango",
    "grapes": "Üzüm", "watermelon": "Karpuz", "muskmelon": "Kavun",
    "apple": "Elma", "orange": "Portakal", "papaya": "Papaya",
    "coconut": "Hindistan Cevizi", "cotton": "Pamuk",
    "jute": "Jüt", "coffee": "Kahve",
}


# ── Helpers ────────────────────────────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    model   = joblib.load(MODEL_PATH)
    scaler  = joblib.load(SCALER_PATH)
    encoder = joblib.load(ENCODER_PATH)
    feats   = joblib.load(FEATS_PATH)
    return model, scaler, encoder, feats

def check_models():
    return all(os.path.exists(p) for p in [MODEL_PATH, SCALER_PATH, ENCODER_PATH, FEATS_PATH])

def ph_label(ph: float) -> str:
    if ph < 5.5:   return "Çok Asidik 🔴"
    if ph < 6.5:   return "Hafif Asidik 🟠"
    if ph <= 7.5:  return "Nötr 🟢"
    if ph <= 8.5:  return "Hafif Bazik 🔵"
    return "Bazik 🟣"


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-box">
        <h4>🌱 Proje Hakkında</h4>
        <p>Toprak besin değerleri ve iklim koşullarına göre hangi mahsülün
        yetiştirilmesi gerektiğini tahmin eden yapay zeka uygulaması.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📖 Referans Değerler")
    with st.expander("🧪 NPK Rehberi"):
        st.markdown("""
        | Besin | Görevi |
        |-------|--------|
        | **N** | Yaprak & büyüme |
        | **P** | Kök gelişimi |
        | **K** | Meyve kalitesi |
        """)
    with st.expander("🌡️ pH Skalası"):
        st.markdown("""
        - **< 5.5** – Çok asidik
        - **5.5–6.5** – Hafif asidik *(çoğu mahsül)*
        - **6.5–7.5** – Nötr *(ideal)*
        - **> 7.5** – Bazik
        """)
    with st.expander("💧 Yağış Bantları"):
        st.markdown("""
        - **< 100 mm** – Kurak
        - **100–600 mm** – Orta
        - **> 600 mm** – Yağışlı
        """)

    st.markdown("---")
    st.caption("Crop Recommendation Dataset kullanılarak geliştirilmiştir. ")


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <span class="hero-icon">🌾</span>
    <h1 class="hero-title">Mahsül Öneri Sistemi</h1>
    <p class="hero-sub">Toprak ve iklim verilerinize göre en uygun mahsülü keşfedin</p>
</div>
""", unsafe_allow_html=True)

# ── Model check ────────────────────────────────────────────────────────────────
if not check_models():
    st.error(
        "⚠️ Model dosyaları bulunamadı. "
        "Lütfen önce `analiz_ve_modelleme.ipynb` notebook'unu çalıştırın."
    )
    st.stop()

model, scaler, encoder, feature_names = load_artifacts()

# ── Inputs ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">📋 Toprak & İklim Parametreleri</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown('<div class="card-header">🧪 Toprak Besinleri</div>', unsafe_allow_html=True)
    N = st.number_input("Azot (N) – kg/ha", min_value=0, max_value=200, value=50, step=1,
                        help="Topraktaki azot miktarı")
    P = st.number_input("Fosfor (P) – kg/ha", min_value=0, max_value=200, value=50, step=1,
                        help="Topraktaki fosfor miktarı")
    K = st.number_input("Potasyum (K) – kg/ha", min_value=0, max_value=210, value=50, step=1,
                        help="Topraktaki potasyum miktarı")

with col2:
    st.markdown('<div class="card-header">🌡️ İklim Koşulları</div>', unsafe_allow_html=True)
    temperature = st.number_input("Sıcaklık – °C", min_value=0.0, max_value=55.0, value=25.0, step=0.1,
                                  help="Ortalama yıllık sıcaklık")
    humidity = st.number_input("Nem – %", min_value=0.0, max_value=100.0, value=70.0, step=0.1,
                               help="Bağıl nem oranı")
    rainfall = st.number_input("Yağış – mm", min_value=0.0, max_value=3000.0, value=200.0, step=1.0,
                               help="Yıllık toplam yağış miktarı")

with col3:
    st.markdown('<div class="card-header">🌍 Toprak Özellikleri</div>', unsafe_allow_html=True)
    ph = st.number_input("pH Değeri – (0–14)", min_value=0.0, max_value=14.0, value=6.5, step=0.01,
                         help="Toprak pH değeri (0–14)")

    ph_text = ph_label(ph)

    st.markdown("---")
    st.markdown("**Özet:**")
    st.caption(f"N {N} kg/ha · P {P} kg/ha · K {K} kg/ha")
    st.caption(f"Sıcaklık {temperature}°C · Nem {humidity}%")
    st.caption(f"Yağış {rainfall} mm · pH {ph}")

# ── Predict button ─────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
clicked = st.button("🔍 Mahsül Analizi Yap", use_container_width=True, type="primary")

# ── Results modal (st.dialog) ──────────────────────────────────────────────────
@st.dialog("🌾 Mahsül Önerisi", width="large")
def show_result_modal(N, P, K, temperature, humidity, ph, rainfall):
    input_arr    = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
    input_scaled = scaler.transform(input_arr)

    pred_enc   = model.predict(input_scaled)[0]
    pred_label = encoder.inverse_transform([pred_enc])[0]

    probs       = model.predict_proba(input_scaled)[0]
    top3_idx    = np.argsort(probs)[::-1][:3]
    top3_labels = encoder.inverse_transform(top3_idx)
    top3_probs  = probs[top3_idx]

    emoji      = CROP_EMOJI.get(pred_label, "🌿")
    name_tr    = CROP_TR.get(pred_label, pred_label.capitalize())
    confidence = top3_probs[0] * 100

    bar_colors = [
        ("linear-gradient(90deg,#2D6A4F,#40916C)", "#2D6A4F"),
        ("linear-gradient(90deg,#40916C,#52B788)", "#40916C"),
        ("linear-gradient(90deg,#52B788,#74C69D)", "#52B788"),
    ]
    medals = ["🥇", "🥈", "🥉"]

    prob_html = ""
    for i, (lbl, prob) in enumerate(zip(top3_labels, top3_probs)):
        em  = CROP_EMOJI.get(lbl, "🌿")
        tr  = CROP_TR.get(lbl, lbl.capitalize())
        pct = prob * 100
        grad, _ = bar_colors[i]
        prob_html += (
            f'<div class="prob-row">'
            f'<div class="prob-meta">'
            f'<span style="color:#fff;">{medals[i]} {em} {tr} '
            f'<span style="color:rgba(255,255,255,0.6);font-size:0.83em">({lbl})</span></span>'
            f'<span style="color:#FFD700;font-weight:700">{pct:.2f}%</span>'
            f'</div>'
            f'<div class="prob-bg" style="background:rgba(255,255,255,0.15);">'
            f'<div class="prob-fill" style="width:{pct}%;background:{grad}"></div>'
            f'</div></div>'
        )

    rows = [
        ("🌿", "Azot (N)",     f"{N} kg/ha"),
        ("🌿", "Fosfor (P)",   f"{P} kg/ha"),
        ("🌿", "Potasyum (K)", f"{K} kg/ha"),
        ("🌡️", "Sıcaklık",    f"{temperature} °C"),
        ("💧", "Nem",          f"{humidity} %"),
        ("🌍", "pH",           str(ph)),
        ("🌧️", "Yağış",       f"{rainfall} mm"),
    ]
    rows_html = "".join(
        f'<tr><td style="padding:6px 12px;color:rgba(255,255,255,0.75);">{icon} {param}</td>'
        f'<td style="padding:6px 12px;font-weight:600;color:#FFD700;text-align:right;">{val}</td></tr>'
        for icon, param, val in rows
    )

    mega_html = (
        f'<div class="mega-result-card">'
        f'<div class="mega-hero">'
        f'<span class="mega-icon">{emoji}</span>'
        f'<div class="mega-name">{name_tr}</div>'
        f'<div class="mega-en">({pred_label.upper()})</div>'
        f'<div class="mega-confidence">'
        f'<span class="mega-conf-val">{confidence:.1f}%</span>'
        f'<span class="mega-conf-lbl">Tahmin Dağılımı</span>'
        f'</div></div>'
        f'<div class="mega-right">'
        f'<div class="mega-section">'
        f'<div class="mega-section-title">🏆 En Olası 3 Mahsül</div>'
        f'{prob_html}'
        f'</div>'
        f'<div class="mega-section">'
        f'<div class="mega-section-title">📋 Kullanılan Değerler</div>'
        f'<table style="width:100%;border-collapse:collapse;font-size:0.85em;">{rows_html}</table>'
        f'</div>'
        f'</div></div>'
    )
    st.markdown(mega_html, unsafe_allow_html=True)


if clicked:
    show_result_modal(N, P, K, temperature, humidity, ph, rainfall)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div class="footer">
    🌱 Crop Recommendation System &nbsp;·&nbsp;
    Makine Öğrenmesi ile Tarım Analizi &nbsp;·&nbsp;
    22 Mahsül Sınıfı
</div>
""", unsafe_allow_html=True)
