# -*- coding: utf-8 -*-

def symbol_version_determination(data_length, data_type,
        error_correction_level):
    max_data_capacity = get_max_data_capacity(data_length,
            data_type, error_correction_level)
    return choose_version(max_data_capacity)

def finder_pattern():
    """ 7x7
    #######
    #     #
    # ### #
    # ### #
    # ### #
    #     #
    #######
    """

    pass

def separators():
    """ a one-module wide separator between each position pattern
    and encoding region"""

    pass

def timing_pattern():
    """
    The horizontal and vertical Timing Patterns respectively consist of a one
    module wide row or column of alternating dark and light modules,
    commencing and ending with a dark module. The horizontal Timing Pattern
    runs across row 6 of the symbol between the separators for the upper
    Position Detection Patterns; the vertical Timing Pattern similarly runs
    down column 6 of the symbol between the separators for the left-hand
    Position Detection Patterns.  They enable the symbol density and version
    to be determined and provide datum positions for determining module
    coordinates.
    """

    pass

def alignment_pattern():
    """
    Each Alignment Pattern may be viewed as three superimposed concentric
    squares and is constructed of dark 5x́5 modules, light 3x3 modules and
    a single central dark module. The number of Alignment Patterns depends on
    the symbol version and they shall be placed in all Model 2 symbols of
    Version 2 or larger in positions defined in Annex E.
    """

    pass

def encoding_region():
    """
    This region shall contain the symbol characters representing data, those
    representing error correction codewords, the Version Information and
    Format Information. Refer to 8.7.1 for details of the symbol characters.
    Refer to 8.9 for details of the Format Information. Refer to 8.10 for
    details of the Version Information
    """

    data_regions()
    ecc_regions()
    version_information()
    format_information()
    pass

def quiet_zone():
    """
    This is a region 4X wide which shall be free of all other markings,
    surrounding the symbol on all four sides. Its nominal reflectance value
    shall be equal to that of the light modules.
    """
    
def add_error_correction(data):
    return reed_solomon_code(data)
