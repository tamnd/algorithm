# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-probing/. The authors are listed in prov/J1RWHQ.jsonl.

import random

from linear_probing import LinearProbingTable


def mod_home(k: int, m: int) -> int:
    return k % m


def table_of_page() -> LinearProbingTable[int, str]:
    t: LinearProbingTable[int, str] = LinearProbingTable(16, mod_home)
    for k in (18, 34, 50, 20, 31, 47, 15):
        t.insert(k, str(k))
        t.check_invariant()
    return t


def test_example() -> None:
    t = table_of_page()
    s = t.slots()
    assert s == [47, 15, 18, 34, 50, 20] + [None] * 9 + [31]
    assert t.search(50) == 4 and t.search(66) is None
    assert t.delete(18)
    t.check_invariant()
    assert t.slots() == [47, 15, 34, 50, 20] + [None] * 10 + [31]
    assert t.delete(31)
    t.check_invariant()
    assert t.slots() == [15, None, 34, 50, 20] + [None] * 10 + [47]


def test_edges() -> None:
    t: LinearProbingTable[int, int] = LinearProbingTable(2, mod_home)
    assert t.search(0) is None and not t.delete(0) and len(t) == 0
    t.insert(5, 1)
    t.insert(5, 2)
    assert len(t) == 1 and t.get(5) == 2
    assert t.delete(5) and len(t) == 0 and 5 not in t
    t.check_invariant()
    # all keys share one home slot
    u: LinearProbingTable[int, int] = LinearProbingTable(64, lambda k, m: 7)
    for k in range(20):
        u.insert(k, k)
        u.check_invariant()
    for k in range(0, 20, 2):
        assert u.delete(k)
        u.check_invariant()
    assert sorted(k for k, _ in u.items()) == list(range(1, 20, 2))
    # large 64-bit keys
    w: LinearProbingTable[int, int] = LinearProbingTable()
    big = [2**63 - 1, -(2**63), 2**64 + 3]
    for k in big:
        w.insert(k, k)
    assert all(w.get(k) == k for k in big)


def test_wraparound_delete() -> None:
    t: LinearProbingTable[int, int] = LinearProbingTable(8, mod_home)
    for k in (7, 15, 23):  # slots 7, 0, 1
        t.insert(k, 0)
    assert t.slots()[7] == 7 and t.slots()[0] == 15 and t.slots()[1] == 23
    t.delete(7)
    t.check_invariant()
    assert t.slots()[7] == 15 and t.slots()[0] == 23 and t.slots()[1] is None


def test_random_against_dict() -> None:
    rng = random.Random(4127)
    for trial in range(500):
        mod = rng.randint(1, 12)
        t: LinearProbingTable[int, int] = LinearProbingTable(rng.choice([2, 4, 8]), lambda k, m, mod=mod: (k % mod) * 3 + k // 7)
        oracle: dict[int, int] = {}
        for _ in range(rng.randint(0, 80)):
            k = rng.randint(-20, 40)
            op = rng.random()
            if op < 0.5:
                v = rng.randint(0, 999)
                t.insert(k, v)
                oracle[k] = v
            elif op < 0.8:
                assert t.delete(k) == (k in oracle)
                oracle.pop(k, None)
            else:
                assert t.get(k) == oracle.get(k)
            t.check_invariant()
            assert len(t) == len(oracle)
        assert dict(t.items()) == oracle
