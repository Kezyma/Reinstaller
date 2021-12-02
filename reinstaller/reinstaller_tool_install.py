from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem 
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon
from pathlib import Path
from .reinstaller import Reinstaller
from .reinstaller_base import ReinstallerBase
import mobase


class ReinstallerInstallTool(ReinstallerBase, mobase.IPluginTool):

    #region Init
    def __init__(self):
        super(ReinstallerInstallTool, self).__init__()

    def init(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        self.reinstaller = Reinstaller(self.organiser)
        return True
    #endregion

    def settings(self):
        return []

    def __tr(self, trstr):
        return QCoreApplication.translate("Reinstaller", trstr)

    def icon(self):
        return QIcon(str(Path(__file__).parent.joinpath("ui-check.ico")))
        
    def name(self):
        return self.baseName() + "Install Tool"

    def displayName(self):
        return self.baseDisplayName() + "/Install"

    def description(self):
        return self.tooltip()

    def tooltip(self):
        return self.__tr("Runs an installer from a backed up file.")

    def master(self):
        return self.baseName()

    def display(self):
        self.reinstaller.install()
