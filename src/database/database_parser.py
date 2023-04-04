# @auth: Stephen Foster
# @date: March 5th, 2023
# @filename: database_parser.py
# @purpose: The database parser that either accepts or rejects raw input as
# valid database operation language. This parser both tokenizes arguments as 
# well as ensures valid table syntax, then returns the output to database.py 
# to connect to the proper database functionality in database_impl.py.

# also sorry in advance this really the result of not paying enough attention (any)
# in automata and language implementation

import argparse
from enum import Enum
from functools import partial

class DatabaseFunction(Enum):
    COMMENT = -1
    EXIT = 0
    DATABASE_USE = 1
    DATABASE_CREATE = 2
    DATABASE_DROP = 3
    TABLE_CREATE = 4
    TABLE_DROP = 5
    TABLE_SELECT = 6
    TABLE_SELECT_ATTRIBUTE = 7
    TABLE_INSERT_ROW = 8
    TABLE_UPDATE_ROW = 9
    TABLE_FROM = 10
    TABLE_SET_ATTRIBUTE = 11
    TABLE_WHERE_ATTRIBUTE = 12
    TABLE_DELETE_ROW = 13
    TABLE_ALTER_ADD = 14
    TABLE_ALTER_DROP = 15

class __DatabaseParser(Enum):
    COMMENT_PARSER = -1
    EXIT_PARSER = 0
    USE_PARSER = 1
    CREATE_DATABASE_PARSER = 2
    DROP_DATABASE_PARSER = 3
    CREATE_TABLE_PARSER = 4
    DROP_TABLE_PARSER = 5
    SELECT_PARSER = 6
    SELECT_ATTRIBUTE_PARSER = 7
    INSERT_TABLE_ROW_PARSER = 8
    UPDATE_TABLE_ROW_PARSER = 9
    FROM_TABLE_PARSER = 10
    SET_ATTRIBUTE_PARSER = 11
    WHERE_ATTRIBUTE_PARSER = 12
    DELETE_ROW_PARSER = 13
    ALTER_ADD_PARSER = 14
    ALTER_DROP_PARSER = 15

# The argparse extension to further parse Table argument types
class TableParser(argparse.Action):
    def __init__(self, option_strings, *args, **kwargs):
        super(TableParser, self).__init__(option_strings=option_strings, *args, **kwargs)

    def __call__(self, parser, args, values, option_string=None):
        values = self.__sanitize_table(values)
        setattr(args, self.dest, values)

    def __sanitize_table(self, values):
        values = self.__strip_elements(values)
        values = self.__strip_non_identifying(values)
        return values
    
    def __strip_keyword(self, values):
        if len(values) != 0 and values[0].startswith("values"):
            values[0] = values[0][len("values"):]
        return values
    
    def __strip_elements(self, values):
        unwanted = ['(', ')', '|', ',']
        for char in unwanted:
            while char in values:
                values.remove(char)
        return values
    
    def __strip_non_identifying(self, values):
        unwanted_regardless = [',', '|', '\t']
        semantically_dependent = [('(', ')')]

        for i, value in enumerate(values):
            for char in unwanted_regardless:
                if char in value:
                    values[i] = value.replace(char, '')
        
        for i , value in enumerate(values):
            #need to do semantic analysis to rid unnecessary '()'
            for left, right in semantically_dependent:
                while value.startswith(left):
                    values[i], value = value[1:], value[1:]
                
                if (value.count(left) + value.count(right)) % 2 != 0:
                    even = left if (value.count(left) % 2 == 0) and (value.count(left) != 0)  else right
                    #only real hardcoded bit, can make this infinitely better but works for now
                    values[i] = value[1:] if (left == even) else value[:-1]
        
        values_as_dict = {}
        keys = []
        vals = []

        #alternating values are analogous to attribute, constraint, attribute, ...
        for i in range(0, len(values), 2):
            keys.append(values[i])
            vals.append(values[i+1])

        #zip up attribute as key, constraint as value
        for i in range(len(keys)):
            values_as_dict.update({keys[i]:vals[i]})

        return values_as_dict
    
