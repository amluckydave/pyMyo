import sys, os

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

from collections import deque
import numpy as np
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QFileDialog
from PyQt5.QtCore import QTimer, Qt
import pyqtgraph as pg
from myoManager import MyoManager, EventType
from pyMyo_alpha import Ui_Form
from time import sleep

dirName = r'C:\Users'
gesCode = 'error'
gesTime = 5
newCount = 1


class Win(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__ui = Ui_Form()
        self.__ui.setupUi(self)

        self.timer = QTimer(self)
        self.emgcurve = []

        self.emg_data_queue = deque(maxlen=400)
        self.myo = None
        self.n = 400

        self.initUI()

    def initUI(self):
        self.emgplot = pg.PlotWidget()
        pg.setConfigOptions(leftButtonPan=False)
        self.emgplot.setTitle("EMG")
        self.emgplot.setXRange(0, 400)
        self.emgplot.setYRange(0, 3000)
        self.__ui.graph_layout.addWidget(self.emgplot)

        for i in range(8):
            c = self.emgplot.plot(pen=(i, 10))
            c.setPos(0, i * 400)
            self.emgcurve.append(c)

        self.__ui.connectBtn.clicked.connect(self.connection)
        self.__ui.connectBtn.setEnabled(True)

        self.__ui.startBtn.clicked.connect(self.start)
        self.__ui.startBtn.setEnabled(False)

        self.__ui.saveBtn.clicked.connect(self.pause_sample)
        self.__ui.saveBtn.setEnabled(False)

        self.__ui.disConnectBtn.clicked.connect(self.disconnection)
        self.__ui.disConnectBtn.setEnabled(False)

        self.__ui.chooseDir.clicked.connect(self.chooseDir)

    def connection(self):
        self.__ui.chooseDir.setEnabled(False)
        self.__ui.Gesture.setEnabled(False)
        self.__ui.Times.setEnabled(False)

        self.__ui.msgBrowser.append("Trying to connect to Myo (connection will timeout in 5 seconds)" + '\n')
        if not self.myo:
            self.myo = MyoManager(sender=self)

        if not self.myo.connected:
            self.myo.connect()

    def disconnection(self):
        self.__ui.msgBrowser.append("Disconnected from Myo" + '\n')

        if self.myo:
            if self.myo.connected:
                self.myo.disconnect()

    def start(self):
        if self.__ui.startBtn.isEnabled():
            self.__ui.startBtn.setEnabled(False)
            self.__ui.saveBtn.setEnabled(True)

        self.start_sampling()
        self.timer_start()

    def start_sampling(self):
        self.emg_data_queue.append(self.myo.listener.emg)
        output_data = list(self.emg_data_queue)
        output_emg = np.array([x for x in output_data]).T

        return output_emg

    def callback(self, dictMsg):
        typeEvt = dictMsg["type"]
        dataEvt = dictMsg["data"]

        if typeEvt == EventType.battery_level:
            self.__ui.setBETTERY.setText(repr(dataEvt["battery"]))

        if typeEvt == EventType.rssi:
            self.__ui.setRSSI.setText(repr(dataEvt["rssi"]))

        if typeEvt == EventType.connected:
            self.__ui.msgBrowser.append("Connected to "
                                        + repr(dataEvt["name"])
                                        + "with mac address: "
                                        + repr(dataEvt["mac_address"])
                                        + '\n')

            self.__ui.connectBtn.setEnabled(False)
            self.__ui.disConnectBtn.setEnabled(True)
            self.__ui.startBtn.setEnabled(True)
            self.__ui.saveBtn.setEnabled(True)

        elif typeEvt == EventType.disconnected:
            if dataEvt["timeout"]:
                self.__ui.msgBrowser.append("Connection timed out!" + '\n')

            if dataEvt["unOpenMyo"]:
                self.__ui.msgBrowser.append("Unable to connect to Myo Connect. Is Myo Connect running?" + '\n')

            self.__ui.connectBtn.setEnabled(True)
            self.__ui.disConnectBtn.setEnabled(False)
            self.__ui.startBtn.setEnabled(False)
            self.__ui.saveBtn.setEnabled(False)

        elif typeEvt == EventType.emg:
            self.emg_data_queue.append(dataEvt["emg"])

    def pause_sample(self):
        self.timer.stop()
        self.__ui.startBtn.setEnabled(True)
        self.__ui.saveBtn.setEnabled(False)
        self.saveFile()

    def timer_start(self):
        self.timer.timeout.connect(self.update_plots)
        self.timer.start()

    def update_plots(self):
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

    def chooseDir(self):
        global dirName
        dirName = QFileDialog.getExistingDirectory(self,
                                                   "选取文件保存",
                                                   "./")
        self.__ui.dirName.setText(dirName)

    def readConfig(self):
        global gesCode, gesTime
        gesCode = str(self.__ui.Gesture.text())
        gesTime = int(self.__ui.Times.text())

    def saveFile(self):
        emg_data = self.update_plots()
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

            self.__ui.msgBrowser.append('Success in saving: \n' + gesCode + '-' + str(newCount) + '.txt \n')

            newCount += 1
            sleep(1)
            self.start()
        else:
            newCount = 1
            self.__ui.chooseDir.setEnabled(True)
            self.__ui.Gesture.setEnabled(True)
            self.__ui.Times.setEnabled(True)

            self.__ui.Gesture.clear()
            self.__ui.Times.clear()
            self.disconnection()

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Win()

    win.show()
    sys.exit(app.exec_())
