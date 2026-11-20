# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arc-length-method/. The authors are listed in prov/J4J4WD.jsonl.

"""Arc-length continuation (Riks 1979, Crisfield 1981) for f_int(u) = lam P.

The unknowns are the displacements u (a list) and the load factor lam. Each
step moves a distance dl along the equilibrium path, measured by
    |Du|^2 + psi^2 Dlam^2 |P|^2 = dl^2,
and corrects with Newton iterations that keep this constraint (Crisfield's
spherical form; psi = 0 gives the cylindrical form). Matrices are lists of
rows, as in scimat.
"""

import math

import scimat


def arc_length(fint, tangent, P, u0, dl, nsteps, psi=1.0, tol=1e-10, maxit=25, lam0=0.0):
    """Trace the equilibrium path of fint(u) = lam P from (u0, lam0).

    tangent(u) returns d fint / d u. Return a list of (u, lam, iterations), the
    start point included. A step whose quadratic has no real root, or whose
    Newton iteration does not converge, is retried with half the arc length.
    """
    n = len(u0)
    pp = scimat.dot(P, P)
    u, lam = list(u0), lam0  # @line L1
    path = [(list(u), lam, 0)]
    prev = None  # previous increment (Du, Dlam)
    step = 0
    length = dl
    while step < nsteps:  # @line L2
        ut = scimat.solve(tangent(u), P)  # @line L3
        dlam = length / math.sqrt(scimat.dot(ut, ut) + psi * psi * pp)
        if prev is not None and scimat.dot(prev[0], ut) + psi * psi * prev[1] * pp < 0:
            dlam = -dlam  # keep going forward along the path
        du = scimat.scale(dlam, ut)  # @line L4
        ok = False
        for it in range(maxit):  # @line L5
            g = scimat.sub(fint(scimat.add(u, du)), scimat.scale(lam + dlam, P))  # @line L6
            if scimat.norm2(g) <= tol * (1 + abs(lam + dlam) * math.sqrt(pp)):
                ok = True
                break
            kt = tangent(scimat.add(u, du))
            sol = scimat.solve(kt, [[-gi, pi] for gi, pi in zip(g, P)])  # @line L7
            ur = [row[0] for row in sol]
            ut = [row[1] for row in sol]
            root = _constraint_root(du, dlam, ur, ut, pp, psi, length)  # @line L8
            if root is None:
                break
            du = [du[i] + ur[i] + root * ut[i] for i in range(n)]  # @line L9
            dlam += root
        if not ok:
            length /= 2
            if length < dl * 1e-6:
                raise RuntimeError("arc-length step failed")
            continue
        u = scimat.add(u, du)  # @line L10
        lam += dlam
        prev = (du, dlam)
        path.append((list(u), lam, it))
        step += 1
        length = dl
    return path  # @line L11


def _constraint_root(du, dlam, ur, ut, pp, psi, length):
    """Return the correction dmu of the load factor that keeps the arc length.

    The new increment is du + ur + dmu ut. Of the two roots of the quadratic,
    take the one whose new increment makes the smaller angle with du (Crisfield).
    Return None if the roots are not real.
    """
    w = scimat.add(du, ur)
    a = scimat.dot(ut, ut) + psi * psi * pp
    b = 2 * (scimat.dot(ut, w) + psi * psi * dlam * pp)
    c = scimat.dot(w, w) + psi * psi * dlam * dlam * pp - length * length
    disc = b * b - 4 * a * c
    if disc < 0:
        return None
    s = math.sqrt(disc)
    # stable formulas for the two roots
    q = -(b + math.copysign(s, b)) / 2
    roots = [q / a, c / q] if q != 0 else [0.0, 0.0]

    def cosine(mu):
        new = [w[i] + mu * ut[i] for i in range(len(w))]
        return scimat.dot(new, du) + psi * psi * (dlam + mu) * dlam * pp

    return max(roots, key=cosine)


def load_control(fint, tangent, P, u0, lams, tol=1e-10, maxit=50):
    """Newton's method at each prescribed load factor in lams, from the last solution.

    Return a list of (u, lam, iterations). Raise RuntimeError if Newton does not converge.
    """
    u = list(u0)
    out = []
    for lam in lams:
        for it in range(maxit):
            g = scimat.sub(fint(u), scimat.scale(lam, P))
            if scimat.norm2(g) <= tol * (1 + abs(lam) * scimat.norm2(P)):
                break
            u = scimat.sub(u, scimat.solve(tangent(u), g))
        else:
            raise RuntimeError("Newton did not converge at lam = %r" % lam)
        out.append((list(u), lam, it))
    return out


def von_mises_truss(EA=1.0, L=1.0, H=0.5):
    """Return (fint, tangent) of the symmetric two-bar truss with one degree of freedom.

    The bars go from (-L, 0) and (L, 0) to the apex (0, H). u = [w] is the
    downward displacement of the apex, and fint is the upward resisting force
    2 EA y (1/l - 1/l0) with y = H - w, l = sqrt(L^2 + y^2), l0 = sqrt(L^2 + H^2).
    """
    l0 = math.hypot(L, H)

    def fint(u):
        y = H - u[0]
        l = math.hypot(L, y)
        return [2 * EA * y * (1 / l - 1 / l0)]

    def tangent(u):
        y = H - u[0]
        l = math.hypot(L, y)
        return [[-2 * EA * (L * L / l ** 3 - 1 / l0)]]

    return fint, tangent


def von_mises_limit_point(EA=1.0, L=1.0, H=0.5):
    """Return (w, load) at the first limit point of the truss, in closed form.

    d fint / d y = 2 EA (L^2 / l^3 - 1 / l0) is zero at l^3 = L^2 l0.
    """
    l0 = math.hypot(L, H)
    l = (L * L * l0) ** (1 / 3)
    y = math.sqrt(l * l - L * L)
    return H - y, 2 * EA * y * (1 / l - 1 / l0)


def truss_with_spring(k, EA=1.0, L=1.0, H=0.5):
    """Return (fint, tangent) of the truss loaded through a vertical spring of stiffness k.

    u = [w, z]: w is the apex displacement and z the displacement of the loaded
    end of the spring, both downward. The load acts on z, so P = [0, 1].
    The path has a snap-back in z when k is smaller than the largest softening slope.
    """
    f1, t1 = von_mises_truss(EA, L, H)

    def fint(u):
        s = k * (u[1] - u[0])
        return [f1([u[0]])[0] - s, s]

    def tangent(u):
        kt = t1([u[0]])[0][0]
        return [[kt + k, -k], [-k, k]]

    return fint, tangent
