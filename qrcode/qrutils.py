"""qrcode package utilities."""

from numpy import poly1d
from PIL import Image
from math import sqrt
from tempfile import mktemp

from qrreference import (
        alphanumeric_char_string,
        alphanumeric_char_values,
        blocks_per_ecl,
        ecl_index,
        generator_polynomials,
        max_char_capacity_table,
        mode_indicators_table,
        num_of_bits_character_count_indicator,
        symbol_sizes,
        symbol_version_data,
        version_information_bit_string)

from gf import GFPoly, GaloisField


GF256 = GaloisField()


def bch_18_6(symbol_version):
    """Calculate BCH(18,6) on symbol version number.

    This function is not used as in the specs we have a reference table
    covering all the symbol version. It was just to test if I would have
    obtained the same results.
    """
    data_bit_string = to_binstring(symbol_version, 6)
    numerator = (
            poly1d([int(x) for x in data_bit_string]) *
            poly1d([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
    generator_polynomial = poly1d([1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1])
    _quotient, remainder = numerator / generator_polynomial
    coeff_list = [abs(int(x)) for x in remainder.coeffs]
    # don't know why i have some 2 and 3 coefficients. used a modulo operation
    # to obtain the expected results
    coeff_list = [x % 2 for x in coeff_list]
    while len(coeff_list) < 12:
        coeff_list.insert(0, 0)
    coeff_string = ''
    for coeff in coeff_list:
        coeff_string += str(coeff)

    result = data_bit_string + coeff_string
    return result


def bch_15_5(data_bit_string):
    """Calculate BCH(15,5) on input bit string and return the masked result.

    Masking operation is a XOR with the bit string *101010000010010*."""
    numerator = (
            poly1d([int(x) for x in data_bit_string]) *
            poly1d([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
    generator_polynomial = poly1d([1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1])
    _quotient, remainder = numerator / generator_polynomial
    coeff_list = [abs(int(x)) for x in remainder.coeffs]
    coeff_list = [x % 2 for x in coeff_list]
    while len(coeff_list) < 10:
        coeff_list.insert(0, 0)
    coeff_string = ''
    for coeff in coeff_list:
        coeff_string += str(coeff)

    unmasked = data_bit_string + coeff_string
    masked = to_binstring(to_coeff(unmasked) ^ to_coeff('101010000010010'), 15)
    return masked


def data_codewords_per_block(version, ecl):
    """Given symbol version and error correction level returns the number of
    data codewords per each block.

    >>> data_codewords_per_block(7, 'Q')
    [14, 14, 15, 15, 15, 15]
    
    The number of codewords per block is not always the same as shown in
    tables 13-22."""
    return blocks_per_ecl[version][ecl_index[ecl]]


def ec_codewords(version, ecl):
    """Returns the total number of error correction codewords in a QR symbol.

    >>> ec_codewords(7, 'Q')
    108

    """
    return (symbol_version_data[version]['data_capacity'] -
            symbol_version_data[version]['data_codewords'][ecl])


def max_char_capacity(data_type, symbol_version, ecl):
    """Returns the maximum number of characters a defined symbol can
    contain.
    
    >>> max_char_capacity('numeric', 7, 'H')
    154
    
    """
    return max_char_capacity_table[data_type][symbol_version][ecl_index[ecl]]


def max_codewords(version, ecl):
    """Returns the maximum number of codewords a defined symbol can contain.
    
    >>> max_codewords(17, 'Q')
    367
    
    """
    return symbol_version_data[version]['data_codewords'][ecl]


def max_databits(version, ecl):
    """Being a codeword 8 bit long this functions simply multiplies the max
    number of codewords by 8.

    >>> cw = max_codewords(17, 'Q')
    >>> max_databits(17, 'Q') == cw * 8
    True

    """
    return max_codewords(version, ecl) * 8


def mode_indicators(data_mode):
    """Returns the bit string representing the data_mode.

    >>> mode_indicators('numeric')
    '0001'

    """
    return mode_indicators_table[data_mode]


def num_char_count_indicator_bits(version, data_mode):
    """Returns the number of bits of the character count indicator for a given
    symbol version and data mode"""
    return num_of_bits_character_count_indicator[version][data_mode]


def qr_size(version):
    """Given a symbol version number returns the length of the symbol side.
    So a symbol version 1 is a square of 21 size.

    >>> qr_size(1)
    21

    """
    return symbol_sizes[version]


def alphanumeric_codes(input_string):
    """Return a list of character code numbers given an input string."""
    codes = []
    for char in input_string:
        codes.append(alphanumeric_char_values[char.upper()])
    return codes


def version_information(symbol_version):
    """Uses ISO/IEC 18004 Table D.1 but I'd like to calculate BCH(18,6) on my
    own.
    """
    if symbol_version < 7:
        return ''
    return version_information_bit_string[symbol_version]


def determine_datatype(input_string):
    """Given an input string it determines the data mode to be used by the
    encoder.

    >>> determine_datatype('123412341')
    'numeric'
    >>> determine_datatype('asdfasdasd')
    'alphanumeric'
    >>> determine_datatype('test@example.org')
    '8bit'

    """
    if input_string.isdigit():
        return 'numeric'
    elif all(ch.upper() in alphanumeric_char_string
            for ch in input_string):
        return 'alphanumeric'
    else:
        return '8bit'


def determine_symbol_version(input_string, ecl):
    """Determine symbol version for input_string based on error correction
    level with minimum empty space"""
    data_type = determine_datatype(input_string)
    input_string_length = len(input_string)
    current = 1
    while current <= 40:
        if (max_char_capacity(data_type, current, ecl) >=
                input_string_length):
            return current
        else:
            current += 1
    raise Exception("String is too long!")


def split_numeric_input(input_string):
    """The input data string is divided into groups of three digits.
    """
    splitted_data = []
    tmp_string = ''
    for i in range(1, len(input_string) + 1):
        if (i % 3) == 0:
            splitted_data.append("".join([tmp_string, input_string[i - 1]]))
            tmp_string = ''
        else:
            tmp_string += input_string[i - 1]
    if tmp_string:
        splitted_data.append(tmp_string)
    return splitted_data


def split_alphanumeric_input(input_string):
    """Split the input string in a list of strings as specified in ISO/IEC
    18004 8.4.3: Input data characters are divided into groups of two
    characters.
    """
    splitted_data = []
    tmp_list = []
    for i in range(1, len(input_string) + 1):
        if (i % 2) == 0:
            tmp_list.append(input_string[i - 1])
            splitted_data.append(tmp_list)
            tmp_list = []
        else:
            tmp_list.append(input_string[i - 1])
    if tmp_list:
        splitted_data.append(tmp_list)
    return splitted_data


def to_binstring(decimal_number, length=8):
    """Convert a decimal number to a binary string with a fixed length.

    Attention: if the string length is shorter than the real binary
    representation of the number data is lost during conversion.
    """
    return ''.join(str(
        (decimal_number >> i) & 1) for i in range(length - 1, -1, -1))


def pad(bit_string, length):
    """Add a series of zeroes to a bit string up to 'length'.
    """
    zeroes = length - len(bit_string)
    if zeroes < 0:
        raise Exception("Bit string is longer than padding")
    return "".join([bit_string, '0' * zeroes])


def convert(input_string, data_mode):
    """Given an input string and a data mode returns the qrcode bit stream
    representation of the input."""
    if data_mode == 'numeric':
    #: ISO/IEC 18004 8.4.2: The input data string is divided into groups of
    #  three digits, and each group is converted to its 10 bit binary
    #  equivalent.  If the number of input digits is not an exact multiple of
    #  three, the final one or two digits are converted to 4 or 7 bits
    #  respectively.  Returns the input respresentation as a bit string.
        splitted_input = split_numeric_input(input_string)
        data_bit_stream = ''
        for input_string in splitted_input:
            data_bit_stream += to_binstring(int(input_string),
                    (len(input_string) * 3) + 1)
        return data_bit_stream
    #: """ISO/IEC 18004 8.4.3: Input data characters are divided into groups of
    #  two characters which are encoded to 11-bit binary codes. The character
    #  value of the first character is multiplied by 45 and the character value
    #  of the second digit is added to the product. The sum is then converted to
    #  an 11 bit binary number. If the number of input data characters is not a
    #  multiple of two, the character value of the final character is encoded to
    #  a 6-bit binary number.
    elif data_mode == 'alphanumeric':
        input_codes = alphanumeric_codes(input_string)
        splitted_input = split_alphanumeric_input(input_codes)
        data_bit_stream = ''
        for input_string in splitted_input:
            if len(input_string) == 2:
                data_bit_stream += to_binstring(input_string[0] * 45 +
                        input_string[1], 11)
            else:
                data_bit_stream += to_binstring(input_string[0], 6)
        return data_bit_stream
    elif data_mode == '8bit':
        data_bit_stream = ''
        for char in input_string:
            data_bit_stream += to_binstring(ord(char), 8)
        return data_bit_stream

def list_to_bin(coefficients_list):
    """Given a list of codewords represented as integers it returns a
    list of their value as a binary_string.
    """
    return [to_binstring(coeff) for coeff in coefficients_list]


def list_to_coeff(codewords_list):
    """Given a list of codewords represented as binary strings it returns a
    list of their value as an integer.
    """
    return [to_coeff(codeword) for codeword in codewords_list]


def to_coeff(codeword):
    """Given a codeword represented as a binary string it returns its integer
    value.
    """
    count = len(codeword)
    result = 0
    for bit in codeword:
        if bit == '1':
            result += pow(2, count - 1)
        count -= 1
    return result


def reed_solomon(coefficients, num_of_ec_words):
    """Returns the reed-solomon error correction list of coefficients given a
    list of codewords and the number of error correction words.
    """
    num = GFPoly(GF256, coefficients).multiply_by_monomial(num_of_ec_words, 1)
    den = GFPoly(GF256, [GF256.alpha_power(x) for x in
        generator_polynomials[num_of_ec_words]])
    _quotient, rem = num / den
    return rem.coefficients


def make_image(data, path=None, width=None, raw_list=False, zoom=1):
    """Creates a png image for the incoming data.

    :param data: encoded data
    :param path: file system path where the image will be saved
    :param width: the length of the side of the symbol
    :param raw_list: wether data is a raw_list or not
    :param zoom: image zoom multiplier

    If no path is given, a temporary file is created.

    By default data is expected to be in an nested numpy array, but a raw list
    is accepted if the corisponding flag is set.

    If width is not esplicitely given, it is calculated as the square root of
    the data-length."""
    if not raw_list:
        data = [list(array) for array in data]
        data = sum(data, [])
    width = width or sqrt(len(data))
    if width != int(width):
        raise RuntimeError("malformed data")
    width = int(width)
    tmp_data = []
    for i in data:
        if i in (1, 7):
            tmp_data.append(0)
        else:
            tmp_data.append(1)
    img = Image.new("1", (width, width))
    img.putdata(tmp_data)
    img = img.resize((width * zoom, width * zoom))
    path = path or (mktemp() + ".png")
    img.save(path)
    return path, img
