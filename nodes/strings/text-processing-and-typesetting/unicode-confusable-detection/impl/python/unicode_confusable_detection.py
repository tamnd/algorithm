# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unicode-confusable-detection/. The authors are listed in prov/N2QXMJ.jsonl.
"""Confusable detection of UTS 39 section 4 with a subset of confusables.txt.

internal_skeleton is the four steps of internalSkeleton. skeleton is bidiSkeleton(LTR, X)
for text where the bidirectional algorithm gives every character level 0, which is the
case when the text has no character of bidi class R, AL or AN and no explicit
directional formatting character. For such text bidiSkeleton(LTR, X) equals
internalSkeleton(X) (see proofs/correctness.md). Other text raises ValueError.

The tables are short subsets of the Unicode 16.0.0 data files. A code point that is not
in a table is treated as if it had no line there.
"""

import unicodedata

# confusables.txt 16.0.0 (Date: 2024-08-14, 23:39:57 GMT). The first three fields of each
# line are copied; the comments after "#" are shortened to the source name.
CONFUSABLES_LINES = (
    "FF41 ;\t0061 ;\tMA\t# FULLWIDTH LATIN SMALL LETTER A\n"
    "0251 ;\t0061 ;\tMA\t# LATIN SMALL LETTER ALPHA\n"
    "0430 ;\t0061 ;\tMA\t# CYRILLIC SMALL LETTER A\n"
    "0391 ;\t0041 ;\tMA\t# GREEK CAPITAL LETTER ALPHA\n"
    "0410 ;\t0041 ;\tMA\t# CYRILLIC CAPITAL LETTER A\n"
    "0392 ;\t0042 ;\tMA\t# GREEK CAPITAL LETTER BETA\n"
    "0412 ;\t0042 ;\tMA\t# CYRILLIC CAPITAL LETTER VE\n"
    "0435 ;\t0065 ;\tMA\t# CYRILLIC SMALL LETTER IE\n"
    "0415 ;\t0045 ;\tMA\t# CYRILLIC CAPITAL LETTER IE\n"
    "0441 ;\t0063 ;\tMA\t# CYRILLIC SMALL LETTER ES\n"
    "0421 ;\t0043 ;\tMA\t# CYRILLIC CAPITAL LETTER ES\n"
    "0501 ;\t0064 ;\tMA\t# CYRILLIC SMALL LETTER KOMI DE\n"
    "13A0 ;\t0044 ;\tMA\t# CHEROKEE LETTER A\n"
    "0456 ;\t0069 ;\tMA\t# CYRILLIC SMALL LETTER BYELORUSSIAN-UKRAINIAN I\n"
    "04CF ;\t0069 ;\tMA\t# CYRILLIC SMALL LETTER PALOCHKA\n"
    "0131 ;\t0069 ;\tMA\t# LATIN SMALL LETTER DOTLESS I\n"
    "0269 ;\t0069 ;\tMA\t# LATIN SMALL LETTER IOTA\n"
    "0458 ;\t006A ;\tMA\t# CYRILLIC SMALL LETTER JE\n"
    "0261 ;\t0067 ;\tMA\t# LATIN SMALL LETTER SCRIPT G\n"
    "007C ;\t006C ;\tMA\t# VERTICAL LINE\n"
    "0031 ;\t006C ;\tMA\t# DIGIT ONE\n"
    "0049 ;\t006C ;\tMA\t# LATIN CAPITAL LETTER I\n"
    "2160 ;\t006C ;\tMA\t# ROMAN NUMERAL ONE\n"
    "217C ;\t006C ;\tMA\t# SMALL ROMAN NUMERAL FIFTY\n"
    "FF4C ;\t006C ;\tMA\t# FULLWIDTH LATIN SMALL LETTER L\n"
    "2113 ;\t006C ;\tMA\t# SCRIPT SMALL L\n"
    "1D5C5 ;\t006C ;\tMA\t# MATHEMATICAL SANS-SERIF SMALL L\n"
    "01C0 ;\t006C ;\tMA\t# LATIN LETTER DENTAL CLICK\n"
    "0399 ;\t006C ;\tMA\t# GREEK CAPITAL LETTER IOTA\n"
    "0406 ;\t006C ;\tMA\t# CYRILLIC CAPITAL LETTER BYELORUSSIAN-UKRAINIAN I\n"
    "03BF ;\t006F ;\tMA\t# GREEK SMALL LETTER OMICRON\n"
    "043E ;\t006F ;\tMA\t# CYRILLIC SMALL LETTER O\n"
    "0D20 ;\t006F ;\tMA\t# MALAYALAM LETTER TTHA\n"
    "0A66 ;\t006F ;\tMA\t# GURMUKHI DIGIT ZERO\n"
    "0030 ;\t004F ;\tMA\t# DIGIT ZERO\n"
    "039F ;\t004F ;\tMA\t# GREEK CAPITAL LETTER OMICRON\n"
    "0B20 ;\t004F ;\tMA\t# ORIYA LETTER TTHA\n"
    "0440 ;\t0070 ;\tMA\t# CYRILLIC SMALL LETTER ER\n"
    "006D ;\t0072 006E ;\tMA\t# LATIN SMALL LETTER M\n"
    "0445 ;\t0078 ;\tMA\t# CYRILLIC SMALL LETTER HA\n"
    "0443 ;\t0079 ;\tMA\t# CYRILLIC SMALL LETTER U\n"
    "2010 ;\t002D ;\tMA\t# HYPHEN\n"
    "2212 ;\t002D ;\tMA\t# MINUS SIGN\n"
    "01C3 ;\t0021 ;\tMA\t# LATIN LETTER RETROFLEX CLICK\n"
    "0060 ;\t0027 ;\tMA\t# GRAVE ACCENT\n"
)

