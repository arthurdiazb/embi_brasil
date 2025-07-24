from io import BytesIO
import streamlit as st
import pandas as pd
import requests
import time

st.title("EMBI+ Filtrado para Brasil")

# URL do arquivo original
url = 'https://bcrdgdcprod.blob.core.windows.net/documents/entorno-internacional/documents/Serie_Historica_Spread_del_EMBI.xlsx'
anos = st.multiselect("Selecione os anos para a gerar a tabela",range(2020,2026))

# Botão para processar
if st.button("Gerar arquivo Excel"):
    # Exibir mensagem e barra de progresso
    st.write("### Carregando...")
    progress_bar = st.progress(0)

    # Simulação de progresso (opcional, só para UX)
    for perc in range(0, 40, 10):
        time.sleep(0.2)
        progress_bar.progress(perc)

    # Baixar arquivo original
    response = requests.get(url)
    response.raise_for_status()

    for perc in range(40, 70, 10):
        time.sleep(0.2)
        progress_bar.progress(perc)

    # Ler e processar
    df = pd.read_excel(BytesIO(response.content), skiprows=1, index_col=0)[['Brasil']]
    df.index = pd.to_datetime(df.index, format="mixed").sort_values(ascending=False)
    df['Ano'] = df.index.year
    df.index.name = 'Data'
    df = df[df['Ano'].isin(anos)][['Brasil']]

    for perc in range(70, 90, 10):
        time.sleep(0.2)
        progress_bar.progress(perc)

    # Salvar em memória (Excel)
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=True, sheet_name="EMBI+")
        workbook = writer.book
        worksheet = writer.sheets["EMBI+"]
        for cell in worksheet["A"][1:]:
            cell.number_format = "DD/MM/YYYY"
        worksheet.column_dimensions["A"].width = 11

    output.seek(0)
    progress_bar.progress(100)

    # Criar botão de download
    st.download_button(
        label="Clique aqui para baixar o arquivo Excel Filtrado",
        data=output,
        file_name="EMBI_Brasil.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )