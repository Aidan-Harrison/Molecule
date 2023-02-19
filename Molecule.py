# Mini ASM
# Aid Harrison
# 2023

#import numpy as np
import queue
from enum import Enum
from typing import TypeVar

T = TypeVar('T') # Remove?

# Lexer
types = ["int", "flt", "str"]
# Molecule
functions = {} # function name | function line
    # Allows for function overriding
variables = {} # "Variable Name" | <GENERIC>
class STATEMENT_CMDS():
    PUT = 1
    WIPE = 2

class Program:
    def __init__(self, direct : str = "", debugActive : bool = False) -> None:
        self.directory : str = ""
        self.source = []
        self.start_index : int = 0
        self.enumDef : STATEMENT_CMDS() = STATEMENT_CMDS()
        self.commands = {} # Line Index | STATEMENT type 
        self.DEBUG = True
        self.build(direct, debugActive)
        self.typePositions = []

        # New
        self.variable_types = {} # POSITION | Type as str

        if not self.lexer():
            print("FAILED TO COMPILE!")
    def build(self, directory : str, debugActive : bool) -> None:
        if not debugActive:
            self.DEBUG = False
        self.directory = directory
        # Write source and appropiate data
        with open(directory) as f:
            self.source = f.readlines()

    def type_check(self, line : str, index : int) -> int:
        # Get match working!
        if line[index] == 'i':
            return 0
        elif line[index] == 'f':
            return 1
        elif line[index] == 's':
            return 2

    def type_get(self) -> int:
        ...

    def function_call(self, index : int) -> bool:
        print(self.source[index])

    def variable_compile(self) -> bool:
        if self.source[0].find("_VAR") == -1:
            return False
        for line in range(1, len(self.source)):
            f_index : int = -1
            self.source[line].strip() # Clear whitespace
            if self.source[line] == "}": # End of _VAR scope
                break
            for i in types: # Search for datatype | int, flt, str, etc.
                f_index = self.source[line].find(i) # Cheaper to do instead of two function calls
                if f_index != -1: # if valid type found, store position for check
                    #self.typePositions.append(f_index) 
                    self.variable_types[f_index] = i
            if self.source[line].find(":") == -1:
                print("Invalid syntax, used datatype without variable specifier") # Convert to format print
                return False
            # Get variable name and value
            current_var_name : str = ""
            current_value : str = ""

            print("INDEX test: ", self.source[3][4])

            for i in range(f_index, 0, -1):
                if not self.source[line][i].isdigit() and self.source[line][i] != ' ':
                    print(self.source[line][i])
                    current_var_name += self.source[line][i]
            for i in range(f_index+5, len(self.source[line])):
                current_value += self.source[line][i]
            print("VARIABLE NAME: ", current_var_name)
            print("VALUE: ", current_value)
            for i in self.variable_types.values():
                # Get match statement working!
                if i == "int":
                    variables[current_var_name[::-1]] = int(current_value)
                elif i == "flt":
                    variables[current_var_name[::-1]] = float(current_value)
                else:
                    variables[current_var_name[::-1]] = current_value
            # ===========
            #for vPos in self.typePositions:
                #var_type : int = self.type_check(line, f_index) # Store type for later assignment
                #print("type: ", var_type)
                #f_index = line.find(':') # Variable identifier
                #if f_index != -1:
                #    print("Line: ", line)
                #    curVar : str = ""
                #    for i in range(f_index-1, 0, -1):
                #        if not line[i].isdigit() and line[i] != ' ':
                #            curVar += line[i]
                #    if curVar == "":
                #        continue
                #    # Variable is valid, get value
                #    value : str = ""
                #    for i in range(f_index+5, len(line)-1): # Minimum offset of 5
                #        if line[i].isdigit():
                #            value += line[i]
                #    if var_type == 0:
                #        variables[curVar] = int(value)
                #    elif var_type == 1:
                #        variables[curVar] = float(value) 
                #    elif var_type == 2:
                #        variables[curVar] = value
                #    print("V: ", curVar)
        return True

    def lexer(self) -> bool:
        for i in range(0, len(self.source)):
            self.start_index = self.source[i].find("_START")
            if self.start_index != -1:
                break
        if self.start_index == -1:
            print("'_START' not found, please add")
            return False
        if not self.variable_compile():
            print("No variable storage found")
        else:
            print("Variable storage found")
        print(variables)
        lineCount : int = 0
        for line in self.source:
            f_index : int = -1
            line.strip() # Clear starting and ending whitespace
            self.source[lineCount] = line # Rewrite to source
            # === Commands ===
            index = line.find("put") # Interpreted print statement
            if not index == -1:
                output : str = ""
                # Check if string, if not, check against base values, then variables
                for i in range(index+3, len(line)):
                    if line[i] == '"' and line[len(line)-2] == '"':
                        for j in range(i+1, len(line)-2):
                            output += line[j]
                print(output)
                self.commands[lineCount] = self.enumDef.PUT 
            index = line.find("wipe")
            if not index == -1:
                for i in variables.keys():
                    if line.find(i):
                        variables[i] = None
                self.commands[lineCount] = self.enumDef.WIPE
            index = line.find("for")
            if not index == -1:
                # Obtain container OR range
                counterVal : str = ""
                t_variable : str = "" # Used for variable storage, optimise
                    # Only create when needed
                for i in range(index+4, len(line)):
                    if line[i].isdigit(): # Easier to seperate to two counters
                        counterVal += line[i]
                    else: # Variable check
                        t_variable += line[i]
                        for var in variables.keys(): # Optimise, add flag instead of per loop iter!!!!
                            if t_variable == var:
                                counterVal = variables[t_variable]
                loop_range : int = int(counterVal)
                # Store each process in looop | DO
                for i in range(0, loop_range):
                    ...
            # === OPERATORS ===
            index = line.find("++")
            if not index == -1:
                # Get variable
                variable : str = ""
                for i in range(index, 0, -1):
                    if line[i].isalnum():
                        variable += line[i]
                variables[variable[::-1]] += 1
            index = line.find("+")
            if not index == -1:
                # Get variables
                var_1 : str = ""
                var_2 : str = ""
                for i in range(index, 0, -1): # Left
                    if line[i].isalnum():
                        var_1 += line[i]
                var_1[::-1]
                for j in range(index, len(line)):
                    if line[j].isalnum():
                        var_2 += line[j]
                result = variables[var_1] + variables[var_2]
                for cmd in self.commands.keys():
                    if lineCount == cmd:
                        print(result)
            # === Functions ===
            if line.find("_FN") != -1:
                fn_name : str = "" # Make global
                for i in range(3, len(line)):
                    if line[i] == '(':
                        break
                    fn_name += line[i]
                functions[fn_name] = lineCount # Change, get lines in a global manner
            # === FN Execute ===
            if line.find("(") != -1 and line.find(")") != -1:
                if line.find("_FN") == -1:
                    # Get name, call appropiate function
                    fn_name : str = ""
                    for i in range(0, len(line)):
                        if line[i] == '(':
                            break
                        fn_name += line[i]
                    #self.function_call(functions[fn_name]) # Run function
            lineCount += 1
            
        # === DEBUG ===
        print(variables)
        print(functions)
        return True

    def execute(self) -> bool:
        # Iterates over stored assets and computes
        execute_queue : queue = queue.Queue(20) # Max func size of 20
        for func in functions.values():
            #execute_queue.append(func)
            self.function_call(func)

def main() -> None:
    newProgram : Program = Program("HelloWorld.txt", True)

if __name__ == "__main__":
    main()