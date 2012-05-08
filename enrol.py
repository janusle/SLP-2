#!/usr/bin/env python

def readlines(filename):
    lines = []
    with open(filename, 'r') as f:

       for line in f:

          line = line.rstrip("\n").strip()
          if len(line) != 0 and line[0] != '#':
              lines.append(line)

    return lines


def readtable(filename):
    table = []
    lines = readlines(filename)
    for line in lines:
        row = line.split(":")
        for i in range( 0, len(row) ):
            row[i] = row[i].strip()

        table.append(row)
    return table


def writelines(filename, lines):

    result = 1
    try:
       f = open(filename, "w")
       for line in lines:
           f.write(line + "\n")
    except:
       result = 0
    finally:
       f.close()
       return result

import os
import sys

class Enrol:


    def _addSubjects(self, tables):
       for row in tables:
           if len(row) == 2:
               self.__subjects[row[0]] = {"name":  row[1], "class": [] }
           else:
              pass # throw excepiton


    def _readfile( self, filename ):
       try:
         lines = readlines( filename )
       except:
         return []
       else:
         return lines


    def _readtable( self, filename ):
       filename = os.path.join( self._directory, filename )
       tables = readtable( filename )
       return tables


    def _getStudents(self, class_code):

       filename = os.path.join( self._directory, class_code + ".roll" )
       return self._readfile( filename )

    def _addStudents(self, class_code, students ):
       for student in studnets:
           if student not in self.__students:
               self.__students[ student ] =  [ class_code ]
           else:
               if class_code not in self.__students[ student ]:
                 self.__students[ student ].append(class_code)


    def _addClasses(self, tables):
       for row in tables:
           if len(row) == 5:
               if row[0] not in self.__subjects[row[1]]["class"]:#avoid duplicated item
                  self.__subjects[row[1]]["class"].append( row[0] )

               # row[0] is class code
               students = self._getStudents( row[0] )
               self.__classes[row[0]] = [ row[1], row[2], row[3], row[4] ,\
                                          students ]
               _addStudents( row[0], students )
           else:
              pass # throw exception


    def __init__(self, directory):

       self._directory = directory

       self.__subjects = {} # structure { code : { name:xxx, class: [] } }

       self.__classes = {} # structure { class_code: ( subjectcode,time,venue,tutor, students ) }

       self.__students = {} # structure{ id: [ class_code ... ] }

       tables = self._readtable( "SUBJECTS" )
       self._addSubjects( tables )

       tables = self._readtable( "CLASSES" )
       self._addClasses( tables )



       for dirpath,_,files in os.walk( directory ):
           for filename in files:
               if filename.find("SUBJECTS") != -1:
                   pass
               elif filename.find("CLASSES") != -1:
                   pass


    def subjects(self):
        return self.__subjects.keys()


    def subjectName(self, code):
        return self.__subjects[code]["name"]


    def classes(self, subject_code):
        return self.__subjects[subject_code]["class"]


    def classInfo(self, class_code):
        return tuple(self.__classes[class_code])



if __name__ == '__main__':

     '''
     #lines = readtable( "test.txt" )
     lines = readlines( "test.txt" )
     print lines
     writelines( "test_clone.txt" , lines )

     lines = readtable( "test_clone.txt" )
     #lines = readlines( "test_clone.txt" )
     print lines
     '''
     e = Enrol('data')
     print e.subjects()
     print e.classes("ddd")
     #print e.subjectName("dfdfdfdfd")
     print e.classInfo( "class6" )
