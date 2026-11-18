# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/provot-strain-limiting/. The authors are listed in prov/SR6S3F.jsonl.

"""Provot's strain limiting on a 2D mass-spring system.

After an explicit step, each spring longer than (1 + tau) L is shortened by
moving its ends along the spring (Provot 1995, Section 5). Both ends free: both
move, by half the excess each in Provot's rule. One end fixed: only the free end
moves. Both ends fixed: nothing changes. The springs are visited in order and
each correction uses the positions that the earlier corrections left
(Gauss-Seidel). A sweep can be repeated.

A spring (a, b, rest, k) is a tuple. A particle with inverse mass 0 is fixed.
Positions are (x, y) in metres with y up.
"""

import math

GRAVITY = (0.0, -9.81)


def strain(x, spring):
    """(l - L) / L for one spring."""
    a, b, rest = spring[0], spring[1], spring[2]
    return (math.dist(x[a], x[b]) - rest) / rest


def max_strain(x, springs):
    return max(strain(x, s) for s in springs)


def correct_spring(x, inv_mass, spring, target, weights="equal"):
    """Shorten one spring to the length target if it is longer. Change x in place.

    weights="equal" is Provot's rule: half of the excess at each free end.
    weights="mass" splits the excess by inverse mass, which keeps the centre of
    mass of the two particles. Return True if a particle moved.
    """
    a, b = spring[0], spring[1]
    dx = x[b][0] - x[a][0]
    dy = x[b][1] - x[a][1]
    length = math.hypot(dx, dy)  # @line L3
    wa, wb = inv_mass[a], inv_mass[b]
    if length <= target or (wa == 0.0 and wb == 0.0):  # @line L4
        return False
    k = (length - target) / length
    ex, ey = k * dx, k * dy  # @line L5
    if wa > 0.0 and wb > 0.0:
        if weights == "equal":
            sa = sb = 0.5
        else:
            sa = wa / (wa + wb)
            sb = wb / (wa + wb)
        x[a] = (x[a][0] + sa * ex, x[a][1] + sa * ey)  # @line L6
        x[b] = (x[b][0] - sb * ex, x[b][1] - sb * ey)
    elif wa > 0.0:
        x[a] = (x[a][0] + ex, x[a][1] + ey)  # @line L7
    else:
        x[b] = (x[b][0] - ex, x[b][1] - ey)  # @line L8
    return True


def limit_strain(x, inv_mass, springs, tau, sweeps=1, slack=0.0, weights="equal"):
    """Run Provot's correction over the springs. Return (new positions, sweeps run).

    Each sweep visits the springs in the given order. With sweeps=None the
    sweeps repeat until no spring is longer than (1 + tau) L, or until 10000
    sweeps have run. A spring longer than its target (1 + tau)(1 - slack) L is
    shortened to the target. slack = 0 is Provot's rule; a small slack > 0
    makes the repeated sweeps stop after a finite number of sweeps whenever the
    shortened limits can all hold at once (see the proof page).
    """
    x = [tuple(p) for p in x]
    limit = [(1.0 + tau) * s[2] for s in springs]
    target = [(1.0 + tau) * (1.0 - slack) * s[2] for s in springs]
    cap = 10000 if sweeps is None else sweeps
    done = 0
    while done < cap:  # @line L1
        if sweeps is None and all(math.dist(x[s[0]], x[s[1]]) <= lim for s, lim in zip(springs, limit)):
            break
        for s, t in zip(springs, target):  # @line L2
            correct_spring(x, inv_mass, s, t, weights)
        done += 1
    return x, done


def spring_forces(x, v, mass, springs, damping=0.0, gravity=GRAVITY):
    """Gravity plus damped Hooke forces along each spring."""
    f = [[m * gravity[0], m * gravity[1]] for m in mass]
    for a, b, rest, k in springs:
        dx = x[b][0] - x[a][0]
        dy = x[b][1] - x[a][1]
        length = math.hypot(dx, dy)
        ux, uy = dx / length, dy / length
        rel = (v[b][0] - v[a][0]) * ux + (v[b][1] - v[a][1]) * uy
        s = k * (length - rest) + damping * rel
        f[a][0] += s * ux
        f[a][1] += s * uy
        f[b][0] -= s * ux
        f[b][1] -= s * uy
    return f


def step(x, v, mass, inv_mass, springs, dt, tau=0.1, sweeps=1, limited=None,
         damping=0.0, gravity=GRAVITY, slack=0.0, weights="equal"):
    """One step: symplectic Euler, then strain limiting, then new velocities.

    limited is the list of springs to correct (Provot used the structural
    springs, then the structural and shear springs); the default is all springs.
    The velocity is set to (x_new - x_old) / dt so that it matches the
    corrected motion; this is a choice of this code.
    """
    f = spring_forces(x, v, mass, springs, damping, gravity)
    pred = []
    for i in range(len(x)):
        w = inv_mass[i]
        vi = (v[i][0] + dt * w * f[i][0], v[i][1] + dt * w * f[i][1])
        pred.append((x[i][0] + dt * vi[0], x[i][1] + dt * vi[1]))  # @line L9
    new_x, _ = limit_strain(pred, inv_mass, springs if limited is None else limited,
                            tau, sweeps, slack, weights)  # @line L10
    new_v = [((nx_ - ox) / dt, (ny_ - oy) / dt) for (nx_, ny_), (ox, oy) in zip(new_x, x)]  # @line L11
    return new_x, new_v


def grid(nx, ny, spacing, k_struct, k_shear=0.0):
    """A hanging grid: row j = 0 at the top, y = -j spacing. Springs (a, b, rest, k)."""
    def idx(i, j):
        return j * nx + i

    x = [(i * spacing, -j * spacing) for j in range(ny) for i in range(nx)]
    structural, shear = [], []
    for j in range(ny):
        for i in range(nx):
            if i + 1 < nx:
                structural.append((idx(i, j), idx(i + 1, j), spacing, k_struct))
            if j + 1 < ny:
                structural.append((idx(i, j), idx(i, j + 1), spacing, k_struct))
            if k_shear > 0.0 and i + 1 < nx and j + 1 < ny:
                d = spacing * math.sqrt(2.0)
                shear.append((idx(i, j), idx(i + 1, j + 1), d, k_shear))
                shear.append((idx(i + 1, j), idx(i, j + 1), d, k_shear))
    return x, structural, shear
