# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unicode-collation-algorithm/. The authors are listed in prov/7HSE2K.jsonl.
"""The Unicode Collation Algorithm (UTS 10) with a subset of the DUCET.

The main algorithm of UTS 10 section 7: normalize to NFD (S1), map the string to
collation elements by longest match with discontiguous contractions (S2.1), synthesize
implicit weights for code points that are not in the table (S2.2, section 10.1.3),
apply variable weighting (S2.3, section 4), form a sort key (S3) and compare sort keys
in binary (S4).

The table below is a short subset of allkeys-16.0.0.txt (DUCET, Date: 2024-04-25).
The lines are copied verbatim. A code point that is not in the subset gets implicit
weights, so the results agree with the full DUCET only for strings over the code points
of the subset (after NFD).
"""

import unicodedata

ALLKEYS_LINES = """\
@version 16.0.0
0009  ; [*0201.0020.0002] # HORIZONTAL TABULATION (in ISO 6429)
000A  ; [*0202.0020.0002] # LINE FEED (in ISO 6429)
0020  ; [*0209.0020.0002] # SPACE
0021  ; [*0269.0020.0002] # EXCLAMATION MARK
0022  ; [*033A.0020.0002] # QUOTATION MARK
0027  ; [*0337.0020.0002] # APOSTROPHE
002D  ; [*020D.0020.0002] # HYPHEN-MINUS
005F  ; [*020B.0020.0002] # LOW LINE
0300  ; [.0000.0025.0002] # COMBINING GRAVE ACCENT
0301  ; [.0000.0024.0002] # COMBINING ACUTE ACCENT
0302  ; [.0000.0027.0002] # COMBINING CIRCUMFLEX ACCENT
0303  ; [.0000.002D.0002] # COMBINING TILDE
0306  ; [.0000.0026.0002] # COMBINING BREVE
0307  ; [.0000.002E.0002] # COMBINING DOT ABOVE
0308  ; [.0000.002B.0002] # COMBINING DIAERESIS
0309  ; [.0000.003B.0002] # COMBINING HOOK ABOVE
030A  ; [.0000.0029.0002] # COMBINING RING ABOVE
0323  ; [.0000.0042.0002] # COMBINING DOT BELOW
0327  ; [.0000.0030.0002] # COMBINING CEDILLA
0331  ; [.0000.0049.0002] # COMBINING MACRON BELOW
0332  ; [.0000.0021.0002] # COMBINING LOW LINE
0030  ; [.217D.0020.0002] # DIGIT ZERO
0031  ; [.217E.0020.0002] # DIGIT ONE
0032  ; [.217F.0020.0002] # DIGIT TWO
0033  ; [.2180.0020.0002] # DIGIT THREE
0034  ; [.2181.0020.0002] # DIGIT FOUR
0039  ; [.2186.0020.0002] # DIGIT NINE
0061  ; [.2380.0020.0002] # LATIN SMALL LETTER A
0041  ; [.2380.0020.0008] # LATIN CAPITAL LETTER A
00AA  ; [.2380.0020.0014] # FEMININE ORDINAL INDICATOR
00E6  ; [.2380.0020.0004][.0000.011E.0004][.23E7.0020.0004] # LATIN SMALL LETTER AE
00C6  ; [.2380.0020.000A][.0000.011E.0004][.23E7.0020.000A] # LATIN CAPITAL LETTER AE
0062  ; [.239A.0020.0002] # LATIN SMALL LETTER B
0042  ; [.239A.0020.0008] # LATIN CAPITAL LETTER B
0063  ; [.23B4.0020.0002] # LATIN SMALL LETTER C
0043  ; [.23B4.0020.0008] # LATIN CAPITAL LETTER C
0064  ; [.23CA.0020.0002] # LATIN SMALL LETTER D
0044  ; [.23CA.0020.0008] # LATIN CAPITAL LETTER D
0065  ; [.23E7.0020.0002] # LATIN SMALL LETTER E
0045  ; [.23E7.0020.0008] # LATIN CAPITAL LETTER E
0066  ; [.2422.0020.0002] # LATIN SMALL LETTER F
0046  ; [.2422.0020.0008] # LATIN CAPITAL LETTER F
0067  ; [.2431.0020.0002] # LATIN SMALL LETTER G
0047  ; [.2431.0020.0008] # LATIN CAPITAL LETTER G
0068  ; [.2458.0020.0002] # LATIN SMALL LETTER H
0048  ; [.2458.0020.0008] # LATIN CAPITAL LETTER H
0069  ; [.2473.0020.0002] # LATIN SMALL LETTER I
0049  ; [.2473.0020.0008] # LATIN CAPITAL LETTER I
0130  ; [.2473.0020.0008][.0000.002E.0002] # LATIN CAPITAL LETTER I WITH DOT ABOVE
0131  ; [.2477.0020.0002] # LATIN SMALL LETTER DOTLESS I
006A  ; [.248F.0020.0002] # LATIN SMALL LETTER J
004A  ; [.248F.0020.0008] # LATIN CAPITAL LETTER J
006B  ; [.24A8.0020.0002] # LATIN SMALL LETTER K
004B  ; [.24A8.0020.0008] # LATIN CAPITAL LETTER K
006C  ; [.24BC.0020.0002] # LATIN SMALL LETTER L
004C  ; [.24BC.0020.0008] # LATIN CAPITAL LETTER L
006D  ; [.24F6.0020.0002] # LATIN SMALL LETTER M
004D  ; [.24F6.0020.0008] # LATIN CAPITAL LETTER M
006E  ; [.2505.0020.0002] # LATIN SMALL LETTER N
004E  ; [.2505.0020.0008] # LATIN CAPITAL LETTER N
006F  ; [.252C.0020.0002] # LATIN SMALL LETTER O
004F  ; [.252C.0020.0008] # LATIN CAPITAL LETTER O
0070  ; [.255C.0020.0002] # LATIN SMALL LETTER P
0050  ; [.255C.0020.0008] # LATIN CAPITAL LETTER P
0071  ; [.2571.0020.0002] # LATIN SMALL LETTER Q
0051  ; [.2571.0020.0008] # LATIN CAPITAL LETTER Q
0072  ; [.2584.0020.0002] # LATIN SMALL LETTER R
0052  ; [.2584.0020.0008] # LATIN CAPITAL LETTER R
0073  ; [.25C6.0020.0002] # LATIN SMALL LETTER S
0053  ; [.25C6.0020.0008] # LATIN CAPITAL LETTER S
00DF  ; [.25C6.0020.0004][.0000.011E.0004][.25C6.0020.0004] # LATIN SMALL LETTER SHARP S
1E9E  ; [.25C6.0020.000A][.0000.011E.0004][.25C6.0020.000A] # LATIN CAPITAL LETTER SHARP S
0074  ; [.25F1.0020.0002] # LATIN SMALL LETTER T
0054  ; [.25F1.0020.0008] # LATIN CAPITAL LETTER T
0075  ; [.2614.0020.0002] # LATIN SMALL LETTER U
0055  ; [.2614.0020.0008] # LATIN CAPITAL LETTER U
0076  ; [.2644.0020.0002] # LATIN SMALL LETTER V
0056  ; [.2644.0020.0008] # LATIN CAPITAL LETTER V
0077  ; [.2656.0020.0002] # LATIN SMALL LETTER W
0057  ; [.2656.0020.0008] # LATIN CAPITAL LETTER W
0078  ; [.2660.0020.0002] # LATIN SMALL LETTER X
0058  ; [.2660.0020.0008] # LATIN CAPITAL LETTER X
0079  ; [.266C.0020.0002] # LATIN SMALL LETTER Y
0059  ; [.266C.0020.0008] # LATIN CAPITAL LETTER Y
007A  ; [.2682.0020.0002] # LATIN SMALL LETTER Z
005A  ; [.2682.0020.0008] # LATIN CAPITAL LETTER Z
"""

