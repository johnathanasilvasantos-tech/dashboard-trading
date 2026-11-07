import yfinance as yf
import pandas as pd
from datetime import datetime
from firebase_admin import firestore
from backend.firebase_config import get_db
from config import TICKERS_ACOES, COLECAO_SINAIS

def calcular_poc(df_1h):
    df_1h['Preco_Medio'] = (df_1h['High'] + df_1h['Low'] + df_1h['Close']) / 3
    vol_por_preco = df_1h.groupby(df_1h['Preco_Medio'].round(2))['Volume'].sum()
    return float(vol_por_preco.idxmax()) if not vol_por_preco.empty else 0.0

def processar_sinais():
    db = get_db()
    hoje = datetime.now().strftime('%Y-%m-%d')
    resultados = []

    for ticker in TICKERS_ACOES:
        try:
            df_1h = yf.download(ticker, period="60d", interval="1h", progress=False, multi_level_index=False)
            if df_1h.empty: continue
            
            max_1h = float(df_1h['High'].max())
            min_1h = float(df_1h['Low'].min())
            poc_1h = calcular_poc(df_1h)

            df_15m = yf.download(ticker, period="60d", interval="15m", progress=False, multi_level_index=False)
            if df_15m.empty: continue

            df_15m['EMA9'] = df_15m['Close'].ewm(span=9, adjust=False).mean()
            df_15m['EMA34'] = df_15m['Close'].ewm(span=34, adjust=False).mean()
            df_15m['EMA50'] = df_15m['Close'].ewm(span=50, adjust=False).mean()
            df_15m['EMA200'] = df_15m['Close'].ewm(span=200, adjust=False).mean()

            ultimo = df_15m.iloc[-1]
            preco = float(ultimo['Close'])
            ema9, ema34, ema50, ema200 = float(ultimo['EMA9']), float(ultimo['EMA34']), float(ultimo['EMA50']), float(ultimo['EMA200'])

            sinal, motivo = "NEUTRO", "Sem alinhamento claro"
            if preco > ema9 and ema9 > ema34 and ema34 > ema50 and ema50 > ema200 and preco > poc_1h:
                sinal, motivo = "UP", "Preço > EMAs e acima da POC"
            elif preco < ema9 and ema9 < ema34 and ema34 < ema50 and ema50 < ema200 and preco < poc_1h:
                sinal, motivo = "DOWN", "Preço < EMAs e abaixo da POC"

            doc_id = f"{ticker}_{hoje}"
            db.collection(COLECAO_SINAIS).document(doc_id).set({
                'symbol': ticker, 'signal': sinal, 'price': preco,
                'poc_1h': poc_1h, 'max_1h': max_1h, 'min_1h': min_1h,
                'ema9_15m': ema9, 'ema34_15m': ema34, 'ema50_15m': ema50, 'ema200_15m': ema200,
                'reason': motivo, 'updated_at': firestore.SERVER_TIMESTAMP
            })
            resultados.append(f"{ticker}: {sinal}")
        except Exception as e:
            print(f"Erro em {ticker}: {e}")
    return resultados