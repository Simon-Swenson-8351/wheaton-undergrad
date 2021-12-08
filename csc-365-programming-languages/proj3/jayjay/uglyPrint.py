#!/usr/bin/python
'''
Created on Jan 6, 2014

@author: tvandrun
'''

#from jay_ast import *
from parser import parser
from uglyPrinterVisitor import UglyPrinterVisitor
import sys

sourceFile = open(sys.argv[1], 'r')
sourceText = sourceFile.read()
ast = parser.parse(sourceText)

nameStart = sys.argv[1].rfind('/') + 1
upVis = UglyPrinterVisitor(sys.argv[1][nameStart:-7])
upVis.visit(ast)
print upVis.result

