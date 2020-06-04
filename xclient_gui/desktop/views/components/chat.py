from PyQt5.QtWidgets import QListWidget, QWidget, QVBoxLayout, QLineEdit, QHBoxLayout, QPushButton, \
    QListWidgetItem


class MessagesList(QListWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('background-color:gray')
        self.setWordWrap(True)
        self.show()


class NewMessageInput(QHBoxLayout):
    def __init__(self):
        super().__init__()

        message_input = QLineEdit()
        button = QPushButton(">")
        self.addWidget(message_input)
        self.addWidget(button)


class Chat(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        messages = MessagesList()

        messages.addItem("Witaj w pokoju Test1.\nLista aktywnych użytkowników: Jan Kowalski, Pan Zbysiu, Zenek")
        messages.addItem("_____________________________________________________")
        messages.addItem(QListWidgetItem("dsfsd"))
        new_message_input = NewMessageInput()

        layout.addWidget(messages)
        layout.addLayout(new_message_input)
        self.setLayout(layout)
