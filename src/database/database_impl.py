# @auth: Stephen Foster
# @date: March 5th, 2023
# @filename: database_impl.py
# @purpose: The database function implementations. Functions for creating 
# databases, dropping databases, creating tables, dropping tables, etc. exist 
# here. These are the database functions that database.py connect with output 
# from database_parser.py.
import ast
import os
import configparser
import threading

# This is a decorator, a function that wraps another when used with the @ syntax
# This is a decorator that ensures that only one function from database_impl.py can be used at a time
# i.e. making these functions atomic and threadsafe

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

# create a database with a variable length of dbnames
@threadsafe
def create_database(*dbnames: str) -> bool:
    for dbname in dbnames:
        filepath = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + f"/{dbname}")
        try:
            with open(filepath, "x"):
                print(f"Database {dbname} created.")
        except FileExistsError:
            print(f"!Failed to create database {dbname} because it already exists.")

# drop a database with a variable length of dbnames
@threadsafe
def drop_database(*dbnames: str) -> bool:
    for dbname in dbnames:
        filepath = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + f"/{dbname}")
        try:
            os.remove(filepath)
            print(f"Database {dbname} deleted.")
        except FileNotFoundError:
            print(f"!Failed to delete database {dbname} because it does not exist.")


# create a table
@threadsafe
def create_table(dbname: str, tblname: str, **kwargs) -> bool:
    filepath = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + f"/{dbname}")
    db = configparser.SafeConfigParser()
    db.read(filepath)
    try:
        with open(filepath, "w") as new_db:
            if dict(db).get(tblname) == None:
                table_kwargs = {}
                table_kwargs.update({"__rows__":0})
                table_kwargs.update({"__attrs__":len(kwargs.keys())})
                table_kwargs.update(kwargs)

                db[tblname] = table_kwargs
                db.write(new_db)
                print(f"Table {tblname} created.")
            else:
                db.write(new_db)
                print(f"!Failed to create table {tblname} because it already exists.")
    except FileNotFoundError:
        print(f"!Failed to create table {tblname} because {dbname} does not exist.")
        return False

# drop a table
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

# select from table right now only supports * functionality
@threadsafe
def select_from_table(dbname: str, tblname: str, *attributes, row_cond="", cond=""):
    filepath = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + f"/{dbname}")
    db = configparser.SafeConfigParser()
    db.read(filepath)

    try:
        if attributes[0] == '*':
            table = []
            attrs = list(dict(db[tblname]).items())[2:2+int(db[tblname]["__attrs__"])]
            attrs_out = "|".join([" ".join(pair) for pair in attrs])
            print(attrs_out)
            tables = list(dict(db[tblname]).values())[2+int(db[tblname]["__attrs__"]):]
            for table in tables:
                print("|".join(list(ast.literal_eval(table).values())))
        else:
            attrs = []
            for selected in attributes:
                attrs += [selected + ' ' + dict(db[tblname]).get(selected)]
            attrs_out = "|".join(attrs)
            print(attrs_out)
            
            for i in range(int(db[tblname]["__rows__"])):
                entry = ast.literal_eval(db[tblname][str(i)])
                
                if (row_cond != "") and (cond != ""):
                    split = row_cond.split(cond)
                    left, right = entry.get(split[0]), split[1]

                    eval_cond = ""
                    if cond == "=":
                        eval_cond = "=="
                    else:
                        eval_cond = cond

                    eval_string = ""

                    if "char" in db[tblname].get(split[0]):
                        eval_string = "'"+ str(left) +"'" + eval_cond + "'"+str(right)+"'"
                    else:
                        eval_string = str(left) + eval_cond + str(right)

                    if (eval(eval_string)):
                        selected = []
                        for selected_attr in attributes:
                            selected += [entry.get(selected_attr)]
                        print("|".join(selected))
                else:
                    pass
            pass
            
    except Exception as e:
        if isinstance(e, KeyError):
            print(f"!Failed to query table {tblname} because it does not exist.")

