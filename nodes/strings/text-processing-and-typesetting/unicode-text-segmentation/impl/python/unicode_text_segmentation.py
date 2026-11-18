# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unicode-text-segmentation/. The authors are listed in prov/DB4AFE.jsonl.

"""Default grapheme cluster, word and sentence boundaries of UAX 29 revision 45 (Unicode 16.0.0).

Boundaries are offsets in code points from 0 to n. Position b is between s[b-1] and s[b].
The property tables are small hand-built parts of the Unicode Character Database 16.0.0.
Code points that are not in a table get the default value of the file (Other, None, False).
"""

from bisect import bisect_right

# Grapheme_Cluster_Break (GCB). Ranges copied from GraphemeBreakProperty-16.0.0.txt
# (Date: 2024-05-31, 18:09:38 GMT), one range per data line:
#   0000..0009 ; Control       000A ; LF       000D ; CR
#   0300..036F ; Extend        0600..0605 ; Prepend
#   0903 ; SpacingMark         093C ; Extend   093E..0940 ; SpacingMark   094D ; Extend
#   0A03 ; SpacingMark         0D4E ; Prepend
#   1100..115F ; L             1160..11A7 ; V   11A8..11FF ; T
#   200B ; Control             200C ; Extend   200D ; ZWJ   2060..2064 ; Control
#   AC00 ; LV                  AC01..AC1B ; LVT
#   1F1E6..1F1FF ; Regional_Indicator          1F3FB..1F3FF ; Extend
# The file gives "@missing ... Other" for all other code points.
_GCB = [
    (0x0000, 0x0009, "Control"), (0x000A, 0x000A, "LF"), (0x000D, 0x000D, "CR"),
    (0x0300, 0x036F, "Extend"), (0x0600, 0x0605, "Prepend"),
    (0x0903, 0x0903, "SpacingMark"), (0x093C, 0x093C, "Extend"),
    (0x093E, 0x0940, "SpacingMark"), (0x094D, 0x094D, "Extend"),
    (0x0A03, 0x0A03, "SpacingMark"), (0x0D4E, 0x0D4E, "Prepend"),
    (0x1100, 0x115F, "L"), (0x1160, 0x11A7, "V"), (0x11A8, 0x11FF, "T"),
    (0x200B, 0x200B, "Control"), (0x200C, 0x200C, "Extend"), (0x200D, 0x200D, "ZWJ"),
    (0x2060, 0x2064, "Control"), (0xAC00, 0xAC00, "LV"), (0xAC01, 0xAC1B, "LVT"),
    (0x1F1E6, 0x1F1FF, "RI"), (0x1F3FB, 0x1F3FF, "Extend"),
]

# Indic_Conjunct_Break (InCB). Ranges copied from DerivedCoreProperties-16.0.0.txt:
#   0300..036F ; InCB; Extend     0915..0939 ; InCB; Consonant
#   093C ; InCB; Extend           094D ; InCB; Linker      200D ; InCB; Extend
# "@missing: 0000..10FFFF; InCB; None".
_INCB = [
    (0x0300, 0x036F, "Extend"), (0x0915, 0x0939, "Consonant"), (0x093C, 0x093C, "Extend"),
    (0x094D, 0x094D, "Linker"), (0x200D, 0x200D, "Extend"),
]

# Extended_Pictographic. Ranges copied from emoji-data-16.0.0.txt (Date: 2024-05-01):
#   00A9 ; 231A..231B ; 26FE..2701 ; 1F6D1..1F6D2
# The code points 1F467, 1F468, 1F469 and 1F476 are Extended_Pictographic in the same file,
# inside longer ranges that are not copied here, so they are listed one by one.
_PICT = [
    (0x00A9, 0x00A9, True), (0x231A, 0x231B, True), (0x26FE, 0x2701, True),
    (0x1F467, 0x1F469, True), (0x1F476, 0x1F476, True), (0x1F6D1, 0x1F6D2, True),
]

