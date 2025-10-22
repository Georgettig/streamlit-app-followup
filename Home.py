import streamlit as st
import os
import pandas as pd
from datetime import datetime, timedelta
from database import df, df_emails

arquivo = "dados/pedidos_cobrados.xlsx"

# Configurando a aplicação
st.set_page_config(page_title = "App", layout = "wide")
st.title("App de Follow-Up")

# Criando uma cópia da base de dados
df_filtrado = df.copy()

# Inicializando o status dos filtros
if "filtro_status" not in st.session_state:
    st.session_state.filtro_status = None

# Criando os botões de filtro
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Atrasados"):
        st.session_state.filtro_status = "ATRASADO"

with col2:
    if st.button("Dentro do Prazo"):
        st.session_state.filtro_status = "DENTRO"

with col3:
    if st.button("Cobrar Fornecedor"):
        st.session_state.filtro_status = "COBRAR"

with col4:
    if st.button("Limpar Filtros"):
        st.session_state.filtro_status = None
        st.session_state["Fornecedor"] = []
        st.session_state["Comprador"] = []
        st.session_state["Pedido"] = []

# Adicionando o filtro aos botoões criados
if st.session_state.filtro_status == "ATRASADO":
    df_filtrado = df_filtrado[df_filtrado['Status'] == "ATRASADO"]

if st.session_state.filtro_status == "DENTRO":
    df_filtrado = df_filtrado[df_filtrado['Status'] == "DENTRO DO PRAZO"]

if st.session_state.filtro_status == "COBRAR":
    df_filtrado = df_filtrado[(df_filtrado['Data Entrega'] <= datetime.now() + timedelta(days=30))
                                & (df_filtrado['Cobrado'] == "NÃO COBRADO")]

# Criando os filtros na lateral do app
st.sidebar.title("Filtros")

filtro_fornecedor = st.sidebar.multiselect("Fornecedor", sorted(df_filtrado["Fornecedor"].unique()), key="Fornecedor")
if filtro_fornecedor:
    df_filtrado = df_filtrado[df_filtrado["Fornecedor"].isin(filtro_fornecedor)]

filtro_comprador = st.sidebar.multiselect("Comprador", sorted(df_filtrado["Comprador"].unique()), key="Comprador")
if filtro_comprador:
    df_filtrado = df_filtrado[df_filtrado["Comprador"].isin(filtro_comprador)]

filtro_pedido = st.sidebar.multiselect("Pedido", sorted(df_filtrado["Pedido"].unique()), key="Pedido")
if filtro_pedido:
    df_filtrado = df_filtrado[df_filtrado["Pedido"].isin(filtro_pedido)]


# Convertendo datas e códigos
df_filtrado['Data Entrega'] = df_filtrado['Data Entrega'].dt.strftime('%d/%m/%Y')
df_filtrado['Data Pedido'] = df_filtrado['Data Pedido'].dt.strftime('%d/%m/%Y')

df_filtrado['Código'] = df_filtrado['Código'].astype(str)
df_emails['Código'] = df_filtrado['Código'].astype(str)

# Exibir Dataframe
st.markdown(f"Quantidade de Pedidos: :red[{len(df_filtrado)}]")
st.dataframe(df_filtrado)

# Criando botão para enviar e-mail
if st.button("Enviar e-mail"):
    df.loc[df_filtrado.index, 'Cobrado'] = "COBRADO"
    if os.path.exists(arquivo):
        df_existente = pd.read_excel(arquivo)
        df_novos = df_filtrado[~df_filtrado['Pedido'].isin(df_existente['Pedido'])]
        df_salvar = pd.concat([df_existente, df_novos], ignore_index=True)
    else:
        df_salvar = df_filtrado.copy()
    
    df_salvar.to_excel(arquivo, index=False)
    st.success("E-mail enviado com sucesso!")