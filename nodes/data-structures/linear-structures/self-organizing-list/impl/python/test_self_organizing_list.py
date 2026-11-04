# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/self-organizing-list/. The authors are listed in prov/2WXV0M.jsonl.

import random

import pytest

from self_organizing_list import SelfOrganizingList


def build(rule: str, keys: str) -> SelfOrganizingList[str, int]:
    lst: SelfOrganizingList[str, int] = SelfOrganizingList(rule)
    for v, k in enumerate(keys):
        lst.put(k, v)
    if rule == "mtf":  # new keys go to the front; rebuild the order a, b, c, ...
        lst = SelfOrganizingList(rule)
        for v, k in reversed(list(enumerate(keys))):
            lst.put(k, v)
    return lst


def positions(lst: SelfOrganizingList[str, int], reqs: str) -> list[int]:
    out = []
    for k in reqs:
        out.append(list(lst.keys()).index(k) + 1)
        lst.get(k)
        lst.check_invariant()
    return out


def test_example() -> None:
    m = build("mtf", "abcde")
    assert list(m.keys()) == list("abcde")
    assert sum(positions(m, "dbdeadb")) == 25 and "".join(m.keys()) == "bdaec"
    t = build("transpose", "abcde")
    assert positions(t, "dbdeadb") == [4, 2, 3, 5, 3, 3, 1] and "".join(t.keys()) == "bdaec"
    c = build("count", "abcde")
    assert positions(c, "dbdeadb") == [4, 3, 1, 5, 4, 1, 2]
    assert "".join(c.keys()) == "dbeac" and c.counts() == [4, 3, 2, 2, 1]
    t2 = build("transpose", "abcde")
    assert sum(positions(t2, "ed" * 5)) == 50
    m2 = build("mtf", "abcde")
    assert sum(positions(m2, "ed" * 5)) == 26


def test_edges() -> None:
    for rule in ("mtf", "transpose", "count"):
        lst: SelfOrganizingList[int, str] = SelfOrganizingList(rule)
        assert lst.get(1) is None and len(lst) == 0
        lst.delete(1)
        lst.put(1, "x")
        assert lst.get(1) == "x" and lst.get(2) is None
        lst.put(1, "y")
        assert lst.get(1) == "y" and len(lst) == 1
        lst.delete(1)
        assert len(lst) == 0 and list(lst.keys()) == []
        lst.check_invariant()
    with pytest.raises(ValueError):
        SelfOrganizingList("random")


def model_access(rule: str, order: list[list], k: int) -> None:
    """Independent model: a Python list of [key, count] pairs."""
    i = [e[0] for e in order].index(k)
    e = order.pop(i)
    if rule == "mtf":
        order.insert(0, e)
    elif rule == "transpose":
        order.insert(max(i - 1, 0), e)
    else:
        e[1] += 1
        j = 0
        while j < len(order) and order[j][1] >= e[1]:
            j += 1
        order.insert(j, e)


def test_random_against_model() -> None:
    rng = random.Random(1976)
    for trial in range(600):
        rule = ("mtf", "transpose", "count")[trial % 3]
        lst: SelfOrganizingList[int, int] = SelfOrganizingList(rule)
        values: dict[int, int] = {}
        order: list[list] = []
        for _ in range(rng.randint(0, 40)):
            op, k = rng.random(), rng.randrange(8)
            if op < 0.5:
                assert lst.get(k) == values.get(k)
                if k in values:
                    model_access(rule, order, k)
            elif op < 0.85:
                v = rng.randrange(100)
                lst.put(k, v)
                if k in values:
                    model_access(rule, order, k)
                elif rule == "mtf":
                    order.insert(0, [k, 1])
                else:
                    order.append([k, 1])
                values[k] = v
            else:
                lst.delete(k)
                if k in values:
                    del values[k]
                    order = [e for e in order if e[0] != k]
            lst.check_invariant()
            assert list(lst.keys()) == [e[0] for e in order]
            assert len(lst) == len(values)
            if rule == "count":
                assert lst.counts() == [e[1] for e in order]
