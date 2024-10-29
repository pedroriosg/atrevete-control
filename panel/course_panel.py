import streamlit as st
import pandas as pd
from queries import fetch_schools, fetch_years, fetch_courses_of_school, fetch_users_by_course, fetch_attendance_by_course, fetch_attendance_by_date, fetch_detailed_attendance_by_course, fetch_performance_by_assessment_type, fetch_evaluations_by_course, fetch_data_by_assessment_id
from views.users.user_charts import display_user_charts
from views.users.user_education import display_user_education
from views.users.course_attendance import display_course_attendance_chart
from views.users.course_evaluations import display_assessment_performance_chart

@st.cache_data
def get_schools():
    return fetch_schools()

@st.cache_data
def get_years():
    return fetch_years()

@st.cache_data
def get_courses(school, year):
    return fetch_courses_of_school(school, year)

@st.cache_data
def get_users_by_course(course_id):
    return fetch_users_by_course(course_id)

@st.cache_data
def get_attendance_by_course(course_id):
    return fetch_attendance_by_course(course_id)

@st.cache_data
def get_attendance_by_date(course_id, date):
    return fetch_attendance_by_date(course_id, date)

@st.cache_data
def get_evaluations_by_course(course_id):
    return fetch_evaluations_by_course(course_id)

@st.cache_data
def get_performance_by_assessment_type(course_id, assessment_type_id):
    return fetch_performance_by_assessment_type(course_id, assessment_type_id)

@st.cache_data
def get_data_by_assessment_id(course_id, assessment_id):
    return fetch_data_by_assessment_id(course_id, assessment_id)

