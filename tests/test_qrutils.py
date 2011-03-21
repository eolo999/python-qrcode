import sys
sys.path.append('..')

from nose.tools import raises

from qrutils import (split_numeric_input,
        split_alphanumeric_input,
        convert_numeric,
        pad,
        to_coeff,
        list_to_coeff
        )

def test_split_numeric_mode():
    assert(split_numeric_input('01234567') == ['012', '345', '67'])
    assert(split_numeric_input('') == [])

def test_split_alphanumeric_mode():
    assert(split_alphanumeric_input([12,34,54,2,23]) == [[12, 34], [54,2],
        [23]])
    assert(split_numeric_input('') == [])

def test_convert_numeric():
    assert(convert_numeric('01234567') == '000000110001010110011000011')

def test_pad():
    assert pad('0101', 5) == '01010'

@raises(Exception)
def test_wrong_pad():
    pad('0101001', 2)

def test_to_coeff():
    assert to_coeff('0') == 0
    assert to_coeff('1') == 1
    assert to_coeff('10') == 2
    assert to_coeff('11') == 3

def test_list_to_coeff():
    assert list_to_coeff(['110', '1001']) == [6, 9]
