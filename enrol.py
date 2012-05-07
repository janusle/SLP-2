#!/usr/bin/env python

def readlines(filename):
    lines = []
    with open(filename, 'r') as f:

       for line in f:

          line = line.lstrip().rstrip("\n")
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

    def __addSubjects(self, tables):
       for row in tables:
           #error checking
           self.__subjects[row[0]] = row[1]


    def __init__(self, directory):
       import os
       self.__subjects = {}

       for dirpath,_,files in os.walk( directory ):
           for filename in files:
               if filename.find("SUBJECTS") != -1:
                   filename = os.path.join( dirpath, filename )
                   tables = readtable( filename )
                   self.__addSubjects( tables )

    def subjects(self):
        return self.__subjects.keys()


    def subjectName(self, code):
        return self.__subjects[code]


    def classes(self):
        pass

    def classInfo(self):
        pass



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
     print e.subjectName("ddd")
     print e.subjectName("bbb")
     print e.subjectName("dfdfdfdfd")
