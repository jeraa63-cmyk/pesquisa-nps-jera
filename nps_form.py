import streamlit as st

# =============================
# CONFIGURAÇÃO DA PÁGINA
# =============================
st.set_page_config(
    page_title="Pesquisa de Satisfação | Jera Capital",
    layout="centered"
)

# =============================
# CSS GLOBAL
# =============================
st.markdown("""
<style>
/* Fundo geral */
body {
    background-color: #002F3A;
}

/* Caixa branca central */
div.block-container {
    background: #ffffff;
    border-radius: 24px;
    padding: 1.6rem 4rem 3rem 4rem !important;
    max-width: 1100px;
    margin: 1.2rem auto 2.5rem auto;
}

/* Responsividade notebook */
@media (max-width: 1200px){
  div.block-container {
    padding: 1.4rem 2.4rem 2.8rem 2.4rem !important;
  }
}

/* Responsividade celular */
@media (max-width: 768px){
  div.block-container {
    padding: 1.2rem 1.4rem 2.6rem 1.4rem !important;
  }
}

/* Títulos */
h1, h2, h3 {
    text-align: center;
    color: #002F3A;
}

/* Texto */
p {
    text-align: center;
    color: #002F3A;
}

/* Slider centralizado */
div[data-baseweb="slider"] {
    max-width: 640px;
    margin: 0 auto;
}

/* Labels do slider */
.slider-labels {
    display: flex;
    justify-content: space-between;
    max-width: 640px;
    margin: 0.2rem auto 2rem auto;
    font-size: 0.9rem;
    color: #002F3A;
}

/* Rodapé */
.footer {
    text-align: center;
    font-size: 0.8rem;
    color: #6b6b6b;
    margin-top: 3rem;
}
</style>
""", unsafe_allow_html=True)

# =============================
# LOGO (SUBIDO)
# =============================
st.markdown(
    "<img src='https://i.imgur.com/8uQJ4xF.png' "
    "style='display:block;margin:-10px auto 10px auto;width:240px;'>",
    unsafe_allow_html=True
)

# =============================
# TÍTULO PRINCIPAL
# =============================
st.markdown("<h1>PESQUISA DE SATISFAÇÃO</h1>", unsafe_allow_html=True)
st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

# =============================
# CÓDIGO DO CLIENTE
# =============================
st.markdown("<h3>CÓDIGO DO CLIENTE</h3>", unsafe_allow_html=True)
codigo = st.text_input("", placeholder="Ex: 12345", label_visibility="collapsed")

st.markdown("""
<p><strong>Esta é uma pesquisa identificada.</strong><br>
Suas respostas serão tratadas com confidencialidade e utilizadas exclusivamente para
aperfeiçoarmos nossos serviços.</p>
""", unsafe_allow_html=True)

st.markdown("<div style='height:1.6rem'></div>", unsafe_allow_html=True)

if st.button("Iniciar pesquisa"):
    st.session_state["pagina"] = 1

# =============================
# FUNÇÃO DE PERGUNTA OBRIGATÓRIA
# =============================
def pergunta_slider(titulo, texto, key):
    st.markdown(f"<h3>{titulo}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p>{texto}</p>", unsafe_allow_html=True)

    valor = st.slider(
        "",
        min_value=1,
        max_value=5,
        value=None,
        step=1,
        key=key
    )

    st.markdown("""
    <div class="slider-labels">
        <span>1 - Péssimo</span>
        <span>2 - Ruim</span>
        <span>3 - Regular</span>
        <span>4 - Bom</span>
        <span>5 - Excelente</span>
    </div>
    """, unsafe_allow_html=True)

    return valor

# =============================
# PÁGINA 1
# =============================
if st.session_state.get("pagina") == 1:

    r1 = pergunta_slider(
        "Tempo de resolução das solicitações",
        "De 01 a 05, quão satisfeito(a) você está com a agilidade da equipe?",
        "p1"
    )

    r2 = pergunta_slider(
        "Proatividade na comunicação",
        "De 01 a 05, a equipe se comunica de forma proativa?",
        "p2"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("◀ Voltar"):
            st.session_state["pagina"] = 0

    with col2:
        if st.button("Avançar ▶"):
            if r1 is None or r2 is None:
                st.warning("⚠️ Por favor, responda todas as perguntas para continuar.")
            else:
                st.session_state["pagina"] = 2

# =============================
# PÁGINA FINAL — NPS
# =============================
if st.session_state.get("pagina") == 2:

    st.markdown("<h2>NPS</h2>", unsafe_allow_html=True)

    st.markdown("""
    <p>Em uma escala de <strong>0 a 10</strong>, o quanto você recomendaria a Jera Capital
    a amigos ou familiares?</p>
    """, unsafe_allow_html=True)

    nps = st.slider(
        "",
        min_value=0,
        max_value=10,
        value=None,
        step=1,
        key="nps"
    )

    comentario = st.text_area("Comentário final (opcional)")

    if st.button("Enviar respostas"):
        if nps is None:
            st.warning("⚠️ Por favor, selecione uma nota para o NPS.")
        else:
            st.success("✅ Respostas enviadas com sucesso!")

# =============================
# RODAPÉ
# =============================
st.markdown("""
<div class="footer">
© Jera Capital — Todos os direitos reservados.
</div>
""", unsafe_allow_html=True)
