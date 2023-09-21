# States definitions
INIT = 0            # 初始状态
UNDERLINE = 1       # 标识符状态（下划线）
LETTER = 2          # 标识符状态（字母）
DIGIT = 3           # 数字状态
DOT = 4             # 小数点状态
SCI = 5             # 科学记数法状态
DECIMAL = 6         # 小数部分状态
EXP = 7             # 科学记数法的指数状态
APOSTR = 8          # 单引号（字符常量）状态
ESC = 9             # 转义状态
QUOTES = 10         # 双引号（字符串常量）状态
SLASH = 11          # 斜杠状态
LT = 12             # 小于号状态 Less Than
GT = 13             # 大于号状态 Greater Than

BCOMMENT = 21       # 多行注释/**/ BlockCOMMENT
LCOMMENT = 22       # 单行注释 //  LineCOMMENT
