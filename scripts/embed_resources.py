import os
import sys

from database.embed import EmbeddedResource

def main(argc, argv):
    if argc == 2 and argv[1] == "clear":
        EmbeddedResource.clear_resources()
    
    elif argc == 2 and str(argv[1]).startswith("dir="):
        respath = os.path.abspath(argv[1][len("dir="):])
        if os.path.isdir(respath):
            for (dirpath, dirnames, filenames) in os.walk(respath):
                resources = [os.path.realpath(f"{respath}/{file}") for file in filenames]
                EmbeddedResource.embed_resources(resources)

    elif argc >= 2:
        EmbeddedResource.embed_resources(argv[1:])
        
    else:
        raise Exception("Call Error")

if __name__=="__main__":
    sys.exit(main(len(sys.argv), sys.argv))