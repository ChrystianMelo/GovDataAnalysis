import io
import pandas as pd
import json
import sqlite3
import os
import gdown
import streamlit as st

def downloadFile(file_path, url):
  if not (os.path.exists(file_path)):
      gdown.download(url, file_path, quiet=False)

def consulta_1(conn):
    query = """
    SELECT DISTINCT
    NOME_CURSO
    FROM
    GRADUACAO
    WHERE
    GRADUACAO.MODALIDADE = 'Educação a Distância'
    """
    
    df = pd.read_sql_query(query, conn)
    return df

def consulta_2(conn):
    query = """
    SELECT DISTINCT
      NOME_CURSO
    FROM
      GRADUACAO
    WHERE
      CARGA_HORARIA >= 4000
    """
    
    df = pd.read_sql_query(query, conn)
    return df

def consulta_3(conn):
    query = """
    SELECT DISTINCT NOME_INSTITUICAO
    FROM INSTITUICAO
    JOIN GRADUACAO ON GRADUACAO.CODIGO_IES = INSTITUICAO.CODIGO_INSTITUICAO
    JOIN ESPECIALIZACAO ON ESPECIALIZACAO.CODIGO_IES = INSTITUICAO.CODIGO_INSTITUICAO
    """
    
    df = pd.read_sql_query(query, conn)
    return df

def consulta_4(conn):
    query = """
    SELECT DISTINCT
      NOME_CURSO
    FROM
      GRADUACAO, INSTITUICAO, LOCAL_INSTITUICAO, MUNICIPIO
    WHERE
      GRADUACAO.COD_INSTITUICAO = LOCAL_INSTITUICAO.CODIGO_INSTITUICAO AND LOCAL_INSTITUICAO.CODIGO_MUNICIPIO = MUNICIPIO.CODIGO_MUNICIPIO
      AND MUNICIPIO.NOME_MUNICIPIO = 'Belo Horizonte'
    
    """
    
    df = pd.read_sql_query(query, conn)
    return df

def consulta_5(conn):
    query = """
    SELECT DISTINCT
      NOME_ESPECIALIZACAO
    FROM
      ESPECIALIZACAO, INSTITUICAO, LOCAL_INSTITUICAO, MUNICIPIO
    WHERE
      ESPECIALIZACAO.COD_INSTITUICAO = LOCAL_INSTITUICAO.CODIGO_INSTITUICAO AND LOCAL_INSTITUICAO.CODIGO_MUNICIPIO = MUNICIPIO.CODIGO_MUNICIPIO
      AND MUNICIPIO.NOME_MUNICIPIO = 'Belo Horizonte'
    """
    
    df = pd.read_sql_query(query, conn)
    return df


def consulta_6(conn):
    query = """
    SELECT DISTINCT
      NOME_INSTITUICAO
    FROM
      GRADUACAO, ESPECIALIZACAO, INSTITUICAO, LOCAL_INSTITUICAO, MUNICIPIO
    WHERE
      GRADUACAO.COD_INSTITUICAO = LOCAL_INSTITUICAO.CODIGO_INSTITUICAO AND ESPECIALIZACAO.COD_INSTITUICAO = LOCAL_INSTITUICAO.CODIGO_INSTITUICAO AND LOCAL_INSTITUICAO.CODIGO_MUNICIPIO = MUNICIPIO.CODIGO_MUNICIPIO
      AND MUNICIPIO.NOME_MUNICIPIO = 'Belo Horizonte' AND LOCAL_INSTITUICAO.CODIGO_INSTITUICAO = INSTITUICAO.COD_INSTITUICAO
    """
    
    df = pd.read_sql_query(query, conn)
    return df
    
def consulta_7(conn):
    query = """
    SELECT DISTINCT
      NOME_MUNICIPIO
    FROM
      GRADUACAO, ESPECIALIZACAO, LOCAL_INSTITUICAO, MUNICIPIO
    WHERE
      GRADUACAO.COD_INSTITUICAO = LOCAL_INSTITUICAO.CODIGO_INSTITUICAO AND ESPECIALIZACAO.COD_INSTITUICAO = LOCAL_INSTITUICAO.CODIGO_INSTITUICAO AND LOCAL_INSTITUICAO.CODIGO_MUNICIPIO = MUNICIPIO.CODIGO_MUNICIPIO
    """

    df = pd.read_sql_query(query, conn)
    return df

