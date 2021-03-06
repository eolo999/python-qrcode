#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This module handles the displacement of data and Function Patterns of a
qrcode inside a numpy array."""

from numpy import array, rot90

from qrreference import ecl_indicators, symbol_version_data

from qrutils import qr_size, list_to_bin, bch_15_5

from alignment_patterns import get_coordinates

LEGENDA = {
        0: 'light encoding region module',
        1: 'dark encoding region module',
        6: 'light function pattern module',
        7: 'dark function pattern module',
        8: 'format information area',
        9: 'unassigned bit',
        }


def make_array(code):
    """Given a qrcode.Encoder object it returns a complete qrcode array."""
    symbol_array = position_detection_pattern(code.symbol_version)
    symbol_array = alignment_pattern(code.symbol_version, symbol_array)
    symbol_array = timing_pattern(symbol_array)
    if code.symbol_version >= 7:
        symbol_array = version_information_positioning(symbol_array,
                code.version_information)
    symbol_array = protect_format_info_modules(symbol_array)
    unmasked_array = place_data(code, symbol_array)
    masked_array, mask_pattern = apply_masking(unmasked_array)
    final_array = format_information(masked_array,
            code.error_correction_level, mask_pattern)
    return final_array


def apply_masking(unmasked_array):
    """Given an unmasked array returns the masked array and the mask
    pattern. I omit the best mask selection to generate the first symbol.
    I choose to apply '000' masking."""
    for i in range(len(unmasked_array[0])):
        for j in range(len(unmasked_array[0])):
            if (i + j) % 2 == 0:
                if unmasked_array[i][j] == 0:
                    unmasked_array[i][j] = 1
                elif unmasked_array[i][j] == 1:
                    unmasked_array[i][j] = 0
    return unmasked_array, '000'

def format_information(masked_array, ecl, mask_pattern):
    """Place format information in symbol; returns the final array, no further
    operations."""
    format_information_data = bch_15_5(ecl_indicators[ecl] + mask_pattern)
    format_information_data = [int(x) for x in list(format_information_data)]
    # place format_information_data in symbol
    masked_array[:, 8][:6] = format_information_data[:6]
    masked_array[:, 8][7:9] = format_information_data[6:8]
    masked_array[:, 8][-7:] = format_information_data[8:]
    format_information_data.reverse()
    masked_array[8][:6] = format_information_data[:6]
    masked_array[8][7:9] = format_information_data[6:8]
    masked_array[8][-8:] = format_information_data[7:]

    return masked_array

def protect_format_info_modules(symbol_array):
    """Set all format information modules to 8 so that they are not
    overwritten by data placement (which checks that module value is 9 before
    it place data). This is just to quicken the route to have a final symbol to
    test with a decoder. Rewriting will come at that point."""
    symbol_array[:, 8][:6] = 8
    symbol_array[:, 8][7:9] = 8
    symbol_array[8][:6] = 8
    symbol_array[8][7] = 8
    symbol_array[8][-8:] = 8
    symbol_array[:, 8][-7:] = 8
    # It is not clear if this module is always black
    # cfr. ISO/IEC 18004 Fig. 19
    symbol_array[:, 8][-8] = 6
    return symbol_array


def place_data(code, symbol_array):
    """An alternative method for placement in the symbol, which yields the
    same result, is to regard the interleaved codeword sequence as a single
    bit stream, which is placed (starting with the most significant bit) in
    the two-module wide columns alternately upwards and downwards from the
    right to left of the symbol. In each column the bits are placed
    alternately in the right and left modules, moving upwards or downwards
    according to the direction of placement and skipping areas occupied by
    function patterns, changing direction at the top or bottom of the column.
    Each bit shall always be placed in the first available module position.
    """
    # Rotate the array 180 degrees so that data positioning start from
    # symbol_array[0][0]
    symbol_array = rot90(symbol_array, 2)
    flat_data_list = list("".join(list_to_bin(code.final_sequence))) + ([0] *
            symbol_version_data[code.symbol_version]['remainder_bits'])
    top = 0
    bottom = qr_size(code.symbol_version) - 1
    direction = 1
    left_column = 0
    row = 0
    column = 0
    while flat_data_list:
        # If we have reached top or bottom margins
        if direction == 1:
            if row > bottom:
                # reset row to bottom index
                row = bottom
                # shift by 2 columns
                left_column += 2
                column = left_column
                # invert direction
                direction *= -1
        else:
            if row < top:
                # reset row to top index
                row = top
                left_column += 2
                column = left_column
                direction *= -1

        try:
            if symbol_array[row][column] == 9:
                data = flat_data_list.pop(0)
                symbol_array[row][column] = data
        except IndexError:
            pass

        if column % 2 == 0:
            column += 1
        else:
            column = left_column
            row += 1 * direction

    # rotate back the symbol
    return rot90(symbol_array, 2)


def pbm_image(symbol_size, symbol_array):
    """Creates a pbm given a symbol size and a qrcode array."""
    with open('test.pbm', 'w') as output_file:
        output_file.writelines([
            'P1\n',
            " ".join([str(symbol_size), str(symbol_size), '\n'])
             ])
        for arr in symbol_array:
            for module in arr:
                if module == 9:
                    module = 0
                output_file.write("".join([str(module), ' ']))
            output_file.write('\n')
    return True

def version_information_positioning(symbol_array, version_information):
    """Place version information data in the proper array modules."""
    change_bits = ''
    for module in version_information:
        if module == '0':
            change_bits += '6'
        else:
            change_bits += '7'
    version_information = change_bits

    symbol_array[0][-11] = symbol_array[-11][0] = version_information[0]
    symbol_array[0][-10] = symbol_array[-10][0] = version_information[1]
    symbol_array[0][-9] = symbol_array[-9][0] = version_information[2]
    symbol_array[1][-11] = symbol_array[-11][1] = version_information[3]
    symbol_array[1][-10] = symbol_array[-10][1] = version_information[4]
    symbol_array[1][-9] = symbol_array[-9][1] = version_information[5]
    symbol_array[2][-11] = symbol_array[-11][2] = version_information[6]
    symbol_array[2][-10] = symbol_array[-10][2] = version_information[7]
    symbol_array[2][-9] = symbol_array[-9][2] = version_information[8]
    symbol_array[3][-11] = symbol_array[-11][3] = version_information[9]
    symbol_array[3][-10] = symbol_array[-10][3] = version_information[10]
    symbol_array[3][-9] = symbol_array[-9][3] = version_information[11]
    symbol_array[4][-11] = symbol_array[-11][4] = version_information[12]
    symbol_array[4][-10] = symbol_array[-10][4] = version_information[13]
    symbol_array[4][-9] = symbol_array[-9][4] = version_information[14]
    symbol_array[5][-11] = symbol_array[-11][5] = version_information[15]
    symbol_array[5][-10] = symbol_array[-10][5] = version_information[16]
    symbol_array[5][-9] = symbol_array[-9][5] = version_information[17]
    return symbol_array


def position_detection_pattern(symbol_version):
    """Assign Position Detection Pattern bits and relative separators."""
    side_size = qr_size(symbol_version)

    arr = array([[9] * side_size] * side_size)
    arr[0] = arr[6] = [7] * 7 + [6] + [9] * (side_size - 16) + [6] + [7] * 7
    arr[1] = arr[5] = ([7, 6, 6, 6, 6, 6, 7, 6] +
            [9] * (side_size - 16) +
            [6, 7, 6, 6, 6, 6, 6, 7])
    arr[2] = arr[3] = arr[4] = ([7, 6, 7, 7, 7, 6, 7, 6] +
            [9] * (side_size - 16) +
            [6, 7, 6, 7, 7, 7, 6, 7])
    arr[7] = [6] * 8 + [9] * (side_size - 16) + [6] * 8

    arr[-8] = [6] * 8 + [9] * (side_size - 8)
    arr[-1] = arr[-7] = [7] * 7 + [6] + [9] * (side_size - 8)
    arr[-2] = arr[-6] = [7, 6, 6, 6, 6, 6, 7, 6] + [9] * (side_size - 8)
    arr[-3] = arr[-4] = arr[-5] = ([7, 6, 7, 7, 7, 6, 7, 6] +
            [9] * (side_size - 8))
    return arr

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
            symbol_array[6][i] = 7
        else:
            symbol_array[6][i] = 6

    symbol_array[:, 6] = symbol_array[6]
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
    """Actually set alignment modules in a qrcode array."""
    x_coord, y_coord = center

    symbol_array[x_coord - 2][y_coord - 2:y_coord + 3] = [7, 7, 7, 7, 7]
    symbol_array[x_coord - 1][y_coord - 2:y_coord + 3] = [7, 6, 6, 6, 7]
    symbol_array[x_coord][y_coord - 2:y_coord + 3] =     [7, 6, 7, 6, 7]
    symbol_array[x_coord + 1][y_coord - 2:y_coord + 3] = [7, 6, 6, 6, 7]
    symbol_array[x_coord + 2][y_coord - 2:y_coord + 3] = [7, 7, 7, 7, 7]

    return symbol_array


def quiet_zone():
    """
    This is a region 4X wide which shall be free of all other markings,
    surrounding the symbol on all four sides. Its nominal reflectance value
    shall be equal to that of the light modules.
    """
