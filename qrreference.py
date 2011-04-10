# -*- coding: utf-8 -*-
from string import ascii_uppercase, digits, upper

symbol_versions = [(n+1) for n in range(40)]
side_lengths = range(21, 181, 4)

# 21x21 modules to 177x177 modules
# (Versions 1 to 40, increasing in steps of 4 modules per side)
# ISO/IEC 18004 - Table 1 (partial)
symbol_sizes = dict(zip(symbol_versions, side_lengths))

# ISO/IEC 18004 - Table 3
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

# ISO/IEC 18004 - Table 2
mode_indicators = {
        'ECI': '0111',
        'numeric': '0001',
        'alphanumeric': '0010',
        '8bit': '0100',
        'kanji': '1000',
        'structured_append': '0011',
        'fnc1': ['0101', '1001'],
        }

# ISO/IEC 18004 - Table 5
alphanumeric_char_values = dict([(x[1], x[0]) for x in enumerate(digits +
    ascii_uppercase + ' $%*+-./:')])

# ISO/IEC 18004 - Table 1 (partial) and Table 7 (partial)
symbol_version_data = {
        1:  {
            'data_capacity': 26,
            'data_codewords': {'L': 19, 'M': 16, 'Q': 13, 'H': 9},
            'remainder_bits': 0},
        2:  {
            'data_capacity': 44,
            'data_codewords': {'L': 34, 'M': 28, 'Q': 22, 'H': 16},
            'remainder_bits': 7},
        3:  {
            'data_capacity': 70,
            'data_codewords': {'L': 55, 'M': 44, 'Q': 34, 'H': 26},
            'remainder_bits': 7,
            },
        4:  {
            'data_capacity': 100,
            'data_codewords': {'L': 80, 'M': 64, 'Q': 48, 'H': 36},
            'remainder_bits': 7,
            },
        5:  {
            'data_capacity': 134,
            'data_codewords': {'L': 108, 'M': 86, 'Q': 62, 'H': 46},
            'remainder_bits': 7,
            },
        6:  {
            'data_capacity': 172,
            'data_codewords': {'L': 136, 'M': 108, 'Q': 76, 'H': 60},
            'remainder_bits': 7,
            },
        7:  {
            'data_capacity': 196,
            'data_codewords': {'L': 156, 'M': 124, 'Q': 88, 'H': 66},
            'remainder_bits': 0,
            },
        8:  {
            'data_capacity': 242,
            'data_codewords': {'L': 194, 'M': 154, 'Q': 110, 'H': 86},
            'remainder_bits': 0,
            },
        9:  {
            'data_capacity': 292,
            'data_codewords': {'L': 232, 'M': 182, 'Q': 132, 'H': 100},
            'remainder_bits': 0,
            },
        10: {
            'data_capacity': 346,
            'data_codewords': {'L': 274, 'M': 216, 'Q': 154, 'H': 122},
            'remainder_bits': 0,
            },
        11: {
            'data_capacity': 404,
            'data_codewords': {'L': 324, 'M': 254, 'Q': 180, 'H': 140},
            'remainder_bits': 0,
            },
        12: {
            'data_capacity': 466,
            'data_codewords': {'L': 370, 'M': 290, 'Q': 206, 'H': 158},
            'remainder_bits': 0,
            },
        13: {
            'data_capacity': 532,
            'data_codewords': {'L': 428, 'M': 334, 'Q': 244, 'H': 180},
            'remainder_bits': 0,
            },
        14: {
            'data_capacity': 581,
            'data_codewords': {'L': 461, 'M': 365, 'Q': 261, 'H': 197},
            'remainder_bits': 3,
            },
        15: {
            'data_capacity': 655,
            'data_codewords': {'L': 523, 'M': 415, 'Q': 295, 'H': 223},
            'remainder_bits': 3,
            },
        16: {
            'data_capacity': 733,
            'data_codewords': {'L': 589, 'M': 453, 'Q': 325, 'H': 253},
            'remainder_bits': 3,
            },
        17: {
            'data_capacity': 815,
            'data_codewords': {'L': 647, 'M': 507, 'Q': 367, 'H': 283},
            'remainder_bits': 3,
            },
        18: {
            'data_capacity': 901,
            'data_codewords': {'L': 721, 'M': 563, 'Q': 397, 'H': 313},
            'remainder_bits': 3,
            },
        19: {
            'data_capacity': 991,
            'data_codewords': {'L': 795, 'M': 627, 'Q': 445, 'H': 341},
            'remainder_bits': 3,
            },
        20: {
            'data_capacity': 1085,
            'data_codewords': {'L': 861, 'M': 669, 'Q': 485, 'H': 385},
            'remainder_bits': 3,
            },
        21: {
            'data_capacity': 1156,
            'data_codewords': {'L': 932, 'M': 714, 'Q': 512, 'H': 406},
            'remainder_bits': 4,
            },
        22: {
            'data_capacity': 1258,
            'data_codewords': {'L': 1006, 'M': 782, 'Q': 568, 'H': 442},
            'remainder_bits': 4,
            },
        23: {
            'data_capacity': 1364,
            'data_codewords': {'L': 1094, 'M': 860, 'Q': 614, 'H': 464},
            'remainder_bits': 4,
            },
        24: {
            'data_capacity': 1474,
            'data_codewords': {'L': 1174, 'M': 914, 'Q': 664, 'H': 514},
            'remainder_bits': 4,
            },
        25: {
            'data_capacity': 1588,
            'data_codewords': {'L': 1276, 'M': 1000, 'Q': 718, 'H': 538},
            'remainder_bits': 4,
            },
        26: {
            'data_capacity': 1706,
            'data_codewords': {'L': 1370, 'M': 1062, 'Q': 754, 'H': 596},
            'remainder_bits': 4,
            },
        27: {
            'data_capacity': 1828,
            'data_codewords': {'L': 1468, 'M': 1128, 'Q': 808, 'H': 628},
            'remainder_bits': 4,
            },
        28: {
            'data_capacity': 1921,
            'data_codewords': {'L': 1531, 'M': 1193, 'Q': 871, 'H': 661},
            'remainder_bits': 3,
            },
        29: {
            'data_capacity': 2051,
            'data_codewords': {'L': 1631, 'M': 1267, 'Q': 911, 'H': 701},
            'remainder_bits': 3,
            },
        30: {
            'data_capacity': 2185,
            'data_codewords': {'L': 1735, 'M': 1373, 'Q': 985, 'H': 745},
            'remainder_bits': 3,
            },
        31: {
            'data_capacity': 2323,
            'data_codewords': {'L': 1843, 'M': 1455, 'Q': 1033, 'H': 793},
            'remainder_bits': 3,
            },
        32: {
            'data_capacity': 2465,
            'data_codewords': {'L': 1955, 'M': 1541, 'Q': 1115, 'H': 845},
            'remainder_bits': 3,
            },
        33: {
            'data_capacity': 2611,
            'data_codewords': {'L': 2071, 'M': 1631, 'Q': 1171, 'H': 901},
            'remainder_bits': 3,
            },
        34: {
            'data_capacity': 2761,
            'data_codewords': {'L': 2191, 'M': 1725, 'Q': 1231, 'H': 961},
            'remainder_bits': 3,
            },
        35: {
            'data_capacity': 2876,
            'data_codewords': {'L': 2306, 'M': 1812, 'Q': 1286, 'H': 986},
            'remainder_bits': 0,
            },
        36: {
            'data_capacity': 3034,
            'data_codewords': {'L': 2434, 'M': 1914, 'Q': 1354, 'H': 1054},
            'remainder_bits': 0,
            },
        37: {
            'data_capacity': 3196,
            'data_codewords': {'L': 2566, 'M': 1992, 'Q': 1426, 'H': 1096},
            'remainder_bits': 0,
            },
        38: {
            'data_capacity': 3362,
            'data_codewords': {'L': 2702, 'M': 2102, 'Q': 1502, 'H': 1142},
            'remainder_bits': 0,
            },
        39: {
            'data_capacity': 3532,
            'data_codewords': {'L': 2812, 'M': 2216, 'Q': 1582, 'H': 1222},
            'remainder_bits': 0,
            },
        40: {
            'data_capacity': 3706,
            'data_codewords': {'L': 2956, 'M': 2334, 'Q': 1666, 'H': 1276},
            'remainder_bits': 0,
            }
        }

