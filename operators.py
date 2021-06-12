from dictionary import lookup1
from dictionary import lookup2

def load_archives(val):
	#print(val[0], val[1])
	val[0] = lookup1(val[0])
	val[1] = lookup2(val[1])
	#print(val[0], val[1])

	return val