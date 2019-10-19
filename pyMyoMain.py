import sys, os

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

from collections import deque
import numpy as np
from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog
from PyQt5.QtCore import QTimer, Qt
import pyqtgraph as pg
from myoManager import MyoManager, EventType
from pyMyo_alpha import Ui_Form

pg.setConfigOptions(leftButtonPan=False)
dirName = r'C:\Users'
gesCode = 'error'
gesTime = 5
newCount = 1


class Win(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.timer = QTimer(self)
        self.emgcurve = []
        self.oricurve = []
        self.acccurve = []
        self.gyrocurve = []

        self.emg_data_queue = deque(maxlen=400)
        self.acc_data_queue = deque(maxlen=100)
        self.ori_data_queue = deque(maxlen=100)
        self.gyro_data_queue = deque(maxlen=100)

        self.myo = None
        self.initUI()

    def initUI(self):
        self.emgplot = pg.PlotWidget(name='EMGplot')
        self.emgplot.setTitle("EMG")
        self.emgplot.setXRange(0, 400)
        self.emgplot.setYRange(0, 3000)
        self.ui.graph_layout.addWidget(self.emgplot)
        for i in range(8):
            c = self.emgplot.plot(pen=(i, 10))
            c.setPos(0, i * 400)
            self.emgcurve.append(c)

        self.accplot = pg.PlotWidget(name='ACCplot')
        self.accplot.setTitle("Accelerometer")
        self.ui.ACC_layout.addWidget(self.accplot)
        for i in range(3):
            c = self.accplot.plot(pen=(i, 5))
            c.setPos(0, i * 5)
            self.accplot.setXRange(0, 100)
            self.accplot.setYRange(-5, 14)
            self.acccurve.append(c)

        self.oriplot = pg.PlotWidget(name='ORIplot')
        self.oriplot.setTitle("Orientation")
        self.ui.ORI_layout.addWidget(self.oriplot)
        for i in range(4):
            c = self.oriplot.plot(pen=(i, 5))
            c.setPos(0, i * 1)
            self.oriplot.setXRange(0, 100)
            self.oriplot.setYRange(-1, 4)
            self.oricurve.append(c)

        self.gyroplot = pg.PlotWidget(name='GYROplot')
        self.gyroplot.setTitle("Gyroscope ")
        self.ui.GYRO_layout.addWidget(self.gyroplot)
        for i in range(3):
            c = self.gyroplot.plot(pen=(i, 5))
            c.setPos(0, i * 600)
            self.gyroplot.setXRange(0, 100)
            self.gyroplot.setYRange(-1000, 2500)
            self.gyrocurve.append(c)

        self.ui.connectBtn.clicked.connect(self.connection)
        self.ui.startBtn.clicked.connect(self.start)
        self.ui.saveBtn.clicked.connect(self.pause_sample)
        self.ui.disConnectBtn.clicked.connect(self.disconnection)
        self.ui.chooseDir.clicked.connect(self.chooseDir)

        self.ui.connectBtn.setEnabled(True)
        self.ui.disConnectBtn.setEnabled(False)
        self.ui.startBtn.setEnabled(False)
        self.ui.saveBtn.setEnabled(False)

        self.ui.label.setText("<A href='https://github.com/Holaplace/pyMyo'>Check for Update</a>")
        self.ui.label.setOpenExternalLinks(True)

    def connection(self):
        self.ui.chooseDir.setEnabled(False)
        self.ui.Gesture.setEnabled(False)
        self.ui.Times.setEnabled(False)

        self.ui.msgBrowser.append("Trying to connect to Myo (connection will timeout in 5 seconds)." + '\n')
        if not self.myo:
            self.myo = MyoManager(sender=self)

        if not self.myo.connected:
            self.myo.connect()

    def disconnection(self):
        self.timer.stop()

        self.ui.Gesture.clear()
        self.ui.Times.clear()

        self.ui.chooseDir.setEnabled(True)
        self.ui.Gesture.setEnabled(True)
        self.ui.Times.setEnabled(True)

        self.ui.connectBtn.setEnabled(True)
        self.ui.disConnectBtn.setEnabled(False)
        self.ui.startBtn.setEnabled(False)
        self.ui.saveBtn.setEnabled(False)

        self.ui.msgBrowser.append("Disconnected from Myo." + '\n')

        if self.myo:
            if self.myo.connected:
                self.myo.disconnect()

    def start(self):
        if self.ui.startBtn.isEnabled():
            self.ui.startBtn.setEnabled(False)
            self.ui.saveBtn.setEnabled(True)

        self.timer_start()

    def pause_sample(self):
        self.timer.stop()
        self.ui.startBtn.setEnabled(True)
        self.ui.saveBtn.setEnabled(False)
        try:
            self.saveEmgFile()
        except:
            self.ui.msgBrowser.append('Please follow the procedure as operating. \n')
            self.disconnection()

    def callback(self, dictMsg):
        typeEvt = dictMsg["type"]
        dataEvt = dictMsg["data"]

        if typeEvt == EventType.battery_level:
            self.ui.setBETTERY.setText(repr(dataEvt["battery"]))

        if typeEvt == EventType.rssi:
            self.ui.setRSSI.setText(repr(dataEvt["rssi"]))

        if typeEvt == EventType.connected:
            self.ui.msgBrowser.append("Connected to "
                                      + repr(dataEvt["name"])
                                      + "with mac address: "
                                      + repr(dataEvt["mac_address"])
                                      + '. \n')

            self.ui.connectBtn.setEnabled(False)
            self.ui.disConnectBtn.setEnabled(True)
            self.ui.startBtn.setEnabled(True)
            self.ui.saveBtn.setEnabled(False)

        elif typeEvt == EventType.disconnected:
            if dataEvt["timeout"]:
                self.ui.msgBrowser.append("Connection timed out!" + '\n')
                self.disconnection()

            if dataEvt["unOpenMyo"]:
                self.ui.msgBrowser.append("Unable to connect to Myo Connect. Is Myo Connect running?" + '\n')
                self.disconnection()

        elif typeEvt == EventType.emg:
            self.emg_data_queue.append(dataEvt["emg"])

        elif typeEvt == EventType.orientation:
            accData = [dataEvt["acceleration"][0], dataEvt["acceleration"][1], dataEvt["acceleration"][2]]
            oriData = [dataEvt["orientation"][0], dataEvt["orientation"][1],
                       dataEvt["orientation"][2], dataEvt["orientation"][3]]
            gyroData = [dataEvt["gyroscope"][0], dataEvt["gyroscope"][1], dataEvt["gyroscope"][2]]

            self.acc_data_queue.append(accData)
            self.ori_data_queue.append(oriData)
            self.gyro_data_queue.append(gyroData)

    def chooseDir(self):
        global dirName
        dirName = QFileDialog.getExistingDirectory(self,
                                                   "选取文件保存",
                                                   "./")
        self.ui.dirName.setText(dirName)

    def readConfig(self):
        global gesCode, gesTime
        gesCode = str(self.ui.Gesture.text())
        gesTime = int(self.ui.Times.text())

    def saveEmgFile(self):
        emg_data = self.update_plots_emg()
        emg_data = np.array([x for x in emg_data]).T

        temp = emg_data.flatten('A').tolist()
        new = []
        count = 0
        for i in temp:
            new.append(i)
            count += 1
            new.append('\t')
            if count % 8 == 0:
                new.append('\n')

        new = ''.join('%s' % k for k in new)  # surprise code.

        self.readConfig()
        global newCount
        if newCount <= gesTime:
            with open(dirName + '\\' + gesCode + '-' + str(newCount) + '.txt', 'w') as f:
                f.write("{}".format(new))

            self.ui.msgBrowser.append('Success in saving: \n' + gesCode + '-' + str(newCount) + '.txt \n')

            newCount += 1
            if newCount > gesTime:
                newCount = 1
                QTimer.singleShot(500, self.disconnection)
            QTimer.singleShot(500, self.start)

    def timer_start(self):
        self.timer.timeout.connect(self.update_plots_emg)
        self.timer.timeout.connect(self.update_plots_acc)
        self.timer.timeout.connect(self.update_plots_ori)
        self.timer.timeout.connect(self.update_plots_gyro)

        self.timer.start()

    def update_plots_emg(self):
        buffer0 = []
        buffer1 = []
        buffer2 = []
        buffer3 = []
        buffer4 = []
        buffer5 = []
        buffer6 = []
        buffer7 = []
        emgSolve = self.emg_data_queue
        for j in emgSolve:
            emg = j
            buffer0.append(emg[0])
            buffer1.append(emg[1])
            buffer2.append(emg[2])
            buffer3.append(emg[3])
            buffer4.append(emg[4])
            buffer5.append(emg[5])
            buffer6.append(emg[6])
            buffer7.append(emg[7])
        all_buffer = [buffer7, buffer6, buffer5, buffer4, buffer3, buffer2, buffer1, buffer0]
        for i in range(8):
            self.emgcurve[i].setData(all_buffer[i])

        return emgSolve

    def update_plots_acc(self):
        buffer8 = []
        buffer9 = []
        buffer10 = []
        accSlove = self.acc_data_queue
        for k in accSlove:
            acc = k
            buffer8.append(acc[0])
            buffer9.append(acc[1])
            buffer10.append(acc[2])
        acc_buffer = [buffer8, buffer9, buffer10]
        for i in range(3):
            self.acccurve[i].setData(acc_buffer[i])

    def update_plots_ori(self):
        buffer11 = []
        buffer12 = []
        buffer13 = []
        buffer14 = []
        oriSlove = self.ori_data_queue
        for k in oriSlove:
            ori = k
            buffer11.append(ori[0])
            buffer12.append(ori[1])
            buffer13.append(ori[2])
            buffer14.append(ori[3])
        ori_buffer = [buffer11, buffer12, buffer13, buffer14]
        for i in range(4):
            self.oricurve[i].setData(ori_buffer[i])

    def update_plots_gyro(self):
        buffer15 = []
        buffer16 = []
        buffer17 = []
        gyroSlove = self.gyro_data_queue
        for k in gyroSlove:
            gyro = k
            buffer15.append(gyro[0])
            buffer16.append(gyro[1])
            buffer17.append(gyro[2])
        gyro_buffer = [buffer15, buffer16, buffer17]
        for i in range(3):
            self.gyrocurve[i].setData(gyro_buffer[i])

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Alt:
            self.pause_sample()

    def closeEvent(self, event):
        result = QMessageBox.question(
            self, 'Quit', 'Are you sure?',
            QMessageBox.Yes | QMessageBox.No)
        if result == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
