import streamlit as st

# Simula um banco de dados de usuários (em produção, use hashing adequado)
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "user"}
}

# Mapeamento de permissões por papel do usuário
ROLE_PERMISSIONS = {
    "admin": ["dashboard", "configuracoes", "usuarios"],
    "user": ["dashboard"]
}

def initialize_session_state():
    """Inicializa as variáveis de estado da sessão."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.role = None

def login(username, password):
    """Verifica credenciais e realiza login."""
    if username in USERS and USERS[username]["password"] == password:
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.role = USERS[username]["role"]
        return True
    return False

def logout():
    """Realiza logout do usuário."""
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.role = None
    # Recarregar a página para limpar completamente o estado
    st.rerun()

def has_permission(page_name):
    """Verifica se o usuário atual tem permissão para acessar uma página."""
    if not st.session_state.authenticated:
        return False
    
    # A página inicial está disponível para todos os usuários autenticados
    if page_name == "home":
        return True
    
    # Verificar permissões com base no papel do usuário
    return page_name in ROLE_PERMISSIONS.get(st.session_state.role, [])

def login_form():
    """Exibe o formulário de login."""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("🔒 Login")
        st.divider()
        
        with st.form("login_form"):
            username = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")
            submitted = st.form_submit_button("Entrar", use_container_width=True)
            
            if submitted:
                if login(username, password):
                    st.success("Login realizado com sucesso!")
                    st.rerun()  # Recarrega a página para mostrar o conteúdo autenticado
                else:
                    st.error("Usuário ou senha incorretos.")
        
        with st.expander("Usuários disponíveis para teste"):
            st.info("""
            - **Admin**: usuário: admin, senha: admin123
            - **Usuário comum**: usuário: user, senha: user123
            """)

def check_authentication():
    """
    Adiciona a barra lateral com informações do usuário e botão de logout
    quando o usuário está autenticado.
    """
    if st.session_state.authenticated:
        with st.sidebar:
            st.title(f"Bem-vindo, {st.session_state.username}!")
            st.caption(f"Nível: {st.session_state.role}")
            st.divider()
            
            if st.button("🚪 Logout", type="primary", use_container_width=True):
                logout()