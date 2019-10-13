import sys, os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from collections import deque
import numpy as np
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QMessageBox, QApplication, QFileDialog
from PyQt5.QtCore import QTimer
import pyqtgraph as pg
from myoManager import MyoManager, EventType


class Win(QWidget):
    def __init__(self):
        super().__init__()

        self.timer = QTimer(self)
        self.gridLayout = QGridLayout(self)
        self.emgplot = pg.PlotWidget(name='EMGplot')
        self.emgcurve = []
        self.conbtn = QPushButton(self)
        self.startbtn = QPushButton(self)
        self.discbtn = QPushButton(self)
        self.pause = QPushButton(self)

        self.emg_data_queue = deque(maxlen=400)
        self.myo = None
        self.n = 400

        self.initUI()

    def initUI(self):
        self.setGeometry(400, 400, 800, 620)
        self.setWindowTitle("pyMyo")

        self.emgplot.setTitle("EMG")
        self.emgplot.setXRange(0, 400)
        self.emgplot.setYRange(0, 3000)
        self.gridLayout.addWidget(self.emgplot, 4, 1)

        for i in range(8):
            c = self.emgplot.plot(pen=(i, 10))
            c.setPos(0, i * 400)
            self.emgcurve.append(c)

        self.conbtn.setText('Connect')
        self.conbtn.clicked.connect(self.connection)
        self.conbtn.setEnabled(True)
        self.gridLayout.addWidget(self.conbtn, 0, 1)

        self.startbtn.setText('Start')
        self.startbtn.clicked.connect(self.start)
        self.startbtn.setEnabled(False)
        self.gridLayout.addWidget(self.startbtn, 1, 1)

        self.pause.setText('Pause')
        self.pause.clicked.connect(self.pause_sample)
        self.pause.setEnabled(False)
        self.gridLayout.addWidget(self.pause, 2, 1)

        self.discbtn.setText('Disconnect')
        self.discbtn.clicked.connect(self.disconnection)
        self.discbtn.setEnabled(False)
        self.gridLayout.addWidget(self.discbtn, 3, 1)

        self.setLayout(self.gridLayout)

    def connection(self):
        if not self.myo:
            self.myo = MyoManager(sender=self)

        if not self.myo.connected:
            self.myo.connect()

    def disconnection(self):
        if self.myo:
            if self.myo.connected:
                self.myo.disconnect()

    def start(self):
        if self.startbtn.isEnabled():
            self.startbtn.setEnabled(False)
            self.pause.setEnabled(True)

            self.start_sampling()
            self.timer_start()

    def start_sampling(self):
        self.emg_data_queue.append(self.myo.listener.emg)
        output_data = list(self.emg_data_queue)
        output_emg = np.array([x for x in output_data]).T

        return output_emg

    def callback(self, dictMsg):
        typeEvt = dictMsg["type"]
        if typeEvt == EventType.connected:
            self.conbtn.setEnabled(False)
            self.discbtn.setEnabled(True)
            self.startbtn.setEnabled(True)
            self.pause.setEnabled(True)

        elif typeEvt == EventType.disconnected:
            self.conbtn.setEnabled(True)
            self.discbtn.setEnabled(False)
            self.startbtn.setEnabled(False)
            self.pause.setEnabled(False)

        elif typeEvt == EventType.emg:
            self.emg_data_queue.append(dictMsg["emg"])

    def pause_sample(self):
        self.timer.stop()
        self.startbtn.setEnabled(True)
        self.pause.setEnabled(False)
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

        fileName, _ = QFileDialog.getSaveFileName(self,
                                                  "文件保存",
                                                  "./",
                                                  "All Files (*);;Text Files(*.txt)",
                                                  "Text Files(*.txt)")
        if fileName:
            with open(fileName, 'w') as f:
                f.write("{}".format(new))

        self.start()

    def closeEvent(self, event):
        result = QMessageBox.question(
            self, 'Quit', 'are you sure?',
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
