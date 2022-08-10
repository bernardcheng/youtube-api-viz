import streamlit as st
import pandas as pd
import numpy as np
import api_helper as api

def form_callback():
    st.write(st.session_state.text_search)
    df = pd.DataFrame({
        'first column': [1, 2, 3, 4],
        'second column': [10, 20, 30, 40],
    })
    st.write(df)

# with st.form(key='input_form'):
#     search = st.text_input('Search Input', key='text_search')
#     submit_button = st.form_submit_button(label='Submit', on_click=form_callback)
with st.sidebar:
    st.title('Youtube Channel Surf')
    with st.form(key='input_form'):
        api_key = st.text_input('API Key', key='api_key')
        search = st.text_input('Search Input', key='text_search')
        submit_button = st.form_submit_button(label='Submit', on_click=form_callback)
    

# container = st.container()
# if search:
#     container.write(df)