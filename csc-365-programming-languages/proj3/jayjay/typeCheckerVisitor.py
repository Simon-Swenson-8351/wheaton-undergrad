'''
Created on Jan 2, 2014

@author: tvandrun
'''

import jay.typeCheckerVisitor
from typeEnv import TypeEnv

class TypeCheckerVisitor(jay.typeCheckerVisitor.TypeCheckerVisitor):
    
    def visit_Program(self, node):
        self.typeMap = TypeEnv()
        self.uninitialized = set([])
        self.errors = 0

        self.visit(node.main)
        
        if self.errors == 0 :
            print "Program types correctly."
        else :
            print "%s type errors." % self.errors
            
    def visit_Block(self, node):
        self.typeMap.push()
        for d in node.decls :
            self.visit(d)
        for s in node.stmts :
            self.visit(s)    
        self.typeMap.pop()
   
    def visit_CountLoop(self, node):
        self.typeMap.push()
        self.visit(node.initer)
        self.visit(node.expr)
        if self.currentType != "ERR" and self.currentType != "boolean" :
            print "Wrong type for loop guard. Needs: boolean. Found: " + self.currentType
            self.errors += 1
        
        orig = self.uninitialized
        
        self.visit(node.incr)
        self.visit(node.body)
        
        self.uninitialized = orig

        self.typeMap.pop()
        
    def visit_DeclInitializer(self, node):
        v = node.id
        ty = node.typeDec
        if node.id in self.typeMap :
            print "%s previously declared as %s; preferring initial declaration."% (v, self.typeMap[v])
            self.errors += 1
        else :
            self.typeMap[v] = ty
            # don't put it in the uninitialize set---
            # it's initialized right here! 
        
        self.visit(node.expr)
        if self.currentType != "ERR" and self.currentType != ty:
            print "Wrong type for assignment to %s. Needs: %s. Found: %s" % (v, ty, self.currentType)
            self.errors += 1

    def visit_NonDeclInitializer(self, node):
        
        self.visit(node.expr)
        
        v = node.id

        if v in self.uninitialized :
            self.uninitialized.remove(v)

        ty = None if v not in self.typeMap else self.typeMap[v]
        if ty == None :
            print "%s undeclared (for-loop initializer)." % v
            self.errors += 1
        elif self.currentType != "ERR"  and self.currentType != ty:
            print "Wrong type for assignment to %s. Needs: %s. Found: %s" % (v, ty, self.currentType)
            self.errors += 1

    def visit_PTLoop(self, node):
        # We don't need to mess with the uninitialized set. Think about it.
        self.visit(node.body)
        self.visit(node.guard)
        if self.currentType != "ERR" and self.currentType != "boolean" :
            print "Wrong type for loop guard. Needs: boolean. Found: " + self.currentType
            self.errors += 1
        
