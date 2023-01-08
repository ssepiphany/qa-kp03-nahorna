import pytest
from application import app
from file_system import FileSystem

c = app.test_client()


def test_can_create_directory():
    dir = {
        "path": "/my"
    }
    response = c.post('/directory/create', json=dir)

    assert response.status_code == 201
    assert response.data.decode('utf-8') == "Directory [" + dir['path'] + "]  was created."


def test_when_create_existing_direcory_should_fail():
    dir = {
        "path": "/hello"
    }
    response = c.post('/directory/create', json=dir)   
    response = c.post('/directory/create', json=dir)  
    assert response.status_code == 400
    assert response.data.decode('utf-8') == "Directory already exists."


def test_when_add_more_than_max_element_to_dir_should_fail():
    for i in range(6):
        response = c.post('/directory/create', json={
            "path": "/my/dir" + str(i)
        })  

    assert response.status_code == 400
    assert response.data.decode('utf-8') == "Directory /my reached limit of elements [" + str(FileSystem.DIR_MAX_ELEMS) + "]."


def test_can_create_log_text_file():  
    content = "some text is going here"
    log_create_response = c.post('/logtextfile/create', json={
        "path": "/hello/file.log",
        "content": content
    })

    assert log_create_response.status_code == 201
    list_response = c.get('/directory/list/hello')
    assert "file.log" in list_response.data.decode("utf-8")
    log_content_response = c.get('/logtextfile/read/hello,file.log') 
    assert log_content_response.data.decode('utf-8') == content

def test_can_create_bin_file():   
    content = "some text is going here"
    response = c.post('/binaryfile/create', json={
        "path": "/hello/file.bin",
        "content": content
    })
    assert response.status_code == 201
    list_response = c.get('/directory/list/hello') 
    assert "file.bin" in list_response.data.decode("utf-8")
    bin_content_response = c.get('/binaryfile/read/hello,file.bin') 
    assert bin_content_response.data.decode('utf-8') == content


def test_when_create_existing_log_text_file_should_fail():
    content = "some text is going here"
    file = {
        "path": "/hello/file1.log",
        "content": content
    }
    c.post('/logtextfile/create', json=file)
    response = c.post('/logtextfile/create', json=file)
    assert response.status_code == 400
    assert response.data.decode('utf-8') == "File already exists."

def test_when_create_existing_bin_file_should_fail():
    content = "some text is going here"
    file = {
        "path": "/hello/file.bin",
        "content": content
    }
    response = c.post('/binaryfile/create', json=file)
    response = c.post('/binaryfile/create', json=file)
    assert response.status_code == 400
    assert response.data.decode('utf-8') == "File already exists."

def test_can_create_buffer_file(): 
    response = c.post('/bufferfile/create', json={
        "path": "/hello/file.buf"
    })
    assert response.status_code == 201

    list_response = c.get('/directory/list/hello') 
    assert "file.buf" in list_response.data.decode("utf-8")
    assert len(FileSystem.buffContents["/hello/file.buf"]) == 1


def test_when_create_existing_buffer_file_should_fail():
    file = {
        "path": "/hello/file1.buf"
    }
    response = c.post('/bufferfile/create', json=file)
    response = c.post('/bufferfile/create', json=file)
    assert response.status_code == 400
    assert response.data.decode('utf-8') == "File already exists."


def test_can_list_directory_contents():  
    dir_1 = {
        "path": "/work/projects"
    }
    dir_2 = {
        "path": "/work/new"
    }
    response = c.post('/directory/create', json=dir_1)
    response = c.post('directory/create', json=dir_2)

    list_response = c.get('/directory/list/work') 
    assert response.status_code == 201
    assert "projects, new" == list_response.data.decode("utf-8")


def test_can_append_line_to_log_text_file():
    line = "appended line"
    append_response = c.put("logtextfile/append", json={
        "path": "/hello/file.log",
        "line": line
    })
    
    assert append_response.status_code == 200
    log_content_response = c.get('/logtextfile/read/hello,file.log') 
    assert line in log_content_response.data.decode('utf-8')


def test_when_append_line_to_non_existing_log_text_file_should_fail():
    append_response = c.put("logtextfile/append", json={
        "path": "/my/somefile.log",
        "line": "some text is going here"
    })

    assert append_response.status_code == 404
    assert append_response.data.decode('utf-8') == "File doesn't exist."