# ISO/IEC 18004 - Table 7 (partial)
# TODO: should be completed when I'll implement an automatic symbol version
# chooser based on input string
max_char_capacity = {
        'numeric': {
            1: {'L': 41, 'M': 34, 'Q': 27, 'H': 17},
            2: {'L': 77, 'M': 63, 'Q': 48, 'H': 34},
            3: {'L': 127, 'M': 101, 'Q': 77, 'H': 58},
            4: {'L': 187, 'M': 149, 'Q': 111, 'H': 82},
            5: {'L': 255, 'M': 202, 'Q': 144, 'H': 106},
            },
        'alphanumeric': {
            1: {'L': 25, 'M': 20, 'Q': 16, 'H': 10},
            2: {'L': 47, 'M': 30, 'Q': 29, 'H': 20},
            3: {'L': 77, 'M': 61, 'Q': 47, 'H': 35},
            4: {'L': 114, 'M': 90, 'Q': 67, 'H': 50},
            5: {'L': 154, 'M': 122, 'Q': 87, 'H': 64},
            },
        }


def get_max_codewords(version, ecl):
    return symbol_version_data[version]['data_codewords'][ecl]

def get_ec_codewords(version, ecl):
    return (
            symbol_version_data[version]['data_capacity'] -
            symbol_version_data[version]['data_codewords'][ecl])

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