class ValueParser(argparse.Action):
    def __init__(self, option_strings, *args, **kwargs):
        super(ValueParser, self).__init__(option_strings=option_strings, *args, **kwargs)

    def __call__(self, parser, args, values, option_string=None):
        values = self.__sanitize_table(values)
        setattr(args, self.dest, values)

    def __sanitize_table(self, values):
        values = self.__strip_keyword(values)
        values = self.__strip_elements(values)
        values = self.__strip_non_identifying(values)
        return values
    
    def __strip_keyword(self, values):
        if len(values) != 0 and values[0].startswith("values"):
            values[0] = values[0][len("values"):]
        return values
    
    def __strip_elements(self, values):
        unwanted = ['(', ')', '|', ',']
        for char in unwanted:
            while char in values:
                values.remove(char)
        return values
    
    def __strip_non_identifying(self, values):
        unwanted_regardless = [',', '|', '\t']
        semantically_dependent = [('(', ')')]

        for i, value in enumerate(values):
            for char in unwanted_regardless:
                if char in value:
                    values[i] = value.replace(char, '')

        for i , value in enumerate(values):
            #need to do semantic analysis to rid unnecessary '()'
            for left, right in semantically_dependent:
                while value.startswith(left):
                    values[i], value = value[1:], value[1:]
                
                if (value.count(left) + value.count(right)) % 2 != 0:
                    even = left if (value.count(left) % 2 == 0) and (value.count(left) != 0)  else right
                    #only real hardcoded bit, can make this infinitely better but works for now
                    values[i] = value[1:] if (left == even) else value[:-1]
        
        # in future use stack to keep track if we're in string
        # ok cool now time to repeat above for splitting elements on commas
        for i, value in enumerate(values):
            split_vals = value.split(',')
            while '' in split_vals:
                split_vals.remove('')
            
            # probably something giga more pythonic but my head hurts and this took 30 seconds
            if len(split_vals) > 1:
                values.pop(i)
                for j in range(len(split_vals)):
                    values.insert(j + i, split_vals[j])

        for i, value in enumerate(values):
            values[i] = values[i].replace("'", "")

        return values
    
class AttributeParser(argparse.Action):
    def __init__(self, option_strings, *args, **kwargs):
        super(AttributeParser, self).__init__(option_strings=option_strings, *args, **kwargs)

    def __call__(self, parser, args, values, option_string=None):
        values = self.__sanitize_table(values)
        setattr(args, self.dest, values)

    def __sanitize_table(self, values):
        values = self.__strip_keyword(values)
        values = self.__strip_elements(values)
        values = self.__strip_non_identifying(values)
        return values
    
    def __strip_keyword(self, values):
        if len(values) != 0 and values[0].startswith("values"):
            values[0] = values[0][len("values"):]
        return values
    
    def __strip_elements(self, values):
        unwanted = ['(', ')', '|', ',']
        for char in unwanted:
            while char in values:
                values.remove(char)
        return values
    
    def __strip_non_identifying(self, values):
        unwanted_regardless = [',', '|', '\t']
        semantically_dependent = [('(', ')')]

        for i, value in enumerate(values):
            for char in unwanted_regardless:
                if char in value:
                    values[i] = value.replace(char, '')

        for i , value in enumerate(values):
            #need to do semantic analysis to rid unnecessary '()'
            for left, right in semantically_dependent:
                while value.startswith(left):
                    values[i], value = value[1:], value[1:]
                
                if (value.count(left) + value.count(right)) % 2 != 0:
                    even = left if (value.count(left) % 2 == 0) and (value.count(left) != 0)  else right
                    #only real hardcoded bit, can make this infinitely better but works for now
                    values[i] = value[1:] if (left == even) else value[:-1]
        
        # in future use stack to keep track if we're in string
        # ok cool now time to repeat above for splitting elements on commas
        for i, value in enumerate(values):
            split_vals = value.split('=')
            while '' in split_vals:
                split_vals.remove('')
            
            # probably something giga more pythonic but my head hurts and this took 30 seconds
            if len(split_vals) >= 1:
                values.pop(i)
                for j in range(len(split_vals)):
                    values.insert(j + i, split_vals[j])

        for i, value in enumerate(values):
            values[i] = values[i].replace("\"", "")

        for i, value in enumerate(values):
            values[i] = values[i].replace("'", "")
        
        eval_operation = [">", "<", "==", ">=", "<=", "!="]
        operations = ["gt", "lt", "=", "gte", "lte", "dne"]
        operation = ""
        for i, op in enumerate(operations):
            if op in values:
                while op in values:
                    values.remove(op)
                #take the last, should be generalized
                operation = eval_operation[i]

        values_as_dict = {}
        keys = []
        vals = []

        #alternating values are analogous to attribute, constraint, attribute, ...
        for i in range(0, len(values), 2):
            keys.append(values[i])
            vals.append(values[i+1])

        #zip up attribute as key, constraint as value
        for i in range(len(keys)):
            values_as_dict.update({keys[i]:vals[i]})

        values_as_dict.update({"__condition__":operation})
        return values_as_dict