# Word_Break (WB). Ranges copied from WordBreakProperty-16.0.0.txt (Date: 2024-07-29, 16:27:36 GMT):
#   000A ; LF   000D ; CR   0020 ; WSegSpace   0022 ; Double_Quote   0027 ; Single_Quote
#   002C ; MidNum   002E ; MidNumLet   0030..0039 ; Numeric   003A ; MidLetter   003B ; MidNum
#   0041..005A ; ALetter   005F ; ExtendNumLet   0061..007A ; ALetter   0300..036F ; Extend
#   05D0..05EA ; Hebrew_Letter   0641..064A ; ALetter   200D ; ZWJ   2060..2064 ; Format
#   3000 ; WSegSpace   3031..3035 ; Katakana   1F1E6..1F1FF ; Regional_Indicator
#   1F3FB..1F3FF ; Extend
_WB = [
    (0x000A, 0x000A, "LF"), (0x000D, 0x000D, "CR"), (0x0020, 0x0020, "WSegSpace"),
    (0x0022, 0x0022, "Double_Quote"), (0x0027, 0x0027, "Single_Quote"),
    (0x002C, 0x002C, "MidNum"), (0x002E, 0x002E, "MidNumLet"), (0x0030, 0x0039, "Numeric"),
    (0x003A, 0x003A, "MidLetter"), (0x003B, 0x003B, "MidNum"), (0x0041, 0x005A, "ALetter"),
    (0x005F, 0x005F, "ExtendNumLet"), (0x0061, 0x007A, "ALetter"), (0x0300, 0x036F, "Extend"),
    (0x05D0, 0x05EA, "Hebrew_Letter"), (0x0641, 0x064A, "ALetter"), (0x200D, 0x200D, "ZWJ"),
    (0x2060, 0x2064, "Format"), (0x3000, 0x3000, "WSegSpace"), (0x3031, 0x3035, "Katakana"),
    (0x1F1E6, 0x1F1FF, "RI"), (0x1F3FB, 0x1F3FF, "Extend"),
]

# Sentence_Break (SB). Ranges copied from SentenceBreakProperty-16.0.0.txt (Date: 2024-07-29, 16:27:32 GMT):
#   000A ; LF   000D ; CR   0020 ; Sp   0021 ; STerm   0022 ; Close   0027 ; Close   0028 ; Close
#   0029 ; Close   002C ; SContinue   002E ; ATerm   0030..0039 ; Numeric   003F ; STerm
#   0041..005A ; Upper   0061..007A ; Lower   00A0 ; Sp   0300..036F ; Extend   0641..064A ; OLetter
#   200C..200D ; Extend   2018 ; Close   2019 ; Close   201B..201C ; Close   201D ; Close
#   2060..2064 ; Format   3002 ; STerm   4E00..A014 ; OLetter
_SB = [
    (0x000A, 0x000A, "LF"), (0x000D, 0x000D, "CR"), (0x0020, 0x0020, "Sp"),
    (0x0021, 0x0021, "STerm"), (0x0022, 0x0022, "Close"), (0x0027, 0x0029, "Close"),
    (0x002C, 0x002C, "SContinue"), (0x002E, 0x002E, "ATerm"), (0x0030, 0x0039, "Numeric"),
    (0x003F, 0x003F, "STerm"), (0x0041, 0x005A, "Upper"), (0x0061, 0x007A, "Lower"),
    (0x00A0, 0x00A0, "Sp"), (0x0300, 0x036F, "Extend"), (0x0641, 0x064A, "OLetter"),
    (0x200C, 0x200D, "Extend"), (0x2018, 0x2019, "Close"), (0x201B, 0x201D, "Close"),
    (0x2060, 0x2064, "Format"), (0x3002, 0x3002, "STerm"), (0x4E00, 0xA014, "OLetter"),
]


def _lookup(ranges, default):
    starts = [lo for lo, _, _ in ranges]

    def get(c: str):
        cp = ord(c)
        k = bisect_right(starts, cp) - 1
        if k >= 0 and ranges[k][0] <= cp <= ranges[k][1]:
            return ranges[k][2]
        return default

    return get


gcb = _lookup(_GCB, "Other")
incb = _lookup(_INCB, "None")
ext_pict = _lookup(_PICT, False)
wb = _lookup(_WB, "Other")
sb = _lookup(_SB, "Other")

_CONTROL = ("Control", "CR", "LF")


