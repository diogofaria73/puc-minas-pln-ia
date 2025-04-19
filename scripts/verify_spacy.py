#!/usr/bin/env python3
"""
Script para verificar se o modelo do spaCy está instalado corretamente.
"""

import spacy
import os

print("Verificando instalação do spaCy...")

# Verificar modelos disponíveis
try:
    # Tentar carregar o modelo
    print("Tentando carregar o modelo pt_core_news_sm...")
    nlp = spacy.load("pt_core_news_sm")
    print("Modelo carregado com sucesso!")
    
    # Testar o modelo
    texto = "A análise de sentimento é uma parte importante do processamento de linguagem natural."
    doc = nlp(texto)
    
    print("\nTokens do texto de exemplo:")
    for token in doc:
        print(f"Token: {token.text}, Lema: {token.lemma_}, POS: {token.pos_}")
    
    print("\nEntidades nomeadas:")
    for ent in doc.ents:
        print(f"Entidade: {ent.text}, Tipo: {ent.label_}")
        
    print("\nSpaCy está funcionando corretamente!")
    
except Exception as e:
    print(f"Erro ao carregar o modelo: {e}")
    print("\nVocê precisa baixar o modelo pt_core_news_sm usando:")
    print("python -m spacy download pt_core_news_sm")
    
# Verificar o diretório do modelo
try:
    import site
    site_packages = site.getsitepackages()
    print(f"\nDiretórios de pacotes Python: {site_packages}")
    
    # Verificar cada diretório site-packages
    for site_dir in site_packages:
        spacy_models_dir = os.path.join(site_dir, "spacy", "data")
        if os.path.exists(spacy_models_dir):
            print(f"Diretório de modelos spaCy encontrado em: {spacy_models_dir}")
            models = os.listdir(spacy_models_dir)
            print(f"Modelos disponíveis: {models}")
except Exception as e:
    print(f"Erro ao verificar diretórios: {e}") 