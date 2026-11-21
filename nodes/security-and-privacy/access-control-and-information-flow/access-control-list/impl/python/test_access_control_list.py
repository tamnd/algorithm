# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/access-control-list/. The authors are listed in prov/443DQ0.jsonl.

import itertools
import random

from access_control_list import AccessControlList

SUBJECTS = ["alice", "bob", "carol"]
OBJECTS = ["f1", "f2", "p"]
RIGHTS = ["own", "r", "w"]

# The access matrix of the page example.
MATRIX = {
    ("alice", "f1"): {"own", "r", "w"},
    ("alice", "f2"): {"r"},
    ("bob", "f1"): {"r"},
    ("bob", "f2"): {"own", "r", "w"},
    ("bob", "p"): {"w"},
    ("carol", "f2"): {"r"},
    ("carol", "p"): {"w"},
}


def test_page_example_columns() -> None:
    acl = AccessControlList.from_matrix(MATRIX, OBJECTS)
    acl.check_invariant()
    assert acl.entries("f1") == [("alice", frozenset({"own", "r", "w"})), ("bob", frozenset({"r"}))]
    assert [s for s, _ in acl.entries("f2")] == ["alice", "bob", "carol"]
    assert acl.entries("p") == [("bob", frozenset({"w"})), ("carol", frozenset({"w"}))]
    assert acl.check("bob", "f2", "w")
    assert not acl.check("carol", "f2", "w")
    assert not acl.check("alice", "p", "w")


def test_page_example_sequence() -> None:
    acl = AccessControlList()
    acl.grant("bob", "f2", "own")
    acl.grant("bob", "f2", "r")
    acl.grant("bob", "f2", "w")
    acl.grant("alice", "f2", "r")
    acl.grant("carol", "f2", "r")
    assert acl.entries("f2") == [
        ("bob", frozenset({"own", "r", "w"})),
        ("alice", frozenset({"r"})),
        ("carol", frozenset({"r"})),
    ]
    assert not acl.check("carol", "f2", "w")
    acl.revoke("alice", "f2", "r")
    assert acl.entries("f2") == [("bob", frozenset({"own", "r", "w"})), ("carol", frozenset({"r"}))]
    acl.grant("carol", "p", "w")
    acl.revoke_subject("carol")
    assert acl.entries("f2") == [("bob", frozenset({"own", "r", "w"}))]
    assert acl.entries("p") == []
    assert acl.objects() == ["f2", "p"]
    acl.check_invariant()


def test_edge_cases() -> None:
    acl = AccessControlList()
    assert not acl.check("alice", "f1", "r")
    acl.revoke("alice", "f1", "r")
    acl.revoke_subject("alice")
    assert acl.to_matrix() == {}
    acl.create_object("f1")
    assert acl.entries("f1") == []
    acl.grant("alice", "f1", "r")
    acl.grant("alice", "f1", "r")
    assert acl.entries("f1") == [("alice", frozenset({"r"}))]
    acl.revoke("alice", "f1", "w")
    assert acl.rights("alice", "f1") == frozenset({"r"})
    acl.revoke("alice", "f1", "r")
    assert acl.entries("f1") == []
    acl.delete_object("f1")
    assert acl.objects() == []
    acl.check_invariant()


def test_round_trip_all_small_matrices() -> None:
    # Every matrix over 2 subjects, 2 objects and 2 rights: 4 cells, 4 values each.
    cells = list(itertools.product(SUBJECTS[:2], OBJECTS[:2]))
    values = [frozenset(c) for k in range(3) for c in itertools.combinations(RIGHTS[:2], k)]
    for choice in itertools.product(values, repeat=len(cells)):
        matrix = dict(zip(cells, choice))
        acl = AccessControlList.from_matrix(matrix, OBJECTS[:2])
        acl.check_invariant()
        assert acl.to_matrix() == {c: v for c, v in matrix.items() if v}
        for (s, o), v in matrix.items():
            for r in RIGHTS[:2]:
                assert acl.check(s, o, r) == (r in v)


def test_random_operations_against_matrix() -> None:
    rng = random.Random(20251121)
    for _ in range(600):
        acl = AccessControlList()
        model: dict[tuple[str, str], set[str]] = {}
        live: set[str] = set()
        for _ in range(rng.randint(0, 40)):
            op = rng.random()
            s, o, r = rng.choice(SUBJECTS), rng.choice(OBJECTS), rng.choice(RIGHTS)
            if op < 0.4:
                acl.grant(s, o, r)
                model.setdefault((s, o), set()).add(r)
                live.add(o)
            elif op < 0.7:
                acl.revoke(s, o, r)
                model.get((s, o), set()).discard(r)
            elif op < 0.8:
                acl.revoke_subject(s)
                for key in list(model):
                    if key[0] == s:
                        model[key] = set()
            elif op < 0.85:
                acl.delete_object(o)
                live.discard(o)
                for key in list(model):
                    if key[1] == o:
                        model[key] = set()
            else:
                assert acl.check(s, o, r) == (r in model.get((s, o), set()))
            acl.check_invariant()
            expected = {k: frozenset(v) for k, v in model.items() if v}
            assert acl.to_matrix() == expected
            assert set(acl.objects()) == live
        for s, o, r in itertools.product(SUBJECTS, OBJECTS, RIGHTS):
            assert acl.check(s, o, r) == (r in model.get((s, o), set()))
            assert acl.rights(s, o) == frozenset(model.get((s, o), set()))
