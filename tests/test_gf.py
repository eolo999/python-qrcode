#!/usr/bin/env python
# -*- coding: utf-8 -*-

import qrcode as qr
from qrutils import list_to_coeff
from array import array
from rs_generator_polynomials import generator_polynomials
import gf

def test_reed_solomon():
    gf256 = gf.GaloisField()
    a = qr.Encoder('abcde123', 1, 'H', 'alphanumeric')
    A = gf.GFPoly(gf256, list_to_coeff(a.codewords)).multiply_by_monomial(17, 1)
    b = [gf256.alpha_power(x) for x in generator_polynomials[17]]
    B = gf.GFPoly(gf256, b)
    q, r = A.divide(B)
    assert r.coefficients == array('i', [42, 159, 74, 221, 244, 169, 239, 150, 138, 70, 237, 85, 224, 96, 74, 219, 61])

    a = qr.Encoder('01234567', 1, 'M', 'numeric')
    assert a.codewords == [
            '00010000', '00100000', '00001100', '01010110', '01100001', '10000000',
            '11101100', '00010001', '11101100', '00010001', '11101100', '00010001',
            '11101100', '00010001', '11101100', '00010001']

    A = gf.GFPoly(gf256, list_to_coeff(a.codewords)).multiply_by_monomial(10,1)
    b = [gf256.alpha_power(x) for x in generator_polynomials[10]]
    B = gf.GFPoly(gf256, b)
    q,r = A.divide(B)
    assert r.coefficients[0] == 165
    print 'ok'
