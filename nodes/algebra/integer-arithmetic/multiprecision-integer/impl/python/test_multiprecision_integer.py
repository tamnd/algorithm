# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiprecision-integer/. The authors are listed in prov/WZN2G1.jsonl.

import random

import pytest

from multiprecision_integer import MultiprecisionInteger as MP


def mp(x: int, w: int = 4) -> MP:
    return MP.from_int(x, w)


def test_example() -> None:
    x = MP.from_limbs(False, [13, 15, 15], 4)
    assert x.to_int() == 4093
    y = mp(3)
    s = x.add(y)
    assert s.limbs == [0, 0, 0, 1] and s.to_int() == 4096
    d = x.add(mp(-4096))
    assert d.neg and d.limbs == [3] and d.to_int() == -3
    d.check_invariant()


def test_zero_and_one() -> None:
    z = MP(4)
    assert z.limbs == [] and not z.neg and z.to_int() == 0
    one = mp(1)
    assert one.sub(one).limbs == [] and not one.sub(one).neg
    assert mp(-5).add(mp(5)).to_int() == 0 and not mp(-5).add(mp(5)).neg
    assert mp(-5).mul(MP(4)).to_int() == 0 and not mp(-5).mul(MP(4)).neg
    assert z.neg_().to_int() == 0 and not z.neg_().neg
    assert MP.from_limbs(True, [0, 0], 4).to_int() == 0
    assert not MP.from_limbs(True, [0, 0], 4).neg
    assert one.mul(mp(-7)).to_int() == -7


def test_all_limbs_max() -> None:
    for w in (1, 4, 8):
        base = 1 << w
        for n in range(1, 7):
            top = base**n - 1
            x = MP.from_limbs(False, [base - 1] * n, w)
            assert x.to_int() == top
            assert x.add(mp(1, w)).limbs == [0] * n + [1]
            assert x.mul(x).to_int() == top * top
            assert x.add(x).to_int() == 2 * top
            assert mp(base**n, w).sub(mp(1, w)).limbs == [base - 1] * n


def test_compare() -> None:
    vals = [-300, -256, -255, -16, -1, 0, 1, 15, 16, 255, 4096]
    for a in vals:
        for b in vals:
            want = (a > b) - (a < b)
            assert mp(a).compare(mp(b)) == want


def test_divmod_limb() -> None:
    q, r = mp(4093).divmod_limb(10)
    assert (q.to_int(), r) == (409, 3)
    q, r = mp(-4093).divmod_limb(10)
    assert (q.to_int(), r) == (-409, 3)
    q, r = mp(5).divmod_limb(7)
    assert q.limbs == [] and r == 5
    with pytest.raises(ValueError):
        mp(5).divmod_limb(16)
    with pytest.raises(ValueError):
        mp(5).divmod_limb(0)


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        MP.from_limbs(False, [16], 4)
    with pytest.raises(ValueError):
        mp(1, 4).add(mp(1, 8))
    with pytest.raises(ValueError):
        MP(0)


def rand_value(rng: random.Random, w: int) -> int:
    kind = rng.randrange(5)
    n = rng.randint(0, 12)
    if kind == 0:
        v = (1 << (w * n)) - 1
    elif kind == 1:
        v = 1 << (w * n)
    else:
        v = rng.getrandbits(w * n) if n else 0
    return -v if rng.random() < 0.5 else v


def test_random_against_int() -> None:
    rng = random.Random(2026)
    for _ in range(2000):
        w = rng.choice((1, 2, 4, 8))
        a, b = rand_value(rng, w), rand_value(rng, w)
        x, y = mp(a, w), mp(b, w)
        for r, want in ((x.add(y), a + b), (x.sub(y), a - b), (x.mul(y), a * b), (x.neg_(), -a)):
            r.check_invariant()
            assert r.to_int() == want
        assert x.compare(y) == (a > b) - (a < b)
        d = rng.randrange(1, 1 << w)
        q, r = x.divmod_limb(d)
        q.check_invariant()
        assert abs(a) == abs(q.to_int()) * d + r and 0 <= r < d
        assert q.to_int() == 0 or (q.to_int() < 0) == (a < 0)


def test_random_sequences() -> None:
    rng = random.Random(77)
    for _ in range(200):
        w = rng.choice((4, 8))
        x, v = MP(w), 0
        for _ in range(30):
            b = rand_value(rng, w) // (rng.randint(1, 3))
            op = rng.randrange(3)
            if op == 0:
                x, v = x.add(mp(b, w)), v + b
            elif op == 1:
                x, v = x.sub(mp(b, w)), v - b
            elif abs(v) < 1 << 200:
                x, v = x.mul(mp(b % 1000 - 500, w)), v * (b % 1000 - 500)
            x.check_invariant()
            assert x.to_int() == v
