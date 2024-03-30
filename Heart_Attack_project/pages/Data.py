# Import necessary libraries
import pandas as pd 
import streamlit as st 

from zipfile import ZipFile
zip_file_path = 'Heart_Attack_project/Sourse/heart_2022_with_nans.zip'
with ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall()
extracted_files = zip_ref.namelist()
csv_file_name = extracted_files[0] 
df = pd.read_csv(csv_file_name)

# Title for the page
st.markdown(" <center>  <h1> Heart Disease Dataset </h1> </font> </center> </h1> ",
            unsafe_allow_html=True)

# Displaying information about the dataset before cleaning and preprocessing
st.write('Heart Disease Dataset Before Cleaning And Preprocessing:')

# Providing a link to the original dataset
st.markdown('<a href="https://www.kaggle.com/datasets/kamilpytlak/personal-key-indicators-of-heart-disease"> <center> Link to Dataset  </center> </a> ', unsafe_allow_html=True)

# Reading and displaying the dataset before cleaning and preprocessing
#df = pd.read_csv("./Heart_Attack_project/Sourse/heart_2022_with_nans.zip", compression='gzip')
st.write(df)

# Displaying information about the dataset after cleaning and preprocessing
st.write('Heart Disease Dataset After Cleaning And Preprocessing:')

# Providing a link to the cleaned dataset
st.markdown('<a href="https://drive.google.com/file/d/1-v58el0--iKMBrYizO8XEi13VJYyc0mA/view?usp=sharing"> <center> Link to Dataset  </center> </a> ', unsafe_allow_html=True)

# Reading and displaying the cleaned dataset
df = pd.read_csv("./Heart_Attack_project/Sourse/cleaned_data.zip", compression='gzip')
st.write(df)
