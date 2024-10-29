import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

def display_user_education(filtered_data):
    # Total de usuarios
    total_users = len(filtered_data)

    # Gráfico de universidades
    university_counts = filtered_data["establishment_name"].value_counts().sort_index()  # Contar y ordenar alfabéticamente

    # Configuración del gráfico de universidades
    fig_universities = go.Figure(data=[go.Pie(
        labels=university_counts.index,
        values=university_counts.values,
        hoverinfo='label+percent+value',
        textinfo='percent',
    )])

    fig_universities.update_layout(
        title="Universidades de los profesores",
        showlegend=True
    )
    st.plotly_chart(fig_universities, use_container_width=True)

    # Gráfico de carreras
    career_counts = filtered_data["career_name"].value_counts().sort_index()  # Contar y ordenar alfabéticamente

    # Configuración del gráfico de carreras
    fig_careers = go.Figure(data=[go.Pie(
        labels=career_counts.index,
        values=career_counts.values,
        hoverinfo='label+percent+value',
        textinfo='percent',
    )])

    fig_careers.update_layout(
        title="Carreras de los profesores",
        showlegend=True
    )
    st.plotly_chart(fig_careers, use_container_width=True)
