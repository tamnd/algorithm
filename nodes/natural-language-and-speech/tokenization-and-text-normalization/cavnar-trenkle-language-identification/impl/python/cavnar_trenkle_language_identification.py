# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cavnar-trenkle-language-identification/. The authors are listed in prov/2S4GCR.jsonl.

"""Language identification by Cavnar-Trenkle n-gram rank profiles.

A profile is the list of the most frequent character n-grams of a text, for
n = 1 to 5, in decreasing order of count. Ties in the count go to the smaller
string (the paper gives no tie rule). Tokens are maximal runs of letters and
apostrophes; digits, punctuation and spaces separate tokens. For n >= 2 a token
w is padded as "_" + w + "_" * (n - 1), as in the paper, so a token of k
characters gives k + 1 n-grams of each length n >= 2. For n = 1 the letters
alone are used (k unigrams); this is a convention of this file. Case is kept.

The out-of-place distance adds |r - r'| for each n-gram at rank r in the
document profile and rank r' in the category profile, and a fixed maximum
penalty for an n-gram that is missing from the category profile. The paper
gives no value for the penalty; this file uses the profile length L.
"""

import re
from typing import Dict, List, Mapping, Optional, Sequence

TOKEN = re.compile(r"(?:[^\W\d_]|')+")
MAX_N = 5


def tokens(text: str) -> List[str]:
    """Return the maximal runs of letters and apostrophes in text."""
    return TOKEN.findall(text)


def ngram_counts(text: str, max_n: int = MAX_N) -> Dict[str, int]:
    """Return the count of each padded character n-gram of text, for n = 1 to max_n.

    Cost: O(max_n * len(text)) dictionary updates.
    """
    count: Dict[str, int] = {}  # @line L10
    for w in tokens(text):  # @line L11
        for n in range(1, max_n + 1):  # @line L12
            u = w if n == 1 else "_" + w + "_" * (n - 1)  # @line L13
            for i in range(len(u) - n + 1):  # @line L14
                g = u[i : i + n]
                count[g] = count.get(g, 0) + 1
    return count


def profile(text: str, size: int = 300, max_n: int = MAX_N) -> List[str]:
    """Return the size most frequent n-grams of text, highest count first.

    Ties in the count go to the smaller string. Cost: O(max_n * len(text))
    for the counts and O(G log G) for the sort of the G distinct n-grams.
    """
    count = ngram_counts(text, max_n)
    ranked = sorted(count, key=lambda g: (-count[g], g))  # @line L15
    return ranked[:size]  # @line L16


def out_of_place(doc: Sequence[str], cat: Sequence[str], penalty: Optional[int] = None) -> int:
    """Return the out-of-place distance of the document profile doc from the category profile cat.

    penalty is the cost of an n-gram of doc that is not in cat; the default
    is len(cat). Cost: O(len(doc) + len(cat)) with a hash map of the ranks.
    """
    if penalty is None:
        penalty = len(cat)
    rank = {g: r for r, g in enumerate(cat)}
    d = 0  # @line L4
    for r, g in enumerate(doc):  # @line L5
        if g in rank:  # @line L6
            d += abs(r - rank[g])
        else:  # @line L7
            d += penalty
    return d


def train(samples: Mapping[str, str], size: int = 300) -> Dict[str, List[str]]:
    """Return a profile of length at most size for each language from its training text."""
    return {lang: profile(text, size) for lang, text in samples.items()}


def classify(text: str, profiles: Mapping[str, Sequence[str]], size: int = 300) -> str:
    """Return the language whose profile is closest to the profile of text.

    The penalty for a missing n-gram is size. Ties in the distance go to the
    language that comes first in sorted order. Cost: O(len(text)) plus
    O(G log G) for the document profile and O(k size) for k languages.
    """
    if not profiles:
        raise ValueError("no language profiles")
    p = profile(text, size)  # @line L1
    best, best_d = None, None  # @line L2
    for lang in sorted(profiles):  # @line L3
        d = out_of_place(p, profiles[lang], size)
        if best_d is None or d < best_d:  # @line L8
            best, best_d = lang, d
    return best  # @line L9


def distances(text: str, profiles: Mapping[str, Sequence[str]], size: int = 300) -> Dict[str, int]:
    """Return the out-of-place distance of text from each language profile."""
    p = profile(text, size)
    return {lang: out_of_place(p, cat, size) for lang, cat in profiles.items()}
