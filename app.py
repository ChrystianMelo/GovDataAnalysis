# -*- coding: utf-8 -*-
"""StreamlitVersion.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nm4KliLmhS8A8MSFP7zxxyhTY5PGIIge
"""

#pip install streamlit
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

    views_query = "SELECT * FROM sqlite_master WHERE type='table';"
    views_info = pd.read_sql_query(views_query, conn)

    st.subheader('Informações das Views')
    st.write(views_info)

def show_data_info():
    st.header('Informações sobre as Bases de Dados')

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

def main():
    st.title('1. Título - Indicadores sobre Ensino Superior')

    file_path = 'mecData.db'
    if not (os.path.exists(file_path)):
        url = "https://drive.usercontent.google.com/download?id=11-hmllHshrtNt5F1RHKRAd4wTzspIuZ1&export=download&authuser=2&confirm=t&uuid=8cc3ef74-10dc-49f1-a0d8-a52b727138ac&at=APZUnTUR4ucyy1iUFwRrSX7vFx_v:1700484925377"
        gdown.download(url, "mecData.db", quiet=False)

    conn = sqlite3.connect('mecData.db')

    show_data_info()

    show_table_info(conn)

    show_views_info(conn)

    #consultas

    cursor = conn.cursor()

if __name__ == "__main__":
    main()
