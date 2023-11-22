
import numpy as np 
import streamlit as st
from PIL import Image
import cv2
import numpy as np
import time 
from imutils import face_utils
import dlib
import requests
from modules.utils import load_config
import io 
from modules.query import check_user

class Metric():
    def __init__(self, points:np.array) -> None:
        self.points = points 

        self.link = {
            'rest':
                {
                    '1':((19, 37), (24, 44)),
                    '2':((20, 38), (23, 43)),
                    '3':((21, 27), (22, 27)),
                    '4':((37, 41), (44, 46)),
                    '5':((38, 40), (43, 47)),
                    '6':((17, 27), (26, 27)),
                    '7':((19, 27), (24, 27)),
                    '8':((36, 50), (45, 52)),
                    '9':((0, 49), (16, 53)),
                    '10':((0, 48), (16, 54)),
                    '11':((3, 48), (13, 54)),
                    '12':((59, 6), (55, 10))
                },
            'say_E':
                {
                    '1':((19, 41), (23, 47)),
                    '2':((20, 40), (24, 46)),
                    '3':((39, 31), (42, 35)),
                    '4':((0, 31), (16, 35)),
                    '5':((36, 50), (45, 52)),
                    '6':((0, 49), (16, 53)),
                    '7':((0, 48), (45, 54)),
                    '8':((36,48 ), (45, 54)),
                    '9':((3, 48), (13, 54)),
                    '10':((59, 5), (55, 11)),
                    '11':((2, 48), (14, 54)),
                    '12':((61, 67), (63, 65))    
                },
            'say_O':
                {
                    '1':((31, 50), (35, 52)),
                    '2':((32, 50), (34, 52)),
                    '3':((2, 48), (14, 54)),
                    '4':((3, 48), (13, 54)),
                    '5':((4, 48), (12, 54)),
                    '6':((5, 48), (11, 54)),
                    '7':((6, 59), (10, 55)),
                    '8':((7,58 ), (9, 56)),
                    '9':((48, 61), (54, 63)),
                    '10':((5, 59), (55, 11))
                },
            'slight_eye_close':
                {
                    '1':((21, 27), (22, 27)),
                    '2':((19, 27), (24, 27)),
                    '3':((17, 27), (26, 27)),
                    '4':((20, 38), (23, 43)),
                    '5':((19, 37), (24, 44)),
                    '6':((17, 36), (26, 45)),
                    '7':((18, 36), (26, 45)),
                    '8':((38,40 ), (43, 47)),
                    '9':((37, 41), (44, 46)),
                    '10':((40, 31), (47, 35)),
                    '11':((41, 48), (46, 54)),
                    '12':((36, 48), (45, 54))  
                },
            'tight_eye_close':
                {
                    '1':((21, 27), (22, 27)),
                    '2':((19, 27), (24, 27)),
                    '3':((17, 27), (26, 27)),
                    '4':((20, 38), (23, 43)),
                    '5':((19, 37), (24, 44)),
                    '6':((17, 36), (25, 45)),
                    '7':((18, 36), (26, 45)),
                    '8':((0,31 ), (16, 35)),
                    '9':((0, 48), (16, 54)),
                    '10':((40, 31), (47, 35)),
                    '11':((41, 48), (46, 54)),
                    '12':((36, 48), (45, 54))  
                },
            'raised_eyebrows':
                {
                    '1':((19, 37), (24, 44)),
                    '2':((20, 38), (23, 43)),
                    '3':((21, 27), (22, 27)),
                    '4':((37, 41), (44, 46)),
                    '5':((38, 40), (43, 47)),
                    '6':((17, 27), (26, 27)),
                    '7':((19, 27), (24, 27)),
                    '8':((17,31 ), (26, 35)),
                    '9':((19, 31), (24, 35)),
                    '10':((21, 31), (22, 35))  
                }
        }
    
    def get_landmark_distance(self, status) -> np.array:
        
        links = self.link[status]
        
        distance_array = np.zeros((len(links), 2))
        
        for link_index, lr_link in enumerate(links.values()):
            for lr_index, link in enumerate(lr_link):
                a, b = self.points[list(link)]
                distance = np.linalg.norm(a - b, 2)
                distance_array[link_index, lr_index] = distance
        return distance_array 

