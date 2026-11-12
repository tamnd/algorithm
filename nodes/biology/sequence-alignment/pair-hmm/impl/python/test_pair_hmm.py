# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pair-hmm/. The authors are listed in prov/RM3ZE9.jsonl.

import math
import random
from fractions import Fraction as F
from typing import Dict, List, Tuple

from pair_hmm import (
    PairHMM,
    affine_score,
    backward,
    forward,
    joint,
    log_odds_parameters,
    posterior_match,
    random_model_prob,
    viterbi,
)

DNA = "ACGT"


def example_model() -> PairHMM:
    p = {(a, b): (F(1, 8) if a == b else F(1, 24)) for a in DNA for b in DNA}
    return PairHMM(delta=F(1, 5), eps=F(2, 5), tau=F(1, 10), p=p, q={a: F(1, 4) for a in DNA})


def random_model(rng: random.Random, alphabet: str) -> PairHMM:
    delta = F(rng.randint(1, 20), 100)
    tau = F(rng.randint(1, 20), 100)
    eps = F(rng.randint(1, 100 - 100 * tau.numerator // tau.denominator - 1), 100)
    w = {(a, b): rng.randint(1, 9) for a in alphabet for b in alphabet}
    tw = sum(w.values())
    u = {a: rng.randint(1, 9) for a in alphabet}
    tu = sum(u.values())
    return PairHMM(delta, eps, tau, {k: F(v, tw) for k, v in w.items()}, {a: F(v, tu) for a, v in u.items()})


def all_paths(n: int, m: int) -> List[str]:
    """Every state path that emits n residues of x and m of y, with no X next to a Y."""
    out: List[str] = []

    def go(i: int, j: int, prev: str, acc: str) -> None:
        if (i, j) == (n, m):
            out.append(acc)
        if i < n and j < m:
            go(i + 1, j + 1, "M", acc + "M")
        if i < n and prev != "Y":
            go(i + 1, j, "X", acc + "X")
        if j < m and prev != "X":
            go(i, j + 1, "Y", acc + "Y")

    go(0, 0, "M", "")
    return out


def path_prob(h: PairHMM, x: str, y: str, path: str) -> F:
    """Independent product of the transition and emission terms of one path."""
    trans: Dict[Tuple[str, str], F] = {
        ("M", "M"): 1 - 2 * h.delta - h.tau, ("M", "X"): h.delta, ("M", "Y"): h.delta,
        ("X", "X"): h.eps, ("X", "M"): 1 - h.eps - h.tau, ("Y", "Y"): h.eps, ("Y", "M"): 1 - h.eps - h.tau,
    }
    prob, prev, i, j = F(1), "M", 0, 0
    for s in path:
        prob *= trans[(prev, s)]
        if s == "M":
            prob *= h.p[(x[i], y[j])]
            i, j = i + 1, j + 1
        elif s == "X":
            prob *= h.q[x[i]]
            i += 1
        else:
            prob *= h.q[y[j]]
            j += 1
        prev = s
    return prob * h.tau


def oracle(h: PairHMM, x: str, y: str):
    probs = {pa: path_prob(h, x, y, pa) for pa in all_paths(len(x), len(y))}
    return probs, sum(probs.values())


def test_example() -> None:
    h = example_model()
    total, _ = forward(h, "TAG", "TG")
    best, path = viterbi(h, "TAG", "TG")
    probs, want = oracle(h, "TAG", "TG")
    assert total == want
    assert best == max(probs.values())
    assert probs[path] == best
    assert path == "MXM"
    assert sorted(probs) == ["MMX", "MXM", "XMM", "XXMY", "YMXX"]
    assert want == F(43, 1280000) and best == F(1, 51200)
    post = posterior_match(h, "TAG", "TG")
    assert post[1][1] == F(100, 129) and post[2][1] == post[2][2] == F(25, 129)
    best, path = viterbi(h, "GATTC", "GTTAC")
    assert path == "MMMMM" and best == F(1, 94371840)
    assert forward(h, "GATTC", "GTTAC")[0] == F(9417331, 331776000000000)


def test_edges() -> None:
    h = example_model()
    assert forward(h, "", "")[0] == h.tau
    assert viterbi(h, "", "") == (h.tau, "")
    best, path = viterbi(h, "AC", "")
    assert path == "XX" and best == h.delta * h.eps * F(1, 16) * h.tau
    assert forward(h, "AC", "")[0] == best
    assert viterbi(h, "", "G")[1] == "Y"
    assert joint(h, "A", "C", "XY") == 0


def test_enumeration_random() -> None:
    rng = random.Random(7)
    for _ in range(500):
        alphabet = "AB" if rng.random() < 0.5 else "ACG"
        h = random_model(rng, alphabet)
        x = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 3)))
        y = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 3)))
        probs, want = oracle(h, x, y)
        total, _ = forward(h, x, y)
        assert total == want
        best, path = viterbi(h, x, y)
        assert best == max(probs.values()) == probs[path] == joint(h, x, y, path)
        b = backward(h, x, y)
        assert b["M"][0][0] == want
        post = posterior_match(h, x, y)
        for i in range(1, len(x) + 1):
            for j in range(1, len(y) + 1):
                # the M state emits (x_i, y_j) when the counts after it are i and j
                s = F(0)
                for pa, pr in probs.items():
                    ci = cj = 0
                    for st in pa:
                        ci += st in "MX"
                        cj += st in "MY"
                        if st == "M" and (ci, cj) == (i, j):
                            s += pr
                            break
                assert post[i][j] == s / want
        for i in range(1, len(x) + 1):
            assert sum(post[i][j] for j in range(1, len(y) + 1)) <= 1


