import sys
from grammar import *

class LRParser(Grammar):
    def __init__(self, filename: str) -> None:
        super().__init__(filename)
        self.TABLE = self.table()

    def table(self) -> dict:
        self.augment()
        self.dfa()
        return self.construct()

    def augment(self) -> None:
        self.N.add('Z')
        self.P['Z'] = [self.S]
        self.S = 'Z'
        self.FIRST = self.first()
        self.FOLLOW = self.follow()

    def dfa(self) -> None:
        self.C = []
        self.C.append(self.closure({('Z', '.' + self.P['Z'][0], '$')}))
        self.dfa_switch_table = []
        while True:
            expanded = False
            for i in range(len(self.C)):
                for X in self.T | self.N:
                    goto_item = self.goto(self.C[i], X)
                    if goto_item and goto_item not in self.C:
                        self.C.append(goto_item)
                        self.dfa_switch_table.append((i, X, len(self.C) - 1))
                        expanded = True
                    elif goto_item in self.C:
                        self.dfa_switch_table.append((i, X, self.C.index(goto_item)))
            if not expanded:
                break

    def closure(self, I: set) -> set:
        J = I
        while True:
            expanded = False
            for item in J.copy():
                if item[1].index('.') < len(item[1]) - 1:
                    B = item[1][item[1].index('.') + 1]
                    if B in self.N:
                        for rhs in self.P[B]:
                            for b in self.first_beta(item[1][item[1].index('.') + 2:], item[2]):
                                original_size = len(J)
                                J.add((B, '.' + rhs, b))
                                if len(J) > original_size:
                                    expanded = True
            if not expanded:
                break
        return J

    def first_beta(self, beta: str, b: str) -> set:
        FIRST = set()
        for x in beta:
            if x in self.T:
                FIRST.add(x)
                break
            elif x in self.N:
                FIRST.update(self.FIRST[x] - set('ε'))
                if 'ε' not in self.FIRST[x]:
                    break
        if len(FIRST) == 0:
            FIRST.add(b)
        return FIRST

    def goto(self, I: set, X: str) -> set:
        J = set()
        for item in I:
            if item[1].index('.') < len(item[1]) - 1 and item[1][item[1].index('.') + 1] == X:
                J.add((item[0], item[1][:item[1].index('.')] + X + '.' + item[1][item[1].index('.') + 2:], item[2]))
        return self.closure(J)

    def print_dfa(self) -> None:
        for i in range(len(self.C)):
            print('I' + str(i) + ':')
            core_set = set()
            for item in self.C[i]:
                core_set.add((item[0], item[1]))
            for core_item in core_set:
                forwards = []
                for item_ in self.C[i]:
                    if core_item == (item_[0], item_[1]):
                        forwards.append(item_[2])
                print(core_item[0] + '->' + core_item[1] + ', ' + '|'.join(forwards))
            print()
        for switch in self.dfa_switch_table:
            print('I' + str(switch[0]) + ' - ' + switch[1] + ' -> I' + str(switch[2]))

    def construct(self) -> list:
        TABLE = [{x: tuple() for x in self.T | self.N | set('$',)} for i in range(len(self.C))]
        for i in range(len(self.C)):
            for switch in self.dfa_switch_table:
                if switch[0] == i:
                    if switch[1] in self.T:
                        TABLE[i][switch[1]] = ('S', switch[2])
                    elif switch[1] in self.N:
                        TABLE[i][switch[1]] = ('G', switch[2])
            for item in self.C[i]:
                if item[1].index('.') == len(item[1]) - 1:
                    if item[0] == 'Z':
                        TABLE[i]['$'] = ('ACC', None)
                    else:
                        for p in self.P[item[0]]:
                            if p == item[1][:-1]:
                                TABLE[i][item[2]] = ('R', (item[0], p))
        return TABLE

    def print_table(self) -> None:
        print('{:^20}'.format(''), end='')
        for T in list(self.T | set('$')) + list(self.N - set('Z')):
            print('{:^20}'.format(T), end='')
        print()
        for i in range(len(self.C)):
            print('{:^20}'.format('I' + str(i)), end='')
            for T in list(self.T | set('$')) + list(self.N - set('Z')):
                print('{:^20}'.format(str(self.TABLE[i][T])), end='')
            print()

    def analyze(self, s: str) -> None:
        s = s + '$'
        state_stack = [0]
        symbol_stack = ['$']
        while True:
            if not self.TABLE[state_stack[-1]][s[0]]:
                raise Exception('Syntax error')
            action = self.TABLE[state_stack[-1]][s[0]][0]
            operation = self.TABLE[state_stack[-1]][s[0]][1]
            if action == 'S':
                state_stack.append(operation)
                symbol_stack.append(s[0])
                s = s[1:]
                print_stack_and_buffer(symbol_stack, s, 'S' + str(operation))
            elif action == 'R':
                lhs = operation[0]
                rhs = operation[1]
                symbol_stack = symbol_stack[:-len(rhs)]
                state_stack = state_stack[:-len(rhs)]
                symbol_stack.append(lhs)
                if not self.TABLE[state_stack[-1]][lhs]:
                    raise Exception('Syntax error')
                state_stack.append(self.TABLE[state_stack[-1]][lhs][1])
                print_stack_and_buffer(symbol_stack, s, lhs + '->' + rhs)
            elif action == 'ACC':
                break
            else:
                raise Exception('Syntax error')

def print_stack_and_buffer(stack: list, buffer: str, action: str) -> None:
    print('{:<15}'.format(''.join(stack)), end='')
    print('{:>15}'.format(buffer), end='{:>5}'.format(''))
    print('{:<20}'.format(action))

if __name__ == '__main__':
    # parser = LRParser('valid.txt')
    parser = LRParser('valid.txt')
    # print(parser)
    # parser.print_dfa()
    # parser.print_table()
    parser.analyze(input())
