import streamlit as st
import plotly.express as px
from Home import df_filtrado

df_atrasados = df_filtrado.loc[df_filtrado["Status"] == "ATRASADO"]
df_dentro = df_filtrado.loc[df_filtrado["Status"] != "ATRASADO"]

fig1 = px.pie(
    names = ["Atrasados", "Dentro do Prazo"],
    values = [len(df_atrasados), len(df_dentro)],
    hole = 0.4,
    titte = "Status dos Pedidos"
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

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1)

with col2:
    st.plotly_chart(fig2)