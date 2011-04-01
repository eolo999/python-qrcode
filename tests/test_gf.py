#!/usr/bin/env python
# -*- coding: utf-8 -*-

import qrcode as qr
from qrutils import list_to_coeff, reed_solomon
from qrreference import get_ec_codewords
from array import array

def test_reed_solomon():
    a = qr.Encoder('abcde123', 1, 'H', 'alphanumeric')
    num_of_ec_codewords = get_ec_codewords(a.symbol_version,
            a.error_correction_level)
    coeffs = list_to_coeff(a.codewords)
    rs = reed_solomon(coeffs, num_of_ec_codewords)
    assert rs.coefficients == array('i', [42, 159, 74, 221, 244, 169, 239, 150, 138, 70, 237, 85, 224, 96, 74, 219, 61])

    a = qr.Encoder('01234567', 1, 'M', 'numeric')
    assert a.codewords == [
            '00010000', '00100000', '00001100', '01010110', '01100001', '10000000',
            '11101100', '00010001', '11101100', '00010001', '11101100', '00010001',
            '11101100', '00010001', '11101100', '00010001']

    num_of_ec_codewords = get_ec_codewords(a.symbol_version,
            a.error_correction_level)
    coeffs = list_to_coeff(a.codewords)
    rs = reed_solomon(coeffs, num_of_ec_codewords)
    assert rs.coefficients[0] == 165
