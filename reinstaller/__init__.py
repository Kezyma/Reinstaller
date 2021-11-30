import mobase
from .reinstaller_tool_create import ReinstallerCreateTool
from .reinstaller_tool_install import ReinstallerInstallTool
from .reinstaller_tool_delete import ReinstallerDeleteTool

def createPlugins():
    return [ReinstallerCreateTool(),ReinstallerInstallTool(),ReinstallerDeleteTool()]
