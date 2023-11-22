import streamlit as st
from modules.query import select_result, fetch_image
import pandas as pd 
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import cv2
from PIL import Image

new_username = st.text_input("New username")
new_password = st.text_input("New password", type='password')

if st.button("조회하기"):
    response = select_result(new_username, new_password)
    
    if response.status_code == 200: 
        st.session_state.data_table = pd.DataFrame(response.json())

if 'data_table' in st.session_state:
    gb = GridOptionsBuilder.from_dataframe(st.session_state.data_table)
    gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
    gb.configure_side_bar() #Add a sidebar
    gb.configure_selection('single', use_checkbox=True, groupSelectsChildren="Group checkbox select children") # Enable multi-row selection
    gridOptions = gb.build()
    grid_response = AgGrid(
        st.session_state.data_table,
        gridOptions=gridOptions,
        data_return_mode='AS_INPUT',
        update_mode='MODEL_CHANGED',
        fit_columns_on_grid_load=False,
        theme='streamlit', #Add theme color to the table
        enable_enterprise_modules=True,
        height=300,
        width='100%',
        reload_data=False
    )
    st.session_state.data_table = grid_response['data']
    selected_data = pd.DataFrame(grid_response['selected_rows']).reset_index(drop=True)
        
    # 선택된 데이터 View
    if len(selected_data) == 1: 
        response = fetch_image(selected_data.iloc[0]['img_path'])
        from io import BytesIO
        img = Image.open(BytesIO(response.content))
        st.image(img, caption='Image from server', use_column_width=True)
    
# if len(selected_data) >= 2:
#     base_parts = selected_data.iloc[:-1]
# attach_part = selected_data.iloc[-1]

# # 여러개 선택 시 마지막 제외하고 나머지에 대해 Voxel 구성 
# base_npy_list = []
# for i in range(len(base_parts)):
#     row = base_parts.iloc[i]
#     base_npy = np.load(f'./dataset/{car_type}/preprocess/voxel/{row.라인}/{row.UPG}/' + row.parts + '.npy')
#     base_npy_list.append(base_npy)    
# base_npys = np.vstack(base_npy_list)
# # print("base_npys ---: ", base_npys.shape)

# # 선택한 데이터들 중 마지막에 대해 Voxel 구성 
# last_npy = np.load(f'./dataset/{car_type}/preprocess/voxel/{attach_part.라인}/{attach_part.UPG}/' + attach_part.parts + '.npy')

# # f_fig = get_single_fig(last_npy)
# f_fig = get_pair_fig(base_npys, last_npy)
# st.plotly_chart(f_fig, use_container_width = True)


# min_distance = get_closest_dist(base_npys, last_npy)
# print(min_distance)