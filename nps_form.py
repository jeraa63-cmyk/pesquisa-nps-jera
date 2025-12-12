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

# ===================== TELA 1 =====================
if st.session_state["step"] == 1:

    if LOGO_FULL.exists():
        st.markdown(
            f"<img alt='Jera' src='{_img_data_uri(LOGO_FULL)}' "
            "style='display:block;margin:-90px auto 0 auto;width:480px;max-width:95%;'/>",
            unsafe_allow_html=True,
        )

    # ✅ TÍTULO SUBIDO + FONTE REDUZIDA (SEM CONFLITO COM CSS)
    st.markdown(
        """
        <h1 style="
            transform: translateY(-44px);
            font-size: 2.2rem;
        ">
            PESQUISA DE SATISFAÇÃO
        </h1>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:1.1rem;'></div>", unsafe_allow_html=True)

    st.markdown(
        "<p style='font-size:1.2rem;font-weight:650;text-align:center;'>CÓDIGO DO CLIENTE</p>",
        unsafe_allow_html=True,
    )
    st.text_input("", key="client_code", placeholder="Ex.: 12345", max_chars=20)

    st.markdown("<div style='height:0.8rem;'></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div style='text-align:center; line-height:1.6;'>
          <p><strong>Esta é uma pesquisa identificada.</strong></p>
          <p style='font-size:1.05rem;'>
            Suas respostas serão tratadas com confidencialidade e utilizadas exclusivamente
            para aperfeiçoarmos nossos serviços, sempre alinhados aos seus objetivos.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:0.6rem;'></div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([3, 2, 3])
    with c2:
        if st.button("Iniciar pesquisa", key="start_button"):
            if not st.session_state["client_code"].strip():
                st.error("Por favor, preencha o código do cliente.")
            else:
                st.session_state["step"] = 2
                st.rerun()


# ===================== BLOCOS DE PERGUNTAS =====================
BLOCOS = [
    (
        "Qualidade do Relacionamento com a Equipe Jera",
        [
            ("Tempo de resolução às solicitações",
             "De 01 a 05, quanto você está satisfeito(a) com a agilidade e disponibilidade da equipe ao atender suas solicitações?"),
            ("Proatividade na comunicação",
             "De 01 a 05, quanto a equipe se antecipa às suas necessidades e se comunica de forma proativa?")
        ],
    ),
    (
        "Clareza e Relevância das Informações Prestadas",
        [
            ("Clareza das informações apresentadas",
             "De 01 a 05, o quanto as informações e o detalhamento dos relatórios atendem às suas expectativas?"),
            ("Compreensão dos resultados",
             "De 01 a 05, o quanto os relatórios ajudam você a entender se a carteira está caminhando conforme seus objetivos?")
        ],
    ),
    (
        "Efetividade dos Encontros e Alinhamentos",
        [
            ("Frequência, formato e duração das reuniões",
             "De 01 a 05, como você avalia a adequação da frequência, do formato e da duração das reuniões?"),
            ("Relevância e efetividade das reuniões",
             "De 01 a 05, o quanto as reuniões apresentam conteúdos relevantes, claros e bem organizados?")
        ],
    ),
    (
        "Percepção sobre o Desempenho da Carteira",
        [
            ("Satisfação com o retorno obtido",
             "De 01 a 05, o quanto você está satisfeito com o retorno da sua carteira nos últimos meses?"),
            ("Alinhamento entre retorno e perfil de risco",
             "De 01 a 05, o quanto o retorno da carteira está compatível com seu perfil de risco e objetivos financeiros?")
        ],
    ),
    (
        "Compromisso com a Transparência e Integridade",
        [
            ("Independência nas recomendações",
             "De 01 a 05, o quanto você percebe independência e isenção nas recomendações feitas pela equipe?"),
            ("Transparência sobre custos e remunerações",
             "De 01 a 05, o quanto você sente clareza nas informações sobre custos, taxas e formas de remuneração?")
        ],
    ),
]


def _touch(key):
    st.session_state[f"{key}__touched"] = True


def escala_1a5(key):
    if f"{key}__touched" not in st.session_state:
        st.session_state[f"{key}__touched"] = False
    if key not in st.session_state:
        st.session_state[key] = 3

    val = st.slider(
        "",
        1, 5,
        value=st.session_state[key],
        key=key,
        on_change=_touch,
        args=(key,),
        label_visibility="collapsed",
    )
    return val


# ===================== TELAS 2–6 =====================
elif 2 <= st.session_state["step"] <= 6:
    idx = st.session_state["step"] - 2
    titulo, perguntas = BLOCOS[idx]

    st.markdown(f"<h2>{titulo}</h2>", unsafe_allow_html=True)

    respostas = st.session_state.get(f"respostas_{idx}", {})

    for i, (topico, texto) in enumerate(perguntas):
        st.markdown(f"<h3>{topico}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center'>{texto}</p>", unsafe_allow_html=True)
        respostas[topico] = escala_1a5(f"{titulo}_{i}")

    st.session_state[f"respostas_{idx}"] = respostas

    col1, col2, col3 = st.columns([2, 6, 2])
    with col1:
        if st.button("◀ Voltar"):
            st.session_state["step"] -= 1
            st.rerun()
    with col3:
        if st.button("Avançar ►"):
            st.session_state["step"] += 1
            st.rerun()


# ===================== CONFIRMAÇÃO FINAL =====================
elif st.session_state["step"] == 7:
    st.markdown("<h2>✅ Resposta enviada com sucesso</h2>", unsafe_allow_html=True)
    st.success(
        "Agradecemos por dedicar seu tempo para responder à nossa pesquisa. "
        "Suas respostas são muito importantes para que possamos aprimorar continuamente nossos serviços."
    )

    if st.button("➕ Enviar nova resposta"):
        st.session_state.clear()
        st.session_state["step"] = 1
        st.rerun()


# ===================== RODAPÉ =====================
st.markdown(
    "<div class='footer-fixed'>© Jera Capital — Todos os direitos reservados.</div>",
    unsafe_allow_html=True,
)


