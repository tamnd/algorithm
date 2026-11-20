# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quasicontinuum-method/. The authors are listed in prov/7F8PW8.jsonl.
"""The quasicontinuum method on a one-dimensional chain of atoms.

The chain has atoms 0, 1, ..., N - 1 at the reference sites X_i = i a,
with a pair potential on the nearest neighbor bonds (i, i + 1) and, if
nnn is true, on the second neighbor bonds (i, i + 2). A bond can carry a
scale factor (a weak bond is a simple defect).

The repatoms are a sorted list R of atom indices. The positions of all
atoms follow from the repatom positions z by linear interpolation,
y = T z. A subset A of the repatoms is nonlocal (atomistic). The other
atoms are local: their energy is the Cauchy-Born energy per atom
W(F) = phi(F a) + phi(2 F a) of the element that holds them.

Energy-based QC (QCE, Tadmor, Ortiz and Phillips 1996, with the local and
nonlocal repatoms of Shenoy et al. 1999):

    E_QCE(z) = sum over bonds b of c_b phi_b(y_j - y_i)
             + sum over elements e of w_e W(F_e),

    c_b = (number of ends of b in A) / 2,
    w_e = n_e - (number of ends of e in A) / 2,

where n_e is the number of lattice spacings in the element and F_e is its
deformation gradient. This is the sum of the atom energies: half of each
bond for a nonlocal atom, W(F) for a local atom inside an element, and
the mean of W over the two elements for a local repatom.

Force-based QC (QCF): the force on a nonlocal repatom is the exact
atomistic force at y = T z, and the force on a local repatom is the force
of the pure local energy sum n_e W(F_e). QCF has no energy, so its
Newton matrix is not symmetric.

A pair potential is a function r -> (phi(r), phi'(r), phi''(r)).
The two end atoms must be nonlocal repatoms, and the caller lists the
fixed repatoms (the boundary conditions).
"""

from typing import Callable, Sequence

import scimat

Pair = Callable[[float], tuple[float, float, float]]


def lennard_jones(r: float, epsilon: float = 1.0, sigma: float = 1.0) -> tuple[float, float, float]:
    """phi(r) = 4 epsilon ((sigma/r)^12 - (sigma/r)^6) and its first two derivatives."""
    s6 = (sigma / r) ** 6
    s12 = s6 * s6
    return (4.0 * epsilon * (s12 - s6),
            4.0 * epsilon * (-12.0 * s12 + 6.0 * s6) / r,
            4.0 * epsilon * (156.0 * s12 - 42.0 * s6) / (r * r))


class Chain:
    """A chain of n atoms with spacing a, a pair potential, and optional weak bonds."""

    def __init__(self, n: int, a: float, pair: Pair, nnn: bool = True,
                 scale: dict | None = None) -> None:
        self.n = n
        self.a = a
        self.pair = pair
        self.nnn = nnn
        self.scale = dict(scale or {})

    def bonds(self) -> list[tuple[int, int, float]]:
        """All bonds (i, j, s) with i < j and scale factor s."""
        out = []
        reach = 2 if self.nnn else 1
        for i in range(self.n):
            for j in range(i + 1, min(i + reach, self.n - 1) + 1):
                out.append((i, j, self.scale.get((i, j), 1.0)))
        return out

    def cauchy_born(self, f: float) -> tuple[float, float, float]:
        """W(F) per atom for the uniform state y = F X, and W'(F), W''(F)."""
        a = self.a
        v1, d1, s1 = self.pair(f * a)
        w, dw, d2w = v1, a * d1, a * a * s1
        if self.nnn:
            v2, d2, s2 = self.pair(2.0 * f * a)
            w, dw, d2w = w + v2, dw + 2.0 * a * d2, d2w + 4.0 * a * a * s2
        return w, dw, d2w


