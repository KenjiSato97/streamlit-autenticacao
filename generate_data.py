import streamlit as st
from utils.data_manager import create_dataframes, save_dataframes

"""
Script para gerar os dataframes e salvar em arquivos.
Execute este script separadamente para gerar os dados antes de usar o aplicativo.

Comando: python generate_data.py
ou
Comando: streamlit run generate_data.py
"""

def main():
    st.title("Gerador de Dados - Sistema de Avaliação Escolar")
    
    st.write("""
    Este utilitário gera os dados necessários para o sistema de avaliação escolar.
    Os dados serão salvos na pasta 'data/' e estarão disponíveis para o aplicativo.
    """)
    
    if st.button("Gerar Dados", type="primary"):
        with st.spinner("Gerando dataframes..."):
            dataframes = create_dataframes()
            save_dataframes(dataframes)
        
        st.success("Dados gerados com sucesso!")
        
        # Mostrar informações sobre os dataframes gerados
        st.subheader("Resumo dos dados gerados:")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total de Alunos", len(dataframes['df_aluno']))
            st.metric("Total de Escolas", len(dataframes['df_escola']))
        
        with col2:
            st.metric("Total de Provas", len(dataframes['df_prova']))
            st.metric("Total de Gabaritos", len(dataframes['df_gabarito']))
        
        # Mostrar exemplos dos dataframes
        with st.expander("Visualizar amostras dos dados"):
            st.subheader("Alunos")
            st.dataframe(dataframes['df_aluno'].head())
            
            st.subheader("Escolas")
            st.dataframe(dataframes['df_escola'])
            
            st.subheader("Provas (amostra)")
            st.dataframe(dataframes['df_prova'].head())
            
            st.subheader("Gabaritos (amostra)")
            st.dataframe(dataframes['df_gabarito'].head())

if __name__ == "__main__":
    main()