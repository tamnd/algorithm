# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ttl-expiration/. The authors are listed in prov/WFW1C7.jsonl.

import math
import random
from fractions import Fraction

from ttl_expiration import TTLCache, hit_probability, simulate_hit_ratio


class NaiveTTL:
    """Reference: a dict of (value, expiry, ttl), expiry checked by a full scan."""

    def __init__(self, sliding=False):
        self.sliding = sliding
        self.d = {}

    def set(self, key, value, now, ttl):
        if ttl <= 0:
            self.d.pop(key, None)
        else:
            self.d[key] = (value, now + ttl, ttl)

    def get(self, key, now):
        if key not in self.d or now >= self.d[key][1]:
            self.d.pop(key, None)
            return None
        v, _, ttl = self.d[key]
        if self.sliding:
            self.d[key] = (v, now + ttl, ttl)
        return v

    def sweep(self, now):
        dead = [k for k, e in self.d.items() if e[1] <= now]
        for k in dead:
            del self.d[k]
        return len(dead)


def test_absolute_and_sliding_by_hand():
    c = TTLCache()
    c.set("a", 1, now=0, ttl=10)
    assert c.get("a", 9) == 1 and c.get("a", 10) is None  # live on [0, 10)
    s = TTLCache(sliding=True)
    s.set("a", 1, now=0, ttl=10)
    for t in (9, 18, 27):
        assert s.get("a", t) == 1  # each hit moves the expiry to t + 10
    assert s.get("a", 37) is None


def test_lazy_expiry_keeps_memory_until_access_or_sweep():
    c = TTLCache()
    for i in range(5):
        c.set(i, i, now=0, ttl=1 + i)
    assert c.stored() == 5
    assert c.get(0, 3) is None and c.stored() == 4  # removed lazily
    assert c.sweep(3) == 2 and c.stored() == 2  # keys 1 and 2 expire at 2 and 3
    assert c.sweep(100) == 2 and c.stored() == 0


def test_matches_naive_reference():
    for seed in range(40):
        rng = random.Random(seed)
        sliding = seed % 2 == 1
        c, ref = TTLCache(sliding), NaiveTTL(sliding)
        now = Fraction(0)
        for _ in range(400):
            now += Fraction(rng.randrange(0, 4), 2)
            key = rng.randrange(12)
            op = rng.random()
            if op < 0.35:
                ttl = Fraction(rng.randrange(0, 12), 2)
                c.set(key, (seed, now), now, ttl)
                ref.set(key, (seed, now), now, ttl)
            elif op < 0.85:
                assert c.get(key, now) == ref.get(key, now)
            elif op < 0.95:
                assert c.sweep(now) == ref.sweep(now)
                assert set(c.data) == set(ref.d)
            else:
                c.delete(key)
                ref.d.pop(key, None)
            live = {k for k in range(12) if c.contains(k, now)}
            assert live == {k for k, e in ref.d.items() if now < e[1]}
            assert len(c.heap) <= 2 * len(c.data) + 17


def test_sweep_removes_in_expiry_order_and_skips_old_items():
    c = TTLCache()
    c.set("a", 1, 0, 5)
    c.set("a", 2, 0, 50)  # overwrite: the item with expiry 5 is old
    c.set("b", 3, 0, 7)
    assert c.sweep(10) == 1 and set(c.data) == {"a"}
    assert c.get("a", 10) == 2


def test_hit_probability_formulas():
    assert hit_probability(2, 1.5) == 0.75
    assert math.isclose(hit_probability(2, 1.5, sliding=True), 1 - math.exp(-3))
    for x in (0.1, 0.5, 1, 3, 10):
        assert hit_probability(x, 1, sliding=True) >= hit_probability(x, 1)


def test_hit_probability_by_simulation():
    rng = random.Random(2003)
    for lam, ttl in ((2.0, 1.5), (1.0, 1.0), (0.2, 2.0)):
        n = 120000
        p = hit_probability(lam, ttl)
        sim = simulate_hit_ratio(lam, ttl, n, rng)
        assert abs(sim - p) < 0.006, (lam, ttl, sim, p)
        q = hit_probability(lam, ttl, sliding=True)
        sim = simulate_hit_ratio(lam, ttl, n, rng, sliding=True)
        assert abs(sim - q) < 0.006, (lam, ttl, sim, q)
