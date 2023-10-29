# 实验一：词法分析程序的设计与实现

## 使用方法

### 方法一：手工编写的词法分析程序

实现语言为python，在当前目录下输入以下命令运行：

```shell
python lexer.py test.c
```

输出文件为 `tokens.txt`

### 方法二：使用FLEX词法分析器生成程序

在当前目录下执行 `makefile`脚本：

```shell
make
```

若要重新执行，先 `clean`：

```shell
make clean
```

再重新 `make`
