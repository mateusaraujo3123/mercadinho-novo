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
