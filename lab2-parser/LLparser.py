import sys
from grammar import *

class LLParser(Grammar):
    def __init__(self, filename: str) -> None:
        super().__init__(filename)
        self.TABLE = self.table()
    
    def table(self) -> dict:
        """构造 LL(1) 分析表

        Returns:
            dict: LL(1) 分析表，键为非终结符，值为该非终结符的表项，表项为一个字典，键为终结符，值为产生式
        """
        TABLE = {N: {T: '' for T in self.T | set('$')} for N in self.N} # LL(1) 文法，不含多重定义的表项
        for lhs in self.N:
            for rhs in self.P[lhs]:
                if rhs == 'ε':
                    TABLE[lhs]['$'] = rhs
                    for T in self.FOLLOW[lhs]:
                        if not TABLE[lhs][T]:
                            TABLE[lhs][T] = rhs
                else:
                    for T in self.FIRST[rhs[0]]:
                        TABLE[lhs][T] = rhs
                    if 'ε' in self.FIRST[rhs[0]]:
                        for T in self.FOLLOW[lhs]:
                            TABLE[lhs][T] = rhs
        return TABLE
    
    def print_table(self) -> None:
        print('{:^10}'.format(''), end='')
        for T in self.T | set('$'):
            print('{:^10}'.format(T), end='')
        print()
        for N in self.N:
            print('{:^10}'.format(N), end='')
            for T in self.T | set('$'):
                print('{:^10}'.format(self.TABLE[N][T]), end='')
            print()

    def analyze(self, s: str) -> None:
        """语法分析符号串 s

        Args:
            s (str): 待分析的符号串

        Raises:
            Exception: 语法错误，栈顶终结符与缓冲区首符号不匹配
            Exception: 语法错误，栈顶非终结符无法推导出缓冲区首符号
        """
        stack = ['$', self.S]
        buffer = s + '$'
        while True:
            X = stack[-1]
            if X in self.T or X == '$':
                if X == buffer[0]:
                    stack.pop()
                    buffer = buffer[1:]
                else:
                    raise Exception('Syntax Error')
            else:
                if self.TABLE[X][buffer[0]]:
                    if self.TABLE[X][buffer[0]] == 'ε':
                        stack.pop()
                        self.print_stack_and_buffer(stack, buffer, X + '->ε')
                    else:
                        stack.pop()
                        stack += list(self.TABLE[X][buffer[0]])[::-1]
                        self.print_stack_and_buffer(stack, buffer, X + '->' + self.TABLE[X][buffer[0]])
                else:
                    raise Exception('Syntax Error')
            if X == '$':
                break
    
    def print_stack_and_buffer(self, stack: list, buffer: str, action: str) -> None:
        print('{:<15}'.format(''.join(stack)), end='')
        print('{:>15}'.format(buffer), end='{:>5}'.format(''))
        print('{:<20}'.format(action))

def main():
    parser = LLParser('no_recursion.txt')
    # print(parser)
    # parser.print_table()
    parser.analyze(input())

if __name__ == "__main__":
    main()
