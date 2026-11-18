# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conditional-functional-dependency/. The authors are listed in prov/CYNKMP.jsonl.

import itertools
import random

from conditional_functional_dependency import WILD, from_fd, satisfies, violations, violations_brute

# Attributes: 0 CC, 1 AC, 2 PN, 3 NM, 4 STR, 5 CT, 6 ZIP.
CUST = [
    ("01", "908", "1111111", "Mike", "Tree Ave.", "MH", "07974"),
    ("01", "908", "1111111", "Rick", "Tree Ave.", "NYC", "07974"),
    ("01", "212", "2222222", "Joe", "Elm Str.", "NYC", "01202"),
    ("01", "212", "2222222", "Jim", "Elm Str.", "NYC", "02404"),
    ("44", "131", "3333333", "Ben", "High St.", "EDI", "EH4 1DT"),
]
PHI = (
    [0, 1, 2],
    [4, 5, 6],
    [
        ((WILD, WILD, WILD), (WILD, WILD, WILD)),
        (("01", "908", WILD), (WILD, "MH", WILD)),
        (("01", "212", WILD), (WILD, "NYC", WILD)),
    ],
)
AREA_CODE_CITY = ([0, 1], [5], [(("01", "908"), ("MH",)), (("01", "212"), ("NYC",))])


def test_customer_example():
    assert violations(CUST, PHI) == {0, 1, 2, 3}
    # The plain dependency CC, AC -> CT holds on Rick alone; the pattern does not.
    assert violations([CUST[1]], AREA_CODE_CITY) == {0}
    assert violations([CUST[1]], from_fd([0, 1], [5])) == set()
    assert violations([CUST[0], CUST[2], CUST[4]], AREA_CODE_CITY) == set()


def test_unsatisfiable_tableau():
    # ([A] -> [B], {(_, b), (_, c)}): every row breaks one of the two patterns.
    cfd = ([0], [1], [((WILD,), ("b",)), ((WILD,), ("c",))])
    for row in itertools.product("abc", repeat=2):
        assert violations([row], cfd) == {0}


def fd_holds(rows, xs, ys):
    return all(
        any(s[a] != t[a] for a in xs) or all(s[b] == t[b] for b in ys)
        for s, t in itertools.product(rows, repeat=2)
    )


def random_cfd(rng, nattrs):
    attrs = list(range(nattrs))
    rng.shuffle(attrs)
    k = rng.randint(1, nattrs - 1)
    xs, ys = attrs[:k], attrs[k:][: rng.randint(1, nattrs - k)]
    tableau = []
    for _ in range(rng.randint(1, 3)):
        px = tuple(rng.choice([WILD, WILD, 0, 1]) for _ in xs)
        py = tuple(rng.choice([WILD, WILD, 0, 1]) for _ in ys)
        tableau.append((px, py))
    return xs, ys, tableau


def test_against_brute_force_over_pairs():
    rng = random.Random(13)
    for _ in range(400):
        nattrs = rng.randint(2, 4)
        rows = list({tuple(rng.randint(0, 2) for _ in range(nattrs)) for _ in range(rng.randint(0, 12))})
        cfd = random_cfd(rng, nattrs)
        assert violations(rows, cfd) == violations_brute(rows, cfd)


def test_plain_fd_is_a_cfd():
    rng = random.Random(3)
    for _ in range(200):
        rows = list({tuple(rng.randint(0, 2) for _ in range(3)) for _ in range(rng.randint(0, 8))})
        xs = rng.sample(range(3), rng.randint(1, 2))
        ys = [b for b in range(3) if b not in xs][:1]
        assert satisfies(rows, [from_fd(xs, ys)]) == fd_holds(rows, xs, ys)
