# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gor-method/. The authors are listed in prov/KTTQKV.jsonl.

import random
from fractions import Fraction
from math import isclose, log

from gor_method import gor_predict, gor_scores, train


def direct_scores(seq, info, states, half, decision=None):
    """Score each centre j by the direct sum over its window."""
    out = []
    for j in range(len(seq)):
        row = {}
        for s in states:
            total = (decision or {}).get(s, 0)
            for m in range(-half, half + 1):
                if 0 <= j + m < len(seq):
                    total += info.get((s, m, seq[j + m]), 0)
            row[s] = total
        out.append(row)
    return out


def direct_argmax(rows, states):
    return "".join(max(states, key=lambda s: (row[s], -states.index(s))) for row in rows)


def test_example() -> None:
    info = train(["AALAGG", "GGALAA"], ["HHHHCC", "CCHHHH"], "HC", 1, 1.0)
    assert isclose(info[("H", 0, "A")], log(Fraction(49, 36)))
    assert gor_predict("GALAG", info, "HC", 1) == "CHHHC"
    row = gor_scores("GALAG", info, "HC", 1)[2]
    assert isclose(row["H"], info[("H", -1, "A")] + info[("H", 0, "L")] + info[("H", 1, "A")])


def test_training_counts() -> None:
    rng = random.Random(3)
    seqs = ["".join(rng.choice("ACDE") for _ in range(rng.randint(1, 12))) for _ in range(5)]
    labs = ["".join(rng.choice("HEC") for _ in s) for s in seqs]
    info = train(seqs, labs, "HEC", 2, 0.5)
    pairs = [(lab[j], m, seq[j + m]) for seq, lab in zip(seqs, labs)
             for j in range(len(seq)) for m in range(-2, 3) if 0 <= j + m < len(seq)]
    n = sum(len(s) for s in seqs)
    for (s, m, a), v in info.items():
        f = sum(1 for p in pairs if p == (s, m, a))
        fm = sum(1 for p in pairs if p[1:] == (m, a))
        ns = sum(lab.count(s) for lab in labs)
        want = log(((f + 0.5) / (fm + 1.5)) / ((ns + 0.5) / (n + 1.5)))
        assert isclose(v, want, abs_tol=1e-12)


def test_scores_equal_direct_sum_exactly() -> None:
    rng = random.Random(1978)
    for half in (0, 1, 3, 8):
        for _ in range(20):
            info = {(s, m, a): rng.randint(-9, 9) for s in "HETC" for m in range(-half, half + 1) for a in "ACDEFG"}
            seq = "".join(rng.choice("ACDEFG") for _ in range(rng.randint(0, 30)))
            dec = {s: rng.randint(-3, 3) for s in "HETC"}
            got = gor_scores(seq, info, "HETC", half, dec)
            want = direct_scores(seq, info, "HETC", half, dec)
            assert got == want
            assert gor_predict(seq, info, "HETC", half, dec) == direct_argmax(want, "HETC")


def test_trained_table_matches_direct_sum() -> None:
    rng = random.Random(17)
    seqs = ["".join(rng.choice("ACDEFGHIKL") for _ in range(40)) for _ in range(6)]
    labs = ["".join(rng.choice("HEC") for _ in s) for s in seqs]
    info = train(seqs, labs)
    seq = "".join(rng.choice("ACDEFGHIKL") for _ in range(50))
    got = gor_scores(seq, info)
    want = direct_scores(seq, info, "HEC", 8)
    for g, w in zip(got, want):
        for s in "HEC":
            assert isclose(g[s], w[s], abs_tol=1e-9)
