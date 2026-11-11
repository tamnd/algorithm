# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/playfair-cipher/. The authors are listed in prov/3G0PKX.jsonl.
"""The Playfair cipher: digraph substitution with a 5 x 5 key square.

For study only. The cipher falls to digraph frequency analysis and to known
plaintext, and the code is not constant time. Do not use it to protect real
data; use AES-GCM or ChaCha20-Poly1305 from libsodium, a FIPS 140 validated
module, or the standard library of your language.

Conventions: I and J share a cell (J is written as I). The plaintext is
split into pairs; a pair of two equal letters gets the filler X after its
first letter (Q when the letter is X), and an odd last letter gets the
filler X (Q after an X).
"""

ALPHABET25 = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # no J


def letters(text: str) -> str:
    """Keep the letters of text, in upper case, with J written as I."""
    return "".join("I" if c == "J" else c for c in text.upper() if "A" <= c <= "Z")


def key_square(keyword: str) -> str:
    """The 25 letters of the square, row by row: the keyword without repeats, then the rest."""
    seen: list[str] = []
    for c in letters(keyword) + ALPHABET25:
        if c not in seen:
            seen.append(c)
    return "".join(seen)


def prepare(plaintext: str) -> list[str]:
    """Split the letters of plaintext into digraphs of two different letters."""
    t = letters(plaintext)
    out = []
    i = 0
    while i < len(t):
        a = t[i]
        b = t[i + 1] if i + 1 < len(t) else None
        if b is None or a == b:
            out.append(a + ("Q" if a == "X" else "X"))
            i += 1
        else:
            out.append(a + b)
            i += 2
    return out


def _digraph(square: str, a: str, b: str, step: int) -> str:
    """Apply the three rules to the digraph ab; step 1 encrypts, step -1 decrypts."""
    ra, ca = divmod(square.index(a), 5)  # @line L3
    rb, cb = divmod(square.index(b), 5)
    # Same row: the letter to the right. Same column: the letter below.
    # Rectangle: the other corner in the same row.
    if ra == rb:  # @line L4
        return square[5 * ra + (ca + step) % 5] + square[5 * rb + (cb + step) % 5]
    if ca == cb:  # @line L5
        return square[5 * ((ra + step) % 5) + ca] + square[5 * ((rb + step) % 5) + cb]
    return square[5 * ra + cb] + square[5 * rb + ca]  # @line L6


def playfair_encrypt(plaintext: str, keyword: str) -> str:
    """Encrypt the letters of plaintext with the square of keyword."""
    square = key_square(keyword)
    digraphs = prepare(plaintext)  # @line L1
    out = []
    for d in digraphs:  # @line L2
        out.append(_digraph(square, d[0], d[1], 1))
    return "".join(out)  # @line L7


def playfair_decrypt(ciphertext: str, keyword: str) -> str:
    """Undo playfair_encrypt: the same rules with left and up. The fillers stay in the output."""
    square = key_square(keyword)
    t = letters(ciphertext)
    if len(t) % 2:
        raise ValueError("a Playfair ciphertext has an even number of letters")
    return "".join(_digraph(square, t[i], t[i + 1], -1) for i in range(0, len(t), 2))


def known_digraphs(plaintext: str, ciphertext: str) -> dict[str, str]:
    """The part of the digraph table that a known plaintext reveals.

    Each known pair ab -> cd also gives ba -> dc (the reversal property),
    and the decryption entries cd -> ab and dc -> ba. Returns a map from
    cipher digraphs to plain digraphs.
    """
    pairs = prepare(plaintext)
    c = letters(ciphertext)
    out = {}
    for i, p in enumerate(pairs):
        d = c[2 * i : 2 * i + 2]
        out[d] = p
        out[d[::-1]] = p[::-1]
    return out


def digraph_table(keyword: str) -> dict[str, str]:
    """The full substitution on the 600 digraphs of two different letters."""
    square = key_square(keyword)
    return {a + b: _digraph(square, a, b, 1) for a in ALPHABET25 for b in ALPHABET25 if a != b}