def grapheme_boundaries(s: str, extended: bool = True) -> list[int]:
    """Return the extended grapheme cluster boundaries of s (rules GB1 to GB999).

    With extended=False, return the legacy grapheme cluster boundaries: GB9a, GB9b and
    GB9c are not used.
    """
    n = len(s)
    if n == 0:
        return [0]
    bounds = [0]  # @line L1
    ri = 0  # number of RI code points that end right before position i
    ep = False  # the text so far ends with ExtPict Extend*
    pict = False  # the text before s[i-1] ends with ExtPict Extend*
    conj = 0  # 0: none, 1: Consonant [Extend Linker]* without Linker, 2: with a Linker
    for i in range(1, n):  # @line L2
        c = s[i - 1]
        a, b = gcb(c), gcb(s[i])  # @line L3
        pict = ep  # @line L4
        ep = ext_pict(c) or (ep and a == "Extend")
        ri = ri + 1 if a == "RI" else 0
        k = incb(c)
        if k == "Consonant":
            conj = 1
        elif k == "Linker" and conj:
            conj = 2
        elif k != "Extend":
            conj = 0
        if a == "CR" and b == "LF":  # @line L5
            brk = False
        elif a in _CONTROL or b in _CONTROL:  # @line L6
            brk = True
        elif ((a == "L" and b in ("L", "V", "LV", "LVT"))  # @line L7
              or (a in ("LV", "V") and b in ("V", "T"))
              or (a in ("LVT", "T") and b == "T")):
            brk = False
        elif b in ("Extend", "ZWJ") or (extended and (b == "SpacingMark" or a == "Prepend")):  # @line L8
            brk = False
        elif extended and conj == 2 and incb(s[i]) == "Consonant":  # @line L9
            brk = False
        elif pict and a == "ZWJ" and ext_pict(s[i]):  # @line L10
            brk = False
        elif a == "RI" and b == "RI" and ri % 2 == 1:  # @line L11
            brk = False
        else:  # @line L12
            brk = True
        if brk:  # @line L13
            bounds.append(i)
    bounds.append(n)  # @line L14
    return bounds  # @line L15


def grapheme_clusters(s: str, extended: bool = True) -> list[str]:
    b = grapheme_boundaries(s, extended)
    return [s[b[j]:b[j + 1]] for j in range(len(b) - 1)]


# ---------------------------------------------------------------- words

_AH = ("ALetter", "Hebrew_Letter")
_MIDLETQ = ("MidLetter", "MidNumLet", "Single_Quote")
_MIDNUMQ = ("MidNum", "MidNumLet", "Single_Quote")
_WB_IGNORE = ("Extend", "Format", "ZWJ")
_WB_NEWLINE = ("Newline", "CR", "LF")


def _prev_index(p, i, ignore, stops):
    """Index of the code point that stands for the text before position i after the
    rule X (ignore)* -> X (WB4 or SB5). Return -1 at the start of the text."""
    j = i - 1
    while j >= 0 and p[j] in ignore:
        j -= 1
    if j < 0 or p[j] in stops:
        # The ignored code points after sot or a line separator are not absorbed:
        # the first of them stands for itself.
        return j + 1 if j + 1 < i else j
    return j


def _next_index(p, i, ignore):
    """Index of the first code point at or after i that is not ignored, or len(p)."""
    while i < len(p) and p[i] in ignore:
        i += 1
    return i


def word_boundaries(s: str) -> list[int]:
    """Return the default word boundaries of s (rules WB1 to WB999)."""
    n = len(s)
    if n == 0:
        return [0]
    p = [wb(c) for c in s]
    pict = [ext_pict(c) for c in s]
    bounds = [0]
    for i in range(1, n):
        a, b = p[i - 1], p[i]
        if a == "CR" and b == "LF":  # WB3
            brk = False
        elif a in _WB_NEWLINE or b in _WB_NEWLINE:  # WB3a, WB3b
            brk = True
        elif a == "ZWJ" and pict[i]:  # WB3c
            brk = False
        elif a == "WSegSpace" and b == "WSegSpace":  # WB3d
            brk = False
        elif b in _WB_IGNORE:  # WB4
            brk = False
        else:
            brk = _word_rules(p, i)
        if brk:
            bounds.append(i)
    bounds.append(n)
    return bounds


