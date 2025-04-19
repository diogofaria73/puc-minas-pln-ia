# Script PowerShell para facilitar a execução da aplicação Streamlit com Pipenv

# Função para exibir mensagens coloridas
function Write-ColorOutput {
    param (
        [Parameter(Mandatory=$true)]
        [string]$Message,
        
        [Parameter(Mandatory=$true)]
        [string]$Color
    )
    
    $prevColor = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $Color
    Write-Output $Message
    $host.UI.RawUI.ForegroundColor = $prevColor
}

# Verificar se Pipenv está instalado
try {
    $null = Get-Command pipenv -ErrorAction Stop
} catch {
    Write-ColorOutput "❌ Pipenv não está instalado. Instalando..." "Red"
    pip install pipenv
}

# Menu simples
Clear-Host
Write-ColorOutput "🧠 Análise de Sentimento - PUC Minas" "Blue"
Write-ColorOutput "===============================" "Blue"
Write-Output ""
Write-ColorOutput "Escolha uma opção:" "Yellow"
Write-Output "1. Instalar dependências"
Write-Output "2. Baixar recursos necessários"
Write-Output "3. Baixar dados de exemplo"
Write-Output "4. Executar aplicação"
Write-Output "5. Formatar código (dev)"
Write-Output "6. Verificar estilo (lint, dev)"
Write-Output "7. Limpar arquivos temporários"
Write-Output "8. Sair"
Write-Output ""
$option = Read-Host "Opção"

switch ($option) {
    "1" {
        Write-ColorOutput "⏳ Instalando dependências..." "Yellow"
        pipenv install
        Write-ColorOutput "✅ Dependências instaladas com sucesso!" "Green"
    }
    "2" {
        Write-ColorOutput "⏳ Baixando recursos necessários..." "Yellow"
        pipenv run setup
        Write-ColorOutput "✅ Recursos baixados com sucesso!" "Green"
    }
    "3" {
        Write-ColorOutput "⏳ Baixando dados de exemplo..." "Yellow"
        pipenv run download_example
        Write-ColorOutput "✅ Dados de exemplo baixados com sucesso!" "Green"
    }
    "4" {
        Write-ColorOutput "⏳ Executando aplicação..." "Yellow"
        # Iniciar a aplicação em um novo processo
        $process = Start-Process -FilePath "pipenv" -ArgumentList "run app" -PassThru
        
        # Esperar um pouco para o servidor iniciar
        Start-Sleep -Seconds 3
        
        # Abrir o navegador
        Write-ColorOutput "🌐 Abrindo navegador em http://localhost:8501" "Yellow"
        Start-Process "http://localhost:8501"
        
        # Aguardar o usuário querer encerrar
        Write-Output "Pressione Enter para encerrar a aplicação..."
        $null = Read-Host
        
        # Encerrar o processo
        if (-not $process.HasExited) {
            Stop-Process -Id $process.Id -Force
        }
    }
    "5" {
        Write-ColorOutput "⏳ Formatando código com Black..." "Yellow"
        pipenv run format
        Write-ColorOutput "✅ Código formatado com sucesso!" "Green"
    }
    "6" {
        Write-ColorOutput "⏳ Verificando estilo com Flake8..." "Yellow"
        pipenv run lint
        Write-ColorOutput "✅ Verificação de estilo concluída!" "Green"
    }
    "7" {
        Write-ColorOutput "⏳ Limpando arquivos temporários..." "Yellow"
        pipenv run cleanup
        Write-ColorOutput "✅ Limpeza concluída!" "Green"
    }
    "8" {
        Write-ColorOutput "👋 Até mais!" "Blue"
        exit
    }
    default {
        Write-ColorOutput "❌ Opção inválida" "Red"
    }
} 