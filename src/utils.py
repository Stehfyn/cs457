from enum import Enum
import os
import psutil
import stat
import sys
import tempfile

class FileMode(Enum):
    PIPED = 0
    REDIRECTED = 1
    TERMINAL = 2

def get_mode(fd):
    mode = os.fstat(fd).st_mode
    if stat.S_ISFIFO(mode):
        return FileMode.PIPED
    elif stat.S_ISREG(mode):
        return FileMode.REDIRECTED
    else:
        return FileMode.TERMINAL
    
def redirect_stdin_to_tempfile() -> tempfile:
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.close()
    with open(tmp.name, "w") as file:
        instructions = sys.stdin.buffer.read().decode("utf-8")
        file.write(instructions)
    return tmp

def running_interactively() -> bool:
    """Return True if any of our parent processes is a known shell."""
    shells = {"cmd.exe", "bash", "powershell.exe", "WindowsTerminal.exe", "gnome-terminal"}
    parent_names = {parent.name() for parent in psutil.Process().parents()}
    return bool(shells & parent_names)

if os.name == "nt":
    import pywintypes
    import win32gui
    def __hide_console_handler(hwnd, lParam):
        if win32gui.IsWindowVisible(hwnd):
            if os.getcwd()+"\main.exe" in win32gui.GetWindowText(hwnd):
                win32gui.MoveWindow(hwnd, -10000, -10000, 0, 0, True)

    def hide_console():
        win32gui.EnumWindows(__hide_console_handler, None)