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
        modFiles = self.getDownloadFileOptions()
        item, ok = QInputDialog.getItem(self, "Select Installer", "Installer:", modFiles, 0, False)
        if ok and item:
            name, ok = QInputDialog.getText(self, "Name", "Installer Name:", QLineEdit.Normal, str(item).split("-")[0])
            if ok and name:
                self.createInstaller(str(name), str(item))
    
    def install(self):
        item, ok = QInputDialog.getItem(self, "Run Installer", "Installer:", self.getInstallerOptions(), 0, False)
        if ok and item:
            files = self.getInstallerFileOptions(item) 
            if len(files) == 1:
                self.installMod(str(item), str(os.path.basename(str(files[0]))))
            if (len(files)) > 1:
                item2, ok = QInputDialog.getItem(self, "Select File", "File:", self.getFileNamesFromList(files), 0, False)
                if ok and item2:
                    self.installMod(str(item), str(item2))
            
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

    def createInstaller(self, name, file):
        backupFolderPath = self.paths.pluginDataPath() / name
        destFilePath = backupFolderPath / file
        self.copyTo(self.paths.downloadsPath() / file, destFilePath)
        if Path(self.paths.downloadsPath() / (str(file) + ".meta")).exists():
            self.copyTo(self.paths.downloadsPath() / (str(file) + ".meta"), backupFolderPath / (str(file) + ".meta"))
        return name
        
    def installMod(self, name, file):
        self.organiser.installMod(str(self.paths.pluginDataPath() / name / file), str(name))
        return name

    def deleteMod(self, name, file):
        self.deletePath(self.paths.pluginDataPath() / name / file)
        metaPath = self.paths.pluginDataPath() / name / (str(file) + ".meta")
        if (Path(metaPath).exists()):
            self.deletePath(metaPath)
        fileOptions = self.getInstallerFileOptions(name)
        if (len(fileOptions) == 0):
            shutil.rmtree(self.paths.pluginDataPath() / name)
        return name

    def getDownloadFileOptions(self):
        downloadFiles = self.getFolderFileList(self.paths.downloadsPath())
        modFiles = []
        for file in downloadFiles:
            if not str(file).endswith('.meta') and not str(file).endswith('.unfinished'):
                modFiles.append(str(os.path.basename(file)))
        return modFiles

    def getInstallerOptions(self):
        installers = self.getSubFolderList(self.paths.pluginDataPath())
        names = []
        for folder in installers:
            names.append(os.path.basename(folder))
        return names

    def getInstallerFileOptions(self, name):
        installerOpts = self.getFolderFileList(self.paths.pluginDataPath() / name)
        files = []
        for file in installerOpts:
            if not str(file).endswith('.meta'):
                files.append(str(file))
        return files
    
    def getFileNamesFromList(self, list):
        files = []
        for item in list:
            files.append(os.path.basename(str(item)))
        return files

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