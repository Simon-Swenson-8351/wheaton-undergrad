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
            if v in self.typeMap :
                # can't figure out how to spread the next line over
                # multiple lines
                print "%s previously declared as %s; preferring initial declaration."% (v, self.typeMap[v])
                self.errors += 1
            
            else :
                self.typeMap[v] = node.typeDec
                self.uninitialized.add(v)

    ## for statements
                
    def visit_Assignment(self, node):

        self.visit(node.expr)
        
        target = node.target

        #print "1 uninitialized: " + str(self.uninitialized)
        if node.target in self.uninitialized :
            self.uninitialized.remove(node.target)
        #print "2 uninitialized: " + str(self.uninitialized)

        ty = None if target not in self.typeMap else self.typeMap[target]
        if ty == None :
            print "%s undeclared (target of assignment)." % target
            self.errors += 1
        elif self.currentType != "ERR"  and self.currentType != ty:
            print "Wrong type for assignment to %s. Needs: %s. Found: %s" % (target, ty, self.currentType)
            self.errors += 1
   
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
        self.visit(node.guard)
        if self.currentType != "ERR" and self.currentType != "boolean" :
            print "Wrong type for loop guard. Needs: boolean. Found: " + self.currentType
            self.errors += 1
            
        orig = self.uninitialized
        
        self.uninitialized = set(orig)
        self.visit(node.body)
        
        self.uninitialized = orig
        
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
        self.visit(node.expr1)
        ty1 = self.currentType
        self.visit(node.expr2)
        ty2 = self.currentType
        
        if ty1 != "ERR" and ty2 != "ERR" :
            # need to handle == and != separately, unfortunately
            if node.op.representation in ["==", "!="] :
                if not self.compatibleTypes(ty1, ty2):
                    print "Incompatible types " + ty1 + ", " + ty2 + " for comparison."
                    self.errors += 1
                    self.currentType = "ERR"
                else :
                    self.currentType = "boolean"
            else :
                (ot1, ot2, rt) = node.op.tys
                if (ot1, ot2) != (ty1, ty2) :
                    print "Operands do not match for operator %s. Needs: %s, %s. Found: %s, %s" % (node.op.representation, ot1, ot2, ty1, ty2)
                    self.errors += 1
                    self.currentType = "ERR"
                else :
                    self.currentType = rt
        else :
            self.currentType = "ERR"
    
    def compatibleTypes(self, ty1, ty2):
        return ty1 == ty2
    
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

