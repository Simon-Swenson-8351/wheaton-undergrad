'''
Created on Jan 2, 2014

@author: tvandrun
'''

from jayjay_ast import *
import jay.jay_ast

class TranslatorVisitor(NodeVisitor):
    
    def __init__(self):

        self.indentation = 0
        self.supressIndentation = False
        self.resultText = ""
        self.isDoWhile = False
        self.jayDecls = ""
        self.jayStmts = ""
        self.isProgramBlock = False

        # If you choose the "text result" option, then eventually
        # you'll need to put that result in this instance variable
        # (for example, at the end of the visit_Program method).
        # If you choose the modify-the-ast option, then leave this
        # alone
        # self.resultText = None
        # hint: In either option, you'll want some instance variables
        # where you keep track of things (declared variables, etc),
        # which you'll want to initialize here or at the beginning of
        # visit_Program().

    def indent(self, string):
        if self.supressIndentation:
            self.supressIndentation = False
        else:
            for i in range(self.indentation):
                string += "    "
        
    def visit_Program(self, node):
        self.cascade = False
        self.resultText += "public class ProgramName {\n"
        self.indentation += 1
        self.indent(self.resultText)
        self.resultText += "public static void main(String[] args) {\n"

        self.isProgramBlock = True
        self.indentation += 1
        self.visit(node.main)
        
        self.resultText += self.jayDecls
        self.resultText += self.jayStmts

        self.resultText += "}\n"
        self.indentation -= 1
        self.resultText += "}\n"

        print self.resultText
 
        # The following is for the modify-the-ast option only;
        # if you choose the text-result option, you can ignore
        # these hints and delete the lines of code for this
        # method given below.
        # hint 1: If you choose the modify-the-ast option, you'll
        # probably want to maintain a variable standing
        # for the "modified" version of the most recently visited
        # subtree (which might be the original subtree itself, if
        # no modification was necessary), calling it something
        # like replacement. Thus the post condition of visiting
        # node.main is that we have a new, Jay-AST version of
        # the main part of the node in self.replacement.
        # Then, here, set this Program node's
        # main to that replacement
        # node.main = self.replacement
        # hint 2: A JayJay program node does not have a "declarations"
        # portion (since its main is a block, which has declarations),
        # but a Jay program node does have an attribute/instance variable
        # for declarations (called 'decls'). You'll need to set that
        # to something (though probably not to 'None').
        # node.decls = None


    def visit_Declaration(self, node):
        # Since we're translating a do-while loop to a while loop,
        # The body of the do-while essentially needs to be copied
        # once before entering the while loop. Declarations, however,
        # should not be repeated within the while loop.
        if not self.isDoWhile:
            self.indent(self.jayStmts)
            self.jayStmts += node.typeDec + " "
            self.jayStmts += ", ".join(node.ids) + ";\n"

    def visit_Skip(self, node):
        self.indent(self.jayStmts)
        self.jayStmts += ";//skip\n"
    
    def visit_Block(self, node):
        localIsProgramBlock = self.isProgramBlock
        self.isProgramBlock = False
        rememberCascade = self.cascade
        self.cascade = False
        rememberIsDoWhile = self.isDoWhile
        self.isDoWhile = False
        self.indent(self.jayStmts)
        if not localIsProgramBlock:
            self.jayStmts += "{\n"
        self.indentation += 1
        for d in node.decls :
            self.visit(d)
        for s in node.stmts :
            self.visit(s)
        self.indentation -= 1
        self.indent(self.jayStmts)
        if not localIsProgramBlock:
            self.jayStmts += "} "
        if not rememberIsDoWhile :
            self.jayStmts += "\n"
        self.cascade = rememberCascade
 
        # Ok, here is the last hint. For those of you taking the
        # modify-the-ast option. You will need to make
        # a new block because Jay Blocks are different from
        # JayJay Blocks (JayJay Blocks have a decls attribute).
        # One strategy is to build a list of replacement
        # statements, and then use that to make the Jay Block.
        # If you choose the text-result option, you probably also
        # will want something like the replacements list suggested
        # on the next line, but you'll want it to be a list of
        # string representations of the statements.
        '''
        replacements = []
        for d in node.decls :
            pass
        for s in node.stmts :
            pass
        self.replacement = jay.jay_ast.Block(replacements)
        '''

    def visit_Assignment(self, node) :
        self.indent(self.jayStmts)
        self.jayStmts += node.target + " = "
        self.visit(node.expr)
        self.jayStmts += ";\n"

    def visit_Conditional(self, node) :
        if not self.cascade :
            self.indent(self.jayStmts)
        self.jayStmts += "if ("
        self.visit(node.cond)
        self.jayStmts += ") "
        if isinstance(node.thenStmt, Block) :
            self.supressIndentation = True
            self.visit(node.thenStmt)
        else :
            self.jayStmts += "\n" 
            self.indentation += 1
            self.visit(node.thenStmt)
            self.indentation -= 1
        if not isinstance(node.elseStmt, Skip) : 
            self.indent(self.jayStmts)
            self.jayStmts += "else "
            if isinstance(node.elseStmt, Block) :
                self.supressIndentation = True
                self.visit(node.elseStmt)
            elif isinstance(node.elseStmt, Conditional) :
                self.cascade = True
                self.visit(node.elseStmt)
            else :
                self.jayStmts += "\n"
                self.indentation += 1
                self.visit(node.elseStmt)
                self.indentation -= 1
 

    def visit_Loop(self, node) :
        self.indent(self.jayStmts)
        self.jayStmts += "while ("
        self.visit(node.guard)
        self.jayStmts += ") "
        if isinstance(node.body, Block) :
            self.supressIndentation = True
            self.visit(node.body)
        else :
            self.jayStmts += "\n"
            self.indentation += 1
            self.visit(node.body)
            self.indentation -= 1
        
    
    def visit_Print(self, node):
        self.indent(self.jayStmts)
        self.jayStmts += "System.out.println("
        self.visit(node.expr)
        self.jayStmts += ");\n"

    def visit_CountLoop(self, node) :
        print "Started CountLoop"
        # Contain everything in a block. The block will include the initializer and while loop.
        self.indent(self.jayStmts)
        self.jayStmts += "{\n"
        self.indentation += 1
        
        # Print initializer
        if node.initer != None:
            if isinstance(node.initer, DeclInitiallizer):
                # We must separate into declaration and assignment
                self.indent(self.jayDecls)
                self.jayDecls += node.initer.typeDec + " " + node.initer.id + ";\n"
            self.indent(self.jayStmts)
            self.jayStmts += node.initer.id + " = "
            self.visit(node.initer.expr)
            self.jayStmts += ";\n"

        self.indent(self.jayStmts)
        self.jayStmts += "while ("
        if node.expr != None:
            self.visit(node.expr)
        else:
            self.jayStmts += "true"
        self.jayStmts += ") "

        if node.incr != None:
            # We need to synthesize a new block here so that we can add the incr stmt to it.
            newBlock = Block(None, None)
            if isinstance(node.body, Block):
                newBlock.decls = node.body.decls
                newBlock.stmts = node.body.stmts
                newBlock.stmts.append(node.incr)
            else:
                newBlock.stmts.append(node.body)
                newBlock.stmts.append(node.incr)

            self.supressIndentation = True
            self.visit(newBlock)

        elif isinstance(node.body, Block):
            # Is a block, but no incr stmt
            self.supressIndentation = True
            self.visit(node.body)
        else:
            # Not a block, no incr stmt
            self.jayStmts += "\n"
            self.indentation += 1
            self.visit(node.body)
            self.indentation -= 1
        self.indentation -= 1
        self.indent(self.jayStmts)
        self.jayStmts += "}\n"
        print "Finished CountLoop"


    def visit_PTLoop(self, node) :
        print "Started PTLoop"
        # Contain everything in its own block.
        self.indent(self.jayStmts)
        self.jayStmts += "{\n"
        self.indentation += 1

        # Synthesized new while, needed later
        newWhile = While(None, None)
        newWhile.guard = node.guard

        # Print everything for the pre-while loop to ensure the code is executed at least once (if only we had goto keyword!)
        if isinstance(node.stmt, Block):
            # Necessary to take out the braces, which would ruin our scope for the while loop body.
            for d in node.stmt.decls:
                self.visit(d)
            for s in node.stmt.stmts:
                self.visit(s)

            # Add to synthesized new while
            newWhile.body = Block(None, node.stmt.stmts)
        else:
            self.visit(node.stmt)

            newWhile.body = node.stmt

        # Visit new while loop
        self.visit(newWhile)
        self.indent(self.jayStmts)
        self.jayStmts += "}\n"
        self.indentation -= 1 
        print "Finished PTLoop"

    def visit_Variable(self, node) :
        self.jayStmts += node.id

    def visit_Declaration(self, node) :
        self.indent(self.jayDecls)
        declLine = node.typeDec + " "
        for curId in node.ids:
            declLine += curId + ", "
        declLine = declLine[:-2]
        declLine += ";\n"
        self.jayDecls += declLine

    def visit_Variable(self, node):
        self.jayStmts += node.id

    def visit_IntLitExpr(self, node):
        self.jayStmts += "%s" % node.val

    def visit_BoolLitExpr(self, node):
        self.jayStmts += "%s" % str(node.val).lower()

    def visit_BinaryExpr(self, node):
        parens1 = isinstance(node.expr1, BinaryExpr)
        parens2 = isinstance(node.expr2, BinaryExpr)
        if parens1:
            self.jayStmts += "("
            self.visit(node.expr1)
            self.jayStmts += ")"
        else:
            self.visit(node.expr1)
        self.jayStmts += " " + node.op.representation + " "
        if parens2:
            self.jayStmts += "("
            self.visit(node.expr2)
            self.jayStmts += ")"
        else:
            self.visit(node.expr2)
    
    def visit_UnaryExpr(self, node):
        parens = isinstance(node.expr, BinaryExpr)
        self.jayStmts += node.op
        if parens:
            self.jayStmts += "("
            self.visit(node.expr)
            self.jayStmts += ")"
        else:
            self.visit(node.expr)

    
                          
