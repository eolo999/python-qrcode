import sys
sys.path.append('..')

from array import array
from nose.tools import raises

from qrcode import Encoder
from qrutils import (
        split_numeric_input,
        split_alphanumeric_input,
        convert_numeric,
        pad,
        to_coeff,
        list_to_coeff)

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

def test_reed_solomon():
    a = Encoder('abcde123', 1, 'H', 'alphanumeric')
    assert a.ec_blocks[0] == array('i', [42, 159, 74, 221, 244, 169, 239, 150,
        138, 70, 237, 85, 224, 96, 74, 219, 61])

    a = Encoder('01234567', 1, 'M', 'numeric')
    assert a.codewords == [
            '00010000', '00100000', '00001100', '01010110', '01100001', '10000000',
            '11101100', '00010001', '11101100', '00010001', '11101100', '00010001',
            '11101100', '00010001', '11101100', '00010001']

    assert a.ec_blocks[0][0] == 165

    a = Encoder('b'*938, 17, 'L', 'alphanumeric')
    assert len(a.ec_blocks) == 6
    assert len(a.data_blocks[0]) == 107
    assert len(a.data_blocks[1]) == 108

    a = Encoder('a'*60, 5, 'H', 'alphanumeric')
    assert len(a.ec_blocks) == 4
    assert len(a.data_blocks[0]) == 11
    assert len(a.data_blocks[2]) == 12
    assert len(a.final_sequence) == 46 + 88 == 134

    return a
