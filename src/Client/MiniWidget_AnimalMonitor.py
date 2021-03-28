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
        # layout.addWidget(self.widget_title("Readings:"), 1,0,1,2)
        #uncomment below when widget_readings() done
        layout.addWidget(self.widget_readings(), 1,0,1,1)
        # layout.addWidget(self.widget_title("Set Animal Temp:"), 3,0,1,1)
        layout.addWidget(self.widget_spinbox(), 2, 0, 1, 2)
        # layout.addWidget(self.widget_title("Controls:"), 5,0,1,1)
        #Uncomment Below when buttons done
        layout.addWidget(self.widget_buttons(), 3, 0, 2, 1)
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
        2020-02-04 AB: Display the temperature and Heartbeat reading
        '''
        Qw = QBase.QWidget()
        box                      = QBase.QGridLayout()
        values_font = QtGui.QFont("Times", 20, QtGui.QFont.Bold)
        labels_font = QtGui.QFont("Times", 11, QtGui.QFont.Bold)

        self.label_readings      = QBase.QLabel("Set Animal Temp:", parent=self)
        title_font = QtGui.QFont("Times", 12, QtGui.QFont.Bold)
        self.label_readings.setFont(title_font)
        self.label_readings.setStyleSheet('color: grey')

        self.label_temp    = QBase.QLabel("Animal Temp (deg.C)    :", parent=self)
        self.label_temp.setFont(labels_font)

        self.label_temp_surface =  QBase.QLabel("Surface Temp (deg.C)   :", parent=self)
        self.label_temp_surface.setFont(labels_font)

        self.label_hb      = QBase.QLabel("Heartbeat (bpm)         :", parent=self)
        self.label_hb.setFont(labels_font)


        self.text_temp    = QBase.QLabel(" 0.00 ", parent=self)
        self.text_temp.setFont(values_font)
        self.text_temp.setStyleSheet('color: green')

        self.text_temp_surface   = QBase.QLabel(" 0.00 ", parent=self)
        self.text_temp_surface.setFont(values_font)
        self.text_temp_surface.setStyleSheet('color: red')

        self.text_hb     = QBase.QLabel(" 00 ", parent=self)
        self.text_hb.setFont(values_font)
        self.text_hb.setStyleSheet('color: blue')


        # self.button_connect.clicked.connect(self.connect)
        # self.button_ping.clicked.connect(self.ping)
        # self.button_disconnect.clicked.connect(self.disconnect)
        box.addWidget(self.label_readings, 1,0,1,2)
        box.addWidget(self.label_temp, 2,0,1,1)
        box.addWidget(self.text_temp, 2,1,1,1)
        box.addWidget(self.label_temp_surface,3,0,1,1)
        box.addWidget(self.text_temp_surface,3,1,1,1)
        box.addWidget(self.label_hb,4,0,1,1)
        box.addWidget(self.text_hb,4,1,1,1)


        Qw.setLayout(box)

        return Qw

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

        self.label_set_temp      = QBase.QLabel("Set Animal Temp:", parent=self)
        title_font = QtGui.QFont("Times", 12, QtGui.QFont.Bold)
        self.label_set_temp.setFont(title_font)
        self.label_set_temp.setStyleSheet('color: grey')

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
        box.addWidget(self.label_set_temp)
        box.addWidget(self.spinbox)
        box.addWidget(self.button_set )
        Qw.setLayout(box)


        return Qw


    def widget_buttons(self):
        '''
        buttons: Connect & Disconnect
        '''
        Qw = QBase.QWidget()
        box= QBase.QVBoxLayout()

        self.label_connection      = QBase.QLabel("Connection:", parent=self)
        title_font = QtGui.QFont("Times", 12, QtGui.QFont.Bold)
        self.label_connection.setFont(title_font)
        self.label_connection.setStyleSheet('color: grey')

        self.button_connect      = QBase.QPushButton("&Connect", parent=self)
        self.button_connect.setStyleSheet('background-color: rgb(179, 255, 236)')

        self.button_ping         = QBase.QPushButton("&Ping", parent=self)
        self.button_ping.setStyleSheet('background-color: rgb(192,192,192)')

        self.button_disconnect   = QBase.QPushButton("&Disconnect", parent=self)
        self.button_disconnect.setStyleSheet('background-color: rgb(255, 51, 0)')


        self.button_connect.clicked.connect(self.connect)
        self.button_ping.clicked.connect(self.ping)
        self.button_disconnect.clicked.connect(self.disconnect)

        box.addWidget(self.label_connection)
        box.addWidget(self.button_connect)
        box.addWidget(self.button_ping)
        box.addWidget(self.button_disconnect)

        Qw.setLayout(box)

        return Qw

    def new_temp_set(self):
        print("New temp set at: {} deg".format(self.spinbox.value()))
    def ping(self):
        print("ping called")
    def connect(self):
        print("connected")
    def disconnect(self):
        print("Disconnected")

if __name__ == '__main__':
    app = QBase.QApplication(sys.argv)
    monitor = MiniAnimalMonitor()
    monitor.show()

    app.exec_()
    sys.exit(0)
