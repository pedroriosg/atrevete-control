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

menu_options = {
    
    "Mi curso": "Mi curso",
}
menu_selection = st.sidebar.selectbox("", list(menu_options.keys()), format_func=lambda x: menu_options[x])

if menu_selection == "Panel General":
    display_general_panel()

# elif menu_selection == "Usuarios":
#     display_user_panel()

# elif menu_selection == "Mi curso":
#     display_course_panel()
