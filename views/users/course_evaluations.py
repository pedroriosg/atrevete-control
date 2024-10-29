import plotly.graph_objects as go
import numpy as np
import streamlit as st

def display_assessment_performance_chart(performance_data):
    if performance_data and len(performance_data) > 0:
        fig = go.Figure()

        # Extraer datos relevantes de performance_data
        ausentes = [item['absent_users'] for item in performance_data]
        total = [item['total_users'] for item in performance_data]
        asistencia = [item['attendance_percentage'] for item in performance_data]

        # Calcular el rendimiento promedio y porcentaje de asistencia promedio
        average_performance = np.mean([item['average_performance'] for item in performance_data])
        average_attendance = np.mean(asistencia)

        # Añadiendo la traza para el rendimiento promedio por evaluación
        fig.add_trace(go.Scatter(
            x=[item['assessment_name'] for item in performance_data],
            y=[item['average_performance'] for item in performance_data],
            mode='lines+markers+text',
            name=f'Rendimiento promedio ({average_performance:.0f}%)',
            line=dict(color='blue', width=2),
            marker=dict(size=4),
            text=[f"{item['average_performance']:.0f}%" for item in performance_data],  # Sin decimal
            textposition='bottom center',
            textfont=dict(color='blue'),  # Color del texto igual al de la línea
            showlegend=True,
            hoverinfo='skip'
        ))

        # Añadiendo la traza para el porcentaje de asistencia
        fig.add_trace(go.Scatter(
            x=[item['assessment_name'] for item in performance_data],
            y=asistencia,
            mode='lines+markers+text',
            name=f'Asistencia promedio ({average_attendance:.0f}%)',
            line=dict(color='gray', width=0.5, dash='dash'),
            marker=dict(size=4),
            text=[f"{item['attendance_percentage']:.0f}%" for item in performance_data],  # Sin decimal
            textposition='top center',  # Posiciona los números debajo de los puntos
            textfont=dict(color='gray'),  # Color del texto igual al de la línea
            showlegend=True,
            customdata=np.array([asistencia, ausentes, total]).T,  # Combina datos personalizados
            hovertemplate='Ausentes: %{customdata[1]} de %{customdata[2]}'
        ))

        # Configurando el diseño del gráfico
        fig.update_layout(
            xaxis_tickangle=-90,
            yaxis=dict(range=[-5, 100]),  # Ajusta el límite inferior aquí
            template='plotly_white'
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig)
    else:
        st.write("No hay datos de rendimiento de evaluaciones disponibles.")
