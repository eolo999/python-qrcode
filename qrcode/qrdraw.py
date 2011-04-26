#!/usr/bin/python
# -*- coding: utf-8 -*-

from numpy import array, rot90, poly1d

from qrreference import ecl_indicators

from qrutils import make_image, qr_size, list_to_bin, to_binstring, to_coeff

from qrcode import Encoder

from alignment_patterns import get_coordinates

legenda = {
        0: 'light encoding region module',
        1: 'dark encoding region module',
        6: 'light function pattern module',
        7: 'dark function pattern module',
        8: 'format information area',
        9: 'unassigned bit',
        }


def test():
    code = Encoder('1' * 368, 'L')
    symbol_array = position_detection_pattern(code.symbol_version)
    symbol_array = alignment_pattern(code.symbol_version, symbol_array)
    symbol_array = timing_pattern(symbol_array)
    if code.symbol_version >= 7:
        symbol_array = version_information_positioning(symbol_array,
                code.version_information)
    symbol_array = leave_space_for_format_information(symbol_array)
    unmasked_array = place_data(code, symbol_array)
    masked_array, mask_pattern = apply_masking(unmasked_array)
    final_array = format_information(masked_array,
            code.error_correction_level, mask_pattern)

    make_image(final_array, zoom=4)
    #pbm_image(qr_size(code.symbol_version), final_array)
    return symbol_array, final_array


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
    masked_array[:,8][:6] = format_information_data[:6]
    masked_array[:,8][7:9] = format_information_data[6:8]
    masked_array[:,8][-7:] = format_information_data[8:]
    format_information_data.reverse()
    masked_array[8][:6] = format_information_data[:6]
    masked_array[8][7:9] = format_information_data[6:8]
    masked_array[8][-8:] = format_information_data[7:]

    return masked_array

def leave_space_for_format_information(symbol_array):
    """Set all format information modules to 8 so that they are not
    overwritten by data placement (which checks that module value is 9 before
    it place data). This is just to quicken the route to have a final symbol to
    test with a decoder. Rewriting will come at that point."""
    symbol_array[:,8][:6] = 8
    symbol_array[:,8][7:9] = 8
    symbol_array[8][:6] = 8
    symbol_array[8][7] = 8
    symbol_array[8][-8:] = 8
    symbol_array[:,8][-7:] = 8
    # It is not clear if this module is always black
    # cfr. ISO/IEC 18004 Fig. 19
    symbol_array[:,8][-8] = 6
    return symbol_array


def bch_15_5(data_bit_string):
    numerator = (
            poly1d([int(x) for x in data_bit_string]) *
            poly1d([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
    generator_polynomial = poly1d([1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1])
    q, r = numerator / generator_polynomial
    coeff_list = [abs(int(x)) for x in r.coeffs]
    while len(coeff_list) < 10:
        coeff_list.insert(0, 0)
    coeff_string = ''
    for coeff in coeff_list:
        coeff_string += str(coeff)

    unmasked = data_bit_string + coeff_string
    masked = to_binstring(to_coeff(unmasked) ^ to_coeff('101010000010010'), 15)
    return masked


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
    flat_data_list = list("".join(list_to_bin(code.final_sequence)))
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
    with open('test.pbm', 'w') as f:
        f.writelines(['P1\n', " ".join([str(symbol_size), str(symbol_size)]),
            '\n', ])
        for arr in symbol_array:
            for x in arr:
                if x == 9:
                    x = 0
                f.write("".join([str(x), ' ']))
            f.write('\n')
    return True

def version_information_positioning(symbol_array, version_information):
    change_bits = ''
    for c in version_information:
        if c == '0':
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

    a = array([[9] * side_size] * side_size)
    a[0] = a[6] = [7] * 7 + [6] + [9] * (side_size - 16) + [6] + [7] * 7
    a[1] = a[5] = [7, 6, 6, 6, 6, 6, 7, 6] + [9] * (side_size - 16) + [6, 7, 6, 6, 6, 6, 6, 7]
    a[2] = a[3] = a[4] = [7, 6, 7, 7, 7, 6, 7, 6] + [9] * (side_size - 16) + [6, 7, 6, 7, 7, 7, 6, 7]
    a[7] = [6] * 8 + [9] * (side_size - 16) + [6] * 8

    a[-8] = [6] * 8 + [9] * (side_size - 8)
    a[-1] = a[-7] = [7] * 7 + [6] + [9] * (side_size - 8)
    a[-2] = a[-6] = [7, 6, 6, 6, 6, 6, 7, 6] + [9] * (side_size - 8)
    a[-3] = a[-4] = a[-5] = [7, 6, 7, 7, 7, 6, 7, 6] + [9] * (side_size - 8)
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
            symbol_array[6][i] = 7
        else:
            symbol_array[6][i] = 6

    symbol_array[:,6] = symbol_array[6]
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

    symbol_array[x - 2][y - 2:y + 3] = [7, 7, 7, 7, 7]
    symbol_array[x - 1][y - 2:y + 3] = [7, 6, 6, 6, 7]
    symbol_array[x][y - 2:y + 3] =     [7, 6, 7, 6, 7]
    symbol_array[x + 1][y - 2:y + 3] = [7, 6, 6, 6, 7]
    symbol_array[x + 2][y - 2:y + 3] = [7, 7, 7, 7, 7]

    return symbol_array


def quiet_zone():
    """
    This is a region 4X wide which shall be free of all other markings,
    surrounding the symbol on all four sides. Its nominal reflectance value
    shall be equal to that of the light modules.
    """

if __name__ == '__main__':
    test()
