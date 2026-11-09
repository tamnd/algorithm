# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/harmony-search/. The authors are listed in prov/YB0SC1.jsonl.

import random
from collections.abc import Callable, Sequence

Vector = list[float]


def improvise(
    memory: Sequence[Vector], hmcr: float, par: float, bw: float, lower: Sequence[float], upper: Sequence[float], rng: random.Random
) -> Vector:
    """One new vector, coordinate by coordinate: with probability hmcr copy the
    coordinate of a uniform random memory vector and, with probability par,
    add bw * u with u uniform in [-1, 1], clipped to the box; otherwise draw
    the coordinate uniformly in [lower_j, upper_j]. Cost: O(D)."""
    x = []
    for j in range(len(lower)):
        if rng.random() < hmcr:
            v = memory[rng.randrange(len(memory))][j]
            if rng.random() < par:
                v = min(upper[j], max(lower[j], v + bw * rng.uniform(-1.0, 1.0)))
        else:
            v = rng.uniform(lower[j], upper[j])
        x.append(v)
    return x


def harmony_search(
    f: Callable[[Sequence[float]], float],
    lower: Sequence[float],
    upper: Sequence[float],
    hms: int,
    hmcr: float,
    par: float,
    bw: float,
    iterations: int,
    rng: random.Random,
    on_iteration: Callable[[int, list[Vector], list[float]], None] | None = None,
) -> tuple[Vector, float, list[float]]:
    """Harmony search (Geem, Kim and Loganathan 2001; Lee and Geem 2005) for minimizing f on a box.

    The harmony memory holds hms vectors. Each iteration improvises one vector
    and puts it in place of the worst vector if it is strictly better.
    Precondition: hms >= 1, 0 <= hmcr, par <= 1, bw >= 0, lower[j] < upper[j].
    Returns (best vector, its value, history of the best value).
    Cost: O(iterations * (D + hms + c)) time for D variables and evaluation cost c, O(hms * D) space.
    """
    d = len(lower)
    memory = [[rng.uniform(lower[j], upper[j]) for j in range(d)] for _ in range(hms)]  # @line L1
    values = [f(x) for x in memory]
    history = [min(values)]
    for t in range(iterations):  # @line L2
        x = improvise(memory, hmcr, par, bw, lower, upper, rng)  # @line L3
        fx = f(x)
        w = max(range(hms), key=lambda i: values[i])  # @line L4
        if fx < values[w]:  # @line L5
            memory[w], values[w] = x, fx
        history.append(min(values))
        if on_iteration is not None:
            on_iteration(t, [list(v) for v in memory], list(values))
    b = min(range(hms), key=lambda i: values[i])
    return memory[b], values[b], history  # @line L6


def mu_plus_one_es(
    f: Callable[[Sequence[float]], float],
    lower: Sequence[float],
    upper: Sequence[float],
    mu: int,
    p_rec: float,
    p_mut: float,
    sigma: float,
    iterations: int,
    rng: random.Random,
    on_iteration: Callable[[int, list[Vector], list[float]], None] | None = None,
) -> tuple[Vector, float, list[float]]:
    """A (mu + 1) evolution strategy written in ES terms, for the comparison of Weyland (2010).

    Variation, per coordinate: with probability 1 - p_rec a uniform reset
    mutation; otherwise global discrete recombination (the coordinate of a
    uniform random parent) followed, with probability p_mut, by a uniform
    mutation of width sigma. Selection: the mu best of the mu + 1, with a
    tie between the offspring and the worst parent resolved for the parent.
    Same cost as harmony_search.
    """
    d = len(lower)
    parents = [[rng.uniform(lower[j], upper[j]) for j in range(d)] for _ in range(mu)]
    fit = [f(p) for p in parents]
    history = [min(fit)]
    for t in range(iterations):
        child = []
        for j in range(d):
            reset = not rng.random() < p_rec
            if reset:
                child.append(rng.uniform(lower[j], upper[j]))
                continue
            gene = parents[rng.randrange(mu)][j]  # global discrete recombination
            if rng.random() < p_mut:
                gene = min(upper[j], max(lower[j], gene + sigma * rng.uniform(-1.0, 1.0)))
            child.append(gene)
        # (mu + 1) selection: drop the worst of the mu + 1; the offspring on a tie,
        # else the first parent among equal worst values. The others keep their places.
        fc = f(child)
        worst = max(fit)
        if fc < worst:
            k = fit.index(worst)
            parents[k], fit[k] = child, fc
        history.append(min(fit))
        if on_iteration is not None:
            on_iteration(t, [list(p) for p in parents], list(fit))
    b = fit.index(min(fit))
    return parents[b], fit[b], history


def sphere(x: Sequence[float]) -> float:
    return sum(v * v for v in x)
