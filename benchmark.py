#!/usr/bin/env python
# -*- coding: utf-8 -*-

from qrcode import Encoder

def benchmark():
    Encoder('A'*937, 17, 'L', 'alphanumeric')

def main():
    from timeit import Timer
    t = Timer('benchmark()', 'from __main__ import benchmark')
    print t.timeit(100)


if __name__ == '__main__':
    main()
