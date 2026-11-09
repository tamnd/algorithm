# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/omega-test/. The authors are listed in prov/8M5CJY.jsonl.

"""Pugh's omega test: integer feasibility of linear equalities and inequalities.

A constraint is a pair (coeffs, c): coeffs maps a variable to a nonzero int,
and c is an int. In the list eqs it means sum(a * x) + c == 0, and in the
list ineqs it means sum(a * x) + c >= 0. Variables are any hashable values;
the solver makes new variables ("sigma", k) for equality elimination.

solve(eqs, ineqs) returns a model (a dict with an int for each variable that
occurs in the input) or None if no integer solution exists. It always stops.
"""

from math import gcd
from typing import Hashable

Constraint = tuple[dict, int]


def _floor_div(a: int, b: int) -> int:
    return a // b  # Python's // is floor division for b > 0


def _ceil_div(a: int, b: int) -> int:
    return -((-a) // b)


def mod_hat(a: int, m: int) -> int:
    """Pugh's symmetric residue: a - m * floor(a / m + 1/2), in [-m/2, m/2)."""
    return a - m * ((2 * a + m) // (2 * m))


def _clean(coeffs: dict) -> dict:
    return {v: a for v, a in coeffs.items() if a != 0}


def _substitute(con: Constraint, v: Hashable, expr: Constraint) -> Constraint:
    """Replace v by the linear expression expr = (coeffs, c) in con."""
    coeffs, c = con
    a = coeffs.get(v, 0)
    if a == 0:
        return con
    out = dict(coeffs)
    del out[v]
    for w, b in expr[0].items():
        out[w] = out.get(w, 0) + a * b
    return _clean(out), c + a * expr[1]


def normalize_ineq(con: Constraint) -> Constraint:
    """Divide by the gcd of the coefficients and round the constant down."""
    coeffs, c = con
    g = 0
    for a in coeffs.values():
        g = gcd(g, a)
    if g <= 1:
        return con
    return {v: a // g for v, a in coeffs.items()}, _floor_div(c, g)


def bounds_on(ineqs: list[Constraint], z: Hashable) -> tuple[list, list, list]:
    """Split ineqs into lower bounds b*z >= beta, upper bounds a*z <= alpha, rest.

    A lower bound is (b, beta) with beta = (coeffs, c) a linear expression,
    and an upper bound is (a, alpha) in the same way.
    """
    lows, ups, rest = [], [], []
    for coeffs, c in ineqs:
        k = coeffs.get(z, 0)
        if k == 0:
            rest.append((coeffs, c))
            continue
        other = {v: a for v, a in coeffs.items() if v != z}
        if k > 0:  # k z + other + c >= 0, so k z >= -(other + c)
            lows.append((k, ({v: -a for v, a in other.items()}, -c)))
        else:  # other + c >= -k z
            ups.append((-k, (other, c)))
    return lows, ups, rest


def _pair(low: tuple, up: tuple, slack: int) -> Constraint:
    """The constraint b * alpha - a * beta - slack >= 0 for b z >= beta, a z <= alpha."""
    b, (bc, b0) = low
    a, (ac, a0) = up
    out: dict = {}
    for v, x in ac.items():
        out[v] = out.get(v, 0) + b * x
    for v, x in bc.items():
        out[v] = out.get(v, 0) - a * x
    return normalize_ineq((_clean(out), b * a0 - a * b0 - slack))


def real_shadow(ineqs: list[Constraint], z: Hashable) -> list[Constraint]:
    """Fourier-Motzkin projection: the real points of the projection."""
    lows, ups, rest = bounds_on(ineqs, z)
    return rest + [_pair(lo, up, 0) for lo in lows for up in ups]


def dark_shadow(ineqs: list[Constraint], z: Hashable) -> list[Constraint]:
    """A part of the integer projection: b*alpha - a*beta >= (a - 1)(b - 1)."""
    lows, ups, rest = bounds_on(ineqs, z)
    return rest + [_pair(lo, up, (up[0] - 1) * (lo[0] - 1)) for lo in lows for up in ups]


def splinters(ineqs: list[Constraint], z: Hashable) -> list[Constraint]:
    """Equalities b*z = beta + i that cover the integer points the dark shadow misses."""
    lows, ups, _ = bounds_on(ineqs, z)
    if not lows or not ups:
        return []
    amax = max(a for a, _ in ups)
    out = []
    for b, (bc, b0) in lows:
        for i in range(_floor_div(amax * b - amax - b, amax) + 1):
            coeffs = {v: -x for v, x in bc.items()}
            coeffs[z] = b
            out.append((_clean(coeffs), -b0 - i))  # b z - beta - i == 0
    return out


def _value(expr: Constraint, model: dict) -> int:
    coeffs, c = expr
    return c + sum(a * model.setdefault(v, 0) for v, a in coeffs.items())


class Omega:
    def __init__(self) -> None:
        self.fresh = 0
        self.calls = 0

    def _new_var(self) -> tuple:
        self.fresh += 1
        return ("sigma", self.fresh)

    def run(self, eqs: list[Constraint], ineqs: list[Constraint]) -> dict | None:
        self.calls += 1
        eqs = [(_clean(c), k) for c, k in eqs]
        ineqs = [(_clean(c), k) for c, k in ineqs]
        # ---- equalities: solve one variable at a time and substitute
        while eqs:  # @line L1
            coeffs, c = eqs.pop()
            g = 0
            for a in coeffs.values():
                g = gcd(g, a)
            if g == 0:
                if c != 0:
                    return None
                continue
            if c % g != 0:  # @line L2
                return None
            coeffs, c = {v: a // g for v, a in coeffs.items()}, c // g
            k = min(coeffs, key=lambda v: (abs(coeffs[v]), repr(v)))
            ak = coeffs[k]
            s = 1 if ak > 0 else -1
            if abs(ak) == 1:  # @line L3
                # x_k = -s * (sum of the other terms + c)
                expr = ({v: -s * a for v, a in coeffs.items() if v != k}, -s * c)
            else:  # @line L4
                m = abs(ak) + 1
                sigma = self._new_var()
                rest = {v: s * mod_hat(a, m) for v, a in coeffs.items() if v != k}
                rest[sigma] = -s * m
                expr = (_clean(rest), s * mod_hat(c, m))
                eqs.append((coeffs, c))  # the equation stays, in terms of sigma
            eqs = [_substitute(e, k, expr) for e in eqs]  # @line L5
            ineqs = [_substitute(e, k, expr) for e in ineqs]
            model = self.run(eqs, ineqs)
            if model is None:
                return None
            model[k] = _value(expr, model)
            return model
        # ---- inequalities only
        ineqs = [normalize_ineq(e) for e in ineqs]
        for coeffs, c in ineqs:  # @line L6
            if not coeffs and c < 0:
                return None
        ineqs = [e for e in ineqs if e[0]]
        if not ineqs:  # @line L7
            return {}
        z = self._choose(ineqs)  # @line L8
        lows, ups, rest = bounds_on(ineqs, z)
        if not lows or not ups:  # @line L9
            model = self.run([], rest)
            if model is not None:
                self._pick(model, z, lows, ups)
            return model
        exact = all(a == 1 for a, _ in ups) or all(b == 1 for b, _ in lows)
        if exact:  # @line L10
            model = self.run([], real_shadow(ineqs, z))
            if model is not None:
                self._pick(model, z, lows, ups)
            return model
        model = self.run([], dark_shadow(ineqs, z))  # @line L11
        if model is not None:
            self._pick(model, z, lows, ups)
            return model
        for eq in splinters(ineqs, z):  # @line L12
            model = self.run([eq], ineqs)  # @line L13
            if model is not None:
                return model
        return None  # @line L14

    @staticmethod
    def _choose(ineqs: list[Constraint]) -> Hashable:
        """Prefer a variable with an exact projection; then the fewest new pairs."""
        best = None
        variables = sorted({v for c, _ in ineqs for v in c}, key=repr)
        for z in variables:
            lows, ups, _ = bounds_on(ineqs, z)
            exact = not lows or not ups or all(a == 1 for a, _ in ups) or all(b == 1 for b, _ in lows)
            key = (not exact, len(lows) * len(ups))
            if best is None or key < best[0]:
                best = (key, z)
        return best[1]

    @staticmethod
    def _pick(model: dict, z: Hashable, lows: list, ups: list) -> None:
        lo = max((_ceil_div(_value(beta, model), b) for b, beta in lows), default=None)
        hi = min((_floor_div(_value(alpha, model), a) for a, alpha in ups), default=None)
        if lo is None:
            model[z] = 0 if hi is None else hi
        else:
            model[z] = lo
            assert hi is None or lo <= hi


def solve(eqs: list[Constraint], ineqs: list[Constraint]) -> dict | None:
    """Return an integer model of all constraints, or None if there is none."""
    names = {v for c, _ in eqs + ineqs for v in c}
    model = Omega().run(eqs, ineqs)
    if model is None:
        return None
    return {v: model.get(v, 0) for v in names}


def holds(model: dict, eqs: list[Constraint], ineqs: list[Constraint]) -> bool:
    def val(con: Constraint) -> int:
        return con[1] + sum(a * model.get(v, 0) for v, a in con[0].items())

    return all(val(e) == 0 for e in eqs) and all(val(e) >= 0 for e in ineqs)
