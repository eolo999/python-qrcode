#!/usr/bin/env python
# -*- coding: utf-8 -*-

from qrcode import Encoder
from array import array

def test_reed_solomon():
    a = Encoder('abcde123', 1, 'H', 'alphanumeric')
    assert a.ec_blocks[0].coefficients == array('i', [42, 159, 74, 221, 244, 169, 239, 150,
        138, 70, 237, 85, 224, 96, 74, 219, 61])

    a = Encoder('01234567', 1, 'M', 'numeric')
    assert a.codewords == [
            '00010000', '00100000', '00001100', '01010110', '01100001', '10000000',
            '11101100', '00010001', '11101100', '00010001', '11101100', '00010001',
            '11101100', '00010001', '11101100', '00010001']

    assert a.ec_blocks[0].coefficients[0] == 165

    a = Encoder('a'*60, 5, 'H', 'alphanumeric')
    assert len(a.ec_blocks) == 4
    assert len(a.data_blocks[0]) == 11
    assert len(a.data_blocks[2]) == 12

    a = Encoder('b'*938, 17, 'L', 'alphanumeric')
    assert len(a.ec_blocks) == 6
    assert len(a.data_blocks[0]) == 107
    assert len(a.data_blocks[1]) == 108
