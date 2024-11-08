import streamlit as st
from panel.general_panel import display_general_panel
from panel.course_panel import display_course_panel

# Configuración de la página
st.set_page_config(
    page_title="Panel de Control - Fundación Educacional Atrévete",
    layout="wide",
    page_icon="icon.png"  # Cambia esta ruta al ícono real
)

# Clave para desbloquear la vista
secret_key = st.secrets["secret_key"]

# Usa una variable de sesión para controlar si la clave se ha ingresado correctamente
if 'key_entered' not in st.session_state:
    st.session_state.key_entered = False

# Variable de sesión para la opción seleccionada en el menú
if 'menu_selection' not in st.session_state:
    st.session_state.menu_selection = "Mi curso"  # Selecciona "Nosotros" por defecto

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


    # Opciones del menú con botones de ancho completo
    if st.sidebar.button("Mi curso", use_container_width=True, key="mi_curso_button"):
        st.session_state.menu_selection = "Mi curso"
    if st.sidebar.button("Nosotros", use_container_width=True, key="nosotros_button"):
        st.session_state.menu_selection = "Nosotros"
        
    # Agrega un botón para limpiar el cache de datos
    if st.button("Limpiar caché de datos", use_container_width=True):
        st.cache_data.clear()  # Limpia la caché
        st.success("La caché de datos ha sido limpiada exitosamente.")

    # Muestra el contenido basado en la selección del menú
    if st.session_state.menu_selection == "Nosotros":
        display_general_panel()
    elif st.session_state.menu_selection == "Mi curso":
        display_course_panel()

    # Estilo para resaltar el botón activo
    st.markdown(
        f"""
        <style>
        div[role="button"][aria-label="Nosotros"] {{
            background-color: {'#add8e6' if st.session_state.menu_selection == "Nosotros" else '#f0f0f0'};
        }}
        div[role="button"][aria-label="Mi curso"] {{
            background-color: {'#add8e6' if st.session_state.menu_selection == "Mi curso" else '#f0f0f0'};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
