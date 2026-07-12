#css
from utils.styling import aplicar_estilo

aplicar_estilo()

from services.google_macro import ler_dados, salvar_dados

df_devedores = ler_dados("Clientes")
df_produtos = ler_dados("Produtos")

# inicio dashboard
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

import pandas as pd
import requests
import streamlit as st

def ler_dados(nome_aba):
    url_macro = st.secrets["connections"]["gsheets"]["macro_url"]
    try:
        resposta = requests.get(f"{url_macro}?sheet_name={nome_aba}", timeout=15)
        matriz = resposta.json()
        if len(matriz) > 0:
            return pd.DataFrame(matriz[1:], columns=matriz)
    except Exception:
        pass
    return pd.DataFrame()

def salvar_dados(nome_aba, df):
    url_macro = st.secrets["connections"]["gsheets"]["macro_url"]
    df_limpo = df.copy()

    for col in ["Telefone", "Código"]:
        if col in df_limpo.columns:
            df_limpo[col] = df_limpo[col].astype(str).replace(r'\.0$', '', regex=True)

    linhas = []
    for _, row in df_limpo.iterrows():
        linhas.append([str(item) if pd.notnull(item) else "" for item in row.values])

    payload = {"sheet_name": nome_aba, "data": [df_limpo.columns.tolist()] + linhas}
    requests.post(url_macro, json=payload, headers={"Content-Type": "application/json"}, timeout=15)

import streamlit as st
import plotly.express as px

def mostrar_dashboard(df_devedores, df_produtos):
    st.write("## Fluxo de Fiados & Devedores")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top Maiores Devedores")
        if not df_devedores.empty:
            fig = px.bar(df_devedores.sort_values("Divida"), x="Divida", y="Nome", orientation="h")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhuma dívida registrada.")

    with col2:
        st.subheader("Alertas de Estoque")
        for _, prod in df_produtos.iterrows():
            alerta = "⚠️" if prod["Estoque"] <= prod["Minimo"] else "✅"
            st.write(f"{alerta} {prod['Produto']} - {prod['Estoque']} / {prod['Minimo']}")

    st.metric("Soma Total de Fiados", f"R$ {df_devedores['Divida'].sum():,.2f}")
    st.metric("Clientes acima do limite", len(df_devedores[df_devedores["Divida"] > df_devedores["Limite"]]))

import streamlit as st
import pandas as pd
from services.google_macro import salvar_dados

def mostrar_clientes(df_devedores):
    st.header("Gestão de Fiados")

    aba_cad, aba_rem = st.tabs(["➕ Cadastrar Cliente / Lançar", "❌ Remover Cliente"])

    with aba_cad:
        with st.expander("➕ Cadastrar Novo Cliente"):
            nome = st.text_input("Nome do Cliente")
            tel = st.text_input("Telefone")
            limite = st.number_input("Limite (R$)", min_value=0.0, value=200.0)
            if st.button("Salvar Cliente"):
                novo_cli = pd.DataFrame([{"Nome": nome, "Telefone": str(tel).strip(), "Limite": float(limite), "Divida": 0.0}])
                df_devedores = pd.concat([df_devedores, novo_cli], ignore_index=True)
                salvar_dados("Clientes", df_devedores)
                st.success("Cliente cadastrado!")
                st.rerun()

        st.write("### 💸 Lançar Compra ou Pagamento")
        if not df_devedores.empty:
            cliente_sel = st.selectbox("Selecione o Cliente:", df_devedores["Nome"].tolist())
            val = st.number_input("Valor (R$)", min_value=0.01, step=1.0)
            if st.button("🔴 Adicionar Dívida"):
                df_devedores.loc[df_devedores["Nome"] == cliente_sel, "Divida"] += val
                salvar_dados("Clientes", df_devedores)
                st.rerun()
            if st.button("🟢 Abater Dívida"):
                df_devedores.loc[df_devedores["Nome"] == cliente_sel, "Divida"] -= val
                salvar_dados("Clientes", df_devedores)
                st.rerun()

    with aba_rem:
        if not df_devedores.empty:
            cliente_remover = st.selectbox("Selecione para remover:", df_devedores["Nome"].tolist())
            if st.button("🗑️ Remover Cliente"):
                df_devedores = df_devedores[df_devedores["Nome"] != cliente_remover].reset_index(drop=True)
                salvar_dados("Clientes", df_devedores)
                st.rerun()

    st.write("### Lista Geral de Contas")
    st.dataframe(df_devedores, use_container_width=True)

import streamlit as st
import pandas as pd
from services.google_macro import salvar_dados

def mostrar_produtos(df_produtos):
    st.header("Tabelas de Preços e Estoque")

    aba_p1, aba_p2 = st.tabs(["📋 Lista de Produtos", "🗑️ Remover Produto"])

    with aba_p1:
        with st.expander("📦 Adicionar Novo Produto"):
            cod = st.text_input("Código")
            nome_prod = st.text_input("Produto")
            p_varejo = st.number_input("Preço Varejo", min_value=0.0)
            p_atacado = st.number_input("Preço Atacado", min_value=0.0)
            est_inicial = st.number_input("Estoque Atual", min_value=0)
            est_min = st.number_input("Mínimo", min_value=0)
            if st.button("Cadastrar Produto"):
                novo_prod = pd.DataFrame([{"Código": str(cod).strip(), "Produto": nome_prod, "Preço": float(p_varejo), "Atacado": float(p_atacado), "Estoque": int(est_inicial), "Minimo": int(est_min)}])
                df_produtos = pd.concat([df_produtos, novo_prod], ignore_index=True)
                salvar_dados("Produtos", df_produtos)
                st.success("Produto cadastrado!")
                st.rerun()
        st.dataframe(df_produtos, use_container_width=True)

    with aba_p2:
        if not df_produtos.empty:
            prod_remover = st.selectbox("Selecione produto para remover:", df_produtos["Produto"].tolist())
            if st.button("🗑️ Remover Produto"):
                df_produtos = df_produtos[df_produtos["Produto"] != prod_remover].reset_index(drop=True)
                salvar_dados("Produtos", df_produtos)
                st.rerun()
