# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-walk-search/. The authors are listed in prov/ARW077.jsonl.
import math
import random

from qsim import apply_permutation, circuit_matrix, close, is_unitary, norm
from quantum_walk_search import (
    Walk,
    classical_cost,
    complete_with_loops,
    iterations,
    lazy_cycle,
    lazy_hypercube,
    quantum_cost,
    run,
    search,
    success,
    walk_steps,
)


def eigvecs(name, n):
    """Closed-form eigenvectors (v, lambda) of the three symmetric chains on n = 8 vertices."""
    if name == "hypercube":
        d = n.bit_length() - 1
        for s in range(n):
            w = bin(s).count("1")
            yield [(-1) ** bin(s & x).count("1") / math.sqrt(n) for x in range(n)], 1 - w / d
    elif name == "cycle":
        for k in range(n // 2 + 1):
            v = [math.cos(2 * math.pi * k * x / n) for x in range(n)]
            c = math.sqrt(sum(a * a for a in v))
            yield [a / c for a in v], (1 + math.cos(2 * math.pi * k / n)) / 2
    else:
        yield [1 / math.sqrt(n)] * n, 1.0
        for k in range(1, n):
            v = [1.0 if x == 0 else (-1.0 if x == k else 0.0) for x in range(n)]
            yield [a / math.sqrt(2) for a in v], 0.0


CHAINS = [("hypercube", lazy_hypercube(3)), ("cycle", lazy_cycle(8)), ("complete", complete_with_loops(8))]


def test_walk_is_unitary():
    for t in (0, 1):
        w = Walk(lazy_cycle(4), t)
        u = circuit_matrix(w.qubits, lambda s: w.walk(s, blocks=range(1 << t)))
        assert is_unitary(u)
        back = circuit_matrix(w.qubits, lambda s: w.walk(w.walk(s, blocks=range(1 << t)), blocks=range(1 << t), inverse=True))
        assert close(back, circuit_matrix(w.qubits, lambda s: s))


def test_szegedy_spectral_theorem():
    # for an eigenvector v of D with eigenvalue lambda, a = sum v_x |x>|p_x> and b = SWAP a span
    # an invariant plane: W a = 2 lambda b - a and W b = (4 lambda^2 - 1) b - 2 lambda a,
    # so W has the eigenvalues exp(+-2 i theta) there, with cos(theta) = lambda
    for name, p in CHAINS:
        w = Walk(p, 0)
        for v, lam in eigvecs(name, 8):
            a = w.start(v)
            b = apply_permutation(a, w.swap)
            wa, wb = w.walk(a), w.walk(b)
            assert close(wa, [2 * lam * y - x for x, y in zip(a, b)])
            assert close(wb, [(4 * lam * lam - 1) * y - 2 * lam * x for x, y in zip(a, b)])
            if lam == 1.0:
                assert close(wa, a)  # the stationary state is fixed


def p_zero(phi, t):
    """Probability that phase estimation with t ancilla qubits outputs 0 for the phase phi."""
    size = 1 << t
    s = sum(complex(math.cos(phi * k), math.sin(phi * k)) for k in range(size))
    return abs(s) ** 2 / size**2


def test_approximate_reflection():
    for name, p in CHAINS:
        for t in (2, 3):
            w = Walk(p, t)
            pi = w.start()
            assert close(w.reflect_pi(pi), pi)
            for v, lam in eigvecs(name, 8):
                if lam > 1 - 1e-12:
                    continue
                a = w.start(v)
                out = w.reflect_pi(a)
                err = norm([x + y for x, y in zip(out, a)])
                bound = 2 * math.sqrt(p_zero(2 * math.acos(lam), t)) * norm(a)
                assert err <= bound + 1e-9


def test_search_matches_amplitude_amplification():
    eps = 1 / 8
    t1 = iterations(eps)
    ideal = math.sin((2 * t1 + 1) * math.asin(math.sqrt(eps))) ** 2
    st, _ = run(complete_with_loops(8), {5}, 2, t1)
    assert abs(success(st, {5}, 8) - ideal) < 1e-9  # phases 0 and pi are exact with 2 qubits
    st, _ = run(lazy_hypercube(3), {5}, 6, t1)
    assert abs(success(st, {5}, 8) - ideal) < 1e-3
    for t, low in ((3, 0.93), (4, 0.94)):
        st, _ = run(lazy_hypercube(3), {5}, t, t1)
        assert success(st, {5}, 8) > low
        assert abs(sum(abs(a) ** 2 for a in st) - 1) < 1e-9


def test_cost_counts():
    for t, t1 in ((2, 1), (3, 2), (4, 3)):
        _, w = run(lazy_hypercube(3), {1}, t, t1)
        assert w.steps == walk_steps(t, t1)
    _, cost = search(lazy_cycle(8), {2}, 3, 2, random.Random(1))
    assert cost == {"setup": 1, "checks": 3, "walk_steps": 28}


def test_against_brute_force():
    rng = random.Random(2026)
    found = trials = 0
    for _ in range(45):
        name, p = rng.choice(CHAINS)
        marked = set(rng.sample(range(8), rng.randint(0, 3)))
        t1 = iterations(len(marked) / 8) if marked else 2
        x, _ = search(p, marked, 3, t1, rng)
        truth = [v for v in range(8) if v in marked]  # brute force over all vertices
        if not truth:
            assert x is None  # one-sided: never a false answer
        else:
            trials += 1
            assert x is None or x in truth
            found += x is not None
    assert trials >= 30 and found >= 0.8 * trials


def test_cost_formula_johnson():
    # element distinctness as a walk on r-subsets: S = r, C = 0, U = 1, delta = 1/r, eps = (r/N)^2
    for n in (10**4, 10**6):
        best = min(quantum_cost(r, 0, 1, (r / n) ** 2, 1 / r) for r in range(2, n))
        assert 1.8 < best / n ** (2 / 3) < 2.0
        r = round(n ** (2 / 3))
        assert classical_cost(r, 0, 1, (r / n) ** 2, 1 / r) > n
