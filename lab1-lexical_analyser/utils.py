# Token types
ID = "Identifier"       # 标识符
KW = "Keyword"          # 关键字
OP = "Operator"         # 运算符
CS = "Constant"         # 常量
DL = "Delimiter"        # 分隔符
SP = "Special"          # 特殊字符
# 注释直接跳过

# Token tables
# 关键字表
KW_table = ['auto', 'break', 'case', 'char', 'const', 'continue', 'default',
            'do', 'double', 'else', 'enum', 'extern', 'float', 'for',
            'goto', 'if', 'inline', 'int', 'long', 'register', 'restrict',
            'return', 'short', 'signed', 'sizeof', 'static', 'struct', 'switch',
            'typedef', 'union', 'usigned', 'void', 'volatile', 'while', '_Bool',
            '_Complex', '_Imaginary']

# 转义字符表
ESC_table = ['\'', '"', '\\', 'a', 'b', 'f', 'n', 'r', 't', 'v']

# 分隔符表
DL_table = ['(', ')', '[', ']', '{', '}', ',', ';']

# Print functions
def print_error(line, msg):
    print(f'[ERROR] line {line + 1}: {msg}')

def print_warning(line, msg):
    print(f'[WARNING] line {line + 1}: {msg}')

def print_info():
    print("---------------------------------")
    print('''  ____   _                       
 / ___| | |    _____  _____ _ __ 
| |     | |   / _ \ \/ / _ \ '__|
| |___  | |__|  __/>  <  __/ |   
 \____| |_____\___/_/\_\___|_| ''')
    print("---------------------------------")
    print("A Lexical Analyzer for C")
    print("Version: 0.1\nAuthor: dsy")
    print("---------------------------------")
