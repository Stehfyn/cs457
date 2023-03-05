import database as db
import psutil
import sys

def running_interactively():
    """Return True if any of our parent processes is a known shell."""
    shells = {"cmd.exe", "bash", "powershell.exe", "WindowsTerminal.exe", "gnome-terminal"}
    parent_names = {parent.name() for parent in psutil.Process().parents()}
    return bool(shells & parent_names)

def main(argc, argv):
    if argc == 1 and running_interactively():
        db.interpreter()
    elif (argc == 1 and not running_interactively()) or argc == 2 and argv[1].lower() =='gui':
        db.gui()
    elif argc >= 2:
        db.batch_processor(argv[1:])
    else:
        raise Exception("Call Error")

if __name__=="__main__":
    sys.exit(main(len(sys.argv), sys.argv))