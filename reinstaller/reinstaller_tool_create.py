from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem 
from PyQt5 import QtWidgets, QtCore
from pathlib import Path
from .reinstaller import Reinstaller
from .reinstaller_base import ReinstallerBase
import mobase


class ReinstallerCreateTool(ReinstallerBase, mobase.IPluginTool):

    #region Init
    def __init__(self):
        super(ReinstallerCreateTool, self).__init__()

    def init(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        self.reinstaller = Reinstaller(self.organiser)
        return True
    #endregion

    def settings(self):
        return []

    def __tr(self, trstr):
        return QCoreApplication.translate("Reinstaller", trstr)
        
    def name(self):
        return self.baseName() + "Create Tool"

    def displayName(self):
        return self.baseDisplayName() + "/Create"

    def description(self):
        return self.tooltip()

    def tooltip(self):
        return self.__tr("Creates a new installer from a downloaded file.")

    def display(self):
        self.reinstaller.create()