def test_can_delete_log_text_file():
    delete_response = c.delete("logtextfile/delete", json={
        "path": "/hello/file.log"
    })

    list_response = c.get('/directory/list/hello') 
    assert delete_response.status_code == 200
    assert "file.log" not in list_response.data.decode("utf-8")
    assert "/hello/file.log" not in FileSystem.logBinFileContents

def test_can_delete_bin_file():
    delete_response = c.delete("binaryfile/delete", json={
        "path": "/hello/file.bin"
    })

    list_response = c.get('/directory/list/hello') 
    assert delete_response.status_code == 200
    assert "file.bin" not in list_response.data.decode("utf-8")
    assert "/hello/file.bin" not in FileSystem.logBinFileContents

def test_when_delete_non_existing_log_text_file_should_fail():
    delete_response = c.delete("logtextfile/delete", json={
        "path": "/my/filee.log"
    })

    assert delete_response.status_code == 404
    assert delete_response.data.decode('utf-8') == "File doesn't exist."


def test_when_delete_non_existing_bin_file_should_fail():
    delete_response = c.delete("binaryfile/delete", json={
        "path": "/my/filee.bin"
    })

    assert delete_response.status_code == 404
    assert delete_response.data.decode('utf-8') == "File doesn't exist."

def test_can_delete_directory():
    c.post('/logtextfile/create', json={
        "path": "/work/projects/file.log",
        "content": "file content"
    })
    new_dir = {"path": "/work/projects/new_dir"}
    c.post('/directory/create', json=new_dir)

    delete_response = c.delete("directory/delete", json={
        "path": "/work/projects"
    })

    assert delete_response.status_code == 200

    list_response = c.get('/directory/list/work')
    # assert "projects" not in list_response.get_json()
    assert "projects" not in list_response.data.decode("utf-8")

    list_response_2 = c.get('/directory/list/work,projects')
    assert list_response_2.status_code == 404
    assert "/work/projects/file.log" not in FileSystem.logBinFileContents

def test_when_delete_non_existing_directory_should_fail():
    delete_response = c.delete("directory/delete", json={
        "path": "/my/bebe"
    })

    assert delete_response.status_code == 404
    assert delete_response.data.decode("utf-8") == "Directory doesn't exist."


def test_can_move_directory():
    c.post('/binaryfile/create', json={
        "path": "/work/projects/file.bin",
        "content": "some text"
    })

    move_response = c.put("/directory/move", json={
        "old_path": "/work/projects",
        "new_path": "/work/new/projects"
    })

    assert move_response.status_code == 200
    assert "projects" in c.get("/directory/list/work,new").data.decode("utf-8")
    assert c.get("/binaryfile/read/work,new,projects,file.bin").data.decode("utf-8") == "some text" 


def test_when_move_non_existing_directory_should_fail():
    move_response = c.put("/directory/move", json={
        "old_path": "/my/projects",
        "new_path": "/my/new_dir/projects"
    })

    assert move_response.status_code == 404
    assert move_response.data.decode("utf-8") == "Directory doesn't exist."

def test_when_move_element_to_directory_with_same_name_element_should_fail():
    dir = {
        "path": "/aa/bb"
    }
    c.post('/directory/create', json=dir)

    new_dir = {
        "path": "/aa/cc/bb"
    }
    response = c.post('/directory/create', json=new_dir)

    move_response = c.put("/directory/move", json={
        "old_path": "/aa/bb",
        "new_path": "/aa/cc/bb"
    })

    assert move_response.status_code == 404
    assert move_response.data.decode("utf-8") == "Directory already exists."

def test_can_move_log_text_file(): 
    c.post('/logtextfile/create', json={
        "path": "/hello/file.log",
        "content": "some text"
    })

    move_response = c.put("/logtextfile/move", json={
        "old_path": "/hello/file.log",
        "new_path": "/hello/bye/file.log"
    })

    assert move_response.status_code == 200
    assert "file.log" in c.get('/directory/list/hello,bye').data.decode("utf-8")
    assert c.get("/logtextfile/read/hello,bye,file.log").data.decode("utf-8") == "some text" 

