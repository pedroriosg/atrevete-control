import streamlit as st
import pandas as pd
from queries import (
    fetch_schools, fetch_years, fetch_courses_of_school, fetch_users_by_course,
    fetch_attendance_by_course, fetch_attendance_by_date, fetch_detailed_attendance_by_course,
    fetch_performance_by_assessment_type, fetch_evaluations_by_course, fetch_data_by_assessment_id
)
from views.users.user_charts import display_user_charts_general
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
        selected_year = st.selectbox("Selecciona un año", years_names, key="selected_year")

    with col2:
        selected_school = st.selectbox("Selecciona un colegio", school_names, key="selected_school")

    if selected_school and selected_year:
        courses_data = get_courses(selected_school, selected_year)
        courses_list = courses_data['grade_name'] + " - " + courses_data['subject_name']

        with col3:
            if not courses_data.empty:
                selected_course = st.selectbox("Selecciona un curso", courses_list, key="selected_course")
                selected_course_id = courses_data[courses_list == selected_course]['course_id'].values[0]

        # Verificar si ha habido cambios en año, colegio o curso
        if (
            'last_year' not in st.session_state or
            'last_school' not in st.session_state or
            'last_course' not in st.session_state or
            st.session_state.selected_year != st.session_state.last_year or
            st.session_state.selected_school != st.session_state.last_school or
            st.session_state.selected_course != st.session_state.last_course
        ):
            # Actualizar los valores actuales en la sesión
            st.session_state.last_year = st.session_state.selected_year
            st.session_state.last_school = st.session_state.selected_school
            st.session_state.last_course = st.session_state.selected_course

            # Actualizar datos dependientes
            st.session_state.attendance_data = get_attendance_by_course(selected_course_id)
            st.session_state.detailed_attendance = fetch_detailed_attendance_by_course(selected_course_id)
            st.session_state.evaluations_data = fetch_evaluations_by_course(selected_course_id)
            st.session_state.users_data = get_users_by_course(selected_course_id)

        # Sección de asistencia
        with st.expander("Asistencia", expanded=True):
            attendance_data = st.session_state.attendance_data
            display_course_attendance_chart(attendance_data)

            detailed_attendance = st.session_state.detailed_attendance
            if not detailed_attendance.empty:
                detailed_attendance = format_attendance_data(detailed_attendance)
                st.write("Ranking de asistencia")
                st.dataframe(detailed_attendance, use_container_width=True)

            dates = attendance_data['class_date'].unique().tolist()
            selected_date, attendance_filter = display_attendance_filters(dates)

            if selected_date:
                display_filtered_attendance(selected_course_id, selected_date, attendance_filter)

        # Sección de evaluaciones
        with st.expander("Evaluaciones", expanded=True):
            evaluations_data = st.session_state.evaluations_data
            if not evaluations_data.empty:
                display_evaluation_filters(evaluations_data, selected_course_id)
            else:
                st.write("No se encontraron evaluaciones para este curso.")

        # Sección de usuarios
        with st.expander("Usuarios", expanded=True):
            display_user_filters()

def format_attendance_data(detailed_attendance):
    # Obtiene las fechas para renombrar columnas y les agrega "/" cada dos caracteres
    date_t = '/'.join(detailed_attendance.loc[0, 'date_t'][i:i+2] for i in range(0, len(detailed_attendance.loc[0, 'date_t']), 2))
    date_t1 = '/'.join(detailed_attendance.loc[0, 'date_t1'][i:i+2] for i in range(0, len(detailed_attendance.loc[0, 'date_t1']), 2))
    date_t2 = '/'.join(detailed_attendance.loc[0, 'date_t2'][i:i+2] for i in range(0, len(detailed_attendance.loc[0, 'date_t2']), 2))

    # Renombra las columnas de asistencia con las fechas formateadas
    detailed_attendance = detailed_attendance.rename(columns={
        'attended_t': date_t,
        'attended_t1': date_t1,
        'attended_t2': date_t2
    })

    # Convierte 0 y 1 en los íconos de check y cruz
    for date_column in [date_t, date_t1, date_t2]:
        detailed_attendance[date_column] = detailed_attendance[date_column].apply(lambda x: '✅' if x == 1 else '❌')

    # Formatea el porcentaje de asistencia total como un entero sin decimales y con símbolo de %
    detailed_attendance['total_attendance_percentage'] = detailed_attendance['total_attendance_percentage'].apply(lambda x: f"{x:.0f}%")

    # Retorna el DataFrame con las columnas renombradas y el formateo aplicado
    return detailed_attendance[['name', 'lastName', date_t2, date_t1, date_t, 'total_attendance_percentage']]


def display_attendance_filters(dates):
    col1, col2 = st.columns(2)
    with col1:
        selected_date = st.selectbox("Selecciona una fecha", dates[::-1])
    with col2:
        attendance_filter = st.selectbox("Filtrar por asistencia", ["Ausentes", "Presentes"])
    return selected_date, attendance_filter

def display_filtered_attendance(course_id, selected_date, attendance_filter):
    attendance_status = get_attendance_by_date(course_id, selected_date)
    present_students = attendance_status[attendance_status['attendance_status'] == 'present']
    absent_students = attendance_status[attendance_status['attendance_status'] == 'absent']
    filtered_data = present_students if attendance_filter == "Presentes" else absent_students
    st.dataframe(filtered_data[['name', 'lastName', 'phone']], use_container_width=True)

def display_evaluation_filters(evaluations_data, course_id):
    assessment_type_mapping = {row['assessment_type_name']: row['assessment_type_id'] for _, row in evaluations_data.iterrows()}
    selected_assessment_type_name = st.selectbox("Selecciona un tipo de evaluación", list(assessment_type_mapping.keys()))

    if selected_assessment_type_name in assessment_type_mapping:
        selected_assessment_type_id = assessment_type_mapping[selected_assessment_type_name]
        performance_data = get_performance_by_assessment_type(course_id, selected_assessment_type_id)
        display_assessment_performance_chart(performance_data)
        display_specific_evaluation_filter(evaluations_data, selected_assessment_type_id, course_id)

def display_specific_evaluation_filter(evaluations_data, selected_assessment_type_id, course_id):
    selected_assessments = evaluations_data[evaluations_data['assessment_type_id'] == selected_assessment_type_id]
    assessment_ids = selected_assessments['assessment_id'].tolist()
    evaluation_names = selected_assessments['assessment_name'].tolist()

    if evaluation_names:
        selected_evaluation_name = st.selectbox("Selecciona una evaluación", evaluation_names)
        selected_assessment_id = assessment_ids[evaluation_names.index(selected_evaluation_name)]
        st.session_state.selected_assessment_id = selected_assessment_id
        assessment_data = fetch_data_by_assessment_id(course_id, selected_assessment_id)

        filter_option = st.selectbox("Filtrar por:", ["Presentes", "Ausentes"])
        filtered_data = assessment_data[assessment_data["absent_users"] == (0 if filter_option == "Presentes" else 1)]
        
        st.dataframe(filtered_data.drop(columns=["absent_users"]), use_container_width=True)

def display_user_filters():
    user_data = st.session_state.users_data
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
    st.dataframe(user_data[columns_to_display], use_container_width=True)

    display_user_charts_general(user_data)

    # Conditionally display user education based on the role filter
    # if role_filter != "Alumnos":
    #     display_user_education(user_data)
