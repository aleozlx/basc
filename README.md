basc
====

基于peglet构造的BASIC示例解析编译器。

BASIC parser and compiler using peglet.

##用法 Usage

```
python basc.py [-p,--parse|-b,--goto] infile
```
*其中infile表示输入bas源文件。
*-p,--parse 表示输出语法解析树（以元组表示）
*-b,--goto 表示混淆器模式，所有循环结构用GOTO语句重写。
*否则把bas源码转换为Python，输出文件在控制台的标准输出中。

infile: Specifies the input BASIC source file.
-p,--parse: To parse file only. (Represented with tuples) 
-b,--goto: Working as a confuser, rewriting loops with GOTO.
By default, basc will convert infile into Python, using stdout for output.

##示例 Example

###测试 Make a test first

```
make testbasc
```

###解析文件 Parse BASIC source file
```
python basc.py example/countdown.bas -p
```

###转换为Python源代码 Compile BASIC source file to Python
```
python basc.py example/sumassert.bas
```

###生成示例 Build all examples
```
make examples
```
查看示例的输出，或运行： 
Then you can either view it or run it!
```
python debug/sumassert.py
```

##参考 Reference

Peglet: https://github.com/darius/peglet

tinybasic: https://github.com/raysohn/tinybasic
