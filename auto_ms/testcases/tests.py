from auto_ms.modules import parse, process
import os
import logging
from pprint import pprint
from math import isclose


def compare_floats(iter1, iter2, abs_tol=0):
    if len(iter1) != len(iter2):
        print("l1, l2 = {}, {}".format(len(iter1), len(iter2)))
        raise Exception("Comparing iterables of different lengths")
    print([(i1, i2) for i1, i2 in zip(iter1, iter2)])
    return [isclose(i1, i2, abs_tol=abs_tol) for i1, i2 in zip(iter1, iter2)]


class TestConsume:
    """
    Tests the basic input parsing and preparation
    """
    def setUp(self):
        self.test_input = 'testdata/d1.dat'

    def test_input_exists(self):
        assert(os.path.exists(self.test_input))

    def test_parse_file(self):
        filepath = os.path.join(os.getcwd(), self.test_input)

        parsed = parse.parse_file(self.test_input)
        # test if the number of lines is correct. Test random
        assert('header' in parsed)
        assert('data' in parsed)
        assert(len(parsed['header']) == 18)
        print(len(parsed['data']))
        assert(len(parsed['data']) == 287)

    def test_parse_header(self):
        parsed = parse.parse_file(self.test_input)
        header = parse.parse_header(parsed['header'])
        assert(len(header['info']) == 8)
        assert(True)

    def test_parse_data(self):
        parsed = parse.parse_file(self.test_input)
        data = parse.parse_data(parsed['data'])
        assert(len(data) == 286)

    def test_process_data(self):
        parsed = parse.parse_file(self.test_input)
        data = parse.parse_data(parsed['data'])
        splat = process.split_data(data)
        assert(sum(len(item) for key, item in splat.items()) == 286)


class TestCalculation:
    def setUp(self):
        self.test_input = 'testdata/d1.dat'
        self.parsed = parse.parse_file(self.test_input)
        self.data = process.subset(parse.parse_data(self.parsed['data']))
        self.split_data = process.split_data(self.data)
        # constants
        self.e_mass = 51.2
        self.moles = 1.80563E-05
        self.dmc = -0.00049552
        self.y_mass = 0

    def test_split_data(self):
        '''
        test if splitting on temperature was successful
        '''
        data = process.split_data(self.data)
        assert(len([i for i in data]) == 11)
        assert(all(len(item) == 26 for key, item in data.items()))

    def test_calculate_chi_emu(self):
        '''
        test computation of chi'
        '''
        chi_p_9 = [1.176521697E+00, 1.180596448E+00, 1.186582442E+00, 1.186887044E+00, 1.185842673E+00, 1.185383415E+00, 1.196762258E+00, 1.182433201E+00, 1.179014453E+00, 1.172666260E+00, 1.161455779E+00, 1.142176100E+00, 1.109916200E+00, 1.060565882E+00, 9.798276582E-01, 8.742521438E-01, 7.420805363E-01, 5.980623825E-01, 4.589033314E-01, 3.400980983E-01, 2.460153759E-01, 1.781820536E-01, 1.328352793E-01, 1.050353970E-01, 8.704781446E-02, 7.949300709E-02]
        chi_pp_9 = [5.79125807E-03, 1.57611883E-02, 1.78999107E-02, 2.32795929E-02, 3.10151403E-02, 4.07936431E-02, 4.99399018E-02, 6.98392529E-02, 9.25013074E-02, 1.22170508E-01, 1.60224904E-01, 2.10839599E-01, 2.71452180E-01, 3.40006994E-01, 4.14694289E-01, 4.76665536E-01, 5.18070850E-01, 5.27697675E-01, 5.03510295E-01, 4.50508070E-01, 3.84649542E-01, 3.15148936E-01, 2.50025191E-01, 1.96101544E-01, 1.51325664E-01, 1.18261640E-01]
        print([i for i in self.split_data])
        output = process.calculate_chi(self.split_data[9.0], self.e_mass, self.y_mass,
                                       self.moles, self.dmc)
        logging.debug(output)
        logging.debug([len(i) for k, i in output.items()])
        logging.debug(len(chi_p_9))
        logging.debug(chi_p_9[:5])
        logging.debug(output["chi' (emu)"][:5])
        # test chi'
        cur_chi = output["chi' (emu)"]
        compared = compare_floats(chi_p_9, cur_chi, abs_tol=1.0E-5)
        compared_fail = compare_floats(chi_p_9, cur_chi, abs_tol=1.0E-10)
        print(compared)
        assert(all(compared))
        assert(not all(compared_fail))

        # test chi''
        cur_chi = output['chi" (emu)']
        compared = compare_floats(chi_pp_9, cur_chi, abs_tol=1.0E-5)
        compared_fail = compare_floats(chi_pp_9, cur_chi, abs_tol=1.0E-10)
        print(compared)
        assert(all(compared))
        assert(not all(compared_fail))

    def test_calculate_chi_fit(self):
        pass

    def test_optimize_chi_fit(self):
        pass