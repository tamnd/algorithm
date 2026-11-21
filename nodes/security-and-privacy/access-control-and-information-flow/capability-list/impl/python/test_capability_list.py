# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/capability-list/. The authors are listed in prov/P22TZC.jsonl.

import itertools
import random

from capability_list import CapabilityList

SUBJECTS = ["alice", "bob", "carol"]
OBJECTS = ["f1", "f2", "p"]
RIGHTS = ["own", "r", "w"]

# The access matrix of the page example.
MATRIX = {
    ("alice", "f1"): frozenset({"own", "r", "w"}),
    ("alice", "f2"): frozenset({"r"}),
    ("bob", "f1"): frozenset({"r"}),
    ("bob", "f2"): frozenset({"own", "r", "w"}),
    ("bob", "p"): frozenset({"w"}),
    ("carol", "f2"): frozenset({"r"}),
    ("carol", "p"): frozenset({"w"}),
}


def build_example() -> tuple[CapabilityList, dict[str, int]]:
    c = CapabilityList()
    a1 = c.create("alice", "f1", {"own", "r", "w"})  # alice slot 0
    b2 = c.create("bob", "f2", {"own", "r", "w"})  # bob slot 0
    bp = c.create("bob", "p", {"w"})  # bob slot 1
    c.delegate("alice", a1, "bob", {"r"})  # bob slot 2
    c.delegate("bob", b2, "alice", {"r"})  # alice slot 1
    cr = c.delegate("bob", b2, "carol", {"r"})  # carol slot 0
    cp = c.delegate("bob", bp, "carol", {"w"})  # carol slot 1
    return c, {"a1": a1, "b2": b2, "bp": bp, "cr": cr, "cp": cp}


def test_page_example_rows() -> None:
    c, s = build_example()
    c.check_invariant()
    assert c.to_matrix() == MATRIX
    assert c.slots("carol") == [(0, "f2", frozenset({"r"})), (1, "p", frozenset({"w"}))]
    assert c.check("carol", 1, "p", "w")
    assert not c.check("carol", 0, "p", "w")  # slot 0 names f2, not p
    assert not c.check("carol", 0, "f2", "w")
    assert c.delegate("carol", 0, "alice", {"w"}) is None  # no amplification
    assert c.holders("f2") == ["alice", "bob", "carol"]


def test_page_example_revoke() -> None:
    c, s = build_example()
    d = c.delegate("carol", s["cr"], "alice", {"r"})  # alice slot 2, a copy of a copy
    assert d == 2
    assert c.revoke("bob", s["b2"]) == 4  # bob's f2, and the copies of alice, carol and alice
    c.check_invariant()
    assert c.slots("alice") == [(0, "f1", frozenset({"own", "r", "w"}))]
    assert c.slots("carol") == [(1, "p", frozenset({"w"}))]
    assert c.holders("f2") == []
    assert not c.check("alice", 2, "f2", "r")
    assert c.revoke("bob", s["b2"]) == 0


def test_edge_cases() -> None:
    c = CapabilityList()
    assert not c.check("alice", 0, "f1", "r")
    assert c.delegate("alice", 0, "bob", set()) is None
    assert c.revoke("alice", 0) == 0
    i = c.create("alice", "f1", set())
    assert c.slots("alice") == [(i, "f1", frozenset())]
    assert c.to_matrix() == {}
    j = c.create("alice", "f1", {"r"})
    k = c.delegate("alice", j, "alice", {"r"})
    assert c.rights("alice", "f1") == frozenset({"r"})
    assert c.revoke("alice", k) == 1
    assert c.check("alice", j, "f1", "r")
    assert c.create("alice", "f2", {"r"}) == 3  # slots are never reused
    c.check_invariant()


class Oracle:
    """Every capability ever made, with a flag for an explicit revoke."""

    def __init__(self) -> None:
        self.caps: list[dict] = []

    def live(self, k: int) -> bool:
        while k is not None:
            if self.caps[k]["revoked"]:
                return False
            k = self.caps[k]["parent"]
        return True

    def find(self, s: str, i: int) -> int | None:
        for k, cap in enumerate(self.caps):
            if cap["holder"] == s and cap["slot"] == i and self.live(k):
                return k
        return None

    def next_slot(self, s: str) -> int:
        return sum(1 for cap in self.caps if cap["holder"] == s)

    def add(self, s: str, o: str, rights: frozenset, parent: int | None) -> int:
        slot = self.next_slot(s)
        self.caps.append({"holder": s, "slot": slot, "obj": o, "rights": rights, "parent": parent, "revoked": False})
        return slot

    def matrix(self) -> dict:
        out: dict = {}
        for k, cap in enumerate(self.caps):
            if self.live(k) and cap["rights"]:
                key = (cap["holder"], cap["obj"])
                out[key] = out.get(key, frozenset()) | cap["rights"]
        return out


def random_rights(rng: random.Random) -> frozenset:
    return frozenset(r for r in RIGHTS if rng.random() < 0.5)


def test_random_operations_against_oracle() -> None:
    rng = random.Random(1966)
    for _ in range(600):
        c = CapabilityList()
        oracle = Oracle()
        for _ in range(rng.randint(0, 30)):
            op = rng.random()
            s, t, o = rng.choice(SUBJECTS), rng.choice(SUBJECTS), rng.choice(OBJECTS)
            i = rng.randint(0, 5)
            if op < 0.25:
                rights = random_rights(rng)
                assert c.create(s, o, rights) == oracle.add(s, o, rights, None)
            elif op < 0.6:
                rights = random_rights(rng)
                k = oracle.find(s, i)
                ok = k is not None and rights <= oracle.caps[k]["rights"]
                got = c.delegate(s, i, t, rights)
                if ok:
                    assert got == oracle.add(t, oracle.caps[k]["obj"], rights, k)
                else:
                    assert got is None
            elif op < 0.8:
                k = oracle.find(s, i)
                before = sum(1 for j in range(len(oracle.caps)) if oracle.live(j))
                if k is not None:
                    oracle.caps[k]["revoked"] = True
                after = sum(1 for j in range(len(oracle.caps)) if oracle.live(j))
                assert c.revoke(s, i) == before - after
            else:
                r = rng.choice(RIGHTS)
                k = oracle.find(s, i)
                want = k is not None and oracle.caps[k]["obj"] == o and r in oracle.caps[k]["rights"]
                assert c.check(s, i, o, r) == want
            c.check_invariant()
            assert c.to_matrix() == oracle.matrix()
        for s, i, o, r in itertools.product(SUBJECTS, range(6), OBJECTS, RIGHTS):
            k = oracle.find(s, i)
            want = k is not None and oracle.caps[k]["obj"] == o and r in oracle.caps[k]["rights"]
            assert c.check(s, i, o, r) == want
