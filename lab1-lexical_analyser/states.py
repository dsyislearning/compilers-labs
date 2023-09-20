# States definitions
INIT = 0        # 初始状态
UNDERLINE = 1   # 标识符状态（下划线）
LETTER = 2      # 标识符状态（字母）
DIGIT = 3       # 数字状态
DOT = 4         # 小数点状态
SCI = 5         # 科学记数法状态
DECIMAL = 6     # 小数部分状态
EXP = 7         # 科学记数法的指数状态
CHAR = 8        # 字符常量状态
