# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prediction-error-method/. The authors are listed in prov/R82NR4.jsonl.

"""Prediction error method for the general linear black-box model.

The model is

    A(q) y(t) = (B(q) / F(q)) u(t) + (C(q) / D(q)) e(t)

with A = 1 + a_1 q^-1 + ... + a_na q^-na, and the same form for C, D and F.
B(q) = b_1 q^-nk + ... + b_nb q^-(nk+nb-1). ARX, ARMAX, OE and Box-Jenkins
are the special cases with some orders set to 0.

The one step ahead prediction error is

    eps(t) = (D / C) (A y(t) - (B / F) u(t)),

computed from rest (all signals 0 before t = 0). pem minimizes
V = (1/M) sum of eps(t)^2 over t = n0, ..., N-1, n0 = max(na, nk + nb - 1,
nc, nd, nf), by damped Gauss-Newton steps. C and F are kept Schur (all zeros
strictly inside the unit circle), so the filters stay bounded.

Precondition: nb >= 1, nk >= 0, the other orders >= 0, len(y) == len(u) and
the data are informative for the model. The start value must have C and F
Schur. The result is a local minimum of V; V need not be convex.

Cost per iteration: O(N d) to filter the data and O(N d^2 + d^3) for the
Gauss-Newton step, d = na + nb + nc + nd + nf, in the real RAM.
"""

from typing import Optional, Sequence

from ctlmat import polymul, polyroots, solve


def _filter(num: Sequence, den: Sequence, x: Sequence) -> list:
    """Return (num(q^-1) / den(q^-1)) x from rest; den[0] must be 1."""
    out = []
    for t in range(len(x)):
        s = 0.0
        for i, c in enumerate(num):
            if t - i < 0:
                break
            s += c * x[t - i]
        for i in range(1, len(den)):
            if t - i < 0:
                break
            s -= den[i] * out[t - i]
        out.append(s)
    return out


def _lag(x: Sequence, k: int, t: int) -> float:
    return x[t - k] if t - k >= 0 else 0.0


def is_schur(poly: Sequence) -> bool:
    """True if every zero of 1 + p_1 z^-1 + ... + p_n z^-n has modulus < 1."""
    if len(poly) <= 1:
        return True
    return all(abs(r) < 1.0 for r in polyroots(list(poly)))


def _split(theta: Sequence, na: int, nb: int, nc: int, nd: int, nf: int):
    i = 0
    parts = []
    for n in (na, nb, nc, nd, nf):
        parts.append(list(theta[i:i + n]))
        i += n
    return parts


def prediction_errors(theta: Sequence, y: Sequence, u: Sequence, na: int, nb: int,
                      nc: int = 0, nd: int = 0, nf: int = 0, nk: int = 1):
    """Return (eps, w, v) for the parameter vector theta = (a, b, c, d, f).

    w = (B / F) u is the noise-free model output, v = A y - w and
    eps = (D / C) v is the prediction error.
    """
    a, b, c, d, f = _split(theta, na, nb, nc, nd, nf)
    apol, cpol, dpol, fpol = [1.0] + a, [1.0] + c, [1.0] + d, [1.0] + f
    bpol = [0.0] * nk + b
    w = _filter(bpol, fpol, u)
    ay = _filter(apol, [1.0], y)
    v = [p - q for p, q in zip(ay, w)]
    eps = _filter(dpol, cpol, v)
    return eps, w, v


def _gradients(theta, y, u, eps, w, v, na, nb, nc, nd, nf, nk):
    """Return the filtered signals that give psi(t) = -d eps(t) / d theta."""
    _, _, c, d, f = _split(theta, na, nb, nc, nd, nf)
    cpol, dpol, fpol = [1.0] + c, [1.0] + d, [1.0] + f
    cf = polymul(cpol, fpol)
    yf = _filter(dpol, cpol, y)
    uf = _filter(dpol, cf, u)
    wf = _filter(dpol, cf, w)
    ef = _filter([1.0], cpol, eps)
    vf = _filter([1.0], cpol, v)
    return yf, uf, wf, ef, vf


def _psi(t, sig, na, nb, nc, nd, nf, nk):
    yf, uf, wf, ef, vf = sig
    return ([-_lag(yf, k, t) for k in range(1, na + 1)]
            + [_lag(uf, nk + k, t) for k in range(nb)]
            + [_lag(ef, k, t) for k in range(1, nc + 1)]
            + [-_lag(vf, k, t) for k in range(1, nd + 1)]
            + [-_lag(wf, k, t) for k in range(1, nf + 1)])


def first_sample(na: int, nb: int, nc: int, nd: int, nf: int, nk: int) -> int:
    """Return n0, the first sample used in the cost."""
    return max(na, nk + nb - 1, nc, nd, nf)


