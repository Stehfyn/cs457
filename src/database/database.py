# @auth: Stephen Foster
# @date: March 5th, 2023
# @filename: database.py
# @purpose: The database program manager. This file contains the DatabaseManager
# class and related functionality to keep track of which database is in use, as 
# well as the implementations of the batch processor, interpreter, and graphical 
# user interface. Additionally, this file implements the wrapper functions that 
# “connect” the output of the database parser to the appropriate database function.

import os
import io
import logging
from contextlib import redirect_stdout
import threading

import database.database_impl as dbi
import database.database_parser as dbp
import dearpygui.dearpygui as dpg

from database.embed import EmbeddedResource

"""Ensure object __calls__ are threadsafe to always return the same class instance"""
_cls_lock = threading.Lock()
class SingletonConstruction(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            global _cls_lock
            with _cls_lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super(SingletonConstruction, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

# make DatabaseManager a singleton, the class that manages database state (use and .exit at the moment)
class DatabaseManager(metaclass=SingletonConstruction):
    def __init__(self):
        self.db_in_use = ""
        self.db_list = []

    def create_db(self, dbname):
        if dbname not in self.db_list:
            self.db_list.append(dbname)
        else:
            raise Exception(dbname)

    def drop_db(self, dbname):
        if dbname in self.db_list:
            self.db_list.remove(dbname)

    def use_db(self, dbname):
        if dbname in self.db_list:
            self.db_in_use = dbname
            print(f"Using database {self.db_in_use}.")
        else:
            print(f"Unable to use database {dbname}. Database does not exist.")

    def get_db_in_use(self):
        return self.db_in_use
    
    def exit(self, *args, **kwargs):
        print("All done.")
        os._exit(0)

# the class that implements the database GUI, it redirects stdout and prints to the window
class DatabaseGUI:
    def __init__(self):
        self.input = ""
        self.output = ""
        self.setup_dpg()
        self.setup_window()

    # app loop
    def run(self):
        dpg.set_primary_window("Primary Window", True)
        while dpg.is_dearpygui_running():
            jobs = dpg.get_callback_queue() # retrieves and clears queue
            dpg.run_callbacks(jobs)

            if dpg.is_key_pressed(dpg.mvKey_Return):
                self.__parse_callback("", "")
            

            dpg.render_dearpygui_frame()

    def __enter__(self):
        return self
    
    def __exit__(self, et, ev, etb):
        return True
    
    def setup_dpg(self):
        dpg.create_context()
        dpg.create_viewport(title='Database', width=600, height=200)
        self.set_icon()
        self.set_font()
        dpg.setup_dearpygui()
        dpg.show_viewport()

    # widget declarations
    def setup_window(self):
        dpg.push_container_stack(dpg.add_window(tag="Primary Window"))
        with dpg.group(horizontal=True):
            dpg.add_input_text(tag="input", default_value="", callback=self.__input_callback)
            dpg.add_button(label="parse", callback=self.__parse_callback)
            dpg.add_button(label="clear", callback=self.__clear_callback)
        dpg.add_text(tag="output",default_value="", wrap=-1, color=(255,0,0,255))
        #dpg.add_slider_float(label="width",min_value=10, max_value=100, default_value=50, callback=lambda s, ud: dpg.configure_item("child1", width=ud))
        #dpg.add_child_window(label="child", tag="child1")

        dpg.pop_container_stack()
        
    
    def set_font(self):
        #font = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + f"/MyriadPro-Light.ttf")
        with EmbeddedResource("MyriadPro-Light.ttf", delete_on_exit=False) as font:
            with dpg.font_registry():
                default_font = dpg.add_font(font, 20)
            dpg.bind_font(default_font)

    def set_icon(self):
        #icon = os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + f"/unr-256x256.ico")
        with EmbeddedResource("UniversityLogo RGB_block_n_blue.ico", delete_on_exit=False) as icon:
        #with EmbeddedResource("UNR-active.ico", delete_on_exit=False) as icon:
            dpg.set_viewport_small_icon(icon)
            dpg.set_viewport_large_icon(icon)
    
    def __input_callback(self, sender, user_data):
        self.input = user_data

    # parse button, redirect stdout to capture output
    def __parse_callback(self, sender, user_data):
        try:
            with io.StringIO() as buf, redirect_stdout(buf):
                function_id, args = parse_command(self.input)
                execute_function(function_id, args)
                self.output += buf.getvalue()
        except:
            logging.exception("Parsing or Execution Error!")

        dpg.configure_item("output", default_value=self.output)
        self.input = ""
        dpg.configure_item("input", default_value=self.input)
    
    # clear button, clear output string and reset text in window
    def __clear_callback(self, sender, user_data):
        self.output = ""
        dpg.configure_item("output", default_value=self.output)

# The database interpreter, just a while True: parse commands and execute functions
def interpreter():
    db = DatabaseManager()
    try:
        while True:
            x = input("# ")
            function_id, args = parse_command(x)
            execute_function(function_id, args)

    except KeyboardInterrupt:
        print("exiting interpreter")

# The database gui, invokes the DatabaseGUI class instance
def gui():
    dbgui = DatabaseGUI()
    with dbgui:
        dbgui.run()

# The database function batch processor, goes through each line of a file, parses it, then executes the relevant function
def batch_processor(argv):
    db = DatabaseManager()
    try:
        for filepath in argv:
            with open(filepath, "r") as file:
                for line in file.readlines():
                    line = line.rstrip()
                    if line != '':
                        function_id, args = parse_command(line)
                        execute_function(function_id, args)
                        
    except Exception as e:
        print(e)
        pass

# The function that does argument passthrough to the database_parser
def parse_command(*args):
    return dbp.parse(*args)

# The high level function that grabs the proper database function to execute based off the parser return values
def execute_function(id: dbp.DatabaseFunction, args):
    if id != dbp.DatabaseFunction.COMMENT:
        func = __get_database_function(id)
        ret = func(**args)

# The database function map that links a function enumerator to a function callable
def __get_database_function(id: dbp.DatabaseFunction):
    database_function_map = {dbp.DatabaseFunction.EXIT:DatabaseManager().exit,
                             dbp.DatabaseFunction.DATABASE_USE:DatabaseManager().use_db,
                             dbp.DatabaseFunction.DATABASE_CREATE:dbi.create_database,
                             dbp.DatabaseFunction.DATABASE_DROP:dbi.drop_database,
                             dbp.DatabaseFunction.TABLE_CREATE:dbi.create_table,
                             dbp.DatabaseFunction.TABLE_DROP:dbi.drop_table,
                             dbp.DatabaseFunction.TABLE_SELECT:dbi.select_from_table,
                             dbp.DatabaseFunction.TABLE_ALTER_ADD:dbi.alter_table_add,
                             dbp.DatabaseFunction.TABLE_ALTER_DROP:dbi.alter_table_drop}
    
    raw_func = database_function_map.get(id)
    wrapper = __get_database_function_wrapper(raw_func)
    return wrapper(raw_func)

# The wrapper map that gets the proper function wrapper based off the database function
# Wrappers are necessary to ensure the database functions are passed only the necessary information
# as arguments
def __get_database_function_wrapper(raw_func):
    database_function_wrapper_map = {DatabaseManager().exit:__exit_wrapper,
                                     DatabaseManager().use_db:__use_wrapper,
                                     dbi.create_database:__create_database_wrapper,
                                     dbi.drop_database:__drop_database_wrapper,
                                     dbi.create_table:__create_table_wrapper,
                                     dbi.drop_table:__drop_table_wrapper,
                                     dbi.select_from_table:__select_from_table_wrapper,
                                     dbi.alter_table_add:__alter_table_add_wrapper}
    
    return database_function_wrapper_map.get(raw_func)

# All of the database function wrappers. Each one of these strips **kwargs 
# and only passes the relevant information to the actual database function

def __exit_wrapper(fn):
    def new(*args, **kwargs):
        try:
            f = fn(*args, **kwargs)
        except Exception as e:
            print(e)
    return new

def __use_wrapper(fn):
    def new(**kwargs):
        try:
            f = fn(kwargs.get("target")[0])
        except Exception as e:
            print(e)
    return new

def __create_database_wrapper(fn):
    def new(**kwargs):
        try:
            targets = kwargs.get("targets")
            for target in targets:
                DatabaseManager().create_db(target)

            f = fn(*targets)

        except Exception as e:
            print(f"!Failed to create database {str(e)} because it already exists.")
    return new

def __drop_database_wrapper(fn):
    def new(**kwargs):
        try:
            targets = kwargs.get("targets")
            for target in targets:
                DatabaseManager().drop_db(target)
            f = fn(*targets)
        except Exception as e:
            print(e)
    return new

def __create_table_wrapper(fn):
    def new(**kwargs):
        try:
            tblname = kwargs.get("targets")[0]
            table = kwargs.get("table")
            f = fn(DatabaseManager().get_db_in_use(), tblname, **table)
        except Exception as e:
            print(e)
    return new

def __drop_table_wrapper(fn):
    def new(**kwargs):
        try:
            tblnames = kwargs.get("targets")
            f = fn(DatabaseManager().get_db_in_use(), *tblnames)
        except Exception as e:
            print(e)
    return new

def __select_from_table_wrapper(fn):
    def new(**kwargs):
        try:
            tblname = kwargs.get("targets")[0]
            attributes = kwargs.get("value")
            f = fn(DatabaseManager().get_db_in_use(), tblname, *attributes)
        except Exception as e:
            print(e)
    return new

def __alter_table_add_wrapper(fn):
    def new(**kwargs):
        try:
            tblname = kwargs.get("targets")[0]
            table = kwargs.get("table")
            f = fn(DatabaseManager().get_db_in_use(), tblname, **table)
        except Exception as e:
            print(e)
    return new

def __alter_table_drop_wrapper(fn):
    def new(**kwargs):
        try:
            tblname = kwargs.get("targets")[0]
            attributes = kwargs.get("value")
            f = fn(DatabaseManager().get_db_in_use(), tblname, *attributes)
        except Exception as e:
            print(e)
    return new