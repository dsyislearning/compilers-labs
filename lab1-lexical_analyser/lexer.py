import sys

from states import *
from utils import *

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
            elif self.state == UNDERLINE or self.state == LETTER: # 标识符状态
                self.token += self.ch
                self.read_char()
                if self.ch != '_' and not self.ch.isdigit() and not self.ch.isalpha():
                    if self.token in KW_table: # 查关键字表
                        self.write_token(KW) # 关键字
                    else:
                        self.write_token(ID) # 标识符
                else:
                    self.state = LETTER # 还是标识符状态
            else:
                break
            # elif self.state == DIGIT: # 数字常数状态
            #     self.token += self.ch
            #     self.read_char()
            #     # TODO
            # elif self.state == DOT: # 句点状态
            #     self.token += self.ch
            #     self.read_char()

    def read_char(self):
        """每调用一次，返回forward指向的buffer中的字符，并把它放入变量C中，然后，移动forward，使之指向下一个字符"""
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
        """检查ch中的字符是否为空格，若是，则反复调用get_char()，直到ch中进入一个非空字符为止"""
        while self.ch.isspace():
            self.read_char()
    
    def write_token(self, token_type):
        """将识别出来的单词记号返回给程序，并刷新token，进入下一轮分析"""
        self.fout.write("<{0}, {1}>\n".format(token_type, self.token))
        self.token = ''
        self.buffer = self.buffer[-1:]
        self.state = INIT


def main():
    analyer = LexicalAnalyzer(sys.argv[1], 'tokens.txt')
    analyer.analyze()


if __name__ == '__main__':
    main()
