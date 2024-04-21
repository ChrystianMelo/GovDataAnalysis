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
    JOIN GRADUACAO ON GRADUACAO.COD_INSTITUICAO = INSTITUICAO.COD_INSTITUICAO
    JOIN ESPECIALIZACAO ON ESPECIALIZACAO.COD_INSTITUICAO = INSTITUICAO.COD_INSTITUICAO
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
#if not (os.path.exists(file_path)):
if (1==1):
    downloadFile("graduacao.csv", "https://dadosabertos.mec.gov.br/images/conteudo/Ind-ensino-superior/2022//PDA_Dados_Cursos_Graduacao_Brasil.csv")
    graduacao =  pd.read_csv("graduacao.csv")

    # O site do mec demora muito para carregar, então vou baixar a partir do meu driver pessoal.
    #downloadFile("especializacao.csv", "https://olinda.mec.gov.br/olinda-ide/servico/PDA_SERES/versao/v1/odata/PDA_Cursos_Especializacao_Brasil?$format=text/csv")
    downloadFile("especializacao.csv", "https://drive.usercontent.google.com/download?id=15Mgq9U3C6775p5AoLdKBmP1-AmiC24_0&export=download&authuser=2&confirm=t&uuid=0ac2db66-0856-42bf-95e1-aa784e7e81c3&at=APZUnTVkI1R4coEJVVDmKx9zBIRW:1700768753058")
    especializacao = pd.read_csv("especializacao.csv")
    
    conn = sqlite3.connect(file_path)

    graduacao.to_sql('Graduacao', conn, if_exists='replace', index=False)
    especializacao.to_sql('Especializacao', conn, if_exists='replace', index=False)

    # Normalização
    cursor = conn.cursor()

    query = """
    SELECT DISTINCT
      CODIGO_AREA_OCDE_CINE AS CODIGO_AREA_CONHECIMENTO, AREA_OCDE_CINE AS NOME_AREA_CONHECIMENTO
    FROM
      Graduacao
    GROUP BY CODIGO_AREA_CONHECIMENTO
    UNION
    SELECT DISTINCT
      CODIGO_OCDE_CINE AS CODIGO_AREA_CONHECIMENTO, OCDE_CINE AS NOME_AREA_CONHECIMENTO
    FROM
      Especializacao
    GROUP BY CODIGO_AREA_CONHECIMENTO
    """
    df = pd.read_sql_query(query, conn)
    df.to_sql('Tematica', conn, if_exists='replace', index=False)
    
    # Adding primary key to Tematica table
    cursor.execute("CREATE UNIQUE INDEX idx_codigo_area_conhecimento ON Tematica (CODIGO_AREA_CONHECIMENTO)")

    conn.commit()
    st.title('10%')

    query = """
    SELECT DISTINCT
      CODIGO_MUNICIPIO, MUNICIPIO AS NOME_MUNICIPIO, UF, REGIAO
    FROM
      Graduacao
    UNION
    SELECT DISTINCT
      CODIGO_MUNICIPIO, MUNICIPIO AS NOME_MUNICIPIO, UF, REGIAO
    FROM
      Especializacao
    """
    df = pd.read_sql_query(query, conn)
    df.to_sql('Municipio', conn, if_exists='replace', index=False)

    # Adding primary key to Municipio table
    cursor.execute("CREATE UNIQUE INDEX idx_codigo_municipio ON Municipio (CODIGO_MUNICIPIO)")

    conn.commit()
    st.title('30%')

    query = """
    SELECT DISTINCT
      CODIGO_IES AS CODIGO_INSTITUICAO, NOME_IES AS NOME_INSTITUICAO
    FROM
      Graduacao
    UNION
    SELECT DISTINCT
      CODIGO_IES AS CODIGO_INSTITUICAO, NOME_IES AS NOME_INSTITUICAO
    FROM
      Especializacao
    """
    df = pd.read_sql_query(query, conn)
    df.to_sql('Instituicao', conn, if_exists='replace', index=False)
    
    # Verificar duplicatas na coluna CODIGO_INSTITUICAO
    cursor.execute("""
        SELECT CODIGO_INSTITUICAO, COUNT(*)
        FROM Instituicao
        GROUP BY CODIGO_INSTITUICAO
        HAVING COUNT(*) > 1
    """)
    duplicates = cursor.fetchall()
    if duplicates:
        print("Duplicatas encontradas!")        
        # Remover duplicatas
        for duplicate in duplicates:
            codigo = duplicate[0]
            cursor.execute("DELETE FROM Instituicao WHERE rowid NOT IN (SELECT MIN(rowid) FROM Instituicao WHERE CODIGO_INSTITUICAO = ?)", (codigo,))
        print("Duplicatas removidas.")

    # Adding primary key to Municipio table
    cursor.execute("CREATE UNIQUE INDEX idx_codigo_instituicao ON Instituicao (CODIGO_INSTITUICAO)")

    conn.commit()
    st.title('50%')

    query = """
    SELECT DISTINCT
      CODIGO_IES AS CODIGO_INSTITUICAO, CODIGO_MUNICIPIO
    FROM
      Graduacao
    UNION
    SELECT DISTINCT
      CODIGO_IES AS CODIGO_INSTITUICAO, CODIGO_MUNICIPIO
    FROM
      Especializacao
    """
    df = pd.read_sql_query(query, conn)
    df.to_sql('Local_Instituicao', conn, if_exists='replace', index=False)
    
    # Adding foreign key constraints to Local_Instituicao table
    cursor.execute("""
    CREATE UNIQUE INDEX idx_local_instituicao ON Local_Instituicao (CODIGO_INSTITUICAO, CODIGO_MUNICIPIO);
    """)

    st.title('70%')

    cursor.execute("""
    CREATE INDEX idx_fk_instituicao ON Local_Instituicao (CODIGO_INSTITUICAO);
    """)

    st.title('75%')

    cursor.execute("""
    CREATE INDEX idx_fk_municipio ON Local_Instituicao (CODIGO_MUNICIPIO);
    """)

    st.title('80%')

    # Verificar duplicatas na coluna CODIGO_INSTITUICAO
    cursor.execute("""
        SELECT CODIGO_INSTITUICAO, COUNT(*)
        FROM Local_Instituicao
        GROUP BY CODIGO_INSTITUICAO
        HAVING COUNT(*) > 1
    """)
    duplicates = cursor.fetchall()
    if duplicates:
        print("Duplicatas encontradas!")        
        # Remover duplicatas
        for duplicate in duplicates:
            codigo = duplicate[0]
            cursor.execute("DELETE FROM Local_Instituicao WHERE rowid NOT IN (SELECT MIN(rowid) FROM Local_Instituicao WHERE CODIGO_INSTITUICAO = ?)", (codigo,))
        print("Duplicatas removidas.")

    cursor.execute("""
    CREATE UNIQUE INDEX idx_local_instituicao_fk_instituicao ON Local_Instituicao (CODIGO_INSTITUICAO);
    """)

    st.title('85%')
    cursor.execute("""
    CREATE UNIQUE INDEX idx_local_instituicao_fk_municipio ON Local_Instituicao (CODIGO_MUNICIPIO);
    """)

    st.title('90%')

    conn.commit()
    st.title('95%')

    # Close the connection
    conn.close()
    st.title('100%')
else:
    conn = sqlite3.connect(file_path)

st.title('Indicadores sobre Ensino Superior')

show_data_info()

show_table_info(conn)

show_views_info(conn)

show_consultas(conn)
