import streamlit as st

def aplicar_estilo():
    st.markdown("""
        <style>
        .stDeployButton, #MainMenu { display: none !important; }
        .topbar {
            background-color: #6A1B9A; padding: 15px; border-radius: 8px;
            color: white !important; margin-bottom: 20px; display: flex;
            justify-content: space-between; align-items: center;
        }
        .dashboard-card {
            background-color: #FFFFFF !important; padding: 20px
