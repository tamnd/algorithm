# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/max-3sat-inapproximability/. The authors are listed in prov/VXQ2G0.jsonl.

"""The map from a PCP verifier to a 3CNF formula, used to prove that MAX 3SAT has a gap.

A verifier is a list of tests, one for each random string. A test is a pair
(positions, accepted) with distinct proof positions and the set of bit tuples
on which the test accepts. Proof position i is the variable i + 1. Clauses use
the DIMACS style: the literal v is variable v, and -v is its negation.
"""

from itertools import product

Clause = tuple[int, ...]
Test = tuple[tuple[int, ...], frozenset[tuple[int, ...]]]


def cnf_of_test(test: Test) -> list[Clause]:
    """One clause for each rejected tuple a: the clause is false exactly on a."""
    pos, acc = test
    out = []
    for a in product((0, 1), repeat=len(pos)):
        if a not in acc:
            out.append(tuple(-(i + 1) if b else (i + 1) for i, b in zip(pos, a)))
    return out


def split_clause(clause: Clause, next_var: int) -> tuple[list[Clause], int]:
    """Replace a clause of width w > 3 by w - 2 clauses of width 3 with w - 3 new variables."""
    w = len(clause)
    if w <= 3:
        return [clause], next_var
    ys = list(range(next_var, next_var + w - 3))
    out = [(clause[0], clause[1], ys[0])]
    for t in range(1, w - 3):
        out.append((-ys[t - 1], clause[t + 1], ys[t]))
    out.append((-ys[-1], clause[-2], clause[-1]))
    return out, next_var + w - 3


def verifier_to_3cnf(tests: list[Test], proof_length: int) -> tuple[list[Clause], list[list[Clause]], int]:
    """Return all clauses, the group of clauses of each test, and the number of variables."""
    next_var = proof_length + 1
    groups = []
    for t in tests:
        group = []
        for c in cnf_of_test(t):
            parts, next_var = split_clause(c, next_var)
            group.extend(parts)
        groups.append(group)
    return [c for g in groups for c in g], groups, next_var - 1


def clauses_per_test_bound(q: int) -> int:
    """K = 2^q * max(1, q - 2): no test produces more clauses."""
    return 2 ** q * max(1, q - 2)


def satisfied_count(clauses: list[Clause], value: dict[int, int]) -> int:
    return sum(1 for c in clauses if any(value[abs(l)] == (1 if l > 0 else 0) for l in c))


def max_satisfied(clauses: list[Clause], num_vars: int) -> int:
    best = 0
    for bits in product((0, 1), repeat=num_vars):
        best = max(best, satisfied_count(clauses, {v + 1: bits[v] for v in range(num_vars)}))
    return best


def max_acceptance(tests: list[Test], proof_length: int) -> int:
    return max(sum(1 for pos, acc in tests if tuple(p[i] for i in pos) in acc)
               for p in product((0, 1), repeat=proof_length))
