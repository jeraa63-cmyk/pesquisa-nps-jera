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

 /* ===================== CAIXA BRANCA (TELA TODA) ===================== */
 section.main, div.block-container {
   background: var(--jera-light) !important;
   border-radius: 22px !important;
   width: 96vw !important;            /* ocupa quase toda a tela */
   min-height: 96vh !important;
   margin: 2vh auto !important;
   padding: 4rem 6rem !important;      /* padding fixo para toda tela */
   box-shadow: 0 6px 18px rgba(0,0,0,.08);
   display: flex !important;
   flex-direction: column !important;
   justify-content: flex-start !important;
   align-items: center !important;
   box-sizing: border-box !important;  /* impede conteúdo de “vazar” */
 }

 /* ===================== TÍTULOS ===================== */
 h1, h2, h3 {
   font-family: 'Ofelia Display', sans-serif !important;
   color: var(--jera-dark);
   text-align: center !important;
 }
 h1 { font-size: 3.8rem !important; font-weight: 700 !important; transform: translateX(18px); }
 h2 { font-size: 2.4rem !important; font-weight: 600 !important; margin-bottom: 2.2rem !important; }
 h3 { font-size: 2.0rem !important; font-weight: 500 !important; }

 @media (max-width: 1024px){
   h1 { transform: none !important; }
 }

 /* ===================== TEXTOS ===================== */
 p, div, span, label {
   font-size: 1.2rem !important;
   line-height: 1.7 !important;
 }

 /* ===================== INPUT DA TELA 1 ===================== */
 .stTextInput {
   display: flex !important;
   justify-content: center !important;
 }
 .stTextInput input {
   font-family: 'Ofelia Text', sans-serif !important;
   font-size: 1.1rem !important;
   text-align: center !important;
   padding: 0.6rem 0.8rem !important;
   border-radius: 8px !important;
   background-color: #f6f6f6 !important;
   width: 285px !important;
 }

 /* ===================== BOTÕES ===================== */
 .stButton > button {
   font-family: 'Ofelia Display', sans-serif !important;
   background: #052B38 !important;
   color: white !important;
   border: 2px solid #052B38 !important;
   border-radius: 12px !important;
   font-weight: 600 !important;
   font-size: 1.1rem !important;
   min-width: 220px !important;
   min-height: 50px !important;
   transition: all 0.25s ease-in-out;
   box-shadow: 0 6px 14px rgba(0,0,0,.15);
 }

 .stButton > button:hover {
   background: #00C1AD !important;
   border-color: #00C1AD !important;
   transform: translateY(-2px);
 }

 div[data-testid="stForm"] {
   border: none !important;
   background: transparent !important;
   padding: 0 !important;
 }

 /* rodapé fixo */
 .footer-fixed {
    position: fixed !important;
    bottom: calc(2vh + 0.5rem) !important;
    left:  calc(1vw + 1rem) !important;
    font-size: 0.9rem !important;
    color: #7A8C94 !important;
    font-family: 'Ofelia Text', sans-serif !important;
    z-index: 9999 !important;
    pointer-events: none;
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

# ===================== ESTADO INICIAL =====================
if "step" not in st.session_state:
    st.session_state["step"] = 1
if "client_code" not in st.session_state:
    st.session_state["client_code"] = ""

# ===================== PERGUNTAS =====================
BLOCOS = [
    (
        "Qualidade do Relacionamento com a Equipe Jera",
        [
            ("Tempo de resolução às solicitações",
             "De 01 a 05, quanto você está satisfeito(a) com a agilidade e disponibilidade da equipe ao atender suas solicitações?"),
            ("Proatividade na comunicação",
             "De 01 a 05, quanto a equipe se antecipa às suas necessidades e se comunica de forma proativa?")
        ]
    ),
    (
        "Clareza e Relevância das Informações Prestadas",
        [
            ("Clareza das informações apresentadas",
             "De 01 a 05, o quanto as informações e o detalhamento dos relatórios atendem às suas expectativas?"),
            ("Compreensão dos resultados",
             "De 01 a 05, o quanto os relatórios ajudam você a entender se a carteira está caminhando conforme seus objetivos?")
        ]
    ),
    (
        "Efetividade dos Encontros e Alinhamentos",
        [
            ("Frequência, formato e duração das reuniões",
             "De 01 a 05, como você avalia a adequação da frequência, do formato e da duração das reuniões?"),
            ("Relevância e efetividade das reuniões",
             "De 01 a 05, o quanto as reuniões apresentam conteúdos relevantes, claros e bem organizados?")
        ]
    ),
    (
        "Percepção sobre o Desempenho da Carteira",
        [
            ("Satisfação com o retorno obtido",
             "De 01 a 05, o quanto você está satisfeito com o retorno da sua carteira nos últimos meses?"),
            ("Alinhamento entre retorno e perfil de risco",
             "De 01 a 05, o quanto o retorno da carteira está compatível com seu perfil de risco e objetivos financeiros?")
        ]
    ),
    (
        "Compromisso com a Transparência e Integridade",
        [
            ("Independência nas recomendações",
             "De 01 a 05, o quanto você percebe independência e isenção nas recomendações feitas pela equipe?"),
            ("Transparência sobre custos e remunerações",
             "De 01 a 05, o quanto você sente clareza nas informações sobre custos, taxas e formas de remuneração?")
        ]
    ),
]

HEADERS = ["timestamp", "client_code", "NPS"] + [p[0] for _, ps in BLOCOS for p in ps] + ["coment_final"]

# ===================== FUNÇÕES =====================
def _validar_secao(notas):
    if any(v is None for v in notas.values()):
        return False, "Por favor, selecione uma opção (1–5) para todas as perguntas."
    return True, ""

def _append_to_excel(row_values):
    try:
        from openpyxl import Workbook, load_workbook
        os.makedirs(os.path.dirname(LOCAL_XLSX_PATH), exist_ok=True)

        if os.path.exists(LOCAL_XLSX_PATH):
            wb = load_workbook(LOCAL_XLSX_PATH)
        else:
            wb = Workbook()
            if wb.active.title != "Respostas":
                wb.remove(wb.active)

        ws = wb["Respostas"] if "Respostas" in wb.sheetnames else wb.create_sheet("Respostas")

        for col, header in enumerate(HEADERS, 1):
            ws.cell(row=1, column=col, value=header)

        next_row = ws.max_row + 1
        for col, val in enumerate(row_values, 1):
            ws.cell(row=next_row, column=col, value=val)

        wb.save(LOCAL_XLSX_PATH)
        return True, "Gravado no Excel."
    except Exception as e:
        return False, str(e)

# ===================== FLUXO =====================
step = st.session_state["step"]

# -------- TELA 1 --------
if step == 1:

    _, c2, _ = st.columns([1, 3, 1])

    with c2:
        if LOGO_FULL.exists():
            st.markdown(
                f"<img src='{_img_data_uri(LOGO_FULL)}' style='width:480px;max-width:95%;margin:0 auto;display:block;'/>",
                unsafe_allow_html=True,
            )

        st.markdown("<h1>PESQUISA DE SATISFAÇÃO</h1>", unsafe_allow_html=True)

        st.markdown("<div style='height:4rem;'></div>", unsafe_allow_html=True)

        st.markdown("<p style='font-size:1.3rem;font-weight:600;text-align:center;'>CÓDIGO DO CLIENTE</p>",
                    unsafe_allow_html=True)

        st.text_input("", key="client_code", placeholder="Ex.: 12345", max_chars=20)

        st.markdown("<div style='height:3rem;'></div>", unsafe_allow_html=True)

        st.markdown(
            """
            <div style='text-align:center; line-height:1.6; margin-bottom:2rem;'>
                <p style='font-size:1.15rem;'><strong>Esta é uma pesquisa identificada.</strong></p>
                <p style='font-size:1.05rem;'>
                    Suas respostas serão tratadas com confidencialidade e utilizadas exclusivamente
                    para aperfeiçoarmos nossos serviços.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        left_spacer, col_btn, right_spacer = st.columns([4.8, 2, 4])

        with col_btn:
            if st.button("Iniciar pesquisa"):
                if not st.session_state["client_code"].strip():
                    st.error("Por favor, preencha o código do cliente.")
                else:
                    st.session_state["step"] = 2
                    st.rerun()

# -------- TELAS 2–6 --------
elif 2 <= step <= 6:

    idx = step - 2
    titulo, perguntas = BLOCOS[idx]

    _, col, _ = st.columns([1, 6, 1])

    with col:

        st.markdown(f"<h2>{titulo}</h2>", unsafe_allow_html=True)

        with st.form(f"form_{idx}"):

            notas = {}

            for i, (topico, texto) in enumerate(perguntas):

                st.markdown(f"<p style='font-size:1.25rem;font-weight:700;text-align:center;'>{topico}</p>",
                            unsafe_allow_html=True)
                st.markdown(f"<p style='text-align:center;margin-top:0.3rem;margin-bottom:0.8rem;'>{texto}</p>",
                            unsafe_allow_html=True)

                _, c2, _ = st.columns([1, 3, 1])
                with c2:
                    notas[topico] = st.radio(
                        "",
                        ["1 - Péssimo", "2 - Ruim", "3 - Regular", "4 - Bom", "5 - Excelente"],
                        horizontal=True,
                        index=None,
                        key=f"{titulo}_{i}",
                    )

                st.write("")

            col1, _, col3 = st.columns([2, 4, 2])

            with col1:
                voltar = st.form_submit_button("◀ Voltar")

            with col3:
                avancar = st.form_submit_button("Avançar ►")

            if voltar:
                st.session_state["step"] -= 1
                st.rerun()

            if avancar:
                ok, msg = _validar_secao(notas)
                if not ok:
                    st.error(msg)
                else:
                    st.session_state[f"respostas_{idx}"] = notas
                    st.session_state["step"] += 1
                    st.rerun()

# -------- TELA NPS --------
elif step == 7:

    _, col, _ = st.columns([1, 6, 1])

    with col:

        st.markdown("<h2>NPS</h2>", unsafe_allow_html=True)

        st.markdown("""
        <p style='font-size:1.25rem;text-align:justify;'>
        Considerando sua experiência com os serviços da <b>Jera Capital</b>, em uma escala de <b>0 a 10</b>,
        o quanto você recomendaria a empresa a amigos ou familiares?
        </p>
        """, unsafe_allow_html=True)

        _, c2, _ = st.columns([1, 3, 1])
        with c2:
            nps = st.radio("", list(range(11)), horizontal=True, index=None, key="nps")

        st.markdown("<p style='font-size:1.2rem;margin-top:2rem;'>Comentário final:</p>",
                    unsafe_allow_html=True)

        coment_final = st.text_area("", key="coment_final")

        col1, _, col3 = st.columns([2, 4, 2])

        with col1:
            voltar = st.button("◀ Voltar")

        with col3:
            enviar = st.button("Enviar respostas ✅")

        if voltar:
            st.session_state["step"] -= 1
            st.rerun()

        if enviar:

            if nps is None:
                st.error("Selecione uma nota de 0 a 10.")
                st.stop()

            code = st.session_state["client_code"].strip()
            if not code:
                st.error("Código do cliente é obrigatório.")
                st.stop()

            row = {
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "client_code": code,
                "NPS": nps,
            }

            for i, (_, perguntas) in enumerate(BLOCOS):
                respostas = st.session_state.get(f"respostas_{i}", {})
                for topico, _ in perguntas:
                    row[topico] = respostas.get(topico)

            row["coment_final"] = coment_final

            try:
                df_old = pd.read_csv("responses.csv")
                df = pd.concat([df_old, pd.DataFrame([row])], ignore_index=True)
            except:
                df = pd.DataFrame([row])

            df.to_csv("responses.csv", index=False)

            ok, msg = _append_to_excel([row.get(h) for h in HEADERS])

            st.session_state["step"] = 8
            st.rerun()

# -------- CONFIRMAÇÃO FINAL --------
elif step == 8:

    st.subheader("✅ Resposta enviada com sucesso")

    st.success(
        "Agradecemos por dedicar seu tempo para responder à nossa pesquisa. "
        "Suas respostas são muito importantes para que possamos aprimorar continuamente."
    )

    st.caption(
        f"Código do cliente: **{st.session_state['client_code']}** • "
        f"{datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )

    if st.button("➕ Enviar nova resposta"):
        for k in list(st.session_state.keys()):
            if k.startswith("respostas_") or k in ["nps", "coment_final"]:
                st.session_state.pop(k)

        st.session_state["client_code"] = ""
        st.session_state["step"] = 1
        st.rerun()

# -------- RODAPÉ FIXO --------
st.markdown(
    "<div class='footer-fixed'>© Jera Capital — Todos os direitos reservados.</div>",
    unsafe_allow_html=True,
)
