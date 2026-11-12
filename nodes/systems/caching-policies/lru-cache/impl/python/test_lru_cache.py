# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lru-cache/. The authors are listed in prov/DKPAX9.jsonl.

import random

from lru_cache import LRUCache


class NaiveLRU:
    """Reference: a plain list of [key, value] pairs, most recently used first."""

    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def _find(self, key):
        for i, (k, _) in enumerate(self.items):
            if k == key:
                return i
        return -1

    def get(self, key, default=None):
        i = self._find(key)
        if i < 0:
            return default
        pair = self.items.pop(i)
        self.items.insert(0, pair)
        return pair[1]

    def put(self, key, value):
        i = self._find(key)
        if i >= 0:
            self.items.pop(i)
            self.items.insert(0, (key, value))
            return None
        evicted = None
        if len(self.items) == self.capacity:
            evicted = self.items.pop()
        self.items.insert(0, (key, value))
        return evicted

    def delete(self, key):
        i = self._find(key)
        if i < 0:
            return False
        self.items.pop(i)
        return True


def check_links(c):
    """The list is a consistent circle and holds exactly the keys of the map."""
    seen = []
    x = c.head.next
    while x is not c.head:
        assert x.next.prev is x and x.prev.next is x
        assert c.map[x.key] is x
        seen.append(x.key)
        x = x.next
    assert len(seen) == len(c.map) <= c.capacity
    assert len(set(seen)) == len(seen)


def test_example():
    c = LRUCache(2)
    assert c.put("a", 1) is None
    assert c.put("b", 2) is None
    assert c.get("a") == 1
    assert c.put("c", 3) == ("b", 2)
    assert c.get("b") is None
    assert c.put("a", 10) is None
    assert c.put("d", 4) == ("c", 3)
    assert c.keys_mru_first() == ["d", "a"]
    assert c.get("a") == 10


def test_page_example():
    c = LRUCache(3)
    log = []
    for op in [("put", 1, "x"), ("put", 2, "y"), ("put", 3, "z"), ("get", 1), ("put", 4, "w"),
               ("get", 2), ("get", 3), ("put", 1, "v"), ("put", 5, "u")]:
        if op[0] == "put":
            log.append(c.put(op[1], op[2]))
        else:
            log.append(c.get(op[1]))
        check_links(c)
    assert log == [None, None, None, "x", (2, "y"), None, "z", None, (4, "w")]
    assert c.keys_mru_first() == [5, 1, 3]


def test_against_naive():
    rng = random.Random(7)
    for _ in range(200):
        cap = rng.randint(1, 5)
        c, ref = LRUCache(cap), NaiveLRU(cap)
        for _ in range(rng.randint(0, 80)):
            key = rng.randrange(8)
            r = rng.random()
            if r < 0.45:
                assert c.get(key) == ref.get(key)
            elif r < 0.9:
                v = rng.randrange(100)
                assert c.put(key, v) == ref.put(key, v)
            else:
                assert c.delete(key) == ref.delete(key)
            check_links(c)
            assert c.keys_mru_first() == [k for k, _ in ref.items]


def test_get_missing_does_not_change_order():
    c = LRUCache(3)
    for k in "abc":
        c.put(k, k)
    assert c.get("z", 0) == 0
    assert c.keys_mru_first() == ["c", "b", "a"]


def test_capacity_one():
    c = LRUCache(1)
    assert c.put(1, 1) is None
    assert c.put(2, 2) == (1, 1)
    assert c.get(1) is None and c.get(2) == 2
    assert len(c) == 1


def test_bad_capacity():
    try:
        LRUCache(0)
    except ValueError:
        return
    raise AssertionError("capacity 0 must be rejected")
