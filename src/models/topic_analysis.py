"""
Módulo para identificação de tópicos em textos usando LDA.
"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

def identificar_topicos(textos, stopwords_pt, n_topicos=3):
    """
    Identifica tópicos em um conjunto de textos usando LDA.
    
    Args:
        textos (list): Lista de textos para análise
        stopwords_pt (set): Conjunto de stopwords em português
        n_topicos (int): Número de tópicos a identificar
        
    Returns:
        list: Lista de tópicos, onde cada tópico é uma lista de palavras
    """
    vetor = CountVectorizer(max_df=0.9, min_df=2, stop_words=list(stopwords_pt))
    
    try:
        # Transformar os textos em matriz de contagem
        matriz = vetor.fit_transform(textos)
        
        # Aplicar LDA
        lda = LatentDirichletAllocation(n_components=n_topicos, random_state=0)
        lda.fit(matriz)
        
        # Extrair os termos mais importantes para cada tópico
        palavras = vetor.get_feature_names_out()
        topicos = []
        
        for i, topico in enumerate(lda.components_):
            termos = [palavras[i] for i in topico.argsort()[-10:]]
            topicos.append(termos)
            
        return topicos
    except Exception as e:
        print(f"Erro ao identificar tópicos: {e}")
        return [] 