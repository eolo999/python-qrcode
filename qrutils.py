from qrreference import alphanumeric_codes
from rs_generator_polynomials import generator_polynomials
from gf import GFPoly, GaloisField

gf256 = GaloisField()


def split_numeric_input(input):
    """The input data string is divided into groups of three digits.
    """
    splitted_data = []
    tmp_string = ''
    for i in range(1, len(input) + 1):
        if (i % 3) == 0:
            splitted_data.append(tmp_string + input[i - 1])
            tmp_string = ''
        else:
            tmp_string += input[i - 1]
    if tmp_string:
        splitted_data.append(tmp_string)
    return splitted_data


def split_alphanumeric_input(input):
    """Split the input string in a list of strings as specified in ISO/IEC
    18004 8.4.3: Input data characters are divided into groups of two
    characters.
    """
    splitted_data = []
    tmp_list = []
    for i in range(1, len(input) + 1):
        if (i % 2) == 0:
            tmp_list.append(input[i - 1])
            splitted_data.append(tmp_list)
            tmp_list = []
        else:
            tmp_list.append(input[i - 1])
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
    return bit_string + '0' * zeroes


def convert_numeric(input):
    """ISO/IEC 18004 8.4.2: The input data string is divided into groups of
    three digits, and each group is converted to its 10 bit binary equivalent.
    If the number of input digits is not an exact multiple of three, the final
    one or two digits are converted to 4 or 7 bits respectively.

    Returns the input respresentation as a bit string.
    """
    splitted_input = split_numeric_input(input)
    data_bit_stream = ''
    for input in splitted_input:
        data_bit_stream += to_binstring(int(input), (len(input) * 3) + 1)
    return data_bit_stream


def convert_alphanumeric(input):
    """ISO/IEC 18004 8.4.3: Input data characters are divided into groups of
    two characters which are encoded to 11-bit binary codes. The character
    value of the first character is multiplied by 45 and the character value
    of the second digit is added to the product. The sum is then converted to
    an 11 bit binary number. If the number of input data characters is not a
    multiple of two, the character value of the final character is encoded to
    a 6-bit binary number.
    """
    input = alphanumeric_codes(input)
    splitted_input = split_alphanumeric_input(input)
    data_bit_stream = ''
    for input in splitted_input:
        if len(input) == 2:
            data_bit_stream += to_binstring(input[0] * 45 + input[1], 11)
        else:
            data_bit_stream += to_binstring(input[0], 6)
    return data_bit_stream


def list_to_bin(coefficients_list):
    """Given a list of codewords represented as integers it returns a
    list of their value as a binary_string.
    """
    return map(to_binstring, coefficients_list)


def list_to_coeff(codewords_list):
    """Given a list of codewords represented as binary strings it returns a
    list of their value as an integer.
    """
    coeff = map(to_coeff, codewords_list)
    return coeff


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
    num = GFPoly(gf256, coefficients).multiply_by_monomial(num_of_ec_words, 1)
    den = GFPoly(gf256, [gf256.alpha_power(x) for x in
        generator_polynomials[num_of_ec_words]])
    q, rem = num.divide(den)
    return rem.coefficients
