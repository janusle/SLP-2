#!/usr/bin/env python2.6
'''
Author: Yan Le
Student number: 3262302

'''

import os


def readlines(filename):
    '''
      **Read file by filename and return a list contains all lines of file.**

      *Args:*
         filename: path of file

      *Returns:*
         list contains each line of file. one element of list match a line of file

      *Raises:*
         IOError: An error occurs if there is anything wrong while reading file
    '''

    lines = []
    with open(filename, 'r') as f:

      for line in f:

        line = line.rstrip("\n").strip()
        if len(line) != 0 and line[0] != '#':
            lines.append(line)

    return lines


def readtable(filename):
    '''
      ** Read a file of colon-delimited lines and returns a list of lists. **

      *Args:*
         filename: path of file

      *Returns:*
         list of lists.
          For example:
             foo:1:12
             bar:2:hello
          will return [['foo','1','12'],['bar','2','hello']]

      *Raises:*
         IOError: An error occurs if there is anything wrong when reading file
    '''

    table = []
    lines = readlines(filename)
    for line in lines:
        row = line.split(":")
        for i in range( 0, len(row) ):
            row[i] = row[i].strip()

        table.append(row)
    return table


def writelines(filename, lines):
    '''
      ** Write a list of string to a file  **

      *Args:*
         filename: path of file
         lines: list of string. Each element of list represents a line

      *Returns:*
         return 0 if fails and 1 if writes successfully

      *Raises:*
         IOError: An error occurs if there is anything wrong when writing file
    '''
    result = 1
    try:
       f = open(filename, "w")
       for line in lines:
           f.write(line + "\n")
       f.close()
    except:
       result = 0

    return result


class Enrol:
    ''' The class encapsulates the tutorial enrolment records.

        It reads enrolment records from the specified data directory.
    '''

    def _addSubjects(self, tables):
       ''' Private method which adds subjects in to self.__subjects'''
       for row in tables:
           if len(row) == 2:
               self.__subjects[row[0]] = {"name":  row[1], "class": [] }
           else:
              pass # throw excepiton

    def _writelines(self,filename , lines ):
       ''' Private method which writes list of string to file by using
           function writelines
       '''
       return writelines(filename, lines)


    def _readfile( self, filename ):
       ''' Private method which reads file and return list by using
           function readfile
       '''
       filename = os.path.join( self.__directory, filename )
       try:
         lines = readlines( filename )
       except:
         return []
       else:
         return lines


    def _readtable( self, filename ):
       ''' Private method which reads a file of colon-delimited lines and
           return list of lists by using function readtable
       '''
       filename = os.path.join( self.__directory, filename )
       tables = readtable( filename )
       return tables


    def _getStudents(self, class_code):
       '''Get student ids who enrol the class

          *Args:*
             class_code: class code

          *Returns:*
             return list of students
       '''
       return self._readfile( class_code + ".roll" )


    def _addStudents(self, class_code, students ):
       ''' add new student to class list

           *Args:*
              class_code: class code
              students: list of students
       '''
       for student in students:
           if student not in self.__students:
               self.__students[ student ] =  [ class_code ]
           else:
               if class_code not in self.__students[ student ]:
                 self.__students[ student ].append(class_code)


    def _addClasses(self, tables):
       ''' add new classes to self.__classes

           *Args:*
             tables: list of classes
       '''
       for row in tables:
           if len(row) == 5 and\
              row[1] in self.__subjects: # row[1] is subject code, check if subject code is existed

               if row[0] not in self.__subjects[row[1]]["class"]:#avoid duplicated item
                  self.__subjects[row[1]]["class"].append( row[0] )

               # row[0] is class code
               students = self._getStudents( row[0] )
               self.__classes[row[0]] = [ row[1], row[2], row[3], row[4] ,\
                                          students ]
               self._addStudents( row[0], students )


    def _addVenues( self, tables ):
        ''' add new venues to self.__venues

            *Args:*
              tables: list of venues
        '''
        for row in tables:
            if len(row) == 2:
              self.__venues[ row[0] ] = row[1]



    def dump(self):
        ''' print all private variables for debuging purpose'''
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
       ''' constructor of enrol class
           It loads all data from files

           *Args:*
              directory: directory name of data files
       '''
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
        ''' get list of all subject codes'''
        return self.__subjects.keys()


    def subjectName(self, code):
        ''' get subject name by its code

            *Args:*
              code: subject code

            *Returns:*
              subject name
        '''
        return self.__subjects[code]["name"]


    def classes(self, subject_code):
        '''get list of class codes for the specified subject

           *Args:*
             subject_code: subject code

           *Returns:*
             list of class codes
        '''
        return self.__subjects[subject_code]["class"]


    def classInfo(self, class_code):
        ''' get info of class by its code

            *Args:*
              class_code: class code

            *Returns:
              a tuple: (subjectcode, time, venue, tutor, students)
        '''
        return tuple(self.__classes[class_code])


    def checkStudent(self, student_id, subject_code=None):
        ''' check enrol status of student

            *Args:*
              student_id: student id
              subject_code: subject code(optional)

            *Returns:*
              if no subject_code is specified, then returns all the
              classes the student is enrolled
              if subject code is specified, then returns class student enroll

            *Raises:*
              if subject code is not existed, KeyError will be raised
        '''
        if subject_code is None and student_id not in self.__students:
           return []


        if subject_code is None:
           return self.__students[ student_id ]
        else:

           classes = self.classes( subject_code ) # no such a subject
           for klass in classes:
               if klass in self.__students[ student_id ]:
                  return klass
           return None

    def enrol(self, student_id, class_code ):
        ''' enrol a class for student

            *Args:*
              student_id: student id
              class_code: class code

            *Returns:*
              1: successful
              None: if fails to do(eg. class is full)

            *Raises:*
              if class code is not existed, KeyError will be raised
        '''
        if student_id not in self.__students:
           self.__students[student_id] = []

        klass = self.classInfo( class_code ) # may raise KeyError
        subject_code = klass[0] # get subject code
        venue = klass[2] # get venue
        cap = self.__venues[ venue ] # get capacity of venue
        enroled_num = len(klass[4])

        if int(cap) - enroled_num  == 0:
            return None  #the class is full

        klass_code = self.checkStudent( student_id, subject_code )
        if klass_code is not None: # if student enroled before, delete previous enrollment
            self.__classes[ klass_code ][4].remove( student_id ) #remove stu_id from classes dict
            self.__students[ student_id ].remove( klass_code ) #remove class code from student dict

        self.__students[ student_id ].append( class_code )
        self.__classes[ class_code ][4].append( student_id )

        # write new enrol to file
        filename = os.path.join(self.__directory, str(class_code) + ".roll")
        students = self.__classes[ class_code ][4]
        result = self._writelines( filename, students )
        # overwrite class file which student enroled before
        if klass_code is not None:
           filename = os.path.join(self.__directory, str(klass_code) + ".roll")
           students = self.__classes[ klass_code ][4]
           result = self._writelines( filename, students )

        if result == 0: #error occur
           #remove the record just added
           self.__students[ student_id ].remove( class_code )
           self.__classes[ class_code ][4].remove( student_id )
           return None

        # All done
        return 1