def test_can_move_bin_file(): 
    c.post('/binaryfile/create', json={
        "path": "/hello/file.bin",
        "content": "some text"
    })

    move_response = c.put("/binaryfile/move", json={
        "old_path": "/hello/file.bin",
        "new_path": "/hello/bye/file.bin"
    })

    assert move_response.status_code == 200
    assert "file.bin" in c.get('/directory/list/hello,bye').data.decode("utf-8")
    assert c.get("/binaryfile/read/hello,bye,file.bin").data.decode("utf-8") == "some text" 


def test_when_move_non_existing_log_text_file_should_fail():
    move_response = c.put("/logtextfile/move", json={
        "old_path": "/my/file.log",
        "new_path": "/my/projects/file.log"
    })

    assert move_response.status_code == 404
    assert move_response.data.decode("utf-8") == "File doesn't exist."

def test_when_move_non_existing_bin_file_should_fail():
    move_response = c.put("/binaryfile/move", json={
        "old_path": "/my/file.bin",
        "new_path": "/my/projects/file.bin"
    })

    assert move_response.status_code == 404
    assert move_response.data.decode("utf-8") == "File doesn't exist."


def test_can_move_buffer_file():
    c.post('/bufferfile/create', json={
        "path": "/hello/file.bin"
    })

    move_response = c.put("/bufferfile/move", json={
        "old_path": "/hello/file.buf",
        "new_path": "/hello/bye/file.buf"
    })

    assert move_response.status_code == 200
    assert "file.buf" in c.get('/directory/list/hello,bye').data.decode("utf-8")
    assert len(FileSystem.buffContents["/hello/bye/file.buf"]) == 1


def test_when_move_non_existing_buffer_file_should_fail():
    move_response = c.put("/bufferfile/move", json={
        "old_path": "/my/file.buf",
        "new_path": "/my/projects/file.buf"
    })

    assert move_response.status_code == 404
    assert move_response.data.decode("utf-8") == "File doesn't exist."


def test_can_read_log_text_file():
    read_response = c.get("/logtextfile/read/hello,bye,file.log")
    assert read_response.status_code == 200
    assert read_response.data.decode("utf-8") == "some text"

def test_can_read_bin_file():
    read_response = c.get("/binaryfile/read/hello,bye,file.bin")
    assert read_response.status_code == 200
    assert read_response.data.decode("utf-8") == "some text"


def test_can_push_element_to_buffer_file(): 
    push_response = c.put("/bufferfile/push", json={
            "path": "/hello/bye/file.buf"
        })

    assert push_response.status_code == 200
    assert len(FileSystem.buffContents["/hello/bye/file.buf"]) == 2

def test_when_add_more_than_max_element_to_buffer_file_should_fail():  
    for _ in range(5):
        push_response = c.put("/bufferfile/push", json={
            "path": "/hello/bye/file.buf"
        })

    assert push_response.status_code == 400
    assert push_response.data.decode("utf-8") == "Cannot push new element to file. Maximum size [" + str(FileSystem.MAX_BUF_FILE_SIZE) + "] was reached."


def test_can_consume_element_from_file():
    consume_response = c.put("/bufferfile/consume", json={
            "path": "/hello/bye/file.buf"
        })

    assert consume_response.status_code == 200
    assert len(FileSystem.buffContents["/hello/bye/file.buf"]) == 4

    
def test_when_delete_from_empty_buffer_file_should_fail():   
    for _ in range(5):
        consume_response = c.put("/bufferfile/consume", json={
            "path": "/hello/bye/file.buf"
        })

    assert consume_response.status_code == 400
    assert consume_response.data.decode("utf-8") == "Cannot consume the element from file. File is empty."

def test_can_move_subdirectories_and_files():
    dir = {
        "path": "/a/b/c/d"
    }
    c.post('/directory/create', json=dir)

    dir = {
        "path": "/a/e"
    }
    c.post('/directory/create', json=dir)

    c.post("/logtextfile/create", json={
        "path": "/a/b/file.log",
        "content": "some text"
    })

    move_response = c.put("/directory/move", json={
        "old_path": "/a/b",
        "new_path": "/a/e/b"
    })

    assert move_response.status_code == 200

    list_response = c.get('/directory/list/a,e,b') 
    assert "c, file.log" == list_response.data.decode("utf-8")

    list_response_2 = c.get('/directory/list/a,e,b,c')
    assert "d" in list_response_2.data.decode("utf-8")