# DerivedCoreProperties-16.0.0.txt, lines of Default_Ignorable_Code_Point (a subset).
DICP_LINES = """\
00AD          ; Default_Ignorable_Code_Point # Cf       SOFT HYPHEN
034F          ; Default_Ignorable_Code_Point # Mn       COMBINING GRAPHEME JOINER
061C          ; Default_Ignorable_Code_Point # Cf       ARABIC LETTER MARK
115F..1160    ; Default_Ignorable_Code_Point # Lo   [2] HANGUL CHOSEONG FILLER..HANGUL JUNGSEONG FILLER
17B4..17B5    ; Default_Ignorable_Code_Point # Mn   [2] KHMER VOWEL INHERENT AQ..KHMER VOWEL INHERENT AA
180B..180D    ; Default_Ignorable_Code_Point # Mn   [3] MONGOLIAN FREE VARIATION SELECTOR ONE..MONGOLIAN FREE VARIATION SELECTOR THREE
180E          ; Default_Ignorable_Code_Point # Cf       MONGOLIAN VOWEL SEPARATOR
180F          ; Default_Ignorable_Code_Point # Mn       MONGOLIAN FREE VARIATION SELECTOR FOUR
200B..200F    ; Default_Ignorable_Code_Point # Cf   [5] ZERO WIDTH SPACE..RIGHT-TO-LEFT MARK
202A..202E    ; Default_Ignorable_Code_Point # Cf   [5] LEFT-TO-RIGHT EMBEDDING..RIGHT-TO-LEFT OVERRIDE
2060..2064    ; Default_Ignorable_Code_Point # Cf   [5] WORD JOINER..INVISIBLE PLUS
2065          ; Default_Ignorable_Code_Point # Cn       <reserved-2065>
2066..206F    ; Default_Ignorable_Code_Point # Cf  [10] LEFT-TO-RIGHT ISOLATE..NOMINAL DIGIT SHAPES
3164          ; Default_Ignorable_Code_Point # Lo       HANGUL FILLER
FE00..FE0F    ; Default_Ignorable_Code_Point # Mn  [16] VARIATION SELECTOR-1..VARIATION SELECTOR-16
FEFF          ; Default_Ignorable_Code_Point # Cf       ZERO WIDTH NO-BREAK SPACE
"""

