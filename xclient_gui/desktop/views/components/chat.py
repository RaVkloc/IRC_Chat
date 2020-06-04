from PyQt5.QtWidgets import QListWidget, QWidget, QVBoxLayout, QLineEdit, QHBoxLayout, QPushButton, \
    QListWidgetItem


class MessagesList(QListWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('background-color:gray')
        self.setWordWrap(True)
        self.show()


class NewMessageInput(QWidget):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.message_input = None

        self.create_gui()

    def create_message_input(self):
        return QLineEdit()

    def send_new_message(self):
        text = self.message_input.text()
        if len(text) > 0:
            self.message_input.setText("")

            # TODO change the string to the modouledef param
            body = {
                "Message": text
            }
            self.client.send_message(body=body)

    def handle_button_clicked(self):
        self.send_new_message()

    def create_push_button(self):
        button = QPushButton(">")
        button.clicked.connect(self.handle_button_clicked)
        return button

    def create_gui(self):
        self.message_input = self.create_message_input()
        push_button = self.create_push_button()

        box_layout = QHBoxLayout()
        box_layout.addWidget(self.message_input)
        box_layout.addWidget(push_button)

        self.setLayout(box_layout)


class Chat(QWidget):
    def __init__(self, client):
        super().__init__()
        layout = QVBoxLayout()

        messages = MessagesList()
        messages.addItem("Witaj w pokoju Test1.\nLista aktywnych użytkowników: Jan Kowalski, Pan Zbysiu, Zenek")
        messages.addItem("_____________________________________________________")
        messages.addItem(QListWidgetItem("dsfsd"))

        new_message_input = NewMessageInput(client)

        layout.addWidget(messages)
        layout.addWidget(new_message_input)

        self.setLayout(layout)
