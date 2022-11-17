from sys import executable, argv, exit as sys_exit
from subprocess import run

if __name__ == "__main__":
    _completed = run([executable, *argv[1:]])
    sys_exit(_completed.returncode)
