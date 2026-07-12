from utils.styling import aplicar_estilo
aplicar_estilo()

import streamlit as st
from services.google_macro import ler_dados
from pages.dashboard import mostrar_dashboard
from pages.clientes import mostrar_clientes
from pages.produtos import mostrar_produtos

st.set_page_config(page_title="Mercadinho Pro", layout="wide")

# Carregar dados
df_devedores = ler_dados("Clientes")
df_produtos = ler_dados("Produtos")

# Menu lateral
menu = st.sidebar.radio("Menu", ["Dashboard", "Gestão de Fiados", "Produtos"])

if menu == "Dashboard":
    mostrar_dashboard(df_devedores, df_produtos)
elif menu == "Gestão de Fiados":
    mostrar_clientes(df_devedores)
elif menu == "Produtos":
    mostrar_produtos(df_produtos)
