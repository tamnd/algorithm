# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alamouti-code/. The authors are listed in prov/04NE33.jsonl.

"""The Alamouti space-time block code: encoder, linear combiner and detector.

A codeword is the 2 by 2 matrix X = [[s1, -conj(s2)], [s2, conj(s1)]]. Row k
is transmit antenna k and column t is time slot t. Receive antenna i sees

    y[i][0] = h[i][0] s1 + h[i][1] s2 + w
    y[i][1] = -h[i][0] conj(s2) + h[i][1] conj(s1) + w

where h[i][k] is the effective gain from transmit antenna k to receive
antenna i. The effective gain includes any amplitude scale, for example
sqrt(Es / 2) when the total symbol energy Es is split over two antennas.
The channel must stay constant over the two slots.

The combiner returns z_k = g s_k + noise with g = sum |h[i][k]|^2, and the
detector picks the point nearest to z_k / g for each k. Because the two
columns of the equivalent channel are orthogonal and have the same norm, this
is the joint maximum likelihood decision of the pair (s1, s2).
"""


def encode(s1: complex, s2: complex) -> list[list[complex]]:
    """The codeword X, with rows as antennas and columns as time slots."""
    s1, s2 = complex(s1), complex(s2)
    return [[s1, -s2.conjugate()],  # @line L1
            [s2, s1.conjugate()]]  # @line L2


def transmit(x: list[list[complex]], h: list[list[complex]]) -> list[list[complex]]:
    """The noiseless received block: y[i][t] = sum over k of h[i][k] x[k][t]."""
    return [[sum(row[k] * x[k][t] for k in range(2)) for t in range(2)] for row in h]


def combine(y: list[list[complex]], h: list[list[complex]]) -> tuple[complex, complex, float]:
    """The combiner outputs (z1, z2, g) for the received block y and the channel h (one row per receive antenna)."""
    if len(y) != len(h) or not h:
        raise ValueError("y and h need one row for each receive antenna")
    hp = [(complex(row[0]), complex(row[1])) for row in h]
    yp = [(complex(row[0]), complex(row[1])) for row in y]
    g = sum(abs(a) ** 2 + abs(b) ** 2 for a, b in hp)  # @line L3
    z1 = sum(a.conjugate() * r1 + b * r2.conjugate() for (a, b), (r1, r2) in zip(hp, yp))  # @line L4
    z2 = sum(b.conjugate() * r1 - a * r2.conjugate() for (a, b), (r1, r2) in zip(hp, yp))  # @line L5
    return z1, z2, g


def _nearest(u: complex, points: list[complex]) -> int:
    best, arg = float("inf"), -1
    for i, p in enumerate(points):
        d = abs(u - p) ** 2
        if d < best:
            best, arg = d, i
    return arg


def decode(y: list[list[complex]], h: list[list[complex]], points: list[complex]) -> tuple[int, int]:
    """The indices into points of the decisions on s1 and s2."""
    z1, z2, g = combine(y, h)
    if g == 0:
        raise ValueError("the channel is zero")
    u1, u2 = z1 / g, z2 / g  # @line L6
    return _nearest(u1, points), _nearest(u2, points)  # @line L7
