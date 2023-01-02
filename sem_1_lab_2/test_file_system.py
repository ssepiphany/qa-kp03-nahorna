import pytest
from application import app
from filesystem import FileSystem

def test_can_create_directory():
    with app.test_client() as c:
        dir = {
            "path": "/my"
        }
        response = c.post('/directory/create', json=dir)

        assert response.status_code == 200
        assert response.data.decode('utf-8') == "Directory [" + dir['path'] + "]  was created."


def test_when_create_existing_direcory_should_fail():
    with app.test_client() as c:
        dir = {
            "path": "/my"
        }
        response = c.post('/directory/create', json=dir)   
        response = c.post('/directory/create', json=dir)  
        assert response.status_code == 400
        assert response.data.decode('utf-8') == "Directory already exists."


def test_when_add_more_than_max_element_to_dir_should_fail():
    fs = FileSystem()
    with app.test_client() as c:
        dir = {
            "path": "/my"
        }
        response = c.post('/directory/create', json=dir)   
        for i in range(6):
            c.post('/directory/create', json={
                "path": "/my/hello" + str(i)
            })  

        assert response.status_code == 400
        assert response.data.decode('utf-8') == "Directory " + dir["path"] + " reached limit of elements [" + str(fs.DIR_MAX_ELEMS) +"]."


def test_can_create_log_text_file():   
    content = "some text is going here"
    with app.test_client() as c:
        response = c.post('/logtextfile/create', json={
            "path": "/my/file.log",
            "content": content
        })
        assert response.status_code == 200
        list_response = c.get('/directory/list', json={
            "path": "/my"
        })
        assert "file.log" in list_response.data
        log_content_response = c.get('/logtextfile/read', json={
            "path": "/my/file.log"
        })
        assert log_content_response.data.decode('utf-8') == content

def test_can_create_bin_file():   
    content = "some text is going here"
    with app.test_client() as c:
        response = c.post('/binaryfile/create', json={
            "path": "/my/file.bin",
            "content": content
        })
    assert response.status_code == 200
    list_response = c.get('/directory/list', json={
        "path": "/my"
    })
    assert "file.bin" in list_response.data
    bin_content_response = c.get('/binaryfile/read', json={
        "path": "/my/file.bin"
    })
    assert bin_content_response.data.decode('utf-8') == content


def test_when_create_existing_log_text_file_should_fail():
    content = "some text is going here"
    with app.test_client() as c:
        file = {
            "path": "/my/file.log",
            "content": content
        }
        response = c.post('/logtextfile/create', json=file)
        response = c.post('/logtextfile/create', json=file)
    assert response.status_code == 400
    assert response.data.decode('utf-8') == "File already exists."

def test_when_create_existing_bin_file_should_fail():
    content = "some text is going here"
    with app.test_client() as c:
        file = {
            "path": "/my/file.bin",
            "content": content
        }
        response = c.post('/binaryfile/create', json=file)
        response = c.post('/binaryfile/create', json=file)
    assert response.status_code == 400
    assert response.data.decode('utf-8') == "File already exists."

def test_can_create_buffer_file(file_system): 
    with app.test_client() as c:
        response = c.post('/bufferfile/create', json={
            "path": "/my/file.buf"
        })
        assert response.status_code == 200

        list_response = c.get('/directory/list', json={
            "path": "/my"
        })
        assert "file.buf" in list_response.data
        assert len(file_system.buffContents["/my/file.buf"]) == 1


def test_when_create_existing_buffer_file_should_fail():
    with app.test_client() as c:
        file = {
            "path": "/my/file.buf"
        }
        response = c.post('/bufferfile/create', json=file)
        response = c.post('/bufferfile/create', json=file)
        assert response.status_code == 400
        assert response.data.decode('utf-8') == "File already exists."