def _word_rules(p, i):
    """WB5 to WB999 at position i, on the sequence after WB4. p[i] is not ignored."""
    j = _prev_index(p, i, _WB_IGNORE, _WB_NEWLINE)
    a = p[j]
    b = p[i]
    jj = _prev_index(p, j, _WB_IGNORE, _WB_NEWLINE) if j > 0 else -1
    aa = p[jj] if jj >= 0 else None
    k = _next_index(p, i + 1, _WB_IGNORE)
    c = p[k] if k < len(p) else None
    if a in _AH and b in _AH:  # WB5
        return False
    if a in _AH and b in _MIDLETQ and c in _AH:  # WB6
        return False
    if aa in _AH and a in _MIDLETQ and b in _AH:  # WB7
        return False
    if a == "Hebrew_Letter" and b == "Single_Quote":  # WB7a
        return False
    if a == "Hebrew_Letter" and b == "Double_Quote" and c == "Hebrew_Letter":  # WB7b
        return False
    if aa == "Hebrew_Letter" and a == "Double_Quote" and b == "Hebrew_Letter":  # WB7c
        return False
    if a == "Numeric" and b == "Numeric":  # WB8
        return False
    if a in _AH and b == "Numeric":  # WB9
        return False
    if a == "Numeric" and b in _AH:  # WB10
        return False
    if aa == "Numeric" and a in _MIDNUMQ and b == "Numeric":  # WB11
        return False
    if a == "Numeric" and b in _MIDNUMQ and c == "Numeric":  # WB12
        return False
    if a == "Katakana" and b == "Katakana":  # WB13
        return False
    if a in _AH + ("Numeric", "Katakana", "ExtendNumLet") and b == "ExtendNumLet":  # WB13a
        return False
    if a == "ExtendNumLet" and b in _AH + ("Numeric", "Katakana"):  # WB13b
        return False
    if a == "RI" and b == "RI":  # WB15, WB16
        count = 0
        t = j
        while t >= 0 and p[t] == "RI":
            count += 1
            t = _prev_index(p, t, _WB_IGNORE, _WB_NEWLINE) if t > 0 else -1
        if count % 2 == 1:
            return False
    return True  # WB999


# ---------------------------------------------------------------- sentences

_SB_IGNORE = ("Extend", "Format")
_PARASEP = ("Sep", "CR", "LF")
_SATERM = ("STerm", "ATerm")


def sentence_boundaries(s: str) -> list[int]:
    """Return the default sentence boundaries of s (rules SB1 to SB998)."""
    n = len(s)
    if n == 0:
        return [0]
    p = [sb(c) for c in s]
    bounds = [0]
    for i in range(1, n):
        a, b = p[i - 1], p[i]
        if a == "CR" and b == "LF":  # SB3
            brk = False
        elif a in _PARASEP:  # SB4
            brk = True
        elif b in _SB_IGNORE:  # SB5
            brk = False
        else:
            brk = _sentence_rules(p, i)
        if brk:
            bounds.append(i)
    bounds.append(n)
    return bounds


def _sentence_rules(p, i):
    """SB6 to SB998 at position i, on the sequence after SB5. p[i] is not ignored."""
    prev = lambda t: _prev_index(p, t, _SB_IGNORE, _PARASEP) if t > 0 else -1  # noqa: E731
    j = prev(i)
    a, b = p[j], p[i]
    jj = prev(j)
    aa = p[jj] if jj >= 0 else None
    if a == "ATerm" and b == "Numeric":  # SB6
        return False
    if aa in ("Upper", "Lower") and a == "ATerm" and b == "Upper":  # SB7
        return False
    # Match SATerm Close* Sp* ending right before i.
    t = j
    sp = 0
    while t >= 0 and p[t] == "Sp":
        sp += 1
        t = prev(t)
    close = 0
    while t >= 0 and p[t] == "Close":
        close += 1
        t = prev(t)
    term = p[t] if t >= 0 and p[t] in _SATERM else None
    if term is None:
        return False  # SB998
    if term == "ATerm":  # SB8
        k = i
        while k < len(p) and p[k] not in ("OLetter", "Upper", "Lower") + _PARASEP + _SATERM:
            k += 1
        if k < len(p) and p[k] == "Lower":
            return False
    if b in ("SContinue",) + _SATERM:  # SB8a
        return False
    if sp == 0 and b in ("Close", "Sp") + _PARASEP:  # SB9
        return False
    if b in ("Sp",) + _PARASEP:  # SB10
        return False
    return True  # SB11


def segments(s: str, bounds: list[int]) -> list[str]:
    return [s[bounds[j]:bounds[j + 1]] for j in range(len(bounds) - 1)]
