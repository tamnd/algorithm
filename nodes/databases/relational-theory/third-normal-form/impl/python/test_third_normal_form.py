# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/third-normal-form/. The authors are listed in prov/SA5P36.jsonl.

import random

from third_normal_form import closure, fd, is_3nf, is_3nf_by_definition, is_bcnf, keys, subsets, violations


def names(xs: list) -> list[str]:
    return sorted("".join(sorted(x)) for x in xs)


def test_city_street_zip() -> None:
    f = [fd("CS", "Z"), fd("Z", "C")]
    assert names(keys("CSZ", f)) == ["CS", "SZ"]
    assert is_3nf("CSZ", f) and is_3nf_by_definition("CSZ", f)
    assert not is_bcnf("CSZ", f)


def test_transitive_dependency() -> None:
    # Employee, Dept, Dept name: E -> D, D -> N.
    f = [fd("E", "D"), fd("D", "N")]
    assert violations("EDN", f) == [(frozenset("D"), "N")]
    assert not is_3nf("EDN", f)
    assert is_3nf("ED", [fd("E", "D")]) and is_3nf("DN", [fd("D", "N")])


def test_partial_dependency() -> None:
    # Student, Course, Grade, student Name: SC -> G, S -> N violates 2NF and so 3NF.
    f = [fd("SC", "G"), fd("S", "N")]
    assert names(keys("SCGN", f)) == ["CS"]
    assert violations("SCGN", f) == [(frozenset("S"), "N")]


def test_course_schema() -> None:
    f = [fd("C", "T"), fd("HR", "C"), fd("HT", "R"), fd("CS", "G"), fd("HS", "R")]
    assert names(keys("CTHRSG", f)) == ["HS"]
    got = sorted(("".join(sorted(x)), a) for x, a in violations("CTHRSG", f))
    assert got == [("C", "T"), ("CS", "G"), ("HR", "C"), ("HT", "R")]


def test_edges() -> None:
    assert is_3nf("AB", []) and is_bcnf("AB", [])
    assert is_3nf("A", [fd("", "A")])
    assert is_3nf("AB", [fd("A", "B"), fd("B", "A")]) and is_bcnf("AB", [fd("A", "B"), fd("B", "A")])


def test_random_against_definition() -> None:
    rng = random.Random(4)
    attrs = "ABCDE"
    for _ in range(400):
        f = [fd(rng.sample(attrs, rng.randint(0, 2)), rng.sample(attrs, rng.randint(1, 2))) for _ in range(rng.randint(0, 5))]
        three = is_3nf(attrs, f)
        assert three == is_3nf_by_definition(attrs, f)
        bcnf = is_bcnf(attrs, f)
        u = frozenset(attrs)
        assert bcnf == all(closure(f, x) == x or closure(f, x) >= u for x in subsets(attrs))
        if bcnf:
            assert three
