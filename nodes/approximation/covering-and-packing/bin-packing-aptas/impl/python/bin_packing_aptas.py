# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bin-packing-aptas/. The authors are listed in prov/SC1BGZ.jsonl.

from fractions import Fraction
from functools import lru_cache
from typing import Sequence, Union

Number = Union[int, Fraction]


def exact_by_counts(types: Sequence[Fraction], counts: Sequence[int]) -> list[list[int]]:
    """Optimal packing of counts[t] items of size types[t] into unit bins.

    Dynamic program over the vector of remaining counts. Each bin is a
    configuration: a vector of counts with total size at most 1. The bin that
    holds the first remaining item is chosen first, which removes symmetry.
    Return the bins as lists of type indices.
    """
    d = len(types)

    def configs(rest: tuple[int, ...], first: int) -> list[tuple[int, ...]]:
        out: list[tuple[int, ...]] = []
        cur = [0] * d
        cur[first] = 1

        def grow(t: int, room: Fraction) -> None:
            if t == d:
                out.append(tuple(cur))
                return
            limit = rest[t] - cur[t]
            add = 0
            while True:
                cur[t] += add
                grow(t + 1, room - add * types[t])
                cur[t] -= add
                add += 1
                if add > limit or add * types[t] > room:
                    break

        grow(0, 1 - types[first])
        return out

    @lru_cache(maxsize=None)
    def best(rest: tuple[int, ...]) -> tuple[int, tuple[tuple[int, ...], ...]]:
        first = next((t for t in range(d) if rest[t]), None)
        if first is None:
            return 0, ()
        top: tuple[int, tuple[tuple[int, ...], ...]] | None = None
        for c in configs(rest, first):
            k, plan = best(tuple(r - x for r, x in zip(rest, c)))
            if top is None or k + 1 < top[0]:
                top = (k + 1, (c,) + plan)
        assert top is not None
        return top

    _, plan = best(tuple(counts))
    return [[t for t in range(d) for _ in range(c[t])] for c in plan]


def bin_packing_aptas(sizes: Sequence[Number], eps: Number, capacity: Number = 1) -> list[list[int]]:
    """Pack the items into at most (1 + eps) OPT + 1 bins, for 0 < eps <= 1.

    Return the bins as lists of 0-based item indices. The running time is
    polynomial in n for each fixed eps, with exponent about 2 / (eps / 2)^2.
    """
    eps = Fraction(eps)
    if not 0 < eps <= 1:
        raise ValueError("eps must be in (0, 1]")
    s = [Fraction(x) / capacity for x in sizes]
    for i, x in enumerate(s):
        if not 0 < x <= 1:
            raise ValueError(f"item {i} has size {sizes[i]}, outside (0, capacity]")
    delta = eps / 2  # @line L1
    large = sorted((i for i in range(len(s)) if s[i] >= delta), key=lambda i: -s[i])
    k_group = int(delta * delta * len(large))
    top_group: list[int] = []
    if k_group == 0:  # @line L2
        types = sorted(set(s[i] for i in large), reverse=True)
        groups = [[i for i in large if s[i] == v] for v in types]
    else:
        groups = [large[a:a + k_group] for a in range(0, len(large), k_group)]  # @line L3
        top_group, groups = groups[0], groups[1:]
        types = [s[g[0]] for g in groups]  # @line L4
    plan = exact_by_counts(types, [len(g) for g in groups])
    pools = [list(g) for g in groups]
    bins = [[pools[t].pop() for t in b] for b in plan]  # @line L5
    bins.extend([i] for i in top_group)
    loads = [sum(s[i] for i in b) for b in bins]
    for i in range(len(s)):  # @line L6
        if s[i] >= delta:
            continue
        j = next((j for j, load in enumerate(loads) if load + s[i] <= 1), len(bins))
        if j == len(bins):
            bins.append([])
            loads.append(Fraction(0))
        bins[j].append(i)
        loads[j] += s[i]
    return bins  # @line L7
