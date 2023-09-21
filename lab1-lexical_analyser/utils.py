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

DL_table = ['(', ')', '[', ']', '{', '}', ',', ';']
