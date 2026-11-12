# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hinge-loss/. The authors are listed in prov/12NTY4.jsonl.
"""The binary hinge loss, its subgradient, the squared hinge, and the multiclass hinge
losses of Crammer and Singer (2001) and of Weston and Watkins (1999)."""


def dot(a: list[float], b: list[float]) -> float:
    return sum(u * v for u, v in zip(a, b))


def hinge(y: int, f: float) -> float:
    """max(0, 1 - y f) for a label y in {-1, +1}."""
    if y not in (-1, 1):
        raise ValueError("labels must be -1 or +1")
    return max(0.0, 1.0 - y * f)


def hinge_subgradient(w: list[float], x: list[float], y: int, c: float = 0.0) -> list[float]:
    """One subgradient in w of max(0, 1 - y w.x). At the kink (y w.x = 1) return -c y x, c in [0, 1]."""
    m = y * dot(w, x)
    if m < 1:
        coef = -y
    elif m > 1:
        coef = 0.0
    else:
        if not 0.0 <= c <= 1.0:
            raise ValueError("c must lie in [0, 1]")
        coef = -c * y
    return [coef * xj for xj in x]


def squared_hinge(y: int, f: float) -> float:
    return hinge(y, f) ** 2


def squared_hinge_derivative(y: int, f: float) -> float:
    """d/df max(0, 1 - y f)^2 = -2 y max(0, 1 - y f); it is continuous."""
    return -2.0 * y * hinge(y, f)


def crammer_singer(f: list[float], y: int) -> float:
    """max(0, 1 + max_{j != y} f_j - f_y) = max_j (f_j + [j != y]) - f_y."""
    return max(fj + (0.0 if j == y else 1.0) for j, fj in enumerate(f)) - f[y]


def weston_watkins(f: list[float], y: int, margin: float = 1.0) -> float:
    """sum_{j != y} max(0, margin - (f_y - f_j))."""
    return sum(max(0.0, margin - (f[y] - fj)) for j, fj in enumerate(f) if j != y)


def crammer_singer_subgradient(f: list[float], y: int) -> list[float]:
    """A subgradient in the score vector f: e_r - e_y with r the first maximizer of f_j + [j != y]."""
    vals = [fj + (0.0 if j == y else 1.0) for j, fj in enumerate(f)]
    r = vals.index(max(vals))
    g = [0.0] * len(f)
    g[r] += 1.0
    g[y] -= 1.0
    return g


def weston_watkins_subgradient(f: list[float], y: int) -> list[float]:
    """A subgradient in f: +1 on each class j != y with an active term, and minus their count on y."""
    g = [0.0] * len(f)
    for j, fj in enumerate(f):
        if j != y and 1.0 - (f[y] - fj) > 0:
            g[j] += 1.0
            g[y] -= 1.0
    return g


def conditional_risk(eta: float, alpha: float) -> float:
    """eta * hinge(+1, alpha) + (1 - eta) * hinge(-1, alpha)."""
    return eta * hinge(1, alpha) + (1 - eta) * hinge(-1, alpha)
