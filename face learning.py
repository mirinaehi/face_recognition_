import face_recognition  # 얼굴 인식 라이브러리
import os  # 운영체제 경로 및 파일 조작
import pickle  # 객체 직렬화

# 학습된 데이터(사진)이 있는 디렉토리
KNOWN_FACES_DIR = 'known_faces'
# 저장할 파일 이름
ENCODINGS_FILE = 'encodings.pickle'

MODEL = 'cnn'  # 얼굴 인식 모델

def load_known_faces(directory):
    """주어진 디렉토리에서 얼굴을 인식하고 인코딩된 데이터를 반환합니다."""
    known_faces, known_names = [], []

    # 디렉토리가 존재하는지 확인
    if not os.path.exists(directory):
        print(f"디렉토리 '{directory}'가 존재하지 않습니다.")
        return [], []

    # 디렉토리 내의 각 하위 디렉토리를 순회
    for name in os.listdir(directory):
        subdir = os.path.join(directory, name)
        # 하위 디렉토리가 디렉토리인지 확인
        if os.path.isdir(subdir):
            for filename in os.listdir(subdir):
                filepath = os.path.join(subdir, filename)
                try:
                    # 이미지를 로드하고 얼굴 인코딩
                    image = face_recognition.load_image_file(filepath)
                    encodings = face_recognition.face_encodings(image, model=MODEL)
                    if encodings:
                        known_faces.append(encodings[0])  # 첫 번째 얼굴 인코딩 추가
                        known_names.append(name)  # 해당 이름 추가
                    else:
                        print(f"얼굴 인식 실패: {filename}")
                except Exception as e:
                    # 파일 처리 중 오류 발생을 알림
                    print(f"파일 처리 중 오류 발생: {filename}, {e}")
    return known_faces, known_names

def save_encodings(file, encodings):
    """인코딩된 데이터를 파일에 저장합니다."""
    with open(file, 'wb') as f:
        pickle.dump(encodings, f)

print('\033[91m얼굴 학습 중...\033[0m')
known_faces, known_names = load_known_faces(KNOWN_FACES_DIR)
save_encodings(ENCODINGS_FILE, (known_faces, known_names))
print('학습된 데이터가 저장되었습니다.')
