# Mini ASM
# Aid Harrison
# 2023

#import numpy as np
import queue
from enum import Enum

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
        self.enumDef : STATEMENT_CMDS() = STATEMENT_CMDS()
        self.commands = {} # Line Index | STATEMENT type 
        self.DEBUG = True
        self.build(direct, debugActive)
        self.typePositions = []
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

    def lexer(self) -> bool:
        if self.source[0].find("_START") == -1:
            print("'_START' not found, please add")
            return False
        lineCount : int = 0
        for line in self.source:
            f_index : int = -1
            line.strip() # Clear starting and ending whitespace
            self.source[lineCount] = line # Rewrite to source
            # === Variables ===
            for i in types: # Search for datatype | int, flt, str, etc.
                f_index = line.find(i)
                if f_index != -1: # if valid type found, store position for check
                    typePositions.append(f_index)
            if not f_index == -1:
                var_type : int = self.type_check(line, f_index) # Store type for later assignment
                #print("type: ", var_type)
                f_index = line.find(':')
                if not f_index == -1:
                    # Get variable
                    print("Line: ", line)
                    curVar : str = ""
                    for i in range(f_index-1, 0, -1):
                        if not line[i].isdigit() and line[i] != ' ':
                            curVar += line[i]
                    #print("V: ", curVar)
                    # Variable is valid, get value
                    value : str = ""
                    for i in range(f_index+6, len(line)-1): # Minimum offset of 6
                        if line[i].isdigit():
                            value += line[i]
                    if var_type == 0:
                        variables[curVar] = int(value)
                    elif var_type == 1:
                        variables[curVar] = float(value) 
                    elif var_type == 2:
                        variables[curVar] = value
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
                # Get variable to wipe
                for i in variables.keys():
                    if line.find(i):
                        ...
                        #print(i)
                self.commands[lineCount] = self.enumDef.WIPE
            index = line.find("for")
            if not index == -1:
                # Obtain container OR range
                for i in range(index+4, len(line)):
                    ...
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