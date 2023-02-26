# import dependecies
import math
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QLabel



# create class
def answer(answ):
    if answ == int(answ):
        return str(int(answ))
    return str(answ)


class Calculator(QWidget):
    def __init__(self):
        super(Calculator, self).__init__()
        self.vbox = QVBoxLayout(self)
        self.hbox_input = QHBoxLayout()
        self.hbox_ground = QHBoxLayout()
        self.hbox_first = QHBoxLayout()
        self.hbox_second = QHBoxLayout()
        self.hbox_third = QHBoxLayout()
        self.hbox_jstnull = QHBoxLayout()
        self.hbox_fourth = QHBoxLayout()
        self.hbox_result = QHBoxLayout()


        self.op = None
        self.num_1 = 0
        self.num_2 = 0
        self.already_used = 0

        self.vbox.addLayout(self.hbox_input)
        self.vbox.addLayout(self.hbox_ground)
        self.vbox.addLayout(self.hbox_first)
        self.vbox.addLayout(self.hbox_second)
        self.vbox.addLayout(self.hbox_third)
        self.vbox.addLayout(self.hbox_jstnull)
        self.vbox.addLayout(self.hbox_fourth)
        self.vbox.addLayout(self.hbox_result)

#        self.input = QLabel(self)
        self.input = QLineEdit(self)
        self.input.setText('0')
        self.hbox_input.addWidget(self.input)
        self.input.setReadOnly(True)


        self.b_clear = QPushButton("AC", self)
        self.hbox_ground.addWidget(self.b_clear)

        self.b_del = QPushButton("DEL", self)
        self.hbox_ground.addWidget(self.b_del)

        self.b_7 = QPushButton("7", self)
        self.hbox_first.addWidget(self.b_7)

        self.b_8 = QPushButton("8", self)
        self.hbox_first.addWidget(self.b_8)

        self.b_9 = QPushButton("9", self)
        self.hbox_first.addWidget(self.b_9)

        self.b_4 = QPushButton("4", self)
        self.hbox_second.addWidget(self.b_4)

        self.b_5 = QPushButton("5", self)
        self.hbox_second.addWidget(self.b_5)

        self.b_6 = QPushButton("6", self)
        self.hbox_second.addWidget(self.b_6)

        self.b_1 = QPushButton("1", self)
        self.hbox_third.addWidget(self.b_1)

        self.b_2 = QPushButton("2", self)
        self.hbox_third.addWidget(self.b_2)

        self.b_3 = QPushButton("3", self)
        self.hbox_third.addWidget(self.b_3)

        self.b_null = QPushButton('SEND')
        self.hbox_jstnull.addWidget(self.b_null)

        self.b_null2 = QPushButton("0", self)
        self.hbox_jstnull.addWidget(self.b_null2)

        self.b_null3 = QPushButton('NUDES')
        self.hbox_jstnull.addWidget(self.b_null3)

        self.b_plus = QPushButton("+", self)
        self.hbox_fourth.addWidget(self.b_plus)

        self.b_minus = QPushButton("-", self)
        self.hbox_fourth.addWidget(self.b_minus)

        self.b_mult = QPushButton("x", self)
        self.hbox_fourth.addWidget(self.b_mult)

        self.b_div = QPushButton("/", self)
        self.hbox_fourth.addWidget(self.b_div)

        self.b_decimal = QPushButton(".", self)
        self.hbox_result.addWidget(self.b_decimal)

        self.b_result = QPushButton("=", self)
        self.hbox_result.addWidget(self.b_result)

        self.b_plus.clicked.connect(lambda: self._operation("+"))
        self.b_minus.clicked.connect(lambda: self._operation("-"))
        self.b_mult.clicked.connect(lambda: self._operation("x"))
        self.b_div.clicked.connect(lambda: self._operation("/"))
        self.b_decimal.clicked.connect(lambda: self._button("."))
        self.b_del.clicked.connect(lambda: self._delete())
        self.b_clear.clicked.connect(lambda: self._ac())
        self.b_result.clicked.connect(self._result)

        self.b_null.clicked.connect(lambda: self._button("231"))
        self.b_null3.clicked.connect(lambda: self._button("8008"))
        self.b_9.clicked.connect(lambda: self._button("9"))
        self.b_8.clicked.connect(lambda: self._button("8"))
        self.b_7.clicked.connect(lambda: self._button("7"))
        self.b_6.clicked.connect(lambda: self._button("6"))
        self.b_5.clicked.connect(lambda: self._button("5"))
        self.b_4.clicked.connect(lambda: self._button("4"))
        self.b_3.clicked.connect(lambda: self._button("3"))
        self.b_2.clicked.connect(lambda: self._button("2"))
        self.b_1.clicked.connect(lambda: self._button("1"))
        self.b_null2.clicked.connect(lambda: self._button("0"))


    def _delete(self):
        line = self.input.text()
        if len(line) == 1:
            self.input.setText('0')
        else:
            self.input.setText(line[:-1])
        self.already_used = 0

    def _ac(self):
        self.input.setText('0')
        self.op = None
        self.num_1 = None
        self.num_2 = None
        self.already_used = 0

    def _button(self, param):
        line = self.input.text()
        if line.count('.') > 0 and param == '.':
            self.input.setText(line.lstrip('0'))
        elif line.count('0') > 0:
            self.input.setText(((line).lstrip('0') + param))
        else:
            self.input.setText((line + param).lstrip('0'))
        self.already_used = 0

    def _operation(self, op):
        if self.op == None:
            self.num_1 = float(self.input.text())
        self.op = op
        self.input.setText('0')
        self.already_used = 0


    def _result(self):
        if self.already_used !=1:
            self.num_2 = float(self.input.text())
        if self.op == "+":
            self.input.setText(answer(self.num_1 + self.num_2))
        elif self.op == "-":
            self.input.setText(answer(self.num_1 - self.num_2))
        elif self.op == "x":
            self.input.setText(answer(self.num_1 * self.num_2))
        elif self.op == "/":
            if self.num_2 !=0:
                self.input.setText(answer(self.num_1 / self.num_2))
