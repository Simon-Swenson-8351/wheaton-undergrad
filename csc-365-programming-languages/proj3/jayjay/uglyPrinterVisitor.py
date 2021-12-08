'''
Created on Jan 6, 2014

@author: tvandrun
'''

from jayjay_ast import *
import sys

class UglyPrinterVisitor(NodeVisitor):
    
    def __init__(self, name):
        self.name = name
        self.indentation = 0
        self.supressIndentation = False
        self.result = ""
        self.isDoWhile = False
    
    def indent(self):
        if self.supressIndentation :
            self.supressIndentation = False
        else :
            for i in range(self.indentation) :
                self.result += "    "
                
    def visit_Program(self, node):
        self.cascade = False
        self.result += "public class %s {" % self.name + "\n"
        self.indentation += 1
        self.indent()
        self.result += "public static void main(String[] args) "

        self.supressIndentation = True
        self.visit(node.main)
            

        self.indentation -= 1  # just out of principle
        self.result += "}\n"
        
    def visit_Declaration(self, node):
        self.indent()
        self.result += node.typeDec + " "
        self.result += ", ".join(node.ids) + ";\n"


    def visit_Skip(self, node):
        self.indent()
        self.result += ";//skip\n"
    
    def visit_Block(self, node):
        rememberCascade = self.cascade
        self.cascade = False
        rememberIsDoWhile = self.isDoWhile
        self.isDoWhile = False
        self.indent()
        self.result += "{\n"
        self.indentation += 1
        for d in node.decls :
            self.visit(d)
        for s in node.stmts :
            self.visit(s)
        self.indentation -= 1
        self.indent()
        self.result += "} "
        if not rememberIsDoWhile :
            self.result += "\n"
        self.cascade = rememberCascade
        
    def visit_Assignment(self, node):
        self.indent()
        self.result += node.target + " = "
        self.visit(node.expr)
        self.result += ";\n"
        
    def visit_Conditional(self, node):
        if not self.cascade :
            self.indent()
        self.result += "if ("
        self.visit(node.cond)
        self.result += ") "
        if isinstance(node.thenStmt, Block) :
            self.supressIndentation = True
            self.visit(node.thenStmt)
        else :
            self.result += "\n"
            self.indentation += 1
            self.visit(node.thenStmt)
            self.indentation -= 1
        if not isinstance(node.elseStmt, Skip) : 
            self.indent()
            self.result += "else "
            if isinstance(node.elseStmt, Block) :
                self.supressIndentation = True
                self.visit(node.elseStmt)
            elif isinstance(node.elseStmt, Conditional) :
                self.cascade = True
                self.visit(node.elseStmt)
            else :
                self.result += "\n"
                self.indentation += 1
                self.visit(node.elseStmt)
                self.indentation -= 1
    
    def visit_Loop(self, node):
        self.indent()
        self.result += "while ("
        self.visit(node.guard)
        self.result += ") "
        if isinstance(node.body, Block) :
            self.supressIndentation = True
            self.visit(node.body)
        else :
            self.result += "\n"
            self.indentation += 1
            self.visit(node.body)
            self.indentation -= 1
    
    def visit_Print(self, node):
        self.indent()
        self.result += "System.out.println("
        self.visit(node.expr)
        self.result += ");\n"

    def visit_CountLoop(self, node) :
        self.indent()
        self.result += "for ("
        if node.initer :
            self.visit(node.initer)
        self.result += "; "
        if node.expr :
            self.visit(node.expr)
        self.result += "; "
        if node.incr :
            self.result += node.incr.target + " = "
            self.visit(node.incr.expr)
        self.result += ") "
        if isinstance(node.body, Block) :
            self.supressIndentation = True
            self.visit(node.body)
        else :
            self.result += "\n"
            self.indentation += 1
            self.visit(node.body)
            self.indentation -= 1

    def visit_DeclInitializer(self, node) :
        self.result += node.typeDec + " " + node.id + " = "
        self.visit(node.expr)

    def visit_NonDeclInitializer(self, node) :
        self.result += node.ide + " = "
        self.visit(node.expr)        


    def visit_PTLoop(self, node) :
        self.indent()
        self.result += "do "
        if isinstance(node.body, Block) :
            self.supressIndentation = True
            self.isDoWhile = True
            self.visit(node.body)
        else :
            self.result += "\n"
            self.indentation += 1
            self.visit(node.body)
            self.indentation -= 1
        self.result += "while ("
        self.visit(node.guard)
        self.result += ");\n"
        

    def visit_Variable(self, node):
        self.result += node.id

    def visit_IntLitExpr(self, node):
        self.result += str(node.val)
        
    def visit_BoolLitExpr(self, node):
        self.result += "true" if node.val else "false"


    def visit_BinaryExpr(self, node):
        if isinstance(node.expr1, BinaryExpr) and node.expr1.op.prec < node.op.prec :
            self.result += "("
            self.visit(node.expr1)
            self.result += ")"
        else :
            self.visit(node.expr1)
 
        self.result += " " + node.op.representation + " "

        # just different enough (<= instead of <) to make it easier
        # to copy and past than to extract a method
        if isinstance(node.expr2, BinaryExpr) and node.expr2.op.prec <= node.op.prec :
            self.result += "("
            self.visit(node.expr2)
            self.result += ")"
        else :
            self.visit(node.expr2)
        
        
    def visit_UnaryExpr(self, node):
        self.result += node.op
        if isinstance(node.expr, BinaryExpr) :
            self.result += "("
            self.visit(node.expr)
            self.result += ")"
        else :
            self.visit(node.expr)
        
