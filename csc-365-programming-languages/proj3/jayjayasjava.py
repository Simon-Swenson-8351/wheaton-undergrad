#!/usr/bin/python

import os
import sys


filename = sys.argv[1]
if filename.endswith("jayjay") :
   nameStart = filename.rfind('/') + 1
   jfilename = filename[nameStart:-6] + "java"
   os.system("cp " + filename + " " + jfilename)
   if os.system("javac " + jfilename) == 0:
       os.system("java " + jfilename[:-5])
       os.system("rm " + jfilename[:-4] + "class")
   os.system("rm " + jfilename)
else:
   print "Please use on a .jayjay file."


