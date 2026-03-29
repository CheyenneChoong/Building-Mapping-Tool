"""
project.py will act as the interface used in the app.py.
This will connect all the backend processes and algorithms.
"""

from pathlib import Path
import json

class Project():
    def __init__(self):
        self.__path = ""
    
    def newProject(self, projectName:str):
        __path = Path("process/project/project.txt")
        if not __path:
            return
        
        with open(str(__path.absolute()), 'r') as __file:
            for __line in __file:
                if __line.strip("\n") == projectName:
                    return
        
        __path = Path("process/project")
        with open(f"{str(__path.absolute())}/{projectName}.json", 'w') as __file:
            __data = {
                "title": projectName,
                "names": [],
                "floors": [],
                "connect": [[], [], []]
            }
            json.dump(__data, __file, indent=4)
        with open(f"{str(__path.absolute())}/project.txt", 'a') as __file:
            __file.write(f"{projectName}\n")
    
    def openProject(self, projectName:str):
        __path = Path("process/project/project.txt")
        if not __path:
            return
        
        with open(str(__path.absolute()), 'r') as __file:
            __data = __file.readlines()
        
        if projectName in __data:
            __path = Path("process/project")
            self.__path = f"{__path}/{projectName}.json"