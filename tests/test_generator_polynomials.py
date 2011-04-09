import sys
sys.path.append('..')

from rs_generator_polynomials import generator_polynomials

def test_generator_polynomials_length():
    for key in generator_polynomials:
        assert len(generator_polynomials[key]) == key + 1

