import streamlit as st
from modules.query import select_result, fetch_image
import pandas as pd 
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import cv2
from PIL import Image

option_list = ['option1', 'option2']

option = st.selectbox(label = "옵션 선택", options = option_list, index = 0, disabled = False)

url = 'https://www.youtube.com/watch?v=FnPF60zjUu0'
st.video(url)