# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unicode-line-breaking-algorithm/. The authors are listed in prov/D4NEZV.jsonl.
# East Asian width and the general category come from unicodedata (unidata_version 16.0.0
# with Python 3.14). The tests use only characters that are assigned in Unicode 3.2, with
# two exceptions: the emoji code points of the LB30a and LB30b tests, and the unassigned
# U+1F02C of a LineBreakTest line. Their classes come from the table in the implementation.
import random
import re
import unicodedata

from unicode_line_breaking_algorithm import (break_positions, line_break_class, line_breaks,
                                             resolve, segments)

# Lines copied from LineBreakTest-16.0.0.txt (Date: 2024-07-05), without the comments.
CONFORMANCE = [
    "× 0076 × 006F × 0075 × 0073 × 0020 ÷ 006D × 0065 × 0020 ÷ 0068 × 0065 × 0075 × 0072 × 0074 × 0065 × 007A × 002C × 0020 ÷ 0076 × 006F × 0075 × 0073 × 0020 ÷ 0064 × 0069 × 0074 × 0065 × 0073 × 0020 × 003A × 0020 ÷ 00AB × 0020 × 0045 × 0078 × 0063 × 0075 × 0073 × 0065 × 007A × 002D ÷ 006D × 006F × 0069 × 002C × 0020 × 00BB × 0020 ÷ 0065 × 0074 × 0020 ÷ 0076 × 006F × 0075 × 0073 × 0020 ÷ 0063 × 0072 × 006F × 0079 × 0065 × 007A × 0020 ÷ 0071 × 0075 × 0065 × 0020 ÷ 0063 × 0065 × 006C × 0061 × 0020 ÷ 0073 × 0075 × 0066 × 0066 × 0069 × 0074 × 0020 × 003F ÷",
    "× 006A × 2019 × 0061 × 0069 × 0020 ÷ 0064 × 0069 × 0074 × 0020 × 003A × 0020 ÷ 00AB × 0020 × 0045 × 0078 × 0063 × 0075 × 0073 × 0065 × 007A × 002D ÷ 006D × 006F × 0069 × 002E × 0020 × 00BB × 0020 ÷ 0049 × 006C × 0020 ÷ 006D × 0065 × 0020 ÷ 0073 × 0065 × 006D × 0062 × 006C × 0065 × 0020 ÷ 0064 × 006F × 006E × 0063 × 0020 ÷ 0071 × 0075 × 0065 × 0020 ÷ 0063 × 2019 × 0065 × 0073 × 0074 × 0020 ÷ 0061 × 0073 × 0073 × 0065 × 007A × 002E ÷",
    "× 0050 × 0061 × 0073 × 0020 ÷ 0075 × 006E × 0065 × 0020 ÷ 0063 × 0069 × 0074 × 0061 × 0074 × 0069 × 006F × 006E × 0020 ÷ 00BB × 005A × 0069 × 0074 × 0061 × 0074 × 00AB × 0020 ÷ 0050 × 0061 × 0073 × 0020 ÷ 0075 × 006E × 0065 × 0020 ÷ 0063 × 0069 × 0074 × 0061 × 0074 × 0069 × 006F × 006E × 0020 ÷ 006E × 006F × 006E × 0020 ÷ 0070 × 006C × 0075 × 0073 ÷",
    "× 00AB × 0020 × 0043 × 0069 × 0074 × 0061 × 0074 × 0069 × 006F × 006E × 0020 × 00BB × 200B ÷ 004B × 0065 × 0069 × 006E × 0020 ÷ 005A × 0069 × 0074 × 0061 × 0074 × 200B ÷ 00AB × 0020 × 0041 × 0075 × 0074 × 0072 × 0065 × 0020 ÷ 0063 × 0069 × 0074 × 0061 × 0074 × 0069 × 006F × 006E × 0020 × 00BB ÷",
    "× 0073 × 0074 × 0061 × 0072 × 0074 × 0020 ÷ 002E × 0037 × 0038 × 0039 × 0020 ÷ 0065 × 006E × 0064 ÷",
    "× 0074 × 0068 × 0065 × 0020 ÷ 0033 × 006D × 0073 × 0020 ÷ 0070 × 006F × 0073 × 0073 × 0065 × 0073 × 0073 × 0069 × 0076 × 0065 × 0020 ÷ 0070 × 0072 × 006F × 006E × 006F × 006D × 0069 × 006E × 0061 × 006C × 0020 ÷ 0073 × 0075 × 0066 × 0066 × 0069 × 0078 × 0020 ÷ 0028 × 0020 × 002D × 0161 × 0075 × 0020 × 0029 ÷",
    "× 004D × 0061 × 0063 × 0020 ÷ 0050 × 0072 × 006F × 0020 ÷ 002D × 0074 × 0069 × 0065 × 0074 × 006F × 006B × 006F × 006E × 0065 ÷",
    "× 6BD5 ÷ 58EB ÷ 608C ÷ FF08 × 0031 × 0039 × 0030 × 0031 ÷ 5E74 ÷ 2014 ÷ 0031 × 0039 × 0033 × 0036 ÷ 5E74 × FF09 × FF0C ÷ 671D ÷ 9C9C ÷ 7C4D ÷ 7EA2 ÷ 519B ÷ 5C06 ÷ 9886 ÷",
    "× 1F02C × 1F3FF ÷",
]


