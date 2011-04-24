from qrcode.qrutils import get_blocks
from qrcode.qrreference import blocks_per_ecl , generator_polynomials

def test_generator_polynomials_length():
    for key in generator_polynomials:
        assert len(generator_polynomials[key]) == key + 1

def test_block_per_ecl_lengths():
    for key in blocks_per_ecl:
        assert len(blocks_per_ecl[key]) == 4


def test_split():
    assert get_blocks(1, 'L') == [19]