def interpolation(n: int, rep: Sequence[int]) -> list[list[tuple[int, float]]]:
    """Row i of T as a list of (repatom index k, weight): y_i = sum w z_k."""
    rows: list[list[tuple[int, float]]] = []
    k = 0
    for i in range(n):
        while k + 1 < len(rep) and rep[k + 1] <= i:
            k += 1
        p = rep[k]
        if p == i:
            rows.append([(k, 1.0)])
        else:
            q = rep[k + 1]
            w = (i - p) / (q - p)
            rows.append([(k, 1.0 - w), (k + 1, w)])
    return rows


def _check(chain: Chain, rep: Sequence[int], nonlocal_set: set) -> None:
    if list(rep) != sorted(set(rep)) or rep[0] != 0 or rep[-1] != chain.n - 1:
        raise ValueError("repatoms must be sorted, distinct, and contain both ends")
    if not nonlocal_set <= set(rep) or 0 not in nonlocal_set or chain.n - 1 not in nonlocal_set:
        raise ValueError("nonlocal atoms must be repatoms and contain both ends")
    for (i, j), s in chain.scale.items():
        if s != 1.0 and not (i in nonlocal_set and j in nonlocal_set):
            raise ValueError("a scaled bond must join two nonlocal atoms")


def positions(t_rows, z: Sequence[float]) -> list[float]:
    """y = T z."""
    return [sum(w * z[k] for k, w in row) for row in t_rows]


def qce_weights(chain: Chain, rep: Sequence[int], nonlocal_set: set):
    """The bond weights c_b (bonds with c_b > 0 only) and the element weights w_e."""
    cb = []
    for i, j, s in chain.bonds():
        c = 0.5 * ((i in nonlocal_set) + (j in nonlocal_set))
        if c > 0.0:
            cb.append((i, j, c * s))
    we = []
    for k in range(len(rep) - 1):
        p, q = rep[k], rep[k + 1]
        we.append((q - p) - 0.5 * ((p in nonlocal_set) + (q in nonlocal_set)))
    return cb, we


def _add_bond(t_rows, g, kmat, i, j, dv, d2v):
    """Add the gradient and Hessian of one bond energy, pulled back by T."""
    for a_idx, sa in ((i, -1.0), (j, 1.0)):
        for k, w in t_rows[a_idx]:
            g[k] += sa * w * dv
            if kmat is not None:
                for b_idx, sb in ((i, -1.0), (j, 1.0)):
                    for m, u in t_rows[b_idx]:
                        kmat[k][m] += sa * sb * w * u * d2v


def qce_energy(chain: Chain, rep, nonlocal_set, z) -> float:
    """E_QCE(z)."""
    t_rows = interpolation(chain.n, rep)
    y = positions(t_rows, z)
    cb, we = qce_weights(chain, rep, nonlocal_set)
    e = sum(c * chain.pair(y[j] - y[i])[0] for i, j, c in cb)
    for k, w in enumerate(we):
        if w != 0.0:
            ne = rep[k + 1] - rep[k]
            e += w * chain.cauchy_born((z[k + 1] - z[k]) / (ne * chain.a))[0]
    return e


def qce_gradient_hessian(chain: Chain, rep, nonlocal_set, z, hessian: bool = True):
    """The gradient of E_QCE with respect to z and, if asked, its Hessian."""
    m = len(rep)
    t_rows = interpolation(chain.n, rep)
    y = positions(t_rows, z)
    cb, we = qce_weights(chain, rep, nonlocal_set)
    g = [0.0] * m
    kmat = [[0.0] * m for _ in range(m)] if hessian else None
    for i, j, c in cb:
        _, dv, d2v = chain.pair(y[j] - y[i])
        _add_bond(t_rows, g, kmat, i, j, c * dv, c * d2v)
    for k, w in enumerate(we):
        if w == 0.0:
            continue
        h = (rep[k + 1] - rep[k]) * chain.a
        _, dw, d2w = chain.cauchy_born((z[k + 1] - z[k]) / h)
        g[k] -= w * dw / h
        g[k + 1] += w * dw / h
        if kmat is not None:
            s = w * d2w / (h * h)
            kmat[k][k] += s
            kmat[k + 1][k + 1] += s
            kmat[k][k + 1] -= s
            kmat[k + 1][k] -= s
    return g, kmat


