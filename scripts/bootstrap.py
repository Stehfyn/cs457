import os
import subprocess
import sys

def ensure_pip(where):
    args = [sys.executable, "-m", "ensurepip"]
    pip = subprocess.run(args, cwd=where)
    return pip.returncode

def install_virtualenv(where):
    args = [sys.executable, "-m", "pip", "install", "virtualenv"]
    install_venv = subprocess.run(args, cwd=where)
    return install_venv.returncode

def create_virtualenv(where):
    print(where)
    args = [sys.executable, "-m", "virtualenv", "venv"]
    act_venv = subprocess.run(args, cwd=where)
    return act_venv.returncode

def bootstrap_venv(where):
    extension = ''

    if os.name == "nt":
        extension = ".bat"

    activate_script = os.path.realpath(where + "/venv/Scripts/activate" + extension)
    print(activate_script)
    args = [activate_script]
    act_venv = subprocess.run(args, cwd=where)

    venv_python =  os.path.realpath(where + "/venv/Scripts/python")
    requirements = os.path.realpath(where + "/requirements.txt")
    args = [venv_python, "-m", "pip", "install", "-r", requirements]
    install_deps = subprocess.run(args, cwd=where)

    deactivate_script = os.path.realpath(where + "/venv/Scripts/deactivate" + extension)
    args = [deactivate_script]
    deact_venv = subprocess.run(args, cwd=where)

    return act_venv + install_deps + deact_venv

def main(argc, argv):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    pip = ensure_pip(root)
    install_venv = install_virtualenv(root)
    create_venv = create_virtualenv(root)
    bootstr_venv = bootstrap_venv(root)

    code = pip + install_venv + create_venv + bootstr_venv
    return code

if __name__=="__main__":
    sys.exit(main(len(sys.argv), sys.argv))