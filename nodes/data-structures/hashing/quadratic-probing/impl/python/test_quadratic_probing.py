# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quadratic-probing/. The authors are listed in prov/HV6EG1.jsonl.

import random

import pytest

from quadratic_probing import (
    DELETED,
    EMPTY,
    QuadraticProbingTable,
    qp_delete,
    qp_insert,
    qp_search,
)


def test_example() -> None:
    t: list[object] = [EMPTY] * 8
    slots = [qp_insert(t, k, k % 8) for k in (10, 18, 26, 34, 7, 15)]
    assert slots == [2, 3, 5, 0, 7, 1]
    assert t == [34, 15, 10, 18, EMPTY, 26, EMPTY, 7]
    assert qp_delete(t, 18, 18 % 8) == 3
    assert t[3] is DELETED
    assert qp_search(t, 26, 26 % 8) == 5
    assert qp_search(t, 42, 42 % 8) is None
    assert qp_insert(t, 42, 42 % 8) == 3
    assert t == [34, 15, 10, 42, EMPTY, 26, EMPTY, 7]


def test_offsets_cover_power_of_two() -> None:
    for p in range(0, 11):
        m = 1 << p
        assert sorted(i * (i + 1) // 2 % m for i in range(m)) == list(range(m))


def test_full_table_and_coverage() -> None:
    # all keys share one home slot, yet all 16 slots get filled
    t: list[object] = [EMPTY] * 16
    for k in range(16):
        qp_insert(t, k, 5)
    assert sorted(t) == list(range(16))  # type: ignore[type-var]
    with pytest.raises(OverflowError):
        qp_insert(t, 99, 5)
    for k in range(16):
        assert t[qp_search(t, k, 5)] == k  # type: ignore[index]
    assert qp_search(t, 99, 5) is None


def test_delete_keeps_later_keys_reachable() -> None:
    t: list[object] = [EMPTY] * 8
    for k in (10, 18, 26):
        qp_insert(t, k, 2)
    qp_delete(t, 10, 2)
    qp_delete(t, 18, 2)
    assert qp_search(t, 26, 2) == 5
    assert qp_delete(t, 99, 2) is None


def test_edges() -> None:
    q: QuadraticProbingTable[int, str] = QuadraticProbingTable(capacity=1)
    assert len(q) == 0 and q.get(3) is None and not q.delete(3)
    q.put(3, "a")
    q.put(3, "b")
    assert len(q) == 1 and q.get(3) == "b"
    assert q.delete(3) and 3 not in q
    q.check_invariant()
    with pytest.raises(ValueError):
        QuadraticProbingTable(capacity=6)


def test_no_duplicate_after_tombstone() -> None:
    q: QuadraticProbingTable[int, int] = QuadraticProbingTable(capacity=8, max_load=1.0, hash_fn=lambda k: 2)
    for k in (10, 18, 26):
        q.put(k, k)
    q.delete(10)
    q.put(26, 0)  # 26 lies past the tombstone; it must be updated, not added again
    assert len(q) == 2 and q.get(26) == 0
    q.check_invariant()


def test_random_against_dict() -> None:
    rng = random.Random(4107)
    for trial in range(500):
        bad_hash = trial % 3 == 0
        q: QuadraticProbingTable[int, int] = QuadraticProbingTable(
            capacity=1 << rng.randint(0, 3),
            max_load=rng.choice([0.5, 0.75, 1.0]),
            hash_fn=(lambda k: k % 3) if bad_hash else hash,
        )
        model: dict[int, int] = {}
        for _ in range(rng.randint(0, 80)):
            k = rng.randint(-20, 40)
            op = rng.random()
            if op < 0.5:
                v = rng.randint(0, 999)
                q.put(k, v)
                model[k] = v
            elif op < 0.75:
                assert q.delete(k) == (k in model)
                model.pop(k, None)
            else:
                assert q.get(k) == model.get(k)
            q.check_invariant()
            assert len(q) == len(model)
        assert sorted(q.items()) == sorted(model.items())
