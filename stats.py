#!/usr/bin/env python

import enrol
import sys
import os
import getopt


def usage():
    sys.stderr.write("Usage: ./stats [--student] [student number]\n")


def getDataDir():
    if 'ENROLDIR' in os.environ:
       directory = os.environ['ENROLDIR']
    else:
       directory = 'data'

    if not os.path.exists( directory ):
      sys.stderr.write("Cannot visit the directory specified, \
the directory may not exists\n")
      usage()
      sys.exit(-1)

    return directory


def getStudentId(argv):

   try:
          optlist, args = getopt.getopt( sys.argv[1:], "", ["student="] )
   except getopt.GetoptError ,err:
          sys.stderr.write(str(err) + "\n")
          usage()
          sys.exit(-1)

   student_id = None
   for opt,val in optlist:
        if opt == "--student":
           student_id = val
           break

   return student_id



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
   student_id = getStudentId( sys.argv[1:] )
   classes = e.checkStudent( student_id )

   if len(classes) != 0 :
       subjects = [ (e.classInfo(klass)[0], e.subjectName( e.classInfo(klass)[0] ), \
                     e.classInfo(klass)[1], e.classInfo(klass)[2] ) \
                     for klass in classes ]

       for subject in subjects:
          print "%s\t%s\t%s @ %s" % subject

   else:
       print "The student didn't enrol any class"
