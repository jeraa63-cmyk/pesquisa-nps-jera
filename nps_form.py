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

 /* ===================== CAIXA BRANCA (TODAS AS TELAS) ===================== */
 section.main, div.block-container {
   background: var(--jera-light) !important;
   border-radius: 22px !important;
   width: 96vw !important;
   height: 96vh !important;
   margin: 2vh auto !important;
   padding: 4rem 6rem !important;
   box-shadow: 0 6px 18px rgba(0,0,0,.08);
   display: flex !important;
   flex-direction: column !important;
   justify-content: flex-start !important;
   align-items: center !important;
 }

 @media (max-width: 1024px){
   section.main, div.block-container {
     width: 100vw !important;
     height: 100vh !important;
     border-radius: 0 !important;
     margin: 0 auto !important;
     padding: 2.5rem 1.5rem 3.5rem 1.5rem !important;
   }
 }

 /* ===================== TÍTULOS ===================== */
 h1, h2, h3 {
   font-family: 'Ofelia Display', sans-serif !important;
   color: var(--jera-dark);
   text-align: center !important;
 }
 h1 { font-size: 3.8rem !important; font-weight: 700 !important; }
 h2 { font-size: 2.4rem !important; font-weight: 600 !important; margin-bottom: 2.2rem !important; }
 h3 { font-size: 2.0rem !important; font-weight: 500 !important; }

 h1 { transform: translateX(18px); }
 @media (max-width: 1024px){
   h1 { transform: none !important; }
 }

 /* ===================== TEXTOS ===================== */
 p, div, span, label {
   font-size: 1.1rem !important;
   line-height: 1.6 !important;
 }

 /* ===================== INPUT DA TELA 1 ===================== */
 .stTextInput {
   display: flex !important;
   justify-content: center !important;
 }
 .stTextInput > div {
   width: fit-content !important;
   margin: 0 auto !important;
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

 /* ===================== ÁREA CENTRAL (TELAS 2–6) ===================== */

 .question-wrapper{
   max-width: 1000px;
   margin: 0 auto;
 }

 .question-block {
   margin-bottom: 3.0rem;
   text-align: center;
 }

 .question-topic {
   font-size: 1.25rem !important;
   font-weight: 700 !important;
   margin-bottom: 0.35rem !important;
   text-align: center !important;
 }

 .question-text {
   margin-top: 0.1rem;
   margin-bottom: 1.3rem;
   text-align: center !important;
 }

 /* ===================== RÉGUAS NPS ===================== */

 .scale-legend-11 {
   display: grid;
   grid-template-columns: repeat(11, 1fr);
   width: 100%;
   max-width: 600px;
   margin: 0.4rem auto 0 auto;
   text-align: center;
   font-size: 0.95rem;
 }

 /* remover borda padrão de forms */
 div[data-testid="stForm"] {
   border: none !important;
   background: transparent !important;
   padding: 0 !important;
 }

 /* ===================== RODAPÉ FIXO ===================== */
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

# ===================== BLOCOS DE PERGUNTAS =====================
BLOCOS = [
    (
        "Qualidade do Relacionamento com a Equipe Jera",
        [
            (
                "Tempo de resolução às solicitações",
                "De 01 a 05, quanto você está satisfeito(a) com a agilidade e disponibilidade da equipe ao atender suas solicitações?",
            ),
            (
                "Proatividade na comunicação",
                "De 01 a 05, quanto a equipe se antecipa às suas necessidades e se comunica de forma proativa?",
            ),
        ],
    ),
    (
        "Clareza e Relevância das Informações Prestadas",
        [
            (
                "Clareza das informações apresentadas",
                "De 01 a 05, o quanto as informações e o detalhamento dos relatórios atendem às suas expectativas?",
            ),
            (
                "Compreensão dos resultados",
                "De 01 a 05, o quanto os relatórios ajudam você a entender se a carteira está caminhando conforme seus objetivos?",
            ),
        ],
    ),
    (
        "Efetividade dos Encontros e Alinhamentos",
        [
            (
                "Frequência, formato e duração das reuniões",
                "De 01 a 05, como você avalia a adequação da frequência, do formato e da duração das reuniões?",
            ),
            (
                "Relevância e efetividade das reuniões",
                "De 01 a 05, o quanto as reuniões apresentam conteúdos relevantes, claros e bem organizados?",
            ),
        ],
    ),
    (
        "Percepção sobre o Desempenho da Carteira",
        [
            (
                "Satisfação com o retorno obtido",
                "De 01 a 05, o quanto você está satisfeito com o retorno da sua carteira nos últimos meses?",
            ),
            (
                "Alinhamento entre retorno e perfil de risco",
                "De 01 a 05, o quanto o retorno da carteira está compatível com seu perfil de risco e objetivos financeiros?",
            ),
        ],
    ),
    (
        "Compromisso com a Transparência e Integridade",
        [
            (
                "Independência nas recomendações",
                "De 01 a 05, o quanto você percebe independência e isenção nas recomendações feitas pela equipe?",
            ),
            (
                "Transparência sobre custos e remunerações",
                "De 01 a 05, o quanto você sente clareza nas informações sobre custos, taxas e formas de remuneração?",
            ),
        ],
    ),
]

HEADERS = (
    ["timestamp", "client_code", "NPS"]
    + [p[0] for _, perguntas in BLOCOS for p in perguntas]
    + ["coment_final"]
)

# ===================== FUNÇÕES AUXILIARES =====================
def _validar_secao(notas):
    if any(v is None for v in notas.values()):
        return False, "Por favor, selecione uma nota de 1 a 5 para todas as perguntas desta seção."
    return True, ""


def _append_to_excel(row_values):
    try:
        from openpyxl import Workbook, load_workbook

        os.makedirs(os.path.dirname(LOCAL_XLSX_PATH), exist_ok=True)

        if os.path.exists(LOCAL_XLSX_PATH):
            wb = load_workbook(LOCAL_XLSX_PATH)
        else:
            wb = Workbook()
            if wb.active and wb.active.title != "Respostas":
                wb.remove(wb.active)

        ws = wb["Respostas"] if "Respostas" in wb.sheetnames else wb.create_sheet(
            "Respostas"
        )

        for col, header in enumerate(HEADERS, 1):
            ws.cell(row=1, column=col, value=header)

        next_row = ws.max_row + 1
        for col, val in enumerate(row_values, 1):
            ws.cell(row=next_row, column=col, value=val)

        wb.save(LOCAL_XLSX_PATH)
        return True, "Gravado no Excel local."
    except Exception as e:
        return False, str(e)


def escala_circulos_1a5(pergunta_key: str):
    """
    Renderiza 5 círculos (números de 1 a 5) que preenchem quando selecionados
    e retorna a nota inteira correspondente.
    """

    # estado atual
    current = st.session_state.get(pergunta_key, None)

    # símbolos unicode: círculos ocos vs preenchidos
    unselected = ["①", "②", "③", "④", "⑤"]
    selected = ["❶", "❷", "❸", "❹", "❺"]
    valores = [1, 2, 3, 4, 5]
    descricoes = ["Péssimo", "Ruim", "Regular", "Bom", "Excelente"]

    # linha dos "botões" (círculos)
    cols_circulos = st.columns(5)
    for col, v, sym_uns, sym_sel in zip(cols_circulos, valores, unselected, selected):
        with col:
            label = sym_sel if current == v else sym_uns
            if st.button(label, key=f"{pergunta_key}_btn_{v}"):
                current = v
                st.session_state[pergunta_key] = v

    # linha das descrições (abaixo, alinhadas)
    cols_labels = st.columns(5)
    for col, v, desc in zip(cols_labels, valores, descricoes):
        with col:
            st.markdown(
                f"<div style='text-align:center;font-size:0.95rem;'>{v} - {desc}</div>",
                unsafe_allow_html=True,
            )

    return current

# ===================== FLUXO DAS TELAS =====================
step = st.session_state["step"]

# -------- TELA 1 --------
if step == 1:

    _, c2, _ = st.columns([1, 3, 1])

    with c2:
        if LOGO_FULL.exists():
            st.markdown(
                f"<img alt='Jera' src='{_img_data_uri(LOGO_FULL)}' "
                "style='display:block;margin:0 auto;width:480px;max-width:95%;'/>",
                unsafe_allow_html=True,
            )

        st.markdown(
            "<h1>PESQUISA DE SATISFAÇÃO</h1>",
            unsafe_allow_html=True,
        )

        st.markdown("<div style='height:4rem;'></div>", unsafe_allow_html=True)

        st.markdown(
            "<p style='font-size:1.3rem;font-weight:600;text-align:center;'>CÓDIGO DO CLIENTE</p>",
            unsafe_allow_html=True,
        )

        st.text_input("", key="client_code", placeholder="Ex.: 12345", max_chars=20)

        st.markdown("<div style='height:3rem;'></div>", unsafe_allow_html=True)

        st.markdown(
            """
        <div style='text-align:center; line-height:1.6; margin-bottom:2rem;'>
            <p style='font-size:1.15rem; margin-bottom:0.8rem;'>
                <strong>Esta é uma pesquisa identificada.</strong>
            </p>
            <p style='font-size:1.05rem;'>
                Suas respostas serão tratadas com confidencialidade e utilizadas exclusivamente
                para aperfeiçoarmos nossos serviços, sempre alinhados aos seus objetivos.
            </p>
        </div>""",
            unsafe_allow_html=True,
        )

        left_spacer, col_btn, right_spacer = st.columns([4, 2, 4])
        with col_btn:
            st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)
            if st.button("Iniciar pesquisa", key="start_button"):
                if not st.session_state["client_code"].strip():
                    st.error("Por favor, preencha o código do cliente.")
                else:
                    st.session_state["step"] = 2
                    st.rerun()