def consulta_8(conn):
    query = """
    SELECT DISTINCT
      NOME_CURSO
    FROM
      GRADUACAO, ESPECIALIZACAO, LOCAL_INSTITUICAO, MUNICIPIO
    WHERE
      (GRADUACAO.COD_INSTITUICAO = LOCAL_INSTITUICAO.CODIGO_INSTITUICAO OR ESPECIALIZACAO.COD_INSTITUICAO = LOCAL_INSTITUICAO.CODIGO_INSTITUICAO) AND LOCAL_INSTITUICAO.CODIGO_MUNICIPIO = MUNICIPIO.CODIGO_MUNICIPIO
      AND MUNICIPIO.UF = 'MG'
    """
    
    df = pd.read_sql_query(query, conn)
    return df
    
def consulta_9(conn):
    query = """
    SELECT DISTINCT
      QT_VAGAS_AUTORIZADAS
    FROM
      GRADUACAO, ESPECIALIZACAO, LOCAL_INSTITUICAO, MUNICIPIO
    WHERE
      (GRADUACAO.COD_INSTITUICAO = LOCAL_INSTITUICAO.CODIGO_INSTITUICAO OR ESPECIALIZACAO.COD_INSTITUICAO = LOCAL_INSTITUICAO.CODIGO_INSTITUICAO) AND LOCAL_INSTITUICAO.CODIGO_MUNICIPIO = MUNICIPIO.CODIGO_MUNICIPIO
      AND MUNICIPIO.UF = 'MG'
    GROUP BY
      GRADUACAO.QT_VAGAS_AUTORIZADAS, ESPECIALIZACAO.QT_VAGAS_AUTORIZADAS
    """
    
    df = pd.read_sql_query(query, conn)
    return df
    
def consulta_10(conn):
    query = """
    SELECT DISTINCT
      NOME_INSTITUICAO
    FROM
      GRADUACAO, ESPECIALIZACAO, INSTITUICAO
    WHERE
      GRADUACAO.COD_INSTITUICAO = INSTITUICAO.COD_INSTITUICAO OR ESPECIALIZACAO.COD_INSTITUICAO = INSTITUICAO.COD_INSTITUICAO
    ORDER BY
      GRADUACAO.QT_VAGAS_AUTORIZADAS, ESPECIALIZACAO.QT_VAGAS_AUTORIZADAS DESC
    """
    
    df = pd.read_sql_query(query, conn)
    return df
    

def show_table_info(conn):
    try:
        st.header('Informações das Tabelas Normalizadas')

        tables_query = "SELECT name FROM sqlite_master WHERE type='table'"
        tables_info = pd.read_sql_query(tables_query, conn)

        st.subheader('Informações das Tabelas')
        st.write(tables_info)
    
    except sqlite3.DatabaseError as e:
        st.error("Erro ao acessar o banco de dados:")
        st.error(e)

def show_views_info(conn):
    try:
        st.header('Informações das Views')

        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        for table in tables:
            st.subheader(f"Informações da Tabela: {table[0]}")

            cursor.execute(f"PRAGMA table_info({table[0]});")
            table_info = cursor.fetchall()

            columns = []
            for col in table_info:
                columns.append({
                    'Nome da Coluna': col[1],
                    'Tipo de Dado': col[2]
                })

            st.write(f"Colunas da Tabela {table[0]}:")
            st.write(columns)
    
    except sqlite3.DatabaseError as e:
        st.error("Erro ao acessar o banco de dados:")
        st.error(e)

