import streamlit as st
import pandas as pd
from utils.auth import check_authentication, login_form, initialize_session_state
from utils.data_manager import load_or_create_dataframes

# Configurações da página
st.set_page_config(
    page_title="Sistema de Avaliação Escolar",
    page_icon="🔒",
    layout="wide"
)

# Inicializar o estado da sessão
initialize_session_state()

def main():
    # Verificar se o usuário está autenticado
    if not st.session_state.authenticated:
        login_form()
    else:
        # Se autenticado, mostra o conteúdo da página inicial
        st.title("📋 Sistema de Avaliação Escolar")
        st.write(f"Olá, {st.session_state.username}! Bem-vindo ao Sistema de Avaliação Escolar.")
        
        # Carregar dataframes
        with st.spinner("Carregando dados..."):
            try:
                dataframes = load_or_create_dataframes()
                df_aluno = dataframes['df_aluno']
                df_escola = dataframes['df_escola']
                
                # Mostrar visão geral dos dados
                col1, col2 = st.columns(2)
                
                with col1:
                    st.info(f"📊 Total de alunos cadastrados: **{len(df_aluno)}**")
                    st.info(f"🏫 Total de escolas cadastradas: **{len(df_escola)}**")
                
                # Exibir informações sobre navegação
                st.success("""
                ### Navegação do Sistema
                
                Utilize o menu lateral para acessar as diferentes funcionalidades:
                
                - **Dashboard**: Visualize estatísticas e gráficos sobre o desempenho dos alunos
                - **Configurações**: Ajuste as configurações do sistema (apenas administradores)
                - **Gerenciar Usuários**: Administre os usuários do sistema (apenas administradores)
                """)
                
                # Mostrar uma amostra dos dados
                with st.expander("Visualizar amostra dos dados"):
                    st.subheader("Alunos cadastrados (amostra)")
                    st.dataframe(df_aluno.head(10), use_container_width=True)
                    
                    st.subheader("Escolas cadastradas")
                    st.dataframe(df_escola, use_container_width=True)
                
            except Exception as e:
                st.error(f"Erro ao carregar os dados: {e}")
                st.info("Você pode gerar os dados utilizando o script 'generate_data.py'")

if __name__ == "__main__":
    # Verificar autenticação antes de mostrar qualquer conteúdo
    check_authentication()
    main()