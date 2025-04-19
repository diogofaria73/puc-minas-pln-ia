#!/usr/bin/env python3
"""
Script para configuração inicial do ambiente.
Baixa recursos necessários para NLTK e spaCy.
"""

import nltk
import spacy
import ssl
import os
import sys

# Adiciona o diretório raiz ao path para poder importar os módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def configurar_ambiente():
    """Configura o ambiente baixando recursos necessários."""
    print("🔄 Iniciando configuração do ambiente...")
    
    # Contornar problemas de SSL para downloads
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    # Download NLTK resources
    print("📦 Baixando recursos NLTK...")
    nltk.download('stopwords')
    nltk.download('punkt')

    # Download spaCy model
    print("📦 Baixando modelo spaCy para português...")
    try:
        spacy.load('pt_core_news_sm')
        print("✅ Modelo spaCy já está instalado!")
    except OSError:
        print("⏳ Instalando modelo spaCy...")
        spacy.cli.download('pt_core_news_sm')
        print("✅ Modelo spaCy instalado com sucesso!")
    
    print("\n✅ Setup concluído! Recursos baixados com sucesso.")
    print("\nPara iniciar a aplicação, execute: streamlit run main.py")

if __name__ == "__main__":
    configurar_ambiente() 