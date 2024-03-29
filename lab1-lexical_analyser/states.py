# States definitions
INIT = 0            # 初始状态
UNDERLINE = 1       # 标识符状态（下划线）
LETTER = 2          # 标识符状态（字母）
DIGIT = 3           # 数字状态
DOT = 4             # 小数点状态
SCI = 5             # 科学记数法状态
DECIMAL = 6         # 小数部分状态
EXP = 7             # 科学记数法的指数状态
APOSTR = 8          # 单引号（字符常量）状态 apostrophe
ESC = 9             # 转义状态
QUOTES = 10         # 双引号（字符串常量）状态
SLASH = 11          # 斜杠（除号）状态
LT = 12             # 小于号状态 Less Than
GT = 13             # 大于号状态 Greater Than
EQ = 14             # 等于号 Equal
ADD = 15            # + 加号状态
DASH = 16           # - 减号状态
STAR = 17           # 星号（乘号）状态
AMPER = 18          # & 号状态 ampersand
PIPE = 19           # | 号状态 pipe
CARET = 20          # ^ 号状态 caret
TIDE = 21           # ~
EXCLAIM = 22        # !
BCOMMENT = 23       # 多行注释/**/ BlockCOMMENT
LCOMMENT = 24       # 单行注释 //  LineCOMMENT
MODULO = 25         # %
HEX = 26            # 十六进制数状态
