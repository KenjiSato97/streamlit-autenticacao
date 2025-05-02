import pandas as pd
import numpy as np
import random
import os

def create_dataframes():
    """
    Cria e retorna os dataframes necessários para o sistema de avaliação escolar:
    - df_aluno: Informações dos alunos
    - df_escola: Cadastro de escolas
    - df_prova: Registros de provas realizadas pelos alunos
    - df_gabarito: Gabaritos das provas por série/matéria
    """
    
    # Criação do df_escola (fazemos primeiro para referenciar nas outras tabelas)
    escolas = [
        {"id_escola": 1, "nomeEscola": "Escola Municipal Paulo Freire", 
         "endereco": "Rua das Flores, 123", "telefone": "(11) 3456-7890", "email": "paulofreire@edu.com"},
        {"id_escola": 2, "nomeEscola": "Colégio Estadual Machado de Assis", 
         "endereco": "Av. Principal, 456", "telefone": "(11) 2345-6789", "email": "machadodeassis@edu.com"},
        {"id_escola": 3, "nomeEscola": "Instituto Educacional Monteiro Lobato", 
         "endereco": "Rua dos Pinheiros, 789", "telefone": "(11) 3456-5678", "email": "monteirolobato@edu.com"},
        {"id_escola": 4, "nomeEscola": "Escola Técnica Santos Dumont", 
         "endereco": "Praça Central, 101", "telefone": "(11) 4567-8901", "email": "santosdumont@edu.com"},
        {"id_escola": 5, "nomeEscola": "Centro Educacional Cecília Meireles", 
         "endereco": "Alameda das Acácias, 202", "telefone": "(11) 5678-9012", "email": "ceciliameireles@edu.com"}
    ]
    df_escola = pd.DataFrame(escolas)
    
    # Criação do df_aluno
    alunos = []
    series = ['1º ano', '2º ano', '3º ano', '4º ano', '5º ano', '6º ano', '7º ano', '8º ano', '9º ano',
              '1º ano médio', '2º ano médio', '3º ano médio']
    generos = ['Masculino', 'Feminino']
    localizacoes = ['Urbana', 'Rural']
    
    for i in range(1, 101):  # Criar 100 alunos
        id_escola = random.randint(1, 5)
        escola_info = next(escola for escola in escolas if escola["id_escola"] == id_escola)
        
        aluno = {
            "id_aluno": i,
            "nomeAluno": f"Aluno {i}",
            "dataNascimento": f"{random.randint(2010, 2016)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            "genero": random.choice(generos),
            "serie": random.choice(series),
            "nomeEscola": escola_info["nomeEscola"],
            "localizacaoEscola": random.choice(localizacoes),
            "laudoMedico": random.choice([True, False, False, False])  # 25% de chance de ter laudo
        }
        alunos.append(aluno)
    
    df_aluno = pd.DataFrame(alunos)
    
    # Criação do df_prova
    provas = []
    materias = [
        "Português", "Inglês", "Arte", "Educação Física", "Espanhol",
        "Matemática", "História", "Geografia", "Ciências", "Religião"
    ]
    
    for aluno in alunos:
        # Cada aluno faz 1 prova de cada matéria
        for materia in materias:
            prova = {
            "id_prova": len(provas) + 1,
            "id_aluno": aluno["id_aluno"],
            "nomeAluno": aluno["nomeAluno"],
            "materia": materia,
            "serie": aluno["serie"]
            }
            # Adicionar respostas às questões (de 1 a 10)
            for i in range(1, 11):
                prova[f"questao_{i}"] = random.choice(['A', 'B'])
            
            provas.append(prova)
    
    df_prova = pd.DataFrame(provas)
    
    # Criação do df_gabarito
    gabaritos = []
    
    # Um gabarito para cada combinação de série e matéria
    for serie in series:
        for materia in materias:
            gabarito = {
                "id_gabarito": len(gabaritos) + 1,
                "serie": serie,
                "materia": materia
            }
            
            # Definir respostas corretas para as questões de 1 a 10
            for i in range(1, 11):
                gabarito[f"questao_{i}"] = random.choice(['A', 'B'])
            
            gabaritos.append(gabarito)
    
    df_gabarito = pd.DataFrame(gabaritos)
    
    return {
        'df_aluno': df_aluno,
        'df_escola': df_escola,
        'df_prova': df_prova,
        'df_gabarito': df_gabarito
    }

def load_or_create_dataframes():
    """
    Tenta carregar os dataframes de arquivos existentes,
    se não existirem, cria novos dataframes.
    """
    try:
        df_aluno = pd.read_parquet('data/df_aluno.parquet')
        df_escola = pd.read_parquet('data/df_escola.parquet')
        df_prova = pd.read_parquet('data/df_prova.parquet')
        df_gabarito = pd.read_parquet('data/df_gabarito.parquet')
        
        return {
            'df_aluno': df_aluno,
            'df_escola': df_escola,
            'df_prova': df_prova,
            'df_gabarito': df_gabarito
        }
    
    except (FileNotFoundError, Exception):
        # Se os arquivos não existirem, cria novos dataframes
        dataframes = create_dataframes()
        # Salva os dataframes
        save_dataframes(dataframes)
        return dataframes

def save_dataframes(dataframes):
    """
    Salva os dataframes em arquivos parquet para uso futuro.
    
    Args:
        dataframes (dict): Dicionário contendo os dataframes
    """
    import os
    
    # Criar pasta data se não existir
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Salvar cada dataframe
    for name, df in dataframes.items():
        df.to_parquet(f'data/{name}.parquet')
    
    print("Dataframes salvos com sucesso!")

def calcular_desempenho(df_prova, df_gabarito):
    """
    Calcula o desempenho dos alunos com base nas respostas e gabaritos
    
    Args:
        df_prova: DataFrame com as respostas dos alunos
        df_gabarito: DataFrame com as respostas corretas
        
    Returns:
        DataFrame com os resultados calculados
    """
    # Criar dataframe para armazenar os resultados
    resultados = []
    
    # Iterar sobre as provas
    for _, prova in df_prova.iterrows():
        # Encontrar o gabarito correspondente
        gabarito = df_gabarito[(df_gabarito['serie'] == prova['serie']) & 
                              (df_gabarito['materia'] == prova['materia'])]
        
        if len(gabarito) == 0:
            continue
            
        gabarito = gabarito.iloc[0]
        
        # Calcular acertos
        acertos = 0
        total_questoes = 0
        
        for i in range(1, 11):
            coluna_questao = f'questao_{i}'
            if coluna_questao in prova and coluna_questao in gabarito:
                total_questoes += 1
                if prova[coluna_questao] == gabarito[coluna_questao]:
                    acertos += 1
        
        # Calcular a nota (0 a 10)
        if total_questoes > 0:
            nota = (acertos / total_questoes) * 10
        else:
            nota = 0
            
        # Adicionar aos resultados
        resultado = {
            'id_prova': prova['id_prova'],
            'id_aluno': prova['id_aluno'],
            'nomeAluno': prova['nomeAluno'],
            'materia': prova['materia'],
            'serie': prova['serie'],
            'acertos': acertos,
            'total_questoes': total_questoes,
            'nota': nota
        }
        resultados.append(resultado)
    
    return pd.DataFrame(resultados)