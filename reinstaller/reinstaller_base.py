from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from pathlib import Path
from .reinstaller import Reinstaller
import mobase

class ReinstallerBase():

    #region Init
    def __init__(self):
        super(ReinstallerBase, self).__init__()

    def init(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        self.reinstaller = Reinstaller(self.organiser)
        return True
    #endregion

    def version(self):
        return mobase.VersionInfo(1, 0, 3, mobase.ReleaseType.ALPHA) 

    def isActive(self):
        return self.reinstaller.settings.enabled()

    def __tr(self, trstr):
        return QCoreApplication.translate("Reinstaller", trstr)

    def icon(self):
        return QIcon(str(Path(__file__).parent.joinpath("rootbuilder.ico")))

    def author(self):
        return "Kezyma"

    def baseName(self):
        return "Reinstaller"

    def baseDisplayName(self):
        return "Reinstaller"

    def settings(self):
        """ Current list of game settings for Mod Organizer. """
        return [
            mobase.PluginSetting("enabled",self.__tr("Enables Reinstaller"),True)
            ]