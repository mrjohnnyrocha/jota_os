# jota_os/shell.py
import argparse
import os
from jota_os.nfs import FileSystem
from jota_os.network import Network
from jota_os.processes import ProcessManager
from jota_os.ai import AIRunner


class Shell:
    def __init__(self, include_ai=False):
        self.input = "jota-os"
        self.fs = FileSystem()
        self.network = Network()
        self.pm = ProcessManager()
        self.ai_runner = AIRunner() if include_ai else None

    def run(self):
        while True:

            self.prompt = f"{self.input}{os.getcwd()}> "
            command = input(self.prompt)
 
            if command.startswith("cd"):
                _, dirname = command.split()
                os.chdir(dirname)
                print(f"Changed directory to {dirname}.")
            elif command.startswith("connect"):
                _, host, port = command.split()
                print(self.network.connect(host, int(port)))
            elif command.startswith("download"):
                _, url, destination = command.split()
                print(self.fs.download(url, destination))
            elif command.startswith("get_file"):
                _, path = command.split()
                print(self.fs.get_file(path))
            elif command.startswith("grep"):
                _, string, *filenames = command.split()
                for filename in filenames:
                    try:
                        with open(filename, 'r') as file:
                            for line in file:
                                if re.search(string, line):
                                    print(line, end='')
                    except FileNotFoundError:
                        print(f"File {filename} not found.")
            elif command.startswith("load_model"):
                _, data = command.split(maxsplit=1)
                self.ai_runner.load_model([int(x) for x in data.split()])
                print("Model loaded.")
            elif command.startswith("ls"):
                print("\n".join(os.listdir('.')))
            elif command.startswith("mkdir"):
                _, dirname = command.split()
                os.makedirs(dirname, exist_ok=True)
                print(f"Directory {dirname} created.")
            elif command.startswith("run"):
                _, *cmd = command.split()
                print(self.pm.run_command(' '.join(cmd)))
            elif command.startswith("pwd"):
                print(os.getcwd())
            elif command.startswith("run_inference"):
                _, instructions = command.split(maxsplit=1)
                instr = parse_instructions(instructions)
                if instr:
                    print(f"Inference result: {self.ai_runner.run_inference(instr)}")
            elif command.startswith("send"):
                _, index, message = command.split(maxsplit=2)
                print(self.network.send(int(index), message))
            elif command == "exit":
                break
            else:
                print("Unknown command.")

def main():
    parser = argparse.ArgumentParser(description="Start the jota-os shell")
    parser.add_argument('--include_ai', action='store_true', help="Include AI Runner in the shell")
    args = parser.parse_args()
    
    shell = Shell(include_ai=args.include_ai)
    shell.run()