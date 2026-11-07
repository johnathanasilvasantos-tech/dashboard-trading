import json

try:
    # Abre o seu arquivo original
    with open('serviceAccountKey.json', 'r') as file:
        dados = json.load(file)
        
    print("\n" + "="*50)
    print("COPIE O TEXTO ABAIXO E COLE NO STREAMLIT SECRETS:")
    print("="*50 + "\n")
    
    print("[firebase]")
    for chave, valor in dados.items():
        if chave == "private_key":
            # A chave privada precisa de aspas triplas por causa das quebras de linha
            print(f'{chave} = """{valor}"""')
        else:
            # As outras chaves precisam de aspas duplas normais
            print(f'{chave} = "{valor}"')
            
    print("\n" + "="*50)
    
except FileNotFoundError:
    print("Erro: O arquivo 'serviceAccountKey.json' não foi encontrado nesta pasta.")