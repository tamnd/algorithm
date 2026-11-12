# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/evidence-lower-bound/. The authors are listed in prov/9XGGSJ.jsonl.

"""The evidence lower bound (ELBO) of a discrete latent variable model.

The model is a joint table joint[z] = p(x, z) for one fixed observation x and
a finite set of latent values z. A variational distribution q is a list of
probabilities over the same z. The functions give

    ELBO(q) = sum_z q(z) (log p(x, z) - log q(z))
    KL(q || p(. | x)) = sum_z q(z) (log q(z) - log p(z | x))

in floating point, and also exactly. A logarithm of a positive rational
number r = prod_p p^(e_p) is the formal sum sum_p e_p log p. So a sum of
rational multiples of logarithms of rationals is a map from primes to
Fractions, and the identity log p(x) = ELBO(q) + KL(q || p(. | x)) can be
checked with no rounding at all.
"""

import math
from fractions import Fraction


def evidence(joint):
    """p(x) = sum_z p(x, z)."""
    return sum(joint)


def posterior(joint):
    """p(z | x) = p(x, z) / p(x)."""
    px = evidence(joint)
    return [pz / px for pz in joint]


def elbo(joint, q):
    """ELBO(q) in floating point. Terms with q(z) = 0 contribute 0."""
    total = 0.0
    for pz, qz in zip(joint, q):
        if qz > 0:
            if pz == 0:
                return -math.inf
            total += float(qz) * (math.log(pz) - math.log(qz))
    return total


def elbo_jensen_terms(joint, q):
    """The two sides of Jensen: log E_q[p(x,z)/q(z)] and E_q[log(p(x,z)/q(z))].

    Over the support of q, E_q[p(x,z)/q(z)] is the part of p(x) on that
    support. The second value is the ELBO and is at most the first one.
    """
    ratio_mean = sum(pz for pz, qz in zip(joint, q) if qz > 0)
    return math.log(ratio_mean), elbo(joint, q)


def kl(q, p):
    """KL(q || p) = sum_z q(z) log(q(z) / p(z)) in floating point."""
    total = 0.0
    for qz, pz in zip(q, p):
        if qz > 0:
            if pz == 0:
                return math.inf
            total += float(qz) * (math.log(qz) - math.log(pz))
    return total


# ---------------------------------------------------------------- exact logs


def _factor(n):
    """Prime factorization of a positive integer by trial division."""
    out = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            out[d] = out.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def exact_log(r):
    """log r for a positive rational r, as a map prime -> integer exponent."""
    r = Fraction(r)
    if r <= 0:
        raise ValueError("log of a non-positive number")
    out = {}
    for p, e in _factor(r.numerator).items():
        out[p] = out.get(p, 0) + e
    for p, e in _factor(r.denominator).items():
        out[p] = out.get(p, 0) - e
    return {p: Fraction(e) for p, e in out.items() if e != 0}


def lin_comb(terms):
    """sum_k c_k log r_k for pairs (c_k, r_k), as a map prime -> Fraction."""
    out = {}
    for c, r in terms:
        for p, e in exact_log(r).items():
            out[p] = out.get(p, Fraction(0)) + Fraction(c) * e
    return {p: e for p, e in out.items() if e != 0}


def add_logs(a, b):
    out = dict(a)
    for p, e in b.items():
        out[p] = out.get(p, Fraction(0)) + e
    return {p: e for p, e in out.items() if e != 0}


def to_float(form):
    return sum(float(e) * math.log(p) for p, e in form.items())


def exact_elbo(joint, q):
    """ELBO(q) exactly, for rational joint and q with q(z) > 0 => p(x, z) > 0."""
    terms = []
    for pz, qz in zip(joint, q):
        if qz > 0:
            terms.append((qz, Fraction(pz) / Fraction(qz)))
    return lin_comb(terms)


def exact_kl(q, p):
    """KL(q || p) exactly, for rational q and p with q(z) > 0 => p(z) > 0."""
    return lin_comb([(qz, Fraction(qz) / Fraction(pz)) for qz, pz in zip(q, p) if qz > 0])


def exact_log_evidence(joint):
    return exact_log(sum(Fraction(v) for v in joint))
