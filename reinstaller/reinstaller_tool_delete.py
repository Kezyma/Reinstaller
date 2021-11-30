from PyQt5.QtCore import QCoreApplication
from .reinstaller_tool import ReinstallerTool
from .reinstaller import Reinstaller
import mobase

class ReinstallerDeleteTool(ReinstallerTool):
    def __init__(self):
        super(ReinstallerDeleteTool, self).__init__()

    def init(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        self.reinstaller = Reinstaller(self.organiser)
        return True

    def name(self):
        return self.baseName() + " Delete Tool"

    def displayName(self):
        return self.baseDisplayName() + "/Delete"

    def description(self):
        return self.tooltip()

    def tooltip(self):
        return self.__tr("Deletes a patch installer from those backed up.")

    def __tr(self, trstr):
        return QCoreApplication.translate("Reinstaller", trstr)

    def display(self):
        self.reinstaller.delete()