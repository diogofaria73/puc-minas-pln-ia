#!/usr/bin/env python3
"""
Script para verificar se os recursos do NLTK estão instalados corretamente.
"""

import nltk
import os

print("Verificando recursos do NLTK...")

# Verificar diretório do NLTK
nltk_data_path = nltk.data.path
print(f"Diretórios de dados do NLTK: {nltk_data_path}")

# Verificar disponibilidade das stopwords
try:
    from nltk.corpus import stopwords
    palavras = stopwords.words('portuguese')
    print(f"Stopwords em português disponíveis: {len(palavras)} palavras")
    print(f"Primeiras 10 stopwords: {palavras[:10]}")
except Exception as e:
    print(f"Erro ao acessar stopwords: {e}")

# Verificar disponibilidade do tokenizador punkt
try:
    from nltk.tokenize import word_tokenize
    texto = "Testando o tokenizador do NLTK. Este é um teste."
    tokens = word_tokenize(texto, language='portuguese')
    print(f"Tokenização funcionando: {tokens}")
except Exception as e:
    print(f"Erro ao usar tokenizador: {e}")

# Verificar diretamente os arquivos
nltk_home = os.path.expanduser("~/nltk_data")
print(f"\nVerificando arquivos no diretório: {nltk_home}")
if os.path.exists(nltk_home):
    print("Diretório nltk_data existe")
    
    stopwords_path = os.path.join(nltk_home, "corpora", "stopwords")
    if os.path.exists(stopwords_path):
        print(f"Diretório stopwords existe: {stopwords_path}")
        
    punkt_path = os.path.join(nltk_home, "tokenizers", "punkt")
    if os.path.exists(punkt_path):
        print(f"Diretório punkt existe: {punkt_path}")
else:
    print("Diretório nltk_data não existe") 