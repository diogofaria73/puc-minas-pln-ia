"""
Módulo para processamento de textos.
Contém funções para limpeza, pré-processamento e análise de texto.
"""

import re
import spacy
from nltk.corpus import stopwords
import nltk

# Garantir recursos necessários
try:
    stopwords.words('portuguese')
except LookupError:
    nltk.download('stopwords')

def load_nlp_resources():
    """
    Carrega recursos de processamento de linguagem natural.
    
    Returns:
        tuple: Modelo spaCy e conjunto de stopwords em português
    """
    try:
        nlp = spacy.load("pt_core_news_sm")
    except OSError:
        spacy.cli.download("pt_core_news_sm")
        nlp = spacy.load("pt_core_news_sm")
        
    stopwords_pt = set(stopwords.words('portuguese'))
    return nlp, stopwords_pt

def limpar_texto(texto):
    """
    Remove URLs, menções, hashtags, pontuação e números de um texto.
    
    Args:
        texto (str): Texto a ser limpo
        
    Returns:
        str: Texto limpo
    """
    texto = re.sub(r"http\S+|www.\S+", "", str(texto))
    texto = re.sub(r"@\w+|#\w+", "", texto)
    texto = re.sub(r"[^\w\s]", "", texto)
    texto = re.sub(r"\d+", "", texto)
    texto = texto.lower().strip()
    return texto

def lematizar(texto, nlp, stopwords_pt):
    """
    Realiza lematização e remove stopwords.
    
    Args:
        texto (str): Texto a ser lematizado
        nlp: Modelo spaCy carregado
        stopwords_pt: Conjunto de stopwords
        
    Returns:
        str: Texto lematizado sem stopwords
    """
    doc = nlp(texto)
    return " ".join([token.lemma_ for token in doc if token.text not in stopwords_pt and token.is_alpha])

def preprocessar_texto(texto, nlp, stopwords_pt):
    """
    Aplica todo o pipeline de pré-processamento ao texto.
    
    Args:
        texto (str): Texto original
        nlp: Modelo spaCy carregado
        stopwords_pt: Conjunto de stopwords
        
    Returns:
        str: Texto pré-processado
    """
    return lematizar(limpar_texto(texto), nlp, stopwords_pt) 