class Grammar:
    def __init__(self, filename: str) -> None:
        self.N = set()
        self.T = set()
        self.S = ''
        self.P = {}
        with open(filename, 'r', encoding='utf-8') as f:
            self.N = set(f.readline().split())
            self.T = set(f.readline().split())
            self.S = f.readline().strip()
            for line in f:
                line = line.strip()
                if line == '':
                    continue
                lhs, rhs = line.split('->')
                lhs = lhs.strip()
                rhs = rhs.strip().split('|')
                if lhs not in self.P:
                    self.P[lhs] = []
                self.P[lhs] += rhs
        self.FIRST = self.first()
        self.FOLLOW = self.follow()

    def first(self) -> dict:
        """求语法所有符号的 FIRST 集

        Returns:
            dict: 语法所有符号的 FIRST 集，键为符号，值为符号的 FIRST 集
        """
        FIRST = {x: set() for x in self.N | self.T}
        while True:
            expanded = False
            for X in self.N | self.T:
                original_size = len(FIRST[X])
                if X in self.T:
                    FIRST[X].add(X)
                elif X in self.N:
                    for rhs in self.P[X]:
                        if rhs[0] in self.T or rhs[0] == 'ε':
                            FIRST[X].add(rhs[0])
                        elif rhs[0] in self.N and X != rhs[0]:
                            FIRST[X].update(FIRST[rhs[0]] - set('ε'))
                            flag = False
                            for i in range(len(rhs) - 1):
                                if 'ε' in FIRST[rhs[i]]:
                                    flag = True
                                    FIRST[X].update(FIRST[rhs[i + 1]] - set('ε'))
                                else:
                                    flag = False
                                    break
                            if flag:
                                FIRST[X].add('ε')
                if len(FIRST[X]) > original_size:
                    expanded = True
            if not expanded:
                break
        return FIRST

    def first_alpha(self, alpha: str) -> set:
        """求某个符号串的 FIRST 集

        Args:
            alpha (str): 符号串

        Returns:
            set: 符号串的 FIRST 集，包含 'ε'
        """
        FIRST = set()
        if alpha == 'ε':
            FIRST.add('ε')
        else:
            flag = True
            for x in alpha:
                if x in self.T:
                    FIRST.add(x)
                    break
                elif x in self.N:
                    FIRST.update(self.FIRST[x] - set('ε'))
                    if 'ε' not in self.FIRST[x]:
                        flag = False
                        break
            if flag:
                FIRST.add('ε')
        return FIRST

    def follow(self) -> dict:
        """求语法所有非终结符的 FOLLOW 集

        Returns:
            dict: 语法所有非终结符的 FOLLOW 集，键为非终结符，值为非终结符的 FOLLOW 集
        """
        FOLLOW = {x: set() for x in self.N}
        FOLLOW[self.S].add('$')
        while True:
            expanded = False
            for A in self.N:
                original_size = sum([len(FOLLOW[X]) for X in FOLLOW])
                for rhs in self.P[A]:
                    if rhs == 'ε':
                            FOLLOW[A].add('$')
                    else:
                        for i in range(len(rhs)):
                            if rhs[i] in self.N:
                                if i < len(rhs) - 1:
                                    if rhs[i + 1] in self.T:
                                        FOLLOW[rhs[i]].add(rhs[i + 1])
                                    elif rhs[i + 1] in self.N:
                                        FIRST_alpha = self.first_alpha(rhs[i + 1:])
                                        FOLLOW[rhs[i]].update(FIRST_alpha - set('ε'))
                                        if 'ε' in FIRST_alpha:
                                            FOLLOW[rhs[i]].update(FOLLOW[A])
                                elif i == len(rhs) - 1:
                                    FOLLOW[rhs[i]].update(FOLLOW[A])
                if sum([len(FOLLOW[X]) for X in FOLLOW]) > original_size:
                    expanded = True
            if not expanded:
                break
        return FOLLOW

    def __str__(self) -> str:
        s = 'N: ' + ' '.join(self.N) + '\n'
        s += 'T: ' + ' '.join(self.T) + '\n'
        s += 'S: ' + self.S + '\n'
        s += 'P:\n'
        for lhs in self.P:
            for rhs in self.P[lhs]:
                s += lhs + ' -> ' + rhs + '\n'
        s += 'FIRST:\n'
        for x in self.FIRST:
            s += x + ': ' + ' '.join(self.FIRST[x]) + '\n'
        s += 'FOLLOW:\n'
        for x in self.FOLLOW:
            s += x + ': ' + ' '.join(self.FOLLOW[x]) + '\n'
        return s
