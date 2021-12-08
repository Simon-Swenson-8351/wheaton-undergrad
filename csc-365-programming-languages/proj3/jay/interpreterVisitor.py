
from jay_ast import NodeVisitor 

class JayRuntimeError(Exception):
    def __init__(self, description):
        self.description = description
    def __str__(self):
        return repr(self.value)


class InterpreterVisitor(NodeVisitor):
    
    #def __init__(self):
        
    # I put these in the visitor for program
    # because 
    def visit_Program(self, node):
        self.result = 0
        self.sigma = {}
        try :
            for s in node.main.stmts :
                self.visit(s)
        except JayRuntimeError as e:
            print 'Jay runtime exception: ' + e.description
    
    # skip and block can be inherited from NodeVisitor
    def visit_Assignment(self, node):
        self.visit(node.expr)
        self.sigma[node.target] = self.result
        
    def visit_Conditional(self, node):
        self.visit(node.cond)
        if self.result :
            self.visit(node.thenStmt)
        else :
            self.visit(node.elseStmt)
    
    def visit_Loop(self, node):
        while True :
            self.visit(node.guard)
            if self.result :
                self.visit(node.body)
            else :
                break
    
    def visit_Print(self, node):
        self.visit(node.expr)
        print self.result
    
    def visit_Variable(self, node):
        self.result = self.sigma[node.id]
        
    def visit_IntLitExpr(self, node):
        self.result = node.val
        
    def visit_BoolLitExpr(self, node):
        self.result = node.val

    def visitResult(self, node):
        self.visit(node)
        return self.result
        
    def visit_BinaryExpr(self, node):
#        self.result = node.op.operation(lambda : (self.visit(node.expr1), 
#                          lambda : self.visit(node.expr2))
        self.result = node.op.operation(lambda : self.visitResult(node.expr1), 
                                        lambda : self.visitResult(node.expr2))

        
    def visit_UnaryExpr(self, node):
        self.visit(node.expr)
        if node.op == "-" :
            self.result = - self.result
        elif node.op == "!" :
            self.result = not self.result
        else :
            print ":("
        