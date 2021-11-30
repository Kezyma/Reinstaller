from PyQt5.QtCore import QCoreApplication
from pathlib import Path
import mobase, pathlib, os

class ReinstallerPaths():
    """ Reinstaller path module. Used to load various paths for the plugin. """

    def __init__(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        super(ReinstallerPaths, self).__init__()

    _downloadsPath = str()
    def downloadsPath(self):
        """ Gets the path to the current downloads folder. """
        if self._downloadsPath == str():
            self._downloadsPath = self.organiser.downloadsPath()
        return Path(self._downloadsPath)

    _pluginDataPath = str()
    def pluginDataPath(self):
        """ Gets the path to the data folder for this plugin. """
        if self._pluginDataPath == str():
            self._pluginDataPath = Path(self.organiser.pluginDataPath()) / "reinstaller"
        if not Path(self._pluginDataPath).exists():
            os.makedirs(self._pluginDataPath)
        return Path(self._pluginDataPath)

    def safePathName(self, path):
        """ Gets a file safe string representing a specific path. """
        return "_".join(os.path.normpath(path).split(os.path.sep)).replace(":", "").replace(" ", "_")

    def sharedPath(self, basePath, childPath):
        """ Determines whether one path is a child of another path. """
        try:
            if os.path.commonpath([os.path.abspath(basePath), os.path.abspath(childPath)]) == os.path.commonpath([os.path.abspath(basePath)]):
                return True
        except:
            return False
        return False
        