def case1(points:np.array) -> bool:
    pt27 = points[27]
    pt39 = points[39]
    pt42 = points[42]
    pt30 = points[30]
    pt2 = points[2]
    pt14 = points[14]
    distance1 = np.linalg.norm(pt27-pt39, 2)
    distance2 = np.linalg.norm(pt27-pt42,2)
    distance3 = np.linalg.norm(pt30-pt2,2)
    distance4 = np.linalg.norm(pt30-pt14,2)
    if (( 1.05 < distance2/distance1 )&  (distance3 /distance4> 1.05)):
        return True 
    elif ((distance1/distance2>1.05)&(1.05<distance4/distance3)):
        return True
    else:
        return False
    
def case2(points:np.array) -> bool:
    pt27 = points[27]
    pt39 = points[39]
    pt42 = points[42]
    pt30 = points[30]
    pt2 = points[2]
    pt14 = points[14]
    distance1 = np.linalg.norm(pt27-pt39, 2)
    distance2 = np.linalg.norm(pt27-pt42,2)
    distance3 = np.linalg.norm(pt30-pt2,2)
    distance4 = np.linalg.norm(pt30-pt14,2)
    if (( 1.05 < distance1/distance2 )&  (distance3 /distance4> 1.05)):
        return True 
    elif ((distance2/distance1>1.05)&(1.05<distance4/distance3)):
        return True
    else:
        return False
    
    
def case3(points:np.array) -> bool:
    pt59 = points[59]
    pt6 = points[6]
    pt55 = points[55]
    pt30 = points[30]
    pt2 = points[2]
    pt14 = points[14]
    pt10 = points[10]
    pt31 = points[31]
    pt33 = points[33]
    pt35 = points[35]
    pt40 = points[40]
    pt47 = points[47]
    distance1 = np.linalg.norm(pt30-pt2, 2)
    distance2 = np.linalg.norm(pt30-pt14,2)
    distance3 = np.linalg.norm(pt59-pt6,2)
    distance4 = np.linalg.norm(pt55-pt10,2)
    distance5 = np.linalg.norm(pt31-pt33, 2)
    distance6 = np.linalg.norm(pt33-pt35,2)
    distance7 = np.linalg.norm(pt40-pt33,2)
    distance8 = np.linalg.norm(pt47-pt33,2)
    
    if((distance1/distance2>1.05)&(1.05<distance4/distance3)&(distance5/distance6>1.05)&(distance7/distance8>1.05)):
        return True
    
    elif((1.05<distance2/distance1)&(distance3/distance4>1.05)&(1.05<distance6/distance5)&(1.05<distance8/distance7)):
        return True
    else:
        return False


def check_center(landmarks):
    # x center
    landmark_min_x, landmark_min_y = landmarks.min(axis=0)
    landmark_max_x, landmark_max_y = landmarks.max(axis=0)
    
    if (st.session_state.center_area['min_x'] <= landmark_min_x) and (landmark_max_x <= st.session_state.center_area['max_x']) and \
        (st.session_state.center_area['min_y'] <= landmark_min_y) and (landmark_max_y <= st.session_state.center_area['max_y']):
        return True
    
    else: 
        return False

def check_face_frontal(landmarks):
    nose_points = landmarks[[27, 28, 29, 30]]
    
    min_x, _ = nose_points.min(axis=0)
    max_x, _ = nose_points.max(axis=0)
    
    if st.session_state.frontal_area['min_x'] <= min_x  and max_x <= st.session_state.frontal_area['max_x'] :
        return True
    else: 
        return False

server_url = "http://cychoi.iptime.org:7659"
start_angle = 0
radius = 50
thickness = 5 
color = (0, 0, 255) 
capture_time = 3

