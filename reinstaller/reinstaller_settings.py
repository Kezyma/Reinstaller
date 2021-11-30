from PyQt5.QtCore import QCoreApplication
import mobase

class ReinstallerSettings():
    """ Reinstaller settings module. Used to load various plugin settings. """

    def __init__(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        super(ReinstallerSettings, self).__init__()

    def __tr(self, trstr):
        return QCoreApplication.translate("Reinstaller", trstr)   

    def enabled(self):
        """ Determines whether Reinstaller is enabled. """
        return self.organiser.pluginSetting("Reinstaller", "enabled")
        

