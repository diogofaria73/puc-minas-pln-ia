"""
Módulo para visualização de dados de análise de texto.
"""

import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import plotly.express as px
import base64
import io

def criar_nuvem_palavras(textos):
    """
    Cria uma nuvem de palavras a partir de textos.
    
    Args:
        textos (list): Lista de textos para criar a nuvem de palavras
        
    Returns:
        objeto: Figura matplotlib com a nuvem de palavras
    """
    texto_completo = " ".join(textos)
    fig, ax = plt.subplots(figsize=(10, 5))
    wordcloud = WordCloud(
        width=800, 
        height=400, 
        background_color='white',
        colormap='viridis'
    ).generate(texto_completo)
    
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    return fig

def grafico_distribuicao_sentimentos(df):
    """
    Cria um gráfico de pizza com a distribuição de sentimentos.
    
    Args:
        df (DataFrame): DataFrame pandas com coluna 'sentimento'
        
    Returns:
        objeto: Figura plotly com o gráfico de distribuição
    """
    fig = px.pie(
        df, 
        names='sentimento', 
        title='Distribuição de Sentimentos',
        color='sentimento',
        color_discrete_map={
            'positivo': '#28a745',
            'neutro': '#ffc107',
            'negativo': '#dc3545'
        }
    )
    return fig

def get_download_link(df, filename, text):
    """
    Cria um link para download de um DataFrame como CSV.
    
    Args:
        df (DataFrame): DataFrame a ser salvo
        filename (str): Nome do arquivo para download
        text (str): Texto do link
        
    Returns:
        str: HTML com link para download
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href 