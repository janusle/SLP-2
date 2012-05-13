#!/usr/bin/env python

import enrol
import sys
import os


def getDataDir():
    if 'ENROLDIR' in os.environ:
       directory = os.environ['ENROLDIR']
    else:
       directory = 'data'

    if not os.path.exists( directory ):
      sys.stderr.write("Cannot visit the directory specified, \
the directory may not exists\n")
      sys.stderr.write("Usage: ./stats [--student] [student number]\n")
      sys.exit(-1)

    return directory



directory = getDataDir() #read directory of data
e = enrol.Enrol(directory)


if len( sys.argv ) == 1: # no argument

   subjects = [ ( subject, e.subjectName(subject), len(e.classes(subject)),\
                sum( [ len(e.classInfo(c)[4]) for c in e.classes(subject) ] ))\
                for subject in e.subjects() ]

   print "Subjects are:"
   for subject in subjects:
       print "%s\t%s\tclasses: %d\tstudents: %d" % subject

else:
  pass
