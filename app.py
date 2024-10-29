import streamlit as st
from panel.general_panel import display_general_panel
from panel.course_panel import display_course_panel
from panel.user_panel import display_user_panel

# Configuración de la página
st.set_page_config(
    page_title="Panel de Control - Fundación Educacional Atrévete",
    layout="wide",
    page_icon="icon.png"  # Cambia esta ruta al ícono real
)

# Agrega el ícono en la parte superior de la barra lateral usando columnas para centrarlo
with st.sidebar:
    cols = st.columns([1, 2, 1])  # Define columnas con proporciones para centrar el ícono
    with cols[1]:  # La columna central
        st.image("ablue.png", use_column_width=True)

# Opciones del menú
menu_options = {
    "Mi curso": "Mi curso",
    # "Usuarios": "Usuarios"
}
menu_selection = st.sidebar.selectbox("", list(menu_options.keys()), format_func=lambda x: menu_options[x])

if menu_selection == "Mi curso":
    display_course_panel()

# elif menu_selection == "Panel General":
#     display_general_panel()

# elif menu_selection == "Usuarios