#            else:
#                self.input.setText("⣿⣿⣿⠟⢹⣶⣶⣝⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿:⣿⣿⡟⢰⡌⠿⢿⣿⡾⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿:⣿⣿⣿⢸⣿⣤⣒⣶⣾⣳⡻⣿⣿⣿⣿⡿⢛⣯⣭⣭⣭⣽⣻⣿⣿⣿:⣿⣿⣿⢸⣿⣿⣿⣿⢿⡇⣶⡽⣿⠟⣡⣶⣾⣯⣭⣽⣟⡻⣿⣷⡽⣿:⣿⣿⣿⠸⣿⣿⣿⣿⢇⠃⣟⣷⠃⢸⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽:⣿⣿⣿⣇⢻⣿⣿⣯⣕⠧⢿⢿⣇⢯⣝⣒⣛⣯⣭⣛⣛⣣⣿⣿⣿⡇:⣿⣿⣿⣿⣌⢿⣿⣿⣿⣿⡘⣞⣿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇:⣿⣿⣿⣿⣿⣦⠻⠿⣿⣿⣷⠈⢞⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇:⣿⣿⣿⣿⣿⣿⣗⠄⢿⣿⣿⡆⡈⣽⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻:⣿⣿⣿⣿⡿⣻⣽⣿⣆⠹⣿⡇⠁⣿⡼⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣾:⣿⠿⣛⣽⣾⣿⣿⠿⠋⠄⢻⣷⣾⣿⣧⠟⣡⣾⣿⣿⣿⣿⣿⣿⡇⣿:⢼⡟⢿⣿⡿⠋⠁⣀⡀⠄⠘⠊⣨⣽⠁⠰⣿⣿⣿⣿⣿⣿⣿⡍⠗⣿:⡼⣿⠄⠄⠄⠄⣼⣿⡗⢠⣶⣿⣿⡇⠄⠄⣿⣿⣿⣿⣿⣿⣿⣇⢠⣿:⣷⣝⠄⠄⢀⠄⢻⡟⠄⣿⣿⣿⣿⠃⠄⠄⢹⣿⣿⣿⣿⣿⣿⣿⢹⣿:⣿⣿⣿⣿⣿⣧⣄⣁⡀⠙⢿⡿⠋⠄⣸⡆⠄⠻⣿⡿⠟⢛⣩⣝⣚⣿:⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣤⣤⣤⣾⣿⣿⣄⠄⠄⠄⣴⣿⣿⣿⣇⣿:⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⡀⠛⠿⣿⣫⣾⣿")
        self.already_used = 1
        self.num_1 = float(self.input.text())


app = QApplication(sys.argv)

win = Calculator()
win.show()

sys.exit(app.exec_())
