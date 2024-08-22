import re
import requests

def traduzir_legenda(arquivo_entrada, arquivo_saida, idioma_destino='pt'):
    # URL do LibreTranslate rodando localmente
    url = "http://localhost:5000/translate"

    # Abrir o arquivo de legenda
    with open(arquivo_entrada, 'r', encoding='utf-8') as entrada, open(arquivo_saida, 'w', encoding='utf-8') as saida:
        for linha in entrada:
            # Se a linha é uma linha de tempo ou índice, mantê-la como está
            if re.match(r'^\d+$', linha) or re.match(r'^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$', linha):
                saida.write(linha)
            else:
                # Fazer a tradução da linha usando a API do LibreTranslate
                payload = {
                    'q': linha.strip(),
                    'source': 'auto',  # Detecta automaticamente o idioma de origem
                    'target': idioma_destino
                }
                response = requests.post(url, data=payload)
                
                # Verificar se a resposta da API foi bem-sucedida
                if response.status_code == 200:
                    linha_traduzida = response.json()['translatedText']
                else:
                    # Em caso de falha na tradução, usar a linha original
                    linha_traduzida = linha.strip()

                # Escrever a linha traduzida no arquivo de saída
                saida.write(linha_traduzida + '\n')

    print(f"Tradução concluída e salva em {arquivo_saida}")

# Uso do script
arquivo_entrada = "ig.srt"
arquivo_saida = "legenda_traduzida.srt"
traduzir_legenda(arquivo_entrada, arquivo_saida)
