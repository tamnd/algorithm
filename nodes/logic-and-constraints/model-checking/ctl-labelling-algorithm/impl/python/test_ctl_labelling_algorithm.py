# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ctl-labelling-algorithm/. The authors are listed in prov/JZ943Y.jsonl.

import random
from collections import deque
from itertools import combinations

import pytest

from ctl_labelling_algorithm import sat, sccs

P, Q, R = ("ap", "p"), ("ap", "q"), ("ap", "r")


# ---------------------------------------------------------------- reference


def lassos(succ: dict, s) -> list:
    """All simple lassos from s: s0 .. s(k-1) distinct, and s(k) equal to some s(j).

    Each one stands for the infinite path s0 .. s(j-1) (s(j) .. s(k-1)) repeated.
    In a finite structure, an infinite path that is a witness or a counterexample
    for a CTL path formula can be replaced by such a lasso.
    """
    out = []
    stack = [[s]]
    while stack:
        path = stack.pop()
        for t in succ[path[-1]]:
            if t in path:
                out.append(path)  # positions 0 .. k-1 cover all suffixes of the lasso
            else:
                stack.append(path + [t])
    return out


def ref_sat(states, succ, label, phi) -> set:
    """Evaluate phi by its definition on all simple lassos (an independent oracle)."""
    memo: dict = {}
    lasso_memo: dict = {}

    def paths(s):
        if s not in lasso_memo:
            lasso_memo[s] = lassos(succ, s)
        return lasso_memo[s]

    def path_holds(op, f, path) -> bool:
        if op == "U":
            for v in path:
                if holds(f[2], v):
                    return True
                if not holds(f[1], v):
                    return False
            return False
        if op == "F":
            return any(holds(f[1], v) for v in path)
        if op == "G":
            return all(holds(f[1], v) for v in path)
        raise ValueError(op)

    def holds(f, s) -> bool:
        key = (f, s)
        if key in memo:
            return memo[key]
        op = f[0]
        if op == "true":
            r = True
        elif op == "false":
            r = False
        elif op == "ap":
            r = f[1] in label[s]
        elif op == "not":
            r = not holds(f[1], s)
        elif op == "and":
            r = holds(f[1], s) and holds(f[2], s)
        elif op == "or":
            r = holds(f[1], s) or holds(f[2], s)
        elif op == "implies":
            r = (not holds(f[1], s)) or holds(f[2], s)
        elif op == "EX":
            r = any(holds(f[1], t) for t in succ[s])
        elif op == "AX":
            r = all(holds(f[1], t) for t in succ[s])
        else:
            quant, temporal = op[0], op[1]
            results = (path_holds(temporal, f, p) for p in paths(s))
            r = any(results) if quant == "E" else all(results)
        memo[key] = r
        return r

    return {s for s in states if holds(phi, s)}


def bfs_reach(succ, sources) -> set:
    seen = set(sources)
    queue = deque(sources)
    while queue:
        v = queue.popleft()
        for w in succ[v]:
            if w not in seen:
                seen.add(w)
                queue.append(w)
    return seen


def random_structure(rng: random.Random, n: int):
    states = list(range(n))
    succ = {s: sorted(set(rng.choice(states) for _ in range(rng.randint(1, 3)))) for s in states}
    label = {s: {a for a in "pqr" if rng.random() < 0.45} for s in states}
    return states, succ, label


UNARY = ["not", "EX", "AX", "EF", "AF", "EG", "AG"]
BINARY = ["and", "or", "implies", "EU", "AU"]


def random_formula(rng: random.Random, depth: int):
    if depth == 0 or rng.random() < 0.25:
        return rng.choice([P, Q, R, P, Q, ("true",)])
    if rng.random() < 0.5:
        return (rng.choice(UNARY), random_formula(rng, depth - 1))
    return (rng.choice(BINARY), random_formula(rng, depth - 1), random_formula(rng, depth - 1))


# ---------------------------------------------------------------- the worked example

EX_STATES = [0, 1, 2, 3, 4, 5]
EX_SUCC = {0: [1, 2], 1: [3], 2: [2, 4], 3: [0], 4: [5], 5: [4]}
EX_LABEL = {0: {"p"}, 1: {"p"}, 2: {"p"}, 3: {"p", "q"}, 4: set(), 5: {"p"}}


