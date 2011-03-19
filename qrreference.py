# -*- coding: utf-8 -*-

from nose.tools import raises

symbol_versions = [(n+1) for n in range(40)]
side_lengths = range(21, 181, 4)

# 21x21 modules to 177x177 modules
# (Versions 1 to 40, increasing in steps of 4 modules per side)
symbol_sizes = dict(zip(symbol_versions, side_lengths))
num_of_bits_character_count_indicator = {}

for version in symbol_versions:
    num_of_bits_character_count_indicator[version] = {}
    if 1 <= version <= 9:
        num_of_bits_character_count_indicator[version]['numeric'] = 10
        num_of_bits_character_count_indicator[version]['alphanumeric'] = 9
        num_of_bits_character_count_indicator[version]['8bit'] = 8
        num_of_bits_character_count_indicator[version]['kanji'] = 8
    elif 10 <= version <= 26:
        num_of_bits_character_count_indicator[version]['numeric'] = 12
        num_of_bits_character_count_indicator[version]['alphanumeric'] = 11
        num_of_bits_character_count_indicator[version]['8bit'] = 16
        num_of_bits_character_count_indicator[version]['kanji'] = 10
    elif 27 <= version <= 40:
        num_of_bits_character_count_indicator[version]['numeric'] = 14
        num_of_bits_character_count_indicator[version]['alphanumeric'] = 13
        num_of_bits_character_count_indicator[version]['8bit'] = 16
        num_of_bits_character_count_indicator[version]['kanji'] = 12

mode_indicators = {
        'ECI': '0111',
        'numeric': '0001',
        'alphanumeric': '0010',
        '8bit': '0100',
        'kanji': '1000',
        'structured_append': '0011',
        'fnc1': ['0101', '1001'],
        'terminator': '0000'
        }

def get_mode_indicators(data_mode):
    return mode_indicators[data_mode]

def get_num_of_bits_character_count_indicator(version, data_mode):
    return num_of_bits_character_count_indicator[version][data_mode]

def get_qr_size(version):
    return symbol_sizes[version]


### TEST

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

