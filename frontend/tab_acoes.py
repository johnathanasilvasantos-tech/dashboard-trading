import streamlit as st
import pandas as pd
from backend.firebase_config import get_db
from components.cards import badge_sinal
from config import COLECAO_SINAIS

@st.cache_data(ttl=60)
def carregar_dados_firebase():
    db = get_db()
    docs = db.collection(COLECAO_SINAIS).stream()
    return pd.DataFrame([doc.to_dict() for doc in docs])

def render_tab_acoes():
    st.markdown("### 📈 Análise Técnica - Ações NASDAQ")
    df = carregar_dados_firebase()
    
    if df.empty:
        st.warning("Nenhum dado encontrado. Rode o backend/technical_analysis.py primeiro.")
        return

    filtro_sinal = st.selectbox("Filtrar por Tendência", ["Todos", "UP", "DOWN", "NEUTRO"])
    if filtro_sinal != "Todos":
        df = df[df['signal'] == filtro_sinal]

    df = df.sort_values('symbol')

    for _, row in df.iterrows():
        with st.container():
            c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1, 2])
            c1.markdown(f"**{row['symbol']}**")
            c2.markdown(f"${row['price']:.2f}")
            c3.markdown(badge_sinal(row['signal']), unsafe_allow_html=True)
            c4.markdown(f"POC: ${row['poc_1h']:.2f}")
            c5.caption(f"{row['reason']}")
            st.divider()