import sys
sys.path.append('..')

from nose.tools import raises

from error_correction import blocks_per_ecl, get_blocks
from qrreference import *

def test_qr_size():
    assert get_qr_size(23) == 109

def test_get_num_of_bits_character_count_indicator():
    assert get_num_of_bits_character_count_indicator(27, 'kanji') == 12
    assert get_num_of_bits_character_count_indicator(1, 'numeric') == 10

@raises(KeyError)
def test_qr_size_wrong_version():
    get_qr_size(43)

def test_get_mode_indicators():
    assert get_mode_indicators('kanji') == '1000'

@raises(KeyError)
def test_get_wrong_mode_indicators():
    get_mode_indicators('adfasdf')
    assert get_mode_indicators('kanji') == '1000'

def test_alphanumeric_codes():
    assert alphanumeric_codes('AC-42') == [10,12,41,4,2]

def test_get_max_codewords():
    assert get_max_codewords(1, 'M') == 16

def test_get_ec_codewords():
    assert get_ec_codewords(1, 'H') == 17

def test_block_per_ecl_lengths():
    for key in blocks_per_ecl:
        assert len(blocks_per_ecl[key]) == 4

def test_split():
    assert get_blocks(1, 'L') == [19]
