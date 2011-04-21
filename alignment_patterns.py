__doc__ = """The Alignment Patterns are positioned symmetrically on either
side of the diagonal running from the top left corner of the symbol to the
bottom right corner. They are spaced as evenly as possible between the Timing
Pattern and the opposite side of the symbol, any uneven spacing being
accommodated between the Timing Pattern and the first Alignment Pattern in the
symbol interior."""

from itertools import product
from qrutils import get_qr_size

#: ISO/IEC 18004 Table E.1
patterns = {
        1:  {'num_ap': 0,  'centers': []},
        2:  {'num_ap': 1,  'centers': [6, 18]},
        3:  {'num_ap': 1,  'centers': [6, 22]},
        4:  {'num_ap': 1,  'centers': [6, 26]},
        5:  {'num_ap': 1,  'centers': [6, 30]},
        6:  {'num_ap': 1,  'centers': [6, 34]},
        7:  {'num_ap': 6,  'centers': [6, 22, 38]},
        8:  {'num_ap': 6,  'centers': [6, 24, 42]},
        9:  {'num_ap': 6,  'centers': [6, 26, 46]},
        10: {'num_ap': 6,  'centers': [6, 28, 50]},
        11: {'num_ap': 6,  'centers': [6, 30, 54]},
        12: {'num_ap': 6,  'centers': [6, 32, 58]},
        13: {'num_ap': 6,  'centers': [6, 34, 62]},
        14: {'num_ap': 13, 'centers': [6, 26, 46, 65]},
        15: {'num_ap': 13, 'centers': [6, 26, 48, 70]},
        16: {'num_ap': 13, 'centers': [6, 26, 50, 74]},
        17: {'num_ap': 13, 'centers': [6, 30, 54, 78]},
        18: {'num_ap': 13, 'centers': [6, 30, 56, 82]},
        19: {'num_ap': 13, 'centers': [6, 30, 58, 86]},
        20: {'num_ap': 13, 'centers': [6, 34, 62, 90]},
        21: {'num_ap': 22, 'centers': [6, 28, 50, 72, 94]},
        22: {'num_ap': 22, 'centers': [6, 26, 50, 74, 98]},
        23: {'num_ap': 22, 'centers': [6, 30, 54, 78, 102]},
        24: {'num_ap': 22, 'centers': [6, 28, 54, 80, 106]},
        25: {'num_ap': 22, 'centers': [6, 32, 58, 84, 110]},
        26: {'num_ap': 22, 'centers': [6, 30, 58, 86, 114]},
        27: {'num_ap': 22, 'centers': [6, 34, 62, 90, 118]},
        28: {'num_ap': 33, 'centers': [6, 26, 50, 74, 98, 122]},
        29: {'num_ap': 33, 'centers': [6, 30, 54, 78, 102, 126]},
        30: {'num_ap': 33, 'centers': [6, 26, 52, 78, 104, 130]},
        31: {'num_ap': 33, 'centers': [6, 30, 56, 82, 108, 134]},
        32: {'num_ap': 33, 'centers': [6, 34, 60, 86, 112, 138]},
        33: {'num_ap': 33, 'centers': [6, 30, 58, 86, 114, 142]},
        34: {'num_ap': 33, 'centers': [6, 34, 62, 90, 118, 146]},
        35: {'num_ap': 46, 'centers': [6, 30, 54, 78, 102, 126, 150]},
        36: {'num_ap': 46, 'centers': [6, 24, 50, 76, 102, 128, 154]},
        37: {'num_ap': 46, 'centers': [6, 28, 54, 80, 106, 132, 158]},
        38: {'num_ap': 46, 'centers': [6, 32, 58, 84, 110, 136, 162]},
        39: {'num_ap': 46, 'centers': [6, 26, 54, 82, 110, 138, 166]},
        40: {'num_ap': 46, 'centers': [6, 30, 58, 86, 114, 142, 170]},
}

def is_valid(coordinates, size):
    """check if the center of an alignment patterns falls over a position
    detection pattern. Returns False in this case.

    TODO: find a nicer way.
    """
    x, y = coordinates
    if x == 6:
        if y == 6 or y == (size - 7) or y == (size - 8):
            return False
        else:
            return True
    elif (x == (size - 7) or x == (size - 8)) and y == 6:
        return False
    else:
        return True

def get_coordinates(symbol_version):
    """Given a symbol version number returns a list of alignment patterns
    center coordinates."""
    centers = get_centers(symbol_version)
    coordinates = [x for x in product(centers, centers)]
    coordinates = [x for x in coordinates if is_valid(x,
        get_qr_size(symbol_version))]
    return coordinates

def get_num_ap(symbol_version):
    """Given a symbol version number returns the number of alignment patters
    of the symbol.
    """
    return patterns[symbol_version]['num_ap']

def get_centers(symbol_version):
    return patterns[symbol_version]['centers']

def test_coordinates():
    assert set(get_coordinates(7)) == set([(6,22), (22, 6), (22, 22), (22, 38),
        (38, 22), (38, 38)])

def test_coordinates_random():
    for symbol_version in range(1, 41):
        assert len(get_coordinates(symbol_version)) == get_num_ap(symbol_version)
