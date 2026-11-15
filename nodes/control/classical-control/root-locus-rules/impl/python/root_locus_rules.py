# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/root-locus-rules/. The authors are listed in prov/V7FWWP.jsonl.

"""Evans rules for the root locus of D(s) + K N(s) = 0, K > 0.

The loop transfer function is K G(s) with G = N/D, N = prod (s - z_k) and
D = prod (s - p_i), so N and D are monic. The input is the list of the n
open-loop poles and the m open-loop zeros, m <= n, closed under complex
conjugation (G has real coefficients), with no pole equal to a zero.

The rules computed here, with the line numbers of the pseudocode:
- L2: the real axis segments of the locus;
- L3: the centroid and the angles of the n - m asymptotes;
- L4, L5: the breakaway and break-in points, the roots s of
  N D' - N' D with K = -D(s)/N(s) real and positive;
- L6, L7: the departure angles at the poles and the arrival angles at the
  zeros, with multiplicity;
- L8: the crossings of the imaginary axis, the real w >= 0 with
  Im(D(jw) N(-jw)) = 0 and K = -D(jw)/N(jw) > 0.

Angles are in degrees in [0, 360). Roots of polynomials come from
ctlmat.polyroots. Tolerances: a pole or zero is real if its imaginary part
is at most 1e-9 (1 + |value|); two poles (or zeros) are the same if they
differ by at most 1e-9 (1 + |value|); a computed K is accepted as real if
its imaginary part is at most 1e-6 (1 + |K|).
"""

import cmath
import math
from dataclasses import dataclass, field

from ctlmat import polyadd, polymul, polyroots, polyval

__all__ = ["LocusRules", "root_locus_rules", "poly_from_roots", "closed_loop_poly"]

_TOL_SAME = 1e-9
_TOL_K = 1e-6


@dataclass
class LocusRules:
    n: int
    m: int
    segments: list = field(default_factory=list)       # [(left, right)], left may be -inf
    centroid: object = None                             # float, or None if n == m
    asymptote_angles: list = field(default_factory=list)
    breakaways: list = field(default_factory=list)      # [(s, K)]
    departures: list = field(default_factory=list)      # [(pole, [angles])]
    arrivals: list = field(default_factory=list)        # [(zero, [angles])]
    crossings: list = field(default_factory=list)       # [(w, K)], w >= 0
    imaginary_axis_on_locus: bool = False               # Im(D(jw) N(-jw)) is identically 0


def _same(a, b):
    return abs(a - b) <= _TOL_SAME * (1.0 + abs(b))


def _is_real(x):
    return abs(x.imag) <= _TOL_SAME * (1.0 + abs(x))


def _group(roots):
    """Distinct values with multiplicities, as [[value, count]]."""
    groups = []
    for r in roots:
        for g in groups:
            if _same(r, g[0]):
                g[1] += 1
                break
        else:
            groups.append([r, 1])
    return groups


def _check_conjugate(roots, what):
    left = list(roots)
    while left:
        r = left.pop()
        if _is_real(r):
            continue
        for i, w in enumerate(left):
            if _same(w, r.conjugate()):
                del left[i]
                break
        else:
            raise ValueError(what + " are not closed under conjugation")


def _poly_c(roots):
    p = [1.0 + 0j]
    for r in roots:
        p = polymul(p, [1.0, -complex(r)])
    return p


def poly_from_roots(roots):
    """Return the monic real polynomial with the given roots, highest power first.

    The roots must be closed under conjugation; the tiny imaginary parts
    left by rounding are dropped.
    """
    return [c.real for c in _poly_c(roots)]


def closed_loop_poly(den, num, k):
    """Return D + K N."""
    return polyadd(den, [k * c for c in num])


def _angle(z):
    """Argument of z in degrees, in [0, 360)."""
    a = math.degrees(cmath.phase(z)) % 360.0
    return 0.0 if a >= 360.0 - 1e-12 else a


def _real_k(den, num, s):
    nv = polyval(num, s)
    if nv == 0:
        return None
    k = -polyval(den, s) / nv
    if abs(k.imag) > _TOL_K * (1.0 + abs(k)):
        return None
    return k.real


