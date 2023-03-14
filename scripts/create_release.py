import os
import subprocess
import sys

def throw_on_fail(fn):
    def new(*args, **kwargs):
        r = fn(*args, **kwargs)
        if r != 0:
            raise Exception("returncode != 0")
        return r
    return new

def get_resources_to_embed(resource_path):
    resources = []
    for (dirpath, dirnames, filenames) in os.walk(resource_path):
        resources.extend([os.path.realpath(f"{dirpath}/{file}") for file in filenames])
    return resources

@throw_on_fail
def embed_resources(here, resources):
    args = [sys.executable, "embed_resources.py"] + resources
    embed = subprocess.run(args, cwd=here)
    return embed.returncode

@throw_on_fail
def build_exe(here, exe_name, icon_path):
    root = os.path.dirname(here)
    rel_path_to_main = os.path.relpath(os.path.realpath(root + "/src/main.py"), root)
    args = ["pyinstaller", "--onefile", "--clean", f"--name={exe_name}", f"--icon={icon_path}", f"{rel_path_to_main}"]
    build = subprocess.run(args, cwd=root)
    return build.returncode

def main(argc, argv):
    if argc == 1:
        here = os.path.dirname(os.path.abspath(__file__))

        resource_path = os.path.abspath(os.path.realpath(here + "/../resources/"))
        resources = get_resources_to_embed(resource_path)
        
        icon_path = ""
        for res in resources:
            if os.path.splitext(res)[1] == ".ico" and "UniversityLogo" in res:
                icon_path = res
        
        embed_resources(here, resources)

        exe_name = "database"
        return build_exe(here, exe_name, icon_path)

    else:
        raise Exception("Call Error")

if __name__=="__main__":
    sys.exit(main(len(sys.argv), sys.argv))