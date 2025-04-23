import streamlit as st
from utils.auth import has_permission, check_authentication

# Configurações da página
st.set_page_config(
    page_title="Configurações - App com Autenticação",
    page_icon="⚙️",
    layout="wide"
)

# Verificar autenticação
check_authentication()

def main():
    if not st.session_state.authenticated:
        st.warning("Você precisa fazer login para acessar esta página.")
        st.stop()
    
    if not has_permission("configuracoes"):
        st.error("⛔ Acesso negado! Você não tem permissão para acessar esta página.")
        st.stop()
    
    # Conteúdo da página
    st.title("⚙️ Configurações")
    st.write("Aqui você pode ajustar as configurações do sistema.")
    
    st.error("Esta página está disponível apenas para administradores.")
    
    # Conteúdo da página de configurações
    with st.form("config_form"):
        st.subheader("Configurações do Sistema")
        
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Gerar relatórios automáticos")
        
        with col2:
            st.selectbox("Frequência de relatórios", ["Diário", "Semanal", "Mensal"])
        
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Endereço de e-mail para notificações")
        with col2:
            st.selectbox("Formato de relatórios", ["PDF", "Excel", "CSV", "JSON"])
        
        submitted = st.form_submit_button("Salvar configurações")
        
        if submitted:
            st.success("Configurações salvas com sucesso!")

if __name__ == "__main__":
    main()