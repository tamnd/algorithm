# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-voronoi-diagram/. The authors are listed in prov/25RNN7.jsonl.

from fractions import Fraction

Point = tuple[int, int]


def _sign(v) -> int:
    return (v > 0) - (v < 0)


def sign_x_minus_y_root(x, y, b) -> int:
    """Exact sign of x - y * sqrt(b) for rationals x, y and b >= 0."""
    s1, s2 = _sign(x), _sign(y) * (b > 0)
    if s2 == 0:
        return s1
    if s1 != s2:
        return s1 if s1 != 0 else -s2
    return s1 * _sign(x * x - y * y * b)


def sign_root_diff(a, b, c) -> int:
    """Exact sign of sqrt(a) - sqrt(b) - c for rationals a, b >= 0 and c."""
    r = 1 if (c > 0 or (c == 0 and b > 0)) else (0 if c == 0 else _sign(b - c * c))  # sign of sqrt(b) + c
    if r <= 0:
        return 1 if (a > 0 or r < 0) else 0
    # both sides positive: compare a with (sqrt(b) + c)^2 = b + c^2 + 2 c sqrt(b)
    return sign_x_minus_y_root(a - b - c * c, 2 * c, b)


def dist2(q: tuple, p: Point):
    return (q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2


class WeightedVoronoiDiagram:
    """Additively or multiplicatively weighted Voronoi diagram of integer sites with integer weights.

    mode "additive": the distance from q to the site (p, w) is |q - p| - w, with w >= 0 (circles of radius w;
    the diagram is the Apollonius diagram). mode "multiplicative": the distance is |q - p| / w, with w > 0.
    Bisectors are hyperbola branches (additive) or Apollonius circles (multiplicative); equal weights give the
    ordinary bisector line. All decisions are exact: square roots are compared by squaring with sign care.
    Cost: insert O(1); nearest O(n); has_cell O(n) (additive) or O(1); bisector O(1).
    Building the full diagram takes O(n log n) (additive, by a sweep) and Theta(n^2) (multiplicative).
    """

    def __init__(self, mode: str, sites: list[tuple[Point, int]] = ()) -> None:
        assert mode in ("additive", "multiplicative")
        self.mode = mode
        self.sites: list[Point] = []
        self.weights: list[int] = []
        for p, w in sites:
            self.insert(p, w)

    def insert(self, p: Point, w: int) -> bool:
        """Add the site p with weight w; return False if p is already a site."""
        assert w >= 0 if self.mode == "additive" else w > 0
        if p in self.sites:
            return False
        self.sites.append(p)
        self.weights.append(w)
        return True

    def compare(self, q: tuple, i: int, j: int) -> int:
        """Sign of dist(q, site i) - dist(q, site j), exact."""
        a, b = dist2(q, self.sites[i]), dist2(q, self.sites[j])
        wi, wj = self.weights[i], self.weights[j]
        if self.mode == "multiplicative":
            return _sign(a * wj * wj - b * wi * wi)
        return sign_root_diff(a, b, wi - wj)  # |q-pi| - wi - (|q-pj| - wj)

    def nearest(self, q: tuple) -> list[Point]:
        """The sites at the smallest weighted distance from q (several only on a cell boundary)."""
        best: list[int] = []
        for i in range(len(self.sites)):  # @line L1
            c = self.compare(q, i, best[0]) if best else -1  # @line L2
            if c < 0:
                best = [i]  # @line L3
            elif c == 0:
                best.append(i)  # @line L4
        return [self.sites[i] for i in best]  # @line L5

    def has_cell(self, p: Point) -> bool:
        """True if the cell of the site p has nonempty interior."""
        i = self.sites.index(p)
        if self.mode == "multiplicative":
            return True  # near p the distance |q - p| / w tends to 0
        # additive: the cell is nonempty iff p is strictly inside it, iff |p - pj| > wj - wi for all j
        wi = self.weights[i]
        return all(sign_root_diff(dist2(p, s), 0, self.weights[j] - wi) > 0
                   for j, s in enumerate(self.sites) if j != i)

    def bisector(self, p: Point, r: Point) -> tuple:
        """The curve of points at equal weighted distance from the sites p and r.

        ("line", a, b, c): the line a x + b y = c. ("circle", center, r2): the Apollonius circle.
        ("hyperbola", p, r, k): the branch |q - p| - |q - r| = k (|k| < |p - r|) around the lighter site.
        ("ray", start, end): additive case |k| = |p - r|: the ray from start away from end.
        ("empty",): additive case |k| > |p - r|: one circle holds the other, one site always wins.
        """
        i, j = self.sites.index(p), self.sites.index(r)
        wi, wj = self.weights[i], self.weights[j]
        line = ("line", 2 * (r[0] - p[0]), 2 * (r[1] - p[1]), r[0] ** 2 + r[1] ** 2 - p[0] ** 2 - p[1] ** 2)
        if wi == wj:
            return line
        if self.mode == "multiplicative":
            # |q - p|^2 wj^2 = |q - r|^2 wi^2: a circle with center (wj^2 p - wi^2 r) / (wj^2 - wi^2)
            den = wj * wj - wi * wi
            center = (Fraction(wj * wj * p[0] - wi * wi * r[0], den), Fraction(wj * wj * p[1] - wi * wi * r[1], den))
            r2 = Fraction(wi * wi * wj * wj * dist2(p, r), den * den)
            return ("circle", center, r2)
        k = wi - wj  # |q - p| - |q - r| = wi - wj on the bisector
        s = _sign(k * k - dist2(p, r))
        if s > 0:
            return ("empty",)
        if s == 0:
            return ("ray", r, p) if k > 0 else ("ray", p, r)
        return ("hyperbola", p, r, k)
