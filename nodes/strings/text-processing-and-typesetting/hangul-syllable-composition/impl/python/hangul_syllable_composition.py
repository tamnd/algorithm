# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hangul-syllable-composition/. The authors are listed in prov/QKVWX9.jsonl.

"""Hangul syllable decomposition, composition and names, as in The Unicode Standard 16.0.0,
section 3.12 (Conjoining Jamo Behavior), with the constants of its "Common Constants".

The code does not call unicodedata. The tests compare it with unicodedata.normalize and
unicodedata.name.
"""

SBASE, LBASE, VBASE, TBASE = 0xAC00, 0x1100, 0x1161, 0x11A7
LCOUNT, VCOUNT, TCOUNT = 19, 21, 28
NCOUNT = VCOUNT * TCOUNT  # 588
SCOUNT = LCOUNT * NCOUNT  # 11172

# The data fields of Jamo-16.0.0.txt, https://www.unicode.org/Public/16.0.0/ucd/Jamo.txt
# (property Jamo_Short_Name), with the character names as comments. The file has these 67
# lines: 19 leading consonants, 21 vowels and 27 trailing consonants. U+110B has an empty
# short name.
JAMO_LINES = """\
1100; G # HANGUL CHOSEONG KIYEOK
1101; GG # HANGUL CHOSEONG SSANGKIYEOK
1102; N # HANGUL CHOSEONG NIEUN
1103; D # HANGUL CHOSEONG TIKEUT
1104; DD # HANGUL CHOSEONG SSANGTIKEUT
1105; R # HANGUL CHOSEONG RIEUL
1106; M # HANGUL CHOSEONG MIEUM
1107; B # HANGUL CHOSEONG PIEUP
1108; BB # HANGUL CHOSEONG SSANGPIEUP
1109; S # HANGUL CHOSEONG SIOS
110A; SS # HANGUL CHOSEONG SSANGSIOS
110B; # HANGUL CHOSEONG IEUNG
110C; J # HANGUL CHOSEONG CIEUC
110D; JJ # HANGUL CHOSEONG SSANGCIEUC
110E; C # HANGUL CHOSEONG CHIEUCH
110F; K # HANGUL CHOSEONG KHIEUKH
1110; T # HANGUL CHOSEONG THIEUTH
1111; P # HANGUL CHOSEONG PHIEUPH
1112; H # HANGUL CHOSEONG HIEUH
1161; A # HANGUL JUNGSEONG A
1162; AE # HANGUL JUNGSEONG AE
1163; YA # HANGUL JUNGSEONG YA
1164; YAE # HANGUL JUNGSEONG YAE
1165; EO # HANGUL JUNGSEONG EO
1166; E # HANGUL JUNGSEONG E
1167; YEO # HANGUL JUNGSEONG YEO
1168; YE # HANGUL JUNGSEONG YE
1169; O # HANGUL JUNGSEONG O
116A; WA # HANGUL JUNGSEONG WA
116B; WAE # HANGUL JUNGSEONG WAE
116C; OE # HANGUL JUNGSEONG OE
116D; YO # HANGUL JUNGSEONG YO
116E; U # HANGUL JUNGSEONG U
116F; WEO # HANGUL JUNGSEONG WEO
1170; WE # HANGUL JUNGSEONG WE
1171; WI # HANGUL JUNGSEONG WI
1172; YU # HANGUL JUNGSEONG YU
1173; EU # HANGUL JUNGSEONG EU
1174; YI # HANGUL JUNGSEONG YI
1175; I # HANGUL JUNGSEONG I
11A8; G # HANGUL JONGSEONG KIYEOK
11A9; GG # HANGUL JONGSEONG SSANGKIYEOK
11AA; GS # HANGUL JONGSEONG KIYEOK-SIOS
11AB; N # HANGUL JONGSEONG NIEUN
11AC; NJ # HANGUL JONGSEONG NIEUN-CIEUC
11AD; NH # HANGUL JONGSEONG NIEUN-HIEUH
11AE; D # HANGUL JONGSEONG TIKEUT
11AF; L # HANGUL JONGSEONG RIEUL
11B0; LG # HANGUL JONGSEONG RIEUL-KIYEOK
11B1; LM # HANGUL JONGSEONG RIEUL-MIEUM
11B2; LB # HANGUL JONGSEONG RIEUL-PIEUP
11B3; LS # HANGUL JONGSEONG RIEUL-SIOS
11B4; LT # HANGUL JONGSEONG RIEUL-THIEUTH
11B5; LP # HANGUL JONGSEONG RIEUL-PHIEUPH
11B6; LH # HANGUL JONGSEONG RIEUL-HIEUH
11B7; M # HANGUL JONGSEONG MIEUM
11B8; B # HANGUL JONGSEONG PIEUP
11B9; BS # HANGUL JONGSEONG PIEUP-SIOS
11BA; S # HANGUL JONGSEONG SIOS
11BB; SS # HANGUL JONGSEONG SSANGSIOS
11BC; NG # HANGUL JONGSEONG IEUNG
11BD; J # HANGUL JONGSEONG CIEUC
11BE; C # HANGUL JONGSEONG CHIEUCH
11BF; K # HANGUL JONGSEONG KHIEUKH
11C0; T # HANGUL JONGSEONG THIEUTH
11C1; P # HANGUL JONGSEONG PHIEUPH
11C2; H # HANGUL JONGSEONG HIEUH
"""


