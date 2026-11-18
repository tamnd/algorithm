# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unicode-case-folding/. The authors are listed in prov/GS7516.jsonl.

"""Unicode default case folding (core spec 16.0.0, section 3.13, R4) and caseless matching (D144, D145).

The table is a small part of CaseFolding-16.0.0.txt. The code does not call str.casefold,
str.lower or str.upper. It calls unicodedata.normalize only for NFD in D145.
"""

import unicodedata

# Lines copied verbatim from CaseFolding-16.0.0.txt (Date: 2024-04-30, 21:48:11 GMT),
# https://www.unicode.org/Public/16.0.0/ucd/CaseFolding.txt. Only the lines that the page
# and the tests use are here. The file is sorted by code point, and so is this list.
CASE_FOLDING_LINES = """\
0041; C; 0061; # LATIN CAPITAL LETTER A
0042; C; 0062; # LATIN CAPITAL LETTER B
0043; C; 0063; # LATIN CAPITAL LETTER C
0044; C; 0064; # LATIN CAPITAL LETTER D
0045; C; 0065; # LATIN CAPITAL LETTER E
0046; C; 0066; # LATIN CAPITAL LETTER F
0047; C; 0067; # LATIN CAPITAL LETTER G
0048; C; 0068; # LATIN CAPITAL LETTER H
0049; C; 0069; # LATIN CAPITAL LETTER I
0049; T; 0131; # LATIN CAPITAL LETTER I
004A; C; 006A; # LATIN CAPITAL LETTER J
004B; C; 006B; # LATIN CAPITAL LETTER K
004C; C; 006C; # LATIN CAPITAL LETTER L
004D; C; 006D; # LATIN CAPITAL LETTER M
004E; C; 006E; # LATIN CAPITAL LETTER N
004F; C; 006F; # LATIN CAPITAL LETTER O
0050; C; 0070; # LATIN CAPITAL LETTER P
0051; C; 0071; # LATIN CAPITAL LETTER Q
0052; C; 0072; # LATIN CAPITAL LETTER R
0053; C; 0073; # LATIN CAPITAL LETTER S
0054; C; 0074; # LATIN CAPITAL LETTER T
0055; C; 0075; # LATIN CAPITAL LETTER U
0056; C; 0076; # LATIN CAPITAL LETTER V
0057; C; 0077; # LATIN CAPITAL LETTER W
0058; C; 0078; # LATIN CAPITAL LETTER X
0059; C; 0079; # LATIN CAPITAL LETTER Y
005A; C; 007A; # LATIN CAPITAL LETTER Z
00B5; C; 03BC; # MICRO SIGN
00C5; C; 00E5; # LATIN CAPITAL LETTER A WITH RING ABOVE
00C9; C; 00E9; # LATIN CAPITAL LETTER E WITH ACUTE
00DF; F; 0073 0073; # LATIN SMALL LETTER SHARP S
0130; F; 0069 0307; # LATIN CAPITAL LETTER I WITH DOT ABOVE
0130; T; 0069; # LATIN CAPITAL LETTER I WITH DOT ABOVE
0149; F; 02BC 006E; # LATIN SMALL LETTER N PRECEDED BY APOSTROPHE
017F; C; 0073; # LATIN SMALL LETTER LONG S
01C4; C; 01C6; # LATIN CAPITAL LETTER DZ WITH CARON
01C5; C; 01C6; # LATIN CAPITAL LETTER D WITH SMALL LETTER Z WITH CARON
01C7; C; 01C9; # LATIN CAPITAL LETTER LJ
01C8; C; 01C9; # LATIN CAPITAL LETTER L WITH SMALL LETTER J
0345; C; 03B9; # COMBINING GREEK YPOGEGRAMMENI
0390; F; 03B9 0308 0301; # GREEK SMALL LETTER IOTA WITH DIALYTIKA AND TONOS
03A3; C; 03C3; # GREEK CAPITAL LETTER SIGMA
03C2; C; 03C3; # GREEK SMALL LETTER FINAL SIGMA
03F4; C; 03B8; # GREEK CAPITAL THETA SYMBOL
0587; F; 0565 0582; # ARMENIAN SMALL LIGATURE ECH YIWN
1E9B; C; 1E61; # LATIN SMALL LETTER LONG S WITH DOT ABOVE
1E9E; F; 0073 0073; # LATIN CAPITAL LETTER SHARP S
1E9E; S; 00DF; # LATIN CAPITAL LETTER SHARP S
1F80; F; 1F00 03B9; # GREEK SMALL LETTER ALPHA WITH PSILI AND YPOGEGRAMMENI
1F88; F; 1F00 03B9; # GREEK CAPITAL LETTER ALPHA WITH PSILI AND PROSGEGRAMMENI
1F88; S; 1F80; # GREEK CAPITAL LETTER ALPHA WITH PSILI AND PROSGEGRAMMENI
1FB3; F; 03B1 03B9; # GREEK SMALL LETTER ALPHA WITH YPOGEGRAMMENI
1FBC; F; 03B1 03B9; # GREEK CAPITAL LETTER ALPHA WITH PROSGEGRAMMENI
1FBC; S; 1FB3; # GREEK CAPITAL LETTER ALPHA WITH PROSGEGRAMMENI
2126; C; 03C9; # OHM SIGN
212A; C; 006B; # KELVIN SIGN
212B; C; 00E5; # ANGSTROM SIGN
FB03; F; 0066 0066 0069; # LATIN SMALL LIGATURE FFI
FB05; F; 0073 0074; # LATIN SMALL LIGATURE LONG S T
FB05; S; FB06; # LATIN SMALL LIGATURE LONG S T
FB06; F; 0073 0074; # LATIN SMALL LIGATURE ST
"""


