from nose.tools import raises

from qrreference import alphanumeric_codes

def split_numeric_input(input):
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

def split_alphanumeric_input(input):
    splitted_data = []
    tmp_list = []
    for i in range(1, len(input) + 1):
        if (i % 2) == 0:
            tmp_list.append(input[i-1])
            splitted_data.append(tmp_list)
            tmp_list = []
        else:
            tmp_list.append(input[i-1])
    if tmp_list:
        splitted_data.append(tmp_list)
    return splitted_data

def bin(x, width):
    return ''.join(str((x>>i)&1) for i in xrange(width-1,-1,-1))

def pad(bit_string, length):
    zeroes = length - len(bit_string)
    if zeroes < 0:
        raise Exception("Bit string is longer than padding")
    return bit_string + '0' * zeroes

def convert_numeric(input):
    splitted_input = split_numeric_input(input)
    data_bit_stream = ''
    for input in splitted_input:
        len_input = len(input)
        data_bit_stream += bin(int(input), (len_input * 3) + 1)
    return data_bit_stream

def convert_alphanumeric(input):
    input = alphanumeric_codes(input)
    splitted_input = split_alphanumeric_input(input)
    data_bit_stream = ''
    for input in splitted_input:
        if len(input) == 2:
            data_bit_stream += bin(input[0]*45+input[1], 11)
        else:
            data_bit_stream += bin(input[0], 6)
    return data_bit_stream
### TESTS

def test_split_numeric_mode():
    assert(split_numeric_input('01234567') == ['012', '345', '67'])
    assert(split_numeric_input('') == [])

def test_split_alphanumeric_mode():
    assert(split_alphanumeric_input([12,34,54,2,23]) == [[12, 34], [54,2],
        [23]])
    assert(split_numeric_input('') == [])

def test_convert_numeric():
    assert(convert_numeric('01234567') == '000000110001010110011000011')

def test_pad():
    assert pad('0101', 5) == '01010'

@raises(Exception)
def test_wrong_pad():
    pad('0101001', 2)
