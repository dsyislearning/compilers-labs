%{
#include <stdio.h>
int yylex(void);
void yyerror(const char* msg) {}
%}

%token num

%%
E   :   E '+' T { printf("E->E+T\n"); }
    |   E '-' T { printf("E->E-T\n"); }
    |   T       { printf("E->T\n"); }
    ;

T   :   T '*' F { printf("T->T*F\n"); }
    |   T '/' F { printf("T->T/F\n"); }
    |   F       { printf("T->F\n"); }
    ;

F   :   '(' E ')'   { printf("F->(E)\n"); }
    |   num         { printf("F->num\n"); }
    ;
%%

int main() {
    return yyparse();
}