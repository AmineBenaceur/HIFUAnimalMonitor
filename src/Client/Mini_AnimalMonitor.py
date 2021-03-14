import sys
from PySide2.QtWidgets import QApplication, QWidget, QSpinBox

class MiniAnimalMonitor(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Animal Monitor")
        self.setGeometry(300, 300, 300, 300)

        # hb and temp reading + set temp
        self.spinBox = QSpinBox()
        self.spinBox.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    monitor = MiniAnimalMonitor()
    monitor.show()

    app.exec_()
    sys.exit(0)