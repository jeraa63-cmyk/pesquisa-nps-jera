from pathlib import Path
import base64
import os
import streamlit as st
import pandas as pd
from datetime import datetime

# ===================== CONFIGURAÇÃO: Excel local =====================
LOCAL_XLSX_PATH = r"C:\\Users\\AnaSilvaJeraCapital\\OneDrive - JERA CAPITAL GESTAO DE RECURSOS LTDA\\Comercial - Documentos\\NPS\\Pesquisa_NPS.xlsx"
SHOW_INTERNAL_NPS = False

# ===================== PÁGINA + CSS =====================
st.set_page_config(page_title="PESQUISA DE SATISFAÇÃO", layout="wide")

st.markdown(
    """
<style>
/* ===================== FONTES ===================== */
@font-face {
  font-family: 'Ofelia Display';
  src: url('assets/fontes/OfeliaText-Bold.ttf') format('truetype');
  font-weight: 700;
}
@font-face {
  font-family: 'Ofelia Text';
  src: url('assets/fontes/OfeliaText-Regular.ttf') format('truetype');
  font-weight: 400;
}
@font-face {
  font-family: 'Ofelia Text';
  src: url('assets/fontes/OfeliaText-Medium.ttf') format('truetype');
  font-weight: 500;
}
@font-face {
  font-family: 'Ofelia Text';
  src: url('assets/fontes/OfeliaText-Light.ttf') format('truetype');
  font-weight: 300;
}

/* ===================== VARIÁVEIS ===================== */
:root {
  --jera-primary:#00C1AD;
  --jera-dark:#052B38;
  --jera-bg:#052B38;
  --jera-light:#FFFFFF;
  --muted:#6b7c85;
}

/* ===================== RESET / BACKGROUND ===================== */
header[data-testid="stHeader"], footer {display:none !important;}
html, body, .stApp {
  background: var(--jera-bg) !important;
  font-family: 'Ofelia Text', sans-serif !important;
  color: var(--jera-dark);
  margin: 0 !important;
  padding: 0 !important;
  overflow-x: hidden !important;
}

/* ===================== CAIXA BRANCA ===================== */
div.block-container {
  background: var(--jera-light) !important;
  border-radius: 22px !important;
  width: min(1200px, 96vw) !important;
  margin: 2vh auto !important;
  min-height: calc(100vh - 4vh) !important;
  padding: 3.2rem 4.0rem !important;
  box-shadow: 0 6px 18px rgba(0,0,0,.08);
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
}

@media (max-width: 1200px){
  div.block-container { padding: 2.4rem 2.0rem !important; }
}
@media (max-width: 1024px){
  div.block-container {
    width: 100vw !important;
    border-radius: 0 !important;
    min-height: 100vh !important;
    padding: 2.0rem 1.2rem 2.6rem 1.2rem !important;
  }
}

/* ===================== TIPOGRAFIA ===================== */
h1, h2, h3 {
  font-family: 'Ofelia Display', sans-serif !important;
  text-align: center !important;
  margin-top: 0.4rem !important;
}

h1 { font-size: clamp(2.2rem, 3.2vw, 3.6rem) !important; font-weight: 700 !important; }
h2 { font-size: clamp(1.6rem, 2.3vw, 2.4rem) !important; }
h3 { font-size: clamp(1.2rem, 1.8vw, 2.0rem) !important; }

p, div, span, label {
  font-size: clamp(1.0rem, 1.2vw, 1.15rem) !important;
  line-height: 1.65 !important;
}

/* ===================== INPUT ===================== */
.stTextInput {
  display: flex !important;
  justify-content: center !important;
}
.stTextInput input {
  text-align: center !important;
  width: 285px !important;
  border-radius: 10px !important;
}

/* ===================== BOTÕES ===================== */
.stButton > button {
  background: #052B38 !important;
  color: white !important;
  border-radius: 12px !important;
  min-width: 220px !important;
  min-height: 50px !important;
}

/* ===================== RODAPÉ ===================== */
.footer-fixed {
  position: fixed;
  bottom: 10px;
  left: 16px;
  font-size: 0.9rem;
  color: #7A8C94;
}
</style>
""",
    unsafe_allow_html=True,
)

# ===================== LOGO =====================
BASE_DIR = Path(__file__).parent.resolve()
ASSETS = BASE_DIR / "assets"
LOGO_FULL = ASSETS / "jera-logo-full.png"

def _img_data_uri(p: Path) -> str:
    return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()

# ===================== ESTADO =====================
if "step" not in st.session_state:
    st.session_state["step"] = 1
if "client_code" not in st.session_state:
    st.session_state["client_code"] = ""
