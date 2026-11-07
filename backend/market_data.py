import yfinance as yf
import pandas as pd
from config import TICKERS_INDICES

def get_dados_indices():
    dados = {}
    for nome, ticker in TICKERS_INDICES.items():
        try:
            # Baixa os últimos 5 dias para ter o fechamento de ontem e de hoje
            df = yf.download(ticker, period="5d", interval="1d", progress=False, multi_level_index=False)
            
            if not df.empty and len(df) >= 2:
                preco_atual = float(df['Close'].iloc[-1])
                preco_anterior = float(df['Close'].iloc[-2])
                variacao = preco_atual - preco_anterior
                pct = (variacao / preco_anterior) * 100
                
                dados[nome] = {
                    "preco": preco_atual,
                    "variacao": variacao,
                    "pct": pct,
                    "max": float(df['High'].iloc[-1]),
                    "min": float(df['Low'].iloc[-1]),
                    "historico": df
                }
        except Exception as e:
            print(f"Erro ao buscar {nome}: {e}")
            
    return dados