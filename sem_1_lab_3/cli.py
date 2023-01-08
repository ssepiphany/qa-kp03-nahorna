import requests
import click

@click.group()
def cli():
    pass

@click.command(name='createdir')
@click.argument('path')
def create_directory(path):
    pass


@click.command(name='createlog')
@click.argument('path')
@click.argument('content')
def create_log_text_file(path,content):
    pass


@click.command(name='createbin')
@click.argument('path')
@click.argument('content')
def create_binary_file(path, content):
    pass


@click.command(name='createbuf')
@click.argument('path')
def create_buffer_file(path):
    pass


@click.command(name='listdir')
@click.argument('path')
def list_directory_contents(path):
    pass


@click.command(name='deletedir')
@click.argument('path')
def delete_directory(path):
    pass


@click.command(name='deletelog')
@click.argument('path')
def delete_log_text_file(path):
    pass


@click.command(name='deletebin')
@click.argument('path')
def delete_binary_file(path):
    pass



@click.command(name='deletebuf')
@click.argument('path')
def delete_buffer_file(path):
    pass


@click.command(name='movedir')
@click.argument('old_path')
@click.argument('new_path')
def move_directory(old_path, new_path):
    pass


@click.command(name='movelog')
@click.argument('old_path')
@click.argument('new_path')
def move_log_text_file(old_path, new_path):
    pass


@click.command(name='movebin')
@click.argument('old_path')
@click.argument('new_path')
def move_binary_file(old_path, new_path):
    pass


@click.command(name='movebuf')
@click.argument('old_path')
@click.argument('new_path')
def move_buffer_file(old_path, new_path):
    pass


@click.command(name='readlog')
@click.argument('path')
def read_log_text_file(path):
    pass


@click.command(name='readbin')
@click.argument('path')
def read_binary_file(path):
    pass


@click.command(name='appendlog')
@click.argument('path')
@click.argument('line')
def append_log_text_file(path, line):
    pass


@click.command(name='pushbuf')
@click.argument('path')
def push_buffer_file(path):
    pass


@click.command(name='consumebuf')
@click.argument('path')
def consume_buffer_file(path):
    pass



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