import sys
import os
import base64
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
                             QTextEdit, QFileDialog, QToolBar, QFontComboBox, QSpinBox,
                             QColorDialog, QLabel, QAction, QMessageBox, QDialog, QSplashScreen)
from PyQt5.QtGui import QFont, QColor, QPixmap, QIcon
from PyQt5.QtCore import Qt, QTimer
import qdarkstyle

def encrypt(data):
    encoded = data.encode('utf-8')
    encrypted = base64.b64encode(encoded).decode('utf-8')
    return encrypted

def decrypt(data):
    decoded = base64.b64decode(data.encode('utf-8'))
    return decoded

def encrypt_image(image_path):
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def decrypt_image(encoded_image):
    return base64.b64decode(encoded_image.encode('utf-8'))

class ImagePreviewDialog(QDialog):
    def __init__(self, image_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Image Preview")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        image_label = QLabel(self)
        pixmap = QPixmap()
        pixmap.loadFromData(decrypt_image(image_data))
        image_label.setPixmap(pixmap.scaled(580, 380, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        layout.addWidget(image_label)

        self.setLayout(layout)

class DoxPad(QMainWindow):
    def __init__(self, template=None):
        super().__init__()
        self.template = template
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Dox Pad - Dark Hacker Edition')
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowIcon(QIcon('icon.ico'))

        self.text_edit = QTextEdit(self)
        self.text_edit.setStyleSheet("background-color: #1c1c1c; color: #ffffff; font-family: Consolas; font-size: 14px; border: 1px solid #00ffcc;")
        self.setCentralWidget(self.text_edit)

        if self.template == "person":
            self.text_edit.setPlainText("Name:\nAddress:\nPhone Number:\nEmail:\nSocial Media Accounts:\nAdditional Information:\n")
        elif self.template == "company":
            self.text_edit.setPlainText("Company Name:\nIndustry:\nAddress:\nPhone Number:\nWebsite:\nAdditional Information:\n")
        elif self.template == "dox":
            self.text_edit.setPlainText("Full Name:\nAddress:\nPhone Number:\nDate of Birth:\nSocial Media Accounts:\nEmail:\nSSN:\nBank Info:\n")

        self.create_toolbar()
        self.create_menu()
        self.create_navigation_button()
        self.show()

    def create_toolbar(self):
        toolbar = QToolBar(self)
        self.addToolBar(toolbar)

        self.bold_button = QPushButton('B', self)
        self.bold_button.setCheckable(True)
        self.bold_button.clicked.connect(self.make_bold)
        toolbar.addWidget(self.bold_button)

        self.italic_button = QPushButton('I', self)
        self.italic_button.setCheckable(True)
        self.italic_button.clicked.connect(self.make_italic)
        toolbar.addWidget(self.italic_button)

        self.underline_button = QPushButton('U', self)
        self.underline_button.setCheckable(True)
        self.underline_button.clicked.connect(self.make_underline)
        toolbar.addWidget(self.underline_button)

        font_box = QFontComboBox(self)
        font_box.currentFontChanged.connect(self.change_font)
        toolbar.addWidget(font_box)

        font_size = QSpinBox(self)
        font_size.setValue(14)
        font_size.setRange(8, 72)
        font_size.valueChanged.connect(self.change_font_size)
        toolbar.addWidget(font_size)

        text_color_action = QAction('Text Color', self)
        text_color_action.triggered.connect(self.select_text_color)
        toolbar.addAction(text_color_action)

        insert_image_action = QAction('Insert Image', self)
        insert_image_action.triggered.connect(self.insert_image)
        toolbar.addAction(insert_image_action)

        preview_action = QAction('Preview', self)
        preview_action.triggered.connect(self.preview_images)
        toolbar.addAction(preview_action)

        copy_action = QAction('Copy', self)
        copy_action.setShortcut('Ctrl+C')
        copy_action.triggered.connect(self.text_edit.copy)
        toolbar.addAction(copy_action)

        paste_action = QAction('Paste', self)
        paste_action.setShortcut('Ctrl+V')
        paste_action.triggered.connect(self.text_edit.paste)
        toolbar.addAction(paste_action)

        toolbar.setStyleSheet("background-color: #0a0a0a; color: #00ffcc;")

    def create_menu(self):
        menubar = self.menuBar()
        menubar.setStyleSheet("background-color: #0a0a0a; color: white;")

        file_menu = menubar.addMenu('File')

        save_action = QAction('Save as .dth', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        open_action = QAction('Open .dth', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        quit_action = QAction('Quit', self)
        quit_action.setShortcut('Ctrl+Q')
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        go_back_action = QAction('Go Back', self)
        go_back_action.triggered.connect(self.back_to_menu)
        file_menu.addAction(go_back_action)

    def create_navigation_button(self):
        self.back_button = QPushButton("Back to Menu", self)
        self.back_button.setStyleSheet("background-color: #0a0a0a; color: #00ffcc; font-size: 16px; padding: 10px; border-radius: 5px;")
        self.back_button.clicked.connect(self.back_to_menu)
        self.text_edit.setCornerWidget(self.back_button)

    def back_to_menu(self):
        self.main_menu = MainMenu()
        self.main_menu.show()
        self.close()

    def make_bold(self):
        state = self.bold_button.isChecked()
        font = self.text_edit.font()
        font.setBold(state)
        self.text_edit.setFont(font)
        self.update_formatting_buttons()

    def make_italic(self):
        state = self.italic_button.isChecked()
        font = self.text_edit.font()
        font.setItalic(state)
        self.text_edit.setFont(font)
        self.update_formatting_buttons()

    def make_underline(self):
        state = self.underline_button.isChecked()
        font = self.text_edit.font()
        font.setUnderline(state)
        self.text_edit.setFont(font)
        self.update_formatting_buttons()

    def change_font(self, font):
        self.text_edit.setCurrentFont(font)

    def change_font_size(self, size):
        self.text_edit.setFontPointSize(size)

    def select_text_color(self):
        color = QColorDialog.getColor(Qt.white, self)
        if color.isValid():
            self.text_edit.setTextColor(color)

    def update_formatting_buttons(self):
        self.bold_button.setChecked(self.text_edit.font().bold())
        self.italic_button.setChecked(self.text_edit.font().italic())
        self.underline_button.setChecked(self.text_edit.font().underline())

        if self.bold_button.isChecked():
            self.bold_button.setStyleSheet("background-color: #00ffcc; color: #000000;")
        else:
            self.bold_button.setStyleSheet("background-color: #0a0a0a; color: #00ffcc;")

        if self.italic_button.isChecked():
            self.italic_button.setStyleSheet("background-color: #00ffcc; color: #000000;")
        else:
            self.italic_button.setStyleSheet("background-color: #0a0a0a; color: #00ffcc;")

        if self.underline_button.isChecked():
            self.underline_button.setStyleSheet("background-color: #00ffcc; color: #000000;")
        else:
            self.underline_button.setStyleSheet("background-color: #0a0a0a; color: #00ffcc;")

    def insert_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Insert Image", "", "Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)", options=options)
        if file_name:
            encrypted_image = encrypt_image(file_name)
            self.text_edit.insertHtml(f'<img src="data:image/png;base64,{encrypted_image}"/>')

    def preview_images(self):
        content = self.text_edit.toHtml()
        start_index = 0
        while True:
            start_index = content.find('src="data:image/png;base64,', start_index)
            if start_index == -1:
                break
            end_index = content.find('"', start_index + len('src="data:image/png;base64,'))
            image_data = content[start_index + len('src="data:image/png;base64,'):end_index]
            preview_dialog = ImagePreviewDialog(image_data, self)
            preview_dialog.exec_()
            start_index = end_index

    def save_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "DoxPad Files (*.dth);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'w') as file:
                    encrypted_text = encrypt(self.text_edit.toPlainText())
                    file.write(encrypted_text)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save the file: {e}")

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "DoxPad Files (*.dth);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'r') as file:
                    encrypted_text = file.read()
                    decrypted_text = decrypt(encrypted_text)
                    self.text_edit.setPlainText(decrypted_text)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open the file: {e}")

class SplashScreen(QSplashScreen):
    def __init__(self):
        pixmap = QPixmap('splash_image.png')
        super().__init__(pixmap)

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Dox Pad - Main Menu')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        self.setCentralWidget(QWidget(self))
        self.centralWidget().setLayout(layout)

        self.person_button = QPushButton("Create Person Dox", self)
        self.person_button.clicked.connect(lambda: self.open_dox_pad("person"))
        layout.addWidget(self.person_button)

        self.company_button = QPushButton("Create Company Dox", self)
        self.company_button.clicked.connect(lambda: self.open_dox_pad("company"))
        layout.addWidget(self.company_button)

        self.dox_button = QPushButton("Create Dox", self)
        self.dox_button.clicked.connect(lambda: self.open_dox_pad("dox"))
        layout.addWidget(self.dox_button)

        self.setStyleSheet("background-color: #1c1c1c; color: #00ffcc;")

    def open_dox_pad(self, template):
        self.dox_pad = DoxPad(template)
        self.dox_pad.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    
    splash = SplashScreen()
    splash.show()
    
    QTimer.singleShot(2000, splash.close)
    
    main_menu = MainMenu()
    main_menu.show()
    
    sys.exit(app.exec_())
