# -*- coding: utf-8 -*-

from qrutils import determine_data_mode
from qrreference import get_mode_indicators, get_num_of_bits_character_count_indicator

correction_levels = ['L', 'M', 'Q', 'H']


class Encoder(object):
    def __init__(self, input_string, error_correction_level):
        self.code = ''
        self.input_string = input_string
        self.error_correction_level = error_correction_level
        self.symbol_version = self._determine_version()
        self.data_mode = 'numeric' #determine_data_mode(self.input_string)
        self.mode_bits = get_mode_indicators(self.data_mode)
        self.count_bits = get_num_of_bits_character_count_indicator(
                self.symbol_version,
                self.data_mode
                )

    def encode(self):
        self.convert_data()
#        self._split_codewords()
#        self._add_pad_chars()
#        self._error_correction()
#        self._interleave()
#        self._build_matrix()
#        self._apply_mask()
#        self._generate_format_and_version_info()

    def _determine_version(self):
        return 1

    def convert_data(self):
        """
        Convert the data characters into a bit stream in accordance with the
        rules for the mode in force, as defined in 8.4.1 to 8.4.5
        """
        self.code = (self._insert_indicators() +
                convert_to_binary_repr(self.input_string) +
                self._terminator())
        validate_numeric_bitstream_length(self.input_string, self.code,
                self.count_bits)

    def _insert_indicators(self):
        indicators = self.mode_bits + _bin(len(self.input_string), self.count_bits)
        print indicators
        return indicators

    def _terminator(self):
        return '0000'

    def validate_numeric_bitstream_length(input, output, count_bits):
        #to be implemented
        r = len(input) % 3
        if r != 0:
            r = r * 3 + 1
        return len(output) == (4 + count_bits + 10 * (len(input)/3) + r)

    def _split_codewords(self):
        pass

    def _add_pad_chars(self):
        pass

    def _error_correction(self):
        """
        Divide the codeword sequence into the required number of blocks (as
        defined in Tables 13 to 22) to enable the error correction algorithms
        to be processed. Generate the error correction codewords for each
        block, appending the error correction codewords to the end of the data
        codeword sequence.
        """
        pass

    def _interleave():
        """
        Interleave the data and error correction codewords from each block as
        described in 8.6 (step 3) and add remainder bits as necessary.
        """
        pass

def handle_numeric_input(input):
    data_bits = convert_to_binary_repr(input)
    mode_bits = mode_indicator_bits()
    count_bits = count_indicator_bits(input)
    output = mode_bits + count_bits + data_bits
    if validate_numeric_bitstream_length(input, output, len(count_bits)):
        return output
    else:
        # waiting to build a QRException
        raise Exception


def _split_numeric_input(input):
    splitted_data = []
    tmp_string = ''
    for i in range(1, len(input) + 1):
        if (i % 3) == 0:
            splitted_data.append(tmp_string + input[i-1])
            tmp_string = ''
        else:
            tmp_string += input[i-1]
    if tmp_string:
        splitted_data.append(tmp_string)
    return splitted_data

def convert_to_binary_repr(input):
    splitted_input = _split_numeric_input(input)
    data_bit_stream = ''
    for input in splitted_input:
        len_input = len(input)
        data_bit_stream += _bin(int(input), (len_input * 3) + 1)
    return data_bit_stream

def count_indicator_bits(input, version=1, data_type='numeric'):
    if (data_type == 'numeric') and (version == 1):
        return _bin(len(input), 10)

def mode_indicator_bits(version=1):
    return '0001'

def _bin(x, width):
    return ''.join(str((x>>i)&1) for i in xrange(width-1,-1,-1))

def validate_numeric_bitstream_length(input, output, count_bits):
    #to be implemented
    r = len(input) % 3
    if r != 0:
        r = r * 3 + 1
    return len(output) == (4 + count_bits + 10 * (len(input)/3) + r)


### TESTS

def test_split_numeric_mode():
    assert(_split_numeric_input('01234567') == ['012', '345', '67'])
    assert(_split_numeric_input('') == [])

def test_convert_to_binary_repr():
    assert(convert_to_binary_repr('01234567') == '000000110001010110011000011')

def test_count_indicator_bits():
    assert count_indicator_bits('01234567') == '0000001000'

def test_complete():
    assert(handle_numeric_input('01234567') ==
            '00010000001000000000110001010110011000011')
    assert(handle_numeric_input('0123456789012345') ==
            '00010000010000000000110001010110011010100110111000010100111010100101')

def test_encoder():
    e = Encoder('01234567', 'L')
    e.encode()
    assert e.code == '000100000010000000001100010101100110000110000'
    e = Encoder('0123456789012345', 'L')
    e.encode()
    assert e.code == '000100000100000000001100010101100110101001101110000101001110101001010000'


__numeric__ = """
The input data string is divided into groups of three digits, and each group
is converted to its 10 bit binary equivalent. If the number of input digits is
not an exact multiple of three, the final one or two digits are converted to 4
or 7 bits respectively. The binary data is then concatenated and prefixed with
the Mode Indicator and the Character Count Indicator. The Character Count
Indicator in the Numeric Mode has 10, 12 or 14 bits as defined in Table 3. The
number of input data characters is converted to its 10, 12 or 14 bit binary
equivalent and added after the Mode Indicator and before the binary data
sequence.
"""

