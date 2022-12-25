from typing import List


class FileSystem:
    def __init__(self) -> None:
        pass

    def ls(self, path : str) -> List[str]:  
        pass

    def mkdir(self, path : str) -> bool:
        pass

    def moveDirectory(self, oldPath : str, newPath: str) -> bool:
        pass

    def moveFile(self, oldPath : str, newPath: str) -> bool:
        pass

    def moveBufferFile(self, oldPath : str, newPath : str) -> bool:
        pass

    def createFile(self, path : str) -> bool: 
        pass

    def createBufferFile(self, path : str) -> bool: 
        pass

    def readFile(self, path : str) -> str:
        pass

    def appendLineToFile(self, path : str, line : str) -> bool:
        pass

    def pushElement(self, path : str, el: object) -> bool: 
        pass

    def consumeElement(self, path : str) -> bool:
        pass

    def deleteFile(self, path : str) -> bool:
        pass

    def deleteDirectory(self, path : str) -> bool:
        pass

    def deleteDirectoryFiles(self, path : str) -> None:
        pass

    def deleteDirectorySubdirectories(self, path : str) -> None:
        pass

    