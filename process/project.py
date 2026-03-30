"""
project.py will act as the interface used in the app.py.
This will connect all the backend processes and algorithms.
"""

from pathlib import Path
from process.load import loadData, writeData

class Project():
    def __init__(self):
        self.__path = ""

    def getPath(self) -> str:
        return self.__path
    
    def newProject(self, projectName:str):
        __path = Path("project/project.txt")
        if not __path:
            return
        
        with open(str(__path.absolute()), 'r') as __file:
            for __line in __file:
                if __line.strip("\n") == projectName:
                    return
        
        __path = Path("project")
        __data = {
            "title": projectName,
            "names": [],
            "floors": [],
            "connect": [[], [], [], [], []]
        }
        writeData(f"{str(__path.absolute())}/{projectName}.json", __data)
        with open(f"{str(__path.absolute())}/project.txt", "a") as __file:
            __file.write(f"{projectName}\n")
    
    def openProject(self, projectName:str):
        __path = Path("project/project.txt")
        if not __path:
            return
        
        with open(str(__path.absolute()), "r") as __file:
            for __line in __file:      
                if projectName in __line.strip("\n"):
                    __path = Path("project")
                    self.__path = f"{str(__path.absolute())}/{projectName}.json"
                
    def getTitle(self) -> str:
        __data = loadData(self.__path)
        return __data["title"]

    def updateTitle(self, title:str):
        __data = loadData(self.__path)
        __data["title"] = title
        writeData(self.__path, __data)
    
    def check(self, name:str) -> bool:
        __data = loadData(self.__path)
        __nameList:list[str] = __data["names"]
        if name in __nameList:
            return True
        else:
            return False