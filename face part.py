import face_recognition
import cv2
import os

# 학습된 데이터(사진)이 있는 디렉토리
KNOWN_FACES_DIR = 'known_faces'
# 인식하고자 하는 사진 파일
IMAGE_TO_TEST = 'test_faces/test1.jpg'

TOLERANCE = 0.4
FRAME_THICKNESS = 3
FONT_THICKNESS = 2
#MODEL = 'cnn'
MODEL = 'hog'

def name_to_color(name):
    color = [(ord(c.lower()) - 97) * 8 for c in name[:3]]
    return color

print('얼굴 학습중')
known_faces = []
known_names = []

for name in os.listdir(KNOWN_FACES_DIR):
    for filename in os.listdir(f'{KNOWN_FACES_DIR}/{name}'):
        image = face_recognition.load_image_file(f'{KNOWN_FACES_DIR}/{name}/{filename}')
        # pip install numpy==1.26.3 opencv-python==4.9.0.80
        encoding = face_recognition.face_encodings(image)[0]
        known_faces.append(encoding)
        known_names.append(name)

print('얼굴인식 시작')

# 테스트 이미지 로드
test_image = face_recognition.load_image_file(IMAGE_TO_TEST)

# 테스트 이미지에서 얼굴 위치와 인코딩 추출
locations = face_recognition.face_locations(test_image, model=MODEL)
encodings = face_recognition.face_encodings(test_image, locations)

# 테스트 이미지를 BGR로 변환하여 OpenCV에서 사용할 수 있게 함
test_image = cv2.cvtColor(test_image, cv2.COLOR_RGB2BGR)

for face_encoding, face_location in zip(encodings, locations):
    results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)
    match = None
    if True in results:
        match = known_names[results.index(True)]
        print(f' - {match} from {results}')

        top_left = (face_location[3], face_location[0])
        bottom_right = (face_location[1], face_location[2])
        color = name_to_color(match)
        cv2.rectangle(test_image, top_left, bottom_right, color, FRAME_THICKNESS)
        top_left = (face_location[3], face_location[2])
        bottom_right = (face_location[1], face_location[2] + 22)
        cv2.rectangle(test_image, top_left, bottom_right, color, cv2.FILLED)
        cv2.putText(test_image, match, (face_location[3] + 10, face_location[2] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)

cv2.imshow('Face Recognition', test_image)
cv2.waitKey(0)
cv2.destroyAllWindows()