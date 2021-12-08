from jay_ast import NodeVisitor, Block, Skip, Conditional, BinaryExpr
import sys

class PrettyPrinterVisitor(NodeVisitor):

    def __init__(self, name):
        self.name = name
        self.layer = 0;

    def print_layer_spaces(self):
        s = ""
        for i in range(self.layer):
            s += "    "
        sys.stdout.write(s)

    def visit_Program(self, node):
        self.print_layer_spaces()
        print "public class %s {" % self.name
        print ""
        self.layer += 1

        self.print_layer_spaces()
        print "public static void main(String[] args) {"
        print ""
        self.layer += 1

        for d in node.decls :
            self.visit(d)
        print ""
        for s in node.main.stmts :
            self.visit(s)

        self.layer -= 1
        self.print_layer_spaces()
        print "}"

        self.layer -= 1
        self.print_layer_spaces()
        print "}"


    def visit_Declaration(self, node):
        to_print = ""
        to_print += node.typeDec + " "
        for an_id in node.ids:
            to_print += an_id + ", "
        self.print_layer_spaces()
        print to_print[:-2] + ";"


    def visit_Skip(self, node):
        self.print_layer_spaces()
        print "; // skip"


    def visit_Block(self, node):
        print " {"
        for stmt in node.stmts:
            self.visit(stmt)
        # There's a quirk here with implementation.
        # We need to decrement layer before we print the end bracket.
        self.layer -= 1
        self.print_layer_spaces()
        self.layer += 1
        print "}"

    def visit_Assignment(self, node):
        self.print_layer_spaces()
        sys.stdout.write(node.target + " = ")
        self.visit(node.expr)
        print ";"

    def visit_Conditional(self, node):
        self.print_layer_spaces()
        sys.stdout.write("if ( ")
        self.visit(node.cond)
        print " )"
        self.layer += 1

        self.visit(node.thenStmt)
        self.layer -= 1

        self.print_layer_spaces()
        sys.stdout.write("else")
        self.layer += 1

        self.visit(node.elseStmt)
        self.layer -= 1

    def visit_Loop(self, node):
        self.print_layer_spaces()
        sys.stdout.write("while ( ")
        self.visit(node.guard)
        print " )"
        self.layer += 1

        self.visit(node.body)
        self.layer -= 1


    def visit_Print(self, node):
        self.print_layer_spaces()
        sys.stdout.write("System.out.println( ")
        self.visit(node.expr)
        print " );"

    def visit_Variable(self, node):
        sys.stdout.write(node.id)

    def visit_IntLitExpr(self, node):
        sys.stdout.write(str(node.val))

    def visit_BoolLitExpr(self, node):
        sys.stdout.write("true" if node.val else "false")


    def visit_BinaryExpr(self, node):
        sys.stdout.write("( ")
        self.visit(node.expr1)
        sys.stdout.write(" " + node.op + " ")
        self.visit(node.expr2)
        sys.stdout.write(" )")


    def visit_UnaryExpr(self, node):
        sys.stdout.write(node.op)
        if isinstance(node.expr, BinaryExpr) :
            sys.stdout.write("(")
            self.visit(node.expr)
            sys.stdout.write(")")
        else :
            self.visit(node.expr)

