# -*- coding: utf-8 -*-
from string import ascii_uppercase, digits, upper

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

# cannot enumerate because i need to lookup by char and not by number
alphanumeric_char_values = dict([(x[1], x[0]) for x in enumerate(digits +
    ascii_uppercase + ' $%*+-./:')])

# 1. Divide the data codeword sequence into n blocks as defined in Tables 13
# to 22 according to the version and error correction level.

# Number of symbol characters and input data capacity for versions 1 to 8
max_codewords = {
        1:  {
            'data_codewords': {'L': 19, 'M': 16, 'Q': 13, 'H': 9},
            'ec_codewords':   {'L': 7, 'M': 10, 'Q': 13, 'H': 17}
            },
        2:  {
            'data_codewords': {'L': 34, 'M': 28, 'Q': 22, 'H': 16},
            'ec_codewords':   {'L': 10, 'M': 16, 'Q': 22, 'H': 28}
            },
        3:  {
            'data_codewords': {'L': 55, 'M': 44, 'Q': 34, 'H': 26},
            'ec_codewords':   {'L': 15, 'M': 26, 'Q': 36, 'H': 44}
            },
        4:  {'data_codewords': {'L': 80, 'M': 64, 'Q': 48, 'H': 36},
            'ec_codewords': {}},
        5:  {'data_codewords': {'L': 108, 'M': 86, 'Q': 62, 'H': 46},
            'ec_codewords': {}},
        6:  {'data_codewords': {'L': 136, 'M': 108, 'Q': 76, 'H': 60},
            'ec_codewords': {}},
        7:  {'data_codewords': {'L': 156, 'M': 124, 'Q': 88, 'H': 66},
            'ec_codewords': {}},
        8:  {'data_codewords': {'L': 194, 'M': 154, 'Q': 110, 'H': 86},
            'ec_codewords': {}},
        9:  {'data_codewords': {'L': 232, 'M': 182, 'Q': 132, 'H': 100},
            'ec_codewords': {}},
        10: {'data_codewords': {'L': 274, 'M': 216, 'Q': 154, 'H': 122},
            'ec_codewords': {}},
        11: {'data_codewords': {'L': 324, 'M': 254, 'Q': 180, 'H': 140},
            'ec_codewords': {}},
        12: {'data_codewords': {'L': 370, 'M': 290, 'Q': 206, 'H': 158},
            'ec_codewords': {}},
        13: {'data_codewords': {'L': 428, 'M': 334, 'Q': 244, 'H': 180},
            'ec_codewords': {}},
        14: {'data_codewords': {'L': 461, 'M': 365, 'Q': 261, 'H': 197},
            'ec_codewords': {}},
        15: {'data_codewords': {'L': 523, 'M': 415, 'Q': 295, 'H': 223},
            'ec_codewords': {}},
        16: {'data_codewords': {'L': 589, 'M': 453, 'Q': 325, 'H': 253},
            'ec_codewords': {}},
        17: {'data_codewords': {'L': 647, 'M': 507, 'Q': 367, 'H': 283},
            'ec_codewords': {}},
        18: {'data_codewords': {'L': 721, 'M': 563, 'Q': 397, 'H': 313},
            'ec_codewords': {}},
        19: {'data_codewords': {'L': 795, 'M': 627, 'Q': 445, 'H': 341},
            'ec_codewords': {}},
        20: {'data_codewords': {'L': 861, 'M': 669, 'Q': 485, 'H': 385},
            'ec_codewords': {}},
        21: {'data_codewords': {'L': 721, 'M': 563, 'Q': 397, 'H': 313},
            'ec_codewords': {}},
        22: {'data_codewords': {'L': 721, 'M': 563, 'Q': 397, 'H': 313},
            'ec_codewords': {}},
        23: {'data_codewords': {'L': 721, 'M': 563, 'Q': 397, 'H': 313},
            'ec_codewords': {}},
        24: {'data_codewords': {'L': 721, 'M': 563, 'Q': 397, 'H': 313},
            'ec_codewords': {}},
        25: {'data_codewords': {'L': 721, 'M': 563, 'Q': 397, 'H': 313},
            'ec_codewords': {}},
        26: {'data_codewords': {'L': 721, 'M': 563, 'Q': 397, 'H': 313},
                'ec_codewords': {}},
        27: {'data_codewords': {'L': 721, 'M': 563, 'Q': 397, 'H': 313},
                'ec_codewords': {}},
        28: {'data_codewords': {'L': 721, 'M': 563, 'Q': 397, 'H': 313},
                'ec_codewords': {}},
        29: {'data_codewords': {'L': 721, 'M': 563, 'Q': 397, 'H': 313},
                'ec_codewords': {}},
        30: {'data_codewords': {'L': 721, 'M': 563, 'Q': 397, 'H': 313},
                'ec_codewords': {}},
        31: {'data_codewords': {'L': 721, 'M': 563, 'Q': 397, 'H': 313},
                'ec_codewords': {}},
        32: {'data_codewords': {'L': 721, 'M': 563, 'Q': 397, 'H': 313},
                'ec_codewords': {}},
        33: {'data_codewords': {'L': 721, 'M': 563, 'Q': 397, 'H': 313},
                'ec_codewords': {}},
        34: {'data_codewords': {'L': 721, 'M': 563, 'Q': 397, 'H': 313},
                'ec_codewords': {}},
        35: {'data_codewords': {'L': 721, 'M': 563, 'Q': 397, 'H': 313},
                'ec_codewords': {}},
        36: {'data_codewords': {'L': 721, 'M': 563, 'Q': 397, 'H': 313},
                'ec_codewords': {}},
        37: {'data_codewords': {'L': 721, 'M': 563, 'Q': 397, 'H': 313},
                'ec_codewords': {}},
        38: {'data_codewords': {'L': 721, 'M': 563, 'Q': 397, 'H': 313},
                'ec_codewords': {}},
        39: {'data_codewords': {'L': 721, 'M': 563, 'Q': 397, 'H': 313},
                'ec_codewords': {}},
        40: {'data_codewords': {'L': 721, 'M': 563, 'Q': 397, 'H': 313},
                'ec_codewords': {}}
        }
def get_max_codewords(version, ecl):
    return max_codewords[version]['data_codewords'][ecl]

def get_ec_codewords(version, ecl):
    return max_codewords[version]['ec_codewords'][ecl]

def get_max_databits(version, ecl):
    return get_max_codewords(version, ecl) * 8

def get_mode_indicators(data_mode):
    return mode_indicators[data_mode]

def get_num_of_bits_character_count_indicator(version, data_mode):
    return num_of_bits_character_count_indicator[version][data_mode]

def get_qr_size(version):
    return symbol_sizes[version]

def alphanumeric_codes(input):
    codes = []
    for ch in input:
        codes.append(alphanumeric_char_values[upper(ch)])
    return codes


