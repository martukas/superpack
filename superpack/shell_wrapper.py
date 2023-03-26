#!/usr/bin/env python

import subprocess
import shlex
import os


def run_get_posix(command: str) -> str:
    shell = os.popen(command)
    result: str = shell.read()
    shell.close()
    return result


def run_interactive_posix(command: str):
    subprocess.check_call(shlex.split(command))


def run_get_pwsh(command: str) -> str:
    process = subprocess.Popen(["pwsh", "-Command", "& {" + command + "}"],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               shell=True)
    stdout_value = process.communicate()[0]
    return stdout_value.decode('utf-8')


def run_interactive_pwsh(command: str):
    process = subprocess.Popen(["pwsh", "-Command", "& {" + command + "}"],
                               creationflags=subprocess.CREATE_NEW_CONSOLE)
    process.wait()


if __name__ == "__main__":
    import sys
    command = sys.argv[1]
    print(f"system = {os.name}")
    if os.name == "posix":
        print(run_get_posix(command))
        run_interactive_posix(command)
    elif os.name == "nt":
        print(run_get_pwsh(command))
        run_interactive_pwsh(command)
    exit(0)
