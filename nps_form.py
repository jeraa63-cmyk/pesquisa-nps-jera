from pathlib import Path
import base64
import os
from datetime import datetime

import pandas as pd
import streamlit as st

# ===================== CONFIGURAÇÃO: Excel local =====================
# caminho para uso LOCAL (no seu computador). Em produção (Streamlit Cloud)
# é normal que essa gravação falhe, e o app cai no CSV.
LOCAL_XLSX_PATH = r"C:\\Users\\AnaSilvaJeraCapital\\OneDrive - JERA CAPITAL GESTAO DE RECURSOS LTDA\\Comercial - Documentos\\NPS\\Pesquisa_NPS.xlsx"

# Mostrar (ou não) um NPS interno no final – pode deixar False para os clientes
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

  --card-max: 1500px;

  /* tamanhos responsivos suaves */
  --fs-body: clamp(15px, 1.0vw, 18px);
  --fs-h1:   clamp(32px, 2.6vw, 44px);
  --fs-h2:   clamp(24px, 2.0vw, 32px);
  --fs-h3:   clamp(18px, 1.6vw, 22px);
  --fs-small: clamp(13px, 0.9vw, 15px);
}

/* ===================== RESET / BACKGROUND ===================== */
header[data-testid="stHeader"], footer {display:none !important;}

html, body, .stApp {
  background: var(--jera-bg) !important;
  font-family: 'Ofelia Text', system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
  color: var(--jera-dark);
  margin: 0 !important;
  padding: 0 !important;
}

/* container principal (cartão branco) */
.main .block-container, div.block-container {
  background: var(--jera-light) !important;
  border-radius: 24px !important;
  width: 96vw !important;
  max-width: var(--card-max) !important;
  margin: 2vh auto 2.5vh auto !important;
  padding: 3rem 4rem 4.5rem 4rem !important;
  box-shadow: 0 10px 30px rgba(0,0,0,.08);
  border: 1px solid rgba(0,0,0,.03);
  position: relative;
}

/* telas menores: o cartão ocupa 100% da largura */
@media (max-width: 1024px){
  .main .block-container, div.block-container {
    width: 100vw !important;
    max-width: 100vw !important;
    border-radius: 0 !important;
    margin: 0 auto !important;
    padding: 2.2rem 1.4rem 3.6rem 1.4rem !important;
  }
}

/* ===================== TÍTULOS ===================== */
h1, h2, h3 {
  font-family: 'Ofelia Display', sans-serif !important;
  color: var(--jera-dark);
  text-align: center !important;
}

h1 {
  font-size: var(--fs-h1) !important;
  font-weight: 700 !important;
  line-height: 1.1;
  margin-bottom: 1.6rem !important;
}

h2 {
  font-size: var(--fs-h2) !important;
  font-weight: 600 !important;
  margin-bottom: 2.2rem !important;
}

h3 {
  font-size: var(--fs-h3) !important;
  font-weight: 500 !important;
  margin-bottom: 1.4rem !important;
}

/* ===================== TEXTOS ===================== */
p, div, span, label {
  font-size: var(--fs-body) !important;
  line-height: 1.6 !important;
}

/* parágrafo introdutório de cada seção */
.section-intro {
  max-width: 80ch;
  margin: 0 auto 2.4rem auto;
  text-align: center;
}

/* bloco de pergunta (título + frase) */
.question-block {
  max-width: 90ch;
  margin: 0 auto 2rem auto;
  text-align: center;
}

.question-title {
  font-size: var(--fs-h3) !important;
  font-weight: 600 !important;
  margin-bottom: 0.35rem !important;
}

.question-text {
  font-size: var(--fs-body) !important;
}

/* espaço vertical entre perguntas */
.spacer-questions {
  height: 2.4rem;
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
  font-size: 1.05rem !important;
  text-align: center !important;
  padding: 0.6rem 0.8rem !important;
  border-radius: 10px !important;
  background-color: #f6f6f6 !important;
  width: 260px !important;
}

