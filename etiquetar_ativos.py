import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def adicionar_etiquetas():
    # Define o tipo de cada ativo
    tipos = {
        "QQQ": "ETF",
        "SPY": "ETF",
        "^IXIC": "INDEX",
        "NVDA": "STOCK", "AAPL": "STOCK", "MSFT": "STOCK", "AMZN": "STOCK",
        "GOOGL": "STOCK", "META": "STOCK", "AVGO": "STOCK", "MU": "STOCK",
        "TSLA": "STOCK", "AMD": "STOCK"
    }

    print("Adicionando etiquetas (asset_type) aos documentos...")
    
    # Busca todos os documentos da coleção
    docs = db.collection('yahoo_finance_quotes').stream()
    
    contador = 0
    for doc in docs:
        dados = doc.to_dict()
        symbol = dados.get('symbol')
        
        if symbol in tipos:
            # Atualiza apenas o campo asset_type
            db.collection('yahoo_finance_quotes').document(doc.id).update({
                'asset_type': tipos[symbol]
            })
            contador += 1
            
    print(f"Concluído! {contador} documentos atualizados com sucesso.")

if __name__ == "__main__":
    adicionar_etiquetas()