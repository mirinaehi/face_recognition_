import face_recognition

# 이미지 파일 로드
image = face_recognition.load_image_file("known_faces/keria/keria04.jpg")

# 이미지에서 얼굴 인코딩 추출 (이미지에 여러 얼굴이 있을 경우, 첫 번째 얼굴만 추출)
face_encodings = face_recognition.face_encodings(image)

if face_encodings:
    known_face_encoding = face_encodings[0]  # 첫 번째 얼굴 인코딩 사용
else:
    print("얼굴을 찾을 수 없습니다.")
