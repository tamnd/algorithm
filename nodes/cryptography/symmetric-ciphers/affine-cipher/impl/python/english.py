# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/affine-cipher/. The authors are listed in prov/WCAD3J.jsonl.
"""English statistics shared by the classical cipher pages.

For study only. These helpers score candidate plaintexts in the attacks on
the classical ciphers. They are not part of any secure system.

Sources:
- FREQ: the probabilities of the 26 letters in English that Beker and Piper
  (Cipher Systems, 1982) report, as printed in Stinson and Paterson,
  Cryptography: Theory and Practice, 4th edition, 2018, Table 2.1.
- SAMPLE: the first two sentences of the United States Declaration of
  Independence (1776), public domain. The attack tests encrypt this text.
- TRAIN: the Gettysburg Address of Abraham Lincoln (1863, the Bliss copy),
  public domain, with simplified punctuation. The n-gram model is built only
  from TRAIN, so the model never sees the text that the tests attack.
"""

import math

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

FREQ = {
    "A": 0.082, "B": 0.015, "C": 0.028, "D": 0.043, "E": 0.127, "F": 0.022,
    "G": 0.020, "H": 0.061, "I": 0.070, "J": 0.002, "K": 0.008, "L": 0.040,
    "M": 0.024, "N": 0.067, "O": 0.075, "P": 0.019, "Q": 0.001, "R": 0.060,
    "S": 0.063, "T": 0.091, "U": 0.028, "V": 0.010, "W": 0.023, "X": 0.001,
    "Y": 0.020, "Z": 0.001,
}

SAMPLE = (
    "When in the Course of human events, it becomes necessary for one people "
    "to dissolve the political bands which have connected them with another, "
    "and to assume among the powers of the earth, the separate and equal "
    "station to which the Laws of Nature and of Nature's God entitle them, a "
    "decent respect to the opinions of mankind requires that they should "
    "declare the causes which impel them to the separation. We hold these "
    "truths to be self-evident, that all men are created equal, that they are "
    "endowed by their Creator with certain unalienable Rights, that among "
    "these are Life, Liberty and the pursuit of Happiness."
)

TRAIN = (
    "Four score and seven years ago our fathers brought forth on this "
    "continent, a new nation, conceived in Liberty, and dedicated to the "
    "proposition that all men are created equal. Now we are engaged in a "
    "great civil war, testing whether that nation, or any nation so conceived "
    "and so dedicated, can long endure. We are met on a great battle-field of "
    "that war. We have come to dedicate a portion of that field, as a final "
    "resting place for those who here gave their lives that that nation might "
    "live. It is altogether fitting and proper that we should do this. But, in "
    "a larger sense, we can not dedicate, we can not consecrate, we can not "
    "hallow, this ground. The brave men, living and dead, who struggled here, "
    "have consecrated it, far above our poor power to add or detract. The "
    "world will little note, nor long remember what we say here, but it can "
    "never forget what they did here. It is for us the living, rather, to be "
    "dedicated here to the unfinished work which they who fought here have "
    "thus far so nobly advanced. It is rather for us to be here dedicated to "
    "the great task remaining before us, that from these honored dead we take "
    "increased devotion to that cause for which they gave the last full "
    "measure of devotion, that we here highly resolve that these dead shall "
    "not have died in vain, that this nation, under God, shall have a new "
    "birth of freedom, and that government of the people, by the people, for "
    "the people, shall not perish from the earth."
)


def letters(text: str) -> str:
    """Keep the letters A to Z of text, in upper case."""
    return "".join(c for c in text.upper() if "A" <= c <= "Z")


def counts(text: str) -> list[int]:
    """The number of times each letter A to Z occurs in text."""
    out = [0] * 26
    for c in letters(text):
        out[ord(c) - 65] += 1
    return out


def chi_squared(text: str) -> float:
    """Pearson's chi-squared statistic of the letter counts of text against FREQ.

    A small value means that the letters look like English. The cost is
    linear in the length of text.
    """
    c = counts(text)
    n = sum(c)
    if n == 0:
        return math.inf
    total = 0.0
    for i in range(26):
        expected = n * FREQ[ALPHABET[i]]
        total += (c[i] - expected) ** 2 / expected
    return total


def index_of_coincidence(text: str) -> float:
    """The probability that two letters of text, drawn without replacement, are equal."""
    c = counts(text)
    n = sum(c)
    if n < 2:
        return 0.0
    return sum(x * (x - 1) for x in c) / (n * (n - 1))


def _trigram_log_table() -> list[list[list[float]]]:
    """Log probabilities log P(c | a b) for letters a, b, c, built from TRAIN.

    The trigram counts of TRAIN are smoothed toward the bigram estimate, and
    the bigram counts toward FREQ, each with a weight of 3, so that no
    probability is zero. Word gaps are ignored.
    """
    t = [ord(x) - 65 for x in letters(TRAIN)]
    c2 = [[0] * 26 for _ in range(26)]
    c3: dict[tuple[int, int, int], int] = {}
    for a, b in zip(t, t[1:]):
        c2[a][b] += 1
    for a, b, c in zip(t, t[1:], t[2:]):
        c3[(a, b, c)] = c3.get((a, b, c), 0) + 1
    f = [FREQ[x] / sum(FREQ.values()) for x in ALPHABET]
    p2 = [[(c2[a][b] + 3 * f[b]) / (sum(c2[a]) + 3) for b in range(26)] for a in range(26)]
    return [
        [[math.log((c3.get((a, b, c), 0) + 3 * p2[b][c]) / (c2[a][b] + 3)) for c in range(26)] for b in range(26)]
        for a in range(26)
    ]


TRIGRAM_LOG = _trigram_log_table()


def ngram_score(text: str) -> float:
    """The log likelihood of the letters of text under the trigram model.

    A larger value means that the text looks more like English.
    """
    t = [ord(x) - 65 for x in letters(text)]
    return sum(TRIGRAM_LOG[a][b][c] for a, b, c in zip(t, t[1:], t[2:]))
