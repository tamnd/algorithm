# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/punkt-sentence-tokenizer/. The authors are listed in prov/BAJBZ1.jsonl.

"""Punkt sentence boundary detection, after Kiss and Strunk (2006).

The method is unsupervised: it learns from the text that it splits. A type-based
stage finds abbreviation types by a scaled likelihood ratio. A token-based stage
then looks at the word after each period and decides with three heuristics: the
orthographic heuristic, the collocation heuristic and the frequent sentence
starter heuristic.

Tokens are the runs of non-space characters. Quotes and brackets at the two ends
of a token are ignored, so 'end.)' is a token with a final period. The type of a
token is its word in lower case, without the final marks; a word of digits is
folded into the type NUMBER, as in the paper.

The thresholds 0.3, 7.88 and 30 and the value 0.99 are the ones of the paper,
which found them by manual experiments on Wall Street Journal text.
"""

import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

NUMBER = "##number##"
OPENERS = "\"'([{"
CLOSERS = "\"')]}"
NUMBER_RE = re.compile(r"\d+(?:[.,]\d+)*")
P_ABBREV = 0.99
ABBREV_THRESHOLD = 0.3
COLLOCATION_THRESHOLD = 7.88
STARTER_THRESHOLD = 30.0

UC_START, LC_START, UC_MID, LC_MID = 1, 2, 4, 8


@dataclass(frozen=True)
class Token:
    start: int  # the token covers text[start:end]
    end: int
    kind: str  # "." final period, "..." ellipsis, "?" for ? or !, "" no final mark
    word: str  # the word in its original case, without the final marks
    type: str  # the word in lower case; digits are folded into NUMBER


def tokenize(text: str) -> List[Token]:
    """Split a text at white space and classify the final mark of each token."""
    out = []
    for m in re.finditer(r"\S+", text):
        q = m.group().lstrip(OPENERS).rstrip(CLOSERS)
        if q.endswith("..."):
            kind = "..."
        elif q.endswith("."):
            kind = "."
        elif q[-1:] in ("?", "!"):
            kind = "?"
        else:
            kind = ""
        word = q.rstrip(".?!,;:") or q or m.group()
        typ = word.lower()
        if NUMBER_RE.fullmatch(typ):
            typ = NUMBER
        out.append(Token(m.start(), m.end(), kind, word, typ))
    return out


def _xlogy(k: float, x: float) -> float:
    """k * ln x, with 0 * ln 0 = 0."""
    if k == 0:
        return 0.0
    if x <= 0.0:
        return -math.inf
    return k * math.log(x)


def _binom_ll(k: int, n: int, x: float) -> float:
    """ln of x^k (1-x)^(n-k); the binomial coefficient cancels in each ratio."""
    return _xlogy(k, x) + _xlogy(n - k, 1.0 - x)


def abbreviation_log_lambda(c_with: int, c_without: int, c_period: int, n: int) -> float:
    """Revised log lambda of the type stage: P(. | w) = C(.)/N against P(. | w) = 0.99."""
    k, m = c_with, c_with + c_without
    p = c_period / n
    return -2.0 * (_binom_ll(k, m, p) - _binom_ll(k, m, P_ABBREV))


def abbreviation_score(w: str, c_with: int, c_without: int, c_period: int, n: int) -> float:
    """log lambda times F_length, F_periods and F_penalty, as in Kiss and Strunk."""
    periods = w.count(".")
    length = len(w) - periods
    ll = abbreviation_log_lambda(c_with, c_without, c_period, n)
    return ll * math.exp(-length) * (periods + 1) / length ** c_without


def dunning_log_lambda(c1: int, c2: int, c12: int, n: int) -> float:
    """Dunning's log likelihood ratio for the bigram w1 w2, from C(w1), C(w2), C(w1, w2), N."""
    p = c2 / n
    p1 = c12 / c1
    p2 = (c2 - c12) / (n - c1) if n > c1 else 0.0
    return -2.0 * (_binom_ll(c12, c1, p) + _binom_ll(c2 - c12, n - c1, p)
                   - _binom_ll(c12, c1, p1) - _binom_ll(c2 - c12, n - c1, p2))


def is_collocation(c1: int, c2: int, c12: int, n: int, threshold: float) -> bool:
    """log lambda at least the threshold, and the one-sided test C(w1, w2)/C(w1) > C(w2)/N."""
    if c1 == 0 or c12 == 0:
        return False
    return dunning_log_lambda(c1, c2, c12, n) >= threshold and c12 * n > c2 * c1


def is_initial(t: Token) -> bool:
    return t.kind == "." and len(t.type) == 1 and t.type.isalpha()


