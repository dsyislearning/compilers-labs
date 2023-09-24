%{
#include "token.h"
#define SKIPCHAR 100
int lines = 0;
int characters = 0;
int ID_num = 0;
int KW_num = 0;
int OP_num = 0;
int CS_num = 0;
int DL_num = 0;
int SP_num = 0;
void init_scanner();
void print_info();
void lex_error(char* msg, int line);
%}

%%

[\n]                    { lines++; characters++;  }
[ \t\r\a]+              { characters += yyleng; /* 跳过所有空白字符 */}
"//"[^\n]*              { characters += yyleng; /* 跳过单行注释 */}
"/*".*"*/"              { characters += yyleng; /* 跳过多行注释 */}

"auto"                  { KW_num++; return KW; }
"break"                 { KW_num++; return KW; }
"case"                  { KW_num++; return KW; }
"char"                  { KW_num++; return KW; }
"const"                 { KW_num++; return KW; }
"continue"              { KW_num++; return KW; }
"default"               { KW_num++; return KW; }
"do"                    { KW_num++; return KW; }
"double"                { KW_num++; return KW; }
"else"                  { KW_num++; return KW; }
"enum"                  { KW_num++; return KW; }
"extern"                { KW_num++; return KW; }
"float"                 { KW_num++; return KW; }
"for"                   { KW_num++; return KW; }
"goto"                  { KW_num++; return KW; }
"if"                    { KW_num++; return KW; }
"inline"                { KW_num++; return KW; }
"int"                   { KW_num++; return KW; }
"long"                  { KW_num++; return KW; }
"register"              { KW_num++; return KW; }
"restrict"              { KW_num++; return KW; }
"return"                { KW_num++; return KW; }
"short"                 { KW_num++; return KW; }
"signed"                { KW_num++; return KW; }
"sizeof"                { KW_num++; return KW; }
"static"                { KW_num++; return KW; }
"struct"                { KW_num++; return KW; }
"switch"                { KW_num++; return KW; }
"typedef"               { KW_num++; return KW; }
"union"                 { KW_num++; return KW; }
"usigned"               { KW_num++; return KW; }
"void"                  { KW_num++; return KW; }
"volatile"              { KW_num++; return KW; }
"while"                 { KW_num++; return KW; }
"_Bool"                 { KW_num++; return KW; }
"_Complex"              { KW_num++; return KW; }
"_Imaginary"            { KW_num++; return KW; }

[_a-zA-Z][_a-zA-Z0-9]*  { ID_num++; return ID; }

[*/+-]                  { OP_num++; return OP; }
"="                     { OP_num++; return OP; }
"++"                    { OP_num++; return OP; }
"--"                    { OP_num++; return OP; }
"%"                     { OP_num++; return OP; }
"%="                    { OP_num++; return OP; }
[~|&^]                  { OP_num++; return OP; }
">"                     { OP_num++; return OP; }
">="                    { OP_num++; return OP; }
">>"                    { OP_num++; return OP; }
">>="                   { OP_num++; return OP; }
"<"                     { OP_num++; return OP; }
"<="                    { OP_num++; return OP; }
"<<"                    { OP_num++; return OP; }
"<<="                   { OP_num++; return OP; }
"&&"                    { OP_num++; return OP; }
"&="                    { OP_num++; return OP; }
"||"                    { OP_num++; return OP; }
"|="                    { OP_num++; return OP; }
"!"                     { OP_num++; return OP; }
"!="                    { OP_num++; return OP; }
"->"                    { OP_num++; return OP; }
"."                     { OP_num++; return OP; }

[-+][0-9]+                              { CS_num++; return CS; /* 十进制 */ }
0[0-7]+                                 { CS_num++; return CS; /* 八进制 */ }
0[xX][0-9a-fA-F]+                       { CS_num++; return CS; /* 十六进制 */ }
[-+]?0\.[0-9]+                          { CS_num++; return CS; /* 小于1的浮点数 */ }
[-+]?[1-9][0-9]*\.[0-9]+                { CS_num++; return CS; /* 大于等于1的浮点数 */ }
[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?  { CS_num++; return CS; /* 科学记数法 */ }

'([^'\\]|[\\.])'                    { CS_num++; return CS; /* 字符常量 */ }
\042[^\042\n]*\042                  { CS_num++; return CS; /* 字符串常量 */ }

"("                                 { DL_num++; return DL; }
")"                                 { DL_num++; return DL; }
"["                                 { DL_num++; return DL; }
"]"                                 { DL_num++; return DL; }
"{"                                 { DL_num++; return DL; }
"}"                                 { DL_num++; return DL; }
","                                 { DL_num++; return DL; }
";"                                 { DL_num++; return DL; }

(.)                                 { SP_num++; return SP; }

<<EOF>>                             { return 0; }

%%

int main(int argc, char* argv[]) {
    int token;
    init_scanner();
    while (token = yylex()) {
        if (token != 100) {
            print_token(token);
            puts(yytext);
            characters += yyleng;
        }
    }
    print_info();
    return 0;
}

void init_scanner() {
    printf("%-20s%s\n", "TOKEN-TYPE", "TOKEN-VALUE");
    printf("-------------------------------------------------\n");
}

void print_info() {
    printf("-------------------------------------------------\n");
    printf("Lines: %d, Characters: %d\n", lines, characters);
    printf("Identifiers: %d\nKeywords: %d\nOperators: %d\nConstants: %d\nDelimiters: %d\nSpecial Symbols: %d\n",
            ID_num, KW_num, OP_num, CS_num, DL_num, SP_num);
}

void lex_error(char* msg, int line) {
    printf("\nError at line %-3d: %s\n\n", line, msg);
}

int yywrap(void) {
    return 1; // 只对一个源文件进行词法分析
}
