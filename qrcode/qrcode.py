# -*- coding: utf-8 -*-
"""This module implements the qrcode Encoder class which handles all the
operation needed to translate a string into an image."""

from qrdraw import make_array

from qrutils import (
        convert,
        data_codewords_per_block,
        determine_datatype,
        determine_symbol_version,
        ec_codewords,
        mode_indicators,
        num_char_count_indicator_bits,
        list_to_coeff,
        make_image,
        max_codewords,
        max_databits,
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
        self.count_bits = num_char_count_indicator_bits(
                self.symbol_version, self.data_mode)

        # empty data objects
        self.code = ''
        self.codewords = []
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
        image_path, _image = make_image(self.symbol_array, path=path, zoom=5)
        return image_path

    def _apply_error_correction(self):
        """Creates the error correction block relative to every data block."""
        index = 0
        coeff_list = list_to_coeff(self.codewords)
        code_blocks = data_codewords_per_block(self.symbol_version,
                self.error_correction_level)
        for code_block in code_blocks:
            self.data_blocks.append(coeff_list[index:index + code_block])
            index += code_block

        ec_codewords_per_block = ec_codewords(self.symbol_version,
                self.error_correction_level) / len(code_blocks)

        for code_block in self.data_blocks:
            self.ec_blocks.append(
                    reed_solomon(code_block, ec_codewords_per_block))

    def _create_final_sequence(self):
        """Interleaves codewords from different codeblocks and append error
        correction codewords."""
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
        for count in range(num_of_codewords):
            if count % 2 == 0:
                self.codewords.append(pad0)
            else:
                self.codewords.append(pad1)

    def _terminator(self):
        """Add zeroes to the code string."""
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
        """Split code bit stream into 8 bit codewords."""
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
        for count in range(1, len(code) + 1):
            tmp_word += code[count - 1]
            if count % 8 == 0:
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
        self.code = "".join([self._insert_indicators(),
                    convert(self.input_string, self.data_mode)])

    def _insert_indicators(self):
        """Calculates data indicators."""
        mode_bits = mode_indicators(self.data_mode)
        indicators = "".join([mode_bits, to_binstring(
            len(self.input_string), self.count_bits)])
        return indicators


def _main():
    """Creates two Encoder instances for testing purpose."""
    num = Encoder('01234567', 'L')
    alnum = Encoder('asdfdadas876-asd.', 'L')
    num.save_image()
    alnum.save_image()
    return num, alnum

if __name__ == '__main__':
    _main()
