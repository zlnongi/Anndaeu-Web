import requests

server_url = "http://cychoi.iptime.org:7659"

def check_user(username, password):
    response = requests.post(server_url + "/check_user", json={"username": username, "password": password})
    return response

def select_result(username, password):
    response = requests.post(server_url + "/select_result", json={"username": username, "password": password})
    return response


def signup(username, password):
    response = requests.post(server_url + "/signup", json={"username": username, "password": password})
    
    # if response.status_code == 201:
    #     st.write("Registered successfully.")
    # else:
    #     st.write("Failed to register.")
    return response

def fetch_image(img_path):
    response = requests.post(server_url + "/fetch_image", json={"img_path": img_path})
    return response