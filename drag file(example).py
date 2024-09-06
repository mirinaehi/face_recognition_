import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QAction, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class ImageWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Drag and Drop Image Viewer')
        self.setGeometry(100, 100, 800, 600)

        # QLabel 생성
        self.label = QLabel('Drag an image file here', self)
        self.label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.label)

        # 드래그 앤 드롭 활성화
        self.setAcceptDrops(True)

        # 메뉴바 설정
        self.create_menu()

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
        # QPixmap으로 이미지 로드
        pixmap = QPixmap(file_path)

        # QLabel의 크기를 얻고 비율을 유지하면서 스케일 조정
        label_size = self.label.size()
        scaled_pixmap = pixmap.scaled(label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # QLabel에 이미지 설정
        self.label.setPixmap(scaled_pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageWindow()
    window.show()
    sys.exit(app.exec_())