# The decorator to loop through some list of parsers and see which one fits
# Each parser is aligned with some database function, and that's how we know what function to execute,
# when it passes some parser in __parser_list

def __psuedo_try_next_parser_on_fail(fn, __parser_list):
    def new(*args, **kwargs):
        parsers = __parser_list
        n, parsed_args = 0, argparse.Namespace()
        while (n < len(parsers)):
            try:
                parsed_args = fn(*args, parser=parsers[n])
                break
            #TODO: disambiguate argument errors
            except Exception as e:
                #print(e, type(e))
                n += 1

        if n >= 0:
            return DatabaseFunction(n), vars(parsed_args)
        else:
            return __DatabaseParser(n), vars(parsed_args)
    return new

# The following is the individual parsers defining the tokenization of each database function invocation
# These parser definitions are straightforward.
def __exit_parser():
    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_mutually_exclusive_group()
    parser.add_argument("operation", choices=[".exit"], type=str.lower)
    return parser

def __use_parser():
    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_mutually_exclusive_group()
    parser.add_argument("operation", choices=["use"], type=str.lower)
    parser.add_argument("target", nargs=1)
    return parser

def __create_database_parser():
    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_mutually_exclusive_group()
    parser.add_argument("operation", choices=["create"], type=str.lower)
    parser.add_argument("type", choices=["database"], type=str.lower)
    parser.add_argument("targets", nargs=argparse.ONE_OR_MORE) #custom char action to lint for chars not allowed to make a file with
    return parser

def __drop_database_parser():
    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_mutually_exclusive_group()
    parser.add_argument("operation", choices=["drop"], type=str.lower)
    parser.add_argument("type", choices=["database"], type=str.lower)
    parser.add_argument("targets", nargs=argparse.ONE_OR_MORE)
    return parser

def __create_table_parser():
    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_mutually_exclusive_group()
    parser.add_argument("operation", choices=["create"], type=str.lower)
    parser.add_argument("type", choices=["table"], type=str.lower)
    parser.add_argument("targets", nargs=1)
    parser.add_argument("table", nargs="*", action=TableParser)
    return parser

def __drop_table_parser():
    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_mutually_exclusive_group()
    parser.add_argument("operation", choices=["drop"], type=str.lower)
    parser.add_argument("type", choices=["table"], type=str.lower)
    parser.add_argument("targets", nargs=argparse.ONE_OR_MORE)
    return parser

def __select_parser():
    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_mutually_exclusive_group()
    parser.add_argument("operation", choices=["select"], type=str.lower)
    parser.add_argument("value", nargs=argparse.ONE_OR_MORE)
    parser.add_argument("from", choices=["from"], type=str.lower)
    parser.add_argument("targets", nargs=1)
    return parser

def __select_attribute_parser():
    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_mutually_exclusive_group()
    parser.add_argument("operation", choices=["select"], type=str.lower)
    parser.add_argument("value", nargs=argparse.ONE_OR_MORE, action=ValueParser)
    return parser

def __insert_parser():
    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_mutually_exclusive_group()
    parser.add_argument("operation", choices=["insert"], type=str.lower)
    parser.add_argument("operation(ext)", choices=["into"], type=str.lower)
    parser.add_argument("targets", nargs=1)
    parser.add_argument("values", nargs=argparse.ONE_OR_MORE, action=ValueParser)
    return parser

def __update_parser():
    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_mutually_exclusive_group()
    parser.add_argument("operation", choices=["update"], type=str.lower)
    parser.add_argument("targets", nargs=1)
    return parser

def __from_parser():
    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_mutually_exclusive_group()
    parser.add_argument("operation", choices=["from"], type=str.lower)
    parser.add_argument("targets", nargs=1)
    return parser

def __set_attribute_parser():
    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_mutually_exclusive_group()
    parser.add_argument("operation", choices=["set"], type=str.lower)
    parser.add_argument("targets", nargs=argparse.ONE_OR_MORE, action=AttributeParser)
    return parser

def __where_attribute_parser():
    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_mutually_exclusive_group()
    parser.add_argument("operation", choices=["where"], type=str.lower)
    parser.add_argument("targets", nargs=argparse.ONE_OR_MORE, action=AttributeParser)
    return parser

def __delete_row_parser():
    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_mutually_exclusive_group()
    parser.add_argument("operation", choices=["delete"], type=str.lower)
    parser.add_argument("from", choices=["from"], type=str.lower)
    parser.add_argument("targets", nargs=1)
    return parser

