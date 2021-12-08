
types = ["int", "boolean"]




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
	return aRes / bRes

binOps = {y : BinOp(x, y, z, w, p) for (x, y, z, w, p) in
		[("AND", "&&", lambda a, b : False if not a() else b(), bbb, 1), 
		 ("OR", "||", lambda a, b : True if a() else b, bbb, 0), 
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
	
		
