#!/usr/bin/env python3
"""
Ponto de entrada principal para a aplicação de análise de sentimento.
Utiliza Streamlit para criar uma interface web interativa.
"""

import streamlit as st
from src.web.app import main as app_main

# Inicializa a aplicação Streamlit
if __name__ == "__main__":
    app_main() 