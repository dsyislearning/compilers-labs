# Token types
ID = "Identifier"       # 标识符
KW = "Keyword"          # 关键字
OP = "Operator"         # 运算符
CS = "Constant"         # 常量
SP = "Special Symbol"   # 特殊字符
# 注释直接跳过

# Token tables
KW_table = ['auto', 'double', 'int', 'struct', 'break', 'else', 'long', 'switch',
            'case', 'enum', 'register', 'typedef', 'char', 'extern', 'return', 'union',
            'const', 'float', 'short', 'unsigned', 'continue', 'for', 'signed', 'void',
            'default', 'goto', 'sizeof', 'volatile', 'do', 'if', 'static', 'while', ]

ID_table = []

CS_table = []

SP_table = ['(', ')', '[', ']', '{', '}', '#', ';', '\\']

OP_table = ['+', '-', '*', '/', ]
