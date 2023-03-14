import os
import subprocess
import sys

def ensure_pip(where):
    args = [sys.executable, "-m", "ensurepip"]
    pip = subprocess.run(args, cwd=where)
    return pip.returncode

def install_virtualenv(where):
    args = [sys.executable, "-m", "pip", "install", "virtualenv"]
    venv = subprocess.run(args, cwd=where)
    return venv.returncode

def main(argc, argv):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pip = ensure_pip(root)
    venv = install_virtualenv(root)
    return 0 if (pip + venv) == 0 else 1

if __name__=="__main__":
    sys.exit(main(len(sys.argv), sys.argv))