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

# Clave para desbloquear la vista
secret_key = st.secrets["PASSWORD"]

# Usa una variable de sesión para controlar si la clave se ha ingresado correctamente
if 'key_entered' not in st.session_state:
    st.session_state.key_entered = False

# Crear un contenedor vacío para el input de la clave
key_input_container = st.empty()

# Si la clave no se ha ingresado correctamente, mostrar el input
if not st.session_state.key_entered:
    # Oculta la barra lateral
    st.sidebar.empty()
    
    # Muestra el input para la clave
    user_input = key_input_container.text_input("Contraseña para desbloquear", type="password")
    
    # Verifica si la clave es correcta
    if user_input == secret_key:
        st.session_state.key_entered = True
        key_input_container.empty()  # Limpia el contenedor del input

# Si la clave es correcta, muestra el contenido
if st.session_state.key_entered:
    # Muestra la barra lateral nuevamente si es necesario (opcional)
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

    # Muestra el contenido basado en la selección del menú
    if menu_selection == "Mi curso":
        display_course_panel()
    # elif menu_selection == "Panel General":
    #     display_general_panel()
    # elif menu_selection == "Usuarios":
    #     display_user_panel()
