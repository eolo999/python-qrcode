# -*- coding: utf-8 -*-

from qrdraw import make_array

from qrutils import (
        convert_alphanumeric,
        convert_numeric,
        data_codewords_per_block,
        determine_datatype,
        determine_symbol_version,
        ec_codewords,
        mode_indicators,
        get_num_of_bits_character_count_indicator,
        list_to_coeff,
        make_image,
        max_codewords,
        max_databits,
        pad,
        reed_solomon,
        to_binstring,
        version_information)

class Encoder(object):
    """Encode numeric and alphanumeric strings in a QR Code Symbol version 2.

    :param input_string: the string you wanto to encode
    :param error_correction_level: defines how many erasures or
                                   errors your symbol will tolerate
                                   maintaining its readability.
    """
    def __init__(self, input_string, error_correction_level='L'):
        # input data
        self.input_string = input_string
        self.error_correction_level = error_correction_level

        # automatic recognition data
        self.data_mode = determine_datatype(input_string)
        self.symbol_version = determine_symbol_version(input_string,
                error_correction_level)
        self.count_bits = get_num_of_bits_character_count_indicator(
                self.symbol_version, self.data_mode)

        # empty data objects
        self.code = ''
        self.data_blocks = []
        self.ec_blocks = []
        self.final_sequence = []
        self.version_information = None
        self.symbol_array = None

        self.encode()

    def encode(self):
        """Encode the input string into a sequence of codewords and error
        correction words."""
        self._convert_input_string()
        self.codewords = self._bitstream_to_codewords()
        full = max_codewords(self.symbol_version,
                self.error_correction_level)
        self._fill_symbol_with_pad_codewords(full -
                len(self.codewords))

        self._apply_error_correction()
        self._create_final_sequence()
        if self.symbol_version >= 7:
            self.version_information = version_information(self.symbol_version)
        # apply mask
        # matrix position

    def save_image(self, path=None):
        """Saves the QR Code Symbol to the given 'path'."""
        self.symbol_array = make_array(self)
        image_path = make_image(self.symbol_array, path=path, zoom=5)
        return image_path


    def _apply_error_correction(self):
        """Creates the error correction block relative to every data block."""
        index = 0
        cw = list_to_coeff(self.codewords)
        code_blocks = data_codewords_per_block(self.symbol_version,
                self.error_correction_level)
        for cb in code_blocks:
            self.data_blocks.append(cw[index:index + cb])
            index += cb

        ec_codewords_per_block = ec_codewords(self.symbol_version,
                self.error_correction_level) / len(code_blocks)

        for code_block in self.data_blocks:
            self.ec_blocks.append(
                    reed_solomon(code_block, ec_codewords_per_block))

    def _create_final_sequence(self):
        for i in range(max([len(x) for x in self.data_blocks])):
            for data_block in self.data_blocks:
                try:
                    self.final_sequence.append(data_block[i])
                except IndexError:
                    pass
        for i in range(len(self.ec_blocks[0])):
            for ec_block in self.ec_blocks:
                self.final_sequence.append(ec_block[i])

    def _fill_symbol_with_pad_codewords(self, num_of_codewords):
        """Fill a symbol to its maximum capacity with alternate pad words."""
        pad0 = '11101100'
        pad1 = '00010001'
        for n in range(num_of_codewords):
            if n % 2 == 0:
                self.codewords.append(pad0)
            else:
                self.codewords.append(pad1)

    def _terminator(self):
        symbol_capacity_bits = max_databits(self.symbol_version,
                self.error_correction_level)
        delta = symbol_capacity_bits - len(self.code)
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
        
        # pad bitstream to a multiple of 8
        partial = len(self.code) % 8
        if partial != 0:
            code = "".join([self.code, '0' * (8 - partial)])
        else:
            code = self.code

        # I need to start from 1 not to have the module condition pass on n=0
        # and flush the word to the temporary list
        for n in range(1, len(code) + 1):
            tmp_word += code[n - 1]
            if n % 8 == 0:
                # flush the word to the temporary word list
                codewords.append(tmp_word)
                tmp_word = ''
        return codewords

    def _convert_input_string(self):
        """
        Convert the data characters into a bit stream in accordance with the
        rules for the mode in force, as defined in ISO/IEC 18004 8.4.1 to
        8.4.5.
        """
        if self.data_mode == 'numeric':
            self.code = "".join([self._insert_indicators(),
                    convert_numeric(self.input_string)])
            assert self._validate_numeric_bitstream_length()
        elif self.data_mode == 'alphanumeric':
            self.code = "".join([self._insert_indicators(),
                    convert_alphanumeric(self.input_string)])
            assert self._validate_alphanumeric_bitstream_length()

    def _insert_indicators(self):
        mode_bits = mode_indicators(self.data_mode)
        indicators = "".join([mode_bits, to_binstring(
            len(self.input_string), self.count_bits)])
        return indicators

    def _validate_numeric_bitstream_length(self):
        r = len(self.input_string) % 3
        if r != 0:
            r = r * 3 + 1
        return len(self.code) == (
                4 + self.count_bits +
                10 * (len(self.input_string) / 3) + r)

    def _validate_alphanumeric_bitstream_length(self):
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


def _main():
    global num, alnum
    num = Encoder('01234567', 'L')
    alnum = Encoder('asdfdadas876-asd.', 'L')
    num.save_image()
    alnum.save_image()

if __name__ == '__main__':
    _main()
