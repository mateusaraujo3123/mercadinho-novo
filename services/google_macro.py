import pandas as pd
import requests
import streamlit as st

def ler_dados(nome_aba):
    try:
        url_macro = st.secrets["connections"]["gsheets"]["macro_url"]
        resposta = requests.get(f"{url_macro}?sheet_name={nome_aba}", timeout=15)
        matriz = resposta.json()
        if len(matriz) > 0:
            return pd.DataFrame(matriz[1:], columns=matriz)
    except Exception:
        pass
    if nome_aba == "Clientes":
        return pd.DataFrame(columns=["Nome", "Telefone", "Limite", "Divida"])
    return pd.DataFrame(columns=["Código", "Produto", "Preço", "Atacado", "Estoque", "Minimo"])

def salvar_dados(nome_aba, df):
    try:
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
    except Exception as e:
        st.error(f"Erro ao salvar na aba {nome_aba}: {e}")