def test_log_odds_mapping_exact() -> None:
    """P(path) / P(random) equals the product of Durbin's factors, in exact arithmetic."""
    rng = random.Random(11)
    for _ in range(200):
        h = random_model(rng, "AC")
        eta = F(rng.randint(1, 50), 100)
        x = "".join(rng.choice("AC") for _ in range(rng.randint(0, 3)))
        y = "".join(rng.choice("AC") for _ in range(rng.randint(0, 3)))
        amm, agm = 1 - 2 * h.delta - h.tau, 1 - h.eps - h.tau
        for pa in all_paths(len(x), len(y)):
            ratio = path_prob(h, x, y, pa) / random_model_prob(h, eta, x, y)
            want = h.tau / eta ** 2
            i = j = 0
            prev = "M"
            for st in pa:
                if st == "M":
                    want *= h.p[(x[i], y[j])] / (h.q[x[i]] * h.q[y[j]]) * amm / (1 - eta) ** 2
                    i, j = i + 1, j + 1
                else:
                    if prev == "M":
                        want *= h.delta * agm / ((1 - eta) * amm)
                    else:
                        want *= h.eps / (1 - eta)
                    i, j = i + (st == "X"), j + (st == "Y")
                prev = st
            if pa and pa[-1] != "M":
                want *= amm / agm
            assert ratio == want


def test_viterbi_equals_affine_alignment() -> None:
    rng = random.Random(3)
    for _ in range(300):
        h = random_model(rng, "ACG")
        hf = PairHMM(float(h.delta), float(h.eps), float(h.tau), {k: float(v) for k, v in h.p.items()}, {k: float(v) for k, v in h.q.items()})
        eta = rng.uniform(0.05, 0.5)
        x = "".join(rng.choice("ACG") for _ in range(rng.randint(0, 6)))
        y = "".join(rng.choice("ACG") for _ in range(rng.randint(0, 6)))
        best, _ = viterbi(hf, x, y)
        want = math.log2(best / random_model_prob(hf, eta, x, y))
        assert math.isclose(affine_score(hf, eta, x, y), want, abs_tol=1e-9)


def test_example_scores() -> None:
    h = example_model()
    s, d, e, c, const = log_odds_parameters(h, 0.1)
    assert math.isclose(d, -math.log2(2 / 9)) and math.isclose(e, -math.log2(4 / 9))
    assert c == 0.0
    assert math.isclose(s[("A", "A")], 1 + math.log2(50 / 81))
