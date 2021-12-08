#-----------------------------------------------------------------
# ** ATTENTION **
# This code was automatically generated from the file:
# jayjay/jayjay_ast.cfg 
#
# Do not modify it directly. Modify the configuration file and
# run the generator again.
# ** ** *** ** **
#
# pycparser: c_ast.py
#
# AST Node classes.
#
# Copyright (C) 2008-2012, Eli Bendersky
# License: BSD
#-----------------------------------------------------------------


import sys


class Node(object):
    """ Abstract base class for AST nodes.
    """
    def children(self):
        """ A sequence of all children that are Nodes
        """
        pass

    def show(self, buf=sys.stdout, offset=0, attrnames=False, nodenames=False, showcoord=False, _my_node_name=None):
        """ Pretty print the Node and all its attributes and
            children (recursively) to a buffer.
            
            buf:   
                Open IO buffer into which the Node is printed.
            
            offset: 
                Initial offset (amount of leading spaces) 
            
            attrnames:
                True if you want to see the attribute names in
                name=value pairs. False to only see the values.
                
            nodenames:
                True if you want to see the actual node names 
                within their parents.
            
            showcoord:
                Do you want the coordinates of each Node to be
                displayed.
        """
        lead = ' ' * offset
        if nodenames and _my_node_name is not None:
            buf.write(lead + self.__class__.__name__+ ' <' + _my_node_name + '>: ')
        else:
            buf.write(lead + self.__class__.__name__+ ': ')

        if self.attr_names:
            if attrnames:
                nvlist = [(n, getattr(self,n)) for n in self.attr_names]
                attrstr = ', '.join('%s=%s' % nv for nv in nvlist)
            else:
                vlist = [getattr(self, n) for n in self.attr_names]
                attrstr = ', '.join('%s' % v for v in vlist)
            buf.write(attrstr)

        if showcoord:
            buf.write(' (at %s)' % self.coord)
        buf.write('\n')

        for (child_name, child) in self.children():
            child.show(
                buf,
                offset=offset + 2,
                attrnames=attrnames,
                nodenames=nodenames,
                showcoord=showcoord,
                _my_node_name=child_name)


class NodeVisitor(object):
    """ A base NodeVisitor class for visiting c_ast nodes. 
        Subclass it and define your own visit_XXX methods, where
        XXX is the class name you want to visit with these 
        methods.
        
        For example:
        
        class ConstantVisitor(NodeVisitor):
            def __init__(self):
                self.values = []
            
            def visit_Constant(self, node):
                self.values.append(node.value)

        Creates a list of values of all the constant nodes 
        encountered below the given node. To use it:
        
        cv = ConstantVisitor()
        cv.visit(node)
        
        Notes:
        
        *   generic_visit() will be called for AST nodes for which 
            no visit_XXX method was defined. 
        *   The children of nodes for which a visit_XXX was 
            defined will not be visited - if you need this, call
            generic_visit() on the node. 
            You can use:
                NodeVisitor.generic_visit(self, node)
        *   Modeled after Python's own AST visiting facilities
            (the ast module of Python 3.0)
    """
    def visit(self, node):
        """ Visit a node. 
        """
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)
        
    def generic_visit(self, node):
        """ Called if no explicit visitor function exists for a 
            node. Implements preorder visiting of the node.
        """
        for c_name, c in node.children():
            self.visit(c)


class Program(Node):
    def __init__(self, main, coord=None):
        self.main = main
        self.coord = coord

    def children(self):
        nodelist = []
        if self.main is not None: nodelist.append(("main", self.main))
        return tuple(nodelist)

    attr_names = ()

class Declaration(Node):
    def __init__(self, typeDec, ids, coord=None):
        self.typeDec = typeDec
        self.ids = ids
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.ids or []):
            nodelist.append(("ids[%d]" % i, child))
        return tuple(nodelist)

    attr_names = ('typeDec',)

class Skip(Node):
    def __init__(self, coord=None):
        self.coord = coord

    def children(self):
        return ()

    attr_names = ()

class Block(Node):
    def __init__(self, decls, stmts, coord=None):
        self.decls = decls
        self.stmts = stmts
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.decls or []):
            nodelist.append(("decls[%d]" % i, child))
        for i, child in enumerate(self.stmts or []):
            nodelist.append(("stmts[%d]" % i, child))
        return tuple(nodelist)

    attr_names = ()

