from qrcode.qrdraw import position_detection_pattern, bch_15_5

#def test_position_detection_pattern():
#    """Tautologic test till I'll refactor.
#    """
#    a = position_detection_pattern(1)
#    assert a[0].tolist() == a[6].tolist() == [1, 1, 1, 1, 1, 1, 1, 0, 9, 9, 9,
#            9, 9, 0, 1, 1, 1, 1, 1, 1, 1]
#    assert a[1].tolist() == a[5].tolist() == [1, 0, 0, 0, 0, 0, 1, 0, 9, 9, 9,
#            9, 9, 0, 1, 0, 0, 0, 0, 0, 1]
#    assert a[2].tolist() == a[3].tolist() == a[4].tolist() == [1, 0, 1, 1, 1,
#            0, 1, 0, 9, 9, 9, 9, 9, 0, 1, 0, 1, 1, 1, 0, 1]
#
#    assert a[-1].tolist() == [1, 1, 1, 1, 1, 1, 1] + [0] + [9] * 13
#    assert a[-2].tolist() == [1, 0, 0, 0, 0, 0, 1] + [0] + [9] * 13
#    assert a[-3].tolist() == a[-4].tolist() == a[-5].tolist() == [1, 0, 1, 1, 1, 0, 1] + [0] + [9] * 13
#
#    assert a[7].tolist() == [0] * 8 + [9] * 5 + [0] * 8
#    assert a[-8].tolist() == [0] * 8 + [9] * 13

def test_bch_15_5():
    assert bch_15_5('00101') == '001010011011100'
