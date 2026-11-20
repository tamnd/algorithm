# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/desroziers-diagnostics/. The authors are listed in prov/YFJDYK.jsonl.

"""Desroziers diagnostics of the observation and background error covariances.

Notation of Ide, Courtier, Ghil and Lorenc (1997). Everything is in
observation space. For one analysis, with the background x^b, the analysis
x^a and the observations y:

    d^o_b = y - H x^b          innovation (observation minus background)
    d^a_b = H x^a - H x^b      analysis increment in observation space
    d^o_a = y - H x^a          analysis residual (observation minus analysis)

A linear analysis with the assumed covariances Bt (written here as its
observation space form HBtH^T) and Rt has d^a_b = HBtH^T St^-1 d^o_b, with
St = HBtH^T + Rt. If the assumed covariances are the true ones, the sample
means over many analyses estimate

    E[d^o_a d^o_b^T] = R,           E[d^a_b d^o_b^T] = H B H^T,
    E[d^a_b d^o_a^T] = H A H^T,     E[d^o_b d^o_b^T] = H B H^T + R.

For assumed covariances that are not the true ones, the expected values are
given by expected_statistics. All the routines keep Fraction entries exact.
"""

from fractions import Fraction

import scimat


def gain_in_observation_space(hbht, r):
    """Return G = HBH^T (HBH^T + R)^-1, so that d^a_b = G d^o_b."""
    s = scimat.add(hbht, r)
    # G = HBH^T S^-1, and S and HBH^T are symmetric, so G^T = S^-1 HBH^T.
    return scimat.transpose(scimat.solve(s, hbht))


def desroziers(innovations, hbht, r):
    """Return the sample estimates (R, HBH^T, HAH^T, HBH^T + R) from the innovations.

    Each innovation d^o_b goes through the linear analysis with the assumed
    covariances hbht and r to give d^a_b and d^o_a.
    """
    p = len(r)
    g = gain_in_observation_space(hbht, r)  # @line L1
    sums = {key: scimat.zeros(p) for key in ("oa_ob", "ab_ob", "ab_oa", "ob_ob")}
    for d_ob in innovations:  # @line L2
        d_ab = scimat.matvec(g, d_ob)  # @line L3
        d_oa = scimat.sub(d_ob, d_ab)  # @line L4
        sums["oa_ob"] = scimat.add(sums["oa_ob"], scimat.outer(d_oa, d_ob))  # @line L5
        sums["ab_ob"] = scimat.add(sums["ab_ob"], scimat.outer(d_ab, d_ob))
        sums["ab_oa"] = scimat.add(sums["ab_oa"], scimat.outer(d_ab, d_oa))
        sums["ob_ob"] = scimat.add(sums["ob_ob"], scimat.outer(d_ob, d_ob))
    w = Fraction(1, len(innovations))  # a Fraction times a float is a float
    est = {key: scimat.scale(w, s) for key, s in sums.items()}  # @line L6
    return est["oa_ob"], est["ab_ob"], est["ab_oa"], est["ob_ob"]  # @line L7


def expected_statistics(hbht_true, r_true, hbht, r):
    """Return the exact expected values of the four sample estimates of desroziers.

    The innovations have the true covariance S = HBH^T + R, and the analysis
    uses the assumed hbht and r. With St = hbht + r:
        E[d^o_a d^o_b^T] = r St^-1 S
        E[d^a_b d^o_b^T] = hbht St^-1 S
        E[d^a_b d^o_a^T] = hbht St^-1 S St^-1 r
        E[d^o_b d^o_b^T] = S
    """
    s = scimat.add(hbht_true, r_true)
    st = scimat.add(hbht, r)
    st_inv_s = scimat.solve(st, s)
    oa_ob = scimat.matmul(r, st_inv_s)
    ab_ob = scimat.matmul(hbht, st_inv_s)
    ab_oa = scimat.matmul(ab_ob, scimat.solve(st, r))
    return oa_ob, ab_ob, ab_oa, s


def symmetric_part(a):
    """Return (a + a^T) / 2."""
    at = scimat.transpose(a)
    return [[(x + y) / 2 for x, y in zip(ra, rb)] for ra, rb in zip(a, at)]


def tune(hbht_true, r_true, hbht, r, steps, tune_b=False):
    """Iterate r <- E[d^o_a d^o_b^T] (and hbht <- E[d^a_b d^o_b^T] if tune_b) with exact expectations.

    Return the list of (hbht, r) pairs, starting with the given ones.
    """
    out = [(hbht, r)]
    for _ in range(steps):
        oa_ob, ab_ob, _, _ = expected_statistics(hbht_true, r_true, hbht, r)
        new_r = symmetric_part(oa_ob)
        if tune_b:
            hbht = symmetric_part(ab_ob)
        r = new_r
        out.append((hbht, r))
    return out
