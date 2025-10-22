import streamlit as st
import plotly.graph_objects as go
from Home import df_filtrado

df_atrasados = df_filtrado.loc[df_filtrado["Status"] == "ATRASADO"]
df_dentro_prazo = df_filtrado.loc[df_filtrado["Status"] != "ATRASADO"]

df_cobrados = df_filtrado.loc[df_filtrado["Cobrado"] == "COBRADO"]
df_nao_cobrados = df_filtrado.loc[df_filtrado["Cobrado"] != "COBRADO"]

col1, col2 = st.columns(1,2)

with col1:
    st.metric("Pedidos Atrasados", len(df_atrasados))
    st.metric("Pedidos Cobrados", len(df_cobrados))

with col2:
    st.metric("Pedidos Dentro do Prazo", len(df_dentro_prazo))
    st.metric("Pedidos Não Cobrados", len(df_nao_cobrados))


