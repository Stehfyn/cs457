# @auth: Stephen Foster
# @date: March 5th, 2023
# @filename: assignment1.py
# @purpose: The database program entrypoint. Depending on how the program was
# called (interactively, non-interactively, certain command-line arguments, etc.),
# this file will execute the appropriate functionality found in database.py.

import database as db

from utils import stdin_has_input
from utils import redirect_stdin_to_tempfile
from utils import running_interactively

import sys

def main(argc, argv):
    if stdin_has_input():
        tmp = redirect_stdin_to_tempfile()
        db.batch_processor([tmp.name])

    elif argc == 1 and running_interactively():
        db.interpreter()

    elif (argc == 1 and not running_interactively()) 
        or (argc == 2 and argv[1].lower() =='gui'):
        db.gui()

    elif argc >= 2:
        db.batch_processor(argv[1:])

    else:
        raise Exception("Call Error")

if __name__=="__main__":
    sys.exit(main(len(sys.argv), sys.argv))