def qcf_residual_jacobian(chain: Chain, rep, nonlocal_set, z):
    """QCF: minus the forces on the repatoms, and the Jacobian of that residual."""
    m = len(rep)
    t_rows = interpolation(chain.n, rep)
    y = positions(t_rows, z)
    index = {p: k for k, p in enumerate(rep)}
    r = [0.0] * m
    jac = [[0.0] * m for _ in range(m)]
    for i, j, s in chain.bonds():
        for atom, sa in ((i, -1.0), (j, 1.0)):
            if atom not in nonlocal_set:
                continue
            k = index[atom]
            _, dv, d2v = chain.pair(y[j] - y[i])
            r[k] += sa * s * dv
            for b_idx, sb in ((i, -1.0), (j, 1.0)):
                for mm, u in t_rows[b_idx]:
                    jac[k][mm] += sa * sb * u * s * d2v
    for k in range(m - 1):
        h = (rep[k + 1] - rep[k]) * chain.a
        _, dw, d2w = chain.cauchy_born((z[k + 1] - z[k]) / h)
        ne = rep[k + 1] - rep[k]
        for kk, sk in ((k, -1.0), (k + 1, 1.0)):
            if rep[kk] in nonlocal_set:
                continue
            r[kk] += sk * ne * dw / h
            jac[kk][k] -= sk * ne * d2w / (h * h)
            jac[kk][k + 1] += sk * ne * d2w / (h * h)
    return r, jac


def quasicontinuum(chain: Chain, rep: Sequence[int], nonlocal_set, z0: Sequence[float],
                   fixed: Sequence[int], method: str = "qce", tol: float = 1e-10,
                   max_iter: int = 50) -> tuple[list[float], list[float]]:
    """Solve for the repatom positions z by Newton's method.

    rep: sorted repatom indices; nonlocal_set: the nonlocal repatoms;
    z0: start positions of the repatoms (the fixed ones keep their value);
    fixed: indices into rep of the fixed repatoms; method: "qce" (minimize
    E_QCE) or "qcf" (zero the QCF forces). Return (z, y) with y = T z.
    """
    nonlocal_set = set(nonlocal_set)
    _check(chain, rep, nonlocal_set)
    t_rows = interpolation(chain.n, rep)                                 # @line L1
    if method == "qce":
        qce_weights(chain, rep, nonlocal_set)                            # @line L2
    z = [float(v) for v in z0]
    free = [k for k in range(len(rep)) if k not in set(fixed)]
    for _ in range(max_iter):                                            # @line L3
        y = positions(t_rows, z)                                         # @line L4
        if method == "qce":
            g, kmat = qce_gradient_hessian(chain, rep, nonlocal_set, z)  # @line L5
        else:
            g, kmat = qcf_residual_jacobian(chain, rep, nonlocal_set, z)
        gf = [g[k] for k in free]
        if max(abs(v) for v in gf) < tol:                                # @line L9
            return z, y                                                  # @line L10
        kff = [[kmat[k][m] for m in free] for k in free]                 # @line L6
        delta = scimat.solve(kff, [-v for v in gf])                      # @line L7
        for k, d in zip(free, delta):                                    # @line L8
            z[k] += d
    raise RuntimeError("Newton iteration did not converge")


def full_atomistic(chain: Chain, y0: Sequence[float], fixed: Sequence[int],
                   tol: float = 1e-10) -> list[float]:
    """The exact atomistic equilibrium: QC with every atom a nonlocal repatom."""
    rep = list(range(chain.n))
    z, _ = quasicontinuum(chain, rep, set(rep), y0, fixed, "qce", tol)
    return z
