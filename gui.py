import sys
import bing
import threading
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class StyleSheet(object):
    DefaultTextEidt = "QTextEdit{ padding:5px;font-size:14px;border-style:none;font-family:微软雅黑;background:#f0faff}"
    DefaultTextBrowser = "QTextBrowser{ padding:5px;font-size:14px;border-style:none;font-family:微软雅黑;background:#f0faff;color:#1e1e1e;}"
    DefaultButton = "QWidget { font-size:14px;border-style:none;background:#26a6f2;padding:2px 0px 2px 0px;color:white;font-family:微软雅黑;}QWidget:hover {background:#3688ff}QWidget:pressed {background:#007acc}"


class MainThread(QThread):
    search_finished_signal = pyqtSignal(str)

    def set_query_list(self, words):
        self.words = words

    def run(self):
        res = bing.BingDictList(self.words)
        self.search_finished_signal.emit(res)


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setupUI()
        self.setupFunction()

    def setupUI(self):

        # variable
        margin = 7

        # self style
        self.resize(1000, 500)
        palette1 = QPalette()
        palette1.setColor(self.backgroundRole(), QColor(188, 228, 252))
        self.setPalette(palette1)

        # inputbox
        self.inputBox = QTextEdit()
        self.inputBox.setMinimumWidth(150)
        self.inputBox.setMaximumWidth(200)
        self.inputBox.setStyleSheet(StyleSheet.DefaultTextEidt)

        # search button
        self.searchButton = QPushButton('搜索')
        self.searchButton.setStyleSheet(StyleSheet.DefaultButton)

        # init vertical layout
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(margin)
        vbox.addWidget(self.inputBox)
        vbox.addWidget(self.searchButton)

        # outputbox
        self.outputBox = QTextBrowser()
        self.outputBox.setStyleSheet(StyleSheet.DefaultTextBrowser)

        # init horizontal layout
        hbox = QHBoxLayout()
        hbox.setContentsMargins(margin, margin, margin, margin)
        hbox.setSpacing(margin)
        hbox.addLayout(vbox)
        hbox.addWidget(self.outputBox)
        self.setLayout(hbox)

    def setupFunction(self):
        # search action
        self.searchButton.clicked.connect(self.on_searchButton_clicked)

        # add main thread
        self.mthread = MainThread()

        # connect signal used to tell UI searching has finished and update search result
        self.mthread.search_finished_signal.connect(self.on_search_finished)

    def on_searchButton_clicked(self):
        # set inputbox and search button to disable
        self.set_ui_disabled(True)

        # get words from inputbox
        words = self.inputBox.toPlainText().split('\n')

        self.mthread.set_query_list(words)
        self.mthread.start()

    def on_search_finished(self, res):
        ''' actions to be done when finished the search
        '''
        # update search result
        self.outputBox.setText(res)
        
        # set inputbox and search button to enable
        self.set_ui_disabled(False)


    def set_ui_disabled(self,status):
        ''' set inputbox and search button to enable/disable
        '''
        self.inputBox.setDisabled(status)
        self.searchButton.setDisabled(status)



if __name__ == '__main__':
        
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
