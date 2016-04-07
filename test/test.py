from nose.tools import assert_equal, assert_raises

from calc.calc import *

class TestParseInput(object):
    def test_parse_plus(self):
        calc = Calc()
        out = calc.parse_input('1+2')
        assert_equal(out, ['1', '+', '2'])

    def test_parse_minus(self):
        calc = Calc()
        out = calc.parse_input('3-2')
        assert_equal(out, ['3', '-', '2'])

    def test_parse_multiply(self):
        calc = Calc()
        out = calc.parse_input('1*2')
        assert_equal(out, ['1', '*', '2'])

    def test_parse_divide(self):
        calc = Calc()
        out = calc.parse_input('4/2')
        assert_equal(out, ['4', '/', '2'])

    def test_parse_divide_by_negative(self):
        calc = Calc()
        out = calc.parse_input('4/-2')
        assert_equal(out, ['4', '/', '-2'])

    def test_parse_plus_minus_multiply_divide(self):
        calc = Calc()
        out = calc.parse_input('4*7+2/4-1')
        assert_equal(out, [['4', '*', '7'],'+',[['2', '/', '4'],'-','1']])

class TestEvaluateFactors(object):
    def test_evaluate_1_plus_2(self):
        calc = Calc()
        factored = calc.parse_input('1+2')
        out = calc.evaluate_factors(factored)
        assert_equal(out, (3,1))

    def test_evaluate_1_plus_2_plus_3(self):
        calc = Calc()
        factored = calc.parse_input('1+2+3')
        out = calc.evaluate_factors(factored)
        assert_equal(out, (6,1))

    def test_evaluate_2_minus_1(self):
        calc = Calc()
        factored = calc.parse_input('2-1')
        out = calc.evaluate_factors(factored)
        assert_equal(out, (1,1))

    def test_evaluate_1_minus_2(self):
        calc = Calc()
        factored = calc.parse_input('1-2')
        out = calc.evaluate_factors(factored)
        assert_equal(out, (-1,1))

    def test_evaluate_2_divided_by_2(self):
        calc = Calc()
        factored = calc.parse_input('2/2')
        out = calc.evaluate_factors(factored)
        assert_equal(out, (1,1))

    def test_evaluate_1_divided_by_2(self):
        calc = Calc()
        factored = calc.parse_input('1/2')
        out = calc.evaluate_factors(factored)
        assert_equal(out, (1,2))

    def test_evaluate_minus_1_divided_by_minus_2(self):
        calc = Calc()
        factored = calc.parse_input('-1/-2')
        out = calc.evaluate_factors(factored)
        assert_equal(out, (1,2))

    def test_evaluate_2_times_2(self):
        calc = Calc()
        factored = calc.parse_input('2*2')
        out = calc.evaluate_factors(factored)
        assert_equal(out, (4,1))

    def test_evaluate_1_times_minus_2(self):
        calc = Calc()
        factored = calc.parse_input('1/-2')
        out = calc.evaluate_factors(factored)
        assert_equal(out, (-1,2))

    def test_evaluate_no_input(self):
        calc = Calc()
        assert_raises(ValueError,
                          partial(calc.parse_input, ''))

    def test_evaluate_divide_by_zero(self):
        calc = Calc()
        assert_raises(ValueError,
                          partial(calc.parse_input, '1/0'))

    def test_evaluate_divide_nothing_by_1(self):
        calc = Calc()
        assert_raises(ValueError,
                          partial(calc.parse_input, '/1'))

class TestGetPresentableOutput(object):
    def test_presentable_1_over_4(self):
        calc = Calc()
        factored = calc.parse_input('1/4')
        evaled = calc.evaluate_factors(factored)
        out = calc.get_presentable_output(evaled)
        assert_equal(out, '1 / 4')

    def test_presentable_20_over_2(self):
        calc = Calc()
        factored = calc.parse_input('20/2')
        evaled = calc.evaluate_factors(factored)
        out = calc.get_presentable_output(evaled)
        assert_equal(out, '10 / 1')
        # This could be reduced further, but would no longer be a fraction.
        #assert_equal(out, '10')

