#!/usr/bin/python
#-*-coding:utf8-*-
from __future__ import print_function
from functools import partial

import re, argparse

class Calc(object):
    def __init__(self):
        """Make regular expressions for parsing input.
        """
        self.add = re.compile('\+')
        # Supports division and multiplication with negative numbers: "/-", "*-"
        self.subtract = re.compile('(?<!^)(?<!\*)(?<!/)-')
        self.multiply = re.compile('\*')
        self.divide = re.compile('/')
        self.signs = {'+': self.add,
                      '-': self.subtract,
                      '*': self.multiply,
                      '/': self.divide}

    def main(self):
        """Main loop. Start here.
        """
        while True:
            try:
                inp = ''.join(raw_input(' > ').split(' '))
                factored = self.parse_input(inp)
            except ValueError as e:
                print (4*' ' + '\n'.join(e.args))
                continue
            except KeyboardInterrupt:
                print ('\n', 4*' ' + 'bye bye')
                break
            else:
                print ('  ', self.get_presentable_output(
                        self.evaluate_factors(factored)))

    def get_presentable_output(self, evaluated):
        """Quick method for formatting output.
        """
        a, b = evaluated
        if False and b == 1: # This would have been nice.
            return str(a)
        else:
            return '{} / {}'.format(a,b)


    def parse_input(self, inp):
        """Takes an input string and parses it as a fraction. Returns tuple.
        """
        if inp == '':
            raise ValueError('No input.')
        if False in [_ in '0123456789-+*/' for _ in inp]:
            raise ValueError('Integers (0-9) & operators (+-*/) only, please.')
        if inp[0] in '+*/':
            raise ValueError('First sign connot be "+", "*" or "/".')
        for f in '+-*/':
            if self.signs[f].search(inp, 1):
                factored = self.signs[f].split(inp, 1)
                a = self.parse_input(factored[0])
                b = self.parse_input(factored[1])
                if f == '/' and b == '0':
                    raise ValueError('Divide by zero. Please don\'t.')
                return [a, f, b]
        else:
            return inp

    def evaluate_factors(self, focus):
        """Handler for evaluate_factor.
        """
        return self.reduce(self.evaluate_factor(focus))

    def evaluate_factor(self, focus):
        """Evaluate the parsed input.
        """
        if isinstance(focus, str):
            if self.is_number(focus):
                return (int(focus), 1)
        if isinstance(focus, list):
            sign = focus[1]
            if not isinstance(focus[0], tuple):
                a = self.evaluate_factor(focus[0])
            if not isinstance(focus[2], tuple):
                b = self.evaluate_factor(focus[2])
        common_d = self.find_common_denominator(a, b)
        a = (a[0] * (common_d // a[1]), common_d)
        b = (b[0] * (common_d // b[1]), common_d)
        if sign == '+':
            return a[0] + b[0], common_d
        if sign == '-':
            return a[0] - b[0], common_d
        if sign == '/':
            return a[0] * b[1], a[1] * b[0]
        if sign == '*':
            return a[0] * b[0], a[1] * b[1]

    def find_common_denominator(self, a, b):
        """Find the common denominator from two denominators.
        """
        if a[1]%b[1] == 0:
            return a[1]
        elif b[1]%a[1] == 0:
            return b[1]
        else:
            return a[1]*b[1]

    def reduce(self, fraction):
        """Reduce the fraction.
        """
        a, b = fraction
        # Wanting to reduce the fraction, we loop from the denominator and down.
        for guess in range(b, 1, -1):
            if a%guess==0 and b%guess==0:
                a, b = a//guess, b//guess
        # If the denominator is negative. We fix it.
        if b < 0:
            return -a, -b
        return a, b

    def is_number(self, string):
        """\"string\" is a number. May be negative.
        """
        if string[0] == '-' and len(string)>1: string = string[1:]
        return not False in [ord('0')<=ord(char)<= ord('9') for char in string]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', help='Run the calculator (no testing).',
                        action='store_true')
    args = parser.parse_args()

    if args.run:
        Calc().main()
    else:
        print ("To run tests, please use nose (pip install nose; nosetests).\n"
               "To try out the calculator, run this file with the --run flag.")
