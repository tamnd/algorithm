# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chain-sampling/. The authors are listed in prov/MV8B8B.jsonl.

import random
from collections import Counter, deque
from fractions import Fraction

import pytest

from chain_sampling import ChainSampler


class NeedMore(Exception):
    def __init__(self, n: int) -> None:
        self.n = n


class ReplayRandom(random.Random):
    """Returns scripted outcomes of randrange; raises NeedMore when they run out."""

    def __init__(self, script: list[int]) -> None:
        super().__init__(0)
        self.script = script
        self.pos = 0
        self.prob = Fraction(1)

    def randrange(self, n: int) -> int:  # type: ignore[override]
        if self.pos == len(self.script):
            raise NeedMore(n)
        c = self.script[self.pos]
        self.pos += 1
        self.prob /= n
        return c


def clone(s: ChainSampler, rng: random.Random) -> ChainSampler:
    c: ChainSampler = ChainSampler(s.w, rng)
    c.t, c.want, c.chain = s.t, s.want, deque(s.chain)
    return c


def key(s: ChainSampler) -> tuple:
    return (tuple(s.chain), s.want)


def exact_distribution(w: int, steps: int, step_fn=None):
    """Yield, after each step t, a dict from sampler state to its exact probability."""
    states = {key(ChainSampler(w, random.Random(0))): (Fraction(1), ChainSampler(w, random.Random(0)))}
    for t in range(1, steps + 1):
        nxt: dict = {}
        for p, s in states.values():
            todo: list[list[int]] = [[]]
            while todo:
                script = todo.pop()
                rng = ReplayRandom(script)
                c = clone(s, rng)
                try:
                    (step_fn or ChainSampler.step)(c, t)
                except NeedMore as e:
                    todo.extend(script + [k] for k in range(e.n))
                    continue
                k = key(c)
                q = p * rng.prob
                nxt[k] = (nxt[k][0] + q, nxt[k][1]) if k in nxt else (q, c)
        states = nxt
        assert sum(p for p, _ in states.values()) == 1
        yield t, states


def expected_length(w: int, t: int) -> Fraction:
    r = 1 + Fraction(1, w)
    if t >= w:
        return r**w - 1
    return Fraction(w, t) * (r**t - 1)


@pytest.mark.parametrize("w", [1, 2, 3, 4])
def test_exact_uniformity_and_memory(w: int) -> None:
    steps = {1: 6, 2: 9, 3: 9, 4: 8}[w]
    for t, states in exact_distribution(w, steps):
        dist: dict[int, Fraction] = {}
        mean_len = Fraction(0)
        for p, s in states.values():
            s.check_invariant()
            assert s.sample() == s.sample_index()  # the item value is its index
            dist[s.sample_index()] = dist.get(s.sample_index(), Fraction(0)) + p
            mean_len += p * len(s.chain)
        window = range(max(1, t - w + 1), t + 1)
        assert set(dist) == set(window)
        assert all(dist[i] == Fraction(1, min(t, w)) for i in window)
        assert mean_len == expected_length(w, t)


def literal_step(s: ChainSampler, x: int) -> None:
    """A coin at every arrival, even when the sample expires in the same step."""
    w = s.w
    s.t += 1
    t = s.t
    if t == s.want:
        s.chain.append((t, x))
        s.want = t + 1 + s.rng.randrange(w)
    if s.chain and s.chain[0][0] == t - w:
        s.chain.popleft()
    if s.rng.randrange(min(t, w)) == 0:
        s.chain = deque([(t, x)])
        s.want = t + 1 + s.rng.randrange(w)


def test_coin_at_expiry_step_is_biased() -> None:
    for t, states in exact_distribution(2, 3, literal_step):
        if t == 3:
            dist: dict[int, Fraction] = {}
            for p, s in states.values():
                dist[s.sample_index()] = dist.get(s.sample_index(), Fraction(0)) + p
            assert dist == {2: Fraction(3, 8), 3: Fraction(5, 8)}


def test_seeded_trials() -> None:
    # 20000 runs, window 5, 30 items: each of the 5 window positions is
    # expected 4000 times; the standard deviation is about 57, and the test
    # allows 5 standard deviations.
    rng = random.Random(12345)
    counts: Counter = Counter()
    lengths = 0
    runs, w, n = 20000, 5, 30
    for _ in range(runs):
        s: ChainSampler = ChainSampler(w, rng)
        for x in range(1, n + 1):
            s.step(x)
        counts[s.sample()] += 1
        lengths += len(s.chain)
    assert set(counts) == set(range(n - w + 1, n + 1))
    assert all(abs(c - runs / w) < 5 * 57 for c in counts.values())
    assert abs(lengths / runs - float(expected_length(w, n))) < 0.05


def test_long_stream_invariant_and_memory() -> None:
    rng = random.Random(7)
    for w in [1, 2, 10, 100]:
        s: ChainSampler = ChainSampler(w, rng)
        total = 0
        steps = 4000
        for x in range(1, steps + 1):
            s.step(x)
            s.check_invariant()
            total += len(s.chain)
        assert total / steps < 2.0  # the mean is below e - 1, about 1.72


def test_bad_window() -> None:
    with pytest.raises(ValueError):
        ChainSampler(0, random.Random(1))
