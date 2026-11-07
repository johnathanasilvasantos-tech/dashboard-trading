import streamlit as st
from frontend.tab_acoes import render_tab_acoes
from frontend.tab_operacoes import render_tab_operacoes
from frontend.tab_opcoes import render_tab_opcoes
from config import COR_FUNDO, COR_PRIMARIA, COR_SIDEBAR

st.set_page_config(page_title="Deshbord", layout="wide")

st.markdown(f"""
    <style>
        .stApp {{ background-color: {COR_FUNDO}; color: white; }}
        [data-testid="stSidebar"] {{ background-color: {COR_SIDEBAR}; }}
        h1, h2, h3 {{ color: {COR_PRIMARIA}; }}
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("Deshbord")
    st.markdown("---")
    st.info("Plataforma de Análise Financeira")

tab1, tab2, tab3 = st.tabs(["📊 OPÇÕES", "📈 AÇÕES", "🌐 OPERAÇÕES"])

with tab1:
    render_tab_opcoes()
with tab2:
    render_tab_acoes()
with tab3:
    render_tab_operacoes()