def test_can_list_directory_contents():  
    with app.test_client() as c:
        dir_1 = {
            "path": "/my/projects"
        }
        dir_2 = {
            "path": "/my/new"
        }
        response = c.post('/directory/create', json=dir_1)
        response = c.post('directory/create', json=dir_2)

        list_response = c.get('/directory/list', json={
            "path": "/my"
        })
        assert response.status_code == 200
        assert ["projects", "new"] in list_response.data


def test_can_append_line_to_log_text_file(file_system):
    line = "some text is going here"
    with app.test_client() as c:
        response = c.post('/logtextfile/create', json={
            "path": "/my/file.log",
            "content": "first line"
        })

        append_response = c.put("logtextfile/append", json={
            "path": "/my/file.log",
            "line": line
        })

        log_content_response = c.get('/logtextfile/read', json={
            "path": "/my/file.log"
        })
        assert line in log_content_response.data.decode('utf-8')


def test_when_append_line_to_non_existing_log_text_file_should_fail(file_system):
    with app.test_client() as c:
        append_response = c.put("logtextfile/append", json={
            "path": "/my/file.log",
            "line": "some text is going here"
        })

        assert append_response.status_code == 404
        assert append_response.data.decode('utf-8') == "File doesn't exist."


def test_can_delete_log_text_file(file_system):
    with app.test_client() as c:
        response = c.post('/logtextfile/create', json={
            "path": "/my/file.log",
            "content": "file content"
        })

        delete_response = c.delete("logtextfile/delete", json={
            "path": "/my/file.log"
        })

        list_response = c.get('/directory/list', json={
            "path": "/my"
        })
        assert delete_response.status_code == 200
        assert list_response.data == ""
        assert "/my/file.log" not in file_system.logBinFileContents

def test_can_delete_bin_file(file_system):
    with app.test_client() as c:
        response = c.post('/binaryfile/create', json={
            "path": "/my/file.bin",
            "content": "file content"
        })

        delete_response = c.delete("binaryfile/delete", json={
            "path": "/my/file.bin"
        })

        list_response = c.get('/directory/list', json={
            "path": "/my"
        })
        assert delete_response.status_code == 200
        assert list_response.data == ""
        assert "/my/file.bin" not in file_system.logBinFileContents

def test_when_delete_non_existing_log_text_file_should_fail(file_system):
    with app.test_client() as c:
        delete_response = c.delete("logtextfile/delete", json={
            "path": "/my/file.log"
        })

        assert delete_response.status_code == 404
        assert delete_response.data.decode('utf-8') == "File doesn't exist."


def test_when_delete_non_existing_bin_file_should_fail():
    with app.test_client() as c:
        delete_response = c.delete("binaryfile/delete", json={
            "path": "/my/file.bin"
        })

        assert delete_response.status_code == 404
        assert delete_response.data.decode('utf-8') == "File doesn't exist."

def test_can_delete_directory(file_system):
    with app.test_client() as c:
        dir = {
            "path": "/my/projects"
        }
        response = c.post('/directory/create', json=dir)

        response = c.post('/logtextfile/create', json={
            "path": "/my/projects/file.log",
            "content": "file content"
        })

        new_dir = {
            "path": "/my/projects/new_dir"
        }
        response = c.post('/directory/create', json=new_dir)

        delete_response = c.delete("directory/delete", json={
            "path": "/my/projects"
        })

        list_response = c.get('/directory/list', json={
            "path": "/my"
        })
        assert "projects" not in list_response.data

        list_response_2 = c.get('/directory/list', json={
            "path": "/my/projects"
        })
        assert list_response_2.data.decode('utf-8') == ""
        assert "/my/projects/file.log" not in file_system.logBinFileContents


def test_when_delete_non_existing_directory_should_fail():
    with app.test_client() as c:
        delete_response = c.delete("directory/delete", json={
            "path": "/my"
        })

        assert delete_response.status_code == 404
        assert delete_response.data.decode("utf-8") == "Directory doesn't exist."