class Assignment(Node):
    def __init__(self, target, expr, coord=None):
        self.target = target
        self.expr = expr
        self.coord = coord

    def children(self):
        nodelist = []
        if self.expr is not None: nodelist.append(("expr", self.expr))
        return tuple(nodelist)

    attr_names = ('target',)

class Conditional(Node):
    def __init__(self, cond, thenStmt, elseStmt, coord=None):
        self.cond = cond
        self.thenStmt = thenStmt
        self.elseStmt = elseStmt
        self.coord = coord

    def children(self):
        nodelist = []
        if self.cond is not None: nodelist.append(("cond", self.cond))
        if self.thenStmt is not None: nodelist.append(("thenStmt", self.thenStmt))
        if self.elseStmt is not None: nodelist.append(("elseStmt", self.elseStmt))
        return tuple(nodelist)

    attr_names = ()

class Loop(Node):
    def __init__(self, guard, body, coord=None):
        self.guard = guard
        self.body = body
        self.coord = coord

    def children(self):
        nodelist = []
        if self.guard is not None: nodelist.append(("guard", self.guard))
        if self.body is not None: nodelist.append(("body", self.body))
        return tuple(nodelist)

    attr_names = ()

class Print(Node):
    def __init__(self, expr, coord=None):
        self.expr = expr
        self.coord = coord

    def children(self):
        nodelist = []
        if self.expr is not None: nodelist.append(("expr", self.expr))
        return tuple(nodelist)

    attr_names = ()

class CountLoop (Node):
    def __init__(self, initer, expr, incr, body, coord=None):
        self.initer = initer
        self.expr = expr
        self.incr = incr
        self.body = body
        self.coord = coord

    def children(self):
        nodelist = []
        if self.initer is not None: nodelist.append(("initer", self.initer))
        if self.expr is not None: nodelist.append(("expr", self.expr))
        if self.incr is not None: nodelist.append(("incr", self.incr))
        if self.body is not None: nodelist.append(("body", self.body))
        return tuple(nodelist)

    attr_names = ()

class PTLoop (Node):
    def __init__(self, body, guard, coord=None):
        self.body = body
        self.guard = guard
        self.coord = coord

    def children(self):
        nodelist = []
        if self.body is not None: nodelist.append(("body", self.body))
        if self.guard is not None: nodelist.append(("guard", self.guard))
        return tuple(nodelist)

    attr_names = ()

class DeclInitializer (Node):
    def __init__(self, typeDec, id, expr, coord=None):
        self.typeDec = typeDec
        self.id = id
        self.expr = expr
        self.coord = coord

    def children(self):
        nodelist = []
        if self.typeDec is not None: nodelist.append(("typeDec", self.typeDec))
        if self.expr is not None: nodelist.append(("expr", self.expr))
        return tuple(nodelist)

    attr_names = ('id',)

class NonDeclInitializer (Node):
    def __init__(self, id, expr, coord=None):
        self.id = id
        self.expr = expr
        self.coord = coord

    def children(self):
        nodelist = []
        if self.expr is not None: nodelist.append(("expr", self.expr))
        return tuple(nodelist)

    attr_names = ('id',)

class Variable(Node):
    def __init__(self, id, coord=None):
        self.id = id
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    attr_names = ('id',)

class IntLitExpr(Node):
    def __init__(self, val, coord=None):
        self.val = val
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    attr_names = ('val',)

class BoolLitExpr(Node):
    def __init__(self, val, coord=None):
        self.val = val
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    attr_names = ('val',)

class BinaryExpr(Node):
    def __init__(self, expr1, op, expr2, coord=None):
        self.expr1 = expr1
        self.op = op
        self.expr2 = expr2
        self.coord = coord

    def children(self):
        nodelist = []
        if self.expr1 is not None: nodelist.append(("expr1", self.expr1))
        if self.expr2 is not None: nodelist.append(("expr2", self.expr2))
        return tuple(nodelist)

    attr_names = ('op',)

class UnaryExpr(Node):
    def __init__(self, op, expr, coord=None):
        self.op = op
        self.expr = expr
        self.coord = coord

    def children(self):
        nodelist = []
        if self.expr is not None: nodelist.append(("expr", self.expr))
        return tuple(nodelist)

    attr_names = ('op',)

