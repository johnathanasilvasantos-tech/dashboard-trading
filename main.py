import datetime

import firebase_admin
import yfinance as yf
from firebase_admin import credentials, firestore

# Inicializa o Firebase com a chave de conta de serviço
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

TICKERS = ["AAPL", "MSFT", "TSLA"]


def get_yahoo_finance_quotes(tickers):
    """Obtém cotações reais do Yahoo Finance via yfinance."""
    quotes = {}
    data = yf.download(tickers, period="1d", progress=False)

    for symbol in tickers:
        try:
            price = float(data["Close"][symbol].iloc[-1])
            quotes[symbol] = price
        except (KeyError, IndexError):
            print(f"Não foi possível obter o preço de {symbol}")

    return quotes


def save_quotes():
    today = datetime.date.today().isoformat()  # ex: 2026-11-07
    quotes = get_yahoo_finance_quotes(TICKERS)

    for symbol, price in quotes.items():
        doc_id = f"{symbol}_{today}"
        doc_ref = db.collection("yahoo_finance_quotes").document(doc_id)
        doc_ref.set({
            "symbol": symbol,
            "price": float(price),
            "updated_at": firestore.SERVER_TIMESTAMP,
        })
        print(f"Documento salvo: {doc_id} -> price={price}")


if __name__ == "__main__":
    save_quotes()