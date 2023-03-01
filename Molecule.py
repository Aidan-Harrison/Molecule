# Molecule
# Aid Harrison
# 2023
# Python 3.11.1
# Verison 0.3 (Alpha release)
    # ~ Now supports correct raw value calculation
    # ~ Variable compile now returns the last line to reduce number of iterations
        # ~ After variable compile, indexes are now skipped
    # ~ WIPE command now skips the current line
    # ~ ENUMS used for op code pattern matching
    # ~ Change from iterator to memory access iterating on core
    # ~ General code cleanup
    # ~ Whitespace is now cleared correctly
    # ~ Optimised comment check

# FIX first operand 0 issue on single operator!

import queue
import time
from enum import Enum

functions = {} # function name | function line | Move!
    # Allows for function overriding
class STATEMENT_CMDS():
    PUT    = 1
    WIPE   = 2
class OPERATOR_TOKENS():
    ADD    = 0
    SUB    = 1
    DIV    = 2
    MUL    = 3
    ADD_D  = 4
    SUB_D  = 5
    IS_EQ  = 6
    ADD_EQ = 7
    SUB_EQ = 8
    DIV_EQ = 9
    MUL_EQ = 10
    FN_RET = 11
    RET    = 12
    EQ     = 13

class Program:
    def __init__(self, direct : str = "", debugActive : bool = False) -> None:
        # === CORE DATA ===
        self.directory : str = direct
        self.source : str = []
        self.types : str  = ["int", "flt", "str"]
        self.enumDef = STATEMENT_CMDS()
        self.OP_TK   = OPERATOR_TOKENS()
        self.start_index : int = 0
        self.DEBUG = debugActive
        # === VARIABLES ===
        self.variables = {}
        self.lastType : str = "" # Used for variable compile
        self.operators = ['+', '-', '/', '*', '++', '--', '==', '+=', '-=', '/=', '*=', '->', '<-', '=']
        # === RUN ===
        self.build(direct)
        if not self.lexer():
            print("FAILED TO COMPILE!")
    
    def build(self, directory : str) -> None:
        with open(directory, "r") as f: 
            self.source = f.readlines()
    
    def retrieve_component(input_str : str, target_str : str) -> str:
        s_index : int = input_str.find(target_str)
        return_str : str = input_str[s_index]
        for i in range(s_index+1, len(input_str)):
            if input_str[i].isalnum():
                return_str += input_str[i]
        return return_str

    def function_call(self, index : int) -> bool:
        print(self.source[index])
        return False

    def variable_compile(self) -> bool:
        if self.source[0].find("_VAR") == -1:
            return False
        for line in range(1, len(self.source)): # Optimise if possible!
            f_index : int = -1
            self.source[line] = self.source[line].strip() # Clear whitespace
            if self.source[line] == "": # Ideally remove!
                continue
            elif self.source[line] == "}": # End of _VAR scope | Return index to skip lines
                self.start_index = line+1
                break
            #self.lastType = self.source[line].find([i for i in self.types]) != -1
            for i in self.types: # Search for datatype | int, flt, str, etc.
                if self.source[line].find(i) != -1: # if valid type found, store position for check
                    self.lastType = i
            f_index = self.source[line].find(":")
            if f_index == -1:
                print("Invalid syntax, used datatype without variable specifier | on line: ", line) # Convert to format print
                return False
            current_var_name : str = ""
            current_value : str = ""
            for i in range(f_index-1, -1, -1): # Get name
                if not self.source[line][i].isdigit() and self.source[line][i] != ' ':
                    current_var_name += self.source[line][i]
            for i in range(f_index+5, len(self.source[line])): # Get value
                if self.source[line][i] and self.source[line][i] != ' ' and self.source[line][i] != '=':
                    current_value += self.source[line][i]
            match self.lastType:
                case "int": self.variables[current_var_name[::-1]] = int(current_value)
                case "flt": self.variables[current_var_name[::-1]] = float(current_value)
                case "str": self.variables[current_var_name[::-1]] = current_value
        return True

    def operator_calc(self, cur_line : str, index : int, op_code : int): 
        #print(op_code)
        # Account for -> and <-
        #if op_code > 3: # NOT: +, -, /, *
            #var : str = ""
            #for i in range(index, 0, -1): 
                #if cur_line[i].isalnum():
                    #var += cur_line[i]
            #match op_code:
                #case 4: self.variables[var[::-1]] += 1 # ++
                #case 5: self.variables[var[::-1]] -= 1 # --
            #return -1
        # Standard operators (Two operands)
        # Change to allow variable + raw value!
        var_1 : str = ""
        var_2 : str = ""
        found_f_var : bool = False
        found_s_var : bool = False
        f_type : int = 0 # Defines type | 0 = INT, 1 = FLOAT, ... 
        s_type : int = 0  
        for var in self.variables: # Check for variables
            position : int = cur_line.find(var)
            if position != -1 and position < index: # Left side
                var_1 = var
                found_f_var = True
            elif position != -1 and position > index: # Right side
                var_2 = var
                found_s_var = True
            if found_f_var and found_s_var: 
                break # Prevents overchecking
        if not found_f_var and not found_s_var: 
            for i in range(index-1, -1, -1):
                if cur_line[i].isdigit():
                    var_1 += cur_line[i]
                elif cur_line[i] == '.': # Change!
                    f_type = 1
            for i in range(index+1, len(cur_line)):
                if cur_line[i].isdigit():
                    var_2 += cur_line[i]
                elif cur_line[i] == '.':
                    s_type = 1
        match op_code:
            case 0: # +
                if found_f_var and found_s_var: return self.variables[var_1] + self.variables[var_2]
                else: 
                    match f_type:
                        case 0: var_1 = int(var_1)
                        case 1: var_1 = float(var_1)
                    match s_type:
                        case 0: var_2 = int(var_2)
                        case 1: var_2 = float(var_2)
                    return var_1 + var_2
            case 1: # -
                if found_f_var and found_s_var: return self.variables[var_1] - self.variables[var_2]
                else: 
                    match f_type:
                        case 0: var_1 = int(var_1)
                        case 1: var_1 = float(var_1)
                    match s_type:
                        case 0: var_2 = int(var_2)
                        case 1: var_2 = float(var_2)
                    return var_1 - var_2
            case 2: # /
                if found_f_var and found_s_var: return self.variables[var_1] / self.variables[var_2]
                else: 
                    match f_type:
                        case 0: var_1 = int(var_1)
                        case 1: var_1 = float(var_1)
                    match s_type:
                        case 0: var_2 = int(var_2)
                        case 1: var_2 = float(var_2)
                    return var_1 / var_2
            case 3: # *
                if found_f_var and found_s_var: return self.variables[var_1] * self.variables[var_2]
                else: 
                    match f_type:
                        case 0: var_1 = int(var_1)
                        case 1: var_1 = float(var_1)
                    match s_type:
                        case 0: var_2 = int(var_2)
                        case 1: var_2 = float(var_2)
                    return var_1 * var_2
            case 4: # ++
                print("PLUS PLUS")
                if found_f_var: 
                    self.variables[var_1] += 1
                    return self.variables[var_1]
            case 5: # --
                if found_f_var: 
                    self.variables[var_1] -= 1
                    return self.variables[var_1]
            case 6:
                ...
        return 0
        
    def lexer(self) -> bool:
        for i in range(0, len(self.source)):
            self.start_index = self.source[i].find("_START")
            if self.start_index != -1:
                break
        if self.start_index == -1:
            print("'_START' not found, please add")
            return False
        if not self.variable_compile() and self.DEBUG:
            print("No variable storage found")
        lineCount : int = 0
        for line in range(self.start_index, len(self.source)):
            is_print_line : bool = False # Used for printing anything post "put"
            f_index : int = -1
            self.source[line] = self.source[line].strip() # Clear starting and ending whitespace
            #self.source[lineCount] = self.source[line] # Rewrite to source
            if self.source[line].startswith('/'): # COMMENT CHECK
                continue
            # ================== COMMANDS ==================
            index = self.source[line].find("put") # Reorder to allow line skip?
            if index != -1: 
                is_print_line = True
                output : str = ""
                for i in range(index+3, len(self.source[line])):
                    if self.source[line][i] == '"' and self.source[line][len(self.source[line])-2] == '"': #UPDATE?
                        for j in range(i+1, len(self.source[line])-2):
                            output += self.source[line][j]
                #print(is_print_line)
            if self.source[line].find("wipe") != -1:
                for i in self.variables.keys():
                    if self.source[line].find(i):
                        self.variables[i] = None
                continue # Skip line
            index = self.source[line].find("for")
            if index != -1:
                # Obtain container OR range
                counterVal : str = ""
                t_variable : str = "" # Used for variable storage, optimise
                    # Only create when needed
                for i in range(index+4, len(self.source[line])):
                    if self.source[line][i].isdigit(): # Easier to seperate to two counters
                        counterVal += self.source[line][i]
                    else: # Variable check
                        t_variable += self.source[line][i]
                        for var in self.variables.keys(): # Optimise, add flag instead of per loop iter!!!!
                            if t_variable == var:
                                counterVal = self.variables[t_variable]
                loop_range : int = int(counterVal)
                # Store each process in loop | DO
                for i in range(0, loop_range):
                    ...
            index = self.source[line].find("if")
            if index != -1:
                ...
            # ================== OPERATORS ==================
            # Scan for operators: +, -, /, *, ++, --, etc.
            for i in range(0, len(self.operators)):
                index : int = self.source[line].find(self.operators[i])
                if index != -1: 
                    op_code : int = -1 # Pattern match
                    match self.source[line][index]:
                        case '+':
                            match self.source[line][index+1]:
                                case '+': op_code = self.OP_TK.ADD_D;  break
                                case '=': op_code = self.OP_TK.ADD_EQ; break
                            op_code = self.OP_TK.ADD
                        case '-':
                            match self.source[line][index+1]: # Account for other possible operators
                                case '>': op_code = self.OP_TK.FN_RET; break
                                case '=': op_code = self.OP_TK.SUB_EQ; break
                            match self.source[line][index-1]:
                                case '<': op_code = self.OP_TK.RET; break
                            op_code = self.OP_TK.SUB
                        case '/':
                            match self.source[line][index+1]:
                                case '=': op_code = self.OP_TK.DIV_EQ; break
                            op_code = self.OP_TK.DIV
                        case '*':
                            match self.source[line][index+1]:
                                case '=': op_code = self.OP_TK.MUL_EQ; break
                            op_code = self.OP_TK.MUL
                        case '=':
                            if self.source[line][index+1] == '=': op_code = self.OP_TK.IS_EQ; break
                            op_code = self.OP_TK.EQ
                    result = self.operator_calc(self.source[line], index, op_code)
                    if is_print_line:
                        print(result)
            # ================== FUNCTIONS ==================
            if self.source[line].find("_FN") != -1:
                fn_name : str = "" # Make global
                for i in range(3, len(self.source[line])):
                    if self.source[line][i] == '(':
                        break
                    fn_name += self.source[line][i]
                functions[fn_name] = lineCount # Change, get lines in a global manner
            # ================== FN EXECUTE ==================
            if self.source[line].find("(") != -1 and self.source[line].find(")") != -1:
                if self.source[line].find("_FN") == -1:
                    # Get name, call appropiate function
                    fn_name : str = ""
                    for i in range(0, len(self.source[line])):
                        if self.source[line][i] == '(':
                            break
                        fn_name += self.source[line][i]
                    #self.function_call(functions[fn_name]) # Run function
            lineCount += 1
        return True

    def execute(self) -> bool:
        # Iterates over stored assets and computes
        #execute_queue : queue = queue.Queue(20) # Max func size of 20
        for func in functions.values():
            #execute_queue.append(func)
            self.function_call(func)
        return False

def main() -> None:
    start = time.perf_counter()
    newProgram : Program = Program("HelloWorld.txt", True)
    print(f"\n\n\nTime {time.perf_counter() - start} seconds")

if __name__ == "__main__":
    main()