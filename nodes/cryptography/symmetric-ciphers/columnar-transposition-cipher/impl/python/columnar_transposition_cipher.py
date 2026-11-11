# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/columnar-transposition-cipher/. The authors are listed in prov/G69PV9.jsonl.
"""Columnar transposition, double transposition, and two classical attacks.

For study only. Transposition keeps the letters, so the ciphertext has the
letter counts of the plaintext, and the code is not constant time. Do not
use it to protect real data; use AES-GCM or ChaCha20-Poly1305 from
libsodium, a FIPS 140 validated module, or the standard library of your
language.

Only the letters of the message are used, in upper case. The grid is not
padded: the last row may be short (an irregular columnar transposition).
"""

import itertools
import math

from english import ALPHABET, FREQ, TRAIN, letters, ngram_score


def key_order(key: str) -> list[int]:
    """The column order of a keyword: columns are read in the alphabetical order
    of their key letters, with equal letters from left to right."""
    return sorted(range(len(key)), key=lambda i: (key[i], i))


def _column_lengths(n: int, k: int) -> list[int]:
    return [n // k + (1 if c < n % k else 0) for c in range(k)]


def encrypt_order(plaintext: str, order: list[int]) -> str:
    """Write the letters in rows of k = len(order) and read whole columns in the given order."""
    t = letters(plaintext)
    k = len(order)
    out = []
    for c in order:  # @line L2
        out.append(t[c::k])  # @line L3
    return "".join(out)  # @line L4


def decrypt_order(ciphertext: str, order: list[int]) -> str:
    """Cut the ciphertext into columns of the right lengths and read the rows."""
    t = letters(ciphertext)
    k = len(order)
    lengths = _column_lengths(len(t), k)
    cols = [""] * k
    pos = 0
    for c in order:
        cols[c] = t[pos : pos + lengths[c]]
        pos += lengths[c]
    return "".join(cols[i % k][i // k] for i in range(len(t)))


def columnar_encrypt(plaintext: str, key: str) -> str:
    """Columnar transposition with a keyword."""
    order = key_order(key)  # @line L1
    return encrypt_order(plaintext, order)


def columnar_decrypt(ciphertext: str, key: str) -> str:
    return decrypt_order(ciphertext, key_order(key))


def double_encrypt(plaintext: str, key1: str, key2: str) -> str:
    """Double transposition: two columnar transpositions in a row."""
    return columnar_encrypt(columnar_encrypt(plaintext, key1), key2)


def double_decrypt(ciphertext: str, key1: str, key2: str) -> str:
    return columnar_decrypt(columnar_decrypt(ciphertext, key2), key1)


def break_columnar(ciphertext: str, k: int) -> list[int]:
    """Try all k! column orders and keep the one whose decryption scores best.

    A brute force search with the trigram score; practical for k up to about 7.
    """
    best, best_order = -math.inf, list(range(k))
    for perm in itertools.permutations(range(k)):
        s = ngram_score(decrypt_order(ciphertext, list(perm)))
        if s > best:
            best, best_order = s, list(perm)
    return best_order


def _bigram_log() -> list[list[float]]:
    """log P(b | a) from TRAIN, smoothed toward FREQ with a weight of 3."""
    t = [ord(x) - 65 for x in letters(TRAIN)]
    c2 = [[0] * 26 for _ in range(26)]
    for a, b in zip(t, t[1:]):
        c2[a][b] += 1
    f = [FREQ[x] / sum(FREQ.values()) for x in ALPHABET]
    return [[math.log((c2[a][b] + 3 * f[b]) / (sum(c2[a]) + 3)) for b in range(26)] for a in range(26)]


BIGRAM_LOG = _bigram_log()

_F = [FREQ[x] / sum(FREQ.values()) for x in ALPHABET]
# Pointwise mutual information log(P(b | a) / P(b)): how much more likely b
# is after a than at random. It does not reward a column for common letters.
PMI = [[BIGRAM_LOG[a][b] - math.log(_F[b]) for b in range(26)] for a in range(26)]


def multiple_anagram(ciphertexts: list[str]) -> list[int]:
    """Recover a common transposition from several ciphertexts of the same length.

    Write the ciphertexts one below the other. Column j holds, for every
    message, the letter of one fixed plaintext position. The score of the
    link i -> j is the sum over the messages of PMI[row[i]][row[j]]. Take
    the links from the best down, and keep a link when column i has no
    successor yet, column j has no predecessor yet, and the link does not
    close a cycle. The kept links form one chain. Returns the chain: the
    k-th entry is the ciphertext position of plaintext position k.

    A heuristic. It works well when there are many messages; with few
    messages, some links are wrong.
    """
    rows = [[ord(c) - 65 for c in letters(m)] for m in ciphertexts]
    if not rows:
        return []
    n = len(rows[0])
    if any(len(r) != n for r in rows):
        raise ValueError("the ciphertexts must have the same length")
    edges = sorted(
        ((sum(PMI[r[i]][r[j]] for r in rows), i, j) for i in range(n) for j in range(n) if i != j),
        reverse=True,
    )
    succ: dict[int, int] = {}
    pred: dict[int, int] = {}
    head = list(range(n))  # head[t] is the first node of the chain that ends at t
    tail = list(range(n))  # tail[h] is the last node of the chain that starts at h
    for _, i, j in edges:
        if len(succ) == n - 1:
            break
        if i in succ or j in pred or head[i] == j:
            continue
        succ[i], pred[j] = j, i
        h, t = head[i], tail[j]
        tail[h], head[t] = t, h
    start = next(v for v in range(n) if v not in pred)
    chain = [start]
    while chain[-1] in succ:
        chain.append(succ[chain[-1]])
    return chain
