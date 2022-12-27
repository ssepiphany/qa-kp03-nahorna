from filesystem import FileSystem
from ast import List
import pytest

@pytest.fixture
def file_system():
    return FileSystem()

def test_can_create_directory(file_system):
    file_system.mkdir("/my/projects")
    assert "projects" in file_system.ls("/my")


def test_when_create_existing_direcory_should_fail(file_system):
    file_system.mkdir("/my")    
    with pytest.raises(Exception):
        file_system.mkdir("/my")


def test_when_add_more_than_max_element_to_dir_should_fail(file_system):
    file_system.mkdir("/my")
    for i in range(5):
        file_system.mkdir("/my/hello" + str(i))
    with pytest.raises(Exception):
        file_system.createFile("/my/file.log", "some text")


def test_can_create_log_and_bin_file(file_system):   
    content = "some text is going here"
    file_system.createFile("/my/file.log", content)
    assert ("file.log" in file_system.ls("/my") 
        and file_system.logBinFileContents["/my/file.log"] == content)


def test_when_create_existing_file_should_fail(file_system):
    file_system.createFile("/my/file.bin", "text")
    with pytest.raises(Exception):
        file_system.createFile("/my/file.bin", "text")


def test_can_create_buffer_file(file_system): 
    file_system.createBufferFile("/my/file.buf")
    assert ("file.buf" in file_system.ls("/my") 
        and len(file_system.buffContents["/my/file.buf"]) == 1)


def test_when_create_existing_buffer_file_should_fail(file_system):
    file_system.createBufferFile("/my/file.buf")
    with pytest.raises(Exception):
        file_system.createBufferFile("/my/file.buf")


def test_can_list_directory_contents(file_system):  
    file_system.mkdir("/my/projects")
    file_system.mkdir("/my/new")
    assert ["projects", "new"] == file_system.ls("/my")


def test_can_append_line_to_file(file_system):
    line = "some text is going here"
    file_system.createFile("/my/file.log", "first line")
    file_system.appendLineToFile("/my/file.log", line)
    assert line in file_system.readFile("/my/file.log")


def test_when_append_line_to_non_existing_file_should_fail(file_system):
    with pytest.raises(Exception):
        file_system.appendLineToFile("/my/file.log", "line")


def test_can_delete_file(file_system):
    file_system.createFile("/my/file.log", "file content")
    file_system.deleteFile("/my/file.log")
    assert [] == file_system.ls("/my") and "/my/file.log" not in file_system.logBinFileContents


def test_when_delete_non_existing_file_should_fail(file_system):
    with pytest.raises(Exception):
        file_system.deleteFile("/my/file.log")


def test_can_delete_directory(file_system):
    file_system.mkdir("/my/projects")
    file_system.createFile("/my/projects/file.log", "file content")
    file_system.mkdir("/my/projects/new_dir")
    file_system.deleteDirectory("/my/projects")
    assert ("projects" not in file_system.ls("/my") and file_system.ls("/my/projects") == [])
    assert ("/my/projects/file.log" not in file_system.logBinFileContents)


def test_when_delete_non_existing_directory_should_fail(file_system):
    with pytest.raises(Exception):
        file_system.deleteDirectory("/my")


def test_can_move_directory(file_system):
    file_system.mkdir("/my/projects")
    file_system.mkdir("/my/new_dir")
    file_system.createFile("/my/projects/file.bin", "some text")
    file_system.moveDirectory("/my/projects", "/my/new_dir/projects")
    assert ("projects" in file_system.paths["/my/new_dir"] and file_system.logBinFileContents["/my/new_dir/projects/file.bin"] == "some text")   


def test_when_move_non_existing_directory_should_fail(file_system):
    with pytest.raises(Exception):
        file_system.moveDirectory("/my")


def test_can_move_file(file_system): 
    file_system.mkdir("/my/projects")
    file_system.createFile("/my/file.bin", "some text")
    file_system.moveFile("/my/file.bin", "/my/projects/file.bin")
    assert ("file.bin" in file_system.ls("/my/projects") and file_system.logBinFileContents["/my/projects/file.bin"] == "some text") 


def test_when_move_non_existing_file_should_fail(file_system):
    with pytest.raises(Exception):
        file_system.moveFile("/my/file.log")


def test_can_move_buffer_file(file_system):
    file_system.mkdir("/my/projects")
    file_system.createBufferFile("/my/file.buf")
    file_system.moveBufferFile("/my/file.buf", "/my/projects/file.buf")
    assert ("file.buf" in file_system.ls("/my/projects") and len(file_system.buffContents["/my/projects/file.buf"]) == 1)


def test_when_move_non_existing_buffer_file_should_fail(file_system):
    with pytest.raises(Exception):
        file_system.moveBufferFile("/my/file.buf")


def test_can_move_subdirectories_and_files(file_system):
    file_system.mkdir("/my/new_dir")
    file_system.mkdir("/my/projects/subdir/here")
    file_system.createFile("/my/projects/file.log", "some text")
    file_system.moveDirectory("/my/projects", "/my/new_dir/projects")
    assert ["subdir", "file.log"] == file_system.ls("/my/new_dir/projects") and "here" in file_system.ls("/my/new_dir/projects/subdir")


def test_can_read_file(file_system):
    file_system.createFile("/my/file.log", "first line")
    file_system.appendLineToFile("/my/file.log", "second line")
    assert file_system.readFile("/my/file.log") == "first line\r\nsecond line"


def test_can_push_element_to_buffer_file(file_system): 
    file_system.createBufferFile("/my/file.buf")
    file_system.pushElement("/my/file.buf", object())
    assert len(file_system.buffContents["/my/file.buf"]) == 2


def test_when_add_more_than_max_element_to_buffer_file_should_fail(file_system):
    file_system.createBufferFile("/my/file.buf")
    for _ in range(4):
        file_system.pushElement("/my/file.buf", object())
    with pytest.raises(Exception):
        file_system.pushElement("/my/file.buf", object())


def test_can_consume_element_from_file(file_system):
    file_system.createBufferFile("/my/file.buf")
    file_system.consumeElement("/my/file.buf")
    assert len(file_system.buffContents["/my/file.buf"]) == 0
    

def test_when_delete_from_empty_buffer_file_should_fail(file_system):
    file_system.createBufferFile("/my/file.buf")
    file_system.consumeElement("/my/file.buf")
    with pytest.raises(Exception):
        file_system.consumeElement("/my/file.buf")