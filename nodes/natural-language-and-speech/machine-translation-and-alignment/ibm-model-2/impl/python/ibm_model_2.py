# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ibm-model-2/. The authors are listed in prov/Z3VPZP.jsonl.

"""IBM Model 2 and its EM training (Brown et al. 1993, Section 4.2).

A pair is (f, e): the generated sentence f = f_1 .. f_m and the given sentence
e = e_1 .. e_l. With null=True, the null word e_0 = NULL is put in front of e
and positions run over 0 .. l; without it they run over 1 .. l.

    p(f, a | e) = eps * prod_j a(a_j | j, l, m) t(f_j | e_{a_j})
    p(f | e)    = eps * prod_j sum_i a(i | j, l, m) t(f_j | e_i)

t maps (f_word, e_word) to t(f_word | e_word); a maps (i, j, l, m) to
a(i | j, l, m). The constant eps does not change EM and is left out. All
arithmetic follows the type of the values: with Fraction values it is exact.
"""

import math
from collections import defaultdict
from fractions import Fraction
from typing import Dict, List, Sequence, Tuple

NULL = "<null>"
Pair = Tuple[Sequence[str], Sequence[str]]  # (f, e)
TTable = Dict[Tuple[str, str], Fraction]
ATable = Dict[Tuple[int, int, int, int], Fraction]


def _given(e: Sequence[str], null: bool) -> List[str]:
    return ([NULL] if null else []) + list(e)


def _positions(l: int, null: bool) -> range:
    return range(0 if null else 1, l + 1)


def uniform_t(corpus: Sequence[Pair], null: bool = False) -> TTable:
    vf = sorted({x for f, _ in corpus for x in f})
    ve = sorted({y for _, e in corpus for y in _given(e, null)})
    return {(x, y): Fraction(1, len(vf)) for x in vf for y in ve}


def uniform_a(corpus: Sequence[Pair], null: bool = False) -> ATable:
    """a(i | j, l, m) = 1 / (number of positions) for every shape (l, m) in the corpus."""
    a: ATable = {}
    for f, e in corpus:
        l, m = len(e), len(f)
        pos = _positions(l, null)
        for j in range(1, m + 1):
            for i in pos:
                a[(i, j, l, m)] = Fraction(1, len(pos))
    return a


def model1_t(corpus: Sequence[Pair], rounds: int, null: bool = False) -> TTable:
    """Model 1 training: Model 2 EM with a held uniform. Used as the start of Model 2."""
    t, a = uniform_t(corpus, null), uniform_a(corpus, null)
    for _ in range(rounds):
        t, _ = em_step(corpus, t, a, null)
    return t


def expected_counts(corpus: Sequence[Pair], t: TTable, a: ATable, null: bool = False):
    """The E step: expected link counts c(f, e) and position counts c(i | j, l, m)."""
    ct: Dict[Tuple[str, str], Fraction] = defaultdict(Fraction)
    ca: Dict[Tuple[int, int, int, int], Fraction] = defaultdict(Fraction)
    for f, e in corpus:  # @line L4
        l, m = len(e), len(f)
        es = _given(e, True)  # es[i] is e_i, es[0] is NULL
        pos = _positions(l, null)
        for j, x in enumerate(f, start=1):
            z = sum(a[(i, j, l, m)] * t.get((x, es[i]), 0) for i in pos)  # @line L5
            for i in pos:  # @line L6
                p = a[(i, j, l, m)] * t.get((x, es[i]), 0) / z
                ct[(x, es[i])] += p
                ca[(i, j, l, m)] += p
    return ct, ca


def em_step(corpus: Sequence[Pair], t: TTable, a: ATable, null: bool = False) -> Tuple[TTable, ATable]:
    """One EM round; returns the new t and the new a."""
    ct, ca = expected_counts(corpus, t, a, null)  # @line L3
    tot_t: Dict[str, Fraction] = defaultdict(Fraction)
    for (x, y), v in ct.items():
        tot_t[y] += v
    tot_a: Dict[Tuple[int, int, int], Fraction] = defaultdict(Fraction)
    for (i, j, l, m), v in ca.items():
        tot_a[(j, l, m)] += v
    new_t = {k: (ct[k] / tot_t[k[1]] if tot_t[k[1]] else t[k]) for k in t}  # @line L7
    new_a = {k: (ca[k] / tot_a[k[1:]] if tot_a[k[1:]] else a[k]) for k in a}
    return new_t, new_a


def likelihood(corpus: Sequence[Pair], t: TTable, a: ATable, null: bool = False):
    """The corpus likelihood without eps, as a product."""
    p = Fraction(1)
    for f, e in corpus:
        l, m = len(e), len(f)
        es = _given(e, True)
        for j, x in enumerate(f, start=1):
            p *= sum(a[(i, j, l, m)] * t.get((x, es[i]), 0) for i in _positions(l, null))
    return p


def log_likelihood(corpus: Sequence[Pair], t: TTable, a: ATable, null: bool = False) -> float:
    """The same in nats, as a sum of logs, so long sentences do not underflow."""
    s = 0.0
    for f, e in corpus:
        l, m = len(e), len(f)
        es = _given(e, True)
        for j, x in enumerate(f, start=1):
            s += math.log(sum(a[(i, j, l, m)] * t.get((x, es[i]), 0) for i in _positions(l, null)))
    return s


def train(corpus: Sequence[Pair], rounds: int, null: bool = False, model1_rounds: int = 5,
          t: TTable = None, a: ATable = None) -> Tuple[TTable, ATable, list]:
    """EM for Model 2. t starts from Model 1 training unless given; a starts uniform unless given.

    Returns t, a and the likelihoods before each round and at the end.
    """
    if t is None:
        t = model1_t(corpus, model1_rounds, null)  # @line L1
    if a is None:
        a = uniform_a(corpus, null)
    history = [likelihood(corpus, t, a, null)]
    for _ in range(rounds):  # @line L2
        t, a = em_step(corpus, t, a, null)
        history.append(likelihood(corpus, t, a, null))
    return t, a, history  # @line L8


def viterbi_alignment(f: Sequence[str], e: Sequence[str], t: TTable, a: ATable, null: bool = False) -> List[int]:
    """The best a_j for each j, independently; the smallest i wins a tie."""
    l, m = len(e), len(f)
    es = _given(e, True)
    out = []
    for j, x in enumerate(f, start=1):
        pos = list(_positions(l, null))
        out.append(max(pos, key=lambda i: (a[(i, j, l, m)] * t.get((x, es[i]), 0), -i)))
    return out
