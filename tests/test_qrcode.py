import sys
sys.path.append('..')

from nose.tools import raises

from qrcode import Encoder

def test_numeric_encoder():
    e = Encoder('01234567', 'L')
    assert e.code == '000100000010000000001100010101100110000110000'
    e = Encoder('0123456789012345', 'L')
    assert e.code == '000100000100000000001100010101100110101001101110000101001110101001010000'

def test_alphanumeric_encoder():
    e = Encoder('AC-42', 'L', 'alphanumeric')
    assert e.code == '001000000010100111001110111001110010000100000'

def test_till_rs():
    e = Encoder('01234567', 'M', 'numeric')
    s = ''
    for word in e.codewords:
        s += word
    print s
    good = '00010000001000000000110001010110011000011000000011101100000100011110110000010001111011000001000111101100000100011110110000010001'
    assert s == good

@raises(Exception)
def test_pad():
    e = Encoder('12341234123412341234', 'H')
    e.pad()

