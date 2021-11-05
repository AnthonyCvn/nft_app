import streamlit as st
import pandas as pd
import numpy as np
import scraping_function as sf

# Streamlit title and text
st.title("Alright this is awesome")

# Get the data from 
data_load_state = st.text('Loading data...')

df_nft = sf.get_dataframe_raritytool()


data_load_state.text("Data are loaded")


st.write(df_nft)