def test_can_move_directory(file_system):
    with app.test_client() as c:
        dir = {
            "path": "/my/projects"
        }
        response = c.post('/directory/create', json=dir)

        new_dir = {
            "path": "/my/new_dir"
        }
        response = c.post('/directory/create', json=new_dir)

        response = c.post('/binaryfile/create', json={
            "path": "/my/projects/file.bin",
            "content": "some text"
        })

        move_response = c.put("/directory/move", json={
            "old_path": "/my/projects",
            "new_path": "/my/new_dir/projects"
        })

        assert move_response.status_code == 200
        assert "projects" in file_system.paths["/my/new_dir"]
        assert file_system.logBinFileContents["/my/new_dir/projects/file.bin"] == "some text"


def test_when_move_non_existing_directory_should_fail(file_system):
    with app.test_client() as c:
        move_response = c.put("/directory/move", json={
            "old_path": "/my/projects",
            "new_path": "/my/new_dir/projects"
        })

        assert move_response.status_code == 404
        assert move_response.data.decode("utf-8") == "Directory doesn't exist."

def test_when_move_element_to_directory_with_same_name_element_should_fail():
    with app.test_client() as c:
        dir = {
            "path": "/my/projects"
        }
        response = c.post('/directory/create', json=dir)

        new_dir = {
            "path": "/my/new_dir/projects"
        }
        response = c.post('/directory/create', json=new_dir)

        move_response = c.put("/directory/move", json={
            "old_path": "/my/projects",
            "new_path": "/my/new_dir/projects"
        })

        assert move_response.status_code == 400
        assert move_response.data.decode("utf-8") == "An older element with the same name [projects] already exists in [new_dir] directory."

def test_can_move_log_text_file(file_system): 
    with app.test_client() as c:
        dir = {
            "path": "/my/projects"
        }
        response = c.post('/directory/create', json=dir)

        response = c.post('/logtextfile/create', json={
            "path": "/my/file.log",
            "content": "some text"
        })

        move_response = c.put("/logtextfile/move", json={
            "old_path": "/my/file.log",
            "new_path": "/my/projects/file.log"
        })

        assert move_response.status_code == 200

        list_response = c.get('/directory/list', json={
            "path": "/my/projects"
        })
        assert "file.log" in list_response.data

        assert file_system.logBinFileContents["/my/projects/file.log"] == "some text"

def test_can_move_bin_file(file_system): 
    with app.test_client() as c:
        dir = {
            "path": "/my/projects"
        }
        response = c.post('/directory/create', json=dir)

        response = c.post('/binaryfile/create', json={
            "path": "/my/file.bin",
            "content": "some text"
        })

        move_response = c.put("/binaryfile/move", json={
            "old_path": "/my/file.bin",
            "new_path": "/my/projects/file.bin"
        })

        assert move_response.status_code == 200

        list_response = c.get('/directory/list', json={
            "path": "/my/projects"
        })
        assert "file.bin" in list_response.data
        
        assert file_system.logBinFileContents["/my/projects/file.bin"] == "some text"


def test_when_move_non_existing_log_text_file_should_fail(file_system):
    with app.test_client() as c:
        move_response = c.put("/logtextfile/move", json={
            "old_path": "/my/file.log",
            "new_path": "/my/projects/file.log"
        })

        assert move_response.status_code == 404
        assert move_response.data.decode("utf-8") == "File doesn't exist."

def test_when_move_non_existing_bin_file_should_fail(file_system):
    with app.test_client() as c:
        move_response = c.put("/binaryfile/move", json={
            "old_path": "/my/file.bin",
            "new_path": "/my/projects/file.bin"
        })

        assert move_response.status_code == 404
        assert move_response.data.decode("utf-8") == "File doesn't exist."


def test_can_move_buffer_file(file_system):
    with app.test_client() as c:
        dir = {
            "path": "/my/projects"
        }
        response = c.post('/directory/create', json=dir)

        response = c.post('/bufferfile/create', json={
            "path": "/my/file.bin",
            "content": "some text"
        })

        move_response = c.put("/binaryfile/move", json={
            "old_path": "/my/file.buf",
            "new_path": "/my/projects/file.buf"
        })

        assert move_response.status_code == 200

        list_response = c.get('/directory/list', json={
            "path": "/my/projects"
        })
        assert "file.buf" in list_response.data
        
        assert len(file_system.buffContents["/my/projects/file.buf"]) == 1


