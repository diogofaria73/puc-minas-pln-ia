#!/bin/bash
# Script para facilitar a execução da aplicação Streamlit com Pipenv

# Detectar o sistema operacional
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    OPEN_CMD="open"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    # Windows
    OPEN_CMD="start"
else
    # Linux e outros
    OPEN_CMD="xdg-open"
fi

# Função para exibir mensagens coloridas
function echo_color() {
    local color=$1
    local message=$2
    
    if [ -t 1 ]; then  # Verifica se o stdout é um terminal
        case $color in
            "green")  echo -e "\033[32m$message\033[0m" ;;
            "yellow") echo -e "\033[33m$message\033[0m" ;;
            "red")    echo -e "\033[31m$message\033[0m" ;;
            "blue")   echo -e "\033[34m$message\033[0m" ;;
            *)        echo "$message" ;;
        esac
    else
        echo "$message"
    fi
}

# Verificar se Pipenv está instalado
if ! command -v pipenv &> /dev/null; then
    echo_color "red" "❌ Pipenv não está instalado. Instalando..."
    pip install pipenv
fi

# Menu simples
clear
echo_color "blue" "🧠 Análise de Sentimento - PUC Minas"
echo_color "blue" "==============================="
echo ""
echo_color "yellow" "Escolha uma opção:"
echo "1. Instalar dependências"
echo "2. Baixar recursos necessários"
echo "3. Baixar dados de exemplo"
echo "4. Executar aplicação"
echo "5. Formatar código (dev)"
echo "6. Verificar estilo (lint, dev)"
echo "7. Limpar arquivos temporários"
echo "8. Sair"
echo ""
read -p "Opção: " option

case $option in
    1)
        echo_color "yellow" "⏳ Instalando dependências..."
        pipenv install
        echo_color "green" "✅ Dependências instaladas com sucesso!"
        ;;
    2)
        echo_color "yellow" "⏳ Baixando recursos necessários..."
        pipenv run setup
        echo_color "green" "✅ Recursos baixados com sucesso!"
        ;;
    3)
        echo_color "yellow" "⏳ Baixando dados de exemplo..."
        pipenv run download_example
        echo_color "green" "✅ Dados de exemplo baixados com sucesso!"
        ;;
    4)
        echo_color "yellow" "⏳ Executando aplicação..."
        # Iniciar a aplicação em segundo plano
        pipenv run app &
        APP_PID=$!
        
        # Esperar um pouco para o servidor iniciar
        sleep 3
        
        # Abrir o navegador
        echo_color "yellow" "🌐 Abrindo navegador em http://localhost:8501"
        $OPEN_CMD http://localhost:8501
        
        # Aguardar o processo da aplicação terminar
        wait $APP_PID
        ;;
    5)
        echo_color "yellow" "⏳ Formatando código com Black..."
        pipenv run format
        echo_color "green" "✅ Código formatado com sucesso!"
        ;;
    6)
        echo_color "yellow" "⏳ Verificando estilo com Flake8..."
        pipenv run lint
        echo_color "green" "✅ Verificação de estilo concluída!"
        ;;
    7)
        echo_color "yellow" "⏳ Limpando arquivos temporários..."
        pipenv run cleanup
        echo_color "green" "✅ Limpeza concluída!"
        ;;
    8)
        echo_color "blue" "👋 Até mais!"
        exit 0
        ;;
    *)
        echo_color "red" "❌ Opção inválida"
        ;;
esac 