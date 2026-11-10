# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hypercube-shares-join/. The authors are listed in prov/38S9XN.jsonl.

"""The Shares (HyperCube) join of Afrati and Ullman, on a small MapReduce simulator.

The k reducers are the cells of a grid with one dimension per attribute. The
side of the grid in the direction of attribute A is the share x_A, and the
product of the shares is k. A tuple fixes the coordinates of the attributes it
has, by a hash of each value, and is copied to every cell along the other
directions. So the communication is the sum over the relations of
|relation| times the product of the shares of the attributes it lacks.
"""

import itertools
import math
import zlib
from dataclasses import dataclass, field
from typing import Any

# A query is a list of relations; each relation is (attribute names, list of tuples).
Relation = tuple[tuple[str, ...], list[tuple[Any, ...]]]


def h(attr: str, value: Any, share: int) -> int:
    """The hash of one attribute: a salted CRC-32, the same in every process, mod the share."""
    return zlib.crc32(f"{attr}\x00{value!r}".encode("utf-8")) % share


@dataclass
class SharesStats:
    pairs_sent: int = 0
    reducer_input: list[int] = field(default_factory=list)

    @property
    def largest_reducer_input(self) -> int:
        return max(self.reducer_input, default=0)


def attributes(query: list[Relation]) -> list[str]:
    """The attributes of the query, in order of first use."""
    seen: list[str] = []
    for attrs, _ in query:
        seen.extend(a for a in attrs if a not in seen)
    return seen


def communication(sizes_and_attrs: list[tuple[int, tuple[str, ...]]], shares: dict[str, float]) -> float:
    """sum over relations of |relation| * product of the shares of the attributes it lacks."""
    return sum(size * math.prod(x for a, x in shares.items() if a not in attrs) for size, attrs in sizes_and_attrs)


def cell_id(coords: tuple[int, ...], sides: tuple[int, ...]) -> int:
    """Mixed radix: (i, j, l) with sides (x, y, w) maps to i*y*w + j*w + l."""
    cid = 0
    for c, side in zip(coords, sides):
        cid = cid * side + c
    return cid


def local_join(attrs_order: list[str], parts: list[Relation]) -> list[tuple[Any, ...]]:
    """Join a few relations on one machine: backtrack over the relations, with a hash index of each
    relation on the attributes that the earlier relations already bind."""
    out: list[tuple[Any, ...]] = []
    bound: set[str] = set()
    indexes = []
    for rel_attrs, tuples in parts:
        pos = [j for j, a in enumerate(rel_attrs) if a in bound]
        index: dict[tuple[Any, ...], list[tuple[Any, ...]]] = {}
        for t in tuples:
            index.setdefault(tuple(t[j] for j in pos), []).append(t)
        indexes.append(([rel_attrs[j] for j in pos], index))
        bound.update(rel_attrs)

    def extend(i: int, binding: dict[str, Any]) -> None:
        if i == len(parts):
            out.append(tuple(binding[a] for a in attrs_order))
            return
        rel_attrs = parts[i][0]
        key_attrs, index = indexes[i]
        for t in index.get(tuple(binding[a] for a in key_attrs), ()):
            if all(binding.get(a, v) == v for a, v in zip(rel_attrs, t)):  # repeated attributes inside one relation
                extend(i + 1, {**binding, **dict(zip(rel_attrs, t))})

    extend(0, {})
    return out


def shares_join(query: list[Relation], shares: dict[str, int]) -> tuple[list[tuple[Any, ...]], SharesStats]:
    """Run one round of the Shares join. Output tuples list the attributes in the order of attributes(query)."""
    order = attributes(query)
    sides = tuple(shares.get(a, 1) for a in order)
    k = math.prod(sides)
    inbox: list[list[list[tuple[Any, ...]]]] = [[[] for _ in query] for _ in range(k)]
    stats = SharesStats(reducer_input=[0] * k)
    for r_index, (rel_attrs, tuples) in enumerate(query):  # @line L1
        for t in tuples:  # @line L2
            fixed = {a: h(a, v, shares.get(a, 1)) for a, v in zip(rel_attrs, t)}
            ranges = [[fixed[a]] if a in fixed else range(side) for a, side in zip(order, sides)]
            for coords in itertools.product(*ranges):  # @line L3
                cid = cell_id(coords, sides)
                inbox[cid][r_index].append(t)  # @line L4
                stats.pairs_sent += 1
                stats.reducer_input[cid] += 1
    output: list[tuple[Any, ...]] = []
    for cell in inbox:  # @line L5
        output.extend(local_join(order, [(attrs, part) for (attrs, _), part in zip(query, cell)]))  # @line L6
    return output, stats


def triangle_shares(r: float, s: float, t: float, k: float) -> tuple[dict[str, float], float]:
    """The Lagrange optimum for R(A,B) S(B,C) T(C,A): s*x_A = t*x_B = r*x_C = (rstk)^(1/3), cost 3 (rstk)^(1/3)."""
    lam_k = (r * s * t * k) ** (1 / 3)
    return {"A": lam_k / s, "B": lam_k / t, "C": lam_k / r}, 3 * lam_k


def chain_shares(r: float, s: float, t: float, k: float) -> tuple[dict[str, float], float]:
    """The Lagrange optimum for R(A,B) S(B,C) T(C,D): x_A = x_D = 1, x_B = sqrt(kr/t), x_C = sqrt(kt/r)."""
    return {"A": 1.0, "B": math.sqrt(k * r / t), "C": math.sqrt(k * t / r), "D": 1.0}, s + 2 * math.sqrt(k * r * t)


def best_integer_shares(sizes_and_attrs: list[tuple[int, tuple[str, ...]]], attrs: list[str],
                        k: int) -> tuple[dict[str, int], int]:
    """Try every way to write k as an ordered product of integer shares; return the cheapest."""
    def factorizations(n: int, m: int):
        if m == 1:
            yield (n,)
            return
        for d in range(1, n + 1):
            if n % d == 0:
                for rest in factorizations(n // d, m - 1):
                    yield (d,) + rest

    best = min(factorizations(k, len(attrs)), key=lambda f: communication(sizes_and_attrs, dict(zip(attrs, f))))
    shares = dict(zip(attrs, best))
    return shares, int(communication(sizes_and_attrs, shares))


def triangles_brute_force(r_rel, s_rel, t_rel) -> list[tuple[Any, Any, Any]]:
    """The one-machine reference for R(A,B) S(B,C) T(C,A), as (a, b, c)."""
    t_set: dict[tuple[Any, Any], int] = {}
    for c, a in t_rel:
        t_set[(c, a)] = t_set.get((c, a), 0) + 1
    return [(a, b, c) for a, b in r_rel for b2, c in s_rel if b == b2 for _ in range(t_set.get((c, a), 0))]
