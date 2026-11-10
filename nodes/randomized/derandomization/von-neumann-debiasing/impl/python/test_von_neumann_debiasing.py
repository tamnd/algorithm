# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/von-neumann-debiasing/. The authors are listed in prov/0S9GAW.jsonl.

import itertools
import random
from fractions import Fraction

from von_neumann_debiasing import peres_debiasing, von_neumann_debiasing


def output_distribution(f, n: int, p: Fraction) -> dict[tuple[int, ...], Fraction]:
    dist: dict[tuple[int, ...], Fraction] = {}
    for x in itertools.product((0, 1), repeat=n):
        w = p ** sum(x) * (1 - p) ** (n - sum(x))
        out = tuple(f(list(x)))
        dist[out] = dist.get(out, Fraction(0)) + w
    return dist


def assert_uniform_given_length(dist: dict[tuple[int, ...], Fraction]) -> None:
    by_length: dict[int, list[Fraction]] = {}
    for out, w in dist.items():
        by_length.setdefault(len(out), []).append(w)
    for length, weights in by_length.items():
        assert len(weights) == 2**length
        assert len(set(weights)) == 1


def test_example() -> None:
    x = [1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1]
    assert von_neumann_debiasing(x) == [0, 1, 0]
    assert peres_debiasing(x) == [0, 1, 0, 0, 0, 0, 1]
    assert peres_debiasing(x, depth=1) == [0, 1, 0]


def test_edges() -> None:
    for f in (von_neumann_debiasing, peres_debiasing):
        assert f([]) == []
        assert f([1]) == []
        assert f([0, 0, 0, 0]) == []
        assert f([1, 1, 1, 1, 1]) == []
        assert f([0, 1]) == [0]
        assert f([1, 0]) == [1]


def test_exact_uniformity_von_neumann() -> None:
    for p in (Fraction(1, 3), Fraction(1, 10), Fraction(1, 2)):
        for n in range(0, 11):
            assert_uniform_given_length(output_distribution(von_neumann_debiasing, n, p))


def test_exact_uniformity_peres() -> None:
    for p in (Fraction(1, 3), Fraction(3, 4)):
        for n in range(0, 11):
            for depth in (1, 2, 3, 64):
                assert_uniform_given_length(output_distribution(lambda b: peres_debiasing(b, depth), n, p))


def test_expected_yield() -> None:
    # Each pair gives one bit with probability 2 p (1 - p).
    for p in (Fraction(1, 3), Fraction(1, 5)):
        for n in range(0, 11):
            dist = output_distribution(von_neumann_debiasing, n, p)
            mean = sum((len(out) * w for out, w in dist.items()), Fraction(0))
            assert mean == (n // 2) * 2 * p * (1 - p)
    dist = output_distribution(peres_debiasing, 4, Fraction(1, 3))
    assert sum((len(out) * w for out, w in dist.items()), Fraction(0)) == Fraction(40, 27)


def test_peres_extends_von_neumann() -> None:
    rng = random.Random(9)
    for _ in range(300):
        x = [rng.randint(0, 1) for _ in range(rng.randint(0, 40))]
        vn = von_neumann_debiasing(x)
        ps = peres_debiasing(x)
        assert ps[: len(vn)] == vn
        assert len(ps) >= len(vn)


def test_rate_statistical() -> None:
    # Fixed seed, p = 0.3, 200000 input bits. The von Neumann rate is
    # p (1 - p) = 0.21 per input bit; Peres with 3 levels has rate 0.4926.
    # Each count is a sum of bounded pair contributions, so a deviation of 0.01
    # has probability far below 1e-6 for a correct implementation.
    rng = random.Random(1)
    n = 200000
    bits = [1 if rng.random() < 0.3 else 0 for _ in range(n)]
    assert abs(len(von_neumann_debiasing(bits)) / n - 0.21) < 0.01
    assert abs(len(peres_debiasing(bits, 3)) / n - 0.4926) < 0.01
    out = peres_debiasing(bits)
    assert abs(sum(out) / len(out) - 0.5) < 0.01


def test_correlated_source_is_not_debiased() -> None:
    # A Markov source: the first bit is fair, then each bit repeats the
    # previous one with probability 3/4. Pairs 01 and 10 are equally likely
    # inside a pair, but the output bits are dependent: the exact probability
    # that two outputs from n = 4 inputs are both 0 is not 1/4 of the
    # probability of two outputs.
    def weight(x: tuple[int, ...]) -> Fraction:
        w = Fraction(1, 2)
        for a, b in zip(x, x[1:]):
            w *= Fraction(3, 4) if a == b else Fraction(1, 4)
        return w

    two = {}
    for x in itertools.product((0, 1), repeat=4):
        out = tuple(von_neumann_debiasing(list(x)))
        if len(out) == 2:
            two[out] = two.get(out, Fraction(0)) + weight(x)
    assert len(set(two.values())) > 1
