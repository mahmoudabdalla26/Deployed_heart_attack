# Import necessary libraries
import numpy as np 
import pandas as pd 
import streamlit as st 
from PIL import Image 

# Title 
st.markdown(" <center>  <h1>  Heart Disease Analysis </h1> </font> </center> </h1> ",
            unsafe_allow_html=True)

# About the project
st.markdown(''' <center>  <h6>
    This app is created to analyze the data of a heart disease. </center> </h6> ''', unsafe_allow_html=True)

# Open the image file
image = Image.open(r"C:\Users\Lenovo\Desktop\mid\Heart_Attack_project\Sourse\image.jpeg")

# Define desired width and height
desired_width = 300
desired_height = 200

# Resize the image
resized_image = image.resize((desired_width, desired_height))

# Display the resized image using Streamlit
st.image(resized_image, caption='Resized Image', use_column_width=True)

