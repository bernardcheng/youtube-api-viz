import streamlit as st
import pandas as pd
import numpy as np
import spacy
from api_helper import *

# Set globals
nlp = spacy.load("en_core_web_lg")

def form_callback():
    st.write('Similar Channels:')

    with st.spinner('Loading...'):
        search_results_link = searchChannelInfo(st.session_state.api_key, st.session_state.text_search, max_results=st.session_state.max_results, use_link=True)
        keywords = extractKeywords(parseSearch(search_results_link), st.session_state.api_key, nlp)
        filterResults = filterSearch(st.session_state.text_search, keywords, st.session_state.api_key, nlp, filter_percentile=st.session_state.sim_filter/100)
        results_df = pd.DataFrame(filterResults)
        st.write(results_df[['channel','viewCount','subscriberCount','videoCount','sim_score']])

with st.sidebar:
    st.title('Youtube Channel Surf')
    with st.form(key='input_form'):
        api_key = st.text_input('API Key', key='api_key', help='Auto-generated API Key when you create a project. See official documentation for details: https://developers.google.com/youtube/registering_an_application')
        search = st.text_input('Search Input', key='text_search', help='Accepted input format: Any youtube video link. For example: https://www.youtube.com/watch?v=a1b2c3d4e5f')
        maxResults = st.slider('Max Search Results', 1, 50, 50, key='max_results', help='Maximum number of results to be returned.')
        threshold = st.slider('Similarity Filter Threshold', 1, 100, 50, key='sim_filter', help='Channels with similarity score of input threshold or higher will be returned after search. (Higher threshold corresponds to more similar channels returned)')
        submit_button = st.form_submit_button(label='Submit', on_click=form_callback)
    
