# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/type-based-alias-analysis/. The authors are listed in prov/FMJ8XA.jsonl.

import random

import ptsgen
from type_based_alias_analysis import (
    Program,
    field_type_decl,
    may_alias_pairs,
    random_program,
    run,
    sm_type_refs,
    type_decl,
    type_refs,
)

METHODS = [type_decl, field_type_decl, sm_type_refs]

PAGE = Program(
    {"Object": None, "A": "Object", "B": "Object", "A1": "A", "A2": "A"},
    {"next": ("A", "A"), "val": ("Object", "Object")},
    {"x": "A1", "y": "A2", "a": "A", "o": "Object", "t": "A"},
    [
        ("new", "x", "A1"),  # 0
        ("new", "y", "A2"),  # 1
        ("copy", "a", "y"),  # 2
        ("store", "x", "next", "a"),  # 3: x.next = a
        ("store", "y", "next", "a"),  # 4: y.next = a
        ("new", "o", "B"),  # 5
        ("store", "o", "val", "o"),  # 6: o.val = o
        ("load", "t", "a", "next"),  # 7: t = a.next
    ],
)


def test_page_example():
    PAGE.check()
    refs = type_refs(PAGE)
    assert refs["A"] == {"A", "A2"} and refs["A1"] == {"A1"}
    assert refs["Object"] == {"Object", "B"}
    r = {i: (i, q, f) for i, q, f in PAGE.references()}
    other = [(3, 4), (3, 7), (4, 7), (3, 6), (4, 6), (6, 7)]

    def answers(method):
        return [(i, j) for i, j in other if method(PAGE, r[i], r[j])]

    assert answers(type_decl) == other
    assert answers(field_type_decl) == [(3, 7), (4, 7)]
    assert answers(sm_type_refs) == [(4, 7)]
    # The run agrees: y.next and a.next touch one object, as a = y.
    touched, _ = run(PAGE, random.Random(1), runs=30, steps=40)
    assert (4, 7) in touched and (3, 7) not in touched and (3, 4) not in touched


def rejected(stmt):
    try:
        Program(PAGE.parent, PAGE.fields, PAGE.types, [stmt]).check()
    except TypeError:
        return True
    return False


def test_ill_typed_programs_are_rejected():
    assert rejected(("copy", "x", "a"))  # a downcast from A to A1
    assert rejected(("load", "t", "o", "next"))  # Object has no field next
    assert not rejected(("copy", "a", "x"))  # an upcast is fine


def test_each_method_refines_the_one_before():
    rng = random.Random(7100)
    for trial in range(200):
        prog = random_program(rng, rng.randint(3, 10), 30)
        td, ftd, sm = (may_alias_pairs(prog, m) for m in METHODS)
        assert sm <= ftd <= td


def test_sound_against_concrete_runs():
    rng = random.Random(7200)
    for trial in range(200):
        prog = random_program(rng, rng.randint(3, 10), 30)
        touched, seen_types = run(prog, rng, runs=15, steps=100)
        refs = type_refs(prog)
        for m in METHODS:
            assert touched <= may_alias_pairs(prog, m), (m.__name__, prog.stmts)
        # Every dynamic class that a variable held is in TypeRefs of its type.
        for v, c in seen_types:
            assert c in refs[prog.types[v]]


def test_runs_do_find_aliases():
    rng = random.Random(7300)
    found = 0
    for trial in range(100):
        prog = random_program(rng, 4, 30)
        touched, _ = run(prog, rng, runs=10, steps=100)
        found += sum(1 for i, j in touched if i != j)
    assert found > 100


def to_points_to(prog):
    """The program in the four forms of ptsgen, with one location per
    allocation site and one location F_f for each field f, shared by all
    objects (a field-based model)."""
    out = []
    for i, s in enumerate(prog.stmts):
        if s[0] == "new":
            out.append(("addr", s[1], "site%d" % i))
        elif s[0] == "copy":
            out.append(("copy", s[1], s[2]))
        elif s[0] == "load":
            out.append(("copy", s[1], "F_" + s[3]))
        else:
            out.append(("copy", "F_" + s[2], s[3]))
    return out


def test_points_to_analysis_is_at_least_as_precise():
    # If Andersen's analysis says that the bases of two references with the
    # same field may point to one object, SMTypeRefs says so too.
    rng = random.Random(7400)
    for trial in range(200):
        prog = random_program(rng, rng.randint(3, 10), 30)
        pts = ptsgen.least_solution(to_points_to(prog))
        sm = may_alias_pairs(prog, sm_type_refs)
        rs = prog.references()
        for a in range(len(rs)):
            for b in range(a, len(rs)):
                (i, q1, f1), (j, q2, f2) = rs[a], rs[b]
                if f1 == f2 and pts.get(q1, set()) & pts.get(q2, set()):
                    assert (i, j) in sm
