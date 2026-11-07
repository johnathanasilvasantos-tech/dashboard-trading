import streamlit as st
from config import COR_ALTA, COR_BAIXA, COR_NEUTRO

def card_kpi(titulo, valor, variacao=None, cor_valor="#FFFFFF"):
    st.markdown(f"""
    <div style="background-color: #151A28; padding: 15px; border-radius: 10px; border-left: 5px solid {cor_valor}; margin-bottom: 10px;">
        <p style="margin: 0; color: #9E9E9E; font-size: 14px;">{titulo}</p>
        <h3 style="margin: 0; color: {cor_valor}; font-size: 24px;">{valor}</h3>
        <p style="margin: 0; color: #9E9E9E; font-size: 12px;">{variacao if variacao else ''}</p>
    </div>
    """, unsafe_allow_html=True)

def badge_sinal(sinal):
    if sinal == "UP":
        return f'<span style="background-color: {COR_ALTA}; color: white; padding: 4px 10px; border-radius: 5px; font-weight: bold;">UP</span>'
    elif sinal == "DOWN":
        return f'<span style="background-color: {COR_BAIXA}; color: white; padding: 4px 10px; border-radius: 5px; font-weight: bold;">DOWN</span>'
    return f'<span style="background-color: {COR_NEUTRO}; color: white; padding: 4px 10px; border-radius: 5px; font-weight: bold;">NEUTRO</span>'