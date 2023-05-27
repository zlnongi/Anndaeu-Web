import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av

def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")

    flipped = img[::-1,:,:] if flip else img

    return av.VideoFrame.from_ndarray(flipped, format="bgr24")

with st.sidebar:
    choose = st.radio(
        "안면 대칭 is YOU",
        ["홈", "진단하기", "마이페이지", "교정운동하기"],
        index=0,
        key="main_menu",
    )

if choose == "진단하기":
    flip = st.checkbox("Flip")

    webrtc_streamer(
        key="example",
        video_frame_callback=video_frame_callback
    )
elif choose == "마이페이지":
    sub_menu = st.radio(
        "마이페이지",
        ["진단결과보기", "개인정보수정"],
        index=0,
        key="sub_menu",
    )

    if sub_menu == "진단결과보기":
        st.write("진단 결과를 표시하는 부분입니다.")
        # 진단결과 표시하는 코드를 작성하세요.

    elif sub_menu == "개인정보수정":
        st.write("개인정보 수정하는 부분입니다.")
        # 개인정보 수정하는 코드를 작성하세요.
