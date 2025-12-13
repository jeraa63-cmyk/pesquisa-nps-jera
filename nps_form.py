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

:root {
  --jera-primary:#00C1AD;
  --jera-dark:#052B38;
  --jera-bg:#052B38;
  --jera-light:#FFFFFF;
  --muted:#6b7c85;
}

header[data-testid="stHeader"], footer {display:none !important;}
html, body, .stApp {
  background: var(--jera-bg) !important;
  font-family: 'Ofelia Text', sans-serif !important;
  color: var(--jera-dark);
  margin: 0 !important;
  padding: 0 !important;
  overflow-x: hidden !important;
}

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

h1 {
  font-family: 'Ofelia Display', sans-serif !important;
  text-align: center !important;
  margin-top: -70px !important;   /* 🔽 AJUSTE AQUI */
  font-size: 2.0rem !important;
}

.stTextInput {
  display: flex !important;
  justify-content: center !important;
}
.stTextInput input {
  text-align: center !important;
  width: 285px !important;
  border-radius: 10px !important;
}

.stButton > button {
  font-family: 'Ofelia Display', sans-serif !important;
  background: #052B38 !important;
  color: white !important;
  border-radius: 12px !important;
  min-width: 220px !important;
  min-height: 50px !important;
  box-shadow: 0 6px 14px rgba(0,0,0,.15);
}

.footer-fixed {
  position: fixed !important;
  bottom: 10px !important;
  left: 16px !important;
  font-size: 0.9rem !important;
  color: #7A8C94 !important;
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


# ===================== TELA 1 =====================
if st.session_state["step"] == 1:

    if LOGO_FULL.exists():
        st.markdown(
            f"<img src='{_img_data_uri(LOGO_FULL)}' "
            "style='display:block;margin:-90px auto -15px auto;width:480px;max-width:95%;'/>",
            unsafe_allow_html=True,
        )

    st.markdown("<h1>PESQUISA DE SATISFAÇÃO</h1>", unsafe_allow_html=True)

    st.markdown("<p style='text-align:center;font-weight:650;'>CÓDIGO DO CLIENTE</p>", unsafe_allow_html=True)
    st.text_input("", key="client_code", placeholder="Ex.: 12345")

    st.markdown(
        """
        <p style='text-align:center;max-width:800px;margin:auto;'>
        <strong>Esta é uma pesquisa identificada.</strong><br/>
        Suas respostas serão tratadas com confidencialidade e utilizadas exclusivamente
        para aperfeiçoarmos nossos serviços, sempre alinhados aos seus objetivos.
        </p>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Iniciar pesquisa"):
            if st.session_state["client_code"].strip():
                st.session_state["step"] = 2
                st.rerun()
            else:
                st.error("Por favor, preencha o código do cliente.")

st.markdown("<div class='footer-fixed'>© Jera Capital — Todos os direitos reservados.</div>", unsafe_allow_html=True)
