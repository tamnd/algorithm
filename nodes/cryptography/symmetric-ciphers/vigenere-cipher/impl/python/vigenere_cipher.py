# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vigenere-cipher/. The authors are listed in prov/11VG96.jsonl.
"""The Vigenere cipher, its autokey variant, and the classical attack.

For study only. The cipher falls to the index of coincidence and to Kasiski
examination, and the code is not constant time. Do not use it to protect
real data; use AES-GCM or ChaCha20-Poly1305 from libsodium, a FIPS 140
validated module, or the standard library of your language.

Letters keep their case, and other characters are copied without using a key
letter. A key is a nonempty string of letters A to Z.
"""

from english import FREQ, chi_squared, index_of_coincidence, letters


def _shifts(key: str) -> list[int]:
    k = letters(key)
    if not k or len(k) != len(key):
        raise ValueError("the key must be a nonempty string of letters")
    return [ord(c) - 65 for c in k]


def _shift_letter(ch: str, s: int) -> str:
    base = 65 if ch.isupper() else 97
    return chr((ord(ch) - base + s) % 26 + base)


def _is_letter(ch: str) -> bool:
    return "A" <= ch <= "Z" or "a" <= ch <= "z"


def vigenere_encrypt(plaintext: str, key: str, sign: int = 1) -> str:
    """Shift the j-th letter of plaintext by the (j mod m)-th key letter."""
    k = _shifts(key)
    m = len(k)
    out = []
    j = 0
    for ch in plaintext:  # @line L1
        if _is_letter(ch):  # @line L2
            out.append(_shift_letter(ch, sign * k[j % m]))  # @line L3
            j += 1  # @line L4
        else:
            out.append(ch)
    return "".join(out)  # @line L5


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """Undo vigenere_encrypt: shift back by the same key letters."""
    return vigenere_encrypt(ciphertext, key, sign=-1)


def autokey_encrypt(plaintext: str, primer: str) -> str:
    """Vigenere's autokey: the key is the primer followed by the plaintext itself."""
    stream = _shifts(primer)
    out = []
    j = 0
    for ch in plaintext:
        if _is_letter(ch):
            out.append(_shift_letter(ch, stream[j]))
            stream.append(ord(ch.upper()) - 65)
            j += 1
        else:
            out.append(ch)
    return "".join(out)


def autokey_decrypt(ciphertext: str, primer: str) -> str:
    """Undo autokey_encrypt: each recovered letter extends the key."""
    stream = _shifts(primer)
    out = []
    j = 0
    for ch in ciphertext:
        if _is_letter(ch):
            p = _shift_letter(ch, -stream[j])
            out.append(p)
            stream.append(ord(p.upper()) - 65)
            j += 1
        else:
            out.append(ch)
    return "".join(out)


def columns(text: str, m: int) -> list[str]:
    """Split the letters of text into m columns: column i holds the letters at positions i, i + m, ..."""
    t = letters(text)
    return [t[i::m] for i in range(m)]


def mean_column_ic(text: str, m: int) -> float:
    """The mean index of coincidence of the m columns of text."""
    return sum(index_of_coincidence(col) for col in columns(text, m)) / m


def estimate_period(ciphertext: str, max_period: int = 20, ratio: float = 0.85) -> int:
    """The smallest period m whose columns look monoalphabetic.

    For English the IC of one alphabet is about 0.066 and that of uniform
    letters is 1/26, about 0.038. The true period and its multiples give
    the largest mean column IC; a wrong m mixes alphabets and gives less.
    So the smallest m whose mean IC is at least ratio times the largest one
    is taken. A heuristic: short texts make the column ICs noisy.
    """
    n = len(letters(ciphertext))
    top = max(1, min(max_period, n // 2))
    ics = [mean_column_ic(ciphertext, m) for m in range(1, top + 1)]
    best = max(ics)
    for m in range(1, top + 1):
        if ics[m - 1] >= ratio * best:
            return m
    return 1


def friedman_estimate(ciphertext: str) -> float:
    """Friedman's estimate of the period from the IC of the whole ciphertext.

    m = n (kp - kr) / ((n - 1) I - n kr + kp), with kp the English IC of the
    letter table and kr = 1/26. It is a rough estimate, not an integer.
    """
    n = len(letters(ciphertext))
    kp = sum(p * p for p in FREQ.values())
    kr = 1 / 26
    i = index_of_coincidence(ciphertext)
    return n * (kp - kr) / ((n - 1) * i - n * kr + kp)


def column_shift(column: str) -> int:
    """The Caesar shift that makes column look most like English (smallest chi-squared)."""
    return min(range(26), key=lambda s: chi_squared(vigenere_encrypt(column, chr(65 + s), sign=-1)))


def vigenere_break(ciphertext: str, max_period: int = 20) -> str:
    """Recover the key: the period from the IC, then each shift by chi-squared."""
    m = estimate_period(ciphertext, max_period)
    return "".join(chr(65 + column_shift(col)) for col in columns(ciphertext, m))
