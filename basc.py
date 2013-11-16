# -*- coding: utf-8 -*-
import argparse
import peglet
import re
import logging
import random

mydebug = logging.getLogger("basc.debug")
mydebug.addHandler(logging.StreamHandler())
def debug(o):
	"""输出调试信息到basc.debug中。
	Log something into basc.debug for debugging purposes."""
	mydebug.warning(str(o))

class BASICParser(object):
	"""BASIC 语法解析器"""
	def __init__(self):
		"""构造函数，定义了“语法”和“动作”。
		Initialize Actions and Grammar."""
		kwargs = { 
			#“动作”，可以应用于匹配到的语法结构，来转换或构造可以表示其语法结构的元组。 
			#Here are Actions, which can be applied to regex matches.
			"debug": lambda t: "<debug "+t+">",
			"escape": re.escape,
			"hug": peglet.hug,
			"join": peglet.join,
			"mk_if_else": self.mk_if_else,
			"mk_do_loop_while": self.mk_do_loop_while,
			"mk_let": lambda a,b: ('let',a,b),
			"mk_label": lambda t: ('label',t),
			"quote": lambda t:'"%s"' % t,
		}
		#从bas.re读取语法的定义
		#Get BASIC grammar from "bas.re".
		with open('bas.re') as f: self.grammar=f.read()
		self.parser = peglet.Parser(self.grammar, **kwargs)

	
	def __call__(self, program):
		return self.parser(program)

	def mk_if_else(self,*ts):
		"""构造表示if-else结构的元组。
		Make a tuple representing if-else grammar."""
		ielse=ts.index('else')
		return ('if_else',ts[0],ts[1:ielse],ts[ielse+1:])

	def mk_do_loop_while(self,*ts):
		"""构造表示do-loop-while结构的元组。
		Make a tuple representing do-loop-while grammar."""
		return ('dlwhile',ts[-1][1],ts[1:-1])


class BASIC2PythonCompiler(object):
	"""BASIC语言转Python语言，作为向更高级语言转换的示例。
	This is an example converting BASIC to a higher-level programming language, namely Python."""
	def __init__(self,indent=0):
		self.parse_tree = None
		self.hmap = {
			#语法关键词到特定语法转换方法的映射。
			#dict that maps from keyword to a grammar handler.
			"break":self.break_stmt_Handler,
			"continue":self.continue_stmt_Handler,
			"print":self.prt_stmt_Handler,
			"input":self.impt_stmt_Handler,
			"label":self.label_Handler,
			"let":self.let_stmt_Handler,
			"goto":self.goto_stmt_Handler,
			"if":self.if_block_Handler,
			"if_else":self.if_else_block_Handler,
			"do":self.infini_loop_Handler,
			"for":self.for_block_Handler,
			"while":self.while_block_Handler,
			"dlwhile":self.dlwhile_block_Handler,
		}
		#当前上下文缩进级别
		#Initial indentation of this context.
		self.indent=indent

	def __call__(self, parse_tree):
		self.parse_tree = parse_tree
		for line in self.parse_tree:
			if type(line[0]) is str:
				self.hmap[line[0]](line)
			elif type(line[0]) is tuple:
				self.hmap[line[0][0]](line)

	def label_Handler(self,stmt):
		raise Exception('syntax err: LABEL not allowed')

	def break_stmt_Handler(self,stmt):
		self.out('break')

	def continue_stmt_Handler(self,stmt):
		self.out('continue')

	def prt_stmt_Handler(self,stmt):
		self.out('print '+','.join((self.convert(expr) for expr in stmt[1:])))

	def impt_stmt_Handler(self,stmt):
		var_vec=stmt[1:]
		for var in var_vec:
			self.out(var+'=input()')

	def let_stmt_Handler(self,stmt):
		let_kw,lvalue,rvalue=stmt
		self.out(lvalue+'='+self.convert(rvalue))

	def goto_stmt_Handler(self,stmt):
		raise Exception('syntax err: GOTO not allowed')

	def if_block_Handler(self,stmt):
		if_kw,expr=stmt[0]
		self.out('if '+self.convert(expr)+':')
		blockc=self.subcompiler()
		blockc(stmt[1:])

	def if_else_block_Handler(self,stmt):
		header,ifstmt,if_block,else_block=stmt
		self.out('if '+self.convert(ifstmt[1])+':')
		blockc=self.subcompiler()
		blockc(if_block)
		self.out('else:')
		blockc(else_block)

	def infini_loop_Handler(self,stmt):
		self.out('while True:')
		blockc=self.subcompiler()
		blockc(stmt[1:])

	def while_block_Handler(self,stmt):
		while_kw,expr=stmt[0]
		self.out('while '+self.convert(expr)+':')
		blockc=self.subcompiler()
		blockc(stmt[1:])

	def dlwhile_block_Handler(self,stmt):
		while_kw,expr,loopbody=stmt
		self(loopbody)
		self.out('while '+self.convert(expr)+':')
		blockc=self.subcompiler()
		blockc(loopbody)

	def for_block_Handler(self,stmt):
		for_stmt=stmt[0]
		if(len(for_stmt)==4):
			for_kw,var,beginexpr,endexpr=for_stmt
			self.out('for '+var+' in xrange('+self.convert(beginexpr)+','+self.convert(endexpr)+'+1):')
		else:
			for_kw,var,beginexpr,endexpr,stepexpr=for_stmt
			self.out('for '+var+' in xrange('+self.convert(beginexpr)+','+self.convert(endexpr)+'+1,'+self.convert(stepexpr)+'):')
		blockc=self.subcompiler()
		blockc(stmt[1:])

	def out(self,raw):
		"""输出代码
		Output target code."""
		print '\t'*self.indent+raw

	def subcompiler(self):
		"""递归处理代码块
		Recursicely process the code blocks"""
		return BASIC2PythonCompiler(self.indent+1)

	def convert(self,sexpr):
		"""转换表达式
		Convert the expression into a pythonic one."""
		return sexpr.replace('=','==').replace('<>','!=')

