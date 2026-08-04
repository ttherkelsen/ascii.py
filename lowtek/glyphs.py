# Type is:
# B n e s w - Box drawing glyphs (straight)
# D nw se   - Box drawing glyphs (Diagonal)
# C num     - Braile (for counting)
# P num     - Progress bars
#
# For box drawing, each compass direction is a single character
# which determines the type of line going in that direction
# from the center of the glyph.
#
# s - single line
# d - double line
# t - thick line
# r - round corner
# 3 - 3-dotted line
# 4 - 4-dotted line
# 5 - thick 3-dotted line
# 6 - thick 4-dotted line

GLYPHS = {
    'B s s': 0x2500,
    'B t t': 0x2501,
    'Bs s ': 0x2502,
    'Bt t ': 0x2503,
    'B 3 3': 0x2504,
    'B 5 5': 0x2505,
    'B3 3 ': 0x2506,
    'B5 5 ': 0x2507,
    'B 4 4': 0x2508,
    'B 6 6': 0x2509,
    'B4 4 ': 0x250a,
    'B6 6 ': 0x250b,
    'B ss ': 0x250c,
    'B ts ': 0x250d,
    'B st ': 0x250e,
    'B tt ': 0x250f,
    'Bssss': 0x253c,
}
