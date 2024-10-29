import streamlit as st
import plotly.graph_objects as go

def display_user_charts(filtered_data):

    # Crear columnas para mostrar los gráficos uno al lado del otro
    col1, col2 = st.columns(2)

    # Gráfico de validEmail
    with col1:
        valid_email_counts = filtered_data["validEmail"].value_counts()
        fig_valid_email = go.Figure(data=[go.Pie(
            labels=valid_email_counts.index.map({True: "Validado", False: "No validado"}),  # Mapea valores
            values=valid_email_counts.values,
            textinfo="label+percent",
            insidetextorientation="radial"
        )])
        fig_valid_email.update_layout(title="Correos validados")
        st.plotly_chart(fig_valid_email, use_container_width=True)

    # Gráfico de termsAccepted
    with col2:
        terms_accepted_counts = filtered_data["termsAccepted"].value_counts()
        fig_terms_accepted = go.Figure(data=[go.Pie(
            labels=terms_accepted_counts.index.map({True: "Aceptado", False: "No aceptado"}),  # Mapea valores
            values=terms_accepted_counts.values,
            textinfo="label+percent",
            insidetextorientation="radial"
        )])
        fig_terms_accepted.update_layout(title="Términos aceptados")
        st.plotly_chart(fig_terms_accepted, use_container_width=True)

