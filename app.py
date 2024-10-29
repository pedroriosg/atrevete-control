import streamlit as st
from queries import fetch_users, fetch_attendance, fetch_evaluations, fetch_other_data
from views.users.user_table import display_user_table
from views.users.user_charts import display_user_charts
from views.users.user_education import display_user_education
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Panel de Control - Fundación Educacional Atrévete", layout="wide")

# Título y estilo del Dashboard
# Título y estilo del Dashboard
st.title("Fundación Educacional Atrévete")
st.markdown("---")

menu_options = {
    "Usuarios": "👥 Usuarios",
    "Asistencia": "📅 Asistencia",
    "Evaluaciones": "📝 Evaluaciones",
    "Otros": "📋 Otros"
}
menu_selection = st.sidebar.selectbox("", list(menu_options.keys()), format_func=lambda x: menu_options[x])

if menu_selection == "Usuarios":
    # Filtro de rol
    role_filter = st.selectbox("", ["Todos", "Profesores", "Alumnos"])

    # Filtra los datos basándote en el rol seleccionado
    user_data = fetch_users()

    # Filtrar las columnas que deseas mostrar según el rol seleccionado
    if role_filter == "Profesores":
        columns_to_display = ["name", "lastName", "rut", "email", "birthday", "phone", "emergencyName", "emergencyNumber", "emergencyRelationship", "establishment_name", "career_name"]
    elif role_filter == "Alumnos":
        columns_to_display = ["name", "lastName", "rut", "email", "birthday", "phone", "emergencyName", "emergencyNumber", "emergencyRelationship"]
    else:  # Para "Todos"
        columns_to_display = ["name", "lastName", "rut", "email", "birthday", "phone", "emergencyName", "emergencyNumber", "emergencyRelationship"]

    # Seleccionar solo las columnas que deseas mostrar en el DataFrame
    filtered_data_display = user_data[columns_to_display].copy()

    # Convertir la columna birthday a datetime y luego formatearla
    filtered_data_display['birthday'] = pd.to_datetime(filtered_data_display['birthday']).dt.date

    # Ajustar el ancho de las columnas
    column_widths = [100] * len(columns_to_display)  # Ancho fijo para todas las columnas

    # Mostrar la tabla con ancho de columnas ajustado
    st.dataframe(filtered_data_display.style.set_properties(**{'width': f'{column_widths[0]}px'}), use_container_width=True)

    # Llamada a la función que muestra los gráficos de usuarios
    display_user_charts(user_data)
    if role_filter == "Profesores":
        # Llamada a la función que muestra la distribución de universidades y carreras
        display_user_education(user_data)