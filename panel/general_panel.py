import streamlit as st
import pandas as pd
from queries import (
    fetch_years,
    fetch_team_by_year,
    fetch_school_by_year,
    fetch_school_users_details,
    fetch_proportion_type_user,
    fetch_students_by_grade_proportion
)

from views.general.school_users import (display_team_by_year_chart, display_students_by_grade_chart)
from views.general.users_proportion import display_user_charts

@st.cache_data
def get_years():
    # Verificar si el DataFrame está vacío
    years_df = fetch_years()
    if years_df.empty:
        return []  # Devolver una lista vacía si no hay datos

    # Convertir DataFrame a una lista de diccionarios
    return years_df.to_dict(orient="records")

@st.cache_data
def get_team_by_year(year):
    return fetch_team_by_year(year)

@st.cache_data
def get_school_by_year(year):
    return fetch_school_by_year(year)

@st.cache_data
def get_school_users_details(school_id, user_role):
    return fetch_school_users_details(school_id, user_role)

@st.cache_data
def get_proportion_type_user(year):
    return fetch_proportion_type_user(year)

@st.cache_data
def get_students_by_grade_proportion(year_id, user_role):
    return fetch_students_by_grade_proportion(year_id, user_role)


def display_general_panel():
    # Obtener datos de años
    years_data = get_years()

    # Asegurarse de que years_data sea una lista de diccionarios con "name" e "id"
    if not years_data:
        st.error("Error: No se encontraron datos de años.")
        return

    # Extraer nombres e ids de los años
    year_names = [year["name"] for year in years_data]
    year_ids = {year["name"]: year["id"] for year in years_data}
    
    # Configurar el selectbox con el primer año seleccionado por defecto
    selected_year_name = st.selectbox("Seleccione el año", year_names, index=0)
    
    # Obtener el id correspondiente al año seleccionado
    selected_year_id = year_ids[selected_year_name]

    type_user_proportion = get_proportion_type_user(selected_year_id)
    students_by_grade_proportion = get_students_by_grade_proportion(selected_year_id, 'student')
    teachers_by_grade_proportion = get_students_by_grade_proportion(selected_year_id, 'teacher')

    display_user_charts(type_user_proportion, students_by_grade_proportion, teachers_by_grade_proportion)

    # Obtener datos del equipo por año
    team_data = get_team_by_year(selected_year_id)
    display_team_by_year_chart(team_data)

    school_data = get_school_by_year(selected_year_id)

    school_names = school_data['school_name'].unique()
    selected_school_name = st.selectbox("Seleccione la escuela", school_names, index=0)
    selected_school_id = school_data[school_data['school_name'] == selected_school_name]['school_id'].values[0]

    school_users_details = get_school_users_details(selected_school_id, 'student')
    teachers_users_details = get_school_users_details(selected_school_id, 'teacher')
    display_students_by_grade_chart(school_users_details, 'student')
    display_students_by_grade_chart(teachers_users_details, 'teacher')