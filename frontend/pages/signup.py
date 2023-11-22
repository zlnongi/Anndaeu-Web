import streamlit as st
import requests
import json
from flask import Flask, request
from modules.query import signup
# import streamlit_authenticator as stauth

## https://blog.streamlit.io/streamlit-authenticator-part-1-adding-an-authentication-component-to-your-app/ 

base_url = "http://cychoi.iptime.org:7659"


st.subheader("Create a new account")
new_username = st.text_input("New username")
new_password = st.text_input("New password", type='password')

    
if st.button("Sign up"):
    response = signup(new_username, new_password)
    
    if response.status_code == 201:
        st.write("Registered successfully.")
    else:
        st.write("Failed to register.")