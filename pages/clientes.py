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
