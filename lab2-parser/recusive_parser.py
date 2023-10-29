class Parser:
    def __init__(self, s):
        self.s = s + '$'

    def procE(self):
        self.procT()
        print('E->T')
        if self.s[0] == '+':
            self.s = self.s[1:]
            print('E->E+T')
            self.procE()
        elif self.s[0] == '-':
            self.s = self.s[1:]
            print('E->E-T')
            self.procE()
    
    def procT(self):
        self.procF()
        print('T->F')
        if self.s[0] == '*':
            self.s = self.s[1:]
            print('T->T*F')
            self.procT()
        elif self.s[0] == '/':
            self.s = self.s[1:]
            print('T->T/F')
            self.procT()

    def procF(self):
        if self.s[0] == '(':
            self.s = self.s[1:]
            self.procE()
            if self.s[0] == ')':
                self.s = self.s[1:]
                print('F->(E)')
            else:
                raise Exception('Error')
        elif self.s[0] == 'n':
            self.s = self.s[1:]
            print('F->n')
        else:
            raise Exception('Error')

if __name__ == '__main__':
    parser = Parser(input())
    parser.procE()
