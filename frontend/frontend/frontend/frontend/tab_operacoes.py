import streamlit as st
from backend.market_data import get_dados_indices
from components.cards import card_kpi
from components.charts import grafico_linha
from config import COR_ALTA, COR_BAIXA

def render_tab_operacoes():
    st.markdown("### 🌐 Operações - Índices e ETFs")
    dados = get_dados_indices()
    
    if not dados:
        st.warning("Não foi possível carregar os dados de mercado.")
        return

    cols = st.columns(3)
    for i, (nome, info) in enumerate(dados.items()):
        with cols[i]:
            cor = COR_ALTA if info['variacao'] >= 0 else COR_BAIXA
            card_kpi(nome, f"${info['preco']:.2f}", f"{info['pct']:.2f}%", cor)
            st.plotly_chart(grafico_linha(info['historico'], f"{nome} - 5 Dias"), use_container_width=True)