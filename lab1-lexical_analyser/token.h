#ifndef TOKEN_H
#define TOKEN_H

typedef enum {
    ID = 2, KW, OP, CS, DL, SP
} TokenType;

static void print_token(int token) {
    static char* token_strs[] = {
        "Identifier", "Keyword", "Operator", "Constant", "Delimiter", "Special"
    };
    printf("%-20s", token_strs[token - 2]);
}

#endif
