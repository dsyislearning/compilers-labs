import sys

from states import *    # 状态常量
from utils import *     # 记号表

class LexicalAnalyzer:
    def __init__(self, input, output):
        self.fin = input
        self.fout = output
        self.logfile = open('log.txt', 'w')
        self.state = INIT
        self.buffer = ''    # 正常读入的缓冲区
        self.ahead = ''     # 超前读入的缓冲区
        self.ch = ''
        self.token = ''

    def analyze(self):
        """词法分析过程"""
        # 打开文件
        self.fin = open(self.fin, 'r')
        self.fout = open(self.fout, 'w')
        # 状态机逻辑
        while True:
            if self.state == INIT: # 初始状态
                # self.log()
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
                    self.token += self.ch
                    self.write_token(OP) # . 取成员
                elif self.ch == '/':
                    self.state = SLASH
                elif self.ch in DL_table:
                    self.token += self.ch
                    self.write_token(DL) # 分隔符
                else:
                    self.token += self.ch
                    self.write_token(SP) # 特殊字符
            elif self.state == UNDERLINE or self.state == LETTER: # 标识符状态
                self.token += self.ch
                self.read_char()
                if self.ch == '_' or self.ch.isdigit() or self.ch.isalpha():
                    self.state = LETTER # 还是标识符状态
                else:
                    self.retract()
                    if self.token in KW_table: # 查关键字表
                        self.write_token(KW) # 关键字
                    else:
                        self.write_token(ID) # 标识符
            elif self.state == DIGIT: # 数字状态
                self.token += self.ch
                self.read_char()
                if self.ch.isdigit():
                    self.state = DIGIT # 还是数字状态
                elif self.ch == '.':
                    self.state = DOT
                else:
                    self.retract()
                    self.write_token(CS) # 常量（整数）
            elif self.state == DOT: # 小数点状态
                self.token += self.ch
                self.read_char()
                if self.ch.isdigit():
                    self.state = DECIMAL # 小数部分状态
                else:
                    self.handle_errors()
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
            elif self.state == APOSTR: # 单引号状态
                self.token += self.ch
                self.read_char()
                if self.ch == '\\':
                    self.state = ESC # 转义字符
                elif self.ch == '\'' or self.ch == '"':
                    self.handle_errors() # 引号未转义
                else:
                    self.token += self.ch
                    self.read_char()
                    if self.ch == '\'':
                        self.token += self.ch
                        self.write_token(CS)
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
                        self.write_token(CS)
                        self.state = INIT
                    else:
                        self.handle_errors()
            elif self.state == QUOTES: # 双引号状态
                self.token += self.ch
                self.read_char()
                if self.ch == '"':
                    self.token += self.ch
                    self.write_token(CS) # 字符串常量
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
                    else:
                        self.retract()
                        self.write_token(OP) # << 移位运算符
                elif self.ch == '=':
                    self.token += self.ch
                    self.write_token(OP) # <= 比较运算符
                else:
                    self.retract()
                    self.write_token(OP) # < 比较运算符
            elif self.state == GT: # 大于号状态
                self.token += self.ch
                self.read_char()
                if self.ch == '>':
                    self.token += self.ch
                    self.read_char()
                    if self.ch == '=':
                        self.token += self.ch
                        self.write_token(OP) # >>= 赋值运算符
                    else:
                        self.retract()
                        self.write_token(OP) # >> 移位运算符
                elif self.ch == '=':
                    self.token += self.ch
                    self.write_token(OP) # >= 比较运算符
                else:
                    self.retract()
                    self.write_token(OP) # > 比较运算符
            elif self.state == EQ: # =
                self.token += self.ch
                self.read_char()
                if self.ch == '=':
                    self.token += self.ch
                    self.write_token(OP) # ==
                else:
                    self.retract()
                    self.write_token(OP) # =
            elif self.state == ADD: # +
                self.token += self.ch
                self.read_char()
                if self.ch == '+':
                    self.token += self.ch
                    self.write_token(OP) # ++
                elif self.ch == '=':
                    self.token += self.ch
                    self.write_token(OP) # +=
                else:
                    self.retract()
                    self.write_token(OP) # +
            elif self.state == DASH: # -
                self.token += self.ch
                self.read_char()
                if self.ch == '-':
                    self.token += self.ch
                    self.write_token(OP) # --
                elif self.ch == '=':
                    self.token += self.ch
                    self.write_token(OP) # -=
                elif self.ch == '>':
                    self.token += self.ch
                    self.write_token(OP) # ->
                else:
                    self.retract()
                    self.write_token(OP) # -
            elif self.state == STAR: # *
                self.token += self.ch
                self.read_char()
                if self.ch == '=':
                    self.token += self.ch
                    self.write_token(OP) # *=
                else:
                    self.retract()
                    self.write_token(OP) # *
            elif self.state == AMPER: # &
                self.token += self.ch
                self.read_char()
                if self.ch == '&':
                    self.token += self.ch
                    self.write_token(OP) # &&
                elif self.ch == '=':
                    self.token += self.ch
                    self.write_token(OP) # &=
                else:
                    self.retract()
                    self.write_token(OP) # &
            elif self.state == PIPE: # |
                self.token += self.ch
                self.read_char()
                if self.ch == '|':
                    self.token += self.ch
                    self.write_token(OP) # ||
                elif self.ch == '=':
                    self.token += self.ch
                    self.write_token(OP) # |=
                else:
                    self.retract()
                    self.write_token(OP) # |
            elif self.state == CARET: # ^
                self.token += self.ch
                self.read_char()
                if self.ch == '=':
                    self.token += self.ch
                    self.write_token(OP) # ^=
                else:
                    self.retract()
                    self.write_token(OP) # ^
            elif self.state == TIDE:
                self.token += self.ch
                self.write_token(OP) # ~ 按位取反
            elif self.state == EXCLAIM:
                self.token += self.ch
                self.read_char()
                if self.ch == '=':
                    self.token += self.ch
                    self.write_token(OP) # !=
                else:
                    self.retract()
                    self.write_token(OP) # !
            elif self.state == MODULO: # %
                self.token += self.ch
                self.read_char()
                if self.ch == '=':
                    self.token += self.ch
                    self.write_token(OP) # %=
                else:
                    self.retract()
                    self.write_token(OP) # %
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
                self.buffer += self.fin.read(1)
                if self.buffer == '': # 读到文件末尾，结束词法分析程序
                    self.fin.close()
                    self.fout.close()
                    self.logfile.close()
                    exit(0)
        self.ch = self.buffer[-1]
        if self.ahead != '':
            self.buffer += self.ahead[0]
            self.ahead = self.ahead[1:]
        else:
            self.buffer += self.fin.read(1)
        return self.ch

    def read_white(self):
        """检查ch中的字符是否为空格，若是，则反复调用read_char()，直到ch中进入一个非空字符为止"""
        while self.ch.isspace():
            self.buffer = self.buffer[1:]
            self.read_char()

    def write_token(self, token_type):
        """将识别出来的单词记号写入输出，并刷新token，进入下一轮分析"""
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
        # TODO
        self.state = INIT
    
    def log(self):
        self.logfile.write(f'State: {self.state}\t\tC: [{self.ch}]\t\tbuffer: [{self.buffer}]\t\tahead: [{self.ahead}]\n')


def main():
    analyer = LexicalAnalyzer(sys.argv[1], 'tokens.txt')
    analyer.analyze()


if __name__ == '__main__':
    main()
