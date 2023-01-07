import collections
from typing import List


class FileSystem:
    paths = collections.defaultdict(list)
    DIR_MAX_ELEMS = 5
    logBinFileContents = collections.defaultdict(str)
    MAX_BUF_FILE_SIZE = 5
    buffContents = collections.defaultdict(list)

    def mkdir(self, path : str):
        added = self.add_elements_to_directory(path)
        if (added == False):
            raise Exception("Directory already exists.")

    def createFile(self, path : str, content : str): 
        added = self.add_elements_to_directory(path)
        self.logBinFileContents[path] = content
        if (added == False):
            raise Exception("File already exists.")

    def createBufferFile(self, path : str): 
        added = self.add_elements_to_directory(path)
        self.buffContents[path].append(object())
        if (added == False):
            raise Exception("File already exists.")

    def ls(self, path : str) -> List[str]:  
        return self.paths[path]

    def moveDirectory(self, oldPath : str, newPath: str): 
        dirs = oldPath.split("/")
        pathToDir = "/".join(dirs[0:-1]) 
        if (dirs[-1] in self.paths[pathToDir]):   
            content = self.paths[oldPath]
            self.paths[pathToDir].remove(dirs[-1])
            del self.paths[oldPath]
            self.mkdir(newPath)
            self.paths[newPath] += content
            self.delete_empty_directory_path(pathToDir)
            self.moveSubdirectories(oldPath, newPath)
            self.moveInnerBinaryAndLogTextFiles(oldPath, newPath)
            self.moveInnerBufferFiles(oldPath, newPath)
        else:
            raise Exception("Directory doesn't exist.")

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
        elif len(self.buffContents[path]) == self.MAX_BUF_FILE_SIZE:
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
            self.delete_empty_directory_path(pathToFile)

        else:
            raise Exception("File doesn't exist.")

    def deleteDirectory(self, path : str):
        dirs = path.split("/")
        pathToDir = "/".join(dirs[0:-1])

        if (dirs[-1] in self.paths[pathToDir]):
            self.deleteDirectoryFiles(path)
            self.deleteDirectorySubdirectories(path)
            self.paths[pathToDir].remove(dirs[-1])
            self.delete_empty_directory_path(pathToDir)
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

    def moveSubdirectories(self, oldPath : str, newPath : str):
        temp = dict(self.paths)
        for path in temp:
            if str(path).startswith(oldPath):
                common_part = path[len(oldPath)+1:]
                self.paths[newPath + "/" + common_part] = self.paths[path]
                del self.paths[path]

    def moveInnerBinaryAndLogTextFiles(self, oldPath : str, newPath : str):
        temp = dict(self.logBinFileContents)
        for file_path in temp:
            if str(file_path).startswith(oldPath):
                common_part = file_path[len(oldPath)+1:]
                self.logBinFileContents[newPath + "/" + common_part] = self.logBinFileContents[file_path]
                del self.logBinFileContents[file_path]

    def moveInnerBufferFiles(self, oldPath : str, newPath : str):
        temp = dict(self.buffContents)
        for file_path in temp:
            if str(file_path).startswith(oldPath):
                common_part = file_path[len(oldPath)+1:] 
                self.buffContents[newPath + "/" + common_part] = self.buffContents[file_path]
                del self.buffContents[file_path]

    def add_elements_to_directory(self, path : str) -> bool:
        added = False
        dirs = path.split("/")  
        for i in range(1, len(dirs)):
            cur = "/".join(dirs[:i])
            if cur not in self.paths or dirs[i] not in self.paths[cur]:
                if len(self.paths[cur]) == self.DIR_MAX_ELEMS:
                    raise Exception("Directory " + cur + " reached limit of elements [" + str(self.DIR_MAX_ELEMS) +"].")
                added = True
                self.paths[cur].append(dirs[i])
        return added

    def delete_empty_directory_path(self, dirPath):
        if len(self.paths[dirPath]) == 0:
                del self.paths[dirPath]