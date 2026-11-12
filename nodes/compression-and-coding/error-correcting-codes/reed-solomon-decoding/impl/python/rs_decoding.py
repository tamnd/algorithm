# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reed-solomon-decoding/. The authors are listed in prov/KQB2R4.jsonl.
"""Bounded distance decoding of Reed-Solomon codes with errors and erasures.

The code has length n <= 2^m - 1 (shorter means shortened), nsym = n - k = 2t
check symbols, and the consecutive zeros beta^b, ..., beta^(b+nsym-1) of its
generator, with beta = alpha^step. A word w is the list [w_0, ..., w_{n-1}],
the polynomial w(x) = sum w_i x^i.

Pipeline: syndromes -> error locator (Berlekamp-Massey with erasures, or the
Euclidean algorithm of Sugiyama, Kasahara, Hirasawa and Namekawa) -> Chien
search -> Forney -> check. The decoder corrects any nu errors and rho erasures
with 2 nu + rho <= nsym, and returns None when it detects a failure.
"""

from gf import GF2m


def rs_generator(f: GF2m, nsym: int, b: int = 1, step: int = 1) -> list[int]:
    g = [1]
    for j in range(b, b + nsym):
        g = f.pmul(g, [f.alpha(step * j), 1])
    return g


def rs_encode(f: GF2m, msg: list[int], nsym: int, b: int = 1, step: int = 1) -> list[int]:
    """Systematic encoder: check symbols in positions 0 .. nsym - 1, the message above."""
    g = rs_generator(f, nsym, b, step)
    _, rem = f.pdivmod([0] * nsym + list(msg), g)
    return rem + [0] * (nsym - len(rem)) + list(msg)


def syndromes(f: GF2m, w: list[int], nsym: int, b: int = 1, step: int = 1) -> list[int]:
    """[S_b, ..., S_(b+nsym-1)] with S_j = w(beta^j)."""
    return [f.peval(w, f.alpha(step * j)) for j in range(b, b + nsym)]


def locator(f: GF2m, positions: list[int], step: int = 1) -> list[int]:
    """prod (1 - X x) with X = beta^i for each position i."""
    out = [1]
    for i in positions:
        out = f.pmul(out, [1, f.alpha(step * i)])
    return out


def bm_errors_and_erasures(f: GF2m, syn: list[int], gamma: list[int]) -> tuple[list[int], int]:
    """Berlekamp-Massey started from the erasure locator Gamma (rho = deg Gamma).

    Returns (Psi, L) where Psi = Lambda Gamma is the full locator and L its LFSR length.
    """
    rho = len(gamma) - 1
    psi, bpoly, L, m, bval = list(gamma), list(gamma), rho, 1, 1
    for r in range(rho, len(syn)):
        d = 0
        for j in range(min(L, len(psi) - 1) + 1):
            d ^= f.mul(psi[j], syn[r - j])
        if d == 0:
            m += 1
            continue
        coef = f.div(d, bval)
        new = psi + [0] * max(0, m + len(bpoly) - len(psi))
        for j, c in enumerate(bpoly):
            new[m + j] ^= f.mul(coef, c)
        if 2 * L <= r + rho:
            bpoly, bval, L, m = psi, d, r + 1 + rho - L, 1
        else:
            m += 1
        psi = new
    return f.trim(psi), L


def euclid_errors_and_erasures(f: GF2m, syn: list[int], gamma: list[int]) -> list[int] | None:
    """Sugiyama et al.: Euclid on x^(2t) and Xi = S Gamma mod x^(2t); returns Lambda or None."""
    two_t = len(syn)
    rho = len(gamma) - 1
    xi = f.trim(f.pmul(syn, gamma)[:two_t])
    r_prev, r = [0] * two_t + [1], xi
    v_prev, v = [], [1]
    while 2 * (len(r) - 1) >= two_t + rho:  # stop when deg r < (2t + rho) / 2
        q, rem = f.pdivmod(r_prev, r)
        r_prev, r = r, rem
        v_prev, v = v, f.padd(v_prev, f.pmul(q, v))
    if not v or v[0] == 0:
        return None
    return f.pscale(v, f.inv(v[0]))


def chien(f: GF2m, lam: list[int], n: int, step: int = 1) -> list[int]:
    """Positions i in 0 .. n - 1 with Lambda(beta^(-i)) = 0 (registers times beta^(-j))."""
    regs = list(lam)
    mults = [f.alpha(-step * j) for j in range(len(lam))]
    out = []
    for i in range(n):
        s = 0
        for v in regs:
            s ^= v
        if s == 0:
            out.append(i)
        regs = [f.mul(v, c) for v, c in zip(regs, mults)]
    return out


def forney(f: GF2m, syn: list[int], psi: list[int], positions: list[int], b: int, step: int) -> list[int] | None:
    """Y = X^(1-b) Omega(X^-1) / Psi'(X^-1) in characteristic 2."""
    omega = f.trim(f.pmul(syn, psi)[: len(syn)])
    dpsi = f.pderiv(psi)
    vals = []
    for i in positions:
        x = f.alpha(step * i)
        den = f.peval(dpsi, f.inv(x))
        if den == 0:
            return None
        vals.append(f.mul(f.pow(x, 1 - b), f.div(f.peval(omega, f.inv(x)), den)))
    return vals


def rs_decode(f: GF2m, r: list[int], nsym: int, b: int = 1, step: int = 1,
              erasures: list[int] | None = None, method: str = "bm") -> tuple[list[int], list[int]] | None:
    """Return (codeword, error positions) or None when a decoder failure is detected.

    Precondition: len(r) = n <= 2^m - 1, erasure positions are distinct and in range.
    Corrects nu errors and rho erasures whenever 2 nu + rho <= nsym.
    Cost: O(n nsym) for syndromes and Chien search, O(nsym^2) for the locator and Forney.
    """
    n = len(r)
    erasures = sorted(set(erasures or []))
    rho = len(erasures)
    if rho > nsym:
        return None
    syn = syndromes(f, r, nsym, b, step)
    if not any(syn):
        return list(r), []
    gamma = locator(f, erasures, step)
    if method == "bm":
        psi, L = bm_errors_and_erasures(f, syn, gamma)
        lam, rem = f.pdivmod(psi, gamma)  # Psi = Lambda Gamma exactly
        if rem or len(psi) - 1 != L:
            return None
    elif method == "euclid":
        lam = euclid_errors_and_erasures(f, syn, gamma)
        if lam is None:
            return None
        psi = f.pmul(lam, gamma)
    else:
        raise ValueError("method must be 'bm' or 'euclid'")
    nu = len(lam) - 1
    if 2 * nu + rho > nsym:
        return None
    err_pos = chien(f, lam, n, step)
    if len(err_pos) != nu or set(err_pos) & set(erasures):
        return None  # too few roots in range, or a root on an erasure: a failure
    positions = sorted(err_pos + erasures)
    vals = forney(f, syn, psi, positions, b, step)
    if vals is None:
        return None
    c = list(r)
    for i, y in zip(positions, vals):
        c[i] ^= y
    if any(syndromes(f, c, nsym, b, step)):
        return None
    return c, err_pos
