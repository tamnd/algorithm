# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nova-state-encoding/. The authors are listed in prov/EG491A.jsonl.

import itertools
import random

from fsmlogic import all_codes, encoded_cost, encoded_function, exhaustive_best, implements, minimize, symbolic_function
from nova_state_encoding import face, nova_encode, weighted_constraints

# The machine of the page: one input, one output, four states.
M2 = (1, 1, ["s0", "s1", "s2", "s3"], [
    ("0", "s0", "s1", "1"), ("1", "s0", "s0", "1"),
    ("0", "s1", "s0", "1"), ("1", "s1", "s0", "1"),
    ("0", "s2", "s2", "0"), ("1", "s2", "s2", "1"),
    ("0", "s3", "s3", "1"), ("1", "s3", "s2", "0"),
])


def random_fsm(rng: random.Random, n, ni, no):
    states = [f"s{i}" for i in range(n)]
    rows = []
    for s in states:
        for x in range(1 << ni):
            rows.append((format(x, f"0{ni}b"), s, rng.choice(states), "".join(rng.choice("01") for _ in range(no))))
    return (ni, no, states, rows)


def meets(codes, group, k, states):
    mask, val = face(codes, group, k)
    return all(codes[t] & mask != val for t in states if t not in group)


def satisfiable(states, groups, k):
    """Brute force over all codes of k bits."""
    return any(all(meets(dict(zip(states, cs)), g, k, states) for g in groups)
               for cs in itertools.permutations(range(1 << k), len(states)))


def kappa(codes, group, k, states):
    """Least number of cubes over the k state bits that hold the codes of
    group and no code of another state; unused codes are free."""
    pts = list(itertools.product((0, 1), repeat=k))
    as_pt = lambda c: tuple(c >> (k - 1 - b) & 1 for b in range(k))
    on = {as_pt(codes[s]) for s in group}
    off = {as_pt(codes[s]) for s in states if s not in group}
    dc = set(pts) - on - off
    return len(minimize([2] * k, [on], [dc]))


def symbolic_groups(fsm):
    ni, no, states, rows = fsm
    domains, on, dc = symbolic_function(fsm)
    return [frozenset(states[v] for v in range(len(states)) if cube[ni] >> v & 1)
            for cube, _ in minimize(domains, on, dc)]


def test_page_example():
    states = M2[2]
    assert symbolic_groups(M2).__len__() == 7
    assert weighted_constraints(M2) == [
        (frozenset({"s0", "s1"}), 1), (frozenset({"s2", "s3"}), 1), (frozenset({"s0", "s1", "s2"}), 1)]
    k, codes, kept, dropped = nova_encode(M2)
    assert (k, codes) == (2, {"s0": 0, "s1": 1, "s2": 2, "s3": 3})
    assert kept == [frozenset({"s0", "s1"}), frozenset({"s2", "s3"})]
    assert dropped == [frozenset({"s0", "s1", "s2"})]
    assert not satisfiable(states, kept + dropped, 2)
    assert encoded_cost(M2, codes, 2) == (5, 10)
    assert sum(kappa(codes, g, 2, states) for g in symbolic_groups(M2)) == 8
    assert exhaustive_best(M2, 2)[0] == (4, 9)


def test_random_machines():
    rng = random.Random(1990)
    hits = excess = worst = most = 0
    for _ in range(100):
        fsm = random_fsm(rng, 4, 1, 1)
        states = fsm[2]
        k, codes, kept, dropped = nova_encode(fsm)
        assert k == 2 and sorted(codes.values()) == sorted(set(codes.values()))
        # the kept groups are met, and each dropped group fails with the
        # groups kept before it
        assert all(meets(codes, g, k, states) for g in kept)
        before = []
        for g, w in weighted_constraints(fsm):
            if g in kept:
                before.append(g)
            else:
                assert g in dropped and not satisfiable(states, before + [g], k)
        # the proved bound: cubes <= sum over symbolic cubes of kappa
        domains, on, dc = encoded_function(fsm, codes, k)
        exact = minimize(domains, on, dc)
        assert implements(fsm, codes, k, exact)
        assert len(exact) <= sum(kappa(codes, g, k, states) for g in symbolic_groups(fsm))
        # does the greedy keep the largest weight that any code can meet?
        weights = weighted_constraints(fsm)
        got_w = sum(w for g, w in weights if g in kept)
        best_w = max(sum(w for g, w in weights if meets(dict(zip(states, cs)), g, k, states))
                     for cs in all_codes(4, k))
        assert got_w <= best_w
        most += got_w == best_w
        # measured gap of the final logic to the best 2-bit code
        best = exhaustive_best(fsm, k)[0][0]
        got = len(exact)
        hits += got == best
        excess += got - best
        worst = max(worst, got - best)
    assert (most, hits, excess, worst) == MEASURED


# 100 machines: the greedy keeps the largest weight that any 2-bit code can
# meet on all 100; the final logic meets the best 2-bit code on 41, with 71
# extra cubes in total and at most 3 extra cubes on one machine.
MEASURED = (100, 41, 71, 3)
