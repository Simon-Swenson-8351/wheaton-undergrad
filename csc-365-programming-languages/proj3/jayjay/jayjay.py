#!/usr/bin/python
'''
Created on Jan 6, 2014

@author: tvandrun
'''


from parser import parser
from translatorVisitor import TranslatorVisitor
from typeCheckerVisitor import TypeCheckerVisitor
import jay.prettyPrinterVisitor
import jay.typeCheckerVisitor
import jay.interpreterVisitor
import jay.parser
import sys

prnt = False
ex = True

for x in sys.argv[1:] :
    if x.startswith("--") :
        if x == "--print" :
            prnt = True
        elif x == "--no-ex" :
            ex = False
        else :
            print "Unrecognized option " + x
    else :
        sourceFileName = x


sourceFile = open(sys.argv[1], 'r')
sourceText = sourceFile.read()
nameStart = sourceFileName.rfind('/') + 1
progName = sourceFileName[nameStart:-10]

try :
    ast = parser.parse(sourceText)
except SyntaxError :
    print "JayJay syntax error"
    raise

tcVis = TypeCheckerVisitor()
tcVis.visit(ast)

if tcVis.errors == 0 :
    transVis = TranslatorVisitor()
    transVis.visit(ast)
    if transVis.resultText :
        if prnt :
            print transVis.resultText
        try :
            jAst = jay.parser.parser.parse(transVis.resultText)
        except SyntaxError :
            print "Jay syntax error"
            raise
    else :
        jAst = ast
        if prnt :
            jppVis = jay.prettyPrinterVisitor.PrettyPrinterVisitor(progName)
            try :
                jppVis.visit(ast)
            except :
                print "Error while pretty printing Jay AST"
                raise
    if jAst == None :
        print "No Jay AST"
        sys.exit

    jtcVis = jay.typeCheckerVisitor.TypeCheckerVisitor()
    jtcVis.visit(jAst)

    if jtcVis.errors == 0 and ex :
        jiVis = jay.interpreterVisitor.InterpreterVisitor()
        jiVis.visit(jAst)
    else :
        print "Type errors in Jay program"
else :
    print "Type errors in JayJay program"


