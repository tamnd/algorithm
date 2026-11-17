# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/molecular-dynamics/. The authors are listed in prov/CPQSNC.jsonl.
"""Molecular dynamics in the microcanonical (NVE) ensemble with velocity Verlet.

The state is the positions x and the velocities v of N particles in d
dimensions, with masses m. A force field gives the potential energy U(x) and
the forces f = -grad U(x). Each step of length h does a half kick of the
velocities, a drift of the positions, one new force evaluation and a second
half kick (Swope, Andersen, Berens and Wilson 1982). Positions are wrapped
into a periodic box when one is given.

The included force field is the Lennard-Jones pair potential
U(r) = 4 eps ((sigma / r)^12 - (sigma / r)^6), cut at r_c and shifted so that
U(r_c) = 0, with the minimum image convention in a cubic box of side L.
Precondition for the minimum image: r_c <= L / 2.

Cost: one force evaluation per step. The all-pairs force loop here costs
Theta(N^2 d) time per step; cell lists or neighbour lists make it Theta(N)
for a short cutoff at fixed density. Extra space Theta(N d).
"""

from typing import Callable, Optional

Vec = list[float]
ForceField = Callable[[list[Vec]], tuple[float, list[Vec]]]


def minimum_image(dx: float, box: Optional[float]) -> float:
    """The component of the shortest periodic image of a displacement."""
    if box is None:
        return dx
    return dx - box * round(dx / box)


def lennard_jones(
    pos: list[Vec], box: Optional[float] = None, eps: float = 1.0,
    sigma: float = 1.0, rc: Optional[float] = None,
) -> tuple[float, list[Vec]]:
    """Potential energy and forces of a Lennard-Jones system (truncated and shifted at rc)."""
    n, d = len(pos), len(pos[0]) if pos else 0
    if box is not None and rc is not None and rc > box / 2:
        raise ValueError("the minimum image needs rc <= box / 2")
    shift = 0.0
    if rc is not None:
        sr6 = (sigma / rc) ** 6
        shift = 4 * eps * (sr6 * sr6 - sr6)
    u = 0.0
    f = [[0.0] * d for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            r = [minimum_image(pos[i][a] - pos[j][a], box) for a in range(d)]
            r2 = sum(c * c for c in r)
            if rc is not None and r2 >= rc * rc:
                continue
            sr6 = (sigma * sigma / r2) ** 3
            u += 4 * eps * (sr6 * sr6 - sr6) - shift
            # -dU/dr / r = 24 eps (2 sr^12 - sr^6) / r^2
            g = 24 * eps * (2 * sr6 * sr6 - sr6) / r2
            for a in range(d):
                f[i][a] += g * r[a]
                f[j][a] -= g * r[a]
    return u, f


def harmonic(k: float) -> ForceField:
    """Force field of independent springs U = k |x|^2 / 2 for each particle."""
    def field(pos: list[Vec]) -> tuple[float, list[Vec]]:
        u = sum(0.5 * k * c * c for p in pos for c in p)
        return u, [[-k * c for c in p] for p in pos]
    return field


def kinetic(vel: list[Vec], mass: list[float]) -> float:
    """Kinetic energy sum m |v|^2 / 2."""
    return sum(0.5 * m * sum(c * c for c in v) for v, m in zip(vel, mass))


def molecular_dynamics(
    pos: list[Vec], vel: list[Vec], mass: list[float], field: ForceField,
    h: float, steps: int, box: Optional[float] = None,
) -> tuple[list[Vec], list[Vec], list[float]]:
    """Run `steps` velocity Verlet steps of length h.

    Returns the final positions, the final velocities and the total energy
    K + U after step 0, 1, ..., steps. The inputs are not changed.
    Precondition: h > 0, all masses positive.
    """
    x = [list(p) for p in pos]
    v = [list(p) for p in vel]
    d = len(x[0]) if x else 0
    u, f = field(x)                                          # @line L1
    energies = [kinetic(v, mass) + u]
    for _ in range(steps):                                   # @line L2
        for i in range(len(x)):
            for a in range(d):
                v[i][a] += 0.5 * h * f[i][a] / mass[i]       # @line L3
                x[i][a] += h * v[i][a]                       # @line L4
                if box is not None:
                    x[i][a] %= box                           # @line L4
        u, f = field(x)                                      # @line L5
        for i in range(len(x)):
            for a in range(d):
                v[i][a] += 0.5 * h * f[i][a] / mass[i]       # @line L6
        energies.append(kinetic(v, mass) + u)                # @line L7
    return x, v, energies                                    # @line L8
