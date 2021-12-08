#!/usr/bin/python
'''
Created on Jun 18, 2013

@author: thomasvandrunen
'''

from parser import parser
from typeCheckerVisitor import TypeCheckerVisitor
import sys


sourceFile = open(sys.argv[1], 'r')
sourceText = sourceFile.read()
ast = parser.parse(sourceText)

tcVis = TypeCheckerVisitor()
tcVis.visit(ast)

