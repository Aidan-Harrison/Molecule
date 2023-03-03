# Molecule
# Aid Harrison
# 2023
# Python 3.11.1
# Verison 0.4 (Alpha release)
    # ~ Fixed and improved 'put' statement
    # ~ Optimised operator search by only searching for core identifiers 
    # ~ Operators now support same variable calculations: x + x
    # ~ '++' && '--' operator now function as intended
    # ~ Functions and their arguments are now stored
    # ~ Comments now increase linecount
    # ~ Enums restored to global
    # ~ Converted to format prints

# Version 0.4.5
    # ~ Operator calc now uses enums for pattern matching 
    # ~ Now supports '^' (exponent) operator
    # ~ General cleanup

# Version 0.5
    # ~ Changed _FN compile to pre _START instead of post
    # ~ Empty operands are now accounted for
    # ~ var -> value & value -> var operands are now supported
    # ~ '=' operator now functions
    # ~ Now supports the '^=' operator
    # ~ Updated basis for function calling:
        # ~ Function body now stored
        # ~ Functions will be called using the 'call' command

    # ~ Functions can now be called (DO)
        # Done via call command 

# To-do
# FIX first operand 0 issue on single operator!
# Rewrite operator check to do global assignment (code compress)

import time
from enum import Enum
class STATEMENT_CMDS():
    PUT    = 1
    WIPE   = 2
    FOR    = 3
    IF     = 4
    CALL   = 5
class OP_TOKENS():
    ADD    = 0
    SUB    = 1
    DIV    = 2
    MUL    = 3
    EQ     = 4
    EX     = 5
    ADD_D  = 6
    SUB_D  = 7
    IS_EQ  = 8
    ADD_EQ = 9
    SUB_EQ = 10
    DIV_EQ = 11
    MUL_EQ = 12
    EX_EQ  = 13
    FN_RET = 14
    RET    = 15

class FUNCTION_RETURN_CODE():
    INT = 0
    FLT = 1
    STR = 2

class FUNCTION_STORAGE():
    def __init__(self, fn_name : str = "Default FN", argument_list = [], fn_index : int = 0) -> None:
        self.name : str = fn_name
        self.arg_list = argument_list
        self.index : int = fn_index
        self.body = []
        self.RETURN_CODE : int = FUNCTION_RETURN_CODE.INT

    def EXECUTE_FUNCTION(self) -> None:
        ...

    def DEBUG_PRINT(self) -> None:
        print(f"Name: {self.name}")
        print(f"Arguments: {self.arg_list}")
        print(f"Index: {self.index}")
        print(f"Body: {self.body}")
