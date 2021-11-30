from PyQt5.QtCore import QCoreApplication, qInfo
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit
from .reinstaller_settings import ReinstallerSettings
from .reinstaller_paths import ReinstallerPaths
from pathlib import Path
from os import listdir
from shutil import copy2
import mobase, pathlib, os, hashlib, json, shutil, stat

class Reinstaller(QWidget):
    def __init__(self, organiser=mobase.IOrganizer):
        self.organiser = organiser
        self.settings = ReinstallerSettings(self.organiser)
        self.paths = ReinstallerPaths(self.organiser)
        super(Reinstaller, self).__init__()

    def __tr(self, trstr):
        return QCoreApplication.translate("Reinstaller", trstr)
        
    def create(self):
        downloadFiles = self.getFolderFileList(self.paths.downloadsPath())
        modFiles = []
        for file in downloadFiles:
            if not str(file).endswith('.meta') and not str(file).endswith('.unfinished'):
                modFiles.append(os.path.basename(file))

        ## Present user with a list of mods to pick from and a text box to enter the name.
        item, ok = QInputDialog.getItem(self, "Select Installer", "Installer:", modFiles, 0, False)
        if ok and item:
            name, ok = QInputDialog.getText(self, "Name", "Installer Name:", QLineEdit.Normal, str(item).split("-")[0])
            if ok and name:
                qInfo(name)
                qInfo(str(self.paths.downloadsPath() / item))

                backupFolderPath = self.paths.pluginDataPath() / name
                destFilePath = backupFolderPath / item
                self.copyTo(self.paths.downloadsPath() / item, destFilePath)
                if Path(self.paths.downloadsPath() / (str(item) + ".meta")).exists():
                    self.copyTo(self.paths.downloadsPath() / (str(item) + ".meta"), backupFolderPath / (str(item) + ".meta"))
                ## On save, copy the zip (and any .zip.meta file) to plugin data.
    
    def install(self):
        installers = self.getSubFolderList(self.paths.pluginDataPath())
        names = []
        for folder in installers:
            names.append(os.path.basename(folder))

        item, ok = QInputDialog.getItem(self, "Run Installer", "Installer:", names, 0, False)
        if ok and item:
            installerOpts = self.getFolderFileList(self.paths.pluginDataPath() / item)
            files = []
            for file in installerOpts:
                if not str(file).endswith('.meta'):
                    files.append(file)
            if len(files) == 1:
                self.organiser.installMod(str(files[0]), str(item))
            if (len(files)) > 1:
                optionFiles = []
                for opt in files:
                    optionFiles.append(os.path.basename(opt))
                item2, ok = QInputDialog.getItem(self, "Select File", "File:", optionFiles, 0, False)
                if ok and item2:
                    self.organiser.installMod(str(self.paths.pluginDataPath() / item / item2), str(item))
            
    def delete(self):
        installers = self.getSubFolderList(self.paths.pluginDataPath())
        names = []
        for folder in installers:
            names.append(os.path.basename(folder))

        item, ok = QInputDialog.getItem(self, "Delete Installer", "Installer:", names, 0, False)
        if ok and item:
            installerOpts = self.getFolderFileList(self.paths.pluginDataPath() / item)
            files = []
            for file in installerOpts:
                if not str(file).endswith('.meta'):
                    files.append(file)
            if len(files) == 1:
                shutil.rmtree(self.paths.pluginDataPath() / item)
            if (len(files)) > 1:
                optionFiles = []
                for opt in files:
                    optionFiles.append(os.path.basename(opt))
                item2, ok = QInputDialog.getItem(self, "Delete File", "File:", optionFiles, 0, False)
                if ok and item2:
                    self.deletePath(self.paths.pluginDataPath() / item / item2)
                    metaPath = self.paths.pluginDataPath() / item / (str(item2) + ".meta")
                    if (Path(metaPath).exists()):
                        self.deletePath(metaPath)

    def getFolderFileList(self, path):
        """ Lists all files in a folder, including all subfolders """
        res = []   
        # Grab the full contents of the folder.
        for fp in listdir(path):
            afp = path / fp
            # If the content is a file, add it to the list.
            if (Path.is_file(afp)):
                res.append(afp)
            # If the content is a folder, load the contents.
            if (Path.is_dir(afp)):
                res.extend(self.getFolderFileList(afp))
        return res

    def getSubFolderList(self, path):
        """ Lists all folders in a folder, including all subfolders """
        res = []   
        # Grab the full contents of the folder.
        for fp in listdir(path):
            afp = path / fp
            # If the content is a folder, add it and load subfolders.
            if (Path.is_dir(afp)):
                res.append(afp)
                res.extend(self.getSubFolderList(afp))
        return res

    def copyTo(self, fromPath=Path, toPath=Path):
        if (Path(toPath).exists()):
            os.chmod(toPath, stat.S_IWRITE)
        os.makedirs(os.path.dirname(toPath), exist_ok=True)
        copy2(fromPath, toPath)

    def deletePath(self, path=Path):
        if (Path(path).exists()):
            os.chmod(path, stat.S_IWRITE)
        os.remove(path)

    def moveTo(self, fromPath=Path, toPath=Path):
        if (Path(toPath).exists()):
            os.chmod(toPath, stat.S_IWRITE)
        os.makedirs(os.path.dirname(toPath), exist_ok=True)
        shutil.move(fromPath, toPath)