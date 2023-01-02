from flask import Flask, request
app = Flask(__name__)
from filesystem import FileSystem


@app.route('/directory/create', methods=['POST'])
def mkdir():
    pass

@app.route('/binaryfile/create', methods=['POST'])
def create_bin_file():
    pass

@app.route('/logtextfile/create', methods=['POST'])
def create_log_text_file():
    pass

@app.route('/bufferfile/create', methods=['POST'])
def create_buffer_file():
    pass

@app.route('/directory/list', methods=['GET'])
def list():
    pass

@app.route('/directory/delete', methods=['DELETE'])
def delete_directory():
    pass

@app.route('/binaryfile/delete', methods=['DELETE'])
def delete_binary_file():
    pass

@app.route('/logtextfile/delete', methods=['DELETE'])
def delete_log_text_file():
    pass

@app.route('/bufferfile/delete', methods=['DELETE'])
def delete_buffer_file():
    pass

@app.route('/directory/move', methods=['PUT'])
def move_directory():
    pass

@app.route('/binaryfile/move', methods=['PUT'])
def move_bin_file():
    pass

@app.route('/logtextfile/move', methods=['PUT'])
def move_log_text_file():
    pass

@app.route('/bufferfile/move', methods=['PUT'])
def move_buffer_file():
    pass

@app.route('/binaryfile/read', methods=['GET'])
def read_bin_file():
    pass

@app.route('/logtextfile/read', methods=['GET'])
def read_log_text_file():
    pass

@app.route('/logtextfile/append', methods=['PUT'])
def append_line_to_log_text_file():
    pass

@app.route('/bufferfile/push', methods=['PUT'])
def push_element_to_buffer_file():
    pass

@app.route('/bufferfile/consume', methods=['PUT'])
def consume_element_from_buffer_file():
    pass