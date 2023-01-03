from flask import Flask, request
from filesystem import FileSystem
app = Flask(__name__)

fs = FileSystem()

@app.route('/directory/create', methods=['POST'])
def mkdir():
    path_to_dir = request.json['path']
    extension = str(path_to_dir).split(".")[-1]
    try:
        if (extension in ["log", "bin", "buf"]):
            return "Invalid directory name.", 400
        else:
            fs.mkdir(path_to_dir)
            return ("Directory [" + path_to_dir + "]  was created."), 201
    except Exception as ex:
        return str(ex), 400

@app.route('/binaryfile/create', methods=['POST'])
def create_bin_file():
    path_to_file = request.json['path']
    file_content = request.json['content']
    extension = str(path_to_file).split(".")[-1]

    try:
        if (extension == "bin"):
            fs.createFile(path_to_file, file_content)
            return "File [" + path_to_file + "] was created.", 201
        else:
            return "Wrong file name format [" + path_to_file + "] (filename.bin)", 400
    except Exception as ex: 
        return str(ex), 400

@app.route('/logtextfile/create', methods=['POST'])
def create_log_text_file():
    path_to_file = request.json['path']
    file_content = request.json['content']
    extension = str(path_to_file).split(".")[-1]

    try:
        if (extension == "log"):
            fs.createFile(path_to_file, file_content)
            return "File [" + path_to_file + "] was created.", 201
        else:
            return "Wrong file name format [" + path_to_file + "] (filename.log)", 400
    except Exception as ex: 
        return str(ex), 400

@app.route('/bufferfile/create', methods=['POST'])
def create_buffer_file():
    path_to_file = request.json['path']
    extension = str(path_to_file).split(".")[-1]
    try:
        if (extension == "buf"):
            fs.createBufferFile(path_to_file)
            return "File [" + path_to_file + "] was created.", 201
        else:
            return "Wrong file name format [" + path_to_file + "] (filename.buf)", 400
    except Exception as ex:
        return str(ex), 400

@app.route('/directory/list', methods=['GET'])
def list():
    path_to_file = request.json['path']
    res = fs.ls(path_to_file)
    if (len(res) == 0):
        return "Directory [" + path_to_file + "] is empty or doesn't exist.", 404
    else: 
        output = []
        for p in res:
            dir_data = {"path": p}
            output.append(dir_data)
        return output, 201

@app.route('/directory/delete', methods=['DELETE'])
def delete_directory():
    path_to_dir = request.json['path']
    extension = str(path_to_dir).split(".")[-1]
    try:
        if (extension in ["log", "bin", "buf"]):
            return "Invalid directory name.", 400
            
        fs.deleteDirectory(path_to_dir)
        return "Directory [" + path_to_dir + "] was deleted.", 200
    except Exception as ex:
        return str(ex), 404

@app.route('/binaryfile/delete', methods=['DELETE'])
def delete_binary_file():
    path_to_file = request.json['path']
    extension = str(path_to_file).split(".")[-1]

    try:
        if (extension == "bin"):
            fs.deleteFile(path_to_file)
            return "File [" + path_to_file + "] was deleted.", 200
        else:
            return "Wrong file name format [" + path_to_file + "] (filename.bin)", 400
    except Exception as ex:
        return str(ex), 404

@app.route('/logtextfile/delete', methods=['DELETE'])
def delete_log_text_file():
    path_to_file = request.json['path']
    extension = str(path_to_file).split(".")[-1]

    try:
        if (extension == "log"):
            fs.deleteFile(path_to_file)
            return "File [" + path_to_file + "] was deleted.", 200
        else:
            return "Wrong file name format [" + path_to_file + "] (filename.log)", 400
    except Exception as ex:
        return str(ex), 404

@app.route('/bufferfile/delete', methods=['DELETE'])
def delete_buffer_file():
    path_to_file = request.json['path']
    extension = str(path_to_file).split(".")[-1]

    try:
        if (extension == "buf"):
            fs.deleteFile(path_to_file)
            return "File [" + path_to_file + "] was deleted.", 200
        else:
            return "Wrong file name format [" + path_to_file + "] (filename.buf)", 400
    except Exception as ex:
        return str(ex), 404

