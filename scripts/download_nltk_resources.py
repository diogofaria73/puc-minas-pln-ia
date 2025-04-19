#!/usr/bin/env python3
"""
Script para baixar recursos necessários do NLTK.
Contorna problemas com SSL em alguns sistemas.
"""

import nltk

# Tente baixar os recursos
print("Tentando baixar recursos do NLTK...")
try:
    nltk.download('stopwords')
    print("Stopwords baixado com sucesso!")
    nltk.download('punkt')
    print("Punkt baixado com sucesso!")
    print("Todos os recursos do NLTK foram baixados com sucesso!")
except Exception as e:
    print(f"Erro ao baixar recursos do NLTK: {e}")
    
    # Se falhar, tente com o ajuste SSL
    print("\nTentando com ajuste SSL...")
    try:
        import ssl
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
            
        nltk.download('stopwords')
        print("Stopwords baixado com sucesso!")
        nltk.download('punkt')
        print("Punkt baixado com sucesso!")
        print("Todos os recursos do NLTK foram baixados com sucesso com ajuste SSL!")
    except Exception as e2:
        print(f"Erro mesmo com ajuste SSL: {e2}")
        print("\nDica: Você pode tentar baixar os recursos manualmente usando o NLTK Downloader:")
        print("python -m nltk.downloader stopwords punkt") 