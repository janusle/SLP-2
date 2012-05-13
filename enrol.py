#!/usr/bin/env python

import os
import sys


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


class Enrol:

    def _addSubjects(self, tables):
       for row in tables:
           if len(row) == 2:
               self.__subjects[row[0]] = {"name":  row[1], "class": [] }
           else:
              pass # throw excepiton

    def _writelines(filename , lines ):

       return writelines(filename, lines)


    def _readfile( self, filename ):

       filename = os.path.join( self.__directory, filename )
       try:
         lines = readlines( filename )
       except:
         return []
       else:
         return lines


    def _readtable( self, filename ):
       filename = os.path.join( self.__directory, filename )
       tables = readtable( filename )
       return tables


    def _getStudents(self, class_code):
       return self._readfile( class_code + ".roll" )


    def _addStudents(self, class_code, students ):
       for student in students:
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
               self._addStudents( row[0], students )
           else:
              pass # throw exception


    def _addVenues( self, tables ):
        for row in tables:
            if len(row) == 2:
              self.__venues[ row[0] ] = row[1]
            else:
              pass # throw exception


    def dump(self):
        print self.__directory
        print ""
        print self.__subjects
        print ""
        print self.__classes
        print ""
        print self.__students
        print ""
        print self.__venues


    def __init__(self, directory):

       self.__directory = directory

       self.__subjects = {} # structure { code : { name:xxx, class: [] } }

       self.__classes = {} # structure { class_code: ( subjectcode,time,venue,tutor, students ) }

       self.__students = {} # structure{ id: [ class_code ... ] }

       self.__venues = {} # structure { venue_name : capacity }

       tables = self._readtable( "SUBJECTS" )
       self._addSubjects( tables )

       tables = self._readtable( "CLASSES" )
       self._addClasses( tables )

       tables = self._readtable( "VENUES" )
       self._addVenues( tables )

    def subjects(self):
        return self.__subjects.keys()


    def subjectName(self, code):
        return self.__subjects[code]["name"]


    def classes(self, subject_code):
        return self.__subjects[subject_code]["class"]


    def classInfo(self, class_code):
        return tuple(self.__classes[class_code])


    def checkStudent(self, student_id, subject_code=None):

        if student_id not in self.__students:
           return None

        if subject_code is None:
           return self.__students[ student_id ]
        else:

           classes = self.classes( subject_code ) # no such a subject
           for klass in classes:
               if klass in self.__students[ student_id ]:
                  return klass
           return None

    def enrol(self, student_id, class_code ):

        if student_id not in self.__students:
           self.__students[student_id] = []

        klass = self.classInfo( class_code ) # may raise KeyError

        subject_code = klass[0] # get subject code
        venue = klass[2] # get venue
        cap = self.__venue[ venue ] # get capacity of venue
        enroled_num = len(klass[4])

        if int(cap) - enroled_num  == 0:
            return None  #the class is full

        klass_code = checkStudent( student_id, subject_code )
        if klass_code is not None:
            self.__classes[ klass_code ][4].remove( student_id ) #remove stu_id from classes dict
            self.__students[ student_id ].remove( klass_code ) #remove class code from student dict

        self.__students[ student_id ].append( class_code )
        self.__classes[ class_code ][4].append( student_id )

        filename = str(class_code) + ".roll"
        students = self.__classes[ class_code ][4]
        result = self._writelines( filename, students )
        if result == 0: #error occur
           #remove the record just added
           self.__students[ student_id ].remove( class_code )
           self.__classes[ class_code ][4].remove( student_id )
           return None

        # All done
        return 1

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
     #print e.subjects()
     #print e.classes("ddd")
     #print e.subjectName("dfdfdfdfd")
     #print e.classInfo( "class6" )
     #print e.classInfo( "class2" )
     print e.checkStudent( "s3262302" )
     print e.checkStudent( "s3262302", "ddd" )
     print e.checkStudent( "s3262302", "aaa" )
