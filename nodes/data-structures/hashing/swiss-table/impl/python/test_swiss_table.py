# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/swiss-table/. The authors are listed in prov/5PH332.jsonl.

import random

from swiss_table import DELETED, EMPTY, SwissTable, max_fill


def ident(k: int) -> int:
    return k


def layout(t: SwissTable) -> list:
    c = t.ctrl()
    return ["." if x == EMPTY else "D" if x == DELETED else t._keys[s] for s, x in enumerate(c)]


def test_page_example() -> None:
    t = SwissTable(group_width=4, groups=4, hash_fn=ident)
    for k in [3, 7, 131, 11, 15, 19, 23, 27]:
        t.insert(k, -k)
        t.check_invariant()
    assert layout(t) == [3, 7, 11, 15, 131, 19, 23, 27] + ["."] * 8
    assert t.ctrl()[:8] == [3, 7, 11, 15, 3, 19, 23, 27]
    assert t.find(27) == 7 and t.get(27) == -27
    assert t.find(259) is None  # start group 2 holds an EMPTY slot
    assert t.find(1027) is None  # H2 = 3 matches 3 and 131, then group 3 stops it
    assert t.erase(7)
    assert layout(t)[:4] == [3, "D", 11, 15]
    assert t.find(27) == 7  # the tombstone keeps group 0 "full"
    assert t.erase(27)
    assert layout(t)[4:8] == [131, 19, 23, "D"]
    t.insert(35, -35)
    assert layout(t)[:4] == [3, 35, 11, 15]
    assert len(t) == 7 and t._dead == 1
    t.check_invariant()


def test_erase_to_empty_when_group_has_empty() -> None:
    t = SwissTable(group_width=4, groups=4, hash_fn=ident)
    for k in [3, 7]:
        t.insert(k, k)
    assert t.erase(3)
    assert t.ctrl()[0] == EMPTY and t._dead == 0
    assert 7 in t and 3 not in t
    t.check_invariant()


def test_edges() -> None:
    t = SwissTable(group_width=1, groups=1, hash_fn=ident)
    assert len(t) == 0 and t.find(5) is None and not t.erase(5)
    assert t.get(5, "x") == "x"
    t.insert(5, "a")
    t.insert(5, "b")
    assert len(t) == 1 and t.get(5) == "b"
    t.check_invariant()
    for bad in [(0, 1), (4, 3), (4, 0)]:
        try:
            SwissTable(group_width=bad[0], groups=bad[1])
        except ValueError:
            pass
        else:
            raise AssertionError(bad)
    assert max_fill(16) == 14 and max_fill(4) == 3 and max_fill(1) == 0


def test_all_keys_one_group_start() -> None:
    # Every key has the same H1, so they spread over all groups in probe order.
    t = SwissTable(group_width=2, groups=8, hash_fn=lambda k: k & 0x7F)
    for k in range(13):
        t.insert(k, k)
        t.check_invariant()
    for k in range(13):
        assert t.get(k) == k
    assert t.capacity == 16


def test_tombstones_force_rebuild_not_growth() -> None:
    t = SwissTable(group_width=4, groups=4, hash_fn=ident)
    for k in [128 * i for i in range(4)]:  # H1 = i, H2 = 0
        t.insert(k, k)
    cap = t.capacity
    for r in range(200):
        k = 10_000 + r
        t.insert(k, k)
        t.erase(k)
        t.check_invariant()
    assert t.capacity == cap and len(t) == 4


def test_random_against_dict() -> None:
    rng = random.Random(2017)
    for case in range(600):
        w = rng.choice([1, 2, 4, 8, 16])
        t: SwissTable = SwissTable(group_width=w, groups=1, hash_fn=(ident if case % 2 else hash))
        ref: dict = {}
        for _ in range(rng.randint(0, 80)):
            k = rng.randrange(60) * rng.choice([1, 128])
            op = rng.random()
            if op < 0.5:
                t.insert(k, case)
                ref[k] = case
            elif op < 0.8:
                assert t.erase(k) == (k in ref)
                ref.pop(k, None)
            else:
                assert t.get(k) == ref.get(k)
            t.check_invariant()
        assert sorted(t.items()) == sorted(ref.items())