class Program:
    def __init__(self, direct : str = "", debugActive : bool = False) -> None:
        # === CORE DATA ===
        self.directory : str = direct
        self.source : str = []
        self.types : str  = ["int", "flt", "str"]
        #self.ST_CD = STATEMENT_CMDS()
        self.functions : FUNCTION_STORAGE = []
        self.start_index : int = 0
        # === VARIABLES ===
        self.variables = {}
        self.lastType : str = "" # Used for variable compile
        self.operators = ['+', '-', '/', '*', '=', '^', '++', '--', '==', '+=', '-=', '/=', '*=', '^=', '->', '<-']
        # === MISC ===
        self.DEBUG = debugActive
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
    
    def ERROR_CHECK(self) -> bool:
        ...

    def function_call(self, index : int) -> bool:
        print(f"{self.source[index]}")
        return False
    
    def function_compile(self) -> bool:
        for i in range(self.start_index, len(self.source)):
            ...

    def variable_compile(self) -> bool:
        if self.source[0].find("_VAR") == -1:
            return False
        for line in range(1, len(self.source)): # Optimise if possible!
            f_index : int = -1
            self.source[line] = self.source[line].strip() # Clear whitespace
            if self.source[line] == "": # Ideally remove!
                continue
            elif self.source[line] == "}": # End of _VAR scope | Returns index to skip lines
                self.start_index = line+1
                break
            #self.lastType = self.source[line].find([i for i in self.types]) != -1
            for i in self.types: # Search for datatype | int, flt, str, etc.
                if self.source[line].find(i) != -1: # if valid type found, store position for check
                    self.lastType = i
            f_index = self.source[line].find(":")
            if f_index == -1:
                print(f"Invalid syntax, used datatype without variable specifier | on line: {line}") # Convert to format print
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
        # Account for -> and <-
        # Change to allow variable + raw value!
        var_1 : str = ""
        var_2 : str = ""
        found_f_var : bool = False
        found_s_var : bool = False
        f_type : int = 0 # Defines type | 0 = INT, 1 = FLOAT, ... 
        s_type : int = 0  
        for var in self.variables: # Variable check
            l_position : int = cur_line.find(var) # Allows for same variable
            r_position : int = cur_line.rfind(var)
            if l_position != -1 and l_position < index: # Left side
                var_1 = var
                found_f_var = True
            if r_position != -1 and r_position > index: # Right side
                var_2 = var
                found_s_var = True
            if found_f_var and found_s_var: 
                break # Prevents overchecking
        if not found_f_var: # Check for left value
            for i in range(index-1, -1, -1):
                if cur_line[i].isdigit():
                    var_1 += cur_line[i]
                elif cur_line[i] == '.': # Change! Float check
                    f_type = 1
        #if var_1 == "":
            #return
        if not found_s_var:
            for i in range(index+1, len(cur_line)):
                if cur_line[i] == '"':
                    continue
                if cur_line[i].isdigit():
                    var_2 += cur_line[i]
                elif cur_line[i] == '.':
                    s_type = 1
        # print("Right operand: ", var_2)
        if var_2 == "":
            return
        match op_code:
            case OP_TOKENS.ADD: # +
                if found_f_var and found_s_var:       return self.variables[var_1] + self.variables[var_2]
                elif found_f_var and not found_s_var: return self.variables[var_1] + int(var_2)
                elif not found_f_var and found_s_var: return int(var_1) + self.variables[var_2]
                match f_type:
                    case 0: var_1 = int(var_1)
                    case 1: var_1 = float(var_1)
                match s_type:
                    case 0: var_2 = int(var_2)
                    case 1: var_2 = float(var_2)
                return var_1 + var_2
            case OP_TOKENS.SUB: # -
                if found_f_var and found_s_var:       return self.variables[var_1] - self.variables[var_2]
                elif found_f_var and not found_s_var: return self.variables[var_1] - int(var_2)
                elif not found_f_var and found_s_var: return int(var_1) - self.variables[var_2]
                match f_type:
                    case 0: var_1 = int(var_1)
                    case 1: var_1 = float(var_1)
                match s_type:
                    case 0: var_2 = int(var_2)
                    case 1: var_2 = float(var_2)
                return var_1 - var_2
            case OP_TOKENS.DIV: # /
                if found_f_var and found_s_var:       return self.variables[var_1] / self.variables[var_2]
                elif found_f_var and not found_s_var: return self.variables[var_1] / int(var_2)
                elif not found_f_var and found_s_var: return int(var_1) / self.variables[var_2]
                match f_type:
                    case 0: var_1 = int(var_1)
                    case 1: var_1 = float(var_1)
                match s_type:
                    case 0: var_2 = int(var_2)
                    case 1: var_2 = float(var_2)
                return var_1 / var_2
            case OP_TOKENS.MUL: # *
                if found_f_var and found_s_var:       return self.variables[var_1] * self.variables[var_2]
                elif found_f_var and not found_s_var: return self.variables[var_1] * int(var_2)
                elif not found_f_var and found_s_var: return int(var_1) * self.variables[var_2]
                match f_type:
                    case 0: var_1 = int(var_1)
                    case 1: var_1 = float(var_1)
                match s_type:
                    case 0: var_2 = int(var_2)
                    case 1: var_2 = float(var_2)
                return var_1 * var_2
            case OP_TOKENS.ADD_D: # ++
                if found_f_var: 
                    self.variables[var_1] += 1
                    return self.variables[var_1]
            case OP_TOKENS.SUB_D: # --
                if found_f_var: 
                    self.variables[var_1] -= 1
                    return self.variables[var_1]
            case OP_TOKENS.EQ: # = 
                if found_f_var and found_s_var: self.variables[var_1] = self.variables[var_2]
                elif found_f_var and not found_s_var: 
                    match s_type:
                        case 0: self.variables[var_1] = int(var_2)
                        case 1: self.variables[var_1] = float(var_2)
                        case 2: self.variables[var_1] = var_2
            case OP_TOKENS.EX:
                if found_f_var and found_s_var:       return self.variables[var_1] ** self.variables[var_2]
                elif found_f_var and not found_s_var: return self.variables[var_1] ** int(var_2)
                elif not found_f_var and found_s_var: return int(var_1) ** self.variables[var_2]
                match f_type:
                    case 0: var_1 = int(var_1)
                    case 1: var_1 = float(var_1)
                match s_type:
                    case 0: var_2 = int(var_2)
                    case 1: var_2 = float(var_2)
                return var_1**var_2
            case OP_TOKENS.EX_EQ:
                if found_f_var and found_s_var:       
                    result = self.variables[var_1] ** self.variables[var_2]
                    self.variables[var_1] = result
                elif found_f_var and not found_s_var: 
                    result = self.variables[var_1] ** int(var_2)
                    self.variables[var_1] = result
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
            line_output : str = ""
            f_index : int = -1
            self.source[line] = self.source[line].strip() # Clear starting and ending whitespace
            #self.source[lineCount] = self.source[line] # Rewrite to source
            if self.source[line].startswith('/'): # COMMENT CHECK
                lineCount += 1
                continue
            # ================== COMMANDS ==================
            index = self.source[line].find("put") # Reorder to allow line skip?
            if index != -1: 
                is_print_line = True
                for i in range(index+3, len(self.source[line])):
                    if self.source[line][i] != ' ':
                        line_output += self.source[line][i]
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
            for i in range(0, 6): # Only scan through identifiers
                index : int = self.source[line].find(self.operators[i])
                if index != -1: 
                    op_code : int = -1 # Pattern match
                    if index + 1 > len(self.source[line])-1:
                        break
                    match self.source[line][index]:
                        case '+':
                            op_code = OP_TOKENS.ADD
                            match self.source[line][index+1]:
                                case '+': op_code = OP_TOKENS.ADD_D
                                case '=': op_code = OP_TOKENS.ADD_EQ
                        case '-':
                            op_code = OP_TOKENS.SUB
                            match self.source[line][index+1]: 
                                case '>': op_code = OP_TOKENS.FN_RET
                                case '=': op_code = OP_TOKENS.SUB_EQ
                            match self.source[line][index-1]:
                                case '<': op_code = OP_TOKENS.RET
                        case '/':
                            op_code = OP_TOKENS.DIV
                            match self.source[line][index+1]:
                                case '=': op_code = OP_TOKENS.DIV_EQ
                        case '*':
                            op_code = OP_TOKENS.MUL
                            match self.source[line][index+1]:
                                case '=': op_code = OP_TOKENS.MUL_EQ
                        case '=':
                            op_code = OP_TOKENS.EQ
                            if self.source[line][index+1] == '=': op_code = OP_TOKENS.IS_EQ
                        case '^':
                            op_code = OP_TOKENS.EX
                            match self.source[line][index+1]:
                                case '=': op_code = OP_TOKENS.EX_EQ
                    line_output = self.operator_calc(self.source[line], index, op_code)
            # ================== FUNCTIONS ==================
            if self.source[line].find("_FN BLOCK") != -1:
                for i in range(line+1, len(self.source)):
                    ...
                    #print(self.source[j])
            if self.source[line].find("_FN") != -1:
                fn_name : str = "" # Make global
                has_args : bool = False
                arguments = []
                for i in range(3, len(self.source[line])):
                    if self.source[line][i] == '(': # Argument search
                        curArgument : str = ""
                        for j in range(i+1, len(self.source[line])):
                            if self.source[line][j] == ',': # New var
                                arguments.append(curArgument)
                                curArgument = ""
                            elif self.source[line][j] == ' ':
                                continue
                            elif self.source[line][j] == ')':
                                arguments.append(curArgument)
                                has_args = True
                                break
                            else:
                                curArgument += self.source[line][j]
                    if has_args:
                        break
                    if self.source[line][i] != ' ': # Name
                        fn_name += self.source[line][i]
                new_function : FUNCTION_STORAGE = FUNCTION_STORAGE(fn_name, arguments, line)
                for i in range(line, len(self.source)): # Get body
                    if self.source[line] == "} ":
                        break
                    new_function.body.append(self.source[line])
                    # del self.source[line] # FIX!
                self.functions.append(new_function)
            if self.source[line].find("call") != -1:
                for func in self.functions:
                    if self.source[line].find(func.name):
                        func.EXECUTE_FUNCTION()
            # ================== FN EXECUTE ================== | REMOVE!
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
            if is_print_line:
                if line_output in self.variables:
                    print(f"{self.variables[line_output]}")
                else:
                    print(f"{line_output}")
        return True

    def execute(self) -> bool:
        for line in self.source:
            ...
            #for func in self.functions:
                #func.EXECUTE_FUNCTION()
        return False

def main() -> None:
    #start = time.perf_counter()
    newProgram : Program = Program("HelloWorld.txt", True)
    #print(f"\n\n\nTime {time.perf_counter() - start} seconds")

if __name__ == "__main__":
    main()