/* ===================== RADIOS ===================== */
div[role='radiogroup'] {
  display: flex !important;
  flex-wrap: nowrap !important;
  justify-content: center !important;
  align-items: center !important;
  gap: 0.9rem !important;
}

div[role='radiogroup'] label {
  font-size: clamp(14px, 0.9vw, 16px) !important;
  white-space: nowrap !important;
}

/* em telas bem pequenas deixe quebrar em 2 linhas se precisar */
@media (max-width: 768px){
  div[role='radiogroup'] {
    flex-wrap: wrap !important;
  }
}

/* ===================== BOTÕES ===================== */
.stButton > button, button[kind] {
  font-family: 'Ofelia Display', sans-serif !important;
  background: #052B38 !important;
  color: white !important;
  border: 2px solid #052B38 !important;
  border-radius: 14px !important;
  font-weight: 600 !important;
  font-size: 1rem !important;
  min-width: 210px !important;
  min-height: 46px !important;
  padding: 0.45rem 1.4rem !important;
  transition: all 0.2s ease-in-out;
  box-shadow: 0 4px 12px rgba(0,0,0,.15);
}
.stButton > button:hover, button[kind]:hover {
  background: #00C1AD !important;
  border-color: #00C1AD !important;
  transform: translateY(-1px);
}

/* remover bordas padrão dos formulários */
div[data-testid="stForm"] {
  border: none !important;
  background: transparent !important;
  padding: 0 !important;
}

/* ===================== RODAPÉ FIXO ===================== */
.footer-fixed {
  position: fixed !important;
  bottom: 0.7rem !important;
  left: 1.2rem !important;
  font-size: var(--fs-small) !important;
  color: #9fb3bc !important;
  font-family: 'Ofelia Text', sans-serif !important;
  z-index: 9999 !important;
  pointer-events: none;
}

/* ===================== CAMPOS DE TEXTO FINAIS ===================== */
textarea {
  font-size: var(--fs-body) !important;
}

