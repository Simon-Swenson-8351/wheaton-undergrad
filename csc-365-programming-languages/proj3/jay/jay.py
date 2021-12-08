#!/usr/bin/python
'''
Created on Jun 18, 2013

@author: thomasvandrunen
'''

#from jay_ast import *
from parser import parser
from interpreterVisitor import InterpreterVisitor
from typeCheckerVisitor import TypeCheckerVisitor
import sys


sourceFile = open(sys.argv[1], 'r')
sourceText = sourceFile.read()
ast = parser.parse(sourceText)

tcVis = TypeCheckerVisitor()
tcVis.visit(ast)

if tcVis.errors == 0 :
    interpVis = InterpreterVisitor()
    interpVis.visit(ast)


