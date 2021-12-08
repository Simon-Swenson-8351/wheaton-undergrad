from jay_ast import NodeVisitor, Block, Skip, Conditional, BinaryExpr
import sys

class PrettyPrinterVisitor(NodeVisitor):
    
    def __init__(self, name):
        self.name = name
        self.indentation = 0
        self.supressIndentation = False
    
    def indent(self):
        if self.supressIndentation :
            self.supressIndentation = False
        else :
            for i in range(self.indentation) :
                sys.stdout.write("    ")
                
    def visit_Program(self, node):
        self.cascade = False
        print "public class %s {" % self.name
        self.indentation += 1
        self.indent()
        print "public static void main(String[] args) {"
        self.indentation += 1
        for d in node.decls :
            self.visit(d)
        for s in node.main.stmts :
            self.visit(s)
            
        self.indentation -= 1
        self.indent()
        print "}"
        self.indentation -= 1  # just out of principle
        print "}"
        
    def visit_Declaration(self, node):
        self.indent()
        sys.stdout.write(node.typeDec + " ")

        #ids = node.ids

        ## this feels unpythonic
        #i = 0
        #while True:
        #    sys.stdout.write(ids[i])
        #    i += 1
        #    if i >= len(ids): break
        #    sys.stdout.write(", ")
        #print ";"

        ## alternate, presumably more pythonic version        
        #seps = ([','] * (len(ids) - 1)) + [';'] 
        #for (id, sep) in zip(ids, seps) :
        #    sys.stdout.write("%s%s " % (id, sep))
        #print ""

        ## but I found the real pythonic solution: use join
        print ", ".join(node.ids) + ";"


    def visit_Skip(self, node):
        self.indent()
        print ";//skip"
    
    def visit_Block(self, node):
        rememberCascade = self.cascade
        self.cascade = False
        self.indent()
        print "{"
        self.indentation += 1
        for s in node.stmts :
            self.visit(s)
        self.indentation -= 1
        self.indent()
        print "}"
        self.cascade = rememberCascade
        
    def visit_Assignment(self, node):
        self.indent()
        sys.stdout.write(node.target + " = ")
        self.visit(node.expr)
        print ";"
        
    def visit_Conditional(self, node):
        if not self.cascade :
            #self.cascade = False  # I don't know why that was here
            self.indent()
        sys.stdout.write("if (")
        self.visit(node.cond)
        sys.stdout.write(") ")
        if isinstance(node.thenStmt, Block) :
            self.supressIndentation = True
            self.visit(node.thenStmt)
        else :
            print ""
            self.indentation += 1
            self.visit(node.thenStmt)
            self.indentation -= 1
        if not isinstance(node.elseStmt, Skip) : 
            self.indent()
            sys.stdout.write("else ")
            if isinstance(node.elseStmt, Block) :
                self.supressIndentation = True
                self.visit(node.elseStmt)
            elif isinstance(node.elseStmt, Conditional) :
                self.cascade = True
                self.visit(node.elseStmt)
            else :
                print ""
                self.indentation += 1
                self.visit(node.elseStmt)
                self.indentation -= 1
    
    def visit_Loop(self, node):
        self.indent()
        sys.stdout.write("while (")
        self.visit(node.guard)
        sys.stdout.write(") ")
        if isinstance(node.body, Block) :
            self.supressIndentation = True
            self.visit(node.body)
        else :
            print ""
            self.indentation += 1
            self.visit(node.body)
            self.indentation -= 1
    
    def visit_Print(self, node):
        self.indent()
        sys.stdout.write("System.out.println(")
        self.visit(node.expr)
        print ");"

    def visit_Variable(self, node):
        sys.stdout.write(node.id)

    def visit_IntLitExpr(self, node):
        sys.stdout.write(str(node.val))
        
    def visit_BoolLitExpr(self, node):
        sys.stdout.write("true" if node.val else "false")


    def visit_BinaryExpr(self, node):
        if isinstance(node.expr1, BinaryExpr) and node.expr1.op.prec < node.op.prec :
            sys.stdout.write("(")
            self.visit(node.expr1)
            sys.stdout.write(")")
        else :
            self.visit(node.expr1)
 
        sys.stdout.write(" " + node.op.representation + " ")

        # just different enough (<= instead of <) to make it easier
        # to copy and past than to extract a method
        if isinstance(node.expr2, BinaryExpr) and node.expr2.op.prec <= node.op.prec :
            sys.stdout.write("(")
            self.visit(node.expr2)
            sys.stdout.write(")")
        else :
            self.visit(node.expr2)
        
        
    def visit_UnaryExpr(self, node):
        sys.stdout.write(node.op)
        if isinstance(node.expr, BinaryExpr) :
            sys.stdout.write("(")
            self.visit(node.expr)
            sys.stdout.write(")")
        else :
            self.visit(node.expr)
        