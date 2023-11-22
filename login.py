import streamlit as st
import requests
import json
from flask import Flask, request
from modules.query import login, signup

## https://blog.streamlit.io/streamlit-authenticator-part-1-adding-an-authentication-component-to-your-app/ 

def main():
    st.subheader("Login to your account")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        response = login(username, password)
        
        if response.status_code == 200:
            st.write("Logged in successfully.")
        else:
            st.write("Failed to log in.")
        
    st.subheader("Or create a new account")
    new_username = st.text_input("New username")
    new_password = st.text_input("New password", type='password')

    if st.button("Sign up"):
        response = signup(new_username, new_password)
        
        if response.status_code == 201:
            st.write("Registered successfully.")
        else:
            st.write("Failed to register.")
    

if __name__=="__main__":
    main()