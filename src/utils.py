import os
import psutil
import select
import sys
import tempfile

def stdin_has_input() -> bool:
    if os.name == "nt":
        import mscrt
        return msvcrt.kbhit()

    elif os.name == "posix":
        return select.select([sys.stdin,],[],[],0.0)[0]

def redirect_stdin_to_tempfile() -> tempfile:
    tmp = tempfile.NamedTemporaryFile()
    with open(tmp.name, "w") as file:
        instructions = sys.stdin.buffer.read().decode("utf-8")
        file.write(instructions)
    return tmp

def running_interactively() -> bool:
    """Return True if any of our parent processes is a known shell."""
    shells = {"cmd.exe", "bash", "powershell.exe", "WindowsTerminal.exe", "gnome-terminal"}
    parent_names = {parent.name() for parent in psutil.Process().parents()}
    return bool(shells & parent_names)