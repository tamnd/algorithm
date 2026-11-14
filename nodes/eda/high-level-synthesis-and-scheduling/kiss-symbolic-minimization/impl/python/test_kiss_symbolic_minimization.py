# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kiss-symbolic-minimization/. The authors are listed in prov/QRSANA.jsonl.

import itertools
import random

from fsmlogic import all_codes, cost, encoded_cost, encoded_function, exhaustive_best, implements, minimize
from kiss_symbolic_minimization import embed, encoded_cover, face_constraints, kiss_encode, satisfies, symbolic_cover

# The machine of the page: one input, one output, four states.
M1 = (1, 1, ["s0", "s1", "s2", "s3"], [
    ("0", "s0", "s2", "1"), ("1", "s0", "s2", "0"),
    ("0", "s1", "s2", "0"), ("1", "s1", "s2", "1"),
    ("0", "s2", "s3", "0"), ("1", "s2", "s1", "1"),
    ("0", "s3", "s1", "1"), ("1", "s3", "s3", "0"),
])


def random_fsm(rng: random.Random, n, ni, no):
    states = [f"s{i}" for i in range(n)]
    rows = []
    for s in states:
        for x in range(1 << ni):
            rows.append((format(x, f"0{ni}b"), s, rng.choice(states), "".join(rng.choice("01") for _ in range(no))))
    return (ni, no, states, rows)


def brute_min_cubes(domains, on, dc):
    """Least number of cubes, by trying all sets of cubes of growing size."""
    nout = len(on)
    allowed = [on[j] | dc[j] for j in range(nout)]
    terms = []
    for cube in itertools.product(*[range(1, 1 << d) for d in domains]):
        pts = list(itertools.product(*[[v for v in range(d) if cube[i] >> v & 1] for i, d in enumerate(domains)]))
        outs = [j for j in range(nout) if all(p in allowed[j] for p in pts)]
        terms.append(frozenset((p, j) for j in outs for p in pts if p in on[j]))
    terms = sorted({t for t in terms if t}, key=len, reverse=True)
    need = frozenset((p, j) for j in range(nout) for p in on[j])
    for size in range(len(need) + 1):
        for combo in itertools.combinations(terms, size):
            if need <= frozenset().union(*combo):
                return size


def test_minimizer_against_brute_force():
    rng = random.Random(5)
    for _ in range(30):
        domains = rng.choice([[2, 2, 2], [2, 3], [4]])
        pts = list(itertools.product(*[range(d) for d in domains]))
        on, dc = [], []
        for _ in range(2):
            on.append({p for p in pts if rng.random() < 0.4})
            dc.append({p for p in pts if p not in on[-1] and rng.random() < 0.2})
        cover = minimize(domains, on, dc)
        assert len(cover) == brute_min_cubes(domains, on, dc)
        for j in range(2):
            got = {p for p in pts if any(j in outs and all(c[i] >> p[i] & 1 for i in range(len(p))) for c, outs in cover)}
            assert on[j] <= got <= on[j] | dc[j]


def test_page_example():
    cover = symbolic_cover(M1)
    assert len(cover) == 7
    assert face_constraints(cover, M1[2]) == [frozenset({"s0", "s1"})]
    k, codes, _, _ = kiss_encode(M1)
    assert (k, codes) == (2, {"s0": 0, "s1": 1, "s2": 2, "s3": 3})
    enc = encoded_cover(M1, codes, k, cover)
    assert len(enc) == 7 and implements(M1, codes, k, enc)
    assert encoded_cost(M1, codes, k) == (7, 19)
    best, costs = exhaustive_best(M1, 2)
    assert best == (4, 8) and len(costs) == 12
    sat = [encoded_cost(M1, dict(zip(M1[2], cs)), 2) for cs in all_codes(4, 2)
           if satisfies(dict(zip(M1[2], cs)), frozenset({"s0", "s1"}), 2, M1[2])]
    assert len(sat) == 8 and min(sat) == (5, 9) and max(sat) == (7, 19)
    assert exhaustive_best(M1, 3)[0] == (3, 6)


def test_random_machines():
    rng = random.Random(1985)
    hits = excess = worst = longer = compared = 0
    for _ in range(100):
        fsm = random_fsm(rng, 4, 1, 1)
        states = fsm[2]
        cover = symbolic_cover(fsm)
        cons = face_constraints(cover, states)
        k, codes, _, _ = kiss_encode(fsm)
        # k is the least length that meets every face constraint
        if k > 2:
            longer += 1
            assert embed(states, cons, k - 1) is None
            assert not any(all(satisfies(dict(zip(states, cs)), g, k - 1, states) for g in cons)
                           for cs in all_codes(4, k - 1))
        assert all(satisfies(codes, g, k, states) for g in cons)
        # the KISS construction: one encoded cube per symbolic cube at most
        enc = encoded_cover(fsm, codes, k, cover)
        assert len(enc) <= len(cover) and implements(fsm, codes, k, enc)
        domains, on, dc = encoded_function(fsm, codes, k)
        exact = minimize(domains, on, dc)
        assert implements(fsm, codes, k, exact)
        assert len(exact) <= len(enc)
        # every 2-bit code that meets all constraints obeys the same bound
        for cs in all_codes(4, 2):
            cd = dict(zip(states, cs))
            if all(satisfies(cd, g, 2, states) for g in cons):
                assert encoded_cost(fsm, cd, 2)[0] <= len(cover)
        # measured gap to the best code of the same length (up to 3 bits)
        if k > 3:
            continue
        compared += 1
        best = exhaustive_best(fsm, k)[0][0]
        got = cost(exact, domains)[0]
        assert got >= best
        hits += got == best
        excess += got - best
        worst = max(worst, got - best)
    assert (longer, compared, hits, excess, worst) == MEASURED


# 100 machines: 32 need 3 or more bits, 99 need at most 3; KISS meets the
# best code of its own length on 41 of those 99, with 70 extra cubes in
# total and at most 3 extra cubes on one machine.
MEASURED = (32, 99, 41, 70, 3)