def test_worked_example() -> None:
    s, n, lb = EX_STATES, EX_SUCC, EX_LABEL
    comps = sorted(sorted(c) for c in sccs(s, n, {0, 1, 2, 3, 5}))
    assert comps == [[0, 1, 3], [2], [5]]
    assert sat(s, n, lb, ("EG", P)) == {0, 1, 2, 3}
    assert sat(s, n, lb, ("EU", P, Q)) == {0, 1, 3}
    assert sat(s, n, lb, ("AU", P, Q)) == {1, 3}
    assert sat(s, n, lb, ("AF", Q)) == {1, 3}
    assert sat(s, n, lb, ("EG", ("not", Q))) == {0, 2, 4, 5}
    assert sat(s, n, lb, ("AG", ("EF", Q))) == set()
    assert sat(s, n, lb, ("EF", ("AG", ("not", Q)))) == {0, 1, 2, 3, 4, 5}


# ---------------------------------------------------------------- edge cases


def test_single_state_self_loop() -> None:
    states, succ = [0], {0: [0]}
    assert sat(states, succ, {0: {"p"}}, ("EG", P)) == {0}
    assert sat(states, succ, {0: set()}, ("EF", P)) == set()
    assert sat(states, succ, {0: set()}, ("AG", ("not", P))) == {0}


def test_not_total_is_rejected() -> None:
    with pytest.raises(ValueError):
        sat([0, 1], {0: [1], 1: []}, {0: set(), 1: set()}, P)


def test_eg_needs_a_cycle_inside() -> None:
    # 0 -> 1 -> 2 -> 2; p holds at 0 and 1 only, so no p-path is infinite.
    states, succ = [0, 1, 2], {0: [1], 1: [2], 2: [2]}
    label = {0: {"p"}, 1: {"p"}, 2: set()}
    assert sat(states, succ, label, ("EG", P)) == set()
    assert sat(states, succ, label, ("EU", P, ("not", P))) == {0, 1, 2}


def test_au_self_loop_is_not_enough() -> None:
    # 0 -> 0, 0 -> 1; q at 1. A[p U q] fails at 0 because of the path 0 0 0 ...
    states, succ = [0, 1], {0: [0, 1], 1: [1]}
    label = {0: {"p"}, 1: {"q"}}
    assert sat(states, succ, label, ("AU", P, Q)) == {1}
    assert sat(states, succ, label, ("EU", P, Q)) == {0, 1}


def test_deep_nesting_needs_no_recursion() -> None:
    states, succ, label = EX_STATES, EX_SUCC, EX_LABEL
    f, x = P, {s for s in states if "p" in label[s]}
    for _ in range(300):
        f = ("not", ("EX", f))
        x = {s for s in states if not any(t in x for t in succ[s])}
    assert sat(states, succ, label, f) == x


# ---------------------------------------------------------------- random against the reference


def test_random_against_lassos() -> None:
    rng = random.Random(1986)
    for _ in range(400):
        states, succ, label = random_structure(rng, rng.randint(1, 6))
        for _ in range(3):
            phi = random_formula(rng, 3)
            assert sat(states, succ, label, phi) == ref_sat(states, succ, label, phi), (succ, label, phi)


def test_sccs_partition_and_mutual_reachability() -> None:
    rng = random.Random(77)
    for _ in range(300):
        states, succ, _ = random_structure(rng, rng.randint(1, 8))
        inside = {s for s in states if rng.random() < 0.8}
        comps = sccs(states, succ, inside)
        assert sorted(v for c in comps for v in c) == sorted(inside)
        sub = {s: [t for t in succ[s] if t in inside] for s in inside}
        reach = {s: bfs_reach(sub, [s]) for s in inside}
        where = {v: i for i, c in enumerate(comps) for v in c}
        for a in inside:
            for b in inside:
                assert (where[a] == where[b]) == (b in reach[a] and a in reach[b])


# ---------------------------------------------------------------- reachability and invariants against BFS


def test_reachability_and_invariants_against_bfs() -> None:
    rng = random.Random(4242)
    for _ in range(500):
        states, succ, label = random_structure(rng, rng.randint(1, 9))
        targets = {s for s in states if "p" in label[s]}
        ef = sat(states, succ, label, ("EF", P))
        for s in states:
            assert (s in ef) == bool(bfs_reach(succ, [s]) & targets)
        ag = sat(states, succ, label, ("AG", Q))
        invariant_holds = all("q" in label[s] for s in bfs_reach(succ, [0]))
        assert (0 in ag) == invariant_holds