# -------- TELAS 2–6 (PERGUNTAS) --------
elif 2 <= step <= 6:

    idx = step - 2
    titulo, perguntas = BLOCOS[idx]

    st.markdown(
        f"<h2>{titulo}</h2>",
        unsafe_allow_html=True,
    )

    with st.form(f"form_{idx}"):

        st.markdown("<div class='question-wrapper'>", unsafe_allow_html=True)

        notas = {}

        for i, (topico, texto) in enumerate(perguntas):
            st.markdown("<div class='question-block'>", unsafe_allow_html=True)

            st.markdown(
                f"<p class='question-topic'>{topico}</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<p class='question-text'>{texto}</p>",
                unsafe_allow_html=True,
            )

            pergunta_id = f"{titulo}_{i}"

            # círculos ocos que preenchem (1 a 5)
            nota = escala_circulos_1a5(pergunta_id)
            notas[topico] = nota

            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([2, 7, 3])

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

# -------- PÁGINA NPS --------
elif step == 7:

    st.markdown("<h2>NPS</h2>", unsafe_allow_html=True)

    st.markdown(
        """
    <p style='font-size:1.3rem; line-height:1.45; margin-bottom:1.2rem; text-align:center;'>
    Considerando sua experiência com os serviços da <b>Jera Capital</b> ao longo do último ano — incluindo
    atendimento, relatórios, reuniões, transparência e a adequação das soluções ao seu perfil —,
    em uma escala de <b>0 a 10</b>, o quanto você recomendaria a Jera Capital a amigos ou familiares?
    </p>
    <p style='font-size:1.1rem; text-align:center;'>
        <em>(0 = Não recomendaria de forma alguma | 10 = Recomendaria com total confiança)</em>
    </p>
    """,
        unsafe_allow_html=True,
    )

    _, c_centro, _ = st.columns([1, 4, 1])
    with c_centro:
        nps = st.slider(
            "",
            min_value=0,
            max_value=10,
            step=1,
            key="nps",
        )

    st.markdown(
        """
        <div class="scale-legend-11">
            <div>0</div>
            <div>1</div>
            <div>2</div>
            <div>3</div>
            <div>4</div>
            <div>5</div>
            <div>6</div>
            <div>7</div>
            <div>8</div>
            <div>9</div>
            <div>10</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <p style='font-size:1.2rem; font-weight:700; margin-top:2rem; margin-bottom:0.3rem; text-align:center;'>
        Comentário final:
    </p>
    <p style='font-size:1.05rem; margin-top:0; margin-bottom:0.5rem; text-align:center;'>
        Se desejar, utilize este espaço para compartilhar sugestões, elogios ou qualquer ponto que não tenha sido abordado anteriormente.
    </p>
    """,
        unsafe_allow_html=True,
    )

    coment_final = st.text_area("", placeholder="", key="coment_final")

    col1, col2, col3 = st.columns([2, 7, 3])

    with col1:
        voltar = st.button("◀ Voltar")

    with col3:
        enviar = st.button("Enviar respostas ✅")

    if voltar:
        st.session_state["step"] -= 1
        st.rerun()

    if enviar:

        if nps is None:
            st.error("Por favor, selecione uma nota de 0 a 10.")
            st.stop()

        code = st.session_state["client_code"].strip()

        if not code:
            st.error("O campo CÓDIGO DO CLIENTE é obrigatório.")
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
        except FileNotFoundError:
            df = pd.DataFrame([row])

        df.to_csv("responses.csv", index=False)

        ok, msg = _append_to_excel([row.get(h) for h in HEADERS])

        if ok:
            st.success("Respostas gravadas com sucesso no Excel! ✔")
        else:
            st.warning("Não foi possível gravar no Excel. As respostas foram salvas em responses.csv.")

        st.session_state["step"] = 8
        st.rerun()

# -------- CONFIRMAÇÃO FINAL --------
elif step == 8:

    st.subheader("✅ Resposta enviada com sucesso")
    st.success(
        "Agradecemos por dedicar seu tempo para responder à nossa pesquisa. "
        "Suas respostas são muito importantes para que possamos aprimorar continuamente "
        "a qualidade dos nossos serviços e o relacionamento com você."
    )

    st.caption(
        f"Código do cliente: **{st.session_state['client_code']}** • "
        f"Enviado em {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )

    st.markdown(
        "<p style='font-size:1.0rem; color:#052B38; margin-top:1.5rem;'>"
        "Caso tenha qualquer dúvida ou queira conversar conosco, nossa equipe está sempre à disposição."
        "</p>",
        unsafe_allow_html=True,
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
    """
<div class='footer-fixed'>© Jera Capital — Todos os direitos reservados.</div>
""",
    unsafe_allow_html=True,
)