# Scripts-16.0.0.txt (Date: 2024-04-30, 21:48:40 GMT), a subset.
SCRIPTS_LINES = """\
0020          ; Common # Zs       SPACE
002D          ; Common # Pd       HYPHEN-MINUS
0030..0039    ; Common # Nd  [10] DIGIT ZERO..DIGIT NINE
0041..005A    ; Latin # L&  [26] LATIN CAPITAL LETTER A..LATIN CAPITAL LETTER Z
0061..007A    ; Latin # L&  [26] LATIN SMALL LETTER A..LATIN SMALL LETTER Z
038E..03A1    ; Greek # L&  [20] GREEK CAPITAL LETTER UPSILON WITH TONOS..GREEK CAPITAL LETTER RHO
03A3..03E1    ; Greek # L&  [63] GREEK CAPITAL LETTER SIGMA..GREEK SMALL LETTER SAMPI
0400..0481    ; Cyrillic # L& [130] CYRILLIC CAPITAL LETTER IE WITH GRAVE..CYRILLIC SMALL LETTER KOPPA
"""


def parse_confusables(text: str) -> dict:
    """Map each source code point to its prototype string."""
    table = {}
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        src, tgt = (f.strip() for f in line.split(";")[:2])
        table[chr(int(src, 16))] = "".join(chr(int(h, 16)) for h in tgt.split())
    return table


def parse_ranges(text: str) -> list:
    """Parse lines "XXXX..YYYY ; value" into a list of (lo, hi, value)."""
    out = []
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        cps, value = (f.strip() for f in line.split(";"))
        lo, _, hi = cps.partition("..")
        out.append((int(lo, 16), int(hi or lo, 16), value))
    return out


PROTOTYPES = parse_confusables(CONFUSABLES_LINES)
_DICP = parse_ranges(DICP_LINES)
_SCRIPTS = parse_ranges(SCRIPTS_LINES)
_EXPLICIT = {"LRE", "RLE", "LRO", "RLO", "PDF", "LRI", "RLI", "FSI", "PDI"}


def is_default_ignorable(c: str) -> bool:
    cp = ord(c)
    return any(lo <= cp <= hi for lo, hi, _ in _DICP)


def internal_skeleton(x: str) -> str:
    """internalSkeleton(X) of UTS 39 section 4."""
    x = unicodedata.normalize("NFD", x)  # @line L1
    x = "".join(c for c in x if not is_default_ignorable(c))  # @line L2
    y = "".join(PROTOTYPES.get(c, c) for c in x)  # @line L3
    return unicodedata.normalize("NFD", y)  # @line L4


def skeleton(x: str) -> str:
    """skeleton(X) = bidiSkeleton(LTR, X), for text that stays at level 0."""
    for c in x:  # @line L5
        bc = unicodedata.bidirectional(c)
        if bc in ("R", "AL", "AN") or bc in _EXPLICIT:
            raise ValueError(f"U+{ord(c):04X} has bidi class {bc}; the full bidiSkeleton is needed")
        if bc == "BN" and not is_default_ignorable(c):
            raise ValueError(f"U+{ord(c):04X} is BN but not default ignorable")
    return internal_skeleton(x)  # @line L6


def confusable(x: str, y: str) -> bool:
    """X and Y are confusable when their skeletons are equal."""
    return skeleton(x) == skeleton(y)  # @line L7


def resolved_script_set(x: str):
    """The intersection of the script sets of the code points of x.

    Common and Inherited stand for the set of all scripts, written None here.
    Return None for ALL, or a frozenset of script names.
    """
    result = None
    for c in x:
        cp = ord(c)
        found = [v for lo, hi, v in _SCRIPTS if lo <= cp <= hi]
        if not found:
            raise ValueError(f"U+{cp:04X} is not in the script subset")
        if found[0] in ("Common", "Inherited"):
            continue
        s = frozenset([found[0]])
        result = s if result is None else result & s
    return result


def _meet(a, b):
    if a is None:
        return b
    if b is None:
        return a
    return a & b


def classify(x: str, y: str):
    """Return None, "single-script", "whole-script" or "mixed-script"."""
    if not confusable(x, y):  # @line L8
        return None
    rx, ry = resolved_script_set(x), resolved_script_set(y)  # @line L9
    both = _meet(rx, ry)
    if both is None or both:  # @line L10
        return "single-script"
    if (rx is None or rx) and (ry is None or ry):  # @line L11
        return "whole-script"
    return "mixed-script"  # @line L12