def test_when_move_non_existing_buffer_file_should_fail(file_system):
    with app.test_client() as c:
        move_response = c.put("/bufferfile/move", json={
            "old_path": "/my/file.buf",
            "new_path": "/my/projects/file.buf"
        })

        assert move_response.status_code == 404
        assert move_response.data.decode("utf-8") == "File doesn't exist."


def test_can_move_subdirectories_and_files(file_system):
    with app.test_client() as c:
        dir_1 = {
            "path": "/my/new_dir"
        }
        c.post('/directory/create', json=dir_1)

        dir_2 = {
            "path": "/my/projects/subdir/here"
        }
        c.post('/directory/create', json=dir_2)

        response = c.post('/logtextfile/create', json={
            "path": "/my/projects/file.log",
            "content": "some text is going here"
        })

        move_response = c.put("/directory/move", json={
            "old_path": "/my/projects",
            "new_path": "/my/new_dir/projects"
        })

        assert move_response.status_code == 200

        list_response = c.get('/directory/list', json={
            "path": "/my/new_dir/projects"
        })
        assert ["subdir", "file.log"] in list_response.data

        list_response_2 = c.get('/directory/list', json={
            "path": "/my/new_dir/projects/subdir"
        })
        assert "here" in list_response_2.data


def test_can_read_log_text_file(file_system):
    content = "some text is going here"
    with app.test_client() as c:
        response = c.post('/logtextfile/create', json={
            "path": "/my/file.log",
            "content": content
        })

        read_response = c.get("logtextfile/read", json={
            "path": "/my/file.log"
        })
        assert response.status_code == 200
        assert read_response.data.decode("utf-8") == content

def test_can_read_bin_file(file_system):
    content = "some text is going here"
    with app.test_client() as c:
        response = c.post('/binaryfile/create', json={
            "path": "/my/file.bin",
            "content": content
        })

        read_response = c.get("binaryfile/read", json={
            "path": "/my/file.bin"
        })
        assert response.status_code == 200
        assert read_response.data.decode("utf-8") == content


def test_can_push_element_to_buffer_file(file_system): 
    with app.test_client() as c:
        response = c.post('/bufferfile/create', json={
            "path": "/my/file.buf"
        })

        push_response = c.put("bufferfile/push", json={
                "path": "/my/file.buf"
            })

        assert push_response.status_code == 200
        assert len(file_system.buffContents["/my/file.buf"]) == 2

def test_when_add_more_than_max_element_to_buffer_file_should_fail(file_system):
    with app.test_client() as c:
        response = c.post('/bufferfile/create', json={
            "path": "/my/file.buf"
        })
        
        for _ in range(5):
            push_response = c.put("bufferfile/push", json={
                "path": "/my/file.buf"
            })

        assert push_response.status_code == 400
        assert push_response.data.decode("utf-8") == "Cannot push new element to file. Maximum size [" + str(file_system.MAX_BUF_FILE_SIZE) + "] was reached."


def test_can_consume_element_from_file(file_system):
    with app.test_client() as c:
        response = c.post('/bufferfile/create', json={
            "path": "/my/file.buf"
        })

        consume_response = c.put("bufferfile/consume", json={
                "path": "/my/file.buf"
            })

        assert consume_response.status_code == 200
        assert len(file_system.buffContents["/my/file.buf"]) == 0

    

def test_when_delete_from_empty_buffer_file_should_fail(file_system):
    with app.test_client() as c:
        response = c.post('/bufferfile/create', json={
            "path": "/my/file.buf"
        })
        
        for _ in range(2):
            consume_response = c.put("bufferfile/consume", json={
                "path": "/my/file.buf"
            })

        assert consume_response.status_code == 400
        assert consume_response.data.decode("utf-8") == "Cannot consume the element from file. File is empty."