/* centralizar os botões de navegação nas colunas */
form div[data-testid="column"]:nth-of-type(1) {
  text-align: left;
}
form div[data-testid="column"]:nth-of-type(3) {
  text-align: right;
}
</style>
""",
    unsafe_allow_html=True,
)

# ===================== LOGO / PATHS =====================
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
        return False, "Por favor, selecione uma opção (1–5) para todas as perguntas desta seção."
    return True, ""


def _append_to_excel(row_values):
    """
    Tenta acrescentar a resposta em um Excel local.
    Em ambiente de nuvem é normal falhar – o erro é retornado como mensagem.
    """
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


# ===================== FLUXO DAS TELAS =====================
step = st.session_state["step"]

# -------- TELA 1 --------
if step == 1:
    # LOGO CENTRALIZADO
    if LOGO_FULL.exists():
        st.markdown(
            f"<img alt='Jera' src='{_img_data_uri(LOGO_FULL)}' "
            "style='display:block;margin:0 auto 1.4rem;width:min(420px,80%);'/>",
            unsafe_allow_html=True,
        )

    st.markdown("<h1>PESQUISA DE SATISFAÇÃO</h1>", unsafe_allow_html=True)

    st.markdown(
        """
        <p style='text-align:center;max-width:70ch;margin:0 auto 2.4rem;'>
          Por favor, informe seu <strong>CÓDIGO DO CLIENTE</strong> para
          seguirmos com a pesquisa.
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.text_input("", key="client_code", placeholder="Ex.: 12345", max_chars=20)

    st.markdown("<div style='height:2.6rem;'></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div style='text-align:center; line-height:1.6; max-width:72ch; margin:0 auto 2.6rem;'>
            <p>
                <strong>Esta é uma pesquisa identificada.</strong>
            </p>
            <p>
                Suas respostas serão tratadas com confidencialidade e utilizadas exclusivamente
                para aperfeiçoarmos nossos serviços, sempre alinhados aos seus objetivos.
            </p>
        </div>""",
        unsafe_allow_html=True,
    )

    _, col_btn, _ = st.columns([3, 2, 3])
    with col_btn:
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

    st.markdown(f"<h2>{titulo}</h2>", unsafe_allow_html=True)

    with st.form(f"form_{idx}"):
        notas = {}

        for i, (topico, texto) in enumerate(perguntas):
            st.markdown(
                f"""
                <div class='question-block'>
                  <div class='question-title'>{topico}</div>
                  <div class='question-text'>{texto}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            notas[topico] = st.radio(
                "",
                [
                    "1 - Péssimo",
                    "2 - Ruim",
                    "3 - Regular",
                    "4 - Bom",
                    "5 - Excelente",
                ],
                horizontal=True,
                index=None,
                key=f"{titulo}_{i}",
            )

            if i < len(perguntas) - 1:
                st.markdown("<div class='spacer-questions'></div>", unsafe_allow_html=True)

        st.markdown("<div style='height:1.6rem;'></div>", unsafe_allow_html=True)

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
        <p style='max-width:90ch;margin:0 auto 1.4rem;text-align:center;'>
        Considerando sua experiência com os serviços da <b>Jera Capital</b> ao longo do último ano — incluindo
        atendimento, relatórios, reuniões, transparência e a adequação das soluções ao seu perfil —,
        em uma escala de <b>0 a 10</b>, o quanto você recomendaria a Jera Capital a amigos ou familiares?
        </p>
        <p style='font-size:0.95rem;text-align:center;margin-top:0.4rem;margin-bottom:1.8rem;'>
            <em>(0 = Não recomendaria de forma alguma | 10 = Recomendaria com total confiança)</em>
        </p>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns([1, 3, 1])
    with c2:
        nps = st.radio("", list(range(11)), horizontal=True, index=None, key="nps")

    st.markdown(
        """
        <p style='font-size:1.05rem;font-weight:700;margin-top:2.4rem;margin-bottom:0.5rem;text-align:center;'>
            Comentário final:
        </p>
        <p style='font-size:0.98rem;margin-top:0;margin-bottom:0.6rem;text-align:center;'>
            Se desejar, utilize este espaço para compartilhar sugestões, elogios ou qualquer ponto que não tenha sido abordado anteriormente.
        </p>
        """,
        unsafe_allow_html=True,
    )

    coment_final = st.text_area("", placeholder="", key="coment_final")

    st.markdown("<div style='height:1.8rem;'></div>", unsafe_allow_html=True)

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

        # CSV
        try:
            df_old = pd.read_csv("responses.csv")
            df = pd.concat([df_old, pd.DataFrame([row])], ignore_index=True)
        except FileNotFoundError:
            df = pd.DataFrame([row])
        df.to_csv("responses.csv", index=False)

        # Excel local
        ok, msg = _append_to_excel([row.get(h) for h in HEADERS])

        if ok:
            st.success("Respostas gravadas com sucesso no Excel! ✔")
        else:
            st.warning(
                "Não foi possível gravar no Excel local. "
                "As respostas foram salvas em responses.csv."
            )

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
        "<p style='font-size:0.98rem;color:#052B38;margin-top:1.4rem;'>"
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

# ===================== NPS INTERNO OPCIONAL =====================
if SHOW_INTERNAL_NPS:
    try:
        df_int = pd.read_csv("responses.csv")
        if len(df_int.index) > 0 and "NPS" in df_int.columns:
            prom = (df_int["NPS"] >= 9).mean()
            det = (df_int["NPS"] <= 6).mean()
            nps_val = 100 * (prom - det)
            st.metric("NPS (último acumulado)", f"{nps_val:.0f}")
            st.caption(
                f"Promotores: {prom:.0%} • Detratores: {det:.0%} • Respostas: {len(df_int)}"
            )
    except Exception:
        pass
