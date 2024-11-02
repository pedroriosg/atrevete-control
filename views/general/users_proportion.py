import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def display_user_charts(type_user_proportion, student_grade_proportion, teacher_grade_proportion):

    # Crear tres columnas
    col1, col2, col3 = st.columns(3)

    # Gráfico de proporción de usuarios
    with col1:
        # Cambiar nombres de roles
        type_user_proportion['user_role'] = type_user_proportion['user_role'].replace({
            'student': 'Alumnos',
            'teacher': 'Profesores'
        })

        total_users = type_user_proportion['user_count'].sum()  # Calcular el total de usuarios

        # Crear el gráfico de torta
        fig = go.Figure(data=[go.Pie(
            labels=type_user_proportion['user_role'],
            values=type_user_proportion['user_count'],
            textinfo="label+value",  # Mostrar etiqueta y valor
            insidetextorientation="radial"  # Orientación del texto dentro de la torta
        )])

        # Personalizar el layout
        fig.update_layout(
            title="Este año somos {} personas".format(total_users),
            showlegend=True,  # Asegúrate de que las leyendas se muestren
            legend=dict(
                orientation="h",  # Leyenda horizontal
                yanchor="bottom",  # Anclar al fondo
                y=-0.3,  # Ajustar la posición vertical
                xanchor="center",  # Anclar al centro
                x=0.5  # Centrar horizontalmente
            )
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig, use_container_width=True)

    # Gráfico de proporción de alumnos por grado
    with col2:
        # Crear el gráfico de torta
        fig_students = go.Figure(data=[go.Pie(
            labels=student_grade_proportion['grade_name'],
            values=student_grade_proportion['user_count'],
            textinfo="label+value",  # Mostrar etiqueta y valor
            insidetextorientation="radial"  # Orientación del texto dentro de la torta
        )])

        # Personalizar el layout
        fig_students.update_layout(
            title="Proporción de alumnos por grado",
            showlegend=True,  # Asegúrate de que las leyendas se muestren
            legend=dict(
                            orientation="h",  # Leyenda horizontal
                            yanchor="bottom",  # Anclar al fondo
                            y=-0.3,  # Ajustar la posición vertical
                            xanchor="center",  # Anclar al centro
                            x=0.5  # Centrar horizontalmente
                        )
                    )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig_students, use_container_width=True)

    # Gráfico de proporción de profesores por grado
    with col3:
        # Crear el gráfico de torta
        fig_teachers = go.Figure(data=[go.Pie(
            labels=teacher_grade_proportion['grade_name'],
            values=teacher_grade_proportion['user_count'],
            textinfo="label+value",  # Mostrar etiqueta y valor
            insidetextorientation="radial"  # Orientación del texto dentro de la torta
        )])

        # Personalizar el layout
        fig_teachers.update_layout(
            title="Proporción de profesores por grado",
            showlegend=True,  # Asegúrate de que las leyendas se muestren
            legend=dict(
                orientation="h",  # Leyenda horizontal
                yanchor="bottom",  # Anclar al fondo
                y=-0.3,  # Ajustar la posición vertical
                xanchor="center",  # Anclar al centro
                x=0.5  # Centrar horizontalmente
            )
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig_teachers, use_container_width=True)
