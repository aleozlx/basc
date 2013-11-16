source			= blocks
blocks			= block blocks | 
block			= if_block | for_block | do_block 
				| break_stmt | ctn_stmt | prt_stmt | impt_stmt | let_stmt | goto_stmt
				| comment | label | void 

for_block		= for_stmt blocks next_stmt 														hug
				| for_stmt2 blocks next_stmt 														hug
do_block 		= do_stmt blocks loop_stmt 															hug
				| while_stmt blocks loop_stmt 														hug
				| do_stmt blocks while_stmt 														mk_do_loop_while
if_block 		= if_stmt blocks end_if_stmt 														hug
				| if_stmt blocks else_stmt blocks end_if_stmt 										mk_if_else

for_stmt		= idt_idpt (for) __ varnom _ \= _ expr __ (?:to) __ expr endl 						hug
for_stmt2		= idt_idpt (for) __ varnom _ \= _ expr __ (?:to) __ expr __ (?:step) __ expr endl 	hug
next_stmt		= idt_idpt (?:next)(?:[\x20\t]+[A-Za-z_][A-Za-z0-9_]*|) endl
break_stmt		= idt_idpt (break) endl 															hug
ctn_stmt		= idt_idpt (continue) endl 															hug
prt_stmt		= idt_idpt (print) _ expr_list endl 												hug
impt_stmt		= idt_idpt (input) _ var_list endl 													hug
let_stmt 		= idt_idpt (let) _ varnom _ (?:=) _ rvalue endl 									hug
				| idt_idpt varnom _ (?:=) _ rvalue endl 											mk_let
label 			= idt_idpt varnom _ (?::) endl 														mk_label
comment 		= idt_idpt (?:\').* endl 															
goto_stmt 		= idt_idpt (goto) __ varnom endl 													hug
do_stmt			= idt_idpt (do) endl 																hug
loop_stmt		= idt_idpt (?:loop) endl
while_stmt 		= idt_idpt (?:do|loop) __ (while) __ expr endl 										hug
if_stmt			= idt_idpt (if) __ expr __ (?:then) endl 											hug
else_stmt		= idt_idpt (else) endl 																
end_if_stmt 	= idt_idpt (?:end) __ (?:if) endl

varnom			= ([A-Za-z_][A-Za-z0-9_]*)
num				= (\-\d+) | (\d+)
var_list 		= varnom _ , _ var_list
				| varnom
expr_list 		= expr _ , _ expr_list 
				| expr 
				| str _ , _ expr_list
				| str
expr 			= term _ binop _ expr 																join
				| term _ relop _ expr 																join
				| term
term 			= varnom
				| num
				| l_paren _ expr _ r_paren 															join
rvalue			= expr
				| str
str				= " chars " _																		join quote
				| ' sqchars ' _																		join
chars			= char chars 
				|
sqchars			= sqchar sqchars 
				|

char			= ([^\x00-\x1f"\\]) 
				| esc_char
sqchar			= ([^\x00-\x1f'\\]) 
				| esc_char
esc_char		= \\(['"/\\])
				| \\([bfnrt])																		escape
relop 			= (<>|><|<=|<|>=|>|\=) 				
binop 			= (\+|\-|\*|\/)
l_paren 		= (\()
r_paren 		= (\))
idt_idpt		= ^[\x20\t]*
void			= ^\s*\n
endl			= \s*\n
_				= [\x20\t]*
__				= [\x20\t]+
