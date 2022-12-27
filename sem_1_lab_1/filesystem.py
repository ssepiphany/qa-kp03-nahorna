import collections
from typing import List


class FileSystem:
    def __init__(self) -> None:
        self.paths = collections.defaultdict(list)
        self.logBinFileContents = collections.defaultdict(str)
        self.MAX_BUF_FILE_SIZE = 5
        self.buffContents = collections.defaultdict(list)

    def mkdir(self, path : str):
        added = False
        dirs = path.split("/")  
        for i in range(1, len(dirs)):
            cur = "/".join(dirs[:i])
            if cur not in self.paths or dirs[i] not in self.paths[cur]:
                added = True
                self.paths[cur].append(dirs[i])
        if (added == False):
            raise Exception("Directory alredy exists.")

    def createFile(self, path : str, content : str): 
        created = False
        dirs = path.split("/")

        for i in range(1, len(dirs)):
            cur = "/".join(dirs[:i])
            if cur not in self.paths or dirs[i] not in self.paths[cur]:
                created = True
                self.paths[cur].append(dirs[i])

        self.logBinFileContents[path] = content
        if (created == False):
            raise Exception("File already exists.")

    def createBufferFile(self, path : str): 
        created = False
        dirs = path.split("/")

        for i in range(1, len(dirs)):
            cur = "/".join(dirs[:i])
            if cur not in self.paths or dirs[i] not in self.paths[cur]:
                created = True
                self.paths[cur].append(dirs[i])

        self.buffContents[path].append(object())
        if (created == False):
            raise Exception("File already exists.")

    def ls(self, path : str) -> List[str]:  
        return self.paths[path]

    def moveDirectory(self, oldPath : str, newPath: str):
        if (oldPath in self.logBinFileContents):
            self.createFile(newPath)
            self.logBinFileContents[newPath] = self.logBinFileContents[oldPath]
            del self.logBinFileContents[oldPath]
            self.deleteFile(oldPath)
        else:
            raise Exception("File doesn't exist.")

    def moveFile(self, oldPath : str, newPath: str):
        if (oldPath in self.logBinFileContents):
            self.createFile(newPath, self.logBinFileContents[oldPath])
            del self.logBinFileContents[oldPath]
            self.deleteFile(oldPath)
        else:
            raise Exception("File doesn't exist.")

    def moveBufferFile(self, oldPath : str, newPath : str):
        if (oldPath in self.buffContents):
            self.createBufferFile(newPath)
            self.buffContents[newPath] = self.buffContents[oldPath]
            del self.buffContents[oldPath]
            self.deleteFile(oldPath)
        else:
            raise Exception("File doesn't exist.")

    def readFile(self, path : str) -> str:
        if path in self.logBinFileContents:
            return self.logBinFileContents[path].strip("\r\n")
        else:
            return ""

    def appendLineToFile(self, path : str, line : str):
        if path in self.logBinFileContents:
            self.logBinFileContents[path] += "\r\n" + line
        else:
            raise Exception("File doesn't exist.")

    def pushElement(self, path : str, el: object): 
        if path not in self.buffContents:
            raise Exception("File doesn't exist.")
        elif len(self.buffContents[path]) == self.MAX_BUF_FILE_SIZE: #queue.Queue(self.buffContents[path]).full()):
            # return False
            raise Exception("Cannot push new element to file. Maximum size [" + str(self.MAX_BUF_FILE_SIZE) + "] was reached.")

        self.buffContents[path].append(el)

    def consumeElement(self, path : str):
        if path not in self.buffContents:
            raise Exception("File doesn't exist.")
        elif len(self.buffContents[path]) == 0:
            raise Exception("Cannot consume the element from file. File is empty.")
        self.buffContents[path].pop(0)

    def deleteFile(self, path : str):
        dirs = path.split("/")
        pathToFile = "/".join(dirs[0:-1])

        if (dirs[-1] in self.paths[pathToFile]):
            if (path in self.logBinFileContents):
                del self.logBinFileContents[path] 
            elif (path in self.buffContents):
                del self.buffContents[path]  

            self.paths[pathToFile].remove(dirs[-1])

            if len(self.paths[pathToFile]) == 0:
                del self.paths[pathToFile]

        else:
            raise Exception("File doesn't exist.")

    def deleteDirectory(self, path : str):
        dirs = path.split("/")
        pathToDir = "/".join(dirs[0:-1])

        if (dirs[-1] in self.paths[pathToDir]):
            self.deleteDirectoryFiles(path)
            self.deleteDirectorySubdirectories(path)
            self.paths[pathToDir].remove(dirs[-1])

            if len(self.paths[pathToDir]) == 0:
                del self.paths[pathToDir]
        else:
            raise Exception("Directory doesn't exist.")

    def deleteDirectoryFiles(self, path : str) -> None:
        for x in self.paths[path]:
            filePath = path + "/" + x
            if (filePath in self.logBinFileContents):
                del self.logBinFileContents[filePath]
            elif (filePath in self.buffContents):
                del self.buffContents[filePath]

    def deleteDirectorySubdirectories(self, path : str) -> None:
        for k in list(self.paths.keys()):
            if path in k:
                del self.paths[k] 