#!/usr/bin/env python

def readlines(filename):
    lines = []
    f = open(filename, 'r')

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






if __name__ == '__main__':
     lines = readtable( "test.txt" )
     #lines = readlines( "test.txt" )
     print lines

