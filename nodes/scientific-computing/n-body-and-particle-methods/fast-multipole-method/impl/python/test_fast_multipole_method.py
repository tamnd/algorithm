# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-multipole-method/. The authors are listed in prov/2RM7MC.jsonl.
import cmath
import math
import random

from fast_multipole_method import (
    binomials,
    direct,
    eval_local,
    eval_multipole,
    fmm,
    interaction_list,
    l2l,
    m2l,
    m2m,
    p2m,
)


def charges(n, seed):
    rng = random.Random(seed)
    z = [complex(rng.random(), rng.random()) for _ in range(n)]
    q = [rng.uniform(-1.0, 1.0) for _ in range(n)]
    return q, z


def rel_err(a, b):
    num = math.sqrt(sum(abs(x - y) ** 2 for x, y in zip(a, b)))
    den = math.sqrt(sum(abs(y) ** 2 for y in b))
    return num / den


def test_p2m_error_bound_lemma_4_2():
    rng = random.Random(1)
    r = 0.5
    q = [rng.uniform(-1, 1) for _ in range(20)]
    z = [cmath.rect(r * rng.random(), rng.uniform(0, 2 * math.pi)) for _ in q]
    A = sum(abs(x) for x in q)
    for p in (2, 5, 10, 20):
        a = p2m(q, z, 0j, p)
        for w in (1.0 + 0j, 1.3j, -0.8 - 0.9j):
            exact = sum(qi * math.log(abs(w - zi)) for qi, zi in zip(q, z))
            c = abs(w) / r
            err = abs(eval_multipole(a, 0j, w).real - exact)
            bound = A / (p + 1) / (c - 1) * (1 / c) ** p
            assert err <= bound * (1 + 1e-9) + 1e-13


def test_m2m_is_exact():
    q, z = charges(15, 2)
    C = binomials(10)
    old, new = complex(0.3, 0.4), complex(0.5, 0.5)
    b = m2m(p2m(q, z, old, 10), old - new, C)
    ref = p2m(q, z, new, 10)
    assert max(abs(x - y) for x, y in zip(b, ref)) < 1e-12


def test_l2l_is_exact():
    rng = random.Random(3)
    b = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(9)]
    old, new = complex(0.2, -0.1), complex(-0.3, 0.25)
    c = l2l(b, old - new)
    for w in (0j, complex(0.1, 0.2), complex(-0.4, 0.3)):
        v1, d1 = eval_local(b, old, w)
        v2, d2 = eval_local(c, new, w)
        assert abs(v1 - v2) < 1e-12 and abs(d1 - d2) < 1e-11


def test_m2l_against_direct_and_lemma_4_7():
    rng = random.Random(4)
    src = complex(3.0, 1.0)
    R = math.sqrt(0.5)
    c = abs(src) / R - 1
    q = [rng.uniform(-1, 1) for _ in range(12)]
    z = [src + complex(rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5)) for _ in q]
    A = sum(abs(x) for x in q)
    errs = []
    for p in (4, 8, 16):
        b = m2l(p2m(q, z, src, p), src, binomials(p))
        e = 0.0
        for w in (0j, complex(0.4, -0.3), complex(-0.5, 0.5)):
            ref = sum(qi * math.log(abs(w - zi)) for qi, zi in zip(q, z))
            e = max(e, abs(eval_local(b, 0j, w)[0].real - ref))
        bound = A * (4 * math.e * (p + c) * (c + 1) + c * c) / (c * (c - 1)) * (1 / c) ** (p + 1)
        assert e < bound
        errs.append(e)
    assert errs[0] > errs[1] > errs[2]
    assert errs[2] < 1e-8


def test_interaction_list():
    assert len(interaction_list(5, 5, 4)) == 27
    assert len(interaction_list(0, 0, 2)) == 12
    for ix, iy in ((0, 0), (3, 2), (7, 7)):
        for nx, ny in interaction_list(ix, iy, 3):
            assert max(abs(nx - ix), abs(ny - iy)) >= 2
            assert max(abs(nx // 2 - ix // 2), abs(ny // 2 - iy // 2)) <= 1


def test_fmm_matches_direct_and_improves_with_p():
    q, z = charges(400, 5)
    u0, f0 = direct(q, z)
    eu, ef = [], []
    for p in (3, 6, 12, 20):
        u, f, _ = fmm(q, z, p=p, levels=3)
        eu.append(rel_err(u, u0))
        ef.append(rel_err(f, f0))
    assert all(eu[k] > eu[k + 1] for k in range(3))
    assert all(ef[k] > ef[k + 1] for k in range(3))
    assert eu[-1] < 1e-8 and ef[-1] < 1e-7


def test_near_field_pairs():
    q, z = charges(300, 6)
    u, f, st = fmm(q, z, p=16, levels=3)
    box = [(min(int(w.real * 8), 7), min(int(w.imag * 8), 7)) for w in z]
    near = sum(
        1
        for j in range(len(z))
        for i in range(len(z))
        if i != j and max(abs(box[i][0] - box[j][0]), abs(box[i][1] - box[j][1])) <= 1
    )
    assert st["p2p"] == near
    assert st["p2p"] < len(z) * (len(z) - 1)
    u0, _ = direct(q, z)
    assert rel_err(u, u0) < 1e-8


def test_small_inputs():
    u, f, st = fmm([2.0], [complex(0.3, 0.3)], p=5)
    assert u == [0.0] and f == [0j]
    q, z = [1.0, -1.0], [complex(0.1, 0.1), complex(0.9, 0.9)]
    u, f, _ = fmm(q, z, p=20)
    u0, f0 = direct(q, z)
    assert max(abs(a - b) for a, b in zip(u, u0)) < 1e-10
    assert max(abs(a - b) for a, b in zip(f, f0)) < 1e-10
