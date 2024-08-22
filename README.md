# Tradução de Legendas com LibreTranslate

Este projeto oferece um script Python que utiliza a API do [LibreTranslate](https://libretranslate.com/) para traduzir arquivos de legendas (`.srt`) de forma automática, mantendo os tempos originais.

## Pré-requisitos

1. **Docker**: O LibreTranslate é executado em um contêiner Docker.
2. **Python 3.6+**: Necessário para executar o script de tradução.
3. **Bibliotecas Python**: 
   - `requests` para fazer requisições HTTP para a API do LibreTranslate.
4. **mkvextract**: Ferramenta para extrair legendas de arquivos `.mkv`.

## Instalação

### 1. Configuração do LibreTranslate

Para configurar o LibreTranslate, execute o seguinte comando para iniciar o contêiner Docker:

```bash
docker run -d -p 5000:5000 libretranslate/libretranslate
```
Isso irá baixar e iniciar o contêiner do LibreTranslate que estará acessível em http://localhost:5000.

### 2. Instalação das Dependências Python

Instale as dependências necessárias utilizando pip:

```bash
pip install requests
```

### 3. Instalação do mkvtoolnix

Para extrair legendas de arquivos .mkv, você precisará do mkvtoolnix. Se você estiver usando o BigLinux, instale-o com:

```bash
pamac install mkvtoolnix
```

Se estiver usando outra distribuição, utilize o gerenciador de pacotes apropriado. Por exemplo, no Arch Linux:

```bash
sudo pacman -S mkvtoolnix
```

### Extração de Legendas de Arquivos MKV

Para extrair legendas de um arquivo .mkv, siga os passos abaixo:

1. Identifique o número da faixa de legenda:

Primeiro, use o comando mkvinfo para listar todas as faixas no arquivo .mkv:

```bash
mkvinfo arquivo.mkv
```

Encontre a faixa de legenda que você deseja extrair.

2. Extraia a faixa de legenda:

Utilize o comando mkvextract para extrair a faixa de legenda identificada:
```bash
mkvextract tracks arquivo.mkv 1:legenda.srt
```

Substitua 1 pelo número da faixa de legenda e legenda.srt pelo nome desejado para o arquivo de legenda extraído.

## Uso
### 1. Script de Tradução
O script traduz_legenda.py pode ser usado para traduzir arquivos .srt de qualquer idioma para o português brasileiro. Certifique-se de que o contêiner do LibreTranslate esteja em execução antes de rodar o script.

### 2. Exemplo de Uso
Coloque o arquivo .srt que deseja traduzir no mesmo diretório que o script.

Execute o script de tradução:

```bash
python traduz_legenda.py
```

O arquivo traduzido será salvo no mesmo diretório com o nome legenda_traduzida.srt.

### 3. Personalização
Se você quiser traduzir para outro idioma, basta alterar o parâmetro idioma_destino no script:

```bash
idioma_destino = 'es'  # Para traduzir para espanhol, por exemplo.
```

## Exemplo de Script

Aqui está um exemplo de como o script funciona:

```python
import re
import requests
import time

def traduzir_legenda(arquivo_entrada, arquivo_saida, idioma_destino='pt'):
    url = "http://localhost:5000/translate"
    max_retries = 5
    retry_delay = 5  # segundos

    with open(arquivo_entrada, 'r', encoding='utf-8') as entrada, open(arquivo_saida, 'w', encoding='utf-8') as saida:
        for linha in entrada:
            if re.match(r'^\d+$', linha) or re.match(r'^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$', linha):
                saida.write(linha)
            else:
                for attempt in range(max_retries):
                    try:
                        payload = {
                            'q': linha.strip(),
                            'source': 'auto',
                            'target': idioma_destino
                        }
                        response = requests.post(url, data=payload)
                        response.raise_for_status()
                        linha_traduzida = response.json()['translatedText']
                        break
                    except requests.exceptions.RequestException as e:
                        print(f"Erro na tradução: {e}")
                        if attempt < max_retries - 1:
                            print(f"Tentando novamente em {retry_delay} segundos...")
                            time.sleep(retry_delay)
                        else:
                            print("Falha na tradução após várias tentativas. Usando a linha original.")
                            linha_traduzida = linha.strip()
                saida.write(linha_traduzida + '\n')

    print(f"Tradução concluída e salva em {arquivo_saida}")

# Uso do script
arquivo_entrada = "legenda_original.srt"
arquivo_saida = "legenda_traduzida.srt"
traduzir_legenda(arquivo_entrada, arquivo_saida)

```

Licença
Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.

```
Esse `README.md` agora inclui instruções completas para instalação, extração de legendas, uso do script de tradução e personalização. Certifique-se de ajustar qualquer parte conforme necessário para se adequar ao seu projeto específico.
```
