# Análise de Sentimento - PUC Minas

Aplicação para análise de sentimento em textos, desenvolvida para o curso de Processamento de Linguagem Natural da PUC Minas.

## Funcionalidades

- **Análise de Sentimento**: Classifica textos como positivos, neutros ou negativos.
- **Processamento de Texto**: Pré-processamento com limpeza e lematização.
- **Análise de Tópicos**: Identifica tópicos principais usando LDA.
- **Visualizações**: Gráficos, nuvem de palavras e estatísticas.
- **Suporte a Arquivos**: Analisa dados de CSV ou Excel.
- **Interface Amigável**: Interface intuitiva construída com Streamlit.
- **Autenticação de Usuários**: Sistema simples de login para proteger a aplicação.

## Estrutura do Projeto

```
.
├── main.py                 # Ponto de entrada principal da aplicação
├── requirements.txt        # Dependências do projeto
├── README.md               # Documentação do projeto
├── data/                   # Diretório para armazenar dados
├── scripts/                # Scripts utilitários
│   ├── setup.py            # Script de configuração inicial
│   ├── download_example_data.py  # Script para download de dados de exemplo
│   ├── download_nltk_resources.py # Script para download de recursos NLTK
│   ├── verify_nltk.py      # Script para verificar instalação do NLTK
│   ├── verify_spacy.py     # Script para verificar instalação do spaCy
│   ├── gerar_hash_senha.py # Script para gerar hash de senhas para autenticação
│   └── cleanup.py          # Script para limpeza
└── src/                    # Código-fonte da aplicação
    ├── data/               # Módulos para manipulação de dados
    │   ├── __init__.py
    │   └── data_handler.py
    ├── models/             # Implementações de modelos
    │   ├── __init__.py
    │   ├── sentiment_analysis.py
    │   └── topic_analysis.py
    ├── utils/              # Utilitários e ferramentas
    │   ├── __init__.py
    │   ├── text_processing.py
    │   └── visualization.py
    ├── web/                # Interface web com Streamlit
    │   ├── __init__.py
    │   ├── app.py          # Aplicação principal
    │   └── auth.py         # Módulo de autenticação
    └── __init__.py
```

## Requisitos

- Python 3.11 ou superior

## Instalação

1. Clone este repositório:
```bash
git clone https://github.com/seu-usuario/analise-sentimento-pucminas.git
cd analise-sentimento-pucminas
```

2. Crie um ambiente virtual com venv:
```bash
python3 -m venv venv
```

3. Ative o ambiente virtual:
```bash
# No macOS/Linux (método 1 - source):
source venv/bin/activate

# No macOS/Linux (método 2 - usando . - recomendado para macOS):
. venv/bin/activate

# No Windows:
venv\Scripts\activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

5. Baixe os modelos necessários do spaCy:
```bash
python -m spacy download en_core_web_sm
python -m spacy download pt_core_news_sm  # Se necessário para português
```

6. Baixe os recursos do NLTK usando o script auxiliar:
```bash
python scripts/download_nltk_resources.py
```

## Verificação da Instalação

Após a instalação, você pode verificar se tudo está configurado corretamente usando os scripts de verificação:

1. Verificar recursos do NLTK:
```bash
python scripts/verify_nltk.py
```

2. Verificar modelo do spaCy:
```bash
python scripts/verify_spacy.py
```

Estes scripts ajudarão a identificar e resolver problemas com as dependências.

## Uso

1. Ative o ambiente virtual (se ainda não estiver ativo):
```bash
# No macOS/Linux (método 1 - source):
source venv/bin/activate

# No macOS/Linux (método 2 - usando . - recomendado para macOS):
. venv/bin/activate

# No Windows:
venv\Scripts\activate
```

2. Execute a aplicação:
```bash
streamlit run main.py
```

A aplicação ficará disponível no navegador em `http://localhost:8501`.

### Sistema de Autenticação

A aplicação inclui um sistema simples de autenticação. Os usuários padrão são:

- **admin** / **admin**
- **usuario** / **1234**
- **convidado** / **guest**

Para adicionar novos usuários:

1. Gere o hash da senha usando o script auxiliar:
```bash
python scripts/gerar_hash_senha.py
```
ou
```bash
python scripts/gerar_hash_senha.py "sua_senha"
```

2. Adicione o novo usuário ao dicionário `USUARIOS` no arquivo `src/web/auth.py`.

### Download de Dados de Exemplo

Para gerar dados de exemplo para teste:

```bash
python scripts/download_example_data.py
```

### Modos de Análise

#### 1. Análise de Arquivo CSV/Excel
- Faça upload de um arquivo CSV ou Excel.
- Selecione a coluna que contém os textos para análise.
- Clique em "Iniciar Análise de Sentimento".
- Visualize os resultados, gráficos e estatísticas.
- Exporte os resultados para CSV.

#### 2. Análise de Texto Livre
- Digite ou cole um texto.
- Clique em "Analisar Sentimento".
- Visualize o resultado da análise.

## Para Desenvolvedores

### Formatação de Código

O projeto usa Black para formatação de código:

```bash
pip install black
black src/ scripts/ main.py
```

### Verificação de Estilo (Linting)

Use Flake8 para verificar o estilo do código:

```bash
pip install flake8
flake8 src/ scripts/ main.py
```

## Modelo de Linguagem

A aplicação utiliza o modelo `nlptown/bert-base-multilingual-uncased-sentiment` da biblioteca Transformers para realizar a análise de sentimento.

## Notas

- A primeira execução pode ser mais lenta devido ao download do modelo.
- Para arquivos grandes, o processamento pode levar algum tempo.
- Para desativar o ambiente virtual quando terminar, use o comando `deactivate`

## Resolução de Problemas

### Problemas comuns

- **No macOS**: Se o comando `source venv/bin/activate` não funcionar, use `. venv/bin/activate` (com um ponto seguido de espaço) como alternativa.

- **Problemas com NLTK**: Se encontrar erros sobre "Resource stopwords not found", execute o script de download:
  ```bash
  python scripts/download_nltk_resources.py
  ```

- **Erros de SSL no macOS**: Se encontrar erros de SSL ao baixar recursos, o script `download_nltk_resources.py` já inclui uma correção para esse problema. Se mesmo assim persistir, tente usar:
  ```python
  import ssl
  try:
      _create_unverified_https_context = ssl._create_unverified_context
  except AttributeError:
      pass
  else:
      ssl._create_default_https_context = _create_unverified_https_context
  ```

- **Problemas com PyTorch**: Se o pipenv falhar ao instalar o PyTorch, use o ambiente venv e o requirements.txt com versões adequadas para seu sistema.

- **Problemas com spaCy**: Para verificar se o spaCy está instalado corretamente, execute:
  ```bash
  python scripts/verify_spacy.py
  ```

- **Problemas com login**: Se esquecer a senha, você pode verificar ou modificar os usuários no arquivo `src/web/auth.py`.

## Licença

Este projeto é distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes. 