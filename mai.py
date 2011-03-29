#!/usr/bin/env python
# -*- coding: utf-8 -*-

def test_reed_solomon():
    import qrcode as qr
    from qrutils import list_to_coeff
    import gf
    gf256 = gf.GaloisField()
    a = qr.Encoder('abcde123', 1, 'H', 'alphanumeric')
    A = gf.GFPoly(gf256, list_to_coeff(a.codewords)).multiply_by_monomial(17, 1)
    b = [gf.alpha_power(x) for x in [0, 43, 139, 206, 78, 43, 239, 123, 206, 214, 147, 24, 99, 150, 39, 243, 163, 136]]
    B = gf.GFPoly(gf256, b)
    q, r = A.divide(B)
    print r
#    assert r.coefficients == [42, 159, 74, 221, 244, 169, 239, 150, 138, 70, 237, 85, 224, 96, 74, 219, 61]

    print "ISO"
    a = qr.Encoder('01234567', 1, 'M', 'numeric')
    assert a.codewords == [
            '00010000', '00100000', '00001100', '01010110', '01100001', '10000000',
            '11101100', '00010001', '11101100', '00010001', '11101100', '00010001',
            '11101100', '00010001', '11101100', '00010001']

    A = gf.GFPoly(gf256, list_to_coeff(a.codewords)).multiply_by_monomial(10,1)
    b = [gf.alpha_power(x) for x in [0, 251, 67, 46, 61, 118, 70, 64, 94, 32, 45]]
    print b
    B = gf.GFPoly(gf256, b)
    q,r = A.divide(B)
    print r
    assert r.coefficients[0] == 165
