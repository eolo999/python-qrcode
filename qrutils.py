from qrreference import alphanumeric_codes
from rs_generator_polynomials import generator_polynomials
from gf import GFPoly, GaloisField

gf256 = GaloisField()

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

def bin(x, width=8):
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

def list_to_bin(coefficients_list):
    return map(bin, coefficients_list)

def list_to_coeff(codewords_list):
    coeff = map(to_coeff, codewords_list)
    return coeff

def to_coeff(codeword):
    count = len(codeword)
    result = 0
    for bit in codeword:
        if bit == '1':
            result += pow(2, count - 1)
        count -= 1
    return result

def reed_solomon(coefficients, num_of_ec_words):
    num = GFPoly(gf256, coefficients).multiply_by_monomial(num_of_ec_words, 1)
    den = GFPoly(gf256, [gf256.alpha_power(x) for x in
        generator_polynomials[num_of_ec_words]])
    q, rem = num.divide(den)
    return rem.coefficients
