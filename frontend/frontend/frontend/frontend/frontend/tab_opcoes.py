import streamlit as st

def render_tab_opcoes():
    st.markdown("### 📊 Opções")
    st.info("⚠️ Módulo de opções em desenvolvimento. A fonte de dados atual (Yahoo Finance) não fornece dados detalhados de opções (Calls/Puts) em tempo real via API gratuita.")
    # Aqui entrará a lógica de opções quando você integrar uma API paga (ex: Tradier, Polygon)