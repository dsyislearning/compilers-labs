out: flex_out.txt

flex_out.txt: lexer test.c
	./$< < test.c > flex_out.txt

lexer: lex.yy.c token.h
	gcc -o $@ $<

lex.yy.c: lexer.l
	flex $<

clean:
	rm flex_out.txt lex.yy.c lexer
