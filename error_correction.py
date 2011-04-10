ecl_index = {'L': 0, 'M': 1, 'Q': 2, 'H': 3}

# ISO/IEC 18004 - Table 13-22 (partial)
blocks_per_ecl = {
        1: [[19],
            [16],
            [13],
            [9]],

        2: [[34],
            [28],
            [22],
            [16]],

        3: [[55],
            [44],
            [17, 17],
            [13, 13]],

        4: [[80],
            [32, 32],
            [24, 24],
            [9] * 4],

        5: [[108],
            [43, 43],
            [15, 15, 16, 16],
            [11, 11, 12, 12]],

        6: [[68, 68],
            [27] * 4,
            [19] * 4,
            [15] * 4],

        7: [[78, 78],
            [31] * 4,
            [14, 14] + [15] * 4,
            [13] * 4 + [14]],

        8: [[97, 97],
            [38, 38, 39, 39],
            [18] * 4 + [19, 19],
            [14] * 4 + [15, 15]],

        9: [[116, 116],
            [36] * 3 + [37, 37],
            [16] * 4 + [17] * 4,
            [12] * 4 + [13] * 4],

        10: [[68, 68, 69, 69],
            [43] * 4 + [44],
            [19] * 6 + [20, 20],
            [15] * 6 + [16, 16]],

        11: [[81] * 4,
            [50] + [51] * 4,
            [22] * 4 + [23] * 4,
            [12] * 3 + [13] * 8],

        12: [[92, 92, 93, 93],
            [36] * 6 + [37, 37],
            [20] * 4 + [21] * 6,
            [14] * 7 + [15] * 4],

        13: [[107] * 4,
            [37] * 8 + [38],
            [20] * 8 + [21] * 4,
            [11] * 12 + [12] * 4],

        14: [[115] * 3 + [116],
            [40] * 4 + [41] * 5,
            [16] * 11 + [17] * 5,
            [12] * 11 + [13] * 5],

        15: [[87] * 5 + [88],
            [41] * 5 + [42] * 5,
            [24] * 5 + [25] * 7,
            [12] * 11 + [13] * 7],

        16: [[98] * 5 + [99],
            [45] * 7 + [46] * 3,
            [19] * 15 + [20, 20],
            [15] * 3 + [16] * 13],

        17: [[107] + [108] * 5,
            [46] * 10 + [47],
            [22] + [23] * 15,
            [14] * 2 + [15] * 17],

        18: [[120] * 5 + [121],
            [43] * 9 + [44] * 4,
            [22] * 17 + [23],
            [14] * 2 + [15] * 19],

        19: [[113] * 3 + [114] * 4,
            [44] * 3 + [45] * 11,
            [21] * 17 + [22] * 4,
            [13] * 9 + [14] * 16],

        20: [[107] * 3 + [108] * 5,
            [41] * 3 + [42] * 13,
            [24] * 15 + [25] * 5,
            [15] * 15 + [16] * 10],

        21: [[116] * 4 + [117] * 4,
            [42] * 17,
            [22] * 17 + [23] * 6,
            [16] * 19 + [17] * 6],

        22: [[111] * 2 + [112] * 7,
            [46] * 17,
            [24] * 7 + [25] * 16,
            [13] * 34],

        23: [[121] * 4 + [122] * 5,
            [47] * 4 + [48] * 14,
            [24] * 11 + [25] * 14,
            [15] * 16 + [16] * 14],

        24: [[117] * 6 + [118] * 4,
            [45] * 6 + [46] * 14,
            [24] * 11 + [25] * 16,
            [16] * 30 + [17] * 2],

        25: [[106] * 8 + [107] * 4,
            [47] * 8 + [48] * 13,
            [24] * 7 + [25] * 22,
            [15] * 22 + [16] * 13],

        26: [[114] * 10 + [115] * 2,
            [46] * 19 + [47] * 4,
            [22] * 28 + [23] * 6,
            [16] * 33 + [17] * 4],

        27: [[122] * 8 + [123] * 4,
            [45] * 22 + [46] * 3,
            [23] * 8 + [24] * 26,
            [15] * 12 + [16] * 28],

        28: [[117] * 3 + [118] * 10,
            [45] * 3 + [46] * 23,
            [24] * 4 + [25] * 31,
            [15] * 11 + [16] * 31],

        29: [[116] * 7 + [117] * 7,
            [45] * 21 + [46] * 7,
            [23] + [24] * 37,
            [15] * 19 + [16] * 26],

        30: [[115] * 5 + [116] * 10,
            [47] * 19 + [48] * 10,
            [24] * 15 + [25] * 25,
            [15] * 23 + [16] * 25],

        31: [[115] * 13 + [116] * 3,
            [46] * 2 + [47] * 29,
            [24] * 42 + [25],
            [15] * 23 + [16] * 28],

        32: [[115] * 17,
            [46] * 10 + [47] * 23,
            [24] * 10 + [25] * 35,
            [15] * 19 + [16] * 35],

        33: [[115] * 17 + [116],
            [46] * 14 + [47] * 21,
            [24] * 29 + [25] * 19,
            [15] * 11 + [16] * 46],

        34: [[115] * 13 + [116] * 6,
            [46] * 14 + [47] * 23,
            [24] * 44 + [25] * 7,
            [16] * 59 + [17]],

        35: [[121] * 12 + [122] * 7,
            [47] * 12 + [48] * 26,
            [24] * 39 + [25] * 14,
            [15] * 22 + [16] * 41],

        36: [[121] * 6 + [122] * 14,
            [47] * 6 + [48] * 34,
            [24] * 46 + [25] * 10,
            [15] * 2 + [16] * 64],

        37: [[122] * 17 + [123] * 4,
            [46] * 29 + [47] * 14,
            [24] * 49 + [25] * 10,
            [15] * 24 + [16] * 46],

        38: [[122] * 4 + [123] * 18,
            [46] * 13 + [47] * 32,
            [24] * 48 + [25] * 14,
            [15] * 42 + [16] * 32],

        39: [[117] * 20 + [118] * 4,
            [47] * 40 + [48] * 7,
            [24] * 43 + [25] * 22,
            [15] * 10 + [16] * 67],

        40: [[118] * 19 + [119] * 6,
            [47] * 18 + [48] * 31,
            [24] * 34 + [25] * 34,
            [15] * 20 + [16] * 61]}

def get_blocks(version, ecl):
    return blocks_per_ecl[version][ecl_index[ecl]]
