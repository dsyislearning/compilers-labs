# Token types
ID = "Identifier"       # 标识符
KW = "Keyword"          # 关键字
OP = "Operator"         # 运算符
CS = "Constant"         # 常量
SP = "Special Symbol"   # 特殊字符
# 注释直接跳过

# Token tables
KW_table = ['auto', 'break', 'case', 'char', 'const', 'continue', 'default',
            'do', 'double', 'else', 'enum', 'extern', 'float', 'for',
            'goto', 'if', 'inline', 'int', 'long', 'register', 'restrict',
            'return', 'short', 'signed', 'sizeof', 'static', 'struct', 'switch',
            'typedef', 'union', 'usigned', 'void', 'volatile', 'while', '_Bool',
            '_Complex', '_Imaginary']

ID_table = []

CS_table = []

SP_table = ['(', ')', '[', ']', '{', '}', '#', ';', '\\']

OP_table = ['+', '-', '*', '/', ]
