import os

try:
    from maya import mel
    from maya import cmds
    isMaya = True
except ImportError:
    isMaya = False

def onMayaDroppedPythonFile(*args, **kwargs):
    pass


def _onMayaDropped():
    if isMaya:
        main()


def getScriptNamePathLang():
    scriptsDir = getScriptsDir()
    dirItemList = os.listdir(scriptsDir)

    scriptNamePathLang = []
    for dirItem in dirItemList:
        if dirItem.endswith(".py"):
            scriptNamePathLang.append([dirItem.split(".")[0], os.path.join(scriptsDir, dirItem), "python"])
        if dirItem.endswith(".mel"):
            scriptNamePathLang.append([dirItem.split(".")[0], os.path.join(scriptsDir, dirItem), "mel"])

    return scriptNamePathLang


def getCommand(scriptPath):
    with open(scriptPath, "r") as f:
        data = f.read()
    return data


def getScriptsDir():
    currentDir = os.path.dirname(__file__)
    scriptsDir = os.path.join(currentDir, "scripts")
    return scriptsDir


def main():
    scriptNamePathLangs = getScriptNamePathLang()
    updatedMsg = "\nUpdated...\n\n"
    createdMsg = "\nCreated...\n\n"
    for scriptNamePathLang in scriptNamePathLangs:
        name, path, commandLanguage = scriptNamePathLang
        if cmds.runTimeCommand(name, q=True, exists=True):
            cmds.runTimeCommand(name, e=True, delete=True)
            cmds.runTimeCommand(name, category="Custom Scripts", commandLanguage=commandLanguage, command=getCommand(path))
            updatedMsg += "'{}' runtime command\n".format(name)
        else:
            cmds.runTimeCommand(name, category="Custom Scripts", commandLanguage=commandLanguage, command=getCommand(path))
            createdMsg += "'{}' runtime command.\n".format(name)

    cmds.confirmDialog(title="Results",message="{0}\n-----------------------\n{1}".format(updatedMsg, createdMsg))
