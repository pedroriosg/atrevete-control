import streamlit as st
from queries import fetch_users, fetch_schools, fetch_courses_of_school, fetch_years, fetch_users_by_course, fetch_attendance_by_course, fetch_attendance_by_date
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

    # Cargar datos de usuarios al abrir la pestaña
    with st.expander("Usuarios", expanded=True):
        user_data = fetch_users()
        columns_to_display = ["name", "lastName", "rut", "email", "birthday", "phone", "emergencyName", "emergencyNumber", "emergencyRelationship"]
        filtered_data_display = user_data[columns_to_display].copy()
        filtered_data_display['birthday'] = pd.to_datetime(filtered_data_display['birthday']).dt.date
        st.dataframe(filtered_data_display, use_container_width=True)
        display_user_charts(user_data)
        if role_filter == "Profesores":
            display_user_education(user_data)

elif menu_selection == "Colegios":
    schools_data = fetch_schools()
    school_names = schools_data['name'].tolist()
    years_data = fetch_years()
    years_names = years_data['name'].tolist()

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_school = st.selectbox("Selecciona un colegio", school_names)

    with col2:
        selected_year = st.selectbox("Selecciona un año", years_names)

    if selected_school and selected_year:
        courses_data = fetch_courses_of_school(selected_school, selected_year)
        
        with col3:
            if not courses_data.empty:
                courses_list = courses_data['grade_name'] + " - " + courses_data['subject_name']
                selected_course = st.selectbox("Selecciona un curso", courses_list)
                selected_course_id = courses_data[courses_list == selected_course]['course_id'].values[0]

        if selected_course_id is not None:
            course_info = courses_data[courses_data['course_id'] == selected_course_id]
            if not course_info.empty:
                with st.expander("Usuarios", expanded=False):
                    user_data = fetch_users_by_course(selected_course_id)
                    role_filter = st.selectbox("", ["Todos", "Profesores", "Alumnos"])
                    columns_to_display = ["name", "lastName", "phone"]
                    filtered_data_display = user_data[columns_to_display].copy()
                    st.dataframe(filtered_data_display, use_container_width=True)
                    display_user_charts(user_data)
                    if role_filter == "Profesores":
                        display_user_education(user_data)

                with st.expander("Asistencia", expanded=True):
                    attendance_data = fetch_attendance_by_course(selected_course_id)
                    display_course_attendance_chart(attendance_data)

                    # Selector de clases (fechas) para mostrar la asistencia
                    dates = attendance_data['class_date'].unique().tolist()

                    # Crear dos columnas
                    col1, col2 = st.columns(2)

                    with col1:
                        selected_date = st.selectbox("Selecciona una fecha de clase", dates)

                    with col2:
                        attendance_filter = st.selectbox("Filtrar por asistencia", ["Ausentes", "Presentes", "Todos"])

                    if selected_date:
                        attendance_status = fetch_attendance_by_date(selected_course_id, selected_date)

                        # Filtra los presentes y ausentes
                        present_students = attendance_status[attendance_status['attendance_status'] == 'present']
                        absent_students = attendance_status[attendance_status['attendance_status'] == 'absent']

                        # Filtrar el dataframe según la selección
                        if attendance_filter == "Presentes":
                            filtered_data = present_students
                        elif attendance_filter == "Ausentes":
                            filtered_data = absent_students
                        else:
                            filtered_data = attendance_status

                        # Seleccionar columnas relevantes para la visualización
                        filtered_data_display = filtered_data[['name', 'lastName', 'phone']]

                        # Mostrar en una tabla con capacidades de ordenamiento y filtrado
                        st.dataframe(filtered_data_display, use_container_width=True)

                                    
                    

                with st.expander("Evaluaciones", expanded=False):
                    pass  # Aquí colocarías la lógica para cargar evaluaciones si fuera necesario
    else:
        st.write("No hay cursos disponibles para este colegio y año.")
