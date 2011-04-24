#!/usr/bin/env python
# -*- coding: utf-8 -*-

from qrcode.gf import GaloisField

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

