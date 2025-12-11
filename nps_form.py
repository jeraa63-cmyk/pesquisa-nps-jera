# nps_form.py
from pathlib import Path
import base64
import streamlit as st
import pandas as pd
from datetime import datetime

# ============= CHAVE INTERNA (deixe False para o cliente) =============
SHOW_INTERNAL_NPS = False
# ======================================================================

# ===================== CONFIG + CSS BASE =====================
st.set_page_config(page_title="PESQUISA DE SATISFAÇÃO", layout="wide")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root{
  --jera-primary:#00C1AD;
  --jera-dark:#052B38;
  --jera-bg:#026773;
  --card-max:1500px;

  --fs-body:   30px;
  --fs-h1:     50px;
  --fs-h2:     36px;
  --fs-h3:     26px;
  --fs-label:  18px;
  --fs-input:  18px;

  /* espaçamentos globais para “pular ~3 linhas” */
  --gap-title: 3.2rem;   /* após TÍTULO da seção (h2) */
  --gap-intro: 3.0rem;   /* após frase introdutória */
}

/* Esconde o cabeçalho do Streamlit */
header[data-testid="stHeader"]{ display:none !important; }

/* fundo e contêiner */
body, .stApp { background: var(--jera-bg) !important; }
[data-testid="stAppViewContainer"] > .main { padding-top: 1.5rem; }

.main .block-container, div.block-container{
  background:#EAF2F1 !important;
  border-radius:18px;
  box-shadow:0 8px 24px rgba(0,0,0,.08);
  border:1px solid rgba(0,0,0,.04);
  width:100% !important;
  max-width:var(--card-max) !important;
  margin:2rem auto !important;
  position: relative;
  padding:2rem 2rem calc(2.5rem + 80px) 2rem !important;
}

/* fonte base */
html, body, .stApp{
  font-family:"Inter", system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  color:var(--jera-dark);
  font-size: var(--fs-body);
}

/* === TÍTULO (logo abaixo do logo e ~2 dedos à direita) === */
.stApp .main .block-container h1,
.stApp h1{
  font-size: var(--fs-h1) !important;
  font-weight: 800 !important;
  line-height: 1.1;
  text-align:center !important;

  /* encosta no logo e desloca ~2 dedos p/ a direita */
  margin-top: -10px !important;
  transform: translateX(22px);
}

/* No mobile, não desloca para evitar corte lateral */
@media (max-width: 1024px){
  .stApp .main .block-container h1,
  .stApp h1{
    transform: none !important;
    margin-top: .2rem !important;
  }
}

h2{ font-size: var(--fs-h2); font-weight: 700; }

/* ====== ESPAÇAMENTO DESTAQUE (título e intro) ====== */
div[data-testid="stForm"] h2,
.block-container h2{
  display:block;
  margin-top: 0 !important;
  margin-bottom: var(--gap-title) !important;  /* ~3 linhas após o título */
}

.section-intro{
  margin-top: 0 !important;
  margin-bottom: var(--gap-intro) !important;  /* ~3 linhas após a intro */
  font-size: var(--fs-body);
  line-height: 1.45;
}

/* rótulos / textos auxiliares (inclui label do próprio text_input) */
.stTextInput > label,
.stTextArea  > label,
.stSelectbox > label,
.stCheckbox  > label,
div[role='radiogroup'] label{
  font-size: var(--fs-label);
}

.stTextInput > label{
  font-weight: 800 !important;
  font-size: 20px !important;
  text-transform: uppercase;
  letter-spacing:.02em;
  margin-bottom: .10rem !important; /* cola no input */
}

/* campos */
.stTextInput input, .stTextArea textarea{ font-size: var(--fs-input); }

/* frase sob o título principal (sem quebrar em telas largas) */
.guideline{
  display:block;
  text-align:center;
  font-size: clamp(18px, 2.1vw, 28px);
  font-weight: 600;
  white-space: nowrap;
  margin: .25rem auto 1.3rem;
}
@media (max-width: 1024px){
  .guideline{ white-space: normal; }
}

/* zera qualquer empurrão extra do container do TextInput */
.main .block-container div[data-testid="stTextInput"]{
  margin-top: 0 !important;
}