def root_locus_rules(poles, zeros=()):
    """Return a LocusRules record for the poles and zeros of G."""
    poles = [complex(p) for p in poles]
    zeros = [complex(z) for z in zeros]
    n, m = len(poles), len(zeros)
    if n == 0 or m > n:  # @line L1
        raise ValueError("need at least one pole and no more zeros than poles")
    _check_conjugate(poles, "poles")
    _check_conjugate(zeros, "zeros")
    for z in zeros:
        if any(_same(z, p) for p in poles):
            raise ValueError("a pole equals a zero; cancel it first")
    den = poly_from_roots(poles)
    num = poly_from_roots(zeros)
    out = LocusRules(n=n, m=m)

    # L2: a real point is on the locus when an odd number of real poles and
    # zeros (with multiplicity) lie to its right.
    reals = _group([complex(x.real, 0.0) for x in poles + zeros if _is_real(x)])
    reals.sort(key=lambda g: -g[0].real)
    count = 0
    segs = []
    for i, (x, c) in enumerate(reals):  # @line L2
        count += c
        if count % 2 == 1:
            left = reals[i + 1][0].real if i + 1 < len(reals) else -math.inf
            right = x.real
            if segs and segs[-1][0] == right:
                segs[-1] = (left, segs[-1][1])
            else:
                segs.append((left, right))
    out.segments = sorted(segs)

    # L3: asymptotes.
    if n > m:  # @line L3
        out.centroid = (sum(p.real for p in poles) - sum(z.real for z in zeros)) / (n - m)
        out.asymptote_angles = [(2 * k + 1) * 180.0 / (n - m) for k in range(n - m)]

    # L4: W = (N D' - N' D) / (repeated factors), built from the distinct roots.
    pg = _group(poles)
    zg = _group(zeros)
    distinct = [g[0] for g in pg] + [g[0] for g in zg]
    weights = [g[1] for g in pg] + [-g[1] for g in zg]
    w = [0j]
    for i, wt in enumerate(weights):  # @line L4
        term = _poly_c([r for j, r in enumerate(distinct) if j != i])
        w = polyadd(w, [wt * c for c in term])
    w = [c.real for c in w]  # the terms come in conjugate pairs, so W is real
    wbig = max(abs(c) for c in w)
    while len(w) > 1 and abs(w[0]) <= 1e-12 * wbig:
        w.pop(0)
    # L5: keep the roots of W where K = -D/N is real and positive.
    for s in polyroots(w):  # @line L5
        k = _real_k(den, num, s)
        if k is not None and k > 0:
            out.breakaways.append((complex(s.real, 0.0) if _is_real(s) else s, k))

    # L6: departure angles.
    for p, mu in pg:  # @line L6
        base = 180.0 + sum(math.degrees(cmath.phase(p - z)) for z in zeros)
        base -= sum(math.degrees(cmath.phase(p - q)) for q in poles if not _same(q, p))
        out.departures.append((p, sorted(_angle(cmath.exp(1j * math.radians((base + 360.0 * j) / mu))) for j in range(mu))))
    # L7: arrival angles.
    for z, nu in zg:  # @line L7
        base = 180.0 + sum(math.degrees(cmath.phase(z - p)) for p in poles)
        base -= sum(math.degrees(cmath.phase(z - y)) for y in zeros if not _same(y, z))
        out.arrivals.append((z, sorted(_angle(cmath.exp(1j * math.radians((base + 360.0 * j) / nu))) for j in range(nu))))

    # L8: imaginary axis crossings. With D and N real and ascending
    # coefficients d_a, n_b, the coefficient of w^k in D(jw) N(-jw) is
    # j^k r_k with r_k = sum over a + b = k of d_a n_b (-1)^b. Its imaginary
    # part is r_k for k = 1 mod 4, -r_k for k = 3 mod 4 and 0 for even k, so
    # Im(D(jw) N(-jw)) = w R(w^2).
    da = den[::-1]
    na = num[::-1]
    r = [0.0] * (len(da) + len(na) - 1)
    for a, dv in enumerate(da):
        for b, nv in enumerate(na):
            r[a + b] += dv * nv * (-1) ** b
    rasc = [(r[k] if k % 4 == 1 else -r[k]) for k in range(1, len(r), 2)]  # @line L8
    big = max((abs(c) for c in rasc), default=0.0)
    found = []
    k0 = _real_k(den, num, 0j)
    if k0 is not None and k0 > 0:
        found.append((0.0, k0))
    if big == 0.0:
        out.imaginary_axis_on_locus = True
    else:
        rdesc = rasc[::-1]
        while rdesc and abs(rdesc[0]) <= 1e-12 * big:
            rdesc.pop(0)
        for u in (polyroots(rdesc) if len(rdesc) > 1 else []):
            if abs(u.imag) > 1e-7 * (1.0 + abs(u)) or u.real <= 0:
                continue
            om = math.sqrt(u.real)
            k = _real_k(den, num, 1j * om)
            if k is not None and k > 0 and not any(_same(om, f[0]) for f in found):
                found.append((om, k))
    out.crossings = sorted(found)
    return out  # @line L9
