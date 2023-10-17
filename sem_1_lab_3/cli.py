import click
import requests

@click.group()
def cli():
    pass

@click.command(name='createdir')
@click.argument('path')
def create_directory(path):
    response = requests.post("http://127.0.0.1:8888/directory/create",json={'path':path})
    print(response.content)


@click.command(name='createlog')
@click.argument('path')
@click.argument('content')
def create_log_text_file(path,content):
    content.strip("\"")
    response = requests.post("http://127.0.0.1:8888/logtextfile/create",json={
        'path': path,
        'content': content
    })
    print(response.content)


@click.command(name='createbin')
@click.argument('path')
@click.argument('content')
def create_binary_file(path, content):
    content.strip("\"")
    response = requests.post("http://127.0.0.1:8888/binaryfile/create",json={
        'path': path,
        'content': content
    })
    print(response.content)


@click.command(name='createbuf')
@click.argument('path')
def create_buffer_file(path):
    response = requests.post("http://127.0.0.1:8888/bufferfile/create",json={'path':path})
    print(response.content)


@click.command(name='listdir')
@click.argument('path')
def list_directory_contents(path):
    path_to_file = str(",".join(path.split("/")[1:]))
    response = requests.get(f"http://127.0.0.1:8888/directory/list/{path_to_file}") 
    print(response.content)


@click.command(name='deletedir')
@click.argument('path')
# @with_appcontext
def delete_directory(path):
    response = requests.delete("http://127.0.0.1:8888/directory/delete",json={'path':path})
    print(response.content)


@click.command(name='deletelog')
@click.argument('path')
def delete_log_text_file(path):
    response = requests.delete("http://127.0.0.1:8888/logtextfile/delete",json={'path':path})
    print(response.content)


@click.command(name='deletebin')
@click.argument('path')
def delete_binary_file(path):
    response = requests.delete("http://127.0.0.1:8888/binaryfile/delete",json={'path':path})
    print(response.content)



@click.command(name='deletebuf')
@click.argument('path')
def delete_buffer_file(path):
    response = requests.delete("http://127.0.0.1:8888/bufferfile/delete",json={'path':path})
    print(response.content)


@click.command(name='movedir')
@click.argument('old_path')
@click.argument('new_path')
def move_directory(old_path, new_path):
    response = requests.put("http://127.0.0.1:8888/directory/move",json={
        'old_path' : old_path,
        'new_path' : new_path
    })
    print(response.content)


@click.command(name='movelog')
@click.argument('old_path')
@click.argument('new_path')
def move_log_text_file(old_path, new_path):
    response = requests.put("http://127.0.0.1:8888/logtextfile/move",json={
        'old_path' : old_path,
        'new_path' : new_path
    })
    print(response.content)


@click.command(name='movebin')
@click.argument('old_path')
@click.argument('new_path')
def move_binary_file(old_path, new_path):
    response = requests.put("http://127.0.0.1:8888/binaryfile/move",json={
        'old_path' : old_path,
        'new_path' : new_path
    })
    print(response.content)


@click.command(name='movebuf')
@click.argument('old_path')
@click.argument('new_path')
def move_buffer_file(old_path, new_path):
    response = requests.put("http://127.0.0.1:8888/bufferfile/move",json={
        'old_path' : old_path,
        'new_path' : new_path
    })
    print(response.content)


@click.command(name='readlog')
@click.argument('path')
def read_log_text_file(path):
    path_to_file = ",".join(path.split("/")[1:])
    response = requests.get(f"http://127.0.0.1:8888/logtextfile/read/{path_to_file}")
    print(response.content)


@click.command(name='readbin')
@click.argument('path')
def read_binary_file(path):
    path_to_file = ",".join(path.split("/")[1:])
    response = requests.get(f"http://127.0.0.1:8888/binaryfile/read/{path_to_file}")
    print(response.content)


@click.command(name='appendlog')
@click.argument('path')
@click.argument('line')
def append_log_text_file(path, line):
    line.strip("\"")
    response = requests.put("http://127.0.0.1:8888/logtextfile/append",json={
        'path' : path,
        'line' : line
    })
    print(response.content)


@click.command(name='pushbuf')
@click.argument('path')
def push_buffer_file(path):
    response = requests.put("http://127.0.0.1:8888/bufferfile/push",json={'path' : path})
    print(response.content)


@click.command(name='consumebuf')
@click.argument('path')
def consume_buffer_file(path):
    response = requests.put("http://127.0.0.1:8888/bufferfile/consume",json={'path' : path})
    print(response.content)



cli.add_command(create_directory)
cli.add_command(create_log_text_file)
cli.add_command(create_binary_file)
cli.add_command(create_buffer_file)

cli.add_command(list_directory_contents)

cli.add_command(delete_directory)
cli.add_command(delete_log_text_file)
cli.add_command(delete_binary_file)
cli.add_command(delete_buffer_file)

cli.add_command(move_directory)
cli.add_command(move_log_text_file)
cli.add_command(move_binary_file)
cli.add_command(move_buffer_file)

cli.add_command(read_log_text_file)
cli.add_command(read_binary_file)

cli.add_command(append_log_text_file)

cli.add_command(push_buffer_file)
cli.add_command(consume_buffer_file)


if __name__ == '__main__':
    cli()