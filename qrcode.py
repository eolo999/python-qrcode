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

    def apply_error_correction(self):
        # how_many_blocks and how many error correctioin words =>
        #   query ISO spec tables 13-22
        #
        # divide data codewords per num of blocks
        #
        # find generator polynomial for every codeblock =>
        #   query ISO spec tables A.1-A.7
        # get coefficients evaluating alpha_powers
        # 
        # divide every data block by its generator polynomial
        # the coefficients of the remainder are the error-correction codewords
        # join all data/error-correction blocks
        pass
        

    def encode(self):
        self.convert_data()
        self.codewords = self._bitstream_to_codewords()
        max_codewords = get_max_codewords(self.symbol_version,
                self.error_correction_level)
        self.fill_symbol_with_pad_codewords(max_codewords -
                len(self.codewords))
        self.apply_error_correction()
        # apply mask
        # matrix position
        # draw symbol

    def fill_symbol_with_pad_codewords(self, num_of_codewords):
        pad0 = '11101100'
        pad1 = '00010001'
        for n in range(num_of_codewords):
            if n % 2 == 0:
                self.codewords.append(pad0)
            else:
                self.codewords.append(pad1)

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


def main():
    global num, alnum
    num = Encoder('01234567', 1, 'L')
    alnum = Encoder('asdfdadas876-asd.', 1, 'L', 'alphanumeric')

if __name__ == '__main__':
    main()
