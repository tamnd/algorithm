# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/radial-distribution-function/. The authors are listed in prov/WE4PJK.jsonl.

import math

Point = list[float]


def minimum_image_distance(ri: Point, rj: Point, box: float) -> float:
    s = 0.0
    for a, b in zip(ri, rj):
        d = a - b
        d -= box * round(d / box)
        s += d * d
    return math.sqrt(s)


def rdf_histogram(configurations: list[list[Point]], box: float, dr: float, nbins: int) -> tuple[list[float], list[float], list[int]]:
    """The histogram estimate of g(r) in a cubic periodic box of side box.

    Every configuration has the same number N of atoms. Bin k holds the
    distances in [k dr, (k + 1) dr). The result is (r, g, h): the bin
    centers, the estimate of g at each center and the raw counts, where h
    adds 2 for each pair, once for each atom of the pair.
    """
    if nbins * dr > box / 2 + 1e-12:  # @line L1
        raise ValueError("the histogram must stop at half the box")
    h = [0] * nbins  # @line L2
    n = len(configurations[0])
    for positions in configurations:  # @line L3
        if len(positions) != n:
            raise ValueError("every configuration must have the same number of atoms")
        for i in range(n):  # @line L4
            for j in range(i + 1, n):  # @line L4
                d = minimum_image_distance(positions[i], positions[j], box)  # @line L5
                k = int(d / dr)  # @line L6
                if k < nbins:  # @line L6
                    h[k] += 2  # @line L6
    rho = n / box ** 3
    tau = len(configurations)
    r_mid = []
    g = []
    for k in range(nbins):  # @line L7
        lo = k * dr
        n_id = 4 * math.pi * rho / 3 * ((lo + dr) ** 3 - lo ** 3)  # @line L7
        g.append(h[k] / (n * tau * n_id))  # @line L8
        r_mid.append(lo + dr / 2)
    return r_mid, g, h  # @line L9


def coordination_number(g: list[float], dr: float, rho: float, nbins: int) -> float:
    """4 pi rho times the integral of g(r) r^2 from 0 to nbins dr, with g constant on each bin.

    With the histogram estimate this is exactly the mean number of neighbors
    closer than nbins dr.
    """
    total = 0.0
    for k in range(nbins):
        lo = k * dr
        total += g[k] * 4 * math.pi * rho / 3 * ((lo + dr) ** 3 - lo ** 3)
    return total


def simple_cubic(cells: int, a: float) -> list[Point]:
    return [[a * x, a * y, a * z] for x in range(cells) for y in range(cells) for z in range(cells)]