def parse_test_line(line):
    tokens = line.split()
    assert tokens[0] == "×"
    text, breaks = [], []
    for k in range(1, len(tokens), 2):
        text.append(chr(int(tokens[k], 16)))
        if tokens[k + 1] == "÷":
            breaks.append(len(text))
    return "".join(text), breaks


def test_conformance_lines():
    for line in CONFORMANCE:
        s, expected = parse_test_line(line)
        assert break_positions(s) == expected, line


def test_class_table_and_lb1():
    assert line_break_class("a") == "AL" and line_break_class(",") == "IS"
    assert line_break_class("Ω") == "XX" and resolve("Ω") == "AL"
    assert line_break_class("ก") == "SA" and resolve("ก") == "AL"
    assert line_break_class("́") == "CM" and line_break_class("א") == "HL"


def test_mandatory_breaks_and_crlf():
    assert line_breaks("a\r\nb") == [(3, True), (4, True)]
    assert line_breaks("a\rb\nc") == [(2, True), (4, True), (5, True)]
    assert line_breaks("ab") == [(2, True)]
    assert line_breaks("") == []


def test_small_rules():
    assert segments("one two") == ["one ", "two"]  # LB7 and LB18
    assert segments("a  b") == ["a  ", "b"]  # LB7: no break before a space
    assert segments("ab​cd") == ["ab​", "cd"]  # LB8
    assert segments("a b") == ["a b"]  # LB12
    assert segments("a⁠b") == ["a⁠b"]  # LB11
    assert segments("( a)") == ["( a)"]  # LB14 and LB13
    assert segments("well-known") == ["well-", "known"]  # LB21 then a break after HY
    assert segments("-5") == ["-5"]  # LB25 HY x NU
    assert segments("$(12.50)%") == ["$(12.50)%"]  # LB25
    assert segments("一丁") == ["一", "丁"]  # LB31 between ideographs
    assert segments("一、丁") == ["一、", "丁"]  # LB13 before CL
    assert segments("áb") == ["áb"]  # LB9
    assert segments(" ́a") == [" ", "́a"]  # LB10 then LB18
    assert segments("\U0001F1E6\U0001F1E6\U0001F1E6") == ["\U0001F1E6\U0001F1E6", "\U0001F1E6"]  # LB30a
    assert segments("\U0001F466\U0001F3FB") == ["\U0001F466\U0001F3FB"]  # LB30b
    assert segments("א־a") == ["א־a"]  # LB21a
    assert segments("א־ב") == ["א־", "ב"]  # LB21a does not hold before HL


