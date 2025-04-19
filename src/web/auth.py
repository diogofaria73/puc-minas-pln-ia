"""
Módulo para autenticação de usuários na aplicação Streamlit.
Implementa um sistema simplificado de login.
"""

import streamlit as st
import hashlib
import hmac

# Usuários predefinidos (normalmente seriam armazenados em um banco de dados)
# Formato: "nome_usuario": "hash_da_senha"
USUARIOS = {
    "admin": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",  # senha: admin
    "usuario": "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4",  # senha: 1234
    "convidado": "b5fb68ea44b948a4834105c09297cd31a3aaa80b63b8bfdec6ac2e6dbcfb3a00"  # senha: guest
}

def calcular_hash_senha(senha):
    """Calcula o hash SHA-256 de uma senha."""
    return hashlib.sha256(senha.encode()).hexdigest()

def verificar_senha(usuario, senha):
    """Verifica se a senha está correta para o usuário."""
    if usuario not in USUARIOS:
        return False
    
    hash_senha_correto = USUARIOS[usuario]
    hash_senha_fornecido = calcular_hash_senha(senha)
    
    return hmac.compare_digest(hash_senha_correto, hash_senha_fornecido)

def gerar_cookie_auth(usuario):
    """Gera um cookie de autenticação para o usuário."""
    return hashlib.sha256(f"{usuario}:autenticado".encode()).hexdigest()

def autenticar_usuario(usuario, senha):
    """Autentica um usuário e configura o estado da sessão."""
    if verificar_senha(usuario, senha):
        # Configurar o estado de autenticação
        st.session_state.autenticado = True
        st.session_state.usuario = usuario
        st.session_state.token_auth = gerar_cookie_auth(usuario)
        return True
    return False

def logout():
    """Desconecta o usuário."""
    for key in ['autenticado', 'usuario', 'token_auth']:
        if key in st.session_state:
            del st.session_state[key]

def verificar_autenticacao():
    """Verifica se o usuário está autenticado."""
    return st.session_state.get('autenticado', False)

def obter_usuario_atual():
    """Retorna o nome do usuário autenticado."""
    return st.session_state.get('usuario', None)

def pagina_login():
    """Renderiza a página de login."""
    st.title("🔐 Login")
    
    # Verificar se já está autenticado
    if verificar_autenticacao():
        st.success(f"Você já está conectado como {obter_usuario_atual()}")
        
        if st.button("Sair"):
            logout()
            st.experimental_rerun()
            
        return True
    
    # Formulário de login
    with st.form("login_form"):
        st.subheader("Entre com suas credenciais")
        
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            submit = st.form_submit_button("Login")
        
    # Verificação de login
    if submit:
        if usuario and senha:
            if autenticar_usuario(usuario, senha):
                st.success("Login realizado com sucesso!")
                # Recarregar a página imediatamente após o login bem-sucedido
                st.experimental_rerun()
                return True
            else:
                st.error("Usuário ou senha incorretos!")
        else:
            st.warning("Por favor, preencha todos os campos.")
    
    
    return False 