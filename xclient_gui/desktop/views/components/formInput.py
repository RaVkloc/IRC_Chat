from PyQt5.QtWidgets import QLabel, QLineEdit


class Label(QLabel):
    def __init__(self, *args):
        super().__init__(*args)
        self.setStyleSheet("font: 12pt;")


class LineEdit(QLineEdit):
    def __init__(self, placeholder):
        super().__init__()
        self.setPlaceholderText(placeholder)


class FormInput:
    def __init__(self, label, placeholder):
        self.label = label
        self.placeholder = placeholder

    def get_label(self):
        return Label(self.label)

    def get_line_edit(self):
        return LineEdit(self.placeholder)

    def get_input(self):
        return self.get_label(), self.get_line_edit()