# A second implementation: each rule is data, a regular expression for the left side and
# one for the right side, tried in order on a token string.
FLAGS = "ifedhn"


def _flags(ch):
    cat = unicodedata.category(ch)
    return "".join([
        "i" if cat == "Pi" else "-",
        "f" if cat == "Pf" else "-",
        "e" if unicodedata.east_asian_width(ch) in ("F", "W", "H") else "-",
        "d" if ch == "◌" else "-",
        "h" if ch == "‐" else "-",
        # [\p{ExtPict}&\p{Cn}]: emoji-data.txt 16.0.0 has 1F005..1F0CE ; Extended_Pictographic.
        "n" if 0x1F005 <= ord(ch) <= 0x1F0CE and cat == "Cn" else "-",
    ])


def T(*classes, **flag):
    pat = "".join(flag.get(f, ".") for f in FLAGS)
    name = "(?:%s)" % "|".join(classes) if classes else "[A-Z0-9]+"
    return "<%s\\.%s>" % (name, pat)


def NOT(*classes):
    return "<(?!(?:%s)\\.)[A-Z0-9]+\\.[^>]*>" % "|".join(classes)


def ANYOF(*pats):
    return "(?:%s)" % "|".join(pats)


ANY = T()
HARD = ("BK", "CR", "LF", "NL")
SPS = "(?:%s)*" % T("SP")
NUM = T("NU") + "(?:%s)*" % T("SY", "IS")
AKD = ANYOF(T("AK", "AS"), T(d="d"))
X, B, M = "x", "b", "m"

RAW_RULES = [
    (T("BK"), ANY, M), (T("CR"), T("LF"), X), (T("CR"), ANY, M), (T("LF", "NL"), ANY, M),
    (ANY, T(*HARD), X), (ANY, T("SP", "ZW"), X), (T("ZW") + SPS, ANY, B), (T("ZWJ"), ANY, X),
    (NOT(*HARD, "SP", "ZW") + "(?:%s)*" % T("CM", "ZWJ"), T("CM", "ZWJ"), X),
]
RULES = [
    (ANY, T("WJ"), X), (T("WJ"), ANY, X), (T("GL"), ANY, X), (NOT("SP", "BA", "HY"), T("GL"), X),
    (ANY, T("CL", "CP", "EX", "SY"), X), (T("OP") + SPS, ANY, X),
    (ANYOF("^", T(*HARD, "OP", "QU", "GL", "SP", "ZW")) + T("QU", i="i") + SPS, ANY, X),
    (ANY, T("QU", f="f") + ANYOF(T("SP", "GL", "WJ", "CL", "QU", "CP", "EX", "IS", "SY", *HARD, "ZW"), "$"), X),
    (T("SP"), T("IS") + T("NU"), B), (ANY, T("IS"), X), (T("CL", "CP") + SPS, T("NS"), X),
    (T("B2") + SPS, T("B2"), X), (T("SP"), ANY, B),
    (ANY, T("QU", i="-"), X), (T("QU", f="-"), ANY, X),
    (T(e="-"), T("QU"), X), (ANY, T("QU") + ANYOF(T(e="-"), "$"), X), (T("QU"), T(e="-"), X),
    (ANYOF("^", T(e="-")) + T("QU"), ANY, X),
    (ANY, T("CB"), B), (T("CB"), ANY, B),
    (ANYOF("^", T(*HARD, "SP", "ZW", "CB", "GL")) + ANYOF(T("HY"), T(h="h")), T("AL"), X),
    (ANY, T("BA", "HY", "NS"), X), (T("BB"), ANY, X),
    (T("HL") + ANYOF(T("HY"), T("BA", e="-")), NOT("HL"), X), (T("SY"), T("HL"), X),
    (ANY, T("IN"), X),
    (T("AL", "HL"), T("NU"), X), (T("NU"), T("AL", "HL"), X),
    (T("PR"), T("ID", "EB", "EM"), X), (T("ID", "EB", "EM"), T("PO"), X),
    (T("PR", "PO"), T("AL", "HL"), X), (T("AL", "HL"), T("PR", "PO"), X),
    (NUM + T("CL", "CP"), T("PO", "PR"), X), (NUM, T("PO", "PR"), X),
    (T("PO", "PR"), T("OP") + T("NU"), X), (T("PO", "PR"), T("OP") + T("IS") + T("NU"), X),
    (T("PO", "PR", "HY", "IS"), T("NU"), X), (NUM, T("NU"), X),
    (T("JL"), T("JL", "JV", "H2", "H3"), X), (T("JV", "H2"), T("JV", "JT"), X), (T("JT", "H3"), T("JT"), X),
    (T("JL", "JV", "JT", "H2", "H3"), T("PO"), X), (T("PR"), T("JL", "JV", "JT", "H2", "H3"), X),
    (T("AL", "HL"), T("AL", "HL"), X),
    (T("AP"), AKD, X), (AKD, T("VF", "VI"), X), (AKD + T("VI"), ANYOF(T("AK"), T(d="d")), X),
    (AKD, AKD + T("VF"), X),
    (T("IS"), T("AL", "HL"), X),
    (T("AL", "HL", "NU"), T("OP", e="-"), X), (T("CP", e="-"), T("AL", "HL", "NU"), X),
    (ANYOF("^", NOT("RI")) + "(?:%s%s)*" % (T("RI"), T("RI")) + T("RI"), T("RI"), X),
    (T("EB"), T("EM"), X), (T(n="n"), T("EM"), X),
]


