#!/usr/bin/env python3
"""
Script para limpar arquivos temporários e desnecessários do projeto.
"""

import os
import sys
import shutil
from pathlib import Path

def limpar_projeto():
    """Remove arquivos temporários e desnecessários do projeto."""
    # Diretório raiz do projeto
    root_dir = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    # Lista de arquivos para remover
    arquivos_para_remover = [
        # Arquivos na raiz que foram migrados
        root_dir / "app.py",
        root_dir / "download_example_data.py",
        root_dir / "run.sh",
        root_dir / "run.ps1",
        root_dir / "setup.py",
        root_dir / "migrate_to_pipenv.py",
        
        # Arquivos temporários e de exemplo
        root_dir / "Whatarethemostrecentposts_82b4ab34-c534-40c7-9ed1-db5efd98c72d_1.xlsx",
        
        # Cache Python
        root_dir / "__pycache__",
        root_dir / "src" / "__pycache__",
        root_dir / "src" / "data" / "__pycache__",
        root_dir / "src" / "models" / "__pycache__",
        root_dir / "src" / "utils" / "__pycache__",
        root_dir / "src" / "web" / "__pycache__",
        root_dir / "scripts" / "__pycache__",
        
        # Outros arquivos temporários
        root_dir / ".ipynb_checkpoints",
    ]
    
    # Remover arquivos
    for arquivo in arquivos_para_remover:
        if arquivo.exists():
            print(f"Removendo: {arquivo}")
            if arquivo.is_dir():
                shutil.rmtree(arquivo)
            else:
                arquivo.unlink()
    
    # Confirma pasta _old (opcional)
    old_dir = root_dir / "_old"
    if old_dir.exists() and input(f"Remover pasta {old_dir}? (s/n): ").lower() == 's':
        print(f"Removendo pasta: {old_dir}")
        shutil.rmtree(old_dir)
    
    print("\n✅ Limpeza concluída!")

if __name__ == "__main__":
    limpar_projeto() 