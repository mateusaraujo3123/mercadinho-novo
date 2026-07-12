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
