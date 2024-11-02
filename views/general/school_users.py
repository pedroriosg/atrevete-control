import plotly.graph_objects as go
import streamlit as st

def display_team_by_year_chart(team_data):
    if team_data is not None and not team_data.empty:
        fig = go.Figure()

        # Añadir barra para el conteo de estudiantes
        fig.add_trace(go.Bar(
            x=team_data['school_name'],
            y=team_data['student_count'],
            name='Alumnos',
            marker_color='#2e5f7a',  # Color para estudiantes
            text=team_data['student_count'],
            textposition='outside',  # Pone la etiqueta de número encima de la barra
            width=0.15,  # Ajustar el ancho de las barras
            hoverinfo='skip'
        ))

        # Añadir barra para el conteo de profesores
        fig.add_trace(go.Bar(
            x=team_data['school_name'],
            y=team_data['teacher_count'],
            name='Profesores',
            marker_color='#193b56',  # Color para profesores
            text=team_data['teacher_count'],
            textposition='outside',  # Pone la etiqueta de número encima de la barra
            width=0.15,  # Ajustar el ancho de las barras
            hoverinfo='skip'
        ))

        # Configuración del diseño del gráfico
        fig.update_layout(
            title='Cantidad de alumnos y profesores por colegio',
            barmode='group',  # Agrupa barras de 'student' y 'teacher' para cada colegio
            template='plotly_white',
            margin=dict(b=100),  # Aumentar margen inferior para la nota
        )

        # Ajustar el rango del eje y para dejar espacio adicional
        fig.update_yaxes(range=[0, team_data[['student_count', 'teacher_count']].values.max() * 1.2])

        # Añadir la nota debajo del gráfico
        # fig.add_annotation(
        #     text="La cantidad de profesores incorpora al jefe de colegio y a los dos jefes generales",
        #     showarrow=False,
        #     xref="paper", yref="paper",
        #     x=0, y=-0.40,  # Posición de la nota
        #     font=dict(size=12),
        #     align="center"
        # )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig)
    else:
        st.write("No hay datos de usuarios disponibles para el año seleccionado.")

def display_students_by_grade_chart(schools_users_details, user_role):

    if user_role == 'student':
        title = 'Cantidad de alumnos por materia y grado'
        y_label = 'Cantidad de alumnos'
    else:
        title = 'Cantidad de profesores por materia y grado'
        y_label = 'Cantidad de profesores'

    if schools_users_details is not None and not schools_users_details.empty:
        fig = go.Figure()

        # Definir colores para cada materia
        subject_colors = {
            'Lenguaje': '#e20059',
            'Matemáticas': '#193b56',
            'Ciencias': '#ff740d',
            'Historia': '#ffbb37'
        }

        # Obtener los grados y materias únicos
        grades = schools_users_details['grade_name'].unique()
        subjects = schools_users_details['subject_name'].unique()

        # Crear una barra para cada materia en cada grado
        for subject in subjects:
            # Filtrar datos para el subject específico
            subject_data = schools_users_details[schools_users_details['subject_name'] == subject]
            
            # Añadir barra para cada subject en cada grado
            fig.add_trace(go.Bar(
                x=subject_data['grade_name'],
                y=subject_data['student_count'],
                name=subject,  # Nombre de la materia
                text=subject_data['student_count'],
                textposition='outside',  # Etiquetas de cantidad encima de la barra
                width=0.15,  # Ajuste de ancho para mejor separación
                marker_color=subject_colors.get(subject, '#000000'),  # Obtener el color de la materia, por defecto negro
                hoverinfo='skip'
            ))


        # Configuración del diseño del gráfico
        fig.update_layout(
            title=title,
            yaxis_title=y_label,
            barmode='group',  # Agrupa las barras por grado
            bargap=0.3,  # Espaciado entre grupos de barras
            bargroupgap=0.15,  # Espaciado entre barras dentro de cada grupo
            template='plotly_white',
            xaxis=dict(tickmode='linear'),  # Asegura que todos los grados se muestren
            margin=dict(b=100),  # Aumenta margen inferior para la nota
        )

        fig.update_yaxes(range=[0, schools_users_details['student_count'].max() * 1.5])

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig)
    else:
        st.write("No hay datos de estudiantes disponibles para la escuela seleccionada.")
