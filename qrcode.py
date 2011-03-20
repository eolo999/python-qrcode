# -*- coding: utf-8 -*-

from qrutils import (
        convert_numeric,
        convert_alphanumeric,
        bin,
        pad
        )

from qrreference import (
        get_mode_indicators,
        get_num_of_bits_character_count_indicator,
        get_max_databits,
        get_max_codewords,
        )

correction_levels = ['L', 'M', 'Q', 'H']

class Encoder(object):
    def __init__(self,
            input_string,
            symbol_version=1,
            error_correction_level='L',
            data_mode='numeric'):
        self.code = ''
        self.input_string = input_string
        self.error_correction_level = error_correction_level
        self.data_mode = data_mode
        self.symbol_version = symbol_version
        self.mode_bits = get_mode_indicators(self.data_mode)
        self.count_bits = get_num_of_bits_character_count_indicator(
                self.symbol_version,
                self.data_mode
                )
        self.symbol_capacity_bits = get_max_databits(self.symbol_version,
                self.error_correction_level)
        self.encode()

    def encode(self):
        self.convert_data()
        self.codewords = self._bitstream_to_codewords()
        max_codewords = get_max_codewords(self.symbol_version,
                self.error_correction_level)
        self.fill_symbol_with_pad_codewords(max_codewords -
                len(self.codewords))

    def fill_symbol_with_pad_codewords(self, num_of_codewords):
        pad0 = '11101100'
        pad1 = '00010001'
        for n in range(num_of_codewords):
            if n % 2 == 0:
                self.codewords.append(pad0)
            else:
                self.codewords.append(pad1)

#        self._split_codewords()
#        self._add_pad_chars()
#        self._error_correction()
#        self._interleave()
#        self._build_matrix()
#        self._apply_mask()
#        self._generate_format_and_version_info()

    def _terminator(self):
        delta = self.symbol_capacity_bits - len(self.code)
        if delta >= 4:
            num_of_zeroes = 4
        elif 0 <= delta < 4:
            num_of_zeroes = delta
        else:
            raise Exception("Data is greater than symbol capacity")
        self.code += ('0' * num_of_zeroes)

    def _bitstream_to_codewords(self):
        self._terminator()
        codewords = []
        tmp_word = ''
        for n in range(1, len(self.code) + 1):
            tmp_word += self.code[n - 1]
            if n % 8 == 0:
                codewords.append(tmp_word)
                tmp_word = ''
        if tmp_word:
            tmp_word = pad(tmp_word, 8)
            codewords.append(tmp_word)
        return codewords

    def convert_data(self):
        """
        Convert the data characters into a bit stream in accordance with the
        rules for the mode in force, as defined in 8.4.1 to 8.4.5
        """
        if self.data_mode == 'numeric':
            self.code = (self._insert_indicators() +
                    convert_numeric(self.input_string))
            assert self.validate_numeric_bitstream_length()
        elif self.data_mode == 'alphanumeric':
            self.code = (self._insert_indicators() +
                    convert_alphanumeric(self.input_string))
            assert self.validate_alphanumeric_bitstream_length()

    def _insert_indicators(self):
        indicators = self.mode_bits + bin(len(self.input_string), self.count_bits)
        return indicators

    def validate_numeric_bitstream_length(self):
        #to be implemented
        r = len(self.input_string) % 3
        if r != 0:
            r = r * 3 + 1
        return len(self.code) == (4 + self.count_bits + 10 * (len(self.input_string)/3) + r)

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
        return B == 4 + C + 11 * (D / 2) + 6 * (D % 2)

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



def main():
    global num_enc, alnum_enc
    num_enc = Encoder('234522345', 1, 'L')
    alnum_enc = Encoder('asdfdadas876-asd.', 1, 'L', 'alphanumeric')

if __name__ == '__main__':
    main()
