# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/peterson-gorenstein-zierler/. The authors are listed in prov/7Z5YDC.jsonl.
"""The Peterson-Gorenstein-Zierler decoder for Reed-Solomon and BCH codes over GF(2^m).

The code has length n <= 2^m - 1 and the zeros beta^b, ..., beta^(b+2t-1) with
beta = alpha^step. A word w is the list [w_0, ..., w_{n-1}], the polynomial
w(x) = sum w_i x^i. An error at position i has the locator X = beta^i.

The decoder solves the Hankel system M_nu Lambda = S for the error locator,
with nu reduced from t until M_nu is nonsingular (Peterson), finds the roots of
Lambda, and solves a Vandermonde system for the error values (Gorenstein and
Zierler). Over GF(2^m), minus is plus, so -S is S.
"""

from gf import GF2m


def syndromes(f: GF2m, w: list[int], nsym: int, b: int = 1, step: int = 1) -> list[int]:
    """[S_b, ..., S_(b+nsym-1)] with S_j = w(beta^j)."""
    return [f.peval(w, f.alpha(step * j)) for j in range(b, b + nsym)]


def hankel(syn: list[int], nu: int) -> list[list[int]]:
    """M_nu[i][j] = S_(b+i+j) for 0 <= i, j < nu (syn[0] is S_b)."""
    return [[syn[i + j] for j in range(nu)] for i in range(nu)]


def solve(f: GF2m, a: list[list[int]], y: list[int]) -> list[int] | None:
    """Gaussian elimination: the x with a x = y, or None when a is singular. O(nu^3)."""
    size = len(a)
    rows = [list(a[i]) + [y[i]] for i in range(size)]
    for col in range(size):
        piv = next((r for r in range(col, size) if rows[r][col]), None)
        if piv is None:
            return None
        rows[col], rows[piv] = rows[piv], rows[col]
        inv = f.inv(rows[col][col])
        rows[col] = [f.mul(v, inv) for v in rows[col]]
        for r in range(size):
            if r != col and rows[r][col]:
                c = rows[r][col]
                rows[r] = [v ^ f.mul(c, p) for v, p in zip(rows[r], rows[col])]
    return [rows[i][size] for i in range(size)]


def rank(f: GF2m, a: list[list[int]]) -> int:
    """The rank of a square or rectangular matrix over GF(2^m)."""
    rows = [list(r) for r in a]
    rk = 0
    for col in range(len(rows[0]) if rows else 0):
        piv = next((r for r in range(rk, len(rows)) if rows[r][col]), None)
        if piv is None:
            continue
        rows[rk], rows[piv] = rows[piv], rows[rk]
        inv = f.inv(rows[rk][col])
        rows[rk] = [f.mul(v, inv) for v in rows[rk]]
        for r in range(len(rows)):
            if r != rk and rows[r][col]:
                c = rows[r][col]
                rows[r] = [v ^ f.mul(c, p) for v, p in zip(rows[r], rows[rk])]
        rk += 1
    return rk


def pgz_locator(f: GF2m, syn: list[int]) -> list[int]:
    """Peterson's step: [1, Lambda_1, ..., Lambda_nu] for the largest nu <= t with M_nu nonsingular."""
    nu = len(syn) // 2
    while nu > 0:
        coeffs = solve(f, hankel(syn, nu), syn[nu: 2 * nu])
        if coeffs is not None:
            return [1] + coeffs[::-1]  # the unknowns are (Lambda_nu, ..., Lambda_1)
        nu -= 1
    return [1]


def pgz_decode(f: GF2m, r: list[int], nsym: int, b: int = 1,
               step: int = 1) -> tuple[list[int], list[int], list[int]] | None:
    """Return (codeword, error positions, error values), or None for a detected failure.

    Precondition: len(r) = n <= 2^m - 1, nsym = 2t, and the code has the zeros
    beta^b, ..., beta^(b+nsym-1). Corrects every pattern of at most t errors.
    Cost: O(n t) for syndromes and the root search; O(nu^3) per trial of the
    loop, O(t^4) in the worst case over all trials, and O(nu^3) for the values.
    """
    n = len(r)
    syn = syndromes(f, r, nsym, b, step)
    t = nsym // 2
    nu = t  # @line L1
    coeffs = None
    while nu > 0:  # @line L2: reduce nu until M_nu is nonsingular
        # One elimination tests M_nu and, if it is nonsingular, also gives the solution of line L4.
        coeffs = solve(f, hankel(syn, nu), syn[nu: 2 * nu])
        if coeffs is not None:
            break
        nu -= 1
    if nu == 0:  # @line L3
        return (list(r), [], []) if not any(syn) else None
    lam = [1] + coeffs[::-1]  # @line L4: the unknowns are (Lambda_nu, ..., Lambda_1)
    pos = [i for i in range(n) if f.peval(lam, f.alpha(-step * i)) == 0]  # @line L5: roots beta^(-i)
    if len(pos) != nu:  # @line L6
        return None
    xs = [f.alpha(step * i) for i in pos]
    vand = [[f.pow(x, b + i) for x in xs] for i in range(nu)]
    vals = solve(f, vand, syn[:nu])  # @line L7: sum_k Y_k X_k^(b+i) = S_(b+i)
    if vals is None or 0 in vals:
        return None
    c = list(r)
    for i, y in zip(pos, vals):
        c[i] ^= y
    if any(syndromes(f, c, nsym, b, step)):
        return None
    return c, pos, vals  # @line L8
