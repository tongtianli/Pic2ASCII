import sys

from PyQt5.QtCore import QDir, QStringListModel
from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog

from mainwidget import *
from ASCIIparser import *

class MainWindow(Ui_MainWidget, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.model = QStringListModel()
        self.fileList.setModel(self.model)
        self.resizeCheckBox.toggled.connect(self.checkBoxToggled)
        self.addBtn.clicked.connect(self.addFileBtnClicked)
        self.fileList.clicked.connect(self.fileListClicked)
        self.deleteBtn.clicked.connect(self.deleteFileBtnClicked)
        self.outputPathEdit.setText(QDir.currentPath())
        self.browserBtn.clicked.connect(self.browserBtnClicked)
        self.startBtn.clicked.connect(self.startBtnClicked)
        self.clearBtn.clicked.connect(self.clearBtnClicked)

    def browserBtnClicked(self):
        path = QFileDialog.getExistingDirectory(self,"选择保存路径",QDir.currentPath())
        self.outputPathEdit.setText(path)

    def fileListClicked(self):
        print(self.fileList.currentIndex().row())
        self.deleteBtn.setEnabled(True)

    def checkBoxToggled(self):
        if self.resizeCheckBox.isChecked():
            self.widthEdit.setEnabled(True)
            self.heightEdit.setEnabled(True)
        else:
            self.widthEdit.setText("240")
            self.heightEdit.setText("80")
            self.widthEdit.setEnabled(False)
            self.heightEdit.setEnabled(False)

    def addFileBtnClicked(self):
        curList = self.model.stringList()
        flist,_= QFileDialog.getOpenFileNames(self,"选择图片",QDir.currentPath(),"Image files(*.jpg *.png)")
        self.model.setStringList(curList+flist)
        if self.model.rowCount() >0:
            self.clearBtn.setEnabled(True)
            self.startBtn.setEnabled(True)

    def deleteFileBtnClicked(self):
        curIndex = self.fileList.currentIndex().row()
        self.model.removeRow(curIndex)
        if self.model.rowCount() == 0:
            self.deleteBtn.setEnabled(False)
            self.clearBtn.setEnabled(False)
            self.startBtn.setEnabled(False)

    def clearBtnClicked(self):
        self.model.removeA
        self.deleteBtn.setEnabled(False)
        self.clearBtn.setEnabled(False)
        self.startBtn.setEnabled(False)
        self.progressBar.reset()

    def startBtnClicked(self):
        width = int(self.widthEdit.text())
        height = int(self.heightEdit.text())
        outpath = self.outputPathEdit.text()
        stringList = self.model.stringList()
        self.progressBar.setMaximum(len(stringList))
        for each in stringList:
            parser = ASCIIparser(each,outpath,width,height,self)
            parser.parseConpeleted.connect(self.progressbarAcc)
            parser.start()

    def progressbarAcc(self):
        value = self.progressBar.value()
        self.progressBar.setValue(value + 1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())