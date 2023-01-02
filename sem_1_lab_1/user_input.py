from typing import List
from filesystem import FileSystem

def processDelete():
    extension = str(command_parts[1]).split(".")[-1]

    try:
        if (extension in ["log", "bin", "buf"]):
            fs.deleteFile(command_parts[1])
        else:
            fs.deleteDirectory(command_parts[1])
    except Exception as ex:
        print(str(ex))
    else:
        print("[" + command_parts[1] + "] was deleted.")

def processMove():
    extension = str(command_parts[1]).split(".")[-1]
    try: 
        if (extension in ["log", "bin"]):
            fs.moveFile(command_parts[1], command_parts[2])
        elif (extension == "buf"):
            fs.moveBufferFile(command_parts[1], command_parts[2])
        else:
            fs.moveDirectory(command_parts[1], command_parts[2])
    except Exception as ex:
        print(str(ex))
    else:
        print("Element was moved from " + command_parts[1] + " to " + command_parts[2]) 

def processMkDir():
    try:
        fs.mkdir(command_parts[1])
        print("Directory [" + command_parts[1] + "]  was created.")
    except Exception as ex:
        print(str(ex))

def processLs():
    res = fs.ls(command_parts[1])
    if (len(res) == 0):
        print("Directory [" + command_parts[1] + "] is empty or doesn't exist.")
    else: 
        print(res)


def processCreateBufFile():
    extension = str(command_parts[1]).split(".")[-1]
    try:
        if (extension == "buf"):
            fs.createBufferFile(command_parts[1])
            print("File [" + command_parts[1] + "] was created.")
        else:
            print("Wrong file name format [" + command_parts[1] + "] (filename.extension)")
    except Exception as ex:
        print(str(ex))

def processCreateLogBinFile():
    extension = str(command_parts[1]).split(".")[-1]
    content = " ".join(command_parts[2:])

    try:
        if (extension in ["log", "bin"]):
            fs.createFile(command_parts[1], content)
            print("File [" + command_parts[1] + "] was created.")
        else:
            print("Wrong file name format [" + command_parts[1] + "] (filename.extension)")
    except Exception as ex: 
        print(str(ex))

def processRead():
    extension = str(command_parts[1]).split(".")[-1]

    if (extension in ["log", "bin"]):
        res = fs.readFile(command_parts[1])
        if (res == ""):
            print("File [" + command_parts[1] + "] doesn't exist.")
        else:
            print(res)
    else:
        print("You can only read contents of binary and log text files.")
        return

def processAppend():
    extension = str(command_parts[1]).split(".")[-1]

    if (extension == "log"):
        try:
            content = " ".join(command_parts[2:])
            fs.appendLineToFile(command_parts[1], content)
            print("Line [" + content + "] was appended.") 
        except Exception as ex:
            print(str(ex))
    else:
        print("You can only append line to log text file.")

def processPush():
    extension = str(command_parts[1]).split(".")[-1]

    if (extension == "buf"):
        try:
            fs.pushElement(command_parts[1], object())
            print("Element was pushed to the file.") 
        except Exception as ex:
            print(str(ex))
    else:
        print("You can only push element to buffer file.")

def processConsume():
    extension = str(command_parts[1]).split(".")[-1]

    if (extension == "buf"):
        try:
            fs.consumeElement(command_parts[1])
        except Exception as ex:
            print(str(ex))
    else:
        print("You can only consume element from buffer file.")



fs = FileSystem()
print("Hello")

while (True):
    print("Do you want to see the list of commands (y/n): ", end='')
    response = input().strip()
    if response == "y":
        print("1) mkdir [path] (to create directory)\r\n"
        + "2) ls [path] (to list files and subdirectories)\r\n"
        + "3) del [path] (to delete directory or file)\r\n"
        + "4) move [old path] [new path] (to move file or directory to another location)\r\n"
        + "5) create [path] [content] (to create file; [content] is only for log text and binary files)\r\n"
        + "6) read [path] (to read file contents; only for binary and log text files)\r\n"
        + "7) append [path] [line] (to append a line to the end of the log text file)\r\n"
        + "8) push [path] (to push element to the buffer file)\r\n"
        + "9) consume [path] (to pop element from the buffer file)\r\n")
        break
    elif response == "n":
        break
    else:
        print("Wrong input!")

while (True):
    print("Enter the command:")

    command_parts = input().strip().split()

    if (command_parts[0] == "exit"):
        print("Bye")
        break

    if (len(command_parts) == 2):
        if (command_parts[0] == "mkdir"):
            processMkDir()

        elif (command_parts[0] == "ls"):
            processLs()

        elif (command_parts[0] == "del"):
            processDelete()

        elif (command_parts[0] == "create"):
            processCreateBufFile()

        elif (command_parts[0] == "read"):
            processRead()

        elif (command_parts[0] == "push"):
            processPush()

        elif (command_parts[0] == "consume"):
            processConsume()

        else:
            print("No such a command.")
            continue
    elif (len(command_parts) == 3):
        if (command_parts[0] == "move"):
            processMove()
        else:
            print("No such a command.")
    else:
        if (command_parts[0] == "append"):
            processAppend()
        elif (command_parts[0] == "create"):
            processCreateLogBinFile()
        else: 
            print("No such a command.")