@app.route('/directory/move', methods=['PUT'])
def move_directory():
    old_path = request.json['old_path']
    new_path = request.json['new_path']
    try: 
        fs.moveDirectory(old_path, new_path)
        return "Directory was moved from " + old_path + " to " + new_path, 200
    except Exception as ex:
        return str(ex), 404

@app.route('/binaryfile/move', methods=['PUT'])
def move_bin_file():
    old_path = request.json['old_path']
    new_path = request.json['new_path']
    extension = str(old_path).split(".")[-1]
    try: 
        if (extension == "bin"):
            fs.moveFile(old_path, new_path)
            return "File was moved from " + old_path + " to " + new_path, 200
        else:
            return "Wrong file name format [" + old_path + "] (filename.bin)", 400
    except Exception as ex:
        return str(ex), 404

@app.route('/logtextfile/move', methods=['PUT'])
def move_log_text_file():
    old_path = request.json['old_path']
    new_path = request.json['new_path']
    extension = str(old_path).split(".")[-1]
    try: 
        if (extension == "log"):
            fs.moveFile(old_path, new_path)
            return "File was moved from " + old_path + " to " + new_path, 200
        else:
            return "Wrong file name format [" + old_path + "] (filename.log)", 400 
    except Exception as ex:
        return str(ex), 404

@app.route('/bufferfile/move', methods=['PUT'])
def move_buffer_file():
    old_path = request.json['old_path']
    new_path = request.json['new_path']
    extension = str(old_path).split(".")[-1]
    try: 
        if (extension == "buf"):
            fs.moveBufferFile(old_path, new_path)
            return "File was moved from " + old_path + " to " + new_path, 200
        else:
            return "Wrong file name format [" + old_path + "] (filename.buf)"  , 400
    except Exception as ex:
        return str(ex), 404

@app.route('/binaryfile/read', methods=['GET'])
def read_bin_file():
    path_to_file = request.json['path']
    extension = str(path_to_file).split(".")[-1]

    if (extension == "bin"):
        res = fs.readFile(path_to_file)
        if (res == ""):
            return "File [" + path_to_file + "] doesn't exist.", 404
        else:
            return res, 200
    else:
        return "Wrong file name format [" + path_to_file + "] (filename.bin)", 400

@app.route('/logtextfile/read', methods=['GET'])
def read_log_text_file():
    path_to_file = request.json['path']
    extension = str(path_to_file).split(".")[-1]

    if (extension == "log"):
        res = fs.readFile(path_to_file)
        if (res == ""):
            return "File [" + path_to_file + "] doesn't exist.", 404
        else:
            return res, 200
    else:
        return "Wrong file name format [" + path_to_file + "] (filename.log)", 400

@app.route('/logtextfile/append', methods=['PUT'])
def append_line_to_log_text_file():
    path_to_file = request.json['path']
    new_line = request.json['line']
    extension = str(path_to_file).split(".")[-1]

    if (extension == "log"):
        try:
            content = " ".join(path_to_file)
            fs.appendLineToFile(path_to_file, new_line)
            return "Line [" + content + "] was appended.", 200
        except Exception as ex:
            return str(ex), 404
    else:
        return "You can only append line to log text file.", 404

@app.route('/bufferfile/push', methods=['PUT'])
def push_element_to_buffer_file():
    path_to_file = request.json['path']
    extension = str(path_to_file).split(".")[-1]

    if (extension == "buf"):
        try:
            fs.pushElement(path_to_file, object())
            return "Element was pushed to the file.", 200
        except Exception as ex:
            return str(ex), 400
    else:
        return "You can only push element to buffer file.", 400

@app.route('/bufferfile/consume', methods=['PUT'])
def consume_element_from_buffer_file():
    path_to_file = request.json['path']
    extension = str(path_to_file).split(".")[-1]

    if (extension == "buf"):
        try:
            fs.consumeElement(path_to_file)
            return "Element was consumed from the file.", 200
        except Exception as ex:
            return str(ex), 400
    else:
        return "You can only consume element from buffer file.", 400