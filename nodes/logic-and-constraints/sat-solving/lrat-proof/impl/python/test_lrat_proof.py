# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lrat-proof/. The authors are listed in prov/XV3Z16.jsonl.

import itertools
import random

from lrat_proof import (check_lrat, drat_to_lrat, find_rup_hints, format_lrat,
                        parse_lrat)

# IDs 1..8: (1 2 3), (1 2 -3), (1 -2 3), (1 -2 -3), (-1 2 3), ..., (-1 -2 -3)
ALL8 = [[a * 1, b * 2, c * 3] for a in (1, -1) for b in (1, -1) for c in (1, -1)]

PAGE = """9 1 0 -5 1 -6 2 -7 3 -8 4 0
10 2 0 9 5 6 0
10 d 1 2 3 4 0
11 0 9 10 7 8 0
"""


def models(clauses: list[list[int]], n: int) -> list[tuple[bool, ...]]:
    return [b for b in itertools.product([False, True], repeat=n)
            if all(any(b[abs(a) - 1] == (a > 0) for a in c) for c in clauses)]


def random_cnf(rng: random.Random, n: int, m: int) -> list[list[int]]:
    cnf = []
    for _ in range(m):
        vs = rng.sample(range(1, n + 1), min(3, n))
        cnf.append([v if rng.random() < 0.5 else -v for v in vs])
    return cnf


def dpll_proof(f: list[list[int]], n: int) -> list[tuple[str, list[int]]] | None:
    """DRUP proof from a DPLL tree: each closed node adds the negation of its path."""
    proof: list[tuple[str, list[int]]] = []

    def closed(path: list[int]) -> bool:
        db = {i + 1: c for i, c in enumerate(f + [c for _, c in proof])}
        if find_rup_hints(db, [-d for d in path]) is not None:
            proof.append(("a", [-d for d in path]))
            return True
        used = {abs(d) for d in path}
        free = [v for v in range(1, n + 1) if v not in used]
        if not free:
            return False
        x = free[0]
        if closed(path + [-x]) and closed(path + [x]):
            proof.append(("a", [-d for d in path]))
            return True
        return False

    return proof if closed([]) else None


def test_page_example() -> None:
    steps = parse_lrat(PAGE)
    assert check_lrat(ALL8, steps) == (True, None)
    assert format_lrat(steps) == PAGE


def test_generator_on_page_drat() -> None:
    drat = [("a", [1]), ("a", [2]), ("a", [])]
    steps = drat_to_lrat(ALL8, drat)
    assert steps[0] == ("a", 9, [1], [-5, 1, -6, 2, -7, 3, -8, 4])
    assert steps[1] == ("a", 10, [2], [9, 5, 6])
    assert steps[2] == ("a", 11, [], [9, 10, 7, 8])
    assert check_lrat(ALL8, steps) == (True, None)


def test_broken_hints_are_rejected() -> None:
    good = parse_lrat(PAGE)
    # The last hint of a RUP step is the false clause; without it the step fails.
    bad = list(good)
    bad[1] = ("a", 10, [2], [9, 5])
    assert check_lrat(ALL8, bad) == (False, 1)
    # A RAT step must list every clause that contains the negated pivot.
    bad = list(good)
    bad[0] = ("a", 9, [1], [-5, 1, -6, 2, -7, 3])
    assert check_lrat(ALL8, bad) == (False, 0)
    # A hint that is not unit is an error, even if a later hint would conflict.
    bad = list(good)
    bad[3] = ("a", 11, [], [7, 9, 10, 8])
    assert check_lrat(ALL8, bad) == (False, 3)
    # A deleted clause cannot be a hint.
    bad = list(good)
    bad[3] = ("a", 11, [], [9, 10, 7, 1])
    assert check_lrat(ALL8, bad) == (False, 3)


def test_random_refutations() -> None:
    rng = random.Random(17)
    done = 0
    while done < 60:
        n = rng.randint(3, 9)
        f = random_cnf(rng, n, rng.randint(3 * n, 6 * n))
        if models(f, n):
            continue
        drat = dpll_proof(f, n)
        assert drat is not None and drat[-1] == ("a", [])
        steps = drat_to_lrat(f, drat)
        assert check_lrat(f, steps) == (True, None)
        assert check_lrat(f, parse_lrat(format_lrat(steps))) == (True, None)
        # Drop the final hint of one addition: that step must fail, unless
        # it is RAT on its first literal with no candidate clauses at all.
        i = rng.randrange(len(steps))
        _, cid, c, hints = steps[i]
        active = f + [s[2] for s in steps[:i]]
        vacuous = bool(c) and not any(-c[0] in d for d in active)
        if hints and not vacuous:
            bad = steps[:i] + [("a", cid, c, hints[:-1])] + steps[i + 1:]
            assert check_lrat(f, bad) == (False, i)
        done += 1


def test_extension_steps_get_rat_hints() -> None:
    rng = random.Random(23)
    done = 0
    while done < 20:
        n = rng.randint(3, 8)
        f = random_cnf(rng, n, 6 * n)
        if models(f, n):
            continue
        y = n + 1
        ext = [("a", [-y, 1]), ("a", [-y, 2]), ("a", [y, -1, -2])]
        steps = drat_to_lrat(f, ext + dpll_proof(f, n))
        g = f + [ext[0][1], ext[1][1]]
        if find_rup_hints({i + 1: c for i, c in enumerate(g)}, [y, -1, -2]) is None:
            # Not RUP, so RAT on y with two tautological resolvents.
            assert steps[2][3] == [-(len(f) + 1), -(len(f) + 2)]
            done += 1
        assert check_lrat(f, steps) == (True, None)


def test_never_refutes_a_satisfiable_formula() -> None:
    rng = random.Random(5)
    for _ in range(300):
        n = rng.randint(2, 6)
        f = random_cnf(rng, n, rng.randint(1, 3 * n))
        if not models(f, n):
            continue
        ids = list(range(1, len(f) + 1))
        hints = [rng.choice(ids) for _ in range(rng.randint(1, 6))]
        assert check_lrat(f, [("a", len(f) + 1, [], hints)]) == (False, 0)
