import streamlit as st
import pandas as pd
from utils.auth import has_permission, check_authentication

# Configurações da página
st.set_page_config(
    page_title="Gerenciar Usuários - App com Autenticação",
    page_icon="👥",
    layout="wide"
)

# Verificar autenticação
check_authentication()

def main():
    if not st.session_state.authenticated:
        st.warning("Você precisa fazer login para acessar esta página.")
        st.stop()
    
    if not has_permission("usuarios"):
        st.error("⛔ Acesso negado! Você não tem permissão para acessar esta página.")
        st.stop()
    
    # Conteúdo da página
    st.title("👥 Gerenciar Usuários")
    st.write("Gerencie os usuários do sistema.")
    
    st.error("Esta página está disponível apenas para administradores.")
    
    # Tabela de usuários
    df_usuarios = pd.DataFrame([
        {"ID": 1, "Nome": "Admin", "Usuário": "admin", "Nível": "admin", "Último acesso": "23/04/2025 10:45"},
        {"ID": 2, "Nome": "João Silva", "Usuário": "user", "Nível": "user", "Último acesso": "22/04/2025 15:33"},
    ])
    
    st.dataframe(df_usuarios, use_container_width=True)
    
    # Tabs para diferentes operações
    tab1, tab2, tab3 = st.tabs(["Adicionar usuário", "Editar usuário", "Excluir usuário"])
    
    with tab1:
        st.subheader("Adicionar novo usuário")
        with st.form("form_add_usuario"):
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Nome completo")
                st.text_input("Nome de usuário")
            with col2:
                st.text_input("Senha", type="password")
                st.selectbox("Nível de acesso", ["user", "admin"])
            
            submitted = st.form_submit_button("Adicionar usuário")
            if submitted:
                st.success("Usuário adicionado com sucesso! (simulação)")
    
    with tab2:
        st.subheader("Editar usuário existente")
        usuario_para_editar = st.selectbox("Selecione o usuário para editar", ["admin", "user"])
        
        with st.form("form_edit_usuario"):
            st.text_input("Novo nome", value="Nome atual")
            st.selectbox("Novo nível", ["user", "admin"])
            st.text_input("Nova senha", type="password")
            
            submitted = st.form_submit_button("Salvar alterações")
            if submitted:
                st.success(f"Alterações no usuário {usuario_para_editar} salvas com sucesso! (simulação)")
    
    with tab3:
        st.subheader("Excluir usuário")
        st.warning("⚠️ Esta operação não pode ser desfeita!")
        
        usuario_para_excluir = st.selectbox("Selecione o usuário para excluir", ["user"])
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Excluir usuário", type="primary"):
                st.error(f"Usuário {usuario_para_excluir} excluído com sucesso! (simulação)")
        with col2:
            st.button("Cancelar")

if __name__ == "__main__":
    main()
