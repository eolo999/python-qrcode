# -*- coding: utf-8 -*-

from qrutils import (
        convert_numeric,
        convert_alphanumeric,
        bin
        )

from qrreference import (
        get_mode_indicators,
        get_num_of_bits_character_count_indicator
        )

correction_levels = ['L', 'M', 'Q', 'H']

class Encoder(object):
    def __init__(self, input_string, error_correction_level,
            data_mode='numeric'):
        self.code = ''
        self.input_string = input_string
        self.error_correction_level = error_correction_level
        self.symbol_version = self._determine_version()
        self.data_mode = data_mode
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
        if self.data_mode == 'numeric':
            self.code = (self._insert_indicators() +
                    convert_numeric(self.input_string) +
                    self._terminator())
            assert self.validate_numeric_bitstream_length()
        elif self.data_mode == 'alphanumeric':
            self.code = (self._insert_indicators() +
                    convert_alphanumeric(self.input_string) +
                    self._terminator())
            assert self.validate_alphanumeric_bitstream_length()

    def _insert_indicators(self):
        indicators = self.mode_bits + bin(len(self.input_string), self.count_bits)
        return indicators

    def _terminator(self):
        return '0000'

    def validate_numeric_bitstream_length(self):
        #to be implemented
        r = len(self.input_string) % 3
        if r != 0:
            r = r * 3 + 1
        return len(self.code) == (4 + self.count_bits + 10 * (len(self.input_string)/3) + r + 4)

    def validate_alphanumeric_bitstream_length(self):
        """
        B = 4 + C + 11(D DIV 2) + 6(D MOD 2)
        where:
        B = number of bits in bit stream
        C = number of bits in Character Count Indicator ( from Table 3)
        D = number of input data characters
        first and last 4 are respectively for data mode indicator and
        terminator sequence
        """
        B = len(self.code)
        C = self.count_bits
        D = len(self.input_string)
        return B == 4 + C + 11 * (D / 2) + 6 * (D % 2) + 4

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


### TESTS


def test_numeric_encoder():
    e = Encoder('01234567', 'L')
    e.encode()
    assert e.code == '000100000010000000001100010101100110000110000'
    e = Encoder('0123456789012345', 'L')
    e.encode()
    assert e.code == '000100000100000000001100010101100110101001101110000101001110101001010000'

def test_alphanumeric_encoder():
    e = Encoder('AC-42', 'L', 'alphanumeric')
    e.encode()
    assert e.code == '001000000010100111001110111001110010000100000'

