import os
import configparser
import threading

_db_lock = threading.RLock()
def threadsafe(fn):
    def new(*args, **kwargs):
        with _db_lock:
            try:
                r = fn(*args, **kwargs)
            except Exception as e:
                raise e
        return r
    return new

@threadsafe
def create_database(*dbnames: str) -> bool:
    for dbname in dbnames:
        filepath = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + f"/{dbname}")
        try:
            with open(filepath, "x"):
                print(f"Database {dbname} created.")
        except FileExistsError:
            print(f"!Failed to create database {dbname} because it already exists.")
    
@threadsafe
def drop_database(*dbnames: str) -> bool:
    for dbname in dbnames:
        filepath = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + f"/{dbname}")
        try:
            os.remove(filepath)
            print(f"Database {dbname} deleted.")
        except FileNotFoundError:
            print(f"!Failed to delete database {dbname} because it does not exist.")
    
@threadsafe
def create_table(dbname: str, tblname: str, **kwargs) -> bool:
    filepath = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + f"/{dbname}")
    db = configparser.SafeConfigParser()
    db.read(filepath)
    try:
        with open(filepath, "w") as new_db:
            if dict(db).get(tblname) == None:
                db[tblname] = kwargs
                db.write(new_db)
                print(f"Table {tblname} created.")
            else:
                db.write(new_db)
                print(f"!Failed to create table {tblname} because it already exists.")
    except FileNotFoundError:
        print(f"!Failed to create table {tblname} because {dbname} does not exist.")
        return False

@threadsafe
def drop_table(dbname: str, *tblnames) -> bool:
    filepath = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + f"/{dbname}")
    db = configparser.SafeConfigParser()
    db.read(filepath)
    try:
        db = dict(db)
        for tblname in tblnames:
            if tblname in db.keys():
                db.pop(tblname)
                print(f"Table {tblname} deleted.")
            else:
                print(f"!Failed to delete {tblname} because it does not exist.")

        with open(filepath, "w") as new_db:
            new_db_writer = configparser.SafeConfigParser()
            for key, value in db.items():
                new_db_writer[key] = value
                new_db_writer.write(new_db)

    except FileNotFoundError:
        print(f"!Failed to create table {tblname} because {dbname} does not exist.")
        return False

@threadsafe
def select_from_table(dbname: str, tblname: str, *attributes):
    filepath = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + f"/{dbname}")
    db = configparser.SafeConfigParser()
    db.read(filepath)
    try:
        if attributes[0] == '*':
            table = []
            for key, value in dict(db)[tblname].items():
                table.append(f"{key} {value}")
            output = " | ".join(table)
            print(f"{output}")

    except Exception as e:
        if isinstance(e, KeyError):
            print(f"!Failed to query table {tblname} because it does not exist.")

@threadsafe
def alter_table_add(dbname: str, tblname: str, **kwargs) -> bool:
    filepath = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + f"/{dbname}")
    db = configparser.SafeConfigParser()
    db.read(filepath)
    try:
        with open(filepath, "w") as new_db:
            for key, value in kwargs.items():
                if dict(db).get(tblname).get(key) == None:
                    db[tblname].update({key:value})
                    db.write(new_db)
                    print(f"Table {tblname} modified.")
                else:
                    print(f"Table {tblname} unable to be modified. Attribute already exists.")
                    db.write(new_db)
    except FileNotFoundError:
        print(f"!Failed to create table {tblname} because {dbname} does not exist.")
        return False

@threadsafe
def alter_table_drop(dbname: str, tblname: str, **kwargs):
    pass