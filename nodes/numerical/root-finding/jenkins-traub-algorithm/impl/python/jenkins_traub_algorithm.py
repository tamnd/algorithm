# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jenkins-traub-algorithm/. The authors are listed in prov/W75WVA.jsonl.

"""The Jenkins-Traub algorithm for the roots of a complex polynomial.

Coefficients are given highest degree first: a[0] z^n + ... + a[n]. Each root
is found by three stages of shifted H-polynomial iteration, then removed by
deflation. This follows the structure of CPOLY (Jenkins and Traub, 1970) in
plain complex arithmetic, without its scaling and cluster refinements.
"""

import cmath
import math
from collections import namedtuple

U = 2.0 ** -53  # unit roundoff of IEEE double
JTResult = namedtuple("JTResult", "roots evals steps status trace")


def _divide(c, s):
    """Synthetic division of c by (z - s): returns (quotient, value c(s))."""
    q = [c[0]]
    for x in c[1:]:
        q.append(q[-1] * s + x)
    return q[:-1], q[-1]


def _bound(a, s):
    """Rounding error bound for Horner's rule at s: sum of |a_k| |s|^(n-k)."""
    r, b = abs(s), 0.0
    for x in a:
        b = b * r + abs(x)
    return b


def jt_step(p, H, s):
    """One shifted step: returns (H_next normalized to leading coefficient 1,
    the new estimate t, p(s)). H_next = (H(z) - H(s)/p(s) p(z)) / (z - s)."""
    qp, ps = _divide(p, s)
    qh, hs = _divide(H, s)
    if ps == 0:  # s is a root: the limit of the iteration is p(z)/(z - s)
        return [x / qp[0] for x in qp], s, ps
    c = hs / ps
    Hn = [-c * qp[0]] + [qh[i] - c * qp[i + 1] for i in range(len(qh))]
    lead = Hn[0]
    if lead == 0 or not cmath.isfinite(lead):
        return [x / qp[0] for x in qp], s, ps  # restart H from p/(z - s)
    Hn = [x / lead for x in Hn]
    _, hns = _divide(Hn, s)
    t = s - ps / hns if hns != 0 else s
    return Hn, t, ps


def lower_bound(p):
    """Cauchy lower bound: the positive root of |a0| x^n + ... + |a_{n-1}| x - |a_n|."""
    c = [abs(x) for x in p[:-1]] + [-abs(p[-1])]
    lo, hi = 0.0, 1.0
    while _divide(c, hi)[1] < 0:
        hi *= 2.0
    for _ in range(100):  # bisection: the polynomial is increasing for x > 0
        mid = 0.5 * (lo + hi)
        if _divide(c, mid)[1] < 0:
            lo = mid
        else:
            hi = mid
    return lo


def jenkins_traub(a, M=5, L=20, max_shifts=20, max_steps=100000):
    a = [complex(x) for x in a]
    if any(not cmath.isfinite(x) for x in a):
        raise ValueError("coefficients must be finite")
    if not a or a[0] == 0:
        raise ValueError("leading coefficient must be nonzero")
    roots, trace = [], []
    while len(a) > 1 and a[-1] == 0:  # @line L1
        roots.append(0j)
        a.pop()
    p = [x / a[0] for x in a]
    evals = steps = 0
    while len(p) > 2:  # @line L2
        n = len(p) - 1
        H = [(n - k) * p[k] / n for k in range(n)]  # @line L3
        for _ in range(M):
            H, _, _ = jt_step(p, H, 0j)
            evals += 2
            steps += 1
        beta = lower_bound(p)  # @line L4
        theta, found = math.radians(49), None
        for attempt in range(1, max_shifts + 1):  # @line L5
            theta += math.radians(94)
            s = beta * cmath.exp(1j * theta)  # @line L6
            t_prev = t_prev2 = None
            for _ in range(L * attempt):  # @line L7
                if steps >= max_steps:
                    return JTResult(roots, evals, steps, "max-iter", trace)
                H, t, ps = jt_step(p, H, s)
                evals += 2
                steps += 1
                if ps == 0:
                    found = s
                    break
                weak = (t_prev is not None and t_prev2 is not None
                        and abs(t - t_prev) <= 0.5 * abs(t_prev)
                        and abs(t_prev - t_prev2) <= 0.5 * abs(t_prev2))
                t_prev2, t_prev = t_prev, t
                if weak:  # @line L8
                    found, H, e, k = _stage3(p, H, t, max_steps - steps, trace)
                    evals += e
                    steps += k
                    if found is not None:
                        break
                    t_prev = t_prev2 = None
            if found is not None:  # @line L9
                break
        if found is None:  # @line L10
            status = "max-iter" if steps >= max_steps else "failed"
            return JTResult(roots, evals, steps, status, trace)
        roots.append(found)  # @line L11
        p, _ = _divide(p, found)
    if len(p) == 2:
        roots.append(-p[1] / p[0])  # @line L12
    return JTResult(roots, evals, steps, "done", trace)


def _stage3(p, H, s, budget, trace):
    """Variable-shift stage: s <- s - p(s)/H(s) with H updated at each s.
    Accept s when |p(s)| is within 20 times the Horner rounding bound."""
    evals = steps = 0
    path, prev = [s], None
    for _ in range(min(10, budget)):
        ps = _divide(p, s)[1]
        evals += 1
        if abs(ps) <= 20 * U * _bound(p, s):  # converged to rounding level
            trace.append(path)
            return s, H, evals, steps
        if prev is not None and abs(ps) > 10 * prev:  # diverging: give up
            break
        prev = abs(ps)
        H, s, _ = jt_step(p, H, s)
        evals += 2
        steps += 1
        path.append(s)
    return None, H, evals, steps
