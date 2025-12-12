import os
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

import streamlit as st

# Excel
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter


# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Pesquisa de Satisfação | Jera Capital",
    layout="wide",
)

APP_TITLE = "PESQUISA DE SATISFAÇÃO"
FOOTER_TEXT = "© Jera Capital — Todos os direitos reservados."
EXCEL_PATH = "respostas_pesquisa.xlsx"  # salva no mesmo diretório onde você rodar o app

# Paleta base (ajuste se quiser)
COLOR_BG = "#04313B"        # fundo azul/verde escuro
COLOR_PRIMARY = "#0AAE9A"   # verde água (slider)
COLOR_TEXT = "#0B2B33"      # texto escuro


# =========================
# CSS (card branco + responsivo + slider + alinhamentos)
# =========================
st.markdown(
    f"""
<style>
/* Fundo geral */
.stApp {{
  background: {COLOR_BG};
}}

/* Card branco central */
.jera-card {{
  max-width: 1100px;
  margin: 40px auto;
  background: #ffffff;
  border-radius: 26px;
  padding: 48px 64px;
  box-sizing: border-box;
}}

/* Responsivo (notebook / telas menores) */
@media (max-width: 1100px) {{
  .jera-card {{
    margin: 20px 16px;
    padding: 28px 20px;
  }}
}}

/* Títulos */
.h-logo {{
  display:flex;
  justify-content:center;
  align-items:center;
  margin-top: 0px;
  margin-bottom: 20px;
}}

.h1 {{
  text-align:center;
  font-size: 44px;
  letter-spacing: 0.5px;
  margin: 18px 0 24px 0;
  color: {COLOR_TEXT};
  font-weight: 800;
}}

.h2 {{
  text-align:center;
  font-size: 22px;
  margin: 6px 0 6px 0;
  color: {COLOR_TEXT};
  font-weight: 800;
}}

.p {{
  text-align:center;
  color: {COLOR_TEXT};
  font-size: 16px;
  line-height: 1.45;
  margin: 10px 0;
}}

.small {{
  text-align:center;
  color: {COLOR_TEXT};
  font-size: 14px;
  opacity: 0.9;
  margin-top: 8px;
}}

.section {{
  margin-top: 34px;
}}

.hr {{
  height: 1px;
  background: rgba(11,43,51,0.10);
  border: none;
  margin: 26px 0;
}}

/* Linha labels alinhadas (5 colunas / 11 colunas) */
.scale-row {{
  display: grid;
  gap: 0px;
  width: 100%;
  margin: 10px auto 0 auto;
  align-items: start;
}}

.scale-5 {{
  grid-template-columns: repeat(5, 1fr);
}}

.scale-11 {{
  grid-template-columns: repeat(11, 1fr);
}}

.scale-cell {{
  text-align: center;
  color: {COLOR_TEXT};
}}

.scale-num {{
  font-size: 14px;
  opacity: 0.75;
  margin-bottom: 6px;
}}

.scale-label {{
  font-size: 14px;
  font-weight: 600;
}}

/* Slider com cor do tema */
div[data-baseweb="slider"] > div > div > div {{
  background: {COLOR_PRIMARY} !important;
}}
div[data-baseweb="slider"] div[role="slider"] {{
  border-color: {COLOR_PRIMARY} !important;
}}
div[data-baseweb="slider"] div[role="slider"] {{
  box-shadow: 0 0 0 0.2rem rgba(10,174,154,0.20) !important;
}}

/* Botões */
.jera-btn-row {{
  display:flex;
  justify-content:space-between;
  align-items:center;
  margin-top: 28px;
}}

.footer {{
  position: fixed;
  left: 20px;
  bottom: 12px;
  color: rgba(255,255,255,0.55);
  font-size: 12px;
}}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(f"<div class='footer'>{FOOTER_TEXT}</div>", unsafe_allow_html=True)


# =========================
# Helpers
# =========================
def ensure_state():
    if "page" not in st.session_state:
        st.session_state.page = 0
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "client_code" not in st.session_state:
        st.session_state.client_code = ""
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())


def go_next():
    st.session_state.page += 1


def go_prev():
    st.session_state.page = max(0, st.session_state.page - 1)


def set_touched(key: str):
    st.session_state[f"{key}__touched"] = True


def is_touched(key: str) -> bool:
    return bool(st.session_state.get(f"{key}__touched", False))


def save_answer(key: str, value: Any):
    st.session_state.answers[key] = value


def get_answer(key: str) -> Optional[Any]:
    return st.session_state.answers.get(key)


def append_to_excel(filepath: str, row: Dict[str, Any]):
    headers = list(row.keys())

    if not os.path.exists(filepath):
        wb = Workbook()
        ws = wb.active
        ws.title = "Respostas"
        ws.append(headers)
        wb.save(filepath)

    wb = load_workbook(filepath)
    ws = wb["Respostas"]

    # Se o header mudou/está vazio, ajusta (simples e seguro)
    existing_headers = [c.value for c in ws[1]]
    if existing_headers != headers:
        # cria uma nova aba para não bagunçar histórico
        new_title = f"Respostas_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        ws = wb.create_sheet(new_title)
        ws.append(headers)

    ws.append([row.get(h, "") for h in headers])

    # Ajuste de largura
    for i, h in enumerate(headers, start=1):
        col = get_column_letter(i)
        ws.column_dimensions[col].width = max(14, min(50, len(str(h)) + 2))

    wb.save(filepath)


def scale_slider_1a5(
    q_key: str,
    question_title: str,
    question_text: str,
):
    """
    Slider 1-5 sem "resposta automática":
    - Inicializa em 3 visualmente
    - Mas só considera respondido quando o usuário mexer (touched)
    """
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.markdown(f"<div class='h2'>{question_title}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='p'>{question_text}</div>", unsafe_allow_html=True)

    # valor exibido
    default_val = 3
    current_val = int(get_answer(q_key) or default_val)

    val = st.slider(
        label="",
        min_value=1,
        max_value=5,
        value=current_val,
        key=f"slider__{q_key}",
        on_change=set_touched,
        args=(q_key,),
    )

    # salva sempre o número atual (mas valida por touched)
    save_answer(q_key, int(val))

    # números + labels alinhados
    labels = ["Péssimo", "Ruim", "Regular", "Bom", "Excelente"]
    st.markdown("<div class='scale-row scale-5'>", unsafe_allow_html=True)
    for i, lab in enumerate(labels, start=1):
        st.markdown(
            f"""
            <div class='scale-cell'>
              <div class='scale-num'>{i}</div>
              <div class='scale-label'>{i} - {lab}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def scale_slider_0a10(
    q_key: str,
    question_text: str,
):
    default_val = 5
    current_val = int(get_answer(q_key) if get_answer(q_key) is not None else default_val)

    st.markdown(f"<div class='p'>{question_text}</div>", unsafe_allow_html=True)

    val = st.slider(
        label="",
        min_value=0,
        max_value=10,
        value=current_val,
        key=f"slider__{q_key}",
        on_change=set_touched,
        args=(q_key,),
    )
    save_answer(q_key, int(val))

    # Linha com 0..10 alinhados
    st.markdown("<div class='scale-row scale-11'>", unsafe_allow_html=True)
    for i in range(11):
        st.markdown(
            f"""
            <div class='scale-cell'>
              <div class='scale-num'>{i}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)


# =========================
# Perguntas (edite aqui)
# =========================
PAGES: List[Dict[str, Any]] = [
    {
        "type": "start",
    },
    {
        "title": "Efetividade dos Encontros e Alinhamentos",
        "questions": [
            {
                "key": "freq_formato_duracao",
                "title": "Frequência, formato e duração das reuniões",
                "text": "De 01 a 05, como você avalia a adequação da frequência, do formato e da duração das reuniões?",
            },
            {
                "key": "relevancia_efetividade",
                "title": "Relevância e efetividade das reuniões",
                "text": "De 01 a 05, o quanto as reuniões apresentam conteúdos relevantes, claros e bem organizados?",
            },
        ],
    },
    {
        "title": "Qualidade do Relacionamento com a Equipe Jera",
        "questions": [
            {
                "key": "tempo_resolucao",
                "title": "Tempo de resolução às solicitações",
                "text": "De 01 a 05, quanto você está satisfeito(a) com a agilidade e disponibilidade da equipe ao atender suas solicitações?",
            },
            {
                "key": "proatividade",
                "title": "Proatividade na comunicação",
                "text": "De 01 a 05, quanto a equipe se antecipa às suas necessidades e se comunica de forma proativa?",
            },
        ],
    },
    {
        "title": "Compromisso com a Transparência e Integridade",
        "questions": [
            {
                "key": "independencia",
                "title": "Independência nas recomendações",
                "text": "De 01 a 05, o quanto você percebe independência e isenção nas recomendações feitas pela equipe?",
            },
            {
                "key": "transparencia_custos",
                "title": "Transparência sobre custos e remunerações",
                "text": "De 01 a 05, o quanto você sente clareza nas informações sobre custos, taxas e formas de remuneração?",
            },
        ],
    },
    {
        "type": "nps",
    },
]


# =========================
# UI
# =========================
ensure_state()

st.markdown("<div class='jera-card'>", unsafe_allow_html=True)

page_obj = PAGES[st.session_state.page]

# ---------- START PAGE ----------
if page_obj.get("type") == "start":
    # logo (se você quiser, depois eu te digo como colocar imagem do logo aqui)
    st.markdown("<div class='h-logo'>", unsafe_allow_html=True)
    st.markdown(
        "<div style='font-size:44px; font-weight:900; color:#0B2B33; letter-spacing:1px;'>JERA<span style='font-weight:300;'>CAPITAL</span></div>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='h1'>{APP_TITLE}</div>", unsafe_allow_html=True)

    st.markdown("<div class='h2'>CÓDIGO DO CLIENTE</div>", unsafe_allow_html=True)

    client_code = st.text_input(
        label="",
        placeholder="Ex.: 12345",
        value=st.session_state.client_code,
    ).strip()

    st.session_state.client_code = client_code

    st.markdown("<div class='small'><b>Esta é uma pesquisa identificada.</b></div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='p'>Suas respostas serão tratadas com confidencialidade e utilizadas exclusivamente para aperfeiçoarmos nossos serviços, sempre alinhados aos seus objetivos.</div>",
        unsafe_allow_html=True,
    )

    start_clicked = st.button("Iniciar pesquisa", use_container_width=False)

    if start_clicked:
        if not client_code:
            st.error("Por favor, informe o código do cliente para iniciar.")
        else:
            go_next()
            st.rerun()

# ---------- QUESTION PAGES ----------
elif page_obj.get("type") is None:
    st.markdown(f"<div class='h1' style='font-size:36px'>{page_obj['title']}</div>", unsafe_allow_html=True)

    # render perguntas
    for q in page_obj["questions"]:
        scale_slider_1a5(q["key"], q["title"], q["text"])
        st.markdown("<hr class='hr'/>", unsafe_allow_html=True)

    # validação: só avança se o usuário mexeu em todos os sliders da página
    keys = [q["key"] for q in page_obj["questions"]]
    all_touched = all(is_touched(k) for k in keys)

    col_left, col_mid, col_right = st.columns([1, 6, 1])
    with col_left:
        if st.button("◀ Voltar"):
            go_prev()
            st.rerun()
    with col_right:
        if st.button("Avançar ▶"):
            if not all_touched:
                st.error("Responda todas as perguntas (mexa no controle) antes de avançar.")
            else:
                go_next()
                st.rerun()

# ---------- NPS FINAL ----------
elif page_obj.get("type") == "nps":
    st.markdown("<div class='h1' style='font-size:36px'>NPS</div>", unsafe_allow_html=True)

    st.markdown(
        "<div class='p'>Considerando sua experiência com os serviços da <b>Jera Capital</b> ao longo do último ano — incluindo atendimento, relatórios, reuniões, transparência e a adequação das soluções ao seu perfil —, em uma escala de <b>0 a 10</b>, o quanto você recomendaria a Jera Capital a amigos ou familiares?</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='small'><i>(0 = Não recomendaria de forma alguma | 10 = Recomendaria com total confiança)</i></div>", unsafe_allow_html=True)

    scale_slider_0a10("nps", "")

    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.markdown("<div class='h2'>Comentário final:</div>", unsafe_allow_html=True)
    st.markdown("<div class='p'>Se desejar, utilize este espaço para compartilhar sugestões, elogios ou qualquer ponto que não tenha sido abordado anteriormente.</div>", unsafe_allow_html=True)

    comment = st.text_area("", value=str(get_answer("comentario") or ""), height=120)
    save_answer("comentario", comment)
    st.markdown("</div>", unsafe_allow_html=True)

    # validação do NPS: só considera respondido se mexer no slider
    nps_ok = is_touched("nps")

    col_left, col_right = st.columns([1, 1])
    with col_left:
        if st.button("◀ Voltar"):
            go_prev()
            st.rerun()

    with col_right:
        if st.button("Enviar respostas ✅"):
            if not nps_ok:
                st.error("Por favor, selecione uma nota de 0 a 10 (mexa no controle) para enviar.")
            else:
                payload = {
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                    "session_id": st.session_state.session_id,
                    "codigo_cliente": st.session_state.client_code,
                    **st.session_state.answers,
                }
                append_to_excel(EXCEL_PATH, payload)
                st.success("Respostas enviadas com sucesso! Obrigado(a).")
                st.info(f"Arquivo salvo: {os.path.abspath(EXCEL_PATH)}")

                # opcional: limpa para novo respondente
                st.session_state.page = 0
                st.session_state.answers = {}
                st.session_state.session_id = str(uuid.uuid4())
                # não apaga o código automaticamente; se quiser, descomente:
                # st.session_state.client_code = ""
                st.rerun()


st.markdown("</div>", unsafe_allow_html=True)
