from subprocess import Popen, PIPE
from tempfile import mkstemp
from time import sleep as wait

from views import StartMenuView


class Runner:
    """
        This will allow us to launch the app in a separate process and communicate with it. This class supports
        context managers, and it is recommended to use them as this class has multiple open file handles
    """

    __slots__ = ["process", "temp_file", "read_stream", "write_stream"]

    def __init__(self, filename: str):
        self.temp_file = mkstemp()[1]
        self.write_stream = open(self.temp_file, "wb")
        self.read_stream = open(self.temp_file)
        self.process = Popen(filename, stdin=PIPE, stdout=self.write_stream, stderr=self.write_stream)

    def read(self, total_chars_to_read: int):
        read_data = self.read_stream.read(total_chars_to_read)
        while len(read_data) < total_chars_to_read:
            read_data = self.read_stream.read(total_chars_to_read - len(read_data))
            wait(0.1)

        return read_data

    def write(self, data: str, add_newline=True):
        if add_newline:
            data += "\n"
        self.process.stdin.write(data.encode("utf-8"))
        self.process.stdin.flush()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.process.terminate()
        self.write_stream.close()
        self.read_stream.close()

    def exit(self):
        self.process.terminate()
        self.write_stream.close()
        self.read_stream.close()
