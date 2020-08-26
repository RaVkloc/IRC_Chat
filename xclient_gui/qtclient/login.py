from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QDialog, QWidget, QGridLayout, QComboBox, QLineEdit, QLabel, QDialogButtonBox, QVBoxLayout


class LoginWindow(QDialog):
    login_user = QtCore.pyqtSignal(str, str)

    def __init__(self, parent: QWidget):
        super().__init__(parent=parent)
        self.username_combo = None
        self.password_line = None

        self.__createGui()
        self.setMinimumSize(200, 150)
        self.setWindowTitle("Login User")
        self.setModal(True)

    def __createGui(self):
        main_layout = QVBoxLayout(self)
        grid_layout = QGridLayout(self)
        grid_layout.setSpacing(10)

        grid_layout.addWidget(QLabel("Username:"), 0, 0, Qt.AlignRight)
        self.username_combo = QLineEdit(self)
        self.username_combo.setMinimumWidth(150)
        grid_layout.addWidget(self.username_combo, 0, 1)

        grid_layout.addWidget(QLabel("Password:"), 1, 0, Qt.AlignRight)
        self.password_line = QLineEdit(self)
        self.password_line.setEchoMode(QLineEdit.Password)
        self.password_line.setMinimumWidth(150)
        grid_layout.addWidget(self.password_line, 1, 1)

        main_layout.addLayout(grid_layout)

        buttons = QDialogButtonBox()
        buttons.addButton(QDialogButtonBox.Ok)
        buttons.button(QDialogButtonBox.Ok).setText("Login")
        buttons.addButton(QDialogButtonBox.Cancel)
        main_layout.addWidget(buttons)

        buttons.button(QDialogButtonBox.Cancel).clicked.connect(self.close)
        buttons.button(QDialogButtonBox.Ok).clicked.connect(self.ok_clicked)

        self.setLayout(main_layout)

    def ok_clicked(self):
        self.login_user.emit(self.username_combo.text(), self.password_line.text())
        self.close()
