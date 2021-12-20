import face_recognition
import os
import cv2

##### 아두이노
import pyfirmata
DELAY = 1
# Uno 버전
# board = pyfirmata.Arduino('COM4')
board = pyfirmata.ArduinoMega('COM4')

# PWM 신호 (디지털 9번 pin)
servo = board.get_pin('d:9:s')
# digital 신호 (디지털 4번 pin)
led = board.digital[4]

# 문을 닫고 불을 끔
servo.write(0)
led.write(0)
#####

# 학습된 데이터(사진)이 있는 디렉토리
KNOWN_FACES_DIR = 'known_faces'

# 얼굴일치 민감도(0~1 사이이며, 숫자가 작을수록 엄밀하게 판단하여 정확도는 높다. 하지만 너무 깐깐하게 설정하면 얼굴인식이 힘들수도 있음)
TOLERANCE = 0.5

# 얼굴을 잡아주는 겉부분 네모난 프레임과 이름 폰트의 굵기
FRAME_THICKNESS = 3
FONT_THICKNESS = 2

# 딥러닝 모델을 cnn으로
MODEL = 'cnn'  # default: 'hog', other one can be 'cnn' - CUDA accelerated (if available) deep-learning pretrained model

# 이름에 따른 색깔을 (R, G, B) 형태로 Returns
def name_to_color(name):
    # 첫 3글자를 소문자형태로 가져온다 (1st 글자 R, 2nd 글자 G, 3rd 글자 B)
    # 소문자의 아스키코드 범위는 97('a') to 122('z')
    color = [(ord(c.lower())-97)*8 for c in name[:3]]
    return color


# 여러개의 카메라 중 가장 처음의 카메라를 가져옴
video = cv2.VideoCapture(0)

print('얼굴 학습중')
known_faces = []
known_names = []

# We oranize known faces as subfolders of KNOWN_FACES_DIR
# KNOWN_FACES_DIR의 하위폴더로 인식하고자 하는 얼굴들의 이름을 폴더로(name)
# ex) 'known_faces'폴더 안에 'JWP'(name) 폴더 안에 JWP의 사진파일들(filename)이 들어있음
for name in os.listdir(KNOWN_FACES_DIR):

    # 한 사람에(JWP) 대한 사진파일들(filename)
    for filename in os.listdir(f'{KNOWN_FACES_DIR}/{name}'):

        # 파일 image를 불러옴
        image = face_recognition.load_image_file(f'{KNOWN_FACES_DIR}/{name}/{filename}')

        # 식별된 id(encoding)를 가져옴 , 하나의 name당 하나의 id를 가짐
        # encoding은 128-dimension
        encoding = face_recognition.face_encodings(image)[0]

        # 이름과 그에 대한 id를 목록에 추가함
        known_faces.append(encoding)
        known_names.append(name)


print('얼굴인식 시작')

while True:
    ret, image = video.read()

    # CNN을 이용하여 얼굴의 위치를 계산
    locations = face_recognition.face_locations(image, model=MODEL)
    # hog 방식
    # locations = face_recognition.face_locations(image)

    # 특정 위치에 대한 id를 찾아내기 때문에 속도가 더 빠름
    # 사진을 불러오는 코드에서는 locations이 없어서 사진 하나당 encoding의 속도가 느리나,
    # 사진은 몇 장 되지 않고, 여기에는 무한루프로 계속 실행함
    encodings = face_recognition.face_encodings(image, locations)

    for face_encoding, face_location in zip(encodings, locations):
        
        # 128차원의 nparray에서 norm값이 0.5(TOLERANCE) 이하인 것을 발견하면 True
        # 전달된 known_faces의 순서대로 True/False 값의 배열을 반환
        results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)

        # 식별된 얼굴이 하나라도 발견될 경우 해당 id의 얼굴과 얼굴외곽 프레임을 출력한다
        match = None
        if True in results:  # If at least one is true, get a name of first of found labels
            match = known_names[results.index(True)]
            print(f' - {match} from {results}')

            # 문을 열고, 불을 킴
            servo.write(90)
            led.write(1)

            # 외곽 프레임의 위치 측정
            top_left = (face_location[3], face_location[0])
            bottom_right = (face_location[1], face_location[2])

            # 이름에 따른 색깔 결정
            color = name_to_color(match)

            # 얼굴 외각 프레임 및 이름 출력
            cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)
            top_left = (face_location[3], face_location[2])
            bottom_right = (face_location[1], face_location[2] + 22)
            cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)
            cv2.putText(image, match, (face_location[3] + 10, face_location[2] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)

    # 이미지를 보여준다
    cv2.imshow("", image)

    # q 버튼을 누르면 프로그램 종료
    if cv2.waitKey(1) & 0xFF == ord("q"):
        # TODO : q 버튼을 누르면 불은 잘 꺼지나 문(모터)의 각도가 살짝만 바뀜 (똑같은 write(0)인데 이유를 모르겠음)
        servo.write(0)
        led.write(0)
        print("프로그램 종료")
        break


# 모든 자원을 해제
video.release()
cv2.destroyAllWindows()

# servo.write(0)
# exit()