def parse_case_folding(text: str) -> dict[str, dict[str, str]]:
    """Parse lines in the CaseFolding.txt format: code; status; mapping; # name.

    Return a dict from a one-code-point string to a dict from status (C, F, S or T)
    to the mapped string.
    """
    table: dict[str, dict[str, str]] = {}
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        fields = [f.strip() for f in line.split(";")]
        code, status, mapping = fields[0], fields[1], fields[2]
        if status not in ("C", "F", "S", "T"):
            raise ValueError(f"unknown status {status!r} in {raw!r}")
        src = chr(int(code, 16))
        dst = "".join(chr(int(h, 16)) for h in mapping.split())
        table.setdefault(src, {})[status] = dst
    return table


CASE_FOLDING = parse_case_folding(CASE_FOLDING_LINES)


def to_casefold(x: str, full: bool = True, turkic: bool = False,
                table: dict[str, dict[str, str]] = CASE_FOLDING) -> str:
    """Return toCasefold(x): each code point is replaced by its case folding.

    full=True uses the statuses C and F (full folding, as str.casefold);
    full=False uses C and S (simple folding, which keeps the length in code points).
    turkic=True puts the T lines first (the dotted and dotless I of Turkish and Azerbaijani).
    A code point with no line maps to itself.
    """
    out: list[str] = []  # @line L1
    for c in x:  # @line L2
        entry = table.get(c)
        if entry is None:
            out.append(c)
            continue
        if turkic and "T" in entry:  # @line L3
            out.append(entry["T"])
        elif full and "F" in entry:  # @line L4
            out.append(entry["F"])
        elif not full and "S" in entry:  # @line L5
            out.append(entry["S"])
        elif "C" in entry:  # @line L6
            out.append(entry["C"])
        else:  # @line L7
            out.append(c)
    return "".join(out)  # @line L8


def default_caseless_match(x: str, y: str, turkic: bool = False) -> bool:
    """D144: toCasefold(x) = toCasefold(y), with full folding."""
    return to_casefold(x, turkic=turkic) == to_casefold(y, turkic=turkic)


def canonical_caseless_key(x: str, turkic: bool = False) -> str:
    """Return NFD(toCasefold(NFD(x))), the key of D145."""
    nfd = unicodedata.normalize("NFD", x)
    return unicodedata.normalize("NFD", to_casefold(nfd, turkic=turkic))


def canonical_caseless_match(x: str, y: str, turkic: bool = False) -> bool:
    """D145: NFD(toCasefold(NFD(x))) = NFD(toCasefold(NFD(y)))."""
    return canonical_caseless_key(x, turkic) == canonical_caseless_key(y, turkic)  # @line L9
