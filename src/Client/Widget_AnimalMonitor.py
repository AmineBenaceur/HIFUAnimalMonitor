from PySide2.QtWidgets import *
'''
2020-12-03 AB: A client side UI for the animal monitor data
            recieved via client/Server communication (Coming later)

'''



class Widget_MessageBoard(QWidget):

    def __init__(self):
        super(Widget_MessageBoard, self).__init__()


        def Widget_Terminal(self):
            '''
            2020-12-03 AB:
            Update users on status from the RPi
            '''
            self.terminal = QTextEdit()
            self.terminal.setReadOnly(True)

            return self.terminal

        def update(self):
            pass




app = QApplication([])
window = QWidget()
layout = QHBoxLayout() # HORIZONTAL BOX LAYOUT

label = QLabel('Monitor Controls')
button_1 = QPushButton("Connect")
button_2 = QPushButton("Disconnect")
button_3 = QPushButton("Ping")

layout.addWidget(Widget_MessageBoard())
layout.addWidget(label)
layout.addWidget(button_1)
layout.addWidget(button_2)
layout.addWidget(button_3)
window.setLayout(layout)
window.show()
app.exec_()