/* subtítulos (em negrito antes dos radios) */
.block-container p strong{
  font-weight: 800 !important;
  font-size: var(--fs-h3) !important;
  line-height: 1.3;
  display: inline-block;
  margin: .2rem 0 .35rem;
}

/* radios */
input[type="radio"]{ transform:scale(1.08); accent-color:var(--jera-primary); }
div[role='radiogroup'] label{
  margin-right: .55rem;
  padding: .15rem .35rem;
  border-radius: .4rem;
}

/* ==== BOTÕES padrão ==== */
.block-container div[data-testid="stForm"] button[type="submit"],
.block-container div[data-testid="stForm"] .stButton > button,
.block-container .stButton > button,
.block-container .stButton button,
.block-container button[data-testid^="baseButton"],
.block-container button[kind]{
  background:#00C1AD !important;
  color:#ffffff !important;
  border:0 !important;
  border-radius:12px !important;

  display:inline-flex !important;
  align-items:center !important;
  justify-content:center !important;

  font-weight:800 !important;
  font-size:20px !important;
  line-height:1.1 !important;

  width:auto !important;
  min-width:320px !important;
  max-width:100% !important;

  min-height:54px !important;
  white-space:nowrap !important;
  padding:.55rem 1.4rem !important;
  box-shadow:none !important;
}

.block-container div[data-testid="stForm"] button[type="submit"]:hover,
.block-container div[data-testid="stForm"] .stButton > button:hover,
.block-container .stButton > button:hover,
.block-container .stButton button:hover,
.block-container button[data-testid^="baseButton"]:hover,
.block-container button[kind]:hover{
  filter:brightness(.95) !important;
}

/* Alinhar o botão da 3ª coluna à DIREITA (canto do cartão) */
form[id^="form_"] div[data-testid="column"]:nth-of-type(3){ text-align:right; }

/* Tamanho mínimo maior para o botão da 3ª coluna (Avançar/Enviar) */
form[id^="form_"] div[data-testid="column"]:nth-of-type(3) .stButton > button{
  min-width:360px !important;
}

/* Específico da última página (form_nps): deixar ainda mais largo */
form#form_nps div[data-testid="column"]:nth-of-type(3) .stButton > button,
form[aria-label="form_nps"] div[data-testid="column"]:nth-of-type(3) .stButton > button{
  min-width:460px !important;
}

/* espaço caso apareçam dois botões colados em uma mesma coluna */
.block-container .stButton + .stButton{ margin-left:16px !important; }

/* nota do NPS */
.nps-note{
  font-weight: 800;
  margin: .6rem 0 1rem;
}

