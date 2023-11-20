import os
import streamlit as st
import pandas as pd
import sqlite3
import gdown

def show_table_info(conn):
    st.header('Informações das Tabelas Normalizadas')

    tables_query = "SELECT name FROM sqlite_master WHERE type='table'"
    tables_info = pd.read_sql_query(tables_query, conn)
    
    st.subheader('Informações das Tabelas')
    st.write(tables_info)

def show_views_info(conn):
    st.header('Informações das Views')

    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
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
    SELECT DISTINCT
      NOME_INSTITUICAO
    FROM
      GRADUACAO, ESPECIALIZACAO, INSTITUICAO
    WHERE
      GRADUACAO.COD_INSTITUICAO = ESPECIALIZACAO.COD_INSTITUICAO
      AND GRADUACAO.COD_INSTITUICAO = INSTITUICAO.COD_INSTITUICAO;
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
      GRADUACAO.COD_INSTITUICAO = LOCAL_INSTITUICAO.CODIGO_INSTITUICAO AND ESPECIALIZACAO.COD_INSTITUICAO = LOCAL_INSTITUICAO.CODIGO_INSTITUICAO AND LOCAL_INSTITUICAO.CODIGO_MUNICIPIO = MUNICIPIO.CODIGO_MUNICIPIO AND MUNICIPIO.NOME_MUNICIPIO = 'Belo Horizonte' AND LOCAL_INSTITUICAO.CODIGO_INSTITUICAO = INSTITUICAO.COD_INSTITUICAO
    """

    df = pd.read_sql_query(query, conn)
    return df 

def main():
    st.title('1. Título - Indicadores sobre Ensino Superior')

    file_path = 'mecDataReduced.db'
    #file_path = 'mecData.db'
    #if not (os.path.exists(file_path)):
    #    url = "https://drive.usercontent.google.com/download?id=11-hmllHshrtNt5F1RHKRAd4wTzspIuZ1&export=download&authuser=2&confirm=t&uuid=8cc3ef74-10dc-49f1-a0d8-a52b727138ac&at=APZUnTUR4ucyy1iUFwRrSX7vFx_v:1700484925377"
    #    gdown.download(url, "mecData.db", quiet=False)

    conn = sqlite3.connect('mecData.db')

    show_data_info()
    
    show_table_info(conn)

    show_views_info(conn)

    # Botões para acionar as consultas
    if st.button('Consulta 1 - Seleção de cursos de graduação a distância'):
        with st.spinner('Executando consulta...'):
            df_consulta_1 = consulta_1(conn)
            st.dataframe(df_consulta_1)

    if st.button('Consulta 2 - Cursos de Graduação com Carga Horária >= 4000 horas'):
        with st.spinner('Executando consulta...'):
            df_consulta_2 = consulta_2(conn)
            st.dataframe(df_consulta_2)

    if st.button('Consulta 3 - Instituições que ofertam cursos de graduação e especialização'):
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
    
    cursor = conn.cursor()

if __name__ == "__main__":
    main()
