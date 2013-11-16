'Asserting eqt suitable for sum of n squared

print "input n:"
input n

let ans="yes"
for i=1 to n
	let s1=0
	let s2=i*(i+1)*(2*i+1)/6
	for j=1 to i
		s1=s1+j*j
	next
	if s1<>s2 then
		ans="no"
		print i," -> ",s2," [OMG! It should be ",s1,"]"
		break
	else
		print i," -> ",s2," [OK]"
	end if
next

print ans
