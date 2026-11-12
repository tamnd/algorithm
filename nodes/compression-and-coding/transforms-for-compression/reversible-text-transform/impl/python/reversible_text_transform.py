# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reversible-text-transform/. The authors are listed in prov/3C2Q9R.jsonl.

"""Two reversible text transforms that run before a general compressor, and
their composition.

Capital conversion: each maximal run of ASCII letters that is Capitalized
becomes CAP + the run in lower case, and each run of two or more letters in
upper case becomes UPPER + the run in lower case. Runs in mixed case stay as
they are. A literal CAP, UPPER or ESC character in the input is written as
ESC + the character, so the output can always be decoded.

Dictionary transform: each maximal run of ASCII letters that is a word of a
fixed dictionary (at most 255 words) becomes WORD + one character that holds
its index. A literal WORD or DESC character is written as DESC + the character.

encode(x) = dict_encode(cap_encode(x)) and decode(y) = cap_decode(dict_decode(y)).
Each step takes time linear in the length of the text (with a hash map for
the dictionary).
"""

import re
from collections.abc import Sequence

CAP, UPPER, ESC = "\x01", "\x02", "\x03"
WORD, DESC = "\x04", "\x05"

_PIECE = re.compile(r"[A-Za-z]+|.", re.S)


def _is_upper(p: str) -> bool:
    return all("A" <= c <= "Z" for c in p)


def _is_lower(p: str) -> bool:
    return all("a" <= c <= "z" for c in p)


def cap_encode(x: str) -> str:
    out: list[str] = []  # @line L1
    for m in _PIECE.finditer(x):  # @line L2
        p = m.group()
        if p in (CAP, UPPER, ESC):  # @line L3
            out.append(ESC + p)
        elif len(p) >= 2 and _is_upper(p):  # @line L4
            out.append(UPPER + p.lower())
        elif "A" <= p[0] <= "Z" and _is_lower(p[1:]):  # @line L5
            out.append(CAP + p.lower())
        else:
            out.append(p)  # @line L6
    return "".join(out)  # @line L7


def cap_decode(y: str) -> str:
    out: list[str] = []
    pieces = [m.group() for m in _PIECE.finditer(y)]
    i = 0
    while i < len(pieces):
        p = pieces[i]
        if p == ESC:
            if i + 1 >= len(pieces) or pieces[i + 1] not in (CAP, UPPER, ESC):
                raise ValueError("ESC must be followed by a flag character")
            out.append(pieces[i + 1])
            i += 2
        elif p in (CAP, UPPER):
            if i + 1 >= len(pieces) or not _is_lower(pieces[i + 1]):
                raise ValueError("a flag must be followed by a lower-case word")
            w = pieces[i + 1]
            out.append(w.upper() if p == UPPER else w[0].upper() + w[1:])
            i += 2
        else:
            out.append(p)
            i += 1
    return "".join(out)


def dict_encode(x: str, words: Sequence[str]) -> str:
    if len(words) > 255 or len(set(words)) != len(words):
        raise ValueError("at most 255 distinct words")
    if not all(w and w.isascii() and w.isalpha() for w in words):
        raise ValueError("dictionary words must be ASCII letters")
    index = {w: i for i, w in enumerate(words)}
    out: list[str] = []
    for m in _PIECE.finditer(x):
        p = m.group()
        if p in (WORD, DESC):
            out.append(DESC + p)
        elif p in index:
            out.append(WORD + chr(index[p]))
        else:
            out.append(p)
    return "".join(out)


def dict_decode(y: str, words: Sequence[str]) -> str:
    out: list[str] = []
    i = 0
    while i < len(y):
        c = y[i]
        if c == DESC:
            out.append(y[i + 1])
            i += 2
        elif c == WORD:
            out.append(words[ord(y[i + 1])])
            i += 2
        else:
            out.append(c)
            i += 1
    return "".join(out)


def encode(x: str, words: Sequence[str]) -> str:
    return dict_encode(cap_encode(x), words)


def decode(y: str, words: Sequence[str]) -> str:
    return cap_decode(dict_decode(y, words))
