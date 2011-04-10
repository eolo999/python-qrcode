# -*- coding: utf-8 -*-
from numpy import array

from qrreference import get_qr_size
from alignment_patterns import get_coordinates

def test(symbol_version):
    symbol_array = position_detection_pattern(symbol_version)
    alignment_pattern(symbol_version, symbol_array)
    symbol_array = timing_pattern(symbol_array)
    return symbol_array

def position_detection_pattern(symbol_version):
    """Assign Position Detection Pattern bits and relative separators.
    """
    side_size = get_qr_size(symbol_version)

    a = array([[9] * side_size] * side_size)
    a[0] = a[6] = [1] * 7 + [0] + [9] * (side_size - 16) + [0] + [1] * 7
    a[1] = a[5] = [1, 0, 0, 0, 0, 0, 1, 0] + [9] * (side_size - 16) + [0] + [1, 0, 0, 0, 0, 0, 1]
    a[2] = a[3] = a[4] = [1, 0, 1, 1, 1, 0, 1, 0] + [9] * (side_size - 16) + [0, 1, 0, 1, 1, 1, 0, 1]
    a[7] = [0] * 8 + [9] * (side_size - 16) + [0] * 8

    a[-8] = [0] * 8 + [9] * (side_size - 8)
    a[-1] = a[-7] = [1] * 7 + [0] + [9] * (side_size - 8)
    a[-2] = a[-6] = [1, 0, 0, 0, 0, 0, 1] + [0] + [9] * (side_size - 8)
    a[-3] = a[-4] = a[-5] = [1, 0, 1, 1, 1, 0, 1]  + [0] + [9] * (side_size - 8)
    return a

def timing_pattern(symbol_array):
    """
    The horizontal and vertical Timing Patterns respectively consist of a one
    module wide row or column of alternating dark and light modules,
    commencing and ending with a dark module. The horizontal Timing Pattern
    runs across row 6 of the symbol between the separators for the upper
    Position Detection Patterns; the vertical Timing Pattern similarly runs
    down column 6 of the symbol between the separators for the left-hand
    Position Detection Patterns.  They enable the symbol density and version
    to be determined and provide datum positions for determining module
    coordinates.
    """
    for i in range(8, symbol_array.shape[0] - 8):
        if i % 2 == 0:
            symbol_array[6][i] = 1
        else:
            symbol_array[6][i] = 0

    symbol_array[:,6] = symbol_array[6]
    print symbol_array
    return symbol_array

def alignment_pattern(symbol_version, symbol_array):
    """
    Each Alignment Pattern may be viewed as three superimposed concentric
    squares and is constructed of dark 5x́5 modules, light 3x3 modules and
    a single central dark module. The number of Alignment Patterns depends on
    the symbol version and they shall be placed in all Model 2 symbols of
    Version 2 or larger in positions defined in Annex E.
    """
    centers = get_coordinates(symbol_version)
    for center in centers:
        symbol_array = draw_alignment_pattern(center, symbol_array)
    return symbol_array

def draw_alignment_pattern(center, symbol_array):
    x, y = center

    symbol_array[x - 2][y - 2:y + 3] = [1, 1, 1, 1, 1]
    symbol_array[x - 1][y - 2:y + 3] = [1, 0, 0, 0, 1]
    symbol_array[x][y - 2:y + 3] =     [1, 0, 1, 0, 1]
    symbol_array[x + 1][y - 2:y + 3] = [1, 0, 0, 0, 1]
    symbol_array[x + 2][y - 2:y + 3] = [1, 1, 1, 1, 1]

    return symbol_array

def encoding_region():
    """
    This region shall contain the symbol characters representing data, those
    representing error correction codewords, the Version Information and
    Format Information. Refer to 8.7.1 for details of the symbol characters.
    Refer to 8.9 for details of the Format Information. Refer to 8.10 for
    details of the Version Information
    """

    data_regions()
    ecc_regions()
    version_information()
    format_information()
    pass

def quiet_zone():
    """
    This is a region 4X wide which shall be free of all other markings,
    surrounding the symbol on all four sides. Its nominal reflectance value
    shall be equal to that of the light modules.
    """

def add_error_correction(data):
    return reed_solomon_code(data)
