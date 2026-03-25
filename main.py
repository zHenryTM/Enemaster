import pandas as pd
import streamlit as st
from fpdf import FPDF
from fpdf import Align


def obter_microdados():
    url_microdados = "https://github.com/NiedsonEmanoel/NiedsonEmanoel/raw/main/enem/An%C3%A1lise%20de%20Itens/OrdenarPorTri/gerador/provasOrdernadasPorTri.csv"

    return pd.read_csv(url_microdados, encoding="utf-8", decimal=",")


def obter_microdados_filtrados(microdados, materia, habilidade):
    microdados_filtrado = microdados[ (microdados["SG_AREA"] == materia[0:2]) & (microdados["CO_HABILIDADE"] == habilidade) ]

    microdados_filtrado = microdados_filtrado[ ["OCRSearch", "CO_HABILIDADE", "imagAPI", "TX_GABARITO"] ]

    return microdados_filtrado


def gerar_pdf(microdados):

    pdf = FPDF()

    pdf.set_page_background("./imagens/background_paginas.png")

    pdf.set_font("Helvetica", size=12)

    for linha in microdados.itertuples(index=True, name="Pandas"):

        url_imagem_questao = linha.imagAPI

        tamanho_largura_imagem = pdf.epw * 0.66  # pdf.epw é o tamanho da largura da página do PDF

        pdf.add_page()

        pdf.image(url_imagem_questao, x=Align.C, w=tamanho_largura_imagem)
    
    pdf.add_page()

    # inserir o gabarito aqui
    numero_questao = 1

    for linha in microdados.itertuples(index=True, name="Pandas"):

        gabarito = linha.TX_GABARITO

        pdf.write(text=f"{numero_questao}º Questão - {gabarito}\n")

        numero_questao += 1

    # Saída
    pdf.output("lista_questoes.pdf")


def gerar_lista_exercicios():
    microdados = obter_microdados()

    microdados_filtrados = obter_microdados_filtrados(microdados, materia, habilidade)

    gerar_pdf(microdados_filtrados)

    st.session_state.clicked = True


st.header("Enemaster")

st.divider()

materia = st.selectbox("Selecione uma matéria", ["LC - Linguagens", "MT - Matemática", "CN - Naturezas", "CH - Humanas"])

habilidade = st.selectbox(
    "Selecione uma habilidade", 
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
)

if "clicked" not in st.session_state:
    st.session_state.clicked = False

st.button("Gerar!", on_click=gerar_lista_exercicios)

if st.session_state.clicked:
    with open("lista_questoes.pdf", "rb") as f:
        arquivo = f.read()

    file_name = f"H{habilidade} - {materia[5:]}.pdf"

    st.download_button(
        label="Download",
        data=arquivo,
        file_name=file_name,
        mime="application/pdf",
    )

# PRÓXIMOS PASSOS!

# 1- Adicionar botão de download após gerar o material

# 2- Baixar material após apertar o botão de download

# 3- Atualizar o nome do arquivo para deixar correspondente à habilidadede e à matéria

# 4- Disponibilizar primeira versão na web

# 5- Melhorar layout da página inicial Stremalit (animações, textos dinâmicos, etc.)

# 6- Melhorar layout das páginas do PDF (faixa azul em cima da questão, deixando claro qual habilidade ela compõe e nota TRI esperada)

# 7- Melhorar apresentação do gabarito no PDF

# 8- Adicionar seção "sobre" no enemaster, contando a história do programa e seus desenvolvedores

# 9- Adicionar seção "Como estudar?" no enemaster, ensinando como funciona a matriz de referência do enem, o que é a nota TRI em cima de cada questão e etc.

# 10- Disponibilizar versão final