def show_data_info():
    title_with_link = f'Informações sobre as Bases de Dados do [mec](https://dados.gov.br/dados/conjuntos-dados/indicadores-sobre-ensino-superior)'
    st.header(f"# {title_with_link}")

    st.subheader('Tabela de Graduação')
    st.write('Esta tabela contém informações sobre cursos de graduação.')

    grad_columns = [
        'CODIGO_IES', 'NOME_IES', 'CATEGORIA_ADMINISTRATIVA', 'ORGANIZACAO_ACADEMICA',
        'CODIGO_CURSO', 'NOME_CURSO', 'GRAU', 'AREA_OCDE', 'MODALIDADE', 'SITUACAO_CURSO',
        'QT_VAGAS_AUTORIZADAS', 'CARGA_HORARIA', 'CODIGO_AREA_OCDE_CINE', 'AREA_OCDE_CINE',
        'CODIGO_MUNICIPIO', 'MUNICIPIO', 'UF', 'REGIAO'
    ]
    st.write('Colunas:')
    st.write(grad_columns)

    st.subheader('Tabela de Especialização')
    st.write('Esta tabela contém informações sobre cursos de especialização.')

    esp_columns = [
        'CODIGO_IES', 'NOME_IES', 'COD_DA_ESPECIALIZACAO', 'NOME_ESPECIALIZACAO', 'CODIGO_OCDE_CINE',
        'OCDE_CINE', 'CARGA_HORARIA', 'DURACAO_MESES', 'MODALIDADE', 'VAGAS', 'CODIGO_MUNICIPIO',
        'MUNICIPIO', 'UF', 'REGIAO', 'SITUACAO'
    ]
    st.write('Colunas:')
    st.write(esp_columns)

def show_consultas(conn):
    st.header('Consultas')
    if st.button('Consulta 1 - Seleção de cursos de graduação a distância'):
        with st.spinner('Executando consulta...'):
            df_consulta_1 = consulta_1(conn)
            st.dataframe(df_consulta_1)
    
    if st.button('Consulta 2 - Cursos de Graduação com Carga Horária >= 4000 horas'):
        with st.spinner('Executando consulta...'):
            df_consulta_2 = consulta_2(conn)
            st.dataframe(df_consulta_2)
    
    if st.button('Consulta 3 - Instituições que ofertam cursos de graduação e especialização (**)'):
        with st.spinner('Executando consulta...'):
            df_consulta_3 = consulta_3(conn)
            st.dataframe(df_consulta_3)
    
    if st.button('Consulta 4 - Cursos de graduacao ofertados no municipio de Belo Horizonte'):
        with st.spinner('Executando consulta...'):
            df_consulta_4 = consulta_4(conn)
            st.dataframe(df_consulta_4)
    
    if st.button('Consulta 5 - Cursos de especialização ofertados no municipio de Belo Horizonte'):
        with st.spinner('Executando consulta...'):
            df_consulta_5 = consulta_5(conn)
            st.dataframe(df_consulta_5)
    
    if st.button('Consulta 6 - Instituicoes de ensino localizadas em Belo Horizonte que ofertam tanto cursos de graduacao quanto de especializacao'):
        with st.spinner('Executando consulta...'):
            df_consulta_6 = consulta_6(conn)
            st.dataframe(df_consulta_6)
    
    if st.button('Consulta 7 - Municipios que possuem instituicoes de ensino tanto de graduacao quanto de especializacao'):
        with st.spinner('Executando consulta...'):
            df_consulta_7 = consulta_7(conn)
            st.dataframe(df_consulta_7)
    
    if st.button('Consulta 8 - Curso de especializacao e de graduacao ofertados no estado de Minas Gerais'):
        with st.spinner('Executando consulta...'):
            df_consulta_8 = consulta_8(conn)
            st.dataframe(df_consulta_8)
            
    if st.button('Consulta 9 - Vagas totais de especializacao e graduacao em Minas Gerais'):
        with st.spinner('Executando consulta...'):
            df_consulta_9 = consulta_9(conn)
            st.dataframe(df_consulta_9)
            
    if st.button('Consulta 10 - Instituicoes ordenadas por numero de vagas de graduacao e especializacao'):
        with st.spinner('Executando consulta...'):
            df_consulta_10 = consulta_10(conn)
            st.dataframe(df_consulta_10)