@threadsafe
def insert_table_row(dbname: str, tblname: str, *values):
    filepath = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + f"/{dbname}")
    db = configparser.SafeConfigParser()
    db.read(filepath)
    try:
        if len(values) != int(db[tblname]["__attrs__"]):
            raise Exception("Giga Error!!! len(attrs) != len(values)")
        
        with open(filepath, "w") as new_db:
            new_table = {}
            attrs = list(dict(db[tblname]).keys())[2:]

            for i, value in enumerate(values):
                new_table.update({attrs[i]:value})

            db[tblname].update({db[tblname]["__rows__"]:str(new_table)})
            db[tblname]["__rows__"] = str(int(db[tblname]["__rows__"]) + 1)
            db.write(new_db)

    except Exception as e:
        if isinstance(e, FileNotFoundError):
            print(f"!Failed to create table {tblname} because {dbname} does not exist.")
        else:
            print(e)
        return False
    
@threadsafe
def delete_table_row(dbname: str, tblname: str, row_cond: str, cond: str):
    filepath = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + f"/{dbname}")
    db = configparser.SafeConfigParser()
    db.read(filepath)

    try:
        with open(filepath, "w") as new_db:
            records_deleted = 0
            records_to_delete = []
            
            for i in range(int(db[tblname]["__rows__"])):
                entry = ast.literal_eval(db[tblname][str(i)])
                
                split = row_cond.split(cond)
                left, right = entry.get(split[0]), split[1]

                eval_cond = ""
                if cond == "=":
                    eval_cond = "=="
                else:
                    eval_cond = cond

                eval_string = ""
                
                if "char" in db[tblname].get(split[0]):
                    eval_string = "'"+ str(left) +"'" + eval_cond + "'"+str(right)+"'"
                else:
                    eval_string = str(left) + eval_cond + str(right)
            
                if (eval(eval_string)):
                    records_to_delete += [i - records_deleted]
                    records_deleted += 1

            new_table = dict(db[tblname])

            for index in records_to_delete:
                reordered = {}
                for i in range(index, int(new_table.get("__rows__")) - 1):
                    reordered.update({str(i):new_table.get(str(i+1))})
                    new_table.pop(str(i))
                new_table.popitem()

                new_table.update({"__rows__": int(new_table.get("__rows__")) - 1})
                new_table.update(reordered)
            
            db[tblname] = new_table
            db.write(new_db)

            records_string = "record"
            if records_deleted > 1:
                records_string = "records"
            print(f"{records_deleted} {records_string} deleted.")
            
    except Exception as e:
        if isinstance(e, FileNotFoundError):
            print(f"!Failed to create table {tblname} because {dbname} does not exist.")
        else:
            print(e)
        return False
    
@threadsafe
def update_table(dbname: str, tblname: str, target_attr: str, target_val: str, row_cond: str, cond):
    filepath = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + f"/{dbname}")
    db = configparser.SafeConfigParser()
    db.read(filepath)
    
    try:
        with open(filepath, "w") as new_db:
            records_modified = 0
            for i in range(int(db[tblname]["__rows__"])):
                entry = ast.literal_eval(db[tblname][str(i)])
                
                split = row_cond.split(cond)
                left, right = entry.get(split[0]), split[1]

                eval_cond = ""
                if cond == "=":
                    eval_cond = "=="
                else:
                    eval_cond = cond

                eval_string = ""

                if "char" in db[tblname].get(split[0]):
                    eval_string = "'"+ str(left) +"'" + eval_cond + "'"+str(right)+"'"
                else:
                    eval_string = str(left) + eval_cond + str(right)

                if (eval(eval_string)):
                    entry.update({str(target_attr):str(target_val)})
                    records_modified += 1
                db[tblname][str(i)] = str(entry)
                
            db.write(new_db)

            records_string = "record"
            if records_modified > 1:
                records_string = "records"

            print(f"{records_modified} {records_string} modified.")

    except Exception as e:
        if isinstance(e, FileNotFoundError):
            print(f"!Failed to create table {tblname} because {dbname} does not exist.")
        else:
            print(e)
        return False

# alter a table through addition
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
                    db[tblname].update({"__attrs__":str(int(db[tblname].get("__attrs__"))+1)})
                    db.write(new_db)
                    print(f"Table {tblname} modified.")
                else:
                    print(f"Table {tblname} unable to be modified. Attribute already exists.")
                    db.write(new_db)
    except FileNotFoundError:
        print(f"!Failed to create table {tblname} because {dbname} does not exist.")
        return False

# alter a table through attribute deletion, to be implemented
@threadsafe
def alter_table_drop(dbname: str, tblname: str, **kwargs):
    pass