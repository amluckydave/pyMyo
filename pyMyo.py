import sys, os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

from PyQt5.QtWidgets import QApplication
from pyMyoMain import *


def main():
    app = QApplication(sys.argv)
    win = Win()
    win.show()
    win.ui.msgBrowser.append(' ......pyMyo Started...... \n ')
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
