import sys
import os

# from logconfig import *       # 日志系统
from states import *    # 状态常量
from utils import *     # 记号表

class LexicalAnalyzer:
    def __init__(self, input, output):
        self.fin = input
        self.fout = output
        self.state = INIT
        self.buffer = ''    # 正常读入的缓冲区
        self.ahead = ''     # 超前读入的缓冲区
        self.ch = ''
        self.token = ''
        self.warnings = 0
        self.errors = 0
        self.lines = 0
        self.characters = 0
        self.ID_num = 0
        self.KW_num = 0
        self.OP_num = 0
        self.CS_num = 0
        self.DL_num = 0
        self.SP_num = 0

    def analyze(self):
        """词法分析过程"""
        # 打开文件
        self.fin = open(self.fin, 'r')
        self.fout = open(self.fout, 'w')
        # 状态机逻辑
        while True:
            if self.state == INIT: # 初始状态
                # log.debug(f'[State:{self.state}] [C:{repr(self.ch)}] [buffer:{repr(self.buffer)}] [ahead:{repr(self.ahead)}]')
                self.read_char()
                self.read_white()
                if self.ch == '_':
                    self.state = UNDERLINE
                elif self.ch.isalpha():
                    self.state = LETTER
                elif self.ch.isdigit():
                    self.state = DIGIT
                elif self.ch == '\'':
                    self.state = APOSTR
                elif self.ch == '"':
                    self.state = QUOTES
                elif self.ch == '<':
                    self.state = LT
                elif self.ch == '>':
                    self.state = GT
                elif self.ch == '=':
                    self.state = EQ
                elif self.ch == '+':
                    self.state = ADD
                elif self.ch == '-':
                    self.state = DASH
                elif self.ch == '*':
                    self.state = STAR
                elif self.ch == '&':
                    self.state = AMPER
                elif self.ch == '|':
                    self.state = PIPE
                elif self.ch == '^':
                    self.state = CARET
                elif self.ch == '~':
                    self.state = TIDE
                elif self.ch == '!':
                    self.state = EXCLAIM
                elif self.ch == '%':
                    self.state = MODULO
                elif self.ch == '.':
                    self.state = DOT
                elif self.ch == '/':
                    self.state = SLASH
                elif self.ch in DL_table:
                    self.token += self.ch
                    self.write_token(DL) # 分隔符
                    self.DL_num += 1
                else:
                    self.token += self.ch
                    self.write_token(SP) # 特殊字符
                    self.SP_num += 1
            elif self.state == UNDERLINE or self.state == LETTER: # 标识符状态
                self.token += self.ch
                self.read_char()
                if self.ch == '_' or self.ch.isdigit() or self.ch.isalpha():
                    self.state = LETTER # 还是标识符状态
                else:
                    self.retract()
                    if self.token in KW_table: # 查关键字表
                        self.write_token(KW) # 关键字
                        self.KW_num += 1
                    else:
                        self.write_token(ID) # 标识符
                        self.ID_num += 1
            elif self.state == DIGIT: # 数字状态
                self.token += self.ch
                self.read_char()
                if self.ch.isdigit():
                    if self.token[0] == '0' and (self.ch == '8' or self.ch =='9'):
                        self.handle_errors()
                    else:
                        self.state = DIGIT # 还是数字状态
                elif self.ch == '.':
                    self.state = DOT
                elif self.ch == '_' or self.ch.isalpha():
                    self.handle_errors() # 非法标识符
                else:
                    self.retract()
                    self.write_token(CS) # 常量（整数）
                    self.CS_num += 1
            elif self.state == DOT: # 小数点状态
                self.token += self.ch
                self.read_char()
                if self.ch.isdigit():
                    if self.token[0] == '.':
                        self.handle_errors() # 小数点前没有0
                    else:
                        self.state = DECIMAL # 小数部分状态
                else:
                    self.handle_errors() # 小数点后没有0
            elif self.state == DECIMAL: # 小数部分状态
                self.token += self.ch
                self.read_char()
                if self.ch.isdigit():
                    self.state = DECIMAL
                elif self.ch == 'E' or self.ch == 'e':
                    self.state = SCI
                else:
                    self.retract()
                    self.write_token(CS) # 常量（浮点数）
                    self.CS_num += 1
            elif self.state == SCI: # 科学记数法状态
                self.token += self.ch
                self.read_char()
                if self.ch.isdigit() or self.ch == '+' or self.ch == '-':
                    self.state = EXP # 指数部分
                else:
                    self.handle_errors()
            elif self.state == EXP: # 科学记数法指数部分
                self.token += self.ch
                self.read_char()
                if self.ch.isdigit():
                    self.state = EXP
                else:
                    self.retract()
                    self.write_token(CS) # 常量（科学记数法）
                    self.CS_num += 1
            elif self.state == APOSTR: # 单引号状态
                self.token += self.ch
                self.read_char()
                if self.ch == '\\':
                    self.state = ESC # 转义字符
                elif self.ch == '\'':
                    self.handle_errors() # C语言不支持空字符常量
                else:
                    self.token += self.ch
                    self.read_char()
                    if self.ch == '\'':
                        self.token += self.ch
                        self.write_token(CS) # 单字符常量
                        self.CS_num += 1
                    else:
                        self.handle_errors() # 多于一个字符
            elif self.state == ESC: # 转义字符
                self.token += self.ch
                self.read_char()
                if self.ch in ESC_table:
                    self.token += self.ch
                    self.read_char()
                    if self.ch == '\'':
                        self.token += self.ch
                        self.write_token(CS) # 转义字符常量
                        self.CS_num += 1
                        self.state = INIT
                    else:
                        self.handle_errors() # 多于一个字符
                else:
                    if self.ch == '\'':
                        self.handle_errors() # 只有一个转义符号 \
                    else:
                        self.token = self.token[:-1]
                        self.token += self.ch
                        self.read_char()
                        if self.ch == '\'':
                            self.handle_errors() # 无效的转义字符，保留后面一个字符
                        else:
                            self.handle_errors() # 多于一个字符
            elif self.state == QUOTES: # 双引号状态
                self.token += self.ch
                self.read_char()
                if self.ch == '"':
                    self.token += self.ch
                    self.write_token(CS) # 字符串常量
                    self.CS_num += 1
                else:
                    self.state = QUOTES
            elif self.state == LT: # 小于号状态
                self.token += self.ch
                self.read_char()
                if self.ch == '<':
                    self.token += self.ch
                    self.read_char()
                    if self.ch == '=':
                        self.token += self.ch
                        self.write_token(OP) # <<= 赋值运算符
                        self.OP_num += 1
                    else:
                        self.retract()
                        self.write_token(OP) # << 移位运算符
                        self.OP_num += 1
                elif self.ch == '=':
                    self.token += self.ch
                    self.write_token(OP) # <= 比较运算符
                    self.OP_num += 1
                else:
                    self.retract()
                    self.write_token(OP) # < 比较运算符
                    self.OP_num += 1
            elif self.state == GT: # 大于号状态
                self.token += self.ch
                self.read_char()
                if self.ch == '>':
                    self.token += self.ch
                    self.read_char()
                    if self.ch == '=':
                        self.token += self.ch
                        self.write_token(OP) # >>= 赋值运算符
                        self.OP_num += 1
                    else:
                        self.retract()
                        self.write_token(OP) # >> 移位运算符
                        self.OP_num += 1
                elif self.ch == '=':
                    self.token += self.ch
                    self.write_token(OP) # >= 比较运算符
                    self.OP_num += 1
                else:
                    self.retract()
                    self.write_token(OP) # > 比较运算符
                    self.OP_num += 1
            elif self.state == EQ: # =
                self.token += self.ch
                self.read_char()
                if self.ch == '=':
                    self.token += self.ch
                    self.write_token(OP) # ==
                    self.OP_num += 1
                else:
                    self.retract()
                    self.write_token(OP) # =
                    self.OP_num += 1
            elif self.state == ADD: # +
                self.token += self.ch
                self.read_char()
                if self.ch == '+':
                    self.token += self.ch
                    self.write_token(OP) # ++
                    self.OP_num += 1
                elif self.ch == '=':
                    self.token += self.ch
                    self.write_token(OP) # +=
                    self.OP_num += 1
                else:
                    self.retract()
                    self.write_token(OP) # +
                    self.OP_num += 1
            elif self.state == DASH: # -
                self.token += self.ch
                self.read_char()
                if self.ch == '-':
                    self.token += self.ch
                    self.write_token(OP) # --
                    self.OP_num += 1
                elif self.ch == '=':
                    self.token += self.ch
                    self.write_token(OP) # -=
                    self.OP_num += 1
                elif self.ch == '>':
                    self.token += self.ch
                    self.write_token(OP) # ->
                    self.OP_num += 1
                else:
                    self.retract()
                    self.write_token(OP) # -
                    self.OP_num += 1
            elif self.state == STAR: # *
                self.token += self.ch
                self.read_char()
                if self.ch == '=':
                    self.token += self.ch
                    self.write_token(OP) # *=
                    self.OP_num += 1
                else:
                    self.retract()
                    self.write_token(OP) # *
                    self.OP_num += 1
            elif self.state == AMPER: # &
                self.token += self.ch
                self.read_char()
                if self.ch == '&':
                    self.token += self.ch
                    self.write_token(OP) # &&
                    self.OP_num += 1
                elif self.ch == '=':
                    self.token += self.ch
                    self.write_token(OP) # &=
                    self.OP_num += 1
                else:
                    self.retract()
                    self.write_token(OP) # &
                    self.OP_num += 1
            elif self.state == PIPE: # |
                self.token += self.ch
                self.read_char()
                if self.ch == '|':
                    self.token += self.ch
                    self.write_token(OP) # ||
                    self.OP_num += 1
                elif self.ch == '=':
                    self.token += self.ch
                    self.write_token(OP) # |=
                    self.OP_num += 1
                else:
                    self.retract()
                    self.write_token(OP) # |
                    self.OP_num += 1
            elif self.state == CARET: # ^
                self.token += self.ch
                self.read_char()
                if self.ch == '=':
                    self.token += self.ch
                    self.write_token(OP) # ^=
                    self.OP_num += 1
                else:
                    self.retract()
                    self.write_token(OP) # ^
                    self.OP_num += 1
            elif self.state == TIDE:
                self.token += self.ch
                self.write_token(OP) # ~ 按位取反
                self.OP_num += 1
            elif self.state == EXCLAIM:
                self.token += self.ch
                self.read_char()
                if self.ch == '=':
                    self.token += self.ch
                    self.write_token(OP) # !=
                    self.OP_num += 1
                else:
                    self.retract()
                    self.write_token(OP) # !
                    self.OP_num += 1
            elif self.state == MODULO: # %
                self.token += self.ch
                self.read_char()
                if self.ch == '=':
                    self.token += self.ch
                    self.write_token(OP) # %=
                    self.OP_num += 1
                else:
                    self.retract()
                    self.write_token(OP) # %
                    self.OP_num += 1
            elif self.state == SLASH: # 斜杠状态
                self.token += self.ch
                self.read_char()
                if self.ch == '*':
                    self.state = BCOMMENT # 多行注释
                elif self.ch == '/':
                    self.state = LCOMMENT # 单行注释
                else:
                    self.retract()
                    self.write_token(OP) # 操作符（除法）
                    self.OP_num += 1
            elif self.state == BCOMMENT: # 多行注释
                self.read_char()
                while self.ch != '*': # 注释全部跳过
                    self.read_char()
                self.read_char() # 查看第二个*之后的字符
                if self.ch == '/': # 注释结束
                    self.token = ''
                    self.state = INIT
                else:
                    self.state = BCOMMENT
            elif self.state == LCOMMENT: # 单行注释
                self.read_char()
                while self.ch != '\n':
                    self.read_char()
                self.token = ''
                self.state = INIT
            else:
                break

    def read_char(self):
        """每调用一次，返回forward指向的buffer中的字符，并把它放入变量ch中，然后，移动forward，使之指向下一个字符"""
        if self.buffer == '':
            if self.ahead != '':
                self.buffer += self.ahead[0]
                self.ahead = self.ahead[1:]
            else:
                rd = self.fin.read(1)
                if rd == '': # 读到文件末尾，结束词法分析程序
                    self.fin.close()
                    self.fout.close()
                    self.print_result() # 打印结果
                    exit(0)
                else:
                    self.buffer += rd
                    self.characters += 1
                    if rd == '\n':
                        self.lines += 1
        self.ch = self.buffer[-1]
        if self.ahead != '':
            self.buffer += self.ahead[0]
            self.ahead = self.ahead[1:]
        else:
            rd = self.fin.read(1)
            if rd != '':
                self.characters += 1
                if rd == '\n':
                    self.lines += 1
            self.buffer += rd
        return self.ch

    def read_white(self):
        """检查ch中的字符是否为空格，若是，则反复调用read_char()，直到ch中进入一个非空字符为止"""
        while self.ch.isspace():
            self.buffer = self.buffer[1:]
            self.read_char()

    def write_token(self, token_type):
        """将识别出来的单词记号写入输出，并刷新token，进入下一轮分析"""
        # log.debug(f'[State:{self.state}] [C:{repr(self.ch)}] [buffer:{repr(self.buffer)}] [ahead:{repr(self.ahead)}]')
        self.fout.write("{0}: {1}\n".format(token_type, self.token))
        self.token = ''
        self.buffer = self.buffer[-1:]
        self.state = INIT

    def retract(self):
        """向前指针forward后退一个字符"""
        self.ahead = self.buffer[-1] + self.ahead[:]
        self.buffer = self.buffer[:-1]
        self.ch = self.buffer[-2]

    def handle_errors(self):
        """对发现的词法错误进行相应的处理"""
        if self.state == DOT:
            if self.token[0] =='.': # 小数点前没有0
                self.token = '0' + self.token[:]
                self.state = DECIMAL
            else: # 小数点后没有数字，自动补0
                self.warnings += 1
                self.retract()
                self.ch = '0'
                self.state = DECIMAL
        elif self.state == DIGIT:
            if self.ch.isdigit(): # 0开头非八进制，去掉0
                self.warnings += 1
                self.token = self.token[1:]
                self.state = DIGIT # 继续读后面的
            elif self.ch == '_' or self.ch.isalpha(): # 非法标识符（数字开头）
                self.errors += 1
                self.read_char()
                while self.ch.isdigit() or self.ch.isalpha() or self.ch == '_': # 跳过非法标识符
                    self.read_char()
                self.token = ''
                self.state = INIT
        elif self.state == SCI: # 指数部分没有数字，自动补0
            self.warnings += 1
            self.retract()
            self.token += '0'
            self.write_token(CS)
            self.state = INIT
        elif self.state == APOSTR:
            self.errors += 1
            if self.ch == '\'': # 空字符常量
                self.token = ''
                self.state = INIT
            else: # 多于一个字符
                self.retract() # 回退到第一个字符
                self.retract() # 回退到第一个单引号
                self.token = ''
                self.state = INIT
        elif self.state == ESC:
            self.errors += 1
            if self.ch != '\'': # 多于一个字符
                self.retract() # 退回到转义字符
                self.retract() # 退回到转义\
                self.retract() # 退回到第一个单引号
                self.token = ''
                self.state = INIT
            else:
                self.token = ''
                self.state = INIT # 非法转义字符

    def print_result(self):
        print_info()
        print(f"File: {os.path.join(os.getcwd(), self.fin.name)}")
        print(f"Lines: {self.lines}, Characters: {self.characters}")
        print(f'Identifiers: {self.ID_num}')
        print(f'Keywords: {self.KW_num}')
        print(f'Operators: {self.OP_num}')
        print(f'Constants: {self.CS_num}')
        print(f'Delimiters: {self.DL_num}')
        print(f'Special Symbols: {self.SP_num}')
        print(f'Errors: {self.errors}, Warnings: {self.warnings}')
        print(f'Output: {os.path.join(os.getcwd(), self.fout.name)}')


def main():
    analyer = LexicalAnalyzer(sys.argv[1], 'tokens.txt')
    analyer.analyze()


if __name__ == '__main__':
    main()
