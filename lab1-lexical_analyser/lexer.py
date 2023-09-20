import sys

from states import *    # 状态常量
from utils import *     # 记号表

class LexicalAnalyzer:
    def __init__(self, input, output):
        self.fin = input
        self.fout = output
        self.state = INIT
        self.buffer = ''
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
                self.read_char()
                self.read_white()
                if self.ch == '_':
                    self.state = UNDERLINE
                elif self.ch.isalpha():
                    self.state = LETTER
                elif self.ch.isdigit():
                    self.state = DIGIT
                # elif self.ch == '\'':
                #     self.state = CHAR
            elif self.state == UNDERLINE or self.state == LETTER: # 标识符状态
                self.token += self.ch
                self.read_char()
                if self.ch == '_' or self.ch.isdigit() or self.ch.isalpha():
                    self.state = LETTER # 还是标识符状态
                else:
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
                    self.write_token(CS) # 常量（科学记数法）
            else:
                break
                

    def read_char(self):
        """每调用一次，返回forward指向的buffer中的字符，并把它放入变量ch中，然后，移动forward，使之指向下一个字符"""
        if self.buffer == '':
            self.buffer += self.fin.read(1)
            if self.buffer == '': # 读到文件末尾，结束词法分析程序
                self.fin.close()
                self.fout.close()
                exit(0)
        self.ch = self.buffer[-1]
        self.buffer += self.fin.read(1)
        return self.ch

    def read_white(self):
        """检查ch中的字符是否为空格，若是，则反复调用read_char()，直到ch中进入一个非空字符为止"""
        while self.ch.isspace():
            self.read_char()

    def write_token(self, token_type):
        """将识别出来的单词记号写入输出，并刷新token，进入下一轮分析"""
        self.fout.write("<{0}, {1}>\n".format(token_type, self.token))
        self.token = ''
        self.buffer = self.buffer[-1:]
        self.state = INIT

    def handle_errors(self):
        """对发现的词法错误进行相应的处理"""
        # TODO
        self.state = INIT


def main():
    analyer = LexicalAnalyzer(sys.argv[1], 'tokens.txt')
    analyer.analyze()


if __name__ == '__main__':
    main()
