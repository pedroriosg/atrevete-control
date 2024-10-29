import plotly.graph_objects as go
import numpy as np
import streamlit as st

def display_course_attendance_chart(attendance_data):
    if attendance_data is not None and not attendance_data.empty:
        fig = go.Figure()

        # Añadiendo la traza para el porcentaje de asistencia
        fig.add_trace(go.Scatter(
            x=attendance_data['class_date'],
            y=attendance_data['attendance_percentage'],
            mode='lines+markers+text',  # Asegúrate de que 'text' esté habilitado
            name='Porcentaje de Asistencia',
            line=dict(color='blue', width=2),
            marker=dict(size=4),
            text=attendance_data['attended_count'],  # Añadir attendees como texto
            textposition='top center',  # Posición del texto encima de los puntos
            hovertemplate='Cantidad: %{text}<br>Porcentaje: %{y:.2f}%',  # Formato de hover
            showlegend=True  # Si deseas mostrar la leyenda
        ))

        # Calcular la asistencia promedio
        average_attendance = attendance_data['attendance_percentage'].mean()

        # Añadiendo la línea de tendencia
        x_vals = np.arange(len(attendance_data))
        trendline = np.polyfit(x_vals, attendance_data['attendance_percentage'], 1)  # Ajustar una línea de tendencia
        trend = np.polyval(trendline, x_vals)

        fig.add_trace(go.Scatter(
            x=attendance_data['class_date'],
            y=trend,
            mode='lines',
            name='Tendencia',
            line=dict(color='red', width=1, dash='dash')
        ))

        # Añadiendo la línea horizontal para la asistencia promedio
        fig.add_trace(go.Scatter(
            x=attendance_data['class_date'],
            y=[average_attendance] * len(attendance_data),
            mode='lines',
            name=f"Asistencia Promedio ({average_attendance:.0f}%)",
            line=dict(color='green', width=2, dash='dash')
        ))

        # Configurando el diseño del gráfico
        fig.update_layout(
            xaxis_title='Fecha de clase',
            yaxis_title='Porcentaje de asistencia (%)',
            xaxis_tickangle=-90,
            yaxis=dict(range=[-5, 100]),  # Ajusta el límite inferior aquí
            template='plotly_white'
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig)
    else:
        st.write("No hay datos de asistencia disponibles.")
