How to
======

To encode an alphanumeric string in a QR Code symbol with error correction
level set to *M* you have to::

    >>> from qrcode.qrcode import Encoder
    >>> qr = Encoder('your alphanumeric string', 'M')
    >>> qr.final_sequence
    [32, 198, 18, 172, 57, 121, 229, 48, 120, 82, 251, 38, 138, 64, 161, 51, 70, 13, 128, 236, 17, 236, 17, 236, 17, 236, 17, 236, 223, 57, 21, 65, 149, 211, 39, 87, 53, 209, 75, 64, 73, 252, 25, 130]

..

qr.final_sequence is the list of the coefficients ready to be displaced in the
symbol array. Of course every coefficient must be converted to a 8 bit string
with::

    >>> from qrcode.qrutils import list_to_bin
    >>> list_to_bin(qr.final_sequence)
    ['00100000', '11000110', '00010010', '10101100', '00111001', '01111001', '11100101', '00110000', '01111000', '01010010', '11111011', '00100110', '10001010', '01000000', '10100001', '00110011', '01000110', '00001101', '10000000', '11101100', '00010001', '11101100', '00010001', '11101100', '00010001', '11101100', '00010001', '11101100', '11011111', '00111001', '00010101', '01000001', '10010101', '11010011', '00100111', '01010111', '00110101', '11010001', '01001011', '01000000', '01001001', '11111100', '00011001', '10000010']

..

I still have to find an algorithm to place the bits into the symbol array.

**Help appreciated.**

In the **qrdraw** module there's an early stage way to create a symbol array for any
symbol version with Position Detection, Timing and Alignment patterns so that
I'll have a skeleton to test with data displacing.
