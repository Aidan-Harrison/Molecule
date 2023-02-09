# Mini ASM
# Aid Harrison
# 2023

#import numpy as np

# Lexer
assignmentTypes = ["int", "flt", "str"]
# Molecule
functions = {} # function name | function line
    # Allows for function overriding
variables = {} # "Variable Name" | <GENERIC>

class Program:
    def __init__(self) -> None:
        self.directory : str = ""
        self.source = []
    def build(self, directory : str) -> None:
        self.directory = directory
        # Write source and appropiate data
        with open(directory) as f:
            self.source = f.readlines()

    def type_check(self, line : str, index : int) -> int:
        # Get match working
        if line[index] == 'i':
            return 0
        elif line[index] == 'f':
            return 1
        elif line[index] == 's':
            return 2

    def type_get() -> int:
        ...

    def execute(self) -> bool:
        if self.source[0].find("_START") == -1:
            print("'_START' not found, please add")
            return False
        # Lexer
            # === Variables ===
        for line in self.source:
            line.strip() # Clear ending whitespace
            # Check through all possible variable assignments
            f_index : int = -1
            for i in assignmentTypes:
                f_index = line.find(i)
            var_type : int = self.type_check(line, f_index)
            #print("Var: ", var_type)
            if not f_index == -1:
                # Search for valid type syntax and variable name
                f_index = line.find(":")
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
            index = line.find("put") # Get content to print
            if not index == -1:
                #print('FOUND AT ', index, " on line | ", line)
                output : str = ""
                # Check if string, if not, check against base values, then variables
                #print("End: ", line[len(line)-2])
                for i in range(index+3, len(line)):
                    if line[i] == '"' and line[len(line)-2] == '"':
                        for j in range(i+1, len(line)-2):
                            output += line[j]
                    #break
                #print(output)
            index = line.find("wipe")
            if not index == -1:
                # Get variable to wipe
                for i in variables.keys():
                    if line.find(i):
                        ...
                        #print(i)
            index = line.find("for")
            if not index == -1:
                # Obtain container OR range
                ...
            # === Functions ===
            if line.find("_FN") != 1:
                fn_name : str = ""
                for i in range(3, len(line)):
                    if line[i] == '(':
                        break
                    fn_name += line[i]
                functions[fn_name] = line.find("_FN") # Change, get lines in a global manner

        #print(variables)
        #print(functions)
        return True

def main() -> None:
    newProgram : Program = Program()
    newProgram.build("HelloWorld.txt")
    newProgram.execute()
    #if not read(newProgram):
        #print("!COMPILE ERROR!")
    #else:
        #print("COMPILE SUCCESS")

if __name__ == "__main__":
    main()