# ---------------------------------------------------------------- fairness


def fair_set_reference(states, succ, a: set, pairs) -> set:
    """States with a fair infinite path inside a, by brute force over all state sets.

    A set C is the set of states that some path visits infinitely often if and
    only if C is not empty and each state of C reaches each state of C, itself
    included, by a path of one or more steps inside C.
    """
    good: set = set()
    for k in range(1, len(a) + 1):
        for c in combinations(sorted(a), k):
            cs = set(c)
            sub = {s: [t for t in succ[s] if t in cs] for s in cs}
            if not all(cs <= bfs_reach(sub, sub[s]) for s in cs):
                continue
            if all((not cs & p) or (cs & q) for (p, q) in pairs):
                good |= cs
    sub_a = {s: [t for t in succ[s] if t in a] for s in a}
    return {s for s in a if bfs_reach(sub_a, [s]) & good}


def test_fair_eg_against_brute_force() -> None:
    rng = random.Random(1987)
    for _ in range(300):
        states, succ, label = random_structure(rng, rng.randint(1, 6))
        justice = [{s for s in states if rng.random() < 0.4} for _ in range(rng.randint(0, 2))]
        compassion = [
            ({s for s in states if rng.random() < 0.4}, {s for s in states if rng.random() < 0.3})
            for _ in range(rng.randint(0, 2))
        ]
        if not justice and not compassion:
            justice = [set(states)]
        a = {s for s in states if "p" in label[s]}
        pairs = [(set(states), j) for j in justice] + compassion
        expected = fair_set_reference(states, succ, a, pairs)
        got = sat(states, succ, label, ("EG", P), justice=justice, compassion=compassion)
        assert got == expected, (succ, label, justice, compassion)


def test_trivial_fairness_changes_nothing() -> None:
    rng = random.Random(31)
    for _ in range(200):
        states, succ, label = random_structure(rng, rng.randint(1, 6))
        phi = random_formula(rng, 3)
        assert sat(states, succ, label, phi, justice=[set(states)]) == sat(states, succ, label, phi)


def test_justice_hand_made() -> None:
    # 0 -> 0, 0 -> 1, 1 -> 1, p at 1. The path 0 0 0 ... never reaches p.
    states, succ, label = [0, 1], {0: [0, 1], 1: [1]}, {0: set(), 1: {"p"}}
    assert sat(states, succ, label, ("AF", P)) == {1}
    assert sat(states, succ, label, ("AF", P), justice=[{1}]) == {0, 1}
    # The fair EG of "not p" is empty: a fair path must visit 1 again and again.
    assert sat(states, succ, label, ("EG", ("not", P)), justice=[{1}]) == set()


def test_weak_and_strong_fairness_differ() -> None:
    # 0 has the action t enabled (label e); 0 -> 1 -> 0 skips it, 0 -> 2 takes it.
    states = [0, 1, 2]
    succ = {0: [1, 2], 1: [0], 2: [2]}
    label = {0: {"e"}, 1: set(), 2: {"t"}}
    af_t = ("AF", ("ap", "t"))
    assert sat(states, succ, label, af_t) == {2}
    # Weak fairness FG e -> GF t is the justice set "not e or t" = {1, 2}.
    assert sat(states, succ, label, af_t, justice=[{1, 2}]) == {2}
    # Strong fairness GF e -> GF t is the compassion pair ({0}, {2}).
    assert sat(states, succ, label, af_t, compassion=[({0}, {2})]) == {0, 1, 2}


def test_no_fair_path_makes_a_true() -> None:
    # The justice set is never visited on a cycle, so no state has a fair path.
    states, succ, label = [0, 1], {0: [1], 1: [1]}, {0: {"p"}, 1: set()}
    j = [{0}]
    assert sat(states, succ, label, ("EG", ("true",)), justice=j) == set()
    assert sat(states, succ, label, ("AG", ("false",)), justice=j) == {0, 1}
    assert sat(states, succ, label, ("EX", ("true",)), justice=j) == set()
