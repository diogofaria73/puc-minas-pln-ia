"""
Módulo para manipulação de dados de entrada e saída.
"""

import pandas as pd
import numpy as np
import os

def carregar_arquivo(file):
    """
    Carrega um arquivo CSV ou Excel em um DataFrame pandas.
    
    Args:
        file: Objeto de arquivo (pode ser um caminho ou um objeto UploadedFile do Streamlit)
        
    Returns:
        DataFrame: DataFrame pandas com os dados carregados
    """
    # Verifica se é um caminho ou um objeto de upload
    if isinstance(file, str):
        caminho = file
    else:
        nome_arquivo = file.name
        
    # Determina o tipo de arquivo e carrega
    if nome_arquivo.endswith('.csv'):
        return pd.read_csv(file)
    elif nome_arquivo.endswith(('.xlsx', '.xls')):
        return pd.read_excel(file)
    else:
        raise ValueError(f"Formato de arquivo não suportado: {nome_arquivo}")

def salvar_resultados(df, caminho=None):
    """
    Salva um DataFrame com resultados em formato CSV.
    
    Args:
        df (DataFrame): DataFrame a ser salvo
        caminho (str, opcional): Caminho para salvar o arquivo. Se None, usa 'data/resultados.csv'
        
    Returns:
        str: Caminho onde o arquivo foi salvo
    """
    if caminho is None:
        # Garantir que o diretório exista
        os.makedirs('data', exist_ok=True)
        caminho = 'data/resultados.csv'
        
    df.to_csv(caminho, index=False)
    return caminho

def criar_estatisticas(df):
    """
    Cria estatísticas básicas a partir de um DataFrame com resultados de sentimento.
    
    Args:
        df (DataFrame): DataFrame com coluna 'sentimento'
        
    Returns:
        dict: Dicionário com estatísticas de sentimento
    """
    total = len(df)
    positivos = len(df[df['sentimento'] == 'positivo'])
    negativos = len(df[df['sentimento'] == 'negativo'])
    neutros = len(df[df['sentimento'] == 'neutro'])
    
    stats = {
        'total': total,
        'positivos': positivos,
        'positivos_pct': (positivos/total)*100 if total > 0 else 0,
        'neutros': neutros,
        'neutros_pct': (neutros/total)*100 if total > 0 else 0,
        'negativos': negativos,
        'negativos_pct': (negativos/total)*100 if total > 0 else 0,
    }
    
    return stats 