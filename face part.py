import face_recognition
import cv2
import pickle
import numpy as np
from PIL import ImageFont, ImageDraw, Image

# 인식하고자 하는 사진 파일
IMAGE_TO_TEST = 'test_faces/test4.jpg'
# 저장된 파일 이름
ENCODINGS_FILE = 'encodings.pickle'

TOLERANCE = 0.38
FRAME_THICKNESS = 3
FONT_THICKNESS = 2
MODEL = 'hog'

def name_to_color(name):
    # 이름을 색상으로 변환 (RGB 튜플로 반환)
    color = [(ord(c.lower()) - 97) * 8 for c in name[:3]]
    return tuple(color)

# 저장된 학습 데이터 불러오기
with open(ENCODINGS_FILE, 'rb') as f:
    known_faces, known_names = pickle.load(f)

print('\033[91m' + '얼굴 인식 시작' + '\033[0m')

# 테스트 이미지 로드
test_image = face_recognition.load_image_file(IMAGE_TO_TEST)

# 테스트 이미지에서 얼굴 위치와 인코딩 추출
locations = face_recognition.face_locations(test_image, model=MODEL)
encodings = face_recognition.face_encodings(test_image, locations)

# 테스트 이미지를 BGR로 변환하여 OpenCV에서 사용할 수 있게 함
test_image = cv2.cvtColor(test_image, cv2.COLOR_RGB2BGR)

# Pillow로 이미지를 처리하기 위해 변환
test_image_pil = Image.fromarray(test_image)
draw = ImageDraw.Draw(test_image_pil)
fontpath = "fonts/gulim.ttc"  # 사용할 한글 폰트 경로
font = ImageFont.truetype(fontpath, 24)  # 글꼴과 크기 설정

for face_encoding, face_location in zip(encodings, locations):
    results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)
    match = None
    if True in results:
        match = known_names[results.index(True)]
        print(f' - {match} from {results}')

        # 얼굴 외곽 프레임 그리기 (Pillow 사용)
        top_left = (face_location[3], face_location[0])
        bottom_right = (face_location[1], face_location[2])
        color = name_to_color(match)
        draw.rectangle([top_left, bottom_right], outline=color, width=FRAME_THICKNESS)

        # 텍스트 추가 (Pillow 사용)
        text_position = (face_location[3] + 10, face_location[2] + 5)
        draw.text(text_position, match, font=font, fill=color)

# OpenCV에서 사용하기 위해 다시 변환
test_image = np.array(test_image_pil)

# 이미지 표시
cv2.imshow('Face Recognition', test_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
