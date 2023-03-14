import os
import subprocess
import sys

def ensure_pip(where):
    code = 0
    if os.name == "nt":
        args = [sys.executable, "-m", "ensurepip"]
        pip = subprocess.run(args, cwd=where)
        code = pip.returncode
    elif os.name =="posix":
        args = ["sudo", "apt-get", "install", "pip"]
        pip = subprocess.run(args, cwd=where)
        code  = pip.returncode
    return code

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

    act_code = 0
    if os.name == "nt":
        extension = ".bat"
        activate_script = os.path.realpath(where + "/venv/Scripts/activate" + extension)
        args = [activate_script]
        act_venv = subprocess.run(args, cwd=where)
        act_code = act_venv.returncode

    elif os.name == "posix":
        activate_script = os.path.realpath(where + "/venv/bin/activate")
        print(activate_script)
        args = ["source", activate_script]
        act_venv = subprocess.run(args, cwd=where)
        act_code = act_venv.returncode

    venv_python =  os.path.realpath(where + "/venv/Scripts/python")
    requirements = os.path.realpath(where + "/requirements.txt")
    args = [venv_python, "-m", "pip", "install", "-r", requirements]
    install_deps = subprocess.run(args, cwd=where)

    if os.name == "nt":
        args = [venv_python, "-m", "pip", "install", "pypiwin32"]
        install_pypiwin32 = subprocess.run(args,cwd=where)

    deact_code = 0
    if os.name == "nt":
        deactivate_script = os.path.realpath(where + "/venv/Scripts/deactivate" + extension)
        args = [deactivate_script]
        deact_venv = subprocess.run(args, cwd=where)
        deact_code = deact_venv.returncode

    elif os.name == "posix":
        args = ["deactivate"]
        deact_venv = subprocess.run(args, cwd=where)
        deact_code = deact_venv.returncode

    return act_venv.returncode + install_deps.returncode + deact_code.returncode

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