import streamlit as st
from queries import fetch_users, fetch_schools, fetch_courses_of_school, fetch_years, fetch_users_by_course, fetch_attendance_by_course
from views.users.user_table import display_user_table
from views.users.user_charts import display_user_charts
from views.users.user_education import display_user_education
from views.users.course_attendance import display_course_attendance_chart
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Panel de Control - Fundación Educacional Atrévete", layout="wide")

# Título y estilo del Dashboard
st.title("Fundación Educacional Atrévete")
st.markdown("---")

menu_options = {
    "Colegios": "🏫 Colegios",
    "Usuarios": "👥 Usuarios"
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

elif menu_selection == "Colegios":
    # Obtener los nombres de los colegios
    schools_data = fetch_schools()
    school_names = schools_data['name'].tolist()
    years_data = fetch_years()
    years_names = years_data['name'].tolist()

    # Crear columnas para los selectores
    col1, col2, col3 = st.columns(3)

    # Selector de colegios en la primera columna
    with col1:
        selected_school = st.selectbox("Selecciona un colegio", school_names)

    # Selector de años en la segunda columna
    with col2:
        selected_year = st.selectbox("Selecciona un año", years_names)

    # Obtener cursos del colegio seleccionado y el año
    if selected_school and selected_year:
        courses_data = fetch_courses_of_school(selected_school, selected_year)

        # Mostrar cursos como selector en la tercera columna
        with col3:
            if not courses_data.empty:
                # Obtener los nombres de los cursos para el selector
                courses_list = courses_data['grade_name'] + " - " + courses_data['subject_name']
                selected_course = st.selectbox("Selecciona un curso", courses_list)

                # Obtener el ID del curso seleccionado
                selected_course_id = courses_data[courses_list == selected_course]['course_id'].values[0]

        # Mostrar información del curso seleccionado
        if selected_course_id is not None:
            course_info = courses_data[courses_data['course_id'] == selected_course_id]
            if not course_info.empty:
                with st.expander("Usuarios", expanded=False):
                    # Filtro de rol para los usuarios de este curso
                    role_filter = st.selectbox("", ["Todos", "Profesores", "Alumnos"])

                    # Filtra los datos basándote en el rol seleccionado
                    user_data = fetch_users_by_course(selected_course_id)

                    # Filtrar las columnas que deseas mostrar según el rol seleccionado
                    if role_filter == "Profesores":
                        columns_to_display = ["name", "lastName", "phone", "establishment_name", "career_name"]
                        user_data = user_data[user_data['user_course_role'] == 'teacher']
                    elif role_filter == "Alumnos":
                        columns_to_display = ["name", "lastName", "phone", "emergencyName", "emergencyNumber", "emergencyRelationship"]
                    else:  # Para "Todos"
                        columns_to_display = ["name", "lastName", "phone"]

                    # Seleccionar solo las columnas que deseas mostrar en el DataFrame
                    filtered_data_display = user_data[columns_to_display].copy()

                    # Mostrar la tabla con ancho de columnas ajustado
                    st.dataframe(filtered_data_display, use_container_width=True)

                    # Llamada a la función que muestra los gráficos de usuarios para este curso
                    display_user_charts(user_data)
                    if role_filter == "Profesores":
                        # Llamada a la función que muestra la distribución de universidades y carreras
                        display_user_education(user_data)

                    # Desplegable para mostrar información de los usuarios
                    
                # Desplegable para la asistencia
                with st.expander("Asistencia", expanded=False):
                    attendance_data = fetch_attendance_by_course(selected_course_id)
                    display_course_attendance_chart(attendance_data)

                # Desplegable para evaluaciones
                with st.expander("Evaluaciones", expanded=False):
                    # evaluations_data = fetch_evaluations(selected_course_id)
                    # if evaluations_data is not None and not evaluations_data.empty:
                    #     st.dataframe(evaluations_data)
                    # else:
                    #     st.write("No hay datos de evaluaciones disponibles.")
                    pass
    else:
        st.write("No hay cursos disponibles para este colegio y año.")
