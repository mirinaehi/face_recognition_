import sys
import os
import cv2
import face_recognition
import pickle
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QAction, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import ImageFont, ImageDraw, Image
import hashlib


class ImageWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Drag and Drop Face Recognition Viewer')
        self.setGeometry(100, 100, 800, 600)

        # QLabel 생성
        self.label = QLabel('Drag an image file here', self)
        self.label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.label)

        # 드래그 앤 드롭 활성화
        self.setAcceptDrops(True)

        # 이미지의 QPixmap 저장용 변수
        self.pixmap = None
        self.current_image_path = None  # 현재 불러온 이미지 경로 저장

        # QLabel의 최소 크기 설정 (너무 작아지지 않도록 설정)
        self.label.setMinimumSize(100, 100)

        # 메뉴바 설정
        self.create_menu()

        # 얼굴 인식 관련 설정
        self.TOLERANCE = 0.38
        self.FRAME_THICKNESS = 3
        self.FONT_THICKNESS = 2
        self.MODEL = 'hog'
        self.fontpath = "fonts/gulim.ttc"  # 사용할 한글 폰트 경로

        # 인코딩 파일 경로
        self.ENCODINGS_FILE = 'encodings.pickle'

        # 학습된 얼굴 데이터 불러오기
        with open(self.ENCODINGS_FILE, 'rb') as f:
            self.known_faces, self.known_names = pickle.load(f)

    def create_menu(self):
        # 메뉴바 생성
        menu_bar = self.menuBar()

        # 파일 메뉴 생성
        file_menu = menu_bar.addMenu('파일')

        # "이미지 열기" 액션 추가
        open_action = QAction('이미지 열기', self)
        open_action.triggered.connect(self.open_image)
        file_menu.addAction(open_action)

        # "종료" 액션 추가
        exit_action = QAction('종료', self)
        exit_action.triggered.connect(self.close)  # 프로그램 종료
        file_menu.addAction(exit_action)

    def open_image(self):
        # 파일 열기 대화상자를 열고 이미지 파일 선택
        file_path, _ = QFileDialog.getOpenFileName(self, "이미지 파일 열기", "", "이미지 파일 (*.png *.jpg *.jpeg *.bmp *.gif)")

        if file_path:
            self.load_image(file_path)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                self.load_image(file_path)

    def load_image(self, file_path):
        self.current_image_path = file_path  # 현재 파일 경로 저장
        self.pixmap = QPixmap(file_path)  # QPixmap으로 이미지 로드
        self.update_image()  # 이미지를 업데이트
        self.perform_face_recognition()  # 얼굴 인식 실행

    def resizeEvent(self, event):
        # 창 크기가 변경될 때마다 이미지를 업데이트
        self.update_image()

    def update_image(self):
        if self.pixmap:
            # QLabel의 크기를 얻고 비율을 유지하면서 스케일 조정
            label_size = self.label.size()
            scaled_pixmap = self.pixmap.scaled(label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # QLabel에 이미지 설정
            self.label.setPixmap(scaled_pixmap)

    def name_to_color(self, name):
        # 이름을 해시하여 색상으로 변환
        hash_value = hashlib.md5(name.encode()).hexdigest()
        r = int(hash_value[0:2], 16)
        g = int(hash_value[2:4], 16)
        b = int(hash_value[4:6], 16)
        return (r, g, b)

    def perform_face_recognition(self):
        if self.current_image_path:
            # 이미지 로드
            test_image = face_recognition.load_image_file(self.current_image_path)

            # 이미지에서 얼굴 위치와 인코딩 추출
            locations = face_recognition.face_locations(test_image, model=self.MODEL)
            encodings = face_recognition.face_encodings(test_image, locations)

            # 이미지를 BGR로 변환하여 OpenCV에서 사용할 수 있게 함
            test_image = cv2.cvtColor(test_image, cv2.COLOR_RGB2BGR)

            # Pillow로 이미지를 처리하기 위해 변환
            test_image_pil = Image.fromarray(test_image)
            draw = ImageDraw.Draw(test_image_pil)
            font = ImageFont.truetype(self.fontpath, 24)  # 글꼴과 크기 설정

            # 매치된 얼굴의 결과물
            match_list = []

            for face_encoding, face_location in zip(encodings, locations):
                results = face_recognition.compare_faces(self.known_faces, face_encoding, self.TOLERANCE)
                match = None

                if True in results:
                    match = self.known_names[results.index(True)]
                    match_list.append(match)
                    print(f' - {match} from {results}')

                    # 얼굴 외곽 프레임 그리기 (Pillow 사용)
                    top_left = (face_location[3], face_location[0])
                    bottom_right = (face_location[1], face_location[2])
                    color = self.name_to_color(match)

                    # 얼굴 외곽 프레임 그리기
                    draw.rectangle([top_left, bottom_right], outline=color, width=self.FRAME_THICKNESS)

                    # 텍스트 추가 (Pillow 사용)
                    text_position = (face_location[3] + 10, face_location[2] + 5)
                    draw.text(text_position, match, font=font, fill=color)

            # OpenCV에서 사용하기 위해 다시 변환
            test_image = np.array(test_image_pil)

            print('\033[94m' + str(match_list) + '\033[0m')
            # TODO : 얼굴인식 화면을 닫지 않아도 파일을 끌 수 있게 하기
            # 얼굴 인식 결과를 화면에 표시
            cv2.imshow('Face Recognition', test_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageWindow()
    window.show()
    sys.exit(app.exec_())
