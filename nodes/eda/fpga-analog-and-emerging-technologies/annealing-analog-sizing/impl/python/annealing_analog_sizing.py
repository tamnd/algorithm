# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/annealing-analog-sizing/. The authors are listed in prov/A4H89F.jsonl.

"""Annealing-based analog sizing in the style of ASTRX/OBLX, on a toy circuit.

The search is the one of the page: a cost that adds the objective and
weighted penalties for the violated specifications, moves that change one
size by a few grid steps, the Metropolis rule, and geometric cooling.

The circuit is a common-source stage with an ideal current-source load and
a load capacitor. ASTRX/OBLX evaluates a circuit with AWE and real device
models; here the evaluation is the closed-form square-law (Level 1) model.
Its constants are fitted to a process, not derived:
    KP    = 200   the transconductance factor k' = mu C_ox, in uA/V^2
    LAM0  = 0.1   lambda = LAM0 / L, in um/V
The others are a process value and the specifications:
    CGA   = 0.005 the gate capacitance per area, in pF/um^2
    C0    = 1.0   the load capacitance, in pF
Units: W and L in um, I in uA, g_m in uS, C in pF, so g_m / (2 pi C) is in MHz.
"""

import math

KP = 200.0
LAM0 = 0.1
CGA = 0.005
C0 = 1.0

# The specifications: (name, target, weight); each one is "performance >= target".
SPECS = (("gbw_mhz", 10.0, 10.0), ("gain", 100.0, 10.0), ("vov", 0.15, 10.0))
I_REF = 10.0  # the objective is I / I_REF + W L / A_REF: the current, then the area
A_REF = 100.0


def grids():
    """The sizes that the search may use: W, L and I on fixed grids."""
    ws = [0.5 * 10 ** (k / 20) for k in range(41)]  # 0.5 to 50 um
    ls = [0.5 + 0.05 * k for k in range(41)]  # 0.5 to 2.5 um
    cur = [10 ** (k / 100) for k in range(201)]  # 1 to 100 uA
    return [ws, ls, cur]


def performance(w, l, i):
    """The square-law small-signal model of the stage (the stand-in for AWE)."""
    gm = math.sqrt(2 * KP * (w / l) * i)
    vov = math.sqrt(2 * i * l / (KP * w))
    gds = LAM0 / l * i
    cl = C0 + CGA * w * l
    return {"gm": gm, "vov": vov, "gain": gm / gds, "gbw_mhz": gm / (2 * math.pi * cl), "cl": cl}


def cost(point, specs=SPECS):
    """The objective plus the weighted relative violation of each specification."""
    w, l, i = point
    perf = performance(w, l, i)
    c = i / I_REF + w * l / A_REF
    for name, target, weight in specs:
        c += weight * max(0.0, (target - perf[name]) / target)
    return c


def feasible(point, specs=SPECS):
    perf = performance(*point)
    return all(perf[name] >= target for name, target, _ in specs)


def anneal(rng, grid=None, t0=1.0, alpha=0.95, moves=100, t_min=1e-4, specs=SPECS):
    """Simulated annealing over the grid indices. Returns (best point, best cost, indices).

    rng is a random.Random; the run is a function of its seed.
    """
    grid = grid or grids()
    sizes = [len(g) for g in grid]

    def at(idx):
        return tuple(grid[d][idx[d]] for d in range(len(grid)))

    x = [rng.randrange(s) for s in sizes]  # @line L1
    c = cost(at(x), specs)
    best, best_c = list(x), c
    t = t0  # @line L2
    while t > t_min:  # @line L3
        reach = max(1, round(max(sizes) / 4 * t / t0))
        for _ in range(moves):  # @line L4
            y = list(x)  # @line L5: move one variable by a few grid steps
            d = rng.randrange(len(sizes))
            step = rng.randint(1, reach) * rng.choice((-1, 1))
            y[d] = min(sizes[d] - 1, max(0, y[d] + step))
            if y == x:
                continue
            delta = cost(at(y), specs) - c  # @line L6
            if delta <= 0 or rng.random() < math.exp(-delta / t):  # @line L7
                x, c = y, c + delta
                if c < best_c:  # @line L8
                    best, best_c = list(x), c
        t *= alpha  # @line L9
    return at(best), best_c, best  # @line L10
