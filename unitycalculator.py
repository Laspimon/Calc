#!/usr/bin/python
#-*-coding:utf8-*-
from __future__ import print_function
import unittest, re

class Calc(object):

    def __init__(self):
        self.add = re.compile('\+?')
        self.substract = re.compile('-?')
        self.multiply = re.compile('\*?')
        self.divide = re.compile('/?')
        self.signs = {'+': self.add,
                      '-': self.substract,
                      '*': self.multiply,
                      '/': self.divide}

    def main(self):
        while True:
            inp = '4*7+2/4+1' #test
            #inp = raw_input(' >')
            print (self.parse_input(inp))
            break


    def parse_input(self, inp, factors = []):
        for f in '+-*/':
            if f in inp:
                factored = self.signs[f].split(inp, 1)
                print(factored)
                factored.insert(1, f)
                factored[0] = self.parse_input(factored[0])
                factored[2] = self.parse_input(factored[2])
                return factored
        else:
            return inp

if __name__ == '__main__':
    calc = Calc()
    calc.main()
