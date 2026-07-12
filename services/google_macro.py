import pandas as pd
import requests
import streamlit as st

def ler_dados(nome_aba):
    """Busca dados de uma aba específica no Google Sheets via macro."""
    try:
        url_macro = st.secrets["connections"]["gsheets"]["macro_url"]
        resposta = requests.get(f"{url_macro}?sheet_name={nome_aba}", timeout=15)
        matriz = resposta.json()
        if len(matriz) > 0:
            return pd.DataFrame(matriz[1:], columns=matriz)
    except Exception:
        pass
    # Estrutura padrão caso não consiga ler
    if nome_aba == "Clientes":
        return pd.DataFrame(columns=["Nome", "Telefone", "Limite", "Divida"])
    return pd.DataFrame(columns=["Código", "Produto", "Preço", "Atacado", "Estoque", "Minimo"])


def salvar_dados(nome_aba, df_atualizado):
    """Envia os dados atualizados para a aba do Google Sheets via macro."""
    try:
        url_macro = st.secrets["connections"]["gsheets"]["macro_url"]

        # Cópia limpa para evitar problemas
        df_limpo = df_atualizado.copy()

        # Normaliza colunas de texto
        if "Telefone" in df_limpo.columns:
            df_limpo["Telefone"] = df_limpo["Telefone"].astype(str).replace(r'\.0$', '', regex=True)
        if "Código" in df_limpo.columns:
            df_limpo["Código"] = df_limpo["Código"].astype(str).replace(r'\.0$', '', regex=True)

        # Converte valores para tipos simples (int, float, str)
        linhas = []
        for _, row in df_limpo.iterrows():
            linha = []
            for item in row.values:
                if isinstance(item, (int, float)):
                    linha.append(item)
                else:
                    linha.append(str(item) if pd.notnull(item) else "")
            linhas.append(linha)

        payload = {
            "sheet_name": nome_aba,
            "data": [df_limpo.columns.tolist()] + linhas
        }

        requests.post(url_macro, json=payload, headers={"Content-Type": "application/json"}, timeout=15)
    except Exception as e:
        st.error(f"Erro ao salvar na aba {nome_aba}: {e}")
