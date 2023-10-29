%{
#include "y.tab.h"
%}

%%
[0-9]+          { yylval = atoi(yytext); return num; }
[-/+*()\n]      { return yytext[0]; }
.               { return 0; /* end when meet everything else */ }
%%

int yywrap(void) { 
    return 1;
}