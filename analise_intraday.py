import firebase_admin
from firebase_admin import credentials, firestore
import yfinance as yf
import pandas as pd
from datetime import datetime

# Inicializa o Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def extrair_numero(valor):
    """Função auxiliar para garantir que o valor seja um float puro"""
    if isinstance(valor, pd.Series):
        return float(valor.iloc[0])
    return float(valor)

def calcular_poc_1h(df_1h):
    df_1h['Preco_Medio'] = (df_1h['High'] + df_1h['Low'] + df_1h['Close']) / 3
    volume_por_preco = df_1h.groupby(df_1h['Preco_Medio'].round(2))['Volume'].sum()
    if volume_por_preco.empty:
        return extrair_numero(df_1h['Close'].iloc[-1])
    poc = volume_por_preco.idxmax()
    return float(poc)

def analisar_mercado_intraday():
    tickers = ["NVDA", "AAPL", "MSFT", "AMZN", "GOOGL", "META", "AVGO", "MU", "TSLA", "AMD"]
    print("Iniciando Análise Multi-Timeframe (1H e 15M)...\n")
    
    for ticker in tickers:
        print(f"Analisando {ticker}...")
        try:
            # 1. Dados de 1H (Adicionado multi_level_index=False para evitar erro de Series)
            df_1h = yf.download(ticker, period="60d", interval="1h", progress=False, multi_level_index=False)
            if df_1h.empty:
                print(f"  -> Erro: Sem dados de 1H para {ticker}")
                continue
                
            # Extraindo Máxima, Mínima e POC de forma segura
            max_1h = extrair_numero(df_1h['High'].max())
            min_1h = extrair_numero(df_1h['Low'].min())
            poc_1h = calcular_poc_1h(df_1h)
            
            # 2. Dados de 15M
            df_15m = yf.download(ticker, period="60d", interval="15m", progress=False, multi_level_index=False)
            if df_15m.empty:
                print(f"  -> Erro: Sem dados de 15M para {ticker}")
                continue
                
            # 3. Cálculo EMAs
            df_15m['EMA_9'] = df_15m['Close'].ewm(span=9, adjust=False).mean()
            df_15m['EMA_34'] = df_15m['Close'].ewm(span=34, adjust=False).mean()
            df_15m['EMA_50'] = df_15m['Close'].ewm(span=50, adjust=False).mean()
            df_15m['EMA_200'] = df_15m['Close'].ewm(span=200, adjust=False).mean()
            
            # Pegando o último registro de forma segura
            ultimo = df_15m.iloc[-1]
            preco_atual = extrair_numero(ultimo['Close'])
            ema9 = extrair_numero(ultimo['EMA_9'])
            ema34 = extrair_numero(ultimo['EMA_34'])
            ema50 = extrair_numero(ultimo['EMA_50'])
            ema200 = extrair_numero(ultimo['EMA_200'])
            
            # 4. Regra de Sinal
            sinal = "NEUTRO"
            motivo = []
            
            condicao_alta_ema = (preco_atual > ema9) and (ema9 > ema34) and (ema34 > ema50) and (ema50 > ema200)
            condicao_alta_poc = preco_atual > poc_1h
            
            condicao_baixa_ema = (preco_atual < ema9) and (ema9 < ema34) and (ema34 < ema50) and (ema50 < ema200)
            condicao_baixa_poc = preco_atual < poc_1h
            
            if condicao_alta_ema and condicao_alta_poc:
                sinal = "UP"
                motivo.append("Alinhamento de Alta (15M) e Preço acima da POC (1H)")
            elif condicao_baixa_ema and condicao_baixa_poc:
                sinal = "DOWN"
                motivo.append("Alinhamento de Baixa (15M) e Preço abaixo da POC (1H)")
            else:
                motivo.append("Sem alinhamento claro de EMAs ou POC")
                
            # 5. Salvar no Firebase
            data_atual = datetime.now().strftime('%Y-%m-%d')
            doc_id = f"{ticker}_{data_atual}"
            
            db.collection('nasdaq_signals').document(doc_id).set({
                'symbol': ticker,
                'signal': sinal,
                'price': preco_atual,
                'poc_1h': poc_1h,
                'max_1h': max_1h,
                'min_1h': min_1h,
                'ema9_15m': ema9,
                'ema34_15m': ema34,
                'ema50_15m': ema50,
                'ema200_15m': ema200,
                'reason': " | ".join(motivo),
                'updated_at': firestore.SERVER_TIMESTAMP
            })
            
            print(f"  -> {ticker}: SINAL {sinal} | Preço: ${preco_atual:.2f} | POC: ${poc_1h:.2f}")
            
        except Exception as e:
            print(f"  -> Erro ao processar {ticker}: {e}")

if __name__ == "__main__":
    analisar_mercado_intraday()