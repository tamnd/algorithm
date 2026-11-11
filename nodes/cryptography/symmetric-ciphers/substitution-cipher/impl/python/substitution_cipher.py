# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/substitution-cipher/. The authors are listed in prov/QQJETY.jsonl.
"""The simple (monoalphabetic) substitution cipher and a hill-climbing attack.

For study only. The cipher falls to frequency analysis, and the code is not
constant time. Do not use it to protect real data; use AES-GCM or
ChaCha20-Poly1305 from libsodium, a FIPS 140 validated module, or the
standard library of your language.

A key is a string of the 26 letters in some order: the letter at index i is
the image of the i-th letter of the alphabet. Letters keep their case, and
other characters are copied. Cost of encryption: one table lookup per
character.
"""

import math
import random

from english import ALPHABET, FREQ, TRIGRAM_LOG, counts, letters


def check_key(key: str) -> None:
    """Raise ValueError unless key is a permutation of A to Z."""
    if sorted(key) != list(ALPHABET):
        raise ValueError("the key must hold each letter A to Z exactly once")


def invert_key(key: str) -> str:
    """The decryption key: the inverse permutation of key."""
    check_key(key)
    inv = [""] * 26
    for i, c in enumerate(key):
        inv[ord(c) - 65] = ALPHABET[i]
    return "".join(inv)


def substitution_encrypt(plaintext: str, key: str) -> str:
    """Replace each letter of plaintext by its image under key."""
    check_key(key)
    table = {}
    for i in range(26):  # @line L1
        table[ALPHABET[i]] = key[i]
        table[ALPHABET[i].lower()] = key[i].lower()
    out = []
    for ch in plaintext:  # @line L2
        out.append(table.get(ch, ch))  # @line L3
    return "".join(out)  # @line L4


def substitution_decrypt(ciphertext: str, key: str) -> str:
    """Apply the inverse permutation of key."""
    return substitution_encrypt(ciphertext, invert_key(key))


def random_key(rng: random.Random) -> str:
    """A uniformly random key, by a Fisher-Yates shuffle."""
    k = list(ALPHABET)
    rng.shuffle(k)
    return "".join(k)


def key_entropy_bits() -> float:
    """lg(26!), the entropy of a uniform key."""
    return math.lgamma(27) / math.log(2)


def unicity_distance(key_bits: float, redundancy: float) -> float:
    """Shannon's estimate U = H(K) / D of the ciphertext length needed for one key."""
    return key_bits / redundancy


def _score(trigrams: list[tuple[int, int, int, int]], dec: list[int]) -> float:
    return sum(n * TRIGRAM_LOG[dec[a]][dec[b]][dec[c]] for a, b, c, n in trigrams)


def hill_climb(
    ciphertext: str, rng: random.Random, restarts: int = 8, patience: int = 1000
) -> str:
    """Search for the decryption key that makes ciphertext look most like English.

    A heuristic: it returns a local maximum of the trigram score, which is not
    always the true key. Each restart starts from the key that matches the
    letter frequency ranks (with a few random swaps after the first restart),
    then swaps two letters of the key and keeps the swap when the score
    rises. A restart ends after `patience` swaps in a row that do not help.
    Returns the best decryption key found, as a string: the letter at index i
    is the plaintext letter of the i-th ciphertext letter.
    Cost: about restarts * (patience + improvements) score evaluations, each
    linear in the number of distinct trigrams of the ciphertext.
    """
    t = [ord(x) - 65 for x in letters(ciphertext)]
    tri: dict[tuple[int, int, int], int] = {}
    for a, b, c in zip(t, t[1:], t[2:]):
        tri[(a, b, c)] = tri.get((a, b, c), 0) + 1
    trigrams = [(a, b, c, n) for (a, b, c), n in tri.items()]
    cnt = counts(ciphertext)
    cipher_rank = sorted(range(26), key=lambda i: (-cnt[i], i))
    english_rank = sorted(range(26), key=lambda i: (-FREQ[ALPHABET[i]], i))
    best_key: list[int] = []
    best = -math.inf
    for r in range(restarts):
        dec = [0] * 26
        for c, p in zip(cipher_rank, english_rank):
            dec[c] = p
        if r > 0:
            for _ in range(8):
                i, j = rng.randrange(26), rng.randrange(26)
                dec[i], dec[j] = dec[j], dec[i]
        score = _score(trigrams, dec)
        stale = 0
        while stale < patience:
            i, j = rng.sample(range(26), 2)
            dec[i], dec[j] = dec[j], dec[i]
            s = _score(trigrams, dec)
            if s > score:
                score, stale = s, 0
            else:
                dec[i], dec[j] = dec[j], dec[i]
                stale += 1
        if score > best:
            best, best_key = score, dec[:]
    return "".join(ALPHABET[p] for p in best_key)