MODES = ("non-ignorable", "blanked", "shifted", "shift-trimmed")


def parse_allkeys(text: str) -> dict:
    """Parse lines in the allkeys.txt format (UTS 10 section 12.1).

    Return a dict from a tuple of code points (as str) to a list of collation elements.
    A collation element is a tuple (variable, primary, secondary, tertiary).
    """
    table = {}
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line or line.startswith("@"):
            continue
        left, right = line.split(";", 1)
        key = tuple(chr(int(h, 16)) for h in left.split())
        ces = []
        for part in right.strip().lstrip("[").rstrip("]").split("]["):
            variable = part[0] == "*"
            p, s, t = (int(w, 16) for w in part[1:].split("."))
            ces.append((variable, p, s, t))
        table[key] = ces
    return table


DUCET_SUBSET = parse_allkeys(ALLKEYS_LINES)

# Core Han for implicit weights: Unified_Ideograph=True and Block=CJK_Unified_Ideographs
# or CJK_Compatibility_Ideographs (UTS 10 Table 16). Only these ranges are listed here.
_CORE_HAN = [(0x4E00, 0x9FFF)] + [(c, c) for c in (
    0xFA0E, 0xFA0F, 0xFA11, 0xFA13, 0xFA14, 0xFA1F, 0xFA21, 0xFA23, 0xFA24, 0xFA27, 0xFA28, 0xFA29)]