file_path = "mecData.db" 
if (os.path.exists(file_path)):
    graduacao_path = "graduacao.csv"
    if not (os.path.exists(graduacao_path)):
        downloadFile(graduacao_path, "https://dadosabertos.mec.gov.br/images/conteudo/Ind-ensino-superior/2022//PDA_Dados_Cursos_Graduacao_Brasil.csv")
    graduacao =  pd.read_csv(graduacao_path)

    especializacao_path = "especializacao.csv"
    if not (os.path.exists(especializacao_path)):
        # O site do mec demora muito para carregar, então vou baixar a partir do meu driver pessoal.
        #downloadFile(especializacao_path, "https://olinda.mec.gov.br/olinda-ide/servico/PDA_SERES/versao/v1/odata/PDA_Cursos_Especializacao_Brasil?$format=text/csv")
        downloadFile("especializacao.csv", "https://drive.google.com/uc?id=15Mgq9U3C6775p5AoLdKBmP1-AmiC24_0")
    especializacao = pd.read_csv(especializacao_path)
    
    conn = sqlite3.connect(file_path)

    graduacao.to_sql('Graduacao', conn, if_exists='replace', index=False)
    especializacao.to_sql('Especializacao', conn, if_exists='replace', index=False)

    """## Normalização 1"""

    cursor = conn.cursor()

    query = """
    SELECT DISTINCT
      CODIGO_AREA_OCDE_CINE AS CODIGO_AREA_CONHECIMENTO, AREA_OCDE_CINE AS NOME_AREA_CONHECIMENTO
    FROM
      graduacao
    GROUP BY CODIGO_AREA_CONHECIMENTO
    UNION
    SELECT DISTINCT
      CODIGO_OCDE_CINE AS CODIGO_AREA_CONHECIMENTO, OCDE_CINE AS NOME_AREA_CONHECIMENTO
    FROM
      especializacao
    GROUP BY CODIGO_AREA_CONHECIMENTO
    """
    df = pd.read_sql_query(query, conn)
    df.to_sql('Tematica', conn, if_exists='replace', index=False)

    cursor.execute("ALTER TABLE graduacao DROP COLUMN AREA_OCDE_CINE;")
    cursor.execute("ALTER TABLE graduacao DROP COLUMN AREA_OCDE;") #coluna com dado duplicado

    cursor.execute("ALTER TABLE especializacao DROP COLUMN OCDE_CINE;")

    conn.commit()

    print (df)

    query = """
    SELECT DISTINCT
      CODIGO_MUNICIPIO, MUNICIPIO AS NOME_MUNICIPIO, UF, REGIAO
    FROM
      graduacao
    UNION
    SELECT DISTINCT
      CODIGO_MUNICIPIO, MUNICIPIO AS NOME_MUNICIPIO, UF, REGIAO
    FROM
      especializacao
    """

    df = pd.read_sql_query(query, conn)
    df.to_sql('Municipio', conn, if_exists='replace', index=False)

    cursor.execute("ALTER TABLE graduacao DROP COLUMN MUNICIPIO;")
    cursor.execute("ALTER TABLE graduacao DROP COLUMN UF;")
    cursor.execute("ALTER TABLE graduacao DROP COLUMN REGIAO;")

    cursor.execute("ALTER TABLE especializacao DROP COLUMN MUNICIPIO;")
    cursor.execute("ALTER TABLE especializacao DROP COLUMN UF;")
    cursor.execute("ALTER TABLE especializacao DROP COLUMN REGIAO;")

    conn.commit()

    print (df)

    query = """
    SELECT DISTINCT
      CODIGO_IES AS CODIGO_INSTITUICAO, NOME_IES AS NOME_INSTITUICAO
    FROM
      graduacao
    UNION
    SELECT DISTINCT
      CODIGO_IES AS CODIGO_INSTITUICAO, NOME_IES AS NOME_INSTITUICAO
    FROM
      especializacao
    """

    df = pd.read_sql_query(query, conn)
    df.to_sql('Instituicao', conn, if_exists='replace', index=False)

    cursor.execute("ALTER TABLE graduacao DROP COLUMN NOME_IES;")
    cursor.execute("ALTER TABLE graduacao DROP COLUMN CATEGORIA_ADMINISTRATIVA;")
    cursor.execute("ALTER TABLE graduacao DROP COLUMN ORGANIZACAO_ACADEMICA;")

    cursor.execute("ALTER TABLE especializacao DROP COLUMN NOME_IES;")

    conn.commit()

    print (df)

    query = """
    SELECT DISTINCT
      CODIGO_IES AS CODIGO_INSTITUICAO, CODIGO_MUNICIPIO
    FROM
      graduacao
    UNION
    SELECT DISTINCT
      CODIGO_IES AS CODIGO_INSTITUICAO, CODIGO_MUNICIPIO
    FROM
      especializacao
    """

    df = pd.read_sql_query(query, conn)
    df.to_sql('Local_Instituicao', conn, if_exists='replace', index=False)

    cursor.execute("ALTER TABLE graduacao DROP COLUMN CODIGO_MUNICIPIO;")
    cursor.execute("ALTER TABLE especializacao DROP COLUMN CODIGO_MUNICIPIO;")

    conn.commit()

    print (df)

    cursor.execute("ALTER TABLE Graduacao RENAME COLUMN CODIGO_IES TO COD_INSTITUICAO;")

    cursor.execute("ALTER TABLE Especializacao RENAME COLUMN CODIGO_IES TO COD_INSTITUICAO;")

    cursor.execute("ALTER TABLE Especializacao RENAME COLUMN CODIGO_OCDE_CINE TO COD_AREA_CONHECIMENTO;")

    cursor.execute("ALTER TABLE Graduacao RENAME COLUMN CODIGO_AREA_OCDE_CINE TO COD_AREA_CONHECIMENTO;")

    cursor.execute("ALTER TABLE Instituicao RENAME COLUMN CODIGO_INSTITUICAO TO COD_INSTITUICAO;")

    conn.commit()

    """## Normalização 2"""

    # Criar a tabela Graduacao com as chaves primária e estrangeiras
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Graduacao_new (
            COD_INSTITUICAO INTEGER,
            CODIGO_CURSO INTEGER,
            NOME_CURSO TEXT,
            GRAU TEXT,
            MODALIDADE TEXT,
            SITUACAO_CURSO TEXT,
            QT_VAGAS_AUTORIZADAS INTEGER,
            CARGA_HORARIA INTEGER,
            COD_AREA_CONHECIMENTO TEXT,
            PRIMARY KEY (CODIGO_CURSO),
            FOREIGN KEY (COD_INSTITUICAO) REFERENCES Instituicao(COD_INSTITUICAO),
            FOREIGN KEY (COD_AREA_CONHECIMENTO) REFERENCES Tematica(CODIGO_AREA_CONHECIMENTO)
        )
    ''')

    # Copiar dados da tabela Graduacao, IGNORANDO DUPLICATAS
    cursor.execute('''
        INSERT INTO Graduacao_new
        SELECT DISTINCT COD_INSTITUICAO, CODIGO_CURSO, NOME_CURSO, GRAU, MODALIDADE,
               SITUACAO_CURSO, QT_VAGAS_AUTORIZADAS, CARGA_HORARIA, COD_AREA_CONHECIMENTO
        FROM Graduacao
    ''')

    conn.commit()

    # Criar a tabela Especializacao com chaves primária e estrangeiras
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Especializacao_new (
            COD_INSTITUICAO INTEGER,
            COD_DA_ESPECIALIZACAO INTEGER,
            NOME_ESPECIALIZACAO TEXT,
            COD_AREA_CONHECIMENTO REAL,
            CARGA_HORARIA INTEGER,
            DURACAO_MESES INTEGER,
            MODALIDADE TEXT,
            VAGAS INTEGER,
            SITUACAO TEXT,
            PRIMARY KEY (COD_DA_ESPECIALIZACAO),
            FOREIGN KEY (COD_INSTITUICAO) REFERENCES Instituicao(COD_INSTITUICAO),
            FOREIGN KEY (COD_AREA_CONHECIMENTO) REFERENCES Tematica(CODIGO_AREA_CONHECIMENTO)
        )
    ''')

    # Copiar dados da tabela Especializacao, IGNORANDO DUPLICATAS
    cursor.execute('''
        INSERT INTO Especializacao_new
        SELECT DISTINCT COD_INSTITUICAO, COD_DA_ESPECIALIZACAO, NOME_ESPECIALIZACAO,
               COD_AREA_CONHECIMENTO, CARGA_HORARIA, DURACAO_MESES, MODALIDADE, VAGAS, SITUACAO
        FROM Especializacao
    ''')
    conn.commit()

    # Criar a tabela Tematica com chave primária
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Tematica_new (
            CODIGO_AREA_CONHECIMENTO TEXT PRIMARY KEY,
            NOME_AREA_CONHECIMENTO TEXT
        )
    ''')

    # Copiar dados da tabela Tematica
    cursor.execute('''
        INSERT INTO Tematica_new
        SELECT DISTINCT CODIGO_AREA_CONHECIMENTO, NOME_AREA_CONHECIMENTO
        FROM Tematica
    ''')
    conn.commit()

    # Criar a tabela Municipio com chave primária
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Municipio_new (
            CODIGO_MUNICIPIO INTEGER PRIMARY KEY,
            NOME_MUNICIPIO TEXT,
            UF TEXT,
            REGIAO TEXT
        )
    ''')

    # Copiar dados da tabela Municipio, IGNORANDO DUPLICATAS
    cursor.execute('''
        INSERT INTO Municipio_new
        SELECT DISTINCT CODIGO_MUNICIPIO, NOME_MUNICIPIO, UF, REGIAO
        FROM Municipio
    ''')
    conn.commit()

    # Criar a tabela Instituicao com chave primária
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Instituicao_new (
            COD_INSTITUICAO INTEGER PRIMARY KEY,
            NOME_INSTITUICAO TEXT
        )
    ''')

    # Copiar dados da tabela Instituicao, mantendo um único registro para cada COD_INSTITUICAO
    cursor.execute('''
        INSERT INTO Instituicao_new
        SELECT COD_INSTITUICAO, MAX(NOME_INSTITUICAO)
        FROM Instituicao
        GROUP BY COD_INSTITUICAO
    ''')

    conn.commit()

    # Criar a tabela Local_Instituicao com chaves primária e estrangeiras
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Local_Instituicao_new (
            CODIGO_INSTITUICAO INTEGER,
            CODIGO_MUNICIPIO INTEGER,
            PRIMARY KEY (CODIGO_INSTITUICAO, CODIGO_MUNICIPIO),
            FOREIGN KEY (CODIGO_INSTITUICAO) REFERENCES Instituicao(COD_INSTITUICAO),
            FOREIGN KEY (CODIGO_MUNICIPIO) REFERENCES Municipio(CODIGO_MUNICIPIO)
        )
    ''')

    # Copiar dados da tabela Local_Instituicao, IGNORANDO DUPLICATAS
    cursor.execute('''
        INSERT INTO Local_Instituicao_new
        SELECT DISTINCT CODIGO_INSTITUICAO, CODIGO_MUNICIPIO
        FROM Local_Instituicao
    ''')

    conn.commit()

    # Excluir as tabelas antigas
    cursor.execute('DROP TABLE IF EXISTS Graduacao')
    cursor.execute('DROP TABLE IF EXISTS Especializacao')
    cursor.execute('DROP TABLE IF EXISTS Tematica')
    cursor.execute('DROP TABLE IF EXISTS Municipio')
    cursor.execute('DROP TABLE IF EXISTS Instituicao')
    cursor.execute('DROP TABLE IF EXISTS Local_Instituicao')

    # Renomear as novas tabelas para os nomes originais
    cursor.execute('ALTER TABLE Graduacao_new RENAME TO Graduacao')
    cursor.execute('ALTER TABLE Especializacao_new RENAME TO Especializacao')
    cursor.execute('ALTER TABLE Tematica_new RENAME TO Tematica')
    cursor.execute('ALTER TABLE Municipio_new RENAME TO Municipio')
    cursor.execute('ALTER TABLE Instituicao_new RENAME TO Instituicao')
    cursor.execute('ALTER TABLE Local_Instituicao_new RENAME TO Local_Instituicao')

    # Commitar as mudanças
    conn.commit()
else:
    conn = sqlite3.connect(file_path)

st.title('Indicadores sobre Ensino Superior')

show_data_info()

show_table_info(conn)

show_views_info(conn)

show_consultas(conn)
