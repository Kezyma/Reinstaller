from PyQt5.QtCore import QCoreApplication
from .reinstaller_tool import ReinstallerTool
from .reinstaller import Reinstaller
import mobase

class ReinstallerInstallTool(ReinstallerTool):
    def __init__(self):
        super(ReinstallerInstallTool, self).__init__()

    def init(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        self.reinstaller = Reinstaller(self.organiser)
        return True

    def name(self):
        return self.baseName() + " Install Tool"

    def displayName(self):
        return self.baseDisplayName() + "/Install"

    def description(self):
        return self.tooltip()

    def tooltip(self):
        return self.__tr("Runs a patch installer from those backed up.")

    def __tr(self, trstr):
        return QCoreApplication.translate("Reinstaller", trstr)

    def display(self):
        self.reinstaller.install()