def __alter_add_parser():
    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_mutually_exclusive_group()
    parser.add_argument("operation", choices=["alter"], type=str.lower)
    parser.add_argument("type", choices=["table"], type=str.lower)
    parser.add_argument("targets", nargs=1)
    parser.add_argument("alter operation", choices=["add"], type=str.lower)
    parser.add_argument("table", nargs=argparse.ONE_OR_MORE, action=TableParser)
    return parser

def __alter_drop_parser():
    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_mutually_exclusive_group()
    parser.add_argument("operation", choices=["alter"], type=str.lower)
    parser.add_argument("type", choices=["table"], type=str.lower)
    parser.add_argument("targets", nargs=1)
    parser.add_argument("alter operation", choices=["drop"], type=str.lower)
    parser.add_argument("attributes", nargs=argparse.ONE_OR_MORE)
    return parser

# The parser map that pairs a parser enum to the proper database parser
def __get_parser_map():
    parser_map = {}
    parser_map.update({__DatabaseParser.EXIT_PARSER:__exit_parser()})
    parser_map.update({__DatabaseParser.USE_PARSER:__use_parser()})
    parser_map.update({__DatabaseParser.CREATE_DATABASE_PARSER:__create_database_parser()})
    parser_map.update({__DatabaseParser.DROP_DATABASE_PARSER:__drop_database_parser()})
    parser_map.update({__DatabaseParser.CREATE_TABLE_PARSER:__create_table_parser()})
    parser_map.update({__DatabaseParser.DROP_TABLE_PARSER:__drop_table_parser()})
    parser_map.update({__DatabaseParser.SELECT_PARSER:__select_parser()})
    parser_map.update({__DatabaseParser.SELECT_ATTRIBUTE_PARSER:__select_attribute_parser()})
    parser_map.update({__DatabaseParser.INSERT_TABLE_ROW_PARSER:__insert_parser()})
    parser_map.update({__DatabaseParser.UPDATE_TABLE_ROW_PARSER:__update_parser()})
    parser_map.update({__DatabaseParser.FROM_TABLE_PARSER:__from_parser()})
    parser_map.update({__DatabaseParser.SET_ATTRIBUTE_PARSER:__set_attribute_parser()})
    parser_map.update({__DatabaseParser.WHERE_ATTRIBUTE_PARSER:__where_attribute_parser()})
    parser_map.update({__DatabaseParser.DELETE_ROW_PARSER:__delete_row_parser()})
    parser_map.update({__DatabaseParser.ALTER_ADD_PARSER:__alter_add_parser()})
    parser_map.update({__DatabaseParser.ALTER_DROP_PARSER:__alter_drop_parser()})
    return parser_map


# Where __get_parser_map is used, to initialize the __DatabaseFunctionParser decorator 
# as __psuedo_try_next_parser_on_fail with __get_parser_map().values() as the __parser_list

__DatabaseFunctionParser = partial(__psuedo_try_next_parser_on_fail, __parser_list=list(__get_parser_map().values()))
# Initial input sanitization. It ignores inline comments, and does not enforce, but will still allow properly, ; terminated
# commands.

def __input_sanitizer(*args):

    # Not so fun args correction, join args to singular string, strip leading/trailing whitespace chars, split based off internal
    # spaces, and only include the arg if it isn't an empty char
    args = [x for x in "".join(args).strip().split(" ") if x != '']
    
    # Don't enforce instruction termination, but if it is, then remove terminator before parsing
    if len(args) > 0:
        #First, look for comment
        for i, arg in enumerate(args):
            if arg.startswith("--") and i != 0:
                args = args[:i]
        while ';' in args:
            args.remove(';')
        for i, arg in enumerate(args):
            if ';' in arg:
                args[i] = arg.replace(';','')
        while '' in args:
            args.remove('')
        for i, arg in enumerate(args):
            if '>' in arg or '<' in arg or '!=' in arg:
                # argparse is cringe for treating the angle brackets special
                args[i] = args[i].replace('<', "lt")
                args[i] = args[i].replace('>', "gt")
                args[i] = args[i].replace('<=', "lte")
                args[i] = args[i].replace('>=', "gte")
                args[i] = args[i].replace('!=', "dne")

    return args

# Internal parser definition, where __DatabaseFunctionParser loops through all available parsers and returns the proper
# Database function

@__DatabaseFunctionParser
def __parser(*args, **parser):
    return parser["parser"].parse_args(*args)

# External database parse function, detects lines that begin with a comment,
# and otherwise will execute the parse process and find the relevant database function
# to return to database.py

def parse(*args):
    args = __input_sanitizer(*args)

    if not args[0].startswith("--"):
        database_function, parsed = __parser(args)
        return database_function, parsed
    
    else:
        return DatabaseFunction.COMMENT, args