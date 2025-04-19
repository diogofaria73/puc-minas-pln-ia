"""
Módulo principal da aplicação web Streamlit.
"""

import streamlit as st
import pandas as pd
import numpy as np

# Importa módulos do projeto
from src.utils.text_processing import load_nlp_resources, preprocessar_texto
from src.models.sentiment_analysis import load_sentiment_model, analisar_sentimento
from src.models.topic_analysis import identificar_topicos
from src.utils.visualization import criar_nuvem_palavras, grafico_distribuicao_sentimentos, get_download_link
from src.data.data_handler import carregar_arquivo, criar_estatisticas
from src.web.auth import pagina_login, verificar_autenticacao, obter_usuario_atual, logout

@st.cache_resource
def carregar_recursos():
    """Carrega os recursos necessários para a aplicação."""
    nlp, stopwords_pt = load_nlp_resources()
    modelo_sentimento = load_sentiment_model()
    return nlp, stopwords_pt, modelo_sentimento

def configurar_pagina():
    """Configura a página do Streamlit."""
    st.set_page_config(
        page_title="Análise de Sentimento - PUC Minas",
        page_icon="🧠",
        layout="wide"
    )

def modo_arquivo(nlp, stopwords_pt, classificador):
    """Interface para análise de sentimento a partir de arquivo."""
    st.subheader("Carregue um arquivo CSV ou Excel")
    
    # Opção para processar automaticamente
    auto_process = st.checkbox("Processar automaticamente usando a coluna 'Message' quando disponível", value=True)
    
    file = st.file_uploader("Selecione o arquivo", type=["csv", "xlsx", "xls"])
    
    if file is not None:
        try:
            df = carregar_arquivo(file)
            
            # Adicionando um indicador de sucesso ao carregar o arquivo
            st.success(f"Arquivo carregado com sucesso! ({len(df)} linhas)")
            
            st.write("Visualização dos dados:")
            st.dataframe(df.head())
            
            # Verifica se existe a coluna 'Message' - buscando exatamente com esse nome
            message_col = None
            default_col_index = 0
            
            # Primeiro, procurar por "Message" (exatamente)
            if "Message" in df.columns:
                message_col = "Message"
                default_col_index = list(df.columns).index("Message")
            # Caso não encontre, procurar por qualquer coluna que contenha "message" em minúsculo
            else:
                for i, col in enumerate(df.columns):
                    if "message" in col.lower():
                        default_col_index = i
                        message_col = col
                        break
            
            # Seleciona a coluna para análise com a coluna 'Message' como padrão, se existir
            col_texto = st.selectbox(
                "Selecione a coluna que contém o texto para análise:",
                df.columns,
                index=default_col_index
            )
            
            # Se o auto_process está ativado e encontramos a coluna 'Message', processamos automaticamente
            auto_processing = auto_process and message_col is not None
            
            # Botão para iniciar análise (não mostramos se estiver em processamento automático)
            if auto_processing:
                st.info(f"Processamento automático ativado usando a coluna '{message_col}'")
                process_button = True
            else:
                process_button = st.button("Iniciar Análise de Sentimento")
            
            if process_button:
                if col_texto:
                    with st.spinner("Processando os textos..."):
                        # Mostrar exemplo do que está sendo processado
                        st.write("Exemplo de texto a ser analisado:")
                        st.code(df[col_texto].iloc[0][:500] + "..." if len(str(df[col_texto].iloc[0])) > 500 else df[col_texto].iloc[0])
                        
                        # Pré-processamento
                        df['texto_limpo'] = df[col_texto].astype(str).apply(
                            lambda texto: preprocessar_texto(texto, nlp, stopwords_pt)
                        )
                        
                        # Remove textos vazios
                        textos_antes = len(df)
                        df = df[df['texto_limpo'].str.strip() != ""]
                        textos_removidos = textos_antes - len(df)
                        if textos_removidos > 0:
                            st.warning(f"{textos_removidos} textos foram removidos por estarem vazios após o pré-processamento.")
                        
                        # Análise de sentimento
                        st.info(f"Analisando sentimentos de {len(df)} textos...")
                        df["sentimento"] = df["texto_limpo"].apply(
                            lambda x: analisar_sentimento(x, classificador)
                        )
                        
                        # Remove erros
                        erros_antes = len(df)
                        df = df[df["sentimento"] != "erro"]
                        erros_removidos = erros_antes - len(df)
                        if erros_removidos > 0:
                            st.warning(f"{erros_removidos} textos foram removidos devido a erros na análise.")
                        
                        # Mostra resultados
                        st.success(f"Análise concluída para {len(df)} textos!")
                        
                        # Resultados
                        resultados, graficos = st.tabs(["Resultados", "Visualizações"])
                        
                        with resultados:
                            st.write("Dados com análise de sentimento:")
                            
                            # Adicionando filtro por sentimento
                            sentimento_filter = st.multiselect("Filtrar por sentimento:", 
                                                              ["positivo", "neutro", "negativo"], 
                                                              default=["positivo", "neutro", "negativo"])
                            
                            # Aplicando o filtro
                            df_filtered = df[df["sentimento"].isin(sentimento_filter)]
                            
                            # Mostrando os resultados filtrados
                            st.dataframe(df_filtered[[col_texto, 'texto_limpo', 'sentimento']])
                            
                            # Download dos resultados
                            st.markdown(
                                get_download_link(df, "analise_sentimento.csv", "📥 Baixar resultados completos (CSV)"), 
                                unsafe_allow_html=True
                            )
                            
                            # Estatísticas
                            st.subheader("📋 Relatório")
                            
                            stats = criar_estatisticas(df)
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Positivos", f"{stats['positivos']} ({stats['positivos_pct']:.1f}%)")
                            with col2:
                                st.metric("Neutros", f"{stats['neutros']} ({stats['neutros_pct']:.1f}%)")
                            with col3:
                                st.metric("Negativos", f"{stats['negativos']} ({stats['negativos_pct']:.1f}%)")
                            
                            # Recomendações
                            st.subheader("💡 Insights")
                            if stats['negativos'] > stats['positivos']:
                                st.warning("⚠️ Há mais menções negativas que positivas. Recomenda-se investigar as causas e ajustar a comunicação.")
                            else:
                                st.success("✅ Boa percepção geral. Recomenda-se manter a estratégia atual e expandir ações positivas.")
                        
                        with graficos:
                            st.subheader("📊 Visualizações")
                            
                            # Distribuição de sentimentos
                            fig = grafico_distribuicao_sentimentos(df)
                            st.plotly_chart(fig)
                            
                            # Nuvem de palavras
                            st.subheader("🔤 Nuvem de Palavras")
                            fig_nuvem = criar_nuvem_palavras(df['texto_limpo'])
                            st.pyplot(fig_nuvem)
                            
                            # Tópicos LDA
                            st.subheader("🧵 Tópicos Identificados (LDA)")
                            n_topicos = st.slider("Número de tópicos", 2, 10, 3)
                            topicos = identificar_topicos(df['texto_limpo'], stopwords_pt, n_topicos)
                            
                            for i, termos in enumerate(topicos):
                                st.write(f"**Tópico {i+1}:** {' | '.join(termos)}")
                
                else:
                    st.error("Por favor, selecione uma coluna para análise.")
        
        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {str(e)}")
            # Mostrar traceback para depuração
            import traceback
            st.code(traceback.format_exc(), language="python")

