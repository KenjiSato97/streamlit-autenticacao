import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from utils.auth import has_permission, check_authentication
from utils.data_manager import load_or_create_dataframes, calcular_desempenho
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Configurações da página
st.set_page_config(
    page_title="Dashboard - Sistema de Avaliação Escolar",
    page_icon="📊",
    layout="wide"
)

# Verificar autenticação
check_authentication()

def main():
    if not st.session_state.authenticated:
        st.warning("Você precisa fazer login para acessar esta página.")
        st.stop()
    
    if not has_permission("dashboard"):
        st.error("⛔ Acesso negado! Você não tem permissão para acessar esta página.")
        st.stop()
    
    # Título da página
    st.title("📊 Dashboard - Sistema de Avaliação Escolar")
    st.write("Análises e estatísticas do desempenho dos alunos nas avaliações.")
    
    # Carregar ou criar os dataframes
    with st.spinner("Carregando dados..."):
        dataframes = load_or_create_dataframes()
    
    df_aluno = dataframes['df_aluno']
    df_escola = dataframes['df_escola']
    df_prova = dataframes['df_prova']
    df_gabarito = dataframes['df_gabarito']
    
    # Calcular métricas de desempenho
    with st.spinner("Calculando desempenho..."):
        try:
            df_resultados = calcular_desempenho(df_prova, df_gabarito)
        except Exception as e:
            st.error(f"Erro ao calcular desempenho: {e}")
            st.stop()
    
    # Divisão do dashboard em abas
    tab1, tab2, tab3, tab4 = st.tabs(["Visão Geral", "Desempenho por Matéria", "Desempenho por Série", "Análises Específicas"])
    
    #--------------------------
    # TAB 1: VISÃO GERAL
    #--------------------------
    with tab1:
        # Visão geral - Métricas
        st.subheader("Métricas Gerais")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total de Alunos", len(df_aluno))
        with col2:
            st.metric("Total de Escolas", len(df_escola))
        with col3:
            st.metric("Total de Provas", len(df_prova))
        with col4:
            if not df_resultados.empty:
                nota_media = round(df_resultados['nota'].mean(), 2)
                st.metric("Nota Média Geral", f"{nota_media:.2f}")
            else:
                st.metric("Nota Média Geral", "N/A")
        
        # Distribuição de alunos por série
        st.subheader("Distribuição de alunos por série")
        fig, ax = plt.subplots(figsize=(10, 6))
        alunos_por_serie = df_aluno['serie'].value_counts().sort_index()
        sns.barplot(x=alunos_por_serie.index, y=alunos_por_serie.values, ax=ax)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)
        
        # Visualizações de distribuição
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Distribuição por Gênero")
            fig, ax = plt.subplots()
            genero_counts = df_aluno['genero'].value_counts()
            ax.pie(genero_counts, labels=genero_counts.index, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            st.pyplot(fig)
            
        with col2:
            st.subheader("Localização das Escolas")
            fig, ax = plt.subplots()
            localizacao_counts = df_aluno['localizacaoEscola'].value_counts()
            ax.pie(localizacao_counts, labels=localizacao_counts.index, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            st.pyplot(fig)
    
    #--------------------------
    # TAB 2: DESEMPENHO POR MATÉRIA
    #--------------------------
    with tab2:
        st.subheader("Desempenho por Matéria")
        
        if not df_resultados.empty:
            # Desempenho médio por matéria
            desempenho_por_materia = df_resultados.groupby('materia')['nota'].mean().sort_values(ascending=False)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=desempenho_por_materia.index, y=desempenho_por_materia.values, ax=ax)
            plt.xticks(rotation=45, ha='right')
            plt.ylabel('Nota Média')
            plt.tight_layout()
            st.pyplot(fig)
            
            # Filtro por matéria
            materia_selecionada = st.selectbox(
                "Selecione uma matéria para análise detalhada",
                sorted(df_resultados['materia'].unique())
            )
            
            # Análise detalhada da matéria selecionada
            st.subheader(f"Análise de {materia_selecionada}")
            
            # Filtrar dados para a matéria selecionada
            df_materia = df_resultados[df_resultados['materia'] == materia_selecionada]
            
            # Estatísticas descritivas
            col1, col2, col3 = st.columns(3)
            col1.metric("Nota Média", f"{df_materia['nota'].mean():.2f}")
            col2.metric("Nota Mínima", f"{df_materia['nota'].min():.2f}")
            col3.metric("Nota Máxima", f"{df_materia['nota'].max():.2f}")
            
            # Distribuição das notas
            st.write("Distribuição das notas")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(df_materia['nota'], bins=10, kde=True, ax=ax)
            plt.xlabel('Nota')
            plt.ylabel('Frequência')
            st.pyplot(fig)
            
            # Desempenho por série na matéria selecionada
            desempenho_por_serie = df_materia.groupby('serie')['nota'].mean().sort_index()
            
            st.write(f"Desempenho por série em {materia_selecionada}")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=desempenho_por_serie.index, y=desempenho_por_serie.values, ax=ax)
            plt.xticks(rotation=45, ha='right')
            plt.ylabel('Nota Média')
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("Não há dados de resultados disponíveis para análise.")
    
    #--------------------------
    # TAB 3: DESEMPENHO POR SÉRIE
    #--------------------------
    with tab3:
        st.subheader("Desempenho por Série")
        
        if not df_resultados.empty:
            # Desempenho médio por série
            desempenho_por_serie = df_resultados.groupby('serie')['nota'].mean().sort_index()
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=desempenho_por_serie.index, y=desempenho_por_serie.values, ax=ax)
            plt.xticks(rotation=45, ha='right')
            plt.ylabel('Nota Média')
            plt.tight_layout()
            st.pyplot(fig)
            
            # Filtro por série
            serie_selecionada = st.selectbox(
                "Selecione uma série para análise detalhada",
                sorted(df_resultados['serie'].unique())
            )
            
            # Análise detalhada da série selecionada
            st.subheader(f"Análise do {serie_selecionada}")
            
            # Filtrar dados para a série selecionada
            df_serie = df_resultados[df_resultados['serie'] == serie_selecionada]
            
            # Desempenho por matéria na série selecionada
            desempenho_por_materia = df_serie.groupby('materia')['nota'].mean().sort_values(ascending=False)
            
            st.write(f"Desempenho por matéria no {serie_selecionada}")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=desempenho_por_materia.index, y=desempenho_por_materia.values, ax=ax)
            plt.xticks(rotation=45, ha='right')
            plt.ylabel('Nota Média')
            plt.tight_layout()
            st.pyplot(fig)
            
            # Top 5 alunos da série
            st.write(f"Top 5 alunos com melhor desempenho no {serie_selecionada}")
            top_alunos = df_serie.groupby('nomeAluno')['nota'].mean().sort_values(ascending=False).head(5)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=top_alunos.index, y=top_alunos.values, ax=ax)
            plt.xticks(rotation=45, ha='right')
            plt.ylabel('Nota Média')
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("Não há dados de resultados disponíveis para análise.")
    
    #--------------------------
    # TAB 4: ANÁLISES ESPECÍFICAS
    #--------------------------
    with tab4:
        st.subheader("Análises Específicas")
        
        # Análise de alunos com laudos médicos
        if not df_resultados.empty and 'laudoMedico' in df_aluno.columns:
            st.write("Desempenho de Alunos com Laudos Médicos")
            
            # Mesclar resultados com dados de alunos para ter informação de laudo
            df_merged = df_resultados.merge(df_aluno[['id_aluno', 'laudoMedico']], on='id_aluno')
            
            # Agrupar por status de laudo e calcular média
            desempenho_por_laudo = df_merged.groupby('laudoMedico')['nota'].mean()
            
            # Criar dataframe para visualização
            df_laudo = pd.DataFrame({
                'Status': ['Com Laudo Médico', 'Sem Laudo Médico'],
                'Nota Média': [
                    desempenho_por_laudo.get(True, 0),
                    desempenho_por_laudo.get(False, 0)
                ]
            })
            
            # Plotar
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.barplot(x='Status', y='Nota Média', data=df_laudo, ax=ax)
            plt.ylim(0, 10)
            st.pyplot(fig)
            
            # Tabela de desempenho por laudo e matéria
            st.subheader("Desempenho por Matéria e Status de Laudo Médico")
            desempenho_detalhado = df_merged.groupby(['materia', 'laudoMedico'])['nota'].mean().reset_index()
            desempenho_detalhado['laudoMedico'] = desempenho_detalhado['laudoMedico'].map({True: 'Com Laudo', False: 'Sem Laudo'})
            desempenho_detalhado = desempenho_detalhado.pivot(index='materia', columns='laudoMedico', values='nota').reset_index()
            st.dataframe(desempenho_detalhado, use_container_width=True)
        
        # Tabela de resultados detalhados
        st.subheader("Resultados Detalhados")
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        with col1:
            materias = ['Todas'] + sorted(df_resultados['materia'].unique().tolist() if not df_resultados.empty else [])
            materia_selecionada = st.selectbox("Filtrar por Matéria", materias, key="materia_filter")
        
        with col2:
            series = ['Todas'] + sorted(df_resultados['serie'].unique().tolist() if not df_resultados.empty else [])
            serie_selecionada = st.selectbox("Filtrar por Série", series, key="serie_filter")
        
        with col3:
            ordem = st.selectbox("Ordenar por", ["Nota (maior para menor)", "Nota (menor para maior)"])
        
        # Aplicar filtros
        if not df_resultados.empty:
            df_filtrado = df_resultados.copy()
            
            if materia_selecionada != 'Todas':
                df_filtrado = df_filtrado[df_filtrado['materia'] == materia_selecionada]
            
            if serie_selecionada != 'Todas':
                df_filtrado = df_filtrado[df_filtrado['serie'] == serie_selecionada]
            
            # Ordenar
            if ordem == "Nota (maior para menor)":
                df_filtrado = df_filtrado.sort_values('nota', ascending=False)
            else:
                df_filtrado = df_filtrado.sort_values('nota', ascending=True)
            
            # Exibir tabela
            colunas_exibir = ['id_aluno', 'nomeAluno', 'serie', 'materia', 'acertos', 'total_questoes', 'nota']
            st.dataframe(df_filtrado[colunas_exibir], use_container_width=True)
            
            # Download dos dados em PDF

            def gerar_pdf(dataframe):
                buffer = BytesIO()
                pdf = canvas.Canvas(buffer, pagesize=letter)
                pdf.setFont("Helvetica", 10)
                width, height = letter
                x_offset, y_offset = 50, height - 50
                line_height = 15

                pdf.drawString(x_offset, y_offset, "Resultados Filtrados")
                y_offset -= 20

                colunas = dataframe.columns.tolist()
                pdf.drawString(x_offset, y_offset, " | ".join(colunas))
                y_offset -= line_height

                for _, row in dataframe.iterrows():
                    linha = " | ".join(str(row[col]) for col in colunas)
                    pdf.drawString(x_offset, y_offset, linha)
                    y_offset -= line_height
                    if y_offset < 50:  # Nova página se necessário
                        pdf.showPage()
                        pdf.setFont("Helvetica", 10)
                        y_offset = height - 50

                pdf.save()
                buffer.seek(0)
                return buffer

            if not df_filtrado.empty:
                pdf_buffer = gerar_pdf(df_filtrado[colunas_exibir])
                st.download_button(
                    label="📥 Baixar Dados Filtrados (PDF)",
                    data=pdf_buffer,
                    file_name="resultados_filtrados.pdf",
                    mime="application/pdf",
                )
        else:
            st.info("Nenhum resultado disponível para exibição.")

if __name__ == "__main__":
    main()