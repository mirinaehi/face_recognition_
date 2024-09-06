import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class ImageWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 창의 제목을 설정
        self.setWindowTitle('Drag and Drop Image Viewer')

        # 창의 크기와 위치 설정 (x, y, width, height)
        self.setGeometry(100, 100, 800, 600)

        # QLabel 위젯 생성 및 초기 텍스트 설정
        self.label = QLabel('Drag an image file here', self)

        # 텍스트를 중앙 정렬
        self.label.setAlignment(Qt.AlignCenter)

        # QLabel을 메인 윈도우의 중앙 위젯으로 설정
        self.setCentralWidget(self.label)

        # 드래그 앤 드롭을 활성화
        self.setAcceptDrops(True)

    # 드래그 이벤트 처리: 드래그된 데이터가 URL일 경우 허용
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():  # 드래그된 데이터에 파일이 있는지 확인
            event.acceptProposedAction()  # 드래그 동작 허용

    # 드롭 이벤트 처리: 드롭된 파일을 처리
    def dropEvent(self, event):
        # 드롭된 모든 파일 URL에 대해 반복 처리
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()  # 로컬 파일 경로 가져오기
            # 이미지 파일 확장자 체크 (.png, .jpg, .jpeg, .bmp, .gif 만 허용)
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                self.load_image(file_path)  # 이미지 로드 함수 호출

    # 이미지를 로드하고 QLabel에 표시하는 함수
    def load_image(self, file_path):
        pixmap = QPixmap(file_path)  # QPixmap을 사용해 이미지 로드
        self.label.setPixmap(pixmap)  # QLabel에 이미지를 설정
        self.label.setScaledContents(True)  # QLabel 크기에 맞게 이미지 스케일 조정


# 메인 프로그램 시작
if __name__ == '__main__':
    # QApplication 객체 생성 (애플리케이션을 실행하는 핵심 클래스)
    app = QApplication(sys.argv)

    # ImageWindow 객체 생성
    window = ImageWindow()

    # 메인 윈도우 표시
    window.show()

    # 애플리케이션 실행 및 종료 처리
    sys.exit(app.exec_())
