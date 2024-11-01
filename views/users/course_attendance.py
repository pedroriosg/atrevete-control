import plotly.graph_objects as go
import numpy as np
import streamlit as st

import plotly.graph_objects as go
import numpy as np
import streamlit as st

def display_course_attendance_chart(attendance_data):
    if attendance_data is not None and not attendance_data.empty:
        # Modificar las etiquetas del eje X con un '/' cada dos caracteres solo si ya no hay /

        if '/' not in attendance_data['class_date'].iloc[0]:
            attendance_data['class_date'] = attendance_data['class_date'].apply(
                lambda x: '/'.join([x[i:i+2] for i in range(0, len(x), 2)])
            )

        fig = go.Figure()

        # Añadiendo la traza para el porcentaje de asistencia
        fig.add_trace(go.Scatter(
            x=attendance_data['class_date'],
            y=attendance_data['attendance_percentage'],
            mode='lines+markers+text',
            name='Porcentaje de asistencia',
            line=dict(color='blue', width=2),
            marker=dict(size=4),
            text=attendance_data['attended_count'],
            textposition='top center',
            hovertemplate='Cantidad: %{text}<br>Porcentaje: %{y:.2f}%',
            showlegend=True
        ))

        # Calcular la asistencia promedio
        average_attendance = attendance_data['attendance_percentage'].mean()

        # Añadiendo la línea de tendencia
        x_vals = np.arange(len(attendance_data))
        trendline = np.polyfit(x_vals, attendance_data['attendance_percentage'], 1)
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
            name=f"Asistencia promedio ({average_attendance:.0f}%)",
            line=dict(color='green', width=2, dash='dash')
        ))

        # Configurando el diseño del gráfico
        fig.update_layout(
            title='Asistencia total del curso en el tiempo',
            yaxis_title='Porcentaje de asistencia (%)',
            xaxis_tickangle=-90,
            yaxis=dict(range=[-5, 100]),
            template='plotly_white'
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig)
    else:
        st.write("No hay datos de asistencia disponibles.")