def is_number(t: Token) -> bool:
    return t.kind == "." and t.type == NUMBER


@dataclass
class Model:
    count: Counter
    abbrevs: Set[str]
    ortho: Dict[str, int]
    starters: Set[str]
    pairs: Counter
    n: int


def _ortho(u: Token, model: Model) -> Optional[bool]:
    """True: boundary before u, False: no boundary, None: undecided (Figure 3 of the paper)."""
    if all(ch in ";:,.!?" for ch in u.word):
        return False
    flags = model.ortho.get(u.type, 0)
    first = u.word[:1]
    if first.isupper() and flags & (LC_START | LC_MID) and not flags & UC_MID:
        return True
    if first.islower() and (flags & (UC_START | UC_MID) or not flags & LC_START):
        return False
    return None


def _colloc(t: Token, u: Token, model: Model) -> bool:
    c = model.count
    return is_collocation(c[t.type], c[u.type], model.pairs[(t.type, u.type)], model.n,
                          COLLOCATION_THRESHOLD)


def _statistics(toks: List[Token], first: List[bool], count: Counter, abbrevs: Set[str]) -> Model:
    """Case statistics, frequent sentence starters and bigram counts after a period."""
    n = len(toks)
    ortho: Dict[str, int] = {}
    for i, t in enumerate(toks):
        if i == 0:
            start = True
        else:
            prev = toks[i - 1]
            if prev.kind == "..." or (prev.kind == "." and (not first[i - 1] or is_initial(prev) or is_number(prev))):
                continue  # position unknown: after an abbreviation, an ellipsis, an initial or a number
            start = first[i - 1]
        c = t.word[:1]
        if c.isupper():
            ortho[t.type] = ortho.get(t.type, 0) | (UC_START if start else UC_MID)
        elif c.islower():
            ortho[t.type] = ortho.get(t.type, 0) | (LC_START if start else LC_MID)
    sure = [i for i in range(n - 1)
            if toks[i].kind == "." and first[i] and not is_initial(toks[i]) and not is_number(toks[i])]
    after_sure = Counter(toks[i + 1].type for i in sure)
    starters = {w for w, k in after_sure.items()
                if is_collocation(len(sure), count[w], k, n, STARTER_THRESHOLD)}
    pairs = Counter((toks[i].type, toks[i + 1].type) for i in range(n - 1) if toks[i].kind == ".")
    return Model(count, abbrevs, ortho, starters, pairs, n)


def punkt(text: str) -> Tuple[List[Token], List[bool], Model]:
    """Return the tokens, a flag per token that is True if a sentence ends after it, and the model.

    Cost: O(len(text)) expected time and space, with hash tables for the counts.
    """
    toks = tokenize(text)
    n = len(toks)
    count = Counter(t.type for t in toks)  # @line L1
    with_period = Counter(t.type for t in toks if t.kind == ".")
    c_period = sum(with_period.values())
    abbrevs: Set[str] = set()
    for w, k in with_period.items():  # @line L2
        if w == NUMBER or not any(ch.isalpha() for ch in w):
            continue
        s = abbreviation_score(w, k, count[w] - k, c_period, n)  # @line L3
        if s >= ABBREV_THRESHOLD:  # @line L4
            abbrevs.add(w)
    first = [t.kind == "?" or (t.kind == "." and t.type not in abbrevs) for t in toks]  # @line L5
    model = _statistics(toks, first, count, abbrevs)  # @line L6
    ends = list(first)
    for i in range(n - 1):  # @line L7
        t, u = toks[i], toks[i + 1]
        if t.kind not in (".", "..."):
            continue
        if t.kind == "..." or (t.type in abbrevs and not is_initial(t)):  # @line L8
            ends[i] = _ortho(u, model) is True or (u.word[:1].isupper() and u.type in model.starters)  # @line L9
        elif is_initial(t) or is_number(t):  # @line L10
            o = _ortho(u, model)
            if (_colloc(t, u, model) and u.type not in model.starters) or o is False:  # @line L11
                ends[i] = False  # @line L12
            elif is_initial(t) and o is None and u.word[:1].isupper() \
                    and model.ortho.get(u.type, 0) & (LC_START | LC_MID) == 0:  # @line L13
                ends[i] = False  # @line L14
    if n:
        ends[-1] = True  # @line L15
    return toks, ends, model


def split_sentences(text: str) -> List[str]:
    """Split a text into sentences with Punkt trained on the same text."""
    toks, ends, _ = punkt(text)
    out, begin = [], None
    for t, e in zip(toks, ends):
        if begin is None:
            begin = t.start
        if e:
            out.append(text[begin:t.end])
            begin = None
    return out