def display_course_panel():
    schools_data = get_schools()
    school_names = schools_data['name'].tolist()
    years_data = get_years()
    years_names = years_data['name'].tolist()

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_school = st.selectbox("Selecciona un colegio", school_names)

    with col2:
        selected_year = st.selectbox("Selecciona un año", years_names)

    if selected_school and selected_year:
        courses_data = get_courses(selected_school, selected_year)

        with col3:
            if not courses_data.empty:
                courses_list = courses_data['grade_name'] + " - " + courses_data['subject_name']
                selected_course = st.selectbox("Selecciona un curso", courses_list)
                selected_course_id = courses_data[courses_list == selected_course]['course_id'].values[0]

        if selected_course_id is not None:
            course_info = courses_data[courses_data['course_id'] == selected_course_id]
            if not course_info.empty:
                with st.expander("Usuarios", expanded=False):
                    user_data = get_users_by_course(selected_course_id)

                    col_filter_1, col_filter_2, col_filter_3 = st.columns(3)
                    with col_filter_1:
                        role_filter = st.selectbox("Filtrar por rol", ["Todos", "Profesores", "Alumnos"])
                    with col_filter_2:
                        email_verified_filter = st.selectbox("Email verificado", ["Todos", "Sí", "No"])
                    with col_filter_3:
                        terms_accepted_filter = st.selectbox("Términos aceptados", ["Todos", "Sí", "No"])

                    if role_filter != "Todos":
                        role = 'teacher' if role_filter == "Profesores" else 'student'
                        user_data = user_data[user_data['user_course_role'] == role]

                    if email_verified_filter != "Todos":
                        user_data = user_data[user_data['validEmail'] == (email_verified_filter == "Sí")]

                    if terms_accepted_filter != "Todos":
                        user_data = user_data[user_data['termsAccepted'] == (terms_accepted_filter == "Sí")]

                    columns_to_display = ["name", "lastName", "phone"]
                    filtered_data_display = user_data[columns_to_display].copy()
                    st.dataframe(filtered_data_display, use_container_width=True)
                    
                    display_user_charts(user_data)
                    if role_filter == "Profesores":
                        display_user_education(user_data)

                with st.expander("Asistencia", expanded=False):
                    if 'attendance_data' not in st.session_state:
                        st.session_state.attendance_data = get_attendance_by_course(selected_course_id)

                    attendance_data = st.session_state.attendance_data
                    display_course_attendance_chart(attendance_data)

                    if 'detailed_attendance' not in st.session_state:
                        st.session_state.detailed_attendance = fetch_detailed_attendance_by_course(selected_course_id)

                    detailed_attendance = st.session_state.detailed_attendance
                    
                    if not detailed_attendance.empty:
                        # Obtén los valores de asistencia
                        date_t = detailed_attendance.loc[0, 'date_t']
                        date_t1 = detailed_attendance.loc[0, 'date_t1']
                        date_t2 = detailed_attendance.loc[0, 'date_t2']

                        # Renombra las columnas de asistencia usando las fechas
                        detailed_attendance = detailed_attendance.rename(columns={
                            'attended_t': f"{date_t}",
                            'attended_t1': f"{date_t1}",
                            'attended_t2': f"{date_t2}"
                        })

                        # Convierte 0 y 1 en los íconos de check y cruz
                        for date_column in [f"{date_t}", f"{date_t1}", f"{date_t2}"]:
                            detailed_attendance[date_column] = detailed_attendance[date_column].apply(lambda x: '✅' if x == 1 else '❌')

                        # Formatear total_attendance_percentage (está como entero entre 0, 100, lo quiero sin decimales)
                        detailed_attendance['total_attendance_percentage'] = detailed_attendance['total_attendance_percentage'].apply(lambda x: f"{x:.0f}%")

                        # Selecciona y muestra las columnas requeridas
                        st.write("Ranking de asistencia")
                        st.dataframe(detailed_attendance[['name', 'lastName', f"{date_t2}", f"{date_t1}", f"{date_t}", 'total_attendance_percentage']], use_container_width=True)

                    dates = attendance_data['class_date'].unique().tolist()

                    col1, col2 = st.columns(2)

                    with col1:
                        selected_date = st.selectbox("Selecciona una fecha", dates[::-1])

                    with col2:
                        attendance_filter = st.selectbox("Filtrar por asistencia", ["Ausentes", "Presentes"])

                    if selected_date:
                        attendance_status = get_attendance_by_date(selected_course_id, selected_date)

                        present_students = attendance_status[attendance_status['attendance_status'] == 'present']
                        absent_students = attendance_status[attendance_status['attendance_status'] == 'absent']

                        if attendance_filter == "Presentes":
                            filtered_data = present_students
                        elif attendance_filter == "Ausentes":
                            filtered_data = absent_students

                        filtered_data_display = filtered_data[['name', 'lastName', 'phone']]
                        st.dataframe(filtered_data_display, use_container_width=True)

                with st.expander("Evaluaciones", expanded=True):
                    if 'evaluations_data' not in st.session_state:
                        st.session_state.evaluations_data = fetch_evaluations_by_course(selected_course_id)

                    evaluations_data = st.session_state.evaluations_data

                    if not evaluations_data.empty:
                        # Crear un diccionario que mapee los tipos de evaluación a sus IDs
                        assessment_type_mapping = {
                            row['assessment_type_name']: row['assessment_type_id'] 
                            for _, row in evaluations_data.iterrows()
                        }

                        assessment_types = list(assessment_type_mapping.keys())

                        # Selecciona el tipo de evaluación
                        selected_assessment_type_name = st.selectbox("Selecciona un tipo de evaluación", assessment_types)

                        # Verifica que el tipo de evaluación seleccionado existe en el mapeo
                        if selected_assessment_type_name in assessment_type_mapping:
                            selected_assessment_type_id = assessment_type_mapping[selected_assessment_type_name]

                            # Obtener el rendimiento de las evaluaciones para el gráfico
                            performance_data = get_performance_by_assessment_type(selected_course_id, selected_assessment_type_id)
                            display_assessment_performance_chart(performance_data)

                            # Agregar un selectbox para elegir una evaluación específica
                            evaluation_ids = evaluations_data[evaluations_data['assessment_type_id'] == selected_assessment_type_id]['assessment_id'].tolist()
                            evaluation_names = evaluations_data[evaluations_data['assessment_type_id'] == selected_assessment_type_id]['assessment_name'].tolist()

                            if evaluation_ids:  # Verifica que haya IDs de evaluación
                                selected_evaluation_name = st.selectbox("Selecciona una evaluación", evaluation_names)

                                # Obtener el ID de la evaluación seleccionada
                                selected_assessment_id = evaluation_ids[evaluation_names.index(selected_evaluation_name)]

                                # Verificar si el ID de evaluación seleccionado ha cambiado
                                if 'selected_assessment_id' not in st.session_state or st.session_state.selected_assessment_id != selected_assessment_id:
                                    # Actualiza el ID y los datos de la evaluación en session_state
                                    st.session_state.selected_assessment_id = selected_assessment_id
                                    st.session_state.assessment_data = fetch_data_by_assessment_id(selected_course_id, selected_assessment_id)

                                # Usa la variable guardada en session_state
                                assessment_data = st.session_state.assessment_data

                                # Añade un selector para filtrar entre presentes y ausentes
                                filter_option = st.selectbox("Filtrar por:", ["Presentes", "Ausentes"])

                                # Filtra el DataFrame según la selección
                                if filter_option == "Presentes":
                                    filtered_data = assessment_data[assessment_data["absent_users"] == 0]
                                else:  # "Ausentes"
                                    filtered_data = assessment_data[assessment_data["absent_users"] == 1]

                                # Muestra la tabla sin la columna "absent_users"
                                st.dataframe(filtered_data.drop(columns=["absent_users"]), use_container_width=True)
                        else:
                            st.write("Tipo de evaluación no encontrado.")
                    else:
                        st.write("No se encontraron evaluaciones para este curso.")


