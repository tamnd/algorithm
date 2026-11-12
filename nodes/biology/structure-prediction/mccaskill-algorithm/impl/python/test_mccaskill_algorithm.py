# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mccaskill-algorithm/. The authors are listed in prov/Y916HH.jsonl.

import random
from fractions import Fraction
from typing import Iterator

from mccaskill_algorithm import Model, base_pair_probabilities, can_pair, energy, inside, partition_function, sample


def all_structures(s: str, m: int) -> Iterator[list[tuple[int, int]]]:
    """Every secondary structure of s, by brute force over the partner of the first base."""

    def rec(i: int, j: int) -> Iterator[list[tuple[int, int]]]:
        if j - i < 1:
            yield []
            return
        yield from rec(i + 1, j)
        for k in range(i + m + 1, j + 1):
            if can_pair(s[i], s[k]):
                for inner in rec(i + 1, k - 1):
                    for outer in rec(k + 1, j):
                        yield [(i, k)] + inner + outer

    yield from rec(0, len(s) - 1)


def brute(s: str, z, model: Model):
    """Brute-force Z and pair probabilities: the sum of z ** E over allowed structures."""
    Z = Fraction(0)
    weight_with: dict = {}
    for t in all_structures(s, model.m):
        e = energy(s, t, model)
        if e is None:
            continue
        w = z ** e
        Z += w
        for p in t:
            weight_with[p] = weight_with.get(p, 0) + w
    return Z, {p: w / Z for p, w in weight_with.items()}


def test_single_hairpin() -> None:
    # GGGAAACCC: structures are the empty one (E = 0) and stacks ending in a hairpin.
    s = "GGGAAACCC"
    z = Fraction(1, 2)
    Z, _ = brute(s, z, Model())
    assert partition_function(s, z) == Z


def test_partition_function_against_brute_force() -> None:
    rng = random.Random(3)
    for _ in range(120):
        n = rng.randint(0, 13)
        s = "".join(rng.choice("ACGU") for _ in range(n))
        z = Fraction(rng.randint(1, 5), rng.randint(1, 5))
        Z, _ = brute(s, z, Model())
        assert partition_function(s, z) == Z


def test_probabilities_against_brute_force() -> None:
    rng = random.Random(4)
    for _ in range(80):
        n = rng.randint(5, 13)
        s = "".join(rng.choice("GCGCAU") for _ in range(n))
        model = Model(
            m=rng.choice((1, 3)),
            a=rng.randint(0, 4),
            b=rng.randint(-1, 2),
            c=rng.randint(0, 2),
            max_loop=rng.choice((1, 3, 30)),
        )
        z = Fraction(1, rng.randint(2, 4))
        Zb, Pb = brute(s, z, model)
        Z, P = base_pair_probabilities(s, z, model)
        assert Z == Zb
        for p in set(P) | set(Pb):
            assert P.get(p, 0) == Pb.get(p, 0), (s, p)


def test_probabilities_sum() -> None:
    s = "GGGAGAAACUCCCAGCAAAGCUGG"
    z = Fraction(2, 3)
    Z, P = base_pair_probabilities(s, z)
    for x in range(len(s)):
        total = sum(p for (i, j), p in P.items() if x in (i, j))
        assert 0 <= total <= 1


def test_sampling_matches_boltzmann() -> None:
    s = "GGAGGAAAACCCCA"
    z = Fraction(1, 2)
    model = Model()
    Zb, Pb = brute(s, z, model)
    tables = inside(s, z, model)
    rng = random.Random(2024)
    counts: dict = {}
    pair_counts: dict = {}
    trials = 3000
    for _ in range(trials):
        t = tuple(sample(s, z, rng, model, tables))
        assert energy(s, list(t), model) is not None
        counts[t] = counts.get(t, 0) + 1
        for p in t:
            pair_counts[p] = pair_counts.get(p, 0) + 1
    for p, prob in Pb.items():
        assert abs(pair_counts.get(p, 0) / trials - float(prob)) < 0.04
    for t, c in counts.items():
        exact = float(z ** energy(s, list(t), model) / Zb)
        assert abs(c / trials - exact) < 0.04


def test_float_weights() -> None:
    s = "GGGAAAUCCAGCAAAGC"
    zf = 0.6
    zq = Fraction(3, 5)
    assert abs(partition_function(s, zf) - float(partition_function(s, zq))) < 1e-9 * float(partition_function(s, zq))
