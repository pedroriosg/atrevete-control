import streamlit as st
import pandas as pd
from queries import fetch_users
from views.users.user_charts import display_user_charts_general
from views.users.user_education import display_user_education


@st.cache_data
def get_users():
    return fetch_users()

def display_user_panel():
    role_filter = st.selectbox("", ["Todos", "Profesores", "Alumnos"])
    
    with st.expander("Usuarios", expanded=True):
        user_data = fetch_users()
        columns_to_display = ["name", "lastName", "rut", "email", "birthday", "phone", "emergencyName", "emergencyNumber", "emergencyRelationship"]
        filtered_data_display = user_data[columns_to_display].copy()
        filtered_data_display['birthday'] = pd.to_datetime(filtered_data_display['birthday']).dt.date
        st.dataframe(filtered_data_display, use_container_width=True)
        display_user_charts_general(user_data)
        if role_filter == "Profesores":
            display_user_education(user_data)
