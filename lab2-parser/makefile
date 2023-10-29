calc: y.tab.c lex.yy.c
	gcc -o calc y.tab.c lex.yy.c

lex.yy.c: calc.l
	flex calc.l

y.tab.c: calc.y
	bison -vdty calc.y

clean:
	rm -f calc lex.yy.c y.tab.c y.tab.h y.output