"""
Módulo para análise de sentimento em textos.
"""

from transformers import pipeline

def load_sentiment_model():
    """
    Carrega o modelo de análise de sentimento.
    
    Returns:
        objeto: Modelo de análise de sentimento (pipeline)
    """
    return pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

def analisar_sentimento(texto, classificador):
    """
    Analisa o sentimento de um texto.
    
    Args:
        texto (str): Texto a ser analisado
        classificador: Modelo de análise de sentimento
        
    Returns:
        str: Sentimento identificado (positivo, neutro, negativo ou erro)
    """
    try:
        resultado = classificador(texto[:512])[0]
        estrelas = int(resultado['label'][0])
        if estrelas in [4, 5]:
            return "positivo"
        elif estrelas == 3:
            return "neutro"
        else:
            return "negativo"
    except Exception as e:
        print(f"Erro ao analisar sentimento: {e}")
        return "erro" 