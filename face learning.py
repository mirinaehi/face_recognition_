import face_recognition
import os
import pickle

# 학습된 데이터(사진)이 있는 디렉토리
KNOWN_FACES_DIR = 'known_faces'
# 저장할 파일 이름
ENCODINGS_FILE = 'encodings.pickle'

TOLERANCE = 0.38
FRAME_THICKNESS = 3
FONT_THICKNESS = 2

def name_to_color(name):
    color = [(ord(c.lower()) - 97) * 8 for c in name[:3]]
    return color

print('\033[91m' + '얼굴 학습중' + '\033[0m')
known_faces = []
known_names = []

for name in os.listdir(KNOWN_FACES_DIR):
    for filename in os.listdir(f'{KNOWN_FACES_DIR}/{name}'):
        image = face_recognition.load_image_file(f'{KNOWN_FACES_DIR}/{name}/{filename}')
        encoding = face_recognition.face_encodings(image)[0]
        known_faces.append(encoding)
        known_names.append(name)

# 학습된 데이터 저장
with open(ENCODINGS_FILE, 'wb') as f:
    pickle.dump((known_faces, known_names), f)

print('학습된 데이터가 저장되었습니다.')
