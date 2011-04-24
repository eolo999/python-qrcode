from qrcode.qrutils import data_codewords_per_block
from qrcode.qrreference import blocks_per_ecl , generator_polynomials

def test_generator_polynomials_length():
    for key in generator_polynomials:
        assert len(generator_polynomials[key]) == key + 1

def test_block_per_ecl_lengths():
    for key in blocks_per_ecl:
        assert len(blocks_per_ecl[key]) == 4


def test_split():
    assert data_codewords_per_block(1, 'L') == [19]
