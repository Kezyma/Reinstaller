from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem 
from PyQt5 import QtWidgets, QtCore
from pathlib import Path
from .reinstaller import Reinstaller
from .reinstaller_base import ReinstallerBase
import mobase


class ReinstallerTool(ReinstallerBase, mobase.IPluginTool):

    #region Init
    def __init__(self):
        super(ReinstallerTool, self).__init__()

    def init(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        self.reinstaller = Reinstaller(self.organiser)
        self.dialog = self.getDialog()
        return True
    #endregion

    def settings(self):
        return []

    def __tr(self, trstr):
        return QCoreApplication.translate("Reinstaller", trstr)
        
    def name(self):
        return self.baseName()

    def displayName(self):
        return self.baseDisplayName()

    def description(self):
        return self.tooltip()

    def tooltip(self):
        return self.__tr("Opens Reinstaller manager.")

    def display(self):
        self.dialog.show()
        self.rebindUi()

    # Add File

    def addFileTextChanged(self):
        value = self.addFileText.text().strip()
        if value:
            self.addButton.setEnabled(True)
        else:
            self.addButton.setEnabled(False)

    def addFileSelectChanged(self):
        value = self.addFileSelect.currentText()
        if value:
            self.addFileText.setEnabled(True)
            self.addButton.setEnabled(True)
            self.addFileText.setText(str(value).split("-")[0].split(".")[0].strip())
        else:
            self.addFileText.setEnabled(False)
            self.addButton.setEnabled(False)

    def addButtonClick(self):
        name = self.reinstaller.createInstaller(self.addFileText.text().strip(), self.addFileSelect.currentText())
        self.rebindUi()
        return True

    # Install File

    def installerListChanged(self):
        item = self.installerList.currentItem()
        self.installerSelect.clear()
        self.installButton.setEnabled(False)
        self.deleteButton.setEnabled(False)
        if item:
            fileOptions = self.reinstaller.getFileNamesFromList(self.reinstaller.getInstallerFileOptions(item.text()))
            if len(fileOptions) > 0:
                self.installerSelect.addItems(fileOptions)
                self.installButton.setEnabled(True)
                self.deleteButton.setEnabled(True)

    def installButtonClick(self):
        modName = self.installerList.currentItem().text()
        modPath = self.installerSelect.currentText()
        self.reinstaller.installMod(str(modName), str(modPath))

    def deleteButtonClick(self):
        modName = self.installerList.currentItem().text()
        modPath = self.installerSelect.currentText()
        name = self.reinstaller.deleteMod(str(modName), str(modPath))
        self.rebindUi()

    def rebindUi(self):
        self.addFileSelect.clear()
        self.addFileSelect.addItems(self.reinstaller.getDownloadFileOptions())

        self.installerList.clear()
        self.installerList.addItems(self.reinstaller.getInstallerOptions())

    def getDialog(self):
        dialog = QtWidgets.QDialog()
        self.setupUi(dialog)
        return  dialog

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(560, 310)
        Dialog.setWindowTitle("Reinstaller")

        ## Add New Mod
        self.addFileTextLabel = QtWidgets.QLabel(Dialog)
        self.addFileTextLabel.setGeometry(QtCore.QRect(10, 5, 47, 13))
        self.addFileTextLabel.setObjectName("addFileTextLabel")
        self.addFileTextLabel.setText("Name")

        self.addFileText = QtWidgets.QLineEdit(Dialog)
        self.addFileText.setGeometry(QtCore.QRect(10, 20, 180, 20))
        self.addFileText.setObjectName("addFileText")
        self.addFileText.setEnabled(False)
        self.addFileText.textChanged.connect(self.addFileTextChanged)

        self.addFileSelectLabel = QtWidgets.QLabel(Dialog)
        self.addFileSelectLabel.setGeometry(QtCore.QRect(200, 5, 47, 13))
        self.addFileSelectLabel.setObjectName("addFileSelectLabel")
        self.addFileSelectLabel.setText("File")

        self.addFileSelect = QtWidgets.QComboBox(Dialog)
        self.addFileSelect.setGeometry(QtCore.QRect(200, 20, 280, 20))
        self.addFileSelect.setObjectName("addFileSelect")
        self.addFileSelect.currentIndexChanged.connect(self.addFileSelectChanged)

        self.addButton = QtWidgets.QPushButton(Dialog)
        self.addButton.setGeometry(QtCore.QRect(490, 19, 60, 22))
        self.addButton.setObjectName("addButton")
        self.addButton.setText("Add")
        self.addButton.setEnabled(False)
        self.addButton.clicked.connect(self.addButtonClick)

        self.line = QtWidgets.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(0, 45, 560, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        # Select Existing Mod
        self.installersLabel = QtWidgets.QLabel(Dialog)
        self.installersLabel.setGeometry(QtCore.QRect(10, 60, 47, 13))
        self.installersLabel.setObjectName("installersLabel")
        self.installersLabel.setText("Installers")

        self.installerList = QtWidgets.QListWidget(Dialog)
        self.installerList.setGeometry(QtCore.QRect(10, 75, 540, 200))
        self.installerList.setObjectName("installerList")
        self.installerList.currentItemChanged.connect(self.installerListChanged)
        
        self.installerSelect = QtWidgets.QComboBox(Dialog)
        self.installerSelect.setGeometry(QtCore.QRect(10, 280, 400, 21))
        self.installerSelect.setObjectName("installerSelect")

        self.installButton = QtWidgets.QPushButton(Dialog)
        self.installButton.setGeometry(QtCore.QRect(420, 279, 60, 22))
        self.installButton.setObjectName("installButton")
        self.installButton.setText("Install")
        self.installButton.setEnabled(False)
        self.installButton.clicked.connect(self.installButtonClick)

        self.deleteButton = QtWidgets.QPushButton(Dialog)
        self.deleteButton.setGeometry(QtCore.QRect(490, 279, 60, 22))
        self.deleteButton.setObjectName("deleteButton")
        self.deleteButton.setText("Delete")
        self.deleteButton.setEnabled(False)
        self.deleteButton.clicked.connect(self.deleteButtonClick)

        QtCore.QMetaObject.connectSlotsByName(Dialog)
    