def parse_jamo(text: str) -> dict[int, str]:
    out = {}
    for line in text.splitlines():
        fields = line.split("#", 1)[0].split(";")
        out[int(fields[0], 16)] = fields[1].strip()
    return out


JAMO_SHORT_NAME = parse_jamo(JAMO_LINES)


def is_syllable(c: int) -> bool:
    return SBASE <= c < SBASE + SCOUNT


def is_l(c: int) -> bool:
    return LBASE <= c < LBASE + LCOUNT


def is_v(c: int) -> bool:
    return VBASE <= c < VBASE + VCOUNT


def is_t(c: int) -> bool:
    return TBASE < c < TBASE + TCOUNT  # TBASE itself is not a trailing consonant


def decompose_syllable(s: int) -> tuple[int, ...]:
    """Full canonical decomposition of a precomposed syllable: (L, V) or (L, V, T)."""
    if not is_syllable(s):
        raise ValueError(f"U+{s:04X} is not a precomposed Hangul syllable")
    sindex = s - SBASE  # @line L1
    lindex = sindex // NCOUNT  # @line L2
    vindex = (sindex % NCOUNT) // TCOUNT  # @line L3
    tindex = sindex % TCOUNT  # @line L4
    if tindex == 0:  # @line L5
        return (LBASE + lindex, VBASE + vindex)
    return (LBASE + lindex, VBASE + vindex, TBASE + tindex)  # @line L6


def decomposition_mapping(s: int) -> tuple[int, int]:
    """The two-part canonical decomposition mapping: LV to (L, V), LVT to (LV, T)."""
    sindex = s - SBASE
    tindex = sindex % TCOUNT
    if tindex == 0:
        return (LBASE + sindex // NCOUNT, VBASE + (sindex % NCOUNT) // TCOUNT)
    return (s - tindex, TBASE + tindex)


def decompose(text: list[int]) -> list[int]:
    """Replace every precomposed syllable of text by its jamo; keep the rest."""
    out: list[int] = []
    for c in text:
        out.extend(decompose_syllable(c) if is_syllable(c) else (c,))
    return out


def compose(text: list[int]) -> list[int]:
    """Compose L V into LV and LV T into LVT, from left to right."""
    out: list[int] = []  # @line L7
    for c in text:  # @line L8
        last = out[-1] if out else -1
        if is_l(last) and is_v(c):  # @line L9
            out[-1] = SBASE + ((last - LBASE) * VCOUNT + (c - VBASE)) * TCOUNT  # @line L10
        elif is_syllable(last) and (last - SBASE) % TCOUNT == 0 and is_t(c):  # @line L11
            out[-1] = last + (c - TBASE)  # @line L12
        else:
            out.append(c)  # @line L13
    return out  # @line L14


def syllable_name(s: int) -> str:
    """The character name of a precomposed syllable, from the Jamo short names."""
    parts = decompose_syllable(s)  # @line L15
    return "HANGUL SYLLABLE " + "".join(JAMO_SHORT_NAME[j] for j in parts)  # @line L16