# Other Han: Unified_Ideograph=True in other blocks. Only extensions A and B are listed.
_OTHER_HAN = [(0x3400, 0x4DBF), (0x20000, 0x2A6DF)]


def _in(ranges, cp):
    return any(lo <= cp <= hi for lo, hi in ranges)


def implicit_weights(c: str) -> list:
    """Implicit weights [.AAAA.0020.0002][.BBBB.0000.0000] of section 10.1.3."""
    cp = ord(c)
    if _in(_CORE_HAN, cp):
        base = 0xFB40
    elif _in(_OTHER_HAN, cp):
        base = 0xFB80
    else:
        base = 0xFBC0
    return [(False, base + (cp >> 15), 0x0020, 0x0002), (False, (cp & 0x7FFF) | 0x8000, 0, 0)]


def collation_elements(s: str, table=None) -> list:
    """Steps S1 and S2.1, S2.2, S2.4, S2.5: the collation element array of s."""
    if table is None:
        table = DUCET_SUBSET
    longest = max(len(k) for k in table)
    x = list(unicodedata.normalize("NFD", s))  # @line L1
    ces = []
    i = 0  # @line L2
    while i < len(x):  # @line L3
        j = min(len(x), i + longest)  # @line L4
        while j > i + 1 and tuple(x[i:j]) not in table:
            j -= 1
        key = tuple(x[i:j])
        if key in table:
            k = j  # @line L5
            blocker = 0  # the largest ccc of a skipped non-starter
            while k < len(x):
                c = unicodedata.combining(x[k])
                if c == 0:
                    break
                if blocker < c and key + (x[k],) in table:
                    key = key + (x[k],)
                    del x[k]
                else:
                    blocker = max(blocker, c)
                    k += 1
            ces.extend(table[key])  # @line L6
        else:
            ces.extend(implicit_weights(x[i]))
        i = j  # @line L7
    return ces


def apply_variable_weighting(ces: list, mode: str) -> list:
    """Step S2.3 and section 4: return four-level weights (p, s, t, q)."""
    if mode not in MODES:
        raise ValueError(mode)
    out = []
    after_variable = False
    for variable, p, s, t in ces:
        if mode == "non-ignorable":
            out.append((p, s, t, 0))
        elif variable:
            after_variable = True
            out.append((0, 0, 0, p if mode != "blanked" else 0))
        elif p == 0 and s == 0 and t == 0:
            out.append((0, 0, 0, 0))
        elif p == 0 and after_variable:
            out.append((0, 0, 0, 0))
        else:
            if p != 0:
                after_variable = False
            out.append((p, s, t, 0xFFFF if mode != "blanked" else 0))
    return out


def sort_key(s: str, mode: str = "shifted", table=None) -> tuple:
    """Step S3: the sort key of s, a tuple of 16-bit weights with 0000 separators."""
    w = apply_variable_weighting(collation_elements(s, table), mode)  # @line L8
    levels = 3 if mode in ("non-ignorable", "blanked") else 4
    key = []  # @line L9
    for level in range(levels):  # @line L10
        if level > 0:  # @line L11
            key.append(0)
        part = [ce[level] for ce in w if ce[level] != 0]  # @line L12
        if level == 3 and mode == "shift-trimmed":  # @line L13
            while part and part[-1] == 0xFFFF:
                part.pop()
        key.extend(part)
    return tuple(key)  # @line L14


def compare(a: str, b: str, mode: str = "shifted", table=None) -> int:
    """Step S4: -1, 0 or 1 by binary comparison of the sort keys."""
    ka, kb = sort_key(a, mode, table), sort_key(b, mode, table)  # @line L15
    return (ka > kb) - (ka < kb)


def format_key(key: tuple) -> str:
    """Write a sort key as hexadecimal weights with | for the level separators."""
    return " ".join("|" if w == 0 else f"{w:04X}" for w in key)
