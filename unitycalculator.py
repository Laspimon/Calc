#!/usr/bin/python
#-*-coding:utf8-*-
from __future__ import print_function
import unittest, re

class Calc(object):

    factored = None

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
            inp = raw_input(' >')
            self.factored = self.parse_input(inp)
            print (self.factored)
            break


    def parse_input(self, inp, factors = []):
        for f in '+-*/':
            if f in inp:
                factored = self.signs[f].split(inp, 1)
                factored.insert(1, f)
                factored[0] = self.parse_input(factored[0])
                factored[2] = self.parse_input(factored[2])
                return factored
        else:
            return inp

    def evaluate_factors(self, focus = None):
        if focus is None: focus = self.factored
        return self.reduce(self.evaluate_factor(focus))

    def evaluate_factor(self, focus):
        if isinstance(focus, str):
            if [ord('0') <= ord(char) <= ord('9') for char in focus]:
                return (int(focus), 1)
        if isinstance(focus, list):
            if not isinstance(focus[0], tuple):
                focus[0] = self.evaluate_factor(focus[0])
            if not isinstance(focus[2], tuple):
                focus[2] = self.evaluate_factor(focus[2])
        common_d = self.find_common_denominator(focus[0], focus[2])
        focus[0] = (focus[0][0] * (common_d / focus[0][1]), common_d)
        focus[2] = (focus[2][0] * (common_d / focus[2][1]), common_d)
        if focus[1] == '+':
            if not False in [isinstance(_, tuple) for _ in focus[::2]]:
                return focus[0][0] + focus[2][0], common_d
        if focus[1] == '-':
            if not False in [isinstance(_, tuple) for _ in focus[::2]]:
                return focus[0][0] - focus[2][0], common_d
        if focus[1] == '/':
            if not False in [isinstance(_, tuple) for _ in focus[::2]]:
                return focus[0][0] * focus[2][1], focus[0][1] * focus[2][0]
        return focus

    def find_common_denominator(self, a, b):
        if a[1]%b[1] == 0:
            return a[1]
        elif b[1]%a[1] == 0:
            return b[1]
        else:
            return a[1]*b[1]

    def reduce(self, fraction):
        for guess in range(fraction[1],1,-1):
            if fraction[0]%guess==0 and fraction[1]%guess==0:
                return fraction[0]/guess, fraction[1]/guess
        return fraction

class TestParseInput(unittest.TestCase):

    def test_parse_plus(self):
        calc = Calc()
        out = calc.parse_input('1+2')
        self.assertEqual(out, ['1', '+', '2'])

    def test_parse_minus(self):
        calc = Calc()
        out = calc.parse_input('3-2')
        self.assertEqual(out, ['3', '-', '2'])

    def test_parse_multiply(self):
        calc = Calc()
        out = calc.parse_input('1*2')
        self.assertEqual(out, ['1', '*', '2'])

    def test_parse_divide(self):
        calc = Calc()
        out = calc.parse_input('4/2')
        self.assertEqual(out, ['4', '/', '2'])

    def test_parse_plus_minus_multiply_divide(self):
        calc = Calc()
        out = calc.parse_input('4*7+2/4-1')
        self.assertEqual(out, [['4', '*', '7'], '+', [['2', '/', '4'], '-', '1']])

class TestEvaluateFactors(unittest.TestCase):

    def test_evaluate_1_plus_2(self):
        calc = Calc()
        calc.factored = calc.parse_input('1+2')
        out = calc.evaluate_factors()
        self.assertEqual(out, (3,1))

    def test_evaluate_1_plus_2_plus_3(self):
        calc = Calc()
        calc.factored = calc.parse_input('1+2+3')
        out = calc.evaluate_factors()
        self.assertEqual(out, (6,1))

    def test_evaluate_2_minus_1(self):
        calc = Calc()
        calc.factored = calc.parse_input('2-1')
        out = calc.evaluate_factors()
        self.assertEqual(out, (1,1))

    def test_evaluate_1_minus_2(self):
        calc = Calc()
        calc.factored = calc.parse_input('1-2')
        out = calc.evaluate_factors()
        self.assertEqual(out, (-1,1))

    def test_evaluate_2_divided_by_2(self):
        calc = Calc()
        calc.factored = calc.parse_input('2/2')
        out = calc.evaluate_factors()
        self.assertEqual(out, (1,1))

    def test_evaluate_1_divided_by_2(self):
        calc = Calc()
        calc.factored = calc.parse_input('1/2')
        out = calc.evaluate_factors()
        self.assertEqual(out, (1,2))


if __name__ == '__main__':
    unittest.main()
