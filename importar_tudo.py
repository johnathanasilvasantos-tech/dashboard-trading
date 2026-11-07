import firebase_admin
from firebase_admin import credentials, firestore
import yfinance as yf
from datetime import datetime, timedelta

# Inicializa o Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def importar_dados_mercado():
    # Lista completa: ETFs, Índice e Principais Ações
    tickers = [
        "QQQ", "SPY", "^IXIC",  # ETFs e Índice NASDAQ
        "NVDA", "AAPL", "MSFT", "AMZN", "GOOGL", 
        "META", "AVGO", "MU", "TSLA", "AMD" # Principais Ações
    ]
    
    # Define o período (últimos 60 dias para permitir cálculos de médias móveis)
    data_fim = datetime.today()
    data_inicio = data_fim - timedelta(days=60)
    
    print(f"Iniciando importação de {data_inicio.date()} até {data_fim.date()}...")
    
    for ticker in tickers:
        print(f"Processando {ticker}...")
        
        try:
            # Baixa os dados do Yahoo Finance
            dados = yf.download(ticker, start=data_inicio.strftime('%Y-%m-%d'), end=data_fim.strftime('%Y-%m-%d'), progress=False)
            
            if dados.empty:
                print(f"  -> Nenhum dado encontrado para {ticker}.")
                continue
                
            # Itera sobre cada dia do histórico
            for index, row in dados.iterrows():
                data_str = index.strftime('%Y-%m-%d')
                
                # Tratamento para pegar o valor float corretamente (evita erros de Series do Pandas)
                close_val = row['Close']
                if isinstance(close_val, (list, tuple)):
                    preco_fechamento = float(close_val[0])
                elif hasattr(close_val, 'iloc'): # Se for uma Series do Pandas
                    preco_fechamento = float(close_val.iloc[0])
                else:
                    preco_fechamento = float(close_val)
                
                # Limpa o nome do ticker para o ID (remove o ^ do índice)
                ticker_limpo = ticker.replace("^", "")
                doc_id = f"{ticker_limpo}_{data_str}"
                
                # Grava no Firestore
                db.collection('yahoo_finance_quotes').document(doc_id).set({
                    'symbol': ticker,
                    'price': preco_fechamento,
                    'updated_at': firestore.SERVER_TIMESTAMP
                })
                
            print(f"  -> {ticker} importado com sucesso.")
            
        except Exception as e:
            print(f"  -> Erro ao processar {ticker}: {e}")

if __name__ == "__main__":
    importar_dados_mercado()
    print("\nImportação finalizada!")