class BASIC2GOTOAbuserCompiler(object):
	"""BASIC语言转“滥用GOTO”的BASIC语言，作为向更低级语言转换的示例。
	事实上这样的程序可以算是“混淆器”，比如你需要保护宏的源代码，这也不失为一种方法。
	另外这个示例对实现正真的编译器有更多的帮助。
	This is an example converting BASIC to a lower-level programming language. 
	One step closer to assembly if you are struggling to forge your first compiler, like a real one."""
	def __init__(self,loopcontext=None,labels=[]):
		self.parse_tree = None
		self.hmap = {
			"break":self.break_stmt_Handler,
			"continue":self.continue_stmt_Handler,
			"print":self.prt_stmt_Handler,
			"input":self.impt_stmt_Handler,
			"label":self.label_Handler,
			"let":self.let_stmt_Handler,
			"goto":self.goto_stmt_Handler,
			"if":self.if_block_Handler,
			"if_else":self.if_else_block_Handler,
			"do":self.infini_loop_Handler,
			"for":self.for_block_Handler,
			"while":self.while_block_Handler,
			"dlwhile":self.dlwhile_block_Handler,
		}
		self.loopcontext=loopcontext
		self.labels=labels

	def newLabel(self):
		"""创建随机标签。
		Generalize a random label."""
		rrr='QWERTYUIOPASDFGHJKLZXCVBNMasdfghjklqwertyuiopzxcvbnm'
		while True:
			z=''.join((random.choice(rrr) for i in range(8)))
			if not z in self.labels: 
				self.labels.append(z)
				break
		return z

	def __call__(self, parse_tree):
		self.parse_tree = parse_tree
		for line in self.parse_tree:
			if type(line[0]) is str:
				self.hmap[line[0]](line)
			elif type(line[0]) is tuple:
				self.hmap[line[0][0]](line)

	def label_Handler(self,stmt):
		label_kw,lname=stmt
		self.out(lname+':')

	def break_stmt_Handler(self,stmt):
		if self.loopcontext:
			break_lname,continue_lname=self.loopcontext
			self.out('goto '+break_lname)
		else: raise Exception('syntax err: BREAK')

	def continue_stmt_Handler(self,stmt):
		if self.loopcontext:
			break_lname,continue_lname=self.loopcontext
			self.out('goto '+continue_lname)
		else: raise Exception('syntax err: CONTINUE')

	def prt_stmt_Handler(self,stmt):
		self.out('print '+','.join((self.convert(expr) for expr in stmt[1:])))

	def impt_stmt_Handler(self,stmt):
		self.out('input '+','.join(stmt[1:]))

	def let_stmt_Handler(self,stmt):
		let_kw,lvalue,rvalue=stmt
		self.out('let '+lvalue+'='+self.convert(rvalue))

	def goto_stmt_Handler(self,stmt):
		goto_kw,lname=stmt
		self.out('goto '+lname)

	def if_block_Handler(self,stmt):
		if_kw,expr=stmt[0]
		self.out('if '+self.convert(expr)+' then')
		blockc=self.nonloopcontexthandler()
		blockc(stmt[1:])
		self.out('end if')

	def if_else_block_Handler(self,stmt):
		header,ifstmt,if_block,else_block=stmt
		self.out('if '+self.convert(ifstmt[1])+' then')
		blockc=self.nonloopcontexthandler()
		blockc(if_block)
		self.out('else')
		blockc(else_block)
		self.out('end if')

	def infini_loop_Handler(self,stmt):
		loop_begin=self.newLabel()
		loop_end=self.newLabel()
		self.out(loop_begin+':')
		blockc=self.loopcontexthandler(loop_begin,loop_end)
		blockc(stmt[1:])
		self.out(loop_end+':')

	def while_block_Handler(self,stmt):
		loop_begin=self.newLabel()
		loop_end=self.newLabel()
		self.out(loop_begin+':')
		while_kw,expr=stmt[0]
		self.out('if '+self.convert(expr)+' then')
		blockc=self.loopcontexthandler(loop_begin,loop_end)
		blockc(stmt[1:])
		self.out('goto '+loop_begin)
		self.out('end if')
		self.out(loop_end+':')

	def dlwhile_block_Handler(self,stmt):
		loop_begin=self.newLabel()
		loop_end=self.newLabel()
		self.out(loop_begin+':')
		while_kw,expr,loopbody=stmt
		blockc=self.loopcontexthandler(loop_begin,loop_end)
		blockc(loopbody)
		self.out('if '+self.convert(expr)+' then')
		self.out('goto '+loop_begin)
		self.out('end if')
		self.out(loop_end+':')


	def for_block_Handler(self,stmt):
		for_stmt=stmt[0]
		loop_begin=self.newLabel()
		loop_end=self.newLabel()
		blockc=self.loopcontexthandler(loop_begin,loop_end)
		if(len(for_stmt)==4): for_kw,var,beginexpr,endexpr=for_stmt
		else: for_kw,var,beginexpr,endexpr,stepexpr=for_stmt
		self.out('let '+var+'='+self.convert(beginexpr))
		self.out(loop_begin+':')
		self.out('if '+var+'<>('+self.convert(endexpr)+')'+' then')
		blockc(stmt[1:])
		if(len(for_stmt)==4): self.out('let '+var+'='+var+'+1')
		else: self.out('let '+var+'='+var+'+'+self.convert(stepexpr))
		self.out('goto '+loop_begin)
		self.out('else')
		blockc(stmt[1:])
		self.out('end if')
		self.out(loop_end+':')

	def out(self,raw):
		print raw

	def subcompiler(self): 
		b2gac=BASIC2GOTOAbuserCompiler()
		b2gac.labels=self.labels
		return b2gac

	def loopcontexthandler(self,loopbegin,loopend):
		"""循环上下文处理方法，支持处理break和continue语句。
		A special subcompiler handling loop context, where 'break' and 'continue' require good interpretion."""
		sc=self.subcompiler()
		sc.loopcontext=(loopend,loopbegin)
		return sc

	def nonloopcontexthandler(self):
		"""非循环上下文处理方法，继承现有循环上下文。
		A special subcompiler handling non-loop context."""
		return self.loopcontexthandler(self.loopcontext[1],self.loopcontext[0])

	def convert(self,sexpr):
		return sexpr


if __name__ == "__main__":
	arg_parser = argparse.ArgumentParser()
	arg_parser.add_argument("path", nargs='?')
	arg_parser.add_argument("-p", "--parse", action="store_true")
	arg_parser.add_argument("-b", "--goto", action="store_true")
	args = arg_parser.parse_args()
	with open(args.path, "r") as f: 
		program = f.read().encode("ascii", "ignore")
		mypaser=BASICParser()
		if args.parse:
			for line in mypaser(program): print line
		elif args.goto:
			mycompiler=BASIC2GOTOAbuserCompiler()
			mycompiler(mypaser(program))
		else:
			mycompiler=BASIC2PythonCompiler()
			mycompiler(mypaser(program))