/* responsivo básico */
@media (max-width: 1024px){
  .main .block-container{ width:100vw; border-radius:0; margin:0 auto !important; }
}
</style>
""",
    unsafe_allow_html=True,
)

# ===================== LOGOS / PATHS ==================
BASE_DIR = Path(__file__).parent.resolve()
ASSETS = BASE_DIR / "assets"
LOGO_FULL = ASSETS / "jera-logo-full.png"
LOGO_FLAG = ASSETS / "jera-flag.png"

def _img_data_uri(p: Path) -> str:
  return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()

# BANDEIRINHA fixa dentro do cartão (ocultada na 1ª tela)
FLAG_IMG = LOGO_FLAG if LOGO_FLAG.exists() else (LOGO_FULL if LOGO_FULL.exists() else None)
if FLAG_IMG:
  FLAG_URI = _img_data_uri(FLAG_IMG)
  st.markdown(
      f"""
    <style>
      .main .block-container::after,
      div.block-container::after {{
        content: "";
        position: absolute;
        right: 20px; bottom: 20px;
        width: 64px; height: 64px;
        background-image: url("{FLAG_URI}");
        background-size: contain; background-repeat: no-repeat;
        opacity: .96; pointer-events: none; z-index: 20;
      }}
      @media (max-width: 768px){{
        .main .block-container::after, div.block-container::after{{ width:48px;height:48px; }}
      }}
    </style>
    """,
      unsafe_allow_html=True,
  )

# ===================== ESTADO INICIAL DO CÓDIGO DO CLIENTE ==================
if "client_code" not in st.session_state:
  st.session_state["client_code"] = ""
if "client_code_saved" not in st.session_state:
  st.session_state["client_code_saved"] = ""

# ===================== HEADER ==================
def render_header():
  step = st.session_state.get("step", 1)

  if step == 1:
    c1, c2, c3 = st.columns([1, 3, 1])
    with c2:
      p = LOGO_FULL if LOGO_FULL.exists() else (LOGO_FLAG if LOGO_FLAG.exists() else None)
      if p:
        st.markdown(
            f"<img alt='Jera' src='{_img_data_uri(p)}' "
            f"style='display:block;margin:0 auto -0.20rem;width:500px;max-width:92%;'/>",
            unsafe_allow_html=True,
        )
      st.title("PESQUISA DE SATISFAÇÃO")
      st.markdown(
          "<span class='guideline'>Avalie de <b>0 (muito ruim)</b> a "
          "<b>10 (excelente)</b>. Campos de observações são <b>opcionais</b>.</span>",
          unsafe_allow_html=True,
      )

    # Campo CÓDIGO DO CLIENTE — só na etapa 1
    st.text_input(
        "CÓDIGO DO CLIENTE",
        key="client_code",
        placeholder="Ex.: 12345",
        label_visibility="visible",
    )

    # Oculta a bandeirinha só na primeira tela
    st.markdown(
        """
      <style>
        .main .block-container::after, div.block-container::after{
          content: none !important; width:0 !important; height:0 !important; background-image:none !important;
        }
      </style>
      """,
        unsafe_allow_html=True,
    )
  # Demais etapas não mostram o input

# -------- PASSO 1: controle de etapa + header ----------
if "step" not in st.session_state:
  st.session_state["step"] = 1
render_header()

# ======================== FUNÇÕES UI ===================
def bloco(titulo, itens, key_prefix, intro=None, obs_label="Observações (opcional)"):
  st.subheader(titulo)

  if intro:
    st.markdown(f"<p class='section-intro'>{intro}</p>", unsafe_allow_html=True)

  # pré-carrega ao voltar
  saved = st.session_state.get(f"{key_prefix}_data")
  if saved:
    saved_notas = saved.get("notas", {})
    for i, p in enumerate(itens):
      store_key = p["topico"] if isinstance(p, dict) else p
      val = saved_notas.get(store_key)
      if val is not None and f"{key_prefix}_q{i}" not in st.session_state:
        st.session_state[f"{key_prefix}_q{i}"] = val
    if "obs" in saved and f"{key_prefix}_obs" not in st.session_state:
      st.session_state[f"{key_prefix}_obs"] = saved["obs"]

  notas = {}
  for i, p in enumerate(itens):
    if isinstance(p, dict):
      st.markdown(f"**{p['topico']}**")
      label_radio = p["pergunta"]
      store_key = p["topico"]
    else:
      label_radio = p
      store_key = p

    # >>> Sem seleção inicial (obrigatório escolher) <<<
    notas[store_key] = st.radio(
      label_radio,
      list(range(11)),
      horizontal=True,
      index=None,
      key=f"{key_prefix}_q{i}"
    )

  obs = st.text_area(obs_label, placeholder="Escreva livremente…", key=f"{key_prefix}_obs")
  return notas, obs

def _validar_secao(notas_dict, exigir_client_code=False):
  """Retorna (ok, msg_erro)."""
  faltantes = [k for k, v in notas_dict.items() if v is None]
  if faltantes:
    return False, "Por favor, selecione uma nota (0–10) para todos os tópicos desta seção."
  if exigir_client_code:
    code = str(st.session_state.get("client_code", "")).strip()
    if not code:
      return False, "O campo CÓDIGO DO CLIENTE é obrigatório."
  return True, ""

def mostrar_secao(titulo, intro, perguntas, key_prefix, obs_label, show_back=True, exigir_client_code=False):
  with st.form(f"form_{key_prefix}"):
    notas, obs = bloco(titulo, perguntas, key_prefix, intro=intro, obs_label=obs_label)

    col1, col2, col3 = st.columns([2, 7, 3])
    with col1:
      if show_back:
        voltar = st.form_submit_button("◀ Voltar")
      else:
        st.write("")
        voltar = False
    with col3:
      avancar = st.form_submit_button("Avançar ►")

    if voltar:
      st.session_state[f"{key_prefix}_data"] = {"notas": notas, "obs": obs}
      if st.session_state["step"] > 1:
        st.session_state["step"] -= 1
      st.rerun()

    if avancar:
      ok, msg = _validar_secao(notas, exigir_client_code=exigir_client_code)
      if not ok:
        st.error(msg)
      else:
        # Se é a primeira seção (onde exigimos o código), salva o código “definitivo”
        if exigir_client_code:
          st.session_state["client_code_saved"] = str(st.session_state.get("client_code", "")).strip()
        st.session_state[f"{key_prefix}_data"] = {"notas": notas, "obs": obs}
        st.session_state["step"] += 1
        st.rerun()

# ======================= SEÇÕES / TEMAS =======================
rel_intro = "Com base na sua experiência com o nosso atendimento ao longo do último ano, avalie:"
rel_perg = [
  {"topico": "Clareza na comunicação", "pergunta": "De 0 a 10, quanto a comunicação da equipe é clara, objetiva e fácil de entender?"},
  {"topico": "Tempo de resolução às solicitações", "pergunta": "De 0 a 10, quanto você está satisfeito(a) com o tempo de resolução da equipe às suas solicitações?"},
  {"topico": "Acessibilidade da equipe", "pergunta": "De 0 a 10, quanto a equipe está acessível quando você precisa entrar em contato?"},
  {"topico": "Proatividade na comunicação", "pergunta": "De 0 a 10, quanto a equipe se antecipa às suas necessidades e se comunica de forma proativa?"},
  {"topico": "Transparência nas informações", "pergunta": "De 0 a 10, quanto você considera que as informações fornecidas pela equipe são transparentes e confiáveis?"},
]

relat_intro = "Com base nos relatórios recebidos ao longo do último ano, avalie:"
relat_perg = [
  {"topico": "Clareza das informações apresentadas nos relatórios", "pergunta": "De 0 a 10, o quanto as informações sobre o desempenho da carteira são claras e fáceis de entender?"},
  {"topico": "Compreensão dos resultados em relação aos objetivos da carteira", "pergunta": "De 0 a 10, o quanto os relatórios ajudam você a entender se a carteira está caminhando conforme seus objetivos?"},
  {"topico": "Detalhamento das rentabilidades por ativo, classe ou estratégia", "pergunta": "De 0 a 10, o quanto o nível de detalhamento dos retornos (por ativo, classe ou estratégia) atende às suas expectativas?"},
  {"topico": "Comparação com benchmarks ou índices de referência", "pergunta": "De 0 a 10, o quanto os relatórios facilitam a comparação do desempenho da carteira com benchmarks relevantes?"},
  {"topico": "Utilidade do relatório para tomada de decisão", "pergunta": "De 0 a 10, o quanto o relatório mensal contribui para suas decisões patrimoniais e de investimento?"},
]

reun_intro = "Com base nas reuniões realizadas durante o último ano, avalie:"
reun_perg = [
  {"topico": "Frequência das reuniões", "pergunta": "De 0 a 10, o quanto a frequência das reuniões está adequada às suas necessidades e expectativas?"},
  {"topico": "Qualidade do conteúdo apresentado nas reuniões", "pergunta": "De 0 a 10, o quanto os temas tratados nas reuniões são relevantes, claros e bem-organizados?"},
  {"topico": "Efetividade das reuniões para tomada de decisões", "pergunta": "De 0 a 10, o quanto as reuniões contribuem para que você tome decisões mais informadas sobre seu patrimônio?"},
  {"topico": "Formato e duração das reuniões (presencial, online, tempo)", "pergunta": "De 0 a 10, o quanto você está satisfeito com o formato e a duração das reuniões?"},
  {"topico": "Preparação da equipe antes das reuniões", "pergunta": "De 0 a 10, o quanto você percebe que a equipe está bem-preparada e alinhada com suas demandas antes das reuniões?"},
]

desem_intro = "Com base na performance da sua carteira no último ano, avalie:"
desem_perg = [
  {"topico": "Satisfação com o retorno obtido", "pergunta": "De 0 a 10, o quanto você está satisfeito com o retorno da sua carteira nos últimos meses?"},
  {"topico": "Alinhamento entre retorno e perfil de risco", "pergunta": "De 0 a 10, o quanto o retorno da carteira está compatível com seu perfil de risco e objetivos financeiros?"},
  {"topico": "Comparação com expectativas pessoais", "pergunta": "De 0 a 10, o quanto o retorno da carteira atendeu às suas expectativas de rentabilidade?"},
  {"topico": "Comparação com o mercado (benchmarks)", "pergunta": "De 0 a 10, o quanto o desempenho da carteira é satisfatório em relação a índices ou benchmarks de referência?"},
  {"topico": "Constância e estabilidade dos retornos", "pergunta": "De 0 a 10, o quanto você está satisfeito com a consistência do retorno da carteira ao longo do tempo?"},
]

trans_intro = "Com base no relacionamento com a Jera Capital ao longo do último ano, avalie:"
trans_perg = [
  {"topico": "Independência nas recomendações", "pergunta": "De 0 a 10, o quanto você percebe independência e isenção nas recomendações feitas pela nossa equipe?"},
  {"topico": "Atuação ética e íntegra", "pergunta": "De 0 a 10, o quanto você confia que atuamos com ética e integridade em todas as interações?"},
  {"topico": "Comunicação de conflitos de interesse", "pergunta": "De 0 a 10, o quanto você acredita que eventuais conflitos de interesse são comunicados de forma clara e transparente?"},
  {"topico": "Transparência sobre custos e remunerações", "pergunta": "De 0 a 10, o quanto você sente clareza nas informações sobre custos, taxas e formas de remuneração dos nossos serviços?"},
  {"topico": "Alinhamento ético com seus valores", "pergunta": "De 0 a 10, o quanto você sente que nosso relacionamento reflete valores éticos alinhados aos seus e aos da sua família?"},
]

# ===================== ROTEADOR DE ETAPAS ======================
step = st.session_state.get("step", 1)

if step == 1:
  mostrar_secao(
      "Qualidade do Relacionamento com a Equipe Jera",
      rel_intro,
      rel_perg,
      key_prefix="rel",
      obs_label="Deseja comentar ou sugerir algo em relação ao atendimento prestado? (opcional)",
      show_back=False,
      exigir_client_code=True,  # salva client_code_saved ao avançar
  )

elif step == 2:
  mostrar_secao(
      "Clareza e Relevância das Informações Prestadas",
      relat_intro,
      relat_perg,
      key_prefix="relat",
      obs_label="Os relatórios são claros, úteis e bem estruturados? Tem alguma sugestão de melhoria? (opcional)"
  )

elif step == 3:
  mostrar_secao(
      "Efetividade dos Encontros e Alinhamentos",
      reun_intro,
      reun_perg,
      key_prefix="reun",
      obs_label="Referente ao tema Reuniões, alguma sugestão de mudança? (opcional)"
  )

elif step == 4:
  mostrar_secao(
      "Percepção sobre o Desempenho da Carteira",
      desem_intro,
      desem_perg,
      key_prefix="desem",
      obs_label="Há algo que gostaria de mudar na estratégia de investimentos ou nos objetivos da carteira? (opcional)"
  )

elif step == 5:
  mostrar_secao(
      "Compromisso com a Transparência e Integridade",
      trans_intro,
      trans_perg,
      key_prefix="trans",
      obs_label="Há algo que você gostaria que fosse mais claro ou transparente na nossa comunicação/atuação? (opcional)"
  )

elif step == 6:
  with st.form("form_nps"):
    st.subheader("Recomendação")
    st.write("Considerando sua experiência com os serviços da Jera Capital ao longo do último ano — incluindo atendimento, relatórios, reuniões, transparência e adequação das soluções ao seu perfil —")
    st.markdown("<p class='nps-note'>(0 = Não recomendaria de forma alguma | 10 = Recomendaria com total confiança)</p>", unsafe_allow_html=True)

    nps_score = st.radio(
      "Selecione sua nota de recomendação:",
      list(range(11)),
      horizontal=True,
      index=None,
      key="nps_score"
    )

    coment_final = st.text_area("Comentário final (opcional):", placeholder="Se desejar, compartilhe sugestões, elogios ou pontos não abordados.", key="coment_final")

    col1, col2, col3 = st.columns([2, 7, 3])
    with col1:
      voltar = st.form_submit_button("◀ Voltar")
    with col3:
      enviar = st.form_submit_button("Enviar respostas")

    if voltar:
      st.session_state["step"] -= 1
      st.rerun()

    if enviar:
      # usa sempre o valor salvo na etapa 1
      code = str(st.session_state.get("client_code_saved") or st.session_state.get("client_code", "")).strip()
      if not code:
        st.error("O campo CÓDIGO DO CLIENTE é obrigatório.")
        st.stop()
      if nps_score is None:
        st.error("Por favor, selecione sua nota de recomendação (0–10).")
        st.stop()

      rel   = st.session_state.get("rel_data",   {}).get("notas", {})
      relat = st.session_state.get("relat_data", {}).get("notas", {})
      reun  = st.session_state.get("reun_data",  {}).get("notas", {})
      desem = st.session_state.get("desem_data", {}).get("notas", {})
      trans = st.session_state.get("trans_data", {}).get("notas", {})

      rel_obs   = st.session_state.get("rel_data",   {}).get("obs", "")
      relat_obs = st.session_state.get("relat_data", {}).get("obs", "")
      reun_obs  = st.session_state.get("reun_data",  {}).get("obs", "")
      desem_obs = st.session_state.get("desem_data", {}).get("obs", "")
      trans_obs = st.session_state.get("trans_data", {}).get("obs", "")

      row = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "client_code": code,
        "NPS": nps_score,
        "obs_relacionamento": rel_obs,
        "obs_relatorios": relat_obs,
        "obs_reunioes": reun_obs,
        "obs_desempenho": desem_obs,
        "obs_transparencia": trans_obs,
        "coment_final": coment_final,
      }
      for k, v in rel.items():   row[f"Relacionamento — {k}"] = v
      for k, v in relat.items(): row[f"Relatórios — {k}"]     = v
      for k, v in reun.items():  row[f"Reuniões — {k}"]       = v
      for k, v in desem.items(): row[f"Desempenho — {k}"]     = v
      for k, v in trans.items(): row[f"Transparência — {k}"]  = v

      try:
        df_old = pd.read_csv("responses.csv")
        df = pd.concat([df_old, pd.DataFrame([row])], ignore_index=True)
      except FileNotFoundError:
        df = pd.DataFrame([row])
      df.to_csv("responses.csv", index=False)

      # Vai para a tela de confirmação
      st.session_state["submitted_ok"] = True
      st.session_state["step"] = 7
      st.rerun()

elif step == 7:
  st.subheader("Resposta enviada")
  st.success("Obrigada! Suas respostas foram registradas com sucesso.")

  code_show = st.session_state.get("client_code_saved") or st.session_state.get("client_code", "")
  ts = datetime.now().strftime("%d/%m/%Y %H:%M")
  st.caption(f"Código do cliente: **{code_show}** • Enviado em {ts}")

  col1, col2 = st.columns([1, 6])
  with col1:
    if st.button("➕ Enviar nova resposta"):
      # limpa estados para um novo preenchimento
      for k in list(st.session_state.keys()):
        if k.endswith("_data") or k in ["nps_score", "coment_final"]:
          st.session_state.pop(k, None)
      st.session_state["client_code"] = ""
      st.session_state["client_code_saved"] = ""
      st.session_state["submitted_ok"] = False
      st.session_state["step"] = 1
      st.rerun()

# mostra NPS acumulado SOMENTE quando a chave interna estiver True
if SHOW_INTERNAL_NPS:
  try:
    df = pd.read_csv("responses.csv")
    if len(df.index) > 0 and "NPS" in df.columns:
      prom = (df["NPS"] >= 9).mean()
      det  = (df["NPS"] <= 6).mean()
      nps  = 100 * (prom - det)
      st.metric("NPS (último acumulado)", f"{nps:.0f}")
      st.caption(f"Promotores: {prom:.0%} • Detratores: {det:.0%} • Respostas: {len(df)}")
  except Exception:
    pass

# rodapé
st.caption("Este formulário é para uso interno da Jera Capital.")