if __name__=='__main__':
    
    # 이미지 표시할 공간 생성
    image_placeholder = st.empty()

    # 만약 세션에 이미지 존재하면 표시
    if 'pil_image' in st.session_state:
        image_placeholder.image(st.session_state.pil_image, channels="RGB", use_column_width=True)

    info_msg = st.info("얼굴을 인식해주세요", icon="👀")
    # success_msg = st.success('', icon="✅")
    # st.warning("This is a Warning message")
    # error_msg = st.error('', icon="🚨")

    # 버튼 생성
    # diagnosis_button = st.button('진단하기')
    restart_button = st.button("재촬영하기")

    st.subheader("Save to your result")
    username_text = st.text_input("Username")
    password_text = st.text_input("Password", type='password')
    save_button = st.button('저장하기')
    
    # if diagnosis_button:
    #     print('진단')
    #     metric = Metric(st.session_state.landmarks)
    #     st.session_state.result = "정상" # metric.get_landmark_distance('rest')
    #     # st.text('평균 : {}'.format(st.session_state.metric))
    #     diagnosis_button = False
    if restart_button:
        print('비디오 재시작')
        restart_button = False
        st.session_state.video_play = True
    elif save_button:
        print('결과 저장')
        
        response = check_user(username_text, password_text)
        
        if response.status_code == 200 : 
            print('유효한 아이디')
            byte_arr = io.BytesIO()
            st.session_state.pil_image.save(byte_arr, format='JPEG')
            byte_arr.seek(0)
            img_in_bytes = byte_arr.read()
            
            print('서버에 결과 전송중...')
            print(username_text)
            response = requests.post(server_url + "/save_result" , files={"image": img_in_bytes}, data={"result": st.session_state.result, "username": username_text})
            
            if response.ok:
                st.write("The image was successfully uploaded to the server.")
            else:
                st.write("Failed to upload the image.")
            
            save_button = False
        
        elif response.status_code == 401: 
            st.write("존재하지 않는 계정입니다.")

    #-- session state 관리 
    if 'args' not in st.session_state: 
        print('args 로딩중')
        st.session_state.args = load_config('./config/detector.yaml')
    
    if 'elapsed_time' not in st.session_state:
        st.session_state.elapsed_time = 0
    
    if 'detector' not in st.session_state:
        print('detector 로딩중')
        st.session_state.detector = dlib.get_frontal_face_detector()
    
    if 'predictor' not in st.session_state:
        print('predictor 로딩중')
        st.session_state.predictor = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat')

    if 'result' not in st.session_state:
        st.session_state.result = '대칭'

    if 'video_play' not in st.session_state:
        print('video_play true 로 설정')
        st.session_state.video_play = True
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
    if 'video_capture' not in st.session_state:
        print('video_capture 설정')
        image_placeholder.text('카메라를 연결하는 중입니다.')
        
        while True: 
            st.session_state.video_capture = cv2.VideoCapture(0)
            ret, frame = st.session_state.video_capture.read()
            if frame is not None:
                break
        
        print('초기 설정 시작')
        st.session_state.img_h, st.session_state.img_w = frame.shape[0], frame.shape[1]
        st.session_state.center_x = int(st.session_state.img_w * 0.5)
        st.session_state.center_y = int(st.session_state.img_h * 0.5)
        
        # center area
        center_margin_w = int(st.session_state.img_w * 0.5 * st.session_state.args.center_ratio.width)
        center_margin_h = int(st.session_state.img_h * 0.5 * st.session_state.args.center_ratio.height)
        
        st.session_state.center_area = {}
        st.session_state.center_area['min_x'] = st.session_state.center_x - center_margin_w
        st.session_state.center_area['max_x'] = st.session_state.center_x + center_margin_w
        st.session_state.center_area['min_y'] = st.session_state.center_y - center_margin_h
        st.session_state.center_area['max_y'] = st.session_state.center_y + center_margin_h
        
        # face frontal area
        frontal_margin_w = int(st.session_state.img_w * 0.5 * st.session_state.args.face_frontal_ratio.width)
        
        st.session_state.frontal_area = {}
        st.session_state.frontal_area['min_x'] = st.session_state.center_x - frontal_margin_w
        st.session_state.frontal_area['max_x'] = st.session_state.center_x + frontal_margin_w
            
        print('video_capture 설정 끝')
    
    print("st.session_state.video_play : ", st.session_state.video_play)
    st.session_state.start_time = time.time()
    while st.session_state.video_play:
    
        ret, frame = st.session_state.video_capture.read()
        
        if frame is not None:
            color_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # visualize bbox area 
            if st.session_state.args.visualize['center_bbox']:
                cv2.rectangle(
                    color_img, 
                    (st.session_state.center_area['min_x'], st.session_state.center_area['min_y']), 
                    (st.session_state.center_area['max_x'], st.session_state.center_area['max_y']), 
                    (0, 0, 255), 
                    2
                )
            
            if st.session_state.args.visualize['face_frontal_bbox']:
                cv2.rectangle(
                    color_img, 
                    (st.session_state.frontal_area['min_x'], 0), 
                    (st.session_state.frontal_area['max_x'], st.session_state.img_h), 
                    (0, 0, 255), 
                    2
                )
            
            # 얼굴이 존재하는 영역의 BBox 추출 
            rects = st.session_state.detector(gray_img, 1)

            # bbox 수가 0개 또는 2개 이상이면 다시 capture
            if len(rects) == 1:
                for i, rect in enumerate(rects):
                    landmarks = st.session_state.predictor(gray_img, rect)
                    st.session_state.landmarks = face_utils.shape_to_np(landmarks)

                    x, y, w, h = face_utils.rect_to_bb(rect)
                    
                    if st.session_state.args.visualize['detector_bbox']:
                        cv2.rectangle(color_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    if st.session_state.args.visualize['landmark']:
                        for pt_idx, (x, y) in enumerate(st.session_state.landmarks):
                            cv2.circle(color_img, (x, y), 2, (0, 0, 255), -1)
                    
                    #! 특정 잘 됐는지 안됐는지 결정하는 부분
                    # center
                    center_check = check_center(st.session_state.landmarks)
                    
                    # face frontal
                    center_face_frontal = check_face_frontal(st.session_state.landmarks)
                    
                    if center_check and center_face_frontal: # 적절한 사진이 인식된 경우
                        if st.session_state.elapsed_time >= 3 : 
                            st.session_state.video_play = False
                            
                            if(case1(st.session_state.landmarks)==True):
                                st.session_state.result = 'type1 비대칭'
                                st.write("type1 비대칭")
                            elif(case2(st.session_state.landmarks)==True):
                                st.session_state.result = 'type2 비대칭'
                                st.write("type2 비대칭")
                            elif(case3(st.session_state.landmarks)==True):
                                st.session_state.result = 'type3 비대칭'
                                st.write("type3 비대칭")
                            else:
                                st.session_state.result = '대칭'
                                st.write("대칭 축하드려요.")
                    else: 
                        st.session_state.start_time = time.time()
            else: 
                st.session_state.start_time = time.time()
                    
            # PIL 이미지로 변환
            st.session_state.pil_image = Image.fromarray(color_img)
            
            st.session_state.elapsed_time = time.time() - st.session_state.start_time 
            
            # 초에 따라 원을 그리는 끝 각도를 계산 (시계 반대 방향)
            st.session_state.end_angle = int(st.session_state.elapsed_time * (360 / capture_time))
            
            # 타이머 원 그리기
            if st.session_state.video_play == True:
                cv2.ellipse(color_img, (st.session_state.center_x, st.session_state.center_y), (radius, radius), 270, start_angle, st.session_state.end_angle, color, thickness)
            st.session_state.pil_image = Image.fromarray(color_img)
            
            # 이미지 표시
            image_placeholder.image(st.session_state.pil_image, channels="RGB", use_column_width=True)
    