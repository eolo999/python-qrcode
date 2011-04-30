from nose.tools import raises

from qrcode.qrcode import Encoder
from qrcode.qrutils import *

def test_qr_size():
    assert qr_size(23) == 109

def test_get_num_of_bits_character_count_indicator():
    assert get_num_of_bits_character_count_indicator(27, 'kanji') == 12
    assert get_num_of_bits_character_count_indicator(1, 'numeric') == 10

@raises(KeyError)
def test_qr_size_wrong_version():
    qr_size(43)

def test_mode_indicators():
    assert mode_indicators('kanji') == '1000'

@raises(KeyError)
def test_get_wrong_mode_indicators():
    mode_indicators('adfasdf')
    assert mode_indicators('kanji') == '1000'

def test_alphanumeric_codes():
    assert alphanumeric_codes('AC-42') == [10,12,41,4,2]

def test_max_char_capacity():
    assert max_char_capacity('alphanumeric', 35, 'Q') == 1867

def test_max_codewords():
    assert max_codewords(1, 'M') == 16

def test_ec_codewords():
    assert ec_codewords(1, 'H') == 17

def test_version_information_5():
    assert version_information(5) == ''

def test_version_information_7():
    version_string = version_information(7)
    result = '000111110010010100'
    assert version_string == result

def test_version_information_8():
    version_string = version_information(8)
    result = '001000010110111100'
    assert version_string == result

@raises(Exception)
def test_determine_symbol_version_exception():
    assert determine_symbol_version('1' * 8000, 'H') == 1

def test_determine_symbol_version():
    assert determine_symbol_version('1', 'H') == 1
    assert determine_symbol_version('1' * 3390, 'M') == 31

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

def test_numeric_reed_solomon():
    a = Encoder('01234567', 'M')
    assert a.codewords == [
            '00010000', '00100000', '00001100', '01010110', '01100001', '10000000',
            '11101100', '00010001', '11101100', '00010001', '11101100', '00010001',
            '11101100', '00010001', '11101100', '00010001']

    assert a.ec_blocks[0][0] == 165

def test_alphanumeric_reed_solomon():
    a = Encoder('abcde123', 'H')
    assert a.ec_blocks[0] == [42, 159, 74, 221, 244, 169, 239, 150,
        138, 70, 237, 85, 224, 96, 74, 219, 61]

    a = Encoder('b'*938, 'L')
    assert len(a.ec_blocks) == 6
    assert len(a.data_blocks[0]) == 107
    assert len(a.data_blocks[1]) == 108

    a = Encoder('a'*60, 'H')
    assert len(a.ec_blocks) == 4
    assert len(a.data_blocks[0]) == 11
    assert len(a.data_blocks[2]) == 12
    assert len(a.final_sequence) == 46 + 88 == 134

def test_8bit():
    a = Encoder('pink@thepallin.org', 'H')
    assert a.final_sequence
