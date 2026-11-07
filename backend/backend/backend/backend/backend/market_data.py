import yfinance as yf
import pandas as pd
from config import TICKERS_INDICES

def get_dados_indices():
    dados = {}
    for nome, ticker in TICKERS_INDICES.items():
        df = yf.download(ticker, period="5d", interval="1d", progress=False, multi_level_index=False)
        if not df.empty:
            dados[nome] = {
                "preco": float(df['Close'].iloc[-1]),
                "variacao": float(df['Close'].iloc[-1] - df['Close'].iloc[-2]),
                "pct": float(((df['Close'].iloc[-1] - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100),
                "max": float(df['High'].iloc[-1]),
                "min": float(df['Low'].iloc[-1]),
                "historico": df
            }
    return dados