import os
import sys

from database.embed import EmbeddedResource

def main(argc, argv):
    if argc == 2 and argv[1] == "clear":
        EmbeddedResource.clear_resources()
    elif argc >= 2:
        EmbeddedResource.embed_resources(argv[1:])
    else:
        raise Exception("Call Error")

if __name__=="__main__":
    sys.exit(main(len(sys.argv), sys.argv))