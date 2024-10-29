import streamlit as st

def display_user_table(filtered_data):
    st.dataframe(filtered_data)