def _apply(rules, left, right):
    for lpat, rpat, action in rules:
        if re.search("(?:%s)$" % lpat, left) and re.match(rpat, right):
            return action
    return None


def reference_breaks(s, lb=line_break_class):
    raw = [resolve(ch, lb) for ch in s]
    tok = ["<%s.%s>" % (c, _flags(ch)) for c, ch in zip(raw, s)]
    # LB9 and LB10, written from the rule text: a CM or ZWJ joins the previous code point
    # unless that one is BK, CR, LF, NL, SP or ZW.
    unit_tok, start = [], []
    for i, c in enumerate(raw):
        if c in ("CM", "ZWJ") and i > 0 and raw[i - 1] not in HARD + ("SP", "ZW"):
            continue
        unit_tok.append(tok[i] if c not in ("CM", "ZWJ") else "<AL.%s>" % _flags(s[i]))
        start.append(i)
    out = []
    for p in range(1, len(s)):
        act = _apply(RAW_RULES, "".join(tok[:p]), "".join(tok[p:]))
        if act is None:
            k = start.index(p)
            act = _apply(RULES, "".join(unit_tok[:k]), "".join(unit_tok[k:])) or B
        if act != X:
            out.append((p, act == M))
    return out + [(len(s), True)] if s else []


MADE_UP = {"B": "BB", "C": "CB", "I": "IN", "N": "NS", "K": "BK", "L": "NL", "J": "JL",
           "V": "JV", "T": "JT", "k": "AK", "p": "AP", "s": "AS", "f": "VF", "v": "VI",
           "E": "EB", "M": "EM", "R": "RI", "S": "SY", "H": "HL"}


def made_up_classes(c):
    return MADE_UP.get(c) or line_break_class(c)


def test_against_rule_table_reference():
    rng = random.Random(1414)
    real = ("a1 ()}!?,./-$%+\"'«»‘’“” ­́​‍"
            "⁠‐" + chr(0x2014) + "א־一、　（）가각◌"
            "\n\r\tกΑ")
    alphabet = real + "".join(MADE_UP)
    for _ in range(700):
        s = "".join(rng.choice(alphabet) for _ in range(rng.randint(1, 9)))
        assert line_breaks(s, made_up_classes) == reference_breaks(s, made_up_classes), repr(s)


def test_reference_agrees_on_conformance_lines():
    for line in CONFORMANCE:
        s, expected = parse_test_line(line)
        assert [p for p, _ in reference_breaks(s)] == expected
