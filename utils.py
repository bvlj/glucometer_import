from sys import stdout


def print_inline(message: str) -> None:
    stdout.write(u'\u001b[0K')
    stdout.write(u'\u001b[1000D')
    stdout.flush()
    print(message, end='')
