#!/usr/bin/env python

def readlines(filename):
    lines = []
    f = open(filename, 'r')

    for line in f:
        line = line.lstrip().rstrip("\n")
        if line[0] != '#':
           lines.append(line)
    return lines






if __name__ == '__main__':
     lines = readlines( "ffffff" )
     print lines

