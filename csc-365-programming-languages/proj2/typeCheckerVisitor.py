from jay_ast import NodeVisitor 

class TypeCheckerVisitor(NodeVisitor):
    
    def visit_Program(self, node):
        self.typeMap = {}
        self.uninitialized = set([])
        self.errors = 0
        for d in node.decls :
            self.visit(d)
        for s in node.main.stmts :
            self.visit(s)

        if self.errors == 0 :
            print "Program types correctly."
        else :
            print "%s type errors." % self.errors
            
    
    def visit_Declaration(self, node):
        for v in node.ids :
            pass  # add code here


    ## for statements
                
    def visit_Assignment(self, node):

        # post-condition: self.currentType is the type of the
        # right hand side of this assignment if it types correctly
        # (otherwise, it's ERR)
        self.visit(node.expr)
        
        # add code here
   

    def visit_Conditional(self, node):
        self.visit(node.cond)
        if self.currentType != "ERR" and self.currentType != "boolean" :
            print "Wrong type for conditional test. Needs: boolean. Found: " + self.currentType
            self.errors += 1
        
        orig = self.uninitialized
        
        self.uninitialized = set(orig)
        self.visit(node.thenStmt)
        ifBranch = self.uninitialized
        
        self.uninitialized = set(orig)
        self.visit(node.elseStmt)
        elseBranch = self.uninitialized

        # not the most efficient way (could do self.uninitiaized.add(ifBranch))
        # but most readable intent
        self.uninitialized = ifBranch | elseBranch
        
    def visit_Loop(self, node):
        # post-condition: self.currentType is the type of the
        # guard expression (otherwise, it's ERR)
        self.visit(node.guard)

        # add code here

        
    # prints should be hit by inherited methods
        
    ##  for expressions
        
    def visit_Variable(self, node):
        #print "3 uninitialized: " + str(self.uninitialized)
         
        if not node.id in self.typeMap :
            print node.id + " undeclared."
            self.errors += 1
        else : 
            if node.id in self.uninitialized :
                print node.id + " might not be initialized"
                self.errors += 1
            self.currentType = self.typeMap[node.id]
    
    def visit_IntLitExpr(self, node):
        self.currentType = "int"
        
    def visit_BoolLitExpr(self, node):
        self.currentType = "boolean"
    
    def visit_BinaryExpr(self, node):
        self.currentTYpe = "ERR" # delete this line

        #add code here
        
    
    def visit_UnaryExpr(self, node):
        self.visit(node.expr)
        if node.op == "!" :
            if not self.currentType in ["ERR", "boolean"] :
                print "Operand does not match for operator !. Needs: boolean. Found: " + self.currentType
                self.errors += 1
                self.currentType = "ERR"
        elif node.op == "-" :
            if not self.currentType in ["ERR", "int"] :
                print "Operand does not match for operator -. Needs: int. Found: " + self.currentType
                self.errors += 1
                self.currentType = "ERR"

