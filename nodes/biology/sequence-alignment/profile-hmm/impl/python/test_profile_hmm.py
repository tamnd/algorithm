# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/profile-hmm/. The authors are listed in prov/MM4SQ5.jsonl.

import random
from fractions import Fraction as F
from typing import Dict, List, Tuple

from profile_hmm import ProfileHMM, allowed_transitions, build, forward, match_columns, path_probability, state_path, viterbi

MSA = ["TATA-AT", "TATG-AA", "TATG-AT", "CATAGAT", "TA-A-GT", "TGTGTAC"]


def random_model(rng: random.Random, m: int, alphabet: str, plan7: bool) -> ProfileHMM:
    keys = allowed_transitions(m, plan7)
    w = {key: rng.randint(1, 9) for key in keys}
    trans = {}
    for key in keys:
        tot = sum(v for kk, v in w.items() if kk[:2] == key[:2])
        trans[key] = F(w[key], tot)

    def dist() -> Dict[str, F]:
        u = {a: rng.randint(1, 9) for a in alphabet}
        t = sum(u.values())
        return {a: F(v, t) for a, v in u.items()}

    return ProfileHMM(m, alphabet, [{}] + [dist() for _ in range(m)], [dist() for _ in range(m + 1)], trans)


def all_paths(h: ProfileHMM, x: str) -> List[Tuple[List[Tuple[str, int]], F]]:
    """Depth-first enumeration of every state path from Begin to End that emits x."""
    out = []
    n, m = len(x), h.m

    def go(state: Tuple[str, int], i: int, path: List[Tuple[str, int]], prob: F) -> None:
        a, k = state
        for b in ("M", "I", "D"):
            tp = h.trans.get((a, k, b), F(0))
            if tp == 0:
                continue
            if b == "M" and k == m:
                if i == n:
                    out.append((list(path), prob * tp))
                continue
            nxt = (b, k + 1) if b in "MD" else (b, k)
            if b in "MI":
                if i == n:
                    continue
                e = (h.match_emit[k + 1] if b == "M" else h.insert_emit[k])[x[i]]
                go(nxt, i + 1, path + [nxt], prob * tp * e)
            else:
                go(nxt, i, path + [nxt], prob * tp)

    go(("M", 0), 0, [], F(1))
    return out


def test_example_construction() -> None:
    assert match_columns(MSA) == [0, 1, 2, 3, 5, 6]
    assert state_path("TA-A-GT", [0, 1, 2, 3, 5, 6]) == [("M", 0), ("M", 1), ("M", 2), ("D", 3), ("M", 4), ("M", 5), ("M", 6), ("M", 7)]
    h = build(MSA, "ACGT")
    assert h.m == 6
    assert (h.t(("M", 2, "M")), h.t(("M", 2, "D")), h.t(("M", 2, "I"))) == (F(6, 9), F(2, 9), F(1, 9))
    assert h.t(("M", 4, "I")) == F(3, 9) and h.t(("I", 4, "I")) == F(1, 5) and h.t(("I", 4, "M")) == F(3, 5)
    assert h.match_emit[1] == {"A": F(1, 10), "C": F(1, 5), "G": F(1, 10), "T": F(3, 5)}
    assert h.match_emit[3]["T"] == F(2, 3)
    assert h.insert_emit[4] == {"A": F(1, 6), "C": F(1, 6), "G": F(1, 3), "T": F(1, 3)}
    for a in ("M", "I", "D"):
        for k in range(h.m + 1):
            out = [v for key, v in h.trans.items() if key[:2] == (a, k)]
            if out:
                assert sum(out) == 1


def test_example_search() -> None:
    h = build(MSA, "ACGT")
    best, path = viterbi(h, "TATAAT")
    assert path == [("M", k) for k in range(1, 7)]
    assert best == path_probability(h, "TATAAT", path)
    best, path = viterbi(h, "TAAT")
    assert ("D", 3) in path and ("D", 4) in path
    assert forward(h, "TATAAT") > best


def test_edges() -> None:
    h = build(MSA, "ACGT")
    best, path = viterbi(h, "")
    assert path == [("D", k) for k in range(1, 7)]
    assert forward(h, "") == best
    one = build(["A", "A"], "AC")
    assert one.m == 1
    assert forward(one, "A") == sum(p for _, p in all_paths(one, "A"))
    zero = build(["-A", "--"], "AC", symfrac=0.9)
    assert zero.m == 0 and forward(zero, "") == zero.t(("M", 0, "M"))


def test_against_enumeration() -> None:
    rng = random.Random(5)
    for trial in range(500):
        plan7 = trial % 2 == 1
        alphabet = "AB" if rng.random() < 0.5 else "ACG"
        h = random_model(rng, rng.randint(0, 3), alphabet, plan7)
        x = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 4)))
        paths = all_paths(h, x)
        total = sum(p for _, p in paths)
        assert forward(h, x) == total
        best, path = viterbi(h, x)
        assert best == max(p for _, p in paths)
        assert path_probability(h, x, path) == best


def test_built_models_against_enumeration() -> None:
    rng = random.Random(9)
    for _ in range(150):
        rows, cols = rng.randint(1, 4), rng.randint(1, 5)
        msa = ["".join(rng.choice("AC--") for _ in range(cols)) for _ in range(rows)]
        try:
            h = build(msa, "AC", plan7=rng.random() < 0.5)
        except ValueError:  # a D next to an I is not allowed in Plan 7
            h = build(msa, "AC")
        x = "".join(rng.choice("AC") for _ in range(rng.randint(0, 3)))
        paths = all_paths(h, x)
        assert forward(h, x) == sum(p for _, p in paths)
        assert viterbi(h, x)[0] == max(p for _, p in paths)
