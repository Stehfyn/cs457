import database_impl as dbi
import database_parser as dbp
import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
from dearpygui_ext import logger
import itertools
import os
import sys
import io
from contextlib import redirect_stdout
import threading

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

class DatabaseManager(metaclass=SingletonConstruction):
    def __init__(self):
        self.db_in_use = ""
        self.db_list = []

    def create_db(self, dbname):
        if dbname not in self.db_list:
            # check if file exists
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

class DatabaseGUI:
    def __init__(self):
        self.input = ""
        self.output = ""
        self.setup_dpg()
        self.setup_window()
        with dpg.font_registry():
        # first argument ids the path to the .ttf or .otf file
            default_font = dpg.add_font("MyriadPro-Light.ttf", 20)
        dpg.bind_font(default_font)
        demo.show_demo()
        self.logger = logger.mvLogger()
        pass

    def run(self):
        dpg.set_primary_window("Primary Window", True)

        while dpg.is_dearpygui_running():
            jobs = dpg.get_callback_queue() # retrieves and clears queue
            dpg.run_callbacks(jobs)

            dpg.render_dearpygui_frame()

    def __enter__(self):
        return self
    
    def __exit__(self, et, ev, etb):
        return True
    
    def setup_dpg(self):
        dpg.create_context()
        dpg.create_viewport(title='Database', width=1000, height=800)
        self.set_icon()
        dpg.setup_dearpygui()
        dpg.show_viewport()

    def setup_window(self):
        dpg.push_container_stack(dpg.add_window(tag="Primary Window"))
        with dpg.group(horizontal=True):
            dpg.add_input_text(tag="input", default_value="", callback=self.__input_callback)
            dpg.add_button(label="parse", callback=self.__parse_callback)
        dpg.add_text(tag="output",default_value="", wrap=-1, color=(255,0,0,255))
        #self.setup_input_menu()
        #self.setup_plot_view()

        dpg.pop_container_stack()
        
        #self.setup_file_dialog()
    
    def set_icon(self):
        dpg.set_viewport_small_icon("unr-256x256.ico")
        dpg.set_viewport_large_icon("unr-256x256.ico")
    
    def __input_callback(self, sender, user_data):
        self.input = user_data

    def __parse_callback(self, sender, user_data):
        with io.StringIO() as buf, redirect_stdout(buf):
            function_id, args = parse_command(self.input)
            execute_function(function_id, args)
            self.output += buf.getvalue()
            self.logger.log_info(buf.getvalue())
        dpg.configure_item("output", default_value=self.output)
        self.input = ""
        dpg.configure_item("input", default_value=self.input)
    
def interpreter():
    db = DatabaseManager()
    try:
        while True:
            x = input("# ")
            function_id, args = parse_command(x)
            execute_function(function_id, args)

    except KeyboardInterrupt:
        print("exiting interpreter")

def gui():
    dbgui = DatabaseGUI()
    with dbgui:
        dbgui.run()

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
    except:
        pass

def parse_command(*args):
    return dbp.parse(*args)

def execute_function(id: dbp.DatabaseFunction, args):
    if id != dbp.DatabaseFunction.COMMENT:
        func = __get_database_function(id)
        ret = func(**args)

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