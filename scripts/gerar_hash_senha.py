#!/usr/bin/env python3
"""
Script para gerar hash SHA-256 de senhas.
Útil para adicionar novos usuários ao sistema de autenticação.
"""

import hashlib
import getpass
import sys

def gerar_hash_senha(senha):
    """Gera o hash SHA-256 de uma senha"""
    return hashlib.sha256(senha.encode()).hexdigest()

def main():
    print("=== Gerador de Hash de Senha para Autenticação ===")
    print("Este script gera o hash SHA-256 de uma senha para uso no módulo de autenticação.")
    print()
    
    # Verificar se a senha foi fornecida como argumento de linha de comando
    if len(sys.argv) > 1:
        senha = sys.argv[1]
    else:
        # Solicitar a senha do usuário de forma segura (não exibida na tela)
        senha = getpass.getpass("Digite a senha para gerar o hash: ")
    
    if not senha:
        print("Erro: A senha não pode ser vazia.")
        return
    
    # Gerar o hash da senha
    hash_senha = gerar_hash_senha(senha)
    
    print("\nHash SHA-256 gerado:")
    print(hash_senha)
    print("\nUtilize este hash no dicionário USUARIOS no arquivo src/web/auth.py")
    print("Exemplo:")
    print(f'    "novo_usuario": "{hash_senha}",  # senha: {senha}')

if __name__ == "__main__":
    main() 