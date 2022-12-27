import collections
from typing import List


class FileSystem:
    def __init__(self) -> None:
        pass

    def mkdir(self, path : str):
        pass

    def createFile(self, path : str, content : str): 
        pass

    def createBufferFile(self, path : str): 
        pass

    def ls(self, path : str) -> List[str]:  
        pass

    def moveDirectory(self, oldPath : str, newPath: str):
        pass

    def moveFile(self, oldPath : str, newPath: str):
        pass

    def moveBufferFile(self, oldPath : str, newPath : str):
        pass

    def readFile(self, path : str) -> str:
        pass

    def appendLineToFile(self, path : str, line : str):
        pass

    def pushElement(self, path : str, el: object): 
        pass

    def consumeElement(self, path : str):
        pass

    def deleteFile(self, path : str):
        pass

    def deleteDirectory(self, path : str):
        pass