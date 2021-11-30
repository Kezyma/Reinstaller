from PyQt5.QtCore import QCoreApplication
from .reinstaller_tool import ReinstallerTool
from .reinstaller import Reinstaller
import mobase

class ReinstallerCreateTool(ReinstallerTool):
    def __init__(self):
        super(ReinstallerCreateTool, self).__init__()

    def init(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        self.reinstaller = Reinstaller(self.organiser)
        return True

    def name(self):
        return self.baseName() + " Create Tool"

    def displayName(self):
        return self.baseDisplayName() + "/Create"

    def description(self):
        return self.tooltip()

    def tooltip(self):
        return self.__tr("Creates a patch installer from a current download.")

    def __tr(self, trstr):
        return QCoreApplication.translate("Reinstaller", trstr)

    def display(self):
        self.reinstaller.create()