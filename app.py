from utils.styling import aplicar_estilo
aplicar_estilo()

import streamlit as st
from services.google_macro import ler_dados
from pages.dashboard import mostrar_dashboard
from pages.clientes import mostrar_clientes
from pages.produtos import mostrar_produtos

st.set_page_config(page_title="Mercadinho Pro", layout="wide")

#aparencia
st.markdown("""
    <style>
    body, .main, .block-container {
        background-color: #F9F9F9 !important;
        color: #222222 !important;
    }
    </style>
""", unsafe_allow_html=True)

#barra superior
st.markdown('<div class="topbar"><h2 style="margin:0; color:white;">🛍️ MERCADINHO PRO</h2><span>🟢 BANCO DE DADOS ATIVO</span></div>', unsafe_allow_html=True)

col_b1, col_b2, col_b3 = st.columns(3)
with col_b1:
    st.button("👥 PESSOAS", use_container_width=True)
with col_b2:
    st.button("📦 PRODUTOS", use_container_width=True)
with col_b3:
    st.button("📈 CONTAS A RECEBER", use_container_width=True)

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
