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


if __name__ == '__main__':

     #lines = readtable( "test.txt" )
     lines = readlines( "test.txt" )
     print lines
     writelines( "test_clone.txt" , lines )

     lines = readtable( "test_clone.txt" )
     #lines = readlines( "test_clone.txt" )
     print lines



