import sys

if sys.version_info > (3, 2):
    from PySide2 import QtGui, QtCore, QApplication
    import PySide2.QtWidgets as QBase
    def unichr(s):
        return chr(s)
else:
    from PySide import QtGui, QtCore
    import PySide.QtGui as QBase


#SIGNALS
    s_new_temp      = QtCore.Signal()

# Limits
'''
TODO:  set limits, and notify (print or launch popup) when limits reached or exceeded
'''
HB_HIGH = 80
HB_LOW = 35



class MiniAnimalMonitor(QBase.QWidget):
    def __init__(self, parent=None):
        '''
        Init main window, add inner widgets
        '''

        super(MiniAnimalMonitor,self).__init__(parent)

        self.setWindowTitle("Animal Monitor")
        self.setGeometry(300, 300, 300, 300)

        layout = QBase.QGridLayout()

        # hb and temp reading + set temp
        layout.addWidget(self.widget_title("Readings:"), 1,0,1,1)
        #uncomment below when widget_readings() done
        #layout.addWidget(self.widget_readings(), 2,0,1,1)
        layout.addWidget(self.widget_title("Set Temp:"), 3,0,1,1)
        layout.addWidget(self.widget_spinbox(), 4, 0, 1, 2)
        layout.addWidget(self.widget_title("Controls:"), 5,0,1,1)
        #Uncomment Below when buttons done
        # layout.addWidget(self.widget_buttons(), 6, 0, 2, 1)
        layout.setColumnStretch(0, 10)
        self.setLayout(layout)

    def widget_title(self, txt):
        # Qw = QBase.QWidget()
        # box = QBase.QHBoxLayout()
        title = QBase.QLabel(txt, parent=self)
        title_font = QtGui.QFont("Times", 15, QtGui.QFont.Bold)
        title.setFont(title_font)
        title.setStyleSheet('color: grey')
        #title.setStyleSheet("color: grey; border-bottom-width: 1px; border-bottom-style: solid; border-radius: 0px;")
        return title

    def widget_readings(self):
        '''
        display temp and hb
        '''
        pass
    def widget_spinbox(self):
        '''
        2021-03-14 AB: spinbox widget
        '''
        #  create Widget to return and layout
        Qw = QBase.QWidget()
        box  = QBase.QVBoxLayout()

        # styling
        values_font = QtGui.QFont("Times", 20, QtGui.QFont.Bold)
        labels_font = QtGui.QFont("Times", 12, QtGui.QFont.Bold)

        # create label, add styling
        #label_temp    = QBase.QLabel("Set temperature: ", parent=self)
        #label_temp.setFont(labels_font)
        #label_temp.setStyleSheet('color: grey')

        #create spinbox
        self.spinbox = QBase.QDoubleSpinBox()
        self.spinbox.setSingleStep(0.1)
        self.spinbox.setMinimum(20.0)
        self.spinbox.setMaximum(45.0)
        self.spinbox.setValue(37.5)

        # style spinbox
        self.spinbox.setFont(values_font)
        #box.addWidget(label_temp)

        #create button and link to signal/slot
        self.button_set      = QBase.QPushButton("&Set", parent=self)
        self.button_set.clicked.connect(self.new_temp_set)

        #Add components to widget and return
        box.addWidget(self.spinbox)
        box.addWidget(self.button_set )
        Qw.setLayout(box)


        return Qw


    def widget_buttons(self):
        '''
        buttons: Connect & Disconnect
        '''
        pass

    def new_temp_set(self):
        print("New temp set at: {} deg".format(self.spinbox.value()))

if __name__ == '__main__':
    app = QBase.QApplication(sys.argv)
    monitor = MiniAnimalMonitor()
    monitor.show()

    app.exec_()
    sys.exit(0)
