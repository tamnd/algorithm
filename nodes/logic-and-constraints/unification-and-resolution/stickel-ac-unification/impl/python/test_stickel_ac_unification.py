# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stickel-ac-unification/. The authors are listed in prov/JEGV8S.jsonl.

import itertools
import random
from collections import Counter

from stickel_ac_unification import build, diophantine_basis, flatten, stickel_ac_unification

A, B, C = ("a",), ("b",), ("c",)


def plus(*args):
    return build(list(args))


def apply(t, sigma):
    if isinstance(t, str):
        return sigma.get(t, t)
    if len(t) == 1:
        return t
    return (t[0], *[apply(u, sigma) for u in t[1:]])


def canon(t):
    return frozenset(flatten(t).items())


def term_vars(t):
    return sorted(u for u in flatten(t) if isinstance(u, str))


def multisets(alphabet, max_size):
    for k in range(1, max_size + 1):
        for combo in itertools.combinations_with_replacement(alphabet, k):
            yield Counter(combo)


def ac_match(pairs, lam=None):
    """Find lam with flatten(p lam) == q for all (p, q); q holds constants only.

    Pattern p is a Counter of variables and constants. Brute-force backtracking.
    """
    lam = dict(lam or {})
    for p, q in pairs:
        known = Counter()
        free = []
        for u, k in p.items():
            if isinstance(u, str) and u not in lam:
                free.append((u, k))
            elif isinstance(u, str):
                for w, m in lam[u].items():
                    known[w] += k * m
            else:
                known[u] += k
        if known - q:
            return None
        if not free:
            if known != q:
                return None
            continue
        (u, k), rest = free[0], q - known
        alphabet = sorted(rest, key=repr)
        for m in multisets(alphabet, sum(rest.values()) // k):
            if all(rest[w] >= k * c for w, c in m.items()):
                found = ac_match(pairs, {**lam, u: m})
                if found is not None:
                    return found
        return None
    return lam


def is_instance(sigma, rho, xs):
    """True when some lam gives x sigma lam =AC x rho for each x in xs (rho ground)."""
    pairs = [(flatten(sigma.get(x, x)), flatten(rho[x])) for x in xs]
    return ac_match(pairs) is not None


def ground_unifiers(s, t, alphabet, max_size):
    xs = sorted(set(term_vars(s)) | set(term_vars(t)))
    options = list(multisets(alphabet, max_size))
    for vals in itertools.product(options, repeat=len(xs)):
        rho = {x: build(sorted(m.elements(), key=repr)) for x, m in zip(xs, vals)}
        if canon(apply(s, rho)) == canon(apply(t, rho)):
            yield rho


def check(s, t, alphabet=(A, B), max_size=3):
    us = stickel_ac_unification(s, t)
    xs = sorted(set(term_vars(s)) | set(term_vars(t)))
    for sigma in us:
        assert canon(apply(s, sigma)) == canon(apply(t, sigma))
    count = 0
    for rho in ground_unifiers(s, t, alphabet, max_size):
        count += 1
        assert any(is_instance(sigma, rho, xs) for sigma in us), rho
    if not us:
        assert count == 0
    return us


def test_diophantine_basis() -> None:
    assert diophantine_basis([1], [1]) == [(1, 1)]
    assert sorted(diophantine_basis([2], [1, 1])) == [(1, 0, 2), (1, 1, 1), (1, 2, 0)]
    assert sorted(diophantine_basis([1, 1], [1, 1])) == [(0, 1, 0, 1), (0, 1, 1, 0), (1, 0, 0, 1), (1, 0, 1, 0)]
    assert sorted(diophantine_basis([2], [3])) == [(3, 2)]
    # Brute force: the basis generates exactly the solutions in a box.
    rng = random.Random(12)
    for _ in range(40):
        a = [rng.randint(1, 3) for _ in range(rng.randint(1, 2))]
        b = [rng.randint(1, 3) for _ in range(rng.randint(1, 2))]
        basis = diophantine_basis(a, b)
        for v in itertools.product(range(5), repeat=len(a) + len(b)):
            if sum(v) and sum(x * y for x, y in zip(a, v)) == sum(x * y for x, y in zip(b, v[len(a):])):
                assert any(all(p <= q for p, q in zip(w, v)) for w in basis)


def test_example() -> None:
    us = check(plus("x", "x"), plus("y", "z"))
    assert len(us) == 5
    us = check(plus("x", "y"), plus("u", "v"))
    assert len(us) == 7
    us = check(plus("x", A), plus("y", B))
    assert {"x": B, "y": A} in us and len(us) == 2


def test_edges() -> None:
    assert stickel_ac_unification(A, A) == [{}]
    assert stickel_ac_unification(A, B) == []
    assert stickel_ac_unification(plus("x", A), plus("x", B)) == []
    assert stickel_ac_unification(plus("x", A), "x") == []
    assert stickel_ac_unification(plus(A, B), plus(B, A)) == [{}]
    (only,) = stickel_ac_unification("x", plus(A, B))
    assert list(only) == ["x"] and canon(only["x"]) == canon(plus(A, B))
    us = stickel_ac_unification("x", "y")
    assert us == [{"x": "z1", "y": "z1"}]
    check(plus("x", "x"), plus(A, B))
    assert stickel_ac_unification(plus("x", "x"), plus(A, B)) == []
    check(plus("x", "x"), plus(A, A))


def test_random_against_brute_force() -> None:
    rng = random.Random(2468)
    pool = ["x", "y", "z", A, B]
    for _ in range(500):
        left = [rng.choice(pool) for _ in range(rng.randint(1, 3))]
        right = [rng.choice(pool) for _ in range(rng.randint(1, 3))]
        nvars = len({u for u in left + right if isinstance(u, str)})
        check(build(left), build(right), (A, B), 3 if nvars <= 2 else 2)
