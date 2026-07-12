import streamlit as st

def aplicar_estilo():
    st.markdown("""
        <style>
        /* Esconde botões padrão do Streamlit */
        .stDeployButton, #MainMenu { display: none !important; }

        /* Barra superior personalizada */
        .topbar {
            background-color: #6A1B9A; padding: 15px; border-radius: 8px;
            color: white !important; margin-bottom: 20px; display: flex;
            justify-content: space-between; align-items: center;
        }

        /* Cartões do dashboard */
        .dashboard-card {
            background-color: #FFFFFF !important; padding: 20px;
            border-radius: 8px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05); 
            margin-bottom: 20px; border: 1px solid #EAEAEA;
        }

        /* Alertas de estoque */
        .stock-alert { 
            display: flex; justify-content: space-between; 
            padding: 8px 0; border-bottom: 1px solid #EEEEEE; 
        }
        .stock-critical { color: #D32F2F; font-weight: bold; }

        /* Botões customizados */
        div.stButton > button, div[data-testid="stVerticalBlock"] button[data-testid="baseButton-secondary"] {
            background-color: #6A1B9A !important; color: #FFFFFF !important;
            border: none !important; padding: 16px 20px !important;
            font-weight: bold !important; font-size: 16px !important;
            border-radius: 8px !important; box-shadow: 0px 4px 6px rgba(0,0,0,0.15) !important;
        }
        div.stButton > button:hover, div[data-testid="stVerticalBlock"] button[data-testid="baseButton-secondary"]:hover { 
            background-color: #4A148C !important; 
        }
        </style>
    """, unsafe_allow_html=True)
