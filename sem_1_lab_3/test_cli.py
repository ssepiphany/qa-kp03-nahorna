from click.testing import CliRunner
from cli import *

runner = CliRunner()

def test_can_create_directory():
    response = runner.invoke(create_directory, "/my")
    assert response.exit_code == 0
    assert "b'Directory [/my]  was created.'\n" in response.output

def test_can_create_log_text_file():
    response = runner.invoke(create_log_text_file, ["/my/file.log", "log text file text"])
    assert response.exit_code == 0
    assert "b'File [/my/file.log] was created.'\n" in response.output


def test_can_create_binary_file():
    response = runner.invoke(create_binary_file, ["/my/file.bin", "bin file text"])
    assert response.exit_code == 0
    assert "b'File [/my/file.bin] was created.'\n" in response.output


def test_can_create_buffer_file():
    response = runner.invoke(create_buffer_file, "/my/file.buf")
    assert response.exit_code == 0
    assert "b'File [/my/file.buf] was created.'\n" in response.output


def test_can_list_directory():
    response = runner.invoke(list_directory_contents, "/my")
    assert response.exit_code == 0
    assert "b'file.log, file.bin, file.buf'\n" in response.output


def test_can_append_to_log_text_file():
    response = runner.invoke(append_log_text_file, ["/my/file.log", "second line"])
    assert response.exit_code == 0
    assert "b'Line [second line] was appended.'\n" in response.output


def test_can_move_log_text_file():
    response = runner.invoke(move_log_text_file, ["/my/file.log", "/my/hello/file.log"])
    assert response.exit_code == 0
    assert "b'File was moved from /my/file.log to /my/hello/file.log'\n" in response.output


def test_can_move_binary_file():
    response = runner.invoke(move_binary_file, ["/my/file.bin", "/my/hello/file.bin"])
    assert response.exit_code == 0
    assert "b'File was moved from /my/file.bin to /my/hello/file.bin'\n" in response.output


def test_can_move_buffer_file():
    response = runner.invoke(move_buffer_file, ["/my/file.buf", "/my/hello/file.buf"])
    assert response.exit_code == 0
    assert "b'File was moved from /my/file.buf to /my/hello/file.buf'\n" in response.output


def test_can_read_log_text_file():
    response = runner.invoke(read_log_text_file, "/my/hello/file.log")
    assert response.exit_code == 0
    assert "b'log text file text\\r\\nsecond line'\n" in response.output


def test_can_read_binary_file():
    response = runner.invoke(read_binary_file, "/my/hello/file.bin")
    assert response.exit_code == 0
    assert "b'bin file text'\n" in response.output


def test_can_push_to_buffer_file():
    response = runner.invoke(push_buffer_file, "/my/hello/file.buf")
    assert response.exit_code == 0
    assert "b'Element was pushed to the file.'\n" in response.output


def test_can_consume_from_buffer_file():
    response = runner.invoke(consume_buffer_file, "/my/hello/file.buf")
    assert response.exit_code == 0
    assert "b'Element was consumed from the file.'\n" in response.output 


def test_can_move_directory():
    response = runner.invoke(move_directory, ["/my", "/user/my"])
    assert response.exit_code == 0
    assert "b'Directory was moved from /my to /user/my'\n" in response.output


def test_can_delete_log_text_file():
    response = runner.invoke(delete_log_text_file, "/user/my/hello/file.log")
    assert response.exit_code == 0
    assert "b'File [/user/my/hello/file.log] was deleted.'\n" in response.output


def test_can_delete_binary_file():
    response = runner.invoke(delete_binary_file, "/user/my/hello/file.bin")
    assert response.exit_code == 0
    assert "b'File [/user/my/hello/file.bin] was deleted.'\n" in response.output


def test_can_delete_buffer_file():
    response = runner.invoke(delete_buffer_file, "/user/my/hello/file.buf")
    assert response.exit_code == 0
    assert "b'File [/user/my/hello/file.buf] was deleted.'\n" in response.output


def test_can_delete_directory():
    response = runner.invoke(delete_directory, "/user/my")
    assert response.exit_code == 0
    assert "b'Directory [/user/my] was deleted.'\n" in response.output