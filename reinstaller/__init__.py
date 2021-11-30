import mobase
from .reinstaller_tool import ReinstallerTool
from .reinstaller_tool_create import ReinstallerCreateTool
from .reinstaller_tool_delete import ReinstallerDeleteTool
from .reinstaller_tool_install import ReinstallerInstallTool

def createPlugins():
    return [ReinstallerTool(),ReinstallerCreateTool(),ReinstallerDeleteTool(),ReinstallerInstallTool()]
