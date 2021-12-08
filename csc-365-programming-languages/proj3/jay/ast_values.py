from interpreterVisitor import JayRuntimeError 


types = ["int", "boolean"]



#class TypeDec :
#	def __init__(self, val):		
#		self.val = val
#	
#	@classvariable
#	def INT = TypeDec(0)
#	
#	@classvariable
#	def BOOL = TypeDec(1)

class BinOp(object) :
	def __init__(self, name, representation, operation, tys, prec):
		self.name = name
		self.representation = representation
		self.operation = operation
		self.tys = tys
		self.prec = prec

iii = ("int", "int", "int")
iib = ("int", "int", "boolean")
bbb = ("boolean", "boolean", "boolean")

def safeDiv(a, b) :
	aRes = a()
	bRes = b()
	if bRes == 0 :
		raise JayRuntimeError("Division by zero")
	return aRes / bRes

binOps = {y : BinOp(x, y, z, w, p) for (x, y, z, w, p) in
		[("AND", "&&", lambda a, b : False if not a() else b(), bbb, 1), 
		 ("OR", "||", lambda a, b : True if a() else b(), bbb, 0), 
		 ("PLUS", "+", lambda a, b : a() + b(), iii, 3), 
		 ("MINUS", "-", lambda a, b : a() - b(), iii, 3), 
		 ("STAR", "*", lambda a, b : a() * b(), iii, 4),		 
		 ("SLASH", "/", safeDiv, iii, 4), 
		 ("LT", "<", lambda a, b: a () < b(), iib, 2), 
		 ("LTEQ", "<=", lambda a, b: a() <= b(), iib, 2), 
		 ("GT", ">", lambda a, b: a() > b(), iib, 2), 
		 ("GTEQ", ">=", lambda a, b: a() >= b(), iib, 2),
		 ("EQ", "==", lambda a, b: a() == b(), iib, 2), 
		 ("NEQ", "!=", lambda a, b: a() != b(), iib, 2)] }
	
#class BinOp:
#	def __init__(self, op) :
#		self.val = op
		
#	@classvariable
#	def OR = TypeDec("||")
	
		