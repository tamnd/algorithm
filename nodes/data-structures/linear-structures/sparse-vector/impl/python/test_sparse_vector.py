# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-vector/. The authors are listed in prov/E8QPZ3.jsonl.

import math
import random

import pytest

from sparse_vector import SparseVector


def test_example() -> None:
    u = SparseVector(10, {1: 0.5, 4: 2.0, 7: -1.0})
    w = SparseVector(10, {0: 3.0, 4: 1.5, 7: 2.0, 9: 1.0})
    assert u.get(5) == 0
    assert u.dot(w) == 1.0 and w.dot(u) == 1.0
    assert dict(u.plus(w).items()) == {0: 3.0, 1: 0.5, 4: 3.5, 7: 1.0, 9: 1.0}
    z = SparseVector(10, {7: 1.0})
    s = u.plus(z)
    assert dict(s.items()) == {1: 0.5, 4: 2.0}
    s.check_invariant()
    assert math.isclose(u.norm(), 2.29128784747792)
    u.put(4, 0)
    assert dict(u.items()) == {1: 0.5, 7: -1.0}
    u.check_invariant()


def test_edges() -> None:
    e = SparseVector(0)
    assert e.nnz() == 0 and e.norm() == 0.0 and e.dot(SparseVector(0)) == 0.0
    v = SparseVector(3)
    with pytest.raises(IndexError):
        v.put(3, 1.0)
    with pytest.raises(IndexError):
        v.get(-1)
    with pytest.raises(ValueError):
        v.dot(SparseVector(4))
    with pytest.raises(ValueError):
        v.plus(SparseVector(4))
    with pytest.raises(ValueError):
        v.dot_dense([1.0, 2.0])
    v.put(0, 0)
    assert v.nnz() == 0
    v.put(2, 5.0)
    assert v.scale(0).nnz() == 0
    assert v.scale(-2).to_dense() == [0.0, 0.0, -10.0]
    assert v.dot_dense([1.0, 1.0, 3.0]) == 15.0


def test_random_against_dense() -> None:
    rng = random.Random(20261104)
    for _ in range(600):
        d = rng.randint(1, 40)
        u, w = SparseVector(d), SparseVector(d)
        du, dw = [0] * d, [0] * d
        for _ in range(rng.randint(0, 60)):
            vec, dense = (u, du) if rng.random() < 0.5 else (w, dw)
            i = rng.randrange(d)
            x = rng.choice([0, 0, rng.randint(-5, 5)])
            vec.put(i, x)
            dense[i] = x
            vec.check_invariant()
        assert u.to_dense() == du and w.to_dense() == dw
        assert u.nnz() == sum(1 for x in du if x != 0)
        assert u.dot(w) == sum(a * b for a, b in zip(du, dw))
        assert u.dot_dense(dw) == u.dot(w)
        r = u.plus(w)
        r.check_invariant()
        assert r.to_dense() == [a + b for a, b in zip(du, dw)]
        alpha = rng.randint(-3, 3)
        sc = u.scale(alpha)
        sc.check_invariant()
        assert sc.to_dense() == [alpha * a for a in du]
        assert math.isclose(u.norm(), math.sqrt(sum(a * a for a in du)))
        for i in range(d):
            assert u.get(i) == du[i]