def modo_texto_livre(nlp, stopwords_pt, classificador):
    """Interface para análise de sentimento de texto livre."""
    st.subheader("Digite ou cole o texto para análise")
    
    texto_usuario = st.text_area("Texto para análise:", height=150)
    
    if st.button("Analisar Sentimento"):
        if texto_usuario:
            # Pré-processamento
            texto_limpo = preprocessar_texto(texto_usuario, nlp, stopwords_pt)
            
            if texto_limpo.strip() == "":
                st.warning("O texto ficou vazio após o pré-processamento. Tente um texto mais longo.")
            else:
                # Análise de sentimento
                sentimento = analisar_sentimento(texto_usuario, classificador)
                
                # Resultado
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    if sentimento == "positivo":
                        st.success("Sentimento: Positivo ✅")
                    elif sentimento == "neutro":
                        st.info("Sentimento: Neutro ⚠️")
                    elif sentimento == "negativo":
                        st.error("Sentimento: Negativo ❌")
                    else:
                        st.warning("Não foi possível analisar o sentimento.")
                
                with col2:
                    st.write("Texto pré-processado:")
                    st.code(texto_limpo)
        else:
            st.warning("Por favor, digite um texto para análise.")

def main():
    """Função principal da aplicação."""
    configurar_pagina()
    
    # Verificar autenticação
    if not verificar_autenticacao():
        autenticado = pagina_login()
        if not autenticado:
            return  # Parar execução se não estiver autenticado
    
    # Cabeçalho da aplicação
    st.title("📊 Análise de Sentimento de Textos")
    st.markdown("### PUC Minas - Processamento de Linguagem Natural")
    
    # Barra lateral com informações do usuário
    with st.sidebar:
        st.title("Opções")
        
        # Mostrar informações do usuário
        usuario_atual = obter_usuario_atual()
        st.sidebar.info(f"Usuário: **{usuario_atual}**")
        
        if st.sidebar.button("Sair"):
            logout()
            st.experimental_rerun()
        
        # Opções de modo
        st.sidebar.divider()
        modo = st.sidebar.radio("Escolha o modo:", ["Arquivo CSV/Excel", "Texto Livre"])
    
    # Carregar recursos
    with st.spinner("Carregando recursos necessários..."):
        nlp, stopwords_pt, classificador = carregar_recursos()
        st.sidebar.success("✅ Modelos carregados!")
    
    # Interface principal conforme o modo selecionado
    if modo == "Arquivo CSV/Excel":
        modo_arquivo(nlp, stopwords_pt, classificador)
    else:
        modo_texto_livre(nlp, stopwords_pt, classificador)
    
    # Footer
    st.markdown("---")
    st.markdown("Desenvolvido para PUC Minas | PLN e IA - Análise de Sentimento")

# Exportar a função main para ser usada por outros módulos
if __name__ == "__main__":
    main() 