import streamlit as st
import plotly.express as px
from Home import df_filtrado

st.set_page_config(page_title = "App", layout = "wide")
st.title("Gráficos de Indicadores")

df_atrasados = df_filtrado.loc[df_filtrado["Status"] == "ATRASADO"]
df_dentro = df_filtrado.loc[df_filtrado["Status"] != "ATRASADO"]

fig1 = px.pie(
    names = ["Atrasados", "Dentro do Prazo"],
    values = [len(df_atrasados), len(df_dentro)],
    hole = 0.4,
    title = "Status dos Pedidos"
)
fig1.update_layout(legend_title_text = "Status")

df_cobrados = df_filtrado.loc[df_filtrado["Cobrado"] == "COBRADO"]
df_nao_cobrados = df_filtrado.loc[df_filtrado["Cobrado"] != "COBRADO"]

fig2 = px.pie(
    names = ["Cobrados", "Não Cobrados"],
    values = [len(df_cobrados), len(df_nao_cobrados)],
    hole = 0.4,
    title = "Situação dos Pedidos"
)
fig2.update_layout(legend_title_text = "Cobrado")

df_compradores = df_filtrado.groupby("Comprador")["Pedido"].count().sort_values(ascending=False).reset_index()
df_compradores.columns = ["Comprador", "Quantidade Pedidos"]
fig3 = px.bar(
    df_compradores,
    x = "Comprador",
    y = "Quantidade Pedidos",
    title = "Quantidade de Pedidos por Comprador",
    color_continuous_scale = "Blues"
)


df_fornecedores = df_filtrado.groupby("Fornecedor")["Pedido"].count().sort_values(ascending=False).reset_index()
df_fornecedores.columns = ["Fornecedor", "Quantidade Pedidos"]
fig4 = px.bar(
    df_fornecedores,
    x = "Fornecedor",
    y = "Quantidade Pedidos",
    title = "Quantidade de Pedidos por Fornecedor",
    color_continuous_scale = "Blues"
)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1)
    st.plotly_chart(fig3)

with col2:
    st.plotly_chart(fig2)
    st.plotly_chart(fig4)