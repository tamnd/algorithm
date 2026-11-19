# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ibm-model-1/. The authors are listed in prov/Q63VWQ.jsonl.

"""IBM Model 1 and its EM training (Brown et al. 1993, Section 4.1).

A pair is (f, e): the generated sentence f = f_1 .. f_m and the given sentence
e = e_1 .. e_l. With null=True, the null word e_0 = NULL is put in front of e.
The table t maps (f_word, e_word) to t(f_word | e_word).

    p(f | e) = eps / (l + 1)^m * prod_j sum_{i=0..l} t(f_j | e_i)      (with NULL)
    p(f | e) = eps / l^m       * prod_j sum_{i=1..l} t(f_j | e_i)      (without)

The constant eps (the length probability) does not change EM, and the
functions here leave it out. All arithmetic follows the type of t: with
fractions.Fraction values every step is exact.
"""

import math
from collections import defaultdict
from fractions import Fraction
from typing import Dict, List, Sequence, Tuple

NULL = "<null>"
Pair = Tuple[Sequence[str], Sequence[str]]  # (f, e)
Table = Dict[Tuple[str, str], Fraction]


def _given(e: Sequence[str], null: bool) -> List[str]:
    return ([NULL] if null else []) + list(e)


def uniform_table(corpus: Sequence[Pair], null: bool = False) -> Table:
    """t(f | e) = 1 / |V_F| for every source word f and every given word e."""
    vf = sorted({x for f, _ in corpus for x in f})
    ve = sorted({y for _, e in corpus for y in _given(e, null)})
    return {(x, y): Fraction(1, len(vf)) for x in vf for y in ve}


def expected_counts(corpus: Sequence[Pair], t: Table, null: bool = False) -> Dict[Tuple[str, str], Fraction]:
    """The E step: the expected number of links between f_j and e_i, summed over the corpus."""
    c: Dict[Tuple[str, str], Fraction] = defaultdict(Fraction)
    for f, e in corpus:  # @line L4
        es = _given(e, null)
        for x in f:
            z = sum(t.get((x, y), 0) for y in es)  # @line L5
            for y in es:  # @line L6
                c[(x, y)] += t.get((x, y), 0) / z
    return c


def em_step(corpus: Sequence[Pair], t: Table, null: bool = False) -> Table:
    """One EM iteration; returns the new table."""
    c = expected_counts(corpus, t, null)  # @line L3
    total: Dict[str, Fraction] = defaultdict(Fraction)
    for (x, y), v in c.items():
        total[y] += v
    new = {key: (c[key] / total[key[1]] if total[key[1]] else t[key]) for key in t}  # @line L7
    return new


def likelihood(corpus: Sequence[Pair], t: Table, null: bool = False):
    """The corpus likelihood without eps, as a product (exact with Fraction values)."""
    p = Fraction(1)
    for f, e in corpus:
        es = _given(e, null)
        for x in f:
            p *= Fraction(sum(t.get((x, y), 0) for y in es)) / len(es)
    return p


def log_likelihood(corpus: Sequence[Pair], t: Table, null: bool = False) -> float:
    """The same in nats, as a sum of logs, so long corpora do not underflow."""
    s = 0.0
    for f, e in corpus:
        es = _given(e, null)
        for x in f:
            s += math.log(sum(t.get((x, y), 0) for y in es)) - math.log(len(es))
    return s


def train(corpus: Sequence[Pair], iterations: int, null: bool = False, t: Table = None) -> Tuple[Table, list]:
    """Run EM from t (uniform if None). Returns t and the likelihoods before each step and at the end."""
    if t is None:
        t = uniform_table(corpus, null)  # @line L1
    history = [likelihood(corpus, t, null)]
    for _ in range(iterations):  # @line L2
        t = em_step(corpus, t, null)
        history.append(likelihood(corpus, t, null))
    return t, history  # @line L8


def viterbi_alignment(f: Sequence[str], e: Sequence[str], t: Table, null: bool = False) -> List[int]:
    """The best a_j for each j, independently; the smallest i wins a tie.

    Positions are 0 .. l with NULL (0 is NULL), or 1 .. l without it.
    """
    es = _given(e, null)
    first = 0 if null else 1
    return [first + max(range(len(es)), key=lambda k: (t.get((x, es[k]), 0), -k)) for x in f]
