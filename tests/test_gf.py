#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

from qrcode import Encoder
from array import array
from gf import GaloisField

def test_gf_add():
    gf = GaloisField()
    assert gf.add(141, 43) == 166
    assert gf.add(43, 178) == gf.subtract(43, 178)

def test_gf_alpha_power():
    gf = GaloisField()
    assert gf.alpha_power(0) == 1
    assert gf.alpha_power(1) == 2
    assert gf.alpha_power(9) == 58

def test_gf_multiply():
    gf = GaloisField(256, 301)
    assert gf.multiply(14, 33) == 227

def main():
    gf = GaloisField(256, 301)
    for n in range(9):
        print n, '\t', gf.alpha_power(n)


def test_reed_solomon():
    a = Encoder('abcde123', 1, 'H', 'alphanumeric')
    assert a.ec_blocks[0] == array('i', [42, 159, 74, 221, 244, 169, 239, 150,
        138, 70, 237, 85, 224, 96, 74, 219, 61])

    a = Encoder('01234567', 1, 'M', 'numeric')
    assert a.codewords == [
            '00010000', '00100000', '00001100', '01010110', '01100001', '10000000',
            '11101100', '00010001', '11101100', '00010001', '11101100', '00010001',
            '11101100', '00010001', '11101100', '00010001']

    assert a.ec_blocks[0][0] == 165

    a = Encoder('b'*938, 17, 'L', 'alphanumeric')
    assert len(a.ec_blocks) == 6
    assert len(a.data_blocks[0]) == 107
    assert len(a.data_blocks[1]) == 108

    a = Encoder('a'*60, 5, 'H', 'alphanumeric')
    assert len(a.ec_blocks) == 4
    assert len(a.data_blocks[0]) == 11
    assert len(a.data_blocks[2]) == 12
    assert len(a.final_sequence) == 46 + 88 == 134

    return a
