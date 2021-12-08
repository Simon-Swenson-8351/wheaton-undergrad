#!/usr/bin/python

from parser import parser
from prettyPrinterVisitor import PrettyPrinterVisitor
import sys

sourceFile = open(sys.argv[1], 'r')
sourceText = sourceFile.read()
ast = parser.parse(sourceText)

nameStart = sys.argv[1].rfind('/') + 1
ppVis = PrettyPrinterVisitor(sys.argv[1][nameStart:-4])
ppVis.visit(ast)

