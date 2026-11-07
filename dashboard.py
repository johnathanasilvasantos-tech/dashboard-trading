import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
from datetime import datetime

# Configuração da página do Streamlit
st.set_page_config(page_title="Painel de Trading", layout="wide")

# Inicializa o Firebase usando os Secrets do Streamlit
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        try:
            # Tenta ler do Streamlit Secrets (Produção na Nuvem)
            cred_dict = dict(st.secrets["firebase"])
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            # Fallback: Tenta ler do arquivo local (Teste no seu PC)
            st.warning(f"Erro ao ler Secrets: {e}. Tentando ler arquivo local...")
            cred = credentials.Certificate("serviceAccountKey.json")
            firebase_admin.initialize_app(cred)
    return firestore.client()

db = init_firebase()

# Título do Painel
st.title("📊 Painel de Sinais - NASDAQ")
st.markdown("Análise Técnica Multi-Timeframe (EMAs + POC)")

# Botão para atualizar os dados na tela
if st.button("🔄 Atualizar Dados"):
    st.rerun()

# Busca os dados da coleção
hoje = datetime.now().strftime('%Y-%m-%d')
dados = []

docs = db.collection('nasdaq_signals').stream()
for doc in docs:
    d = doc.to_dict()
    # Filtra apenas os dados gerados hoje para não poluir a tela
    if hoje in doc.id:
        dados.append(d)

if not dados:
    st.warning("Nenhum dado encontrado no banco para hoje. Rode o 'analise_intraday.py' primeiro.")
else:
    # Converte para DataFrame
    df = pd.DataFrame(dados)
    
    # Função para colorir as linhas baseado no sinal
    def colorir_sinal(val):
        if val == "UP":
            return 'background-color: #1e4d2b; color: white; font-weight: bold;'
        elif val == "DOWN":
            return 'background-color: #5c1e1e; color: white; font-weight: bold;'
        return 'background-color: #333333; color: white;'

    # Seleciona as colunas para exibir
    colunas_exibir = ['symbol', 'signal', 'price', 'poc_1h', 'ema9_15m', 'ema200_15m', 'reason']
    
    # Garante que as colunas existem antes de filtrar
    colunas_existentes = [col for col in colunas_exibir if col in df.columns]
    df_formatado = df[colunas_existentes].copy()
    
    # Formata os números
    if 'price' in df_formatado.columns:
        df_formatado['price'] = df_formatado['price'].apply(lambda x: f"${x:.2f}")
    if 'poc_1h' in df_formatado.columns:
        df_formatado['poc_1h'] = df_formatado['poc_1h'].apply(lambda x: f"${x:.2f}")
    if 'ema9_15m' in df_formatado.columns:
        df_formatado['ema9_15m'] = df_formatado['ema9_15m'].apply(lambda x: f"${x:.2f}")
    if 'ema200_15m' in df_formatado.columns:
        df_formatado['ema200_15m'] = df_formatado['ema200_15m'].apply(lambda x: f"${x:.2f}")
    
    # Renomeia colunas para ficar bonito
    mapa_colunas = {
        'symbol': 'Ativo', 
        'signal': 'Sinal', 
        'price': 'Preço Atual', 
        'poc_1h': 'POC (1H)', 
        'ema9_15m': 'EMA 9 (15m)', 
        'ema200_15m': 'EMA 200 (15m)', 
        'reason': 'Motivo'
    }
    df_formatado = df_formatado.rename(columns=mapa_colunas)
    
    # Aplica as cores na coluna "Sinal"
    if 'Sinal' in df_formatado.columns:
        styled_df = df_formatado.style.map(colorir_sinal, subset=['Sinal'])
    else:
        styled_df = df_formatado
        
    # Mostra a tabela na tela
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    # Pequeno resumo
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Analisado", len(df))
    col2.metric("Sinais de Alta (UP)", len(df[df['signal'] == 'UP']) if 'signal' in df.columns else 0)
    col3.metric("Sinais de Baixa (DOWN)", len(df[df['signal'] == 'DOWN']) if 'signal' in df.columns else 0)