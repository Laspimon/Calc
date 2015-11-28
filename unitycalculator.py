#!/usr/bin/python
#-*-coding:utf8-*-
from __future__ import print_function
import unittest, re

class Calc(object):

    def __init__(self):
        self.add = re.compile('\+')
        # Supports division and multiplication with negative numbers: "/-", "*-"
        self.substract = re.compile('(?<!^)(?<!\*)(?<!/)-')
        self.multiply = re.compile('\*')
        self.divide = re.compile('/')
        self.signs = {'+': self.add,
                      '-': self.substract,
                      '*': self.multiply,
                      '/': self.divide}

    def main(self):
        while True:
            inp = ''.join(raw_input(' > ').split(' '))
            factored = self.parse_input(inp)
            print ('  ', self.get_presentable_output(
                self.evaluate_factors(factored)))
            break

    def get_presentable_output(self, evaluated):
        a, b = evaluated
        if b == 1:
            return str(a)
        else:
            return '{} / {}'.format(a,b)


    def parse_input(self, inp, factors = []):
        for f in '+-*/':
            if self.signs[f].search(inp, 1):
                factored = self.signs[f].split(inp, 1)
                factored.insert(1, f)
                factored[0] = self.parse_input(factored[0])
                factored[2] = self.parse_input(factored[2])
                return factored
        else:
            return inp

    def evaluate_factors(self, focus):
        return self.reduce(self.evaluate_factor(focus))

    def evaluate_factor(self, focus):
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
        a = (a[0] * (common_d / a[1]), common_d)
        b = (b[0] * (common_d / b[1]), common_d)
        if sign == '+':
            return a[0] + b[0], common_d
        if sign == '-':
            return a[0] - b[0], common_d
        if sign == '/':
            return a[0] * b[1], a[1] * b[0]
        if sign == '*':
            return a[0] * b[0], a[1] * b[1]

    def find_common_denominator(self, a, b):
        if a[1]%b[1] == 0:
            return a[1]
        elif b[1]%a[1] == 0:
            return b[1]
        else:
            return a[1]*b[1]

    def reduce(self, fraction):
        a, b = fraction
        # Wanting to reduce the fraction, we loop from the denominator and down.
        for guess in range(b, 1, -1):
            if a%guess==0 and b%guess==0:
                a, b = a/guess, b/guess
        # If the denominator is negative. We fix it.
        if b < 0:
            return -a, -b
        return a, b

    def is_number(self, string):
        if string[0] == '-' and len(string)>1: string = string[1:]
        return not False in [ord('0') <= ord(char) <= ord('9') for char in string]

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

    def test_parse_divide_by_negative(self):
        calc = Calc()
        out = calc.parse_input('4/-2')
        self.assertEqual(out, ['4', '/', '-2'])

    def test_parse_plus_minus_multiply_divide(self):
        calc = Calc()
        out = calc.parse_input('4*7+2/4-1')
        self.assertEqual(out, [['4', '*', '7'], '+', [['2', '/', '4'], '-', '1']])

class TestEvaluateFactors(unittest.TestCase):

    def test_evaluate_1_plus_2(self):
        calc = Calc()
        factored = calc.parse_input('1+2')
        out = calc.evaluate_factors(factored)
        self.assertEqual(out, (3,1))

    def test_evaluate_1_plus_2_plus_3(self):
        calc = Calc()
        factored = calc.parse_input('1+2+3')
        out = calc.evaluate_factors(factored)
        self.assertEqual(out, (6,1))

    def test_evaluate_2_minus_1(self):
        calc = Calc()
        factored = calc.parse_input('2-1')
        out = calc.evaluate_factors(factored)
        self.assertEqual(out, (1,1))

    def test_evaluate_1_minus_2(self):
        calc = Calc()
        factored = calc.parse_input('1-2')
        out = calc.evaluate_factors(factored)
        self.assertEqual(out, (-1,1))

    def test_evaluate_2_divided_by_2(self):
        calc = Calc()
        factored = calc.parse_input('2/2')
        out = calc.evaluate_factors(factored)
        self.assertEqual(out, (1,1))

    def test_evaluate_1_divided_by_2(self):
        calc = Calc()
        factored = calc.parse_input('1/2')
        out = calc.evaluate_factors(factored)
        self.assertEqual(out, (1,2))

    def test_evaluate_minus_1_divided_by_minus_2(self):
        calc = Calc()
        factored = calc.parse_input('-1/-2')
        out = calc.evaluate_factors(factored)
        self.assertEqual(out, (1,2))

    def test_evaluate_2_times_2(self):
        calc = Calc()
        factored = calc.parse_input('2*2')
        out = calc.evaluate_factors(factored)
        self.assertEqual(out, (4,1))

    def test_evaluate_1_times_minus_2(self):
        calc = Calc()
        factored = calc.parse_input('1/-2')
        out = calc.evaluate_factors(factored)
        self.assertEqual(out, (-1,2))



if __name__ == '__main__':
    Calc().main()
    #unittest.main()

