#!/usr/bin/env python3
"""
Script para download de dados de exemplo para testes da aplicação.
"""

import pandas as pd
import numpy as np
import os
import requests
from tqdm import tqdm
import sys

# Adiciona o diretório raiz ao path para poder importar os módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def download_example_data():
    """
    Download dados de exemplo para testes da aplicação.
    Se não for possível baixar, cria um conjunto de dados sintético.
    """
    print("Criando pasta 'data' se não existir...")
    os.makedirs("data", exist_ok=True)
    
    output_file = "data/dados_exemplo.csv"
    
    if os.path.exists(output_file):
        print(f"O arquivo {output_file} já existe. Pulando download.")
        return
    
    # Tenta baixar dados de exemplo
    try:
        print("Tentando baixar dados de exemplo...")
        
        # URL de exemplo (substitua por uma URL válida se necessário)
        url = "https://raw.githubusercontent.com/neuralmind-ai/portuguese-bert/master/ner_evaluation/data/miniCorpus.conll"
        
        response = requests.get(url)
        response.raise_for_status()
        
        # Processar os dados para criar um CSV
        lines = response.text.strip().split('\n')
        data = []
        current_text = []
        current_label = None
        
        for line in lines:
            if line.strip() == '':
                if current_text:
                    data.append({
                        'texto': ' '.join(current_text),
                        'rotulo': current_label or 'neutro'  # Valor padrão
                    })
                    current_text = []
                continue
                
            parts = line.split()
            if len(parts) >= 2:
                word = parts[0]
                current_text.append(word)
                
                # Tenta inferir sentimento com base nas tags
                if any(tag in parts[-1] for tag in ['POS', 'GOOD', 'POSITIVE']):
                    current_label = 'positivo'
                elif any(tag in parts[-1] for tag in ['NEG', 'BAD', 'NEGATIVE']):
                    current_label = 'negativo'
        
        # Cria o DataFrame
        df = pd.DataFrame(data)
        
    except Exception as e:
        print(f"Erro ao baixar dados: {e}")
        print("Gerando dados sintéticos aleatórios...")
        
        # Criar dados sintéticos
        n_samples = 100
        texts = [
            "Estou muito satisfeito com o curso da PUC Minas. Professores excelentes.",
            "O atendimento online foi ótimo, resolveram meu problema rapidamente.",
            "Achei as aulas interessantes e o conteúdo relevante para o mercado.",
            "A plataforma de ensino é intuitiva e funciona bem na maior parte do tempo.",
            "Recebi feedback rápido dos professores, muito bom.",
            "O curso atendeu minhas expectativas, recomendo.",
            "Os laboratórios da universidade são bem equipados.",
            "A biblioteca digital tem um acervo excelente para pesquisa.",
            "A metodologia de ensino é atual e dinâmica.",
            "Consegui aplicar o conhecimento no meu trabalho, muito útil.",
            
            "A aula foi normal, nada muito especial.",
            "O conteúdo é adequado, mas poderia ser mais aprofundado.",
            "Tive algumas dificuldades, mas consegui acompanhar.",
            "O sistema às vezes fica fora do ar, mas funciona na maior parte do tempo.",
            "Alguns professores respondem rápido, outros demoram um pouco.",
            "O curso é bom, mas esperava mais prática.",
            "Material didático ok, cumpre o básico.",
            "A plataforma é razoável, tem o necessário.",
            "A comunicação com a coordenação poderia ser melhor.",
            "Os trabalhos em grupo às vezes são complicados de organizar.",
            
            "Tive problemas com a matrícula e ninguém resolveu.",
            "O professor não responde emails e não tira dúvidas.",
            "Conteúdo desatualizado e não reflete o mercado atual.",
            "Muitos problemas técnicos durante as aulas online.",
            "O suporte técnico é muito ruim, demoram dias para responder.",
            "Notas lançadas com atraso e sem feedback.",
            "Material didático com muitos erros e mal explicado.",
            "Avaliações muito difíceis e não condizentes com o conteúdo.",
            "Dificuldade para acessar os sistemas da universidade.",
            "Ambiente de estudo barulhento e desconfortável."
        ]
        
        sentiments = {
            text: "positivo" if i < 10 else ("neutro" if i < 20 else "negativo")
            for i, text in enumerate(texts)
        }
        
        # Gerar dados aleatórios
        df = pd.DataFrame({
            'id': range(1, n_samples + 1),
            'data': pd.date_range(start='2023-01-01', periods=n_samples),
            'texto': np.random.choice(texts, size=n_samples),
            'fonte': np.random.choice(['formulário', 'email', 'chat', 'redes sociais'], size=n_samples),
            'departamento': np.random.choice(['graduação', 'pós-graduação', 'administrativo', 'biblioteca'], size=n_samples)
        })
        
        # Atribui sentimento com base no texto
        df['sentimento_original'] = df['texto'].map(sentiments)
        
    # Salva o DataFrame
    print(f"Salvando {len(df)} exemplos em {output_file}...")
    df.to_csv(output_file, index=False)
    print("Download concluído!")

if __name__ == "__main__":
    download_example_data()
    print("\nPara usar o arquivo de exemplo, execute a aplicação com 'streamlit run main.py'")
    print("e selecione o arquivo 'data/dados_exemplo.csv' na interface.") 