def pem_loss(theta: Sequence, y: Sequence, u: Sequence, na: int, nb: int,
             nc: int = 0, nd: int = 0, nf: int = 0, nk: int = 1) -> float:
    """Return V(theta) = mean of eps(t)^2 over t >= n0."""
    eps, _, _ = prediction_errors(theta, y, u, na, nb, nc, nd, nf, nk)
    n0 = first_sample(na, nb, nc, nd, nf, nk)
    return sum(e * e for e in eps[n0:]) / (len(eps) - n0)


def _arx_start(y, u, na, nb, nc, nd, nf, nk):
    """Start value from a least squares ARX fit; c = d = 0."""
    n_ar = na if na > 0 else nf
    n0 = max(n_ar, nk + nb - 1)
    p = n_ar + nb
    r = [[0.0] * p for _ in range(p)]
    g = [0.0] * p
    for t in range(n0, len(y)):
        phi = [-y[t - i] for i in range(1, n_ar + 1)] + [u[t - nk - j] for j in range(nb)]
        for i in range(p):
            for j in range(p):
                r[i][j] += phi[i] * phi[j]
            g[i] += phi[i] * y[t]
    est = solve(r, g)
    ar, bb = est[:n_ar], est[n_ar:]
    a = ar if na > 0 else []
    f = ar if na == 0 else [0.0] * nf
    if nf > 0 and not is_schur([1.0] + f):
        f = [0.0] * nf
    return a + bb + [0.0] * nc + [0.0] * nd + f


def pem(y: Sequence, u: Sequence, na: int, nb: int, nc: int = 0, nd: int = 0,
        nf: int = 0, nk: int = 1, theta0: Optional[Sequence] = None,
        maxiter: int = 100, tol: float = 1e-12) -> dict:
    """Minimize the prediction error cost by damped Gauss-Newton.

    Returns a dict with the polynomials "a", "b", "c", "d", "f" (without the
    leading 1), the vector "theta", the cost "loss" and the number of
    accepted steps "iterations". Raises ValueError if the Gauss-Newton matrix
    is singular (the data are not informative) or theta0 is not admissible.
    """
    if nb < 1 or min(na, nc, nd, nf, nk) < 0:
        raise ValueError("need nb >= 1 and all other orders >= 0")
    if len(y) != len(u):
        raise ValueError("y and u must have the same length")
    dim = na + nb + nc + nd + nf
    n0 = first_sample(na, nb, nc, nd, nf, nk)
    if len(y) - n0 <= dim:
        raise ValueError("too few samples for the model orders")
    if theta0 is None:
        theta = _arx_start(y, u, na, nb, nc, nd, nf, nk)  # @line L1
    else:
        theta = [float(v) for v in theta0]
    if len(theta) != dim:
        raise ValueError("theta0 has the wrong length")

    def admissible(th):
        _, _, c, _, f = _split(th, na, nb, nc, nd, nf)
        return is_schur([1.0] + c) and is_schur([1.0] + f)

    if not admissible(theta):
        raise ValueError("start value must have C and F Schur")
    loss = pem_loss(theta, y, u, na, nb, nc, nd, nf, nk)
    steps = 0
    for _ in range(maxiter):  # @line L2
        eps, w, v = prediction_errors(theta, y, u, na, nb, nc, nd, nf, nk)  # @line L3
        sig = _gradients(theta, y, u, eps, w, v, na, nb, nc, nd, nf, nk)
        r = [[0.0] * dim for _ in range(dim)]
        g = [0.0] * dim
        for t in range(n0, len(y)):
            psi = _psi(t, sig, na, nb, nc, nd, nf, nk)
            for i in range(dim):
                pi = psi[i]
                row = r[i]
                for j in range(dim):
                    row[j] += pi * psi[j]  # @line L4
                g[i] += pi * eps[t]
        try:
            delta = solve(r, g)  # @line L5
        except ValueError:
            raise ValueError("Gauss-Newton matrix is singular: the data are not informative") from None
        mu = 1.0  # @line L6
        accepted = False
        for _ in range(40):
            cand = [th + mu * dl for th, dl in zip(theta, delta)]
            if admissible(cand):
                new_loss = pem_loss(cand, y, u, na, nb, nc, nd, nf, nk)
                if new_loss < loss:
                    accepted = True
                    break
            mu /= 2.0  # @line L7
        if not accepted:
            break
        theta = cand  # @line L8
        old, loss = loss, new_loss
        steps += 1
        if old - loss <= tol * old:  # @line L9
            break
    a, b, c, d, f = _split(theta, na, nb, nc, nd, nf)
    return {"a": a, "b": b, "c": c, "d": d, "f": f, "theta": theta,
            "loss": loss, "iterations": steps}  # @line L10


def simulate_general(a: Sequence, b: Sequence, c: Sequence, d: Sequence, f: Sequence,
                     nk: int, u: Sequence, e: Sequence) -> list:
    """Return y with A y = (B / F) u + (C / D) e, from rest."""
    w = _filter([0.0] * nk + list(b), [1.0] + list(f), u)
    n = _filter([1.0] + list(c), [1.0] + list(d), e)
    s = [p + q for p, q in zip(w, n)]
    return _filter([1.0], [1.0] + list(a), s)
