# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tree-covering-technology-mapping/. The authors are listed in prov/QGBZ88.jsonl.

import random
from itertools import combinations

from tree_covering_technology_mapping import (LIBRARY, evaluate_pattern, matches, tree_cover,
                                              tree_roots)

AREA = {name: area for name, area, _ in LIBRARY}
PAT = {name: pat for name, _, pat in LIBRARY}

# The example of the page: o = NOT(a b + c d), as NAND2 and INV.
#   0 a, 1 b, 2 c, 3 d, 4 = nand(a, b), 5 = nand(c, d), 6 = nand(4, 5), 7 = inv(6)
EX_KINDS = ["in", "in", "in", "in", "nand", "nand", "nand", "inv"]
EX_FANINS = [[], [], [], [], [0, 1], [2, 3], [4, 5], [6]]

# Sharing: n = nand(a, b) feeds o1 = inv(n) = a b and o2 = inv(nand(n, inv(c))) = NOT(a b + c).
#   0 a, 1 b, 2 c, 3 = n, 4 = o1, 5 = inv(c), 6 = nand(n, 5), 7 = o2
SH_KINDS = ["in", "in", "in", "nand", "inv", "inv", "nand", "inv"]
SH_FANINS = [[], [], [], [0, 1], [3], [2], [3, 5], [6]]


def canon_pattern(p) -> str:
    if p == "x":
        return "x"
    if p[0] == "inv":
        return "i(" + canon_pattern(p[1]) + ")"
    return "n(" + ",".join(sorted([canon_pattern(p[1]), canon_pattern(p[2])])) + ")"


CANON = {}
for _name, _area, _pat in LIBRARY:
    c = canon_pattern(_pat)
    CANON[c] = min(CANON.get(c, _area), _area)


def canon_region(kinds, fanins, v, stop) -> str:
    """Shape of the region below v, cut at the nodes of stop and at the inputs."""
    if kinds[v] == "in" or v in stop:
        return "x"
    if kinds[v] == "inv":
        return "i(" + canon_region(kinds, fanins, fanins[v][0], stop) + ")"
    a, b = fanins[v]
    return "n(" + ",".join(sorted([canon_region(kinds, fanins, a, stop),
                                   canon_region(kinds, fanins, b, stop)])) + ")"


def trees(kinds, fanins, outputs) -> dict:
    """Map each tree root to the nodes of its tree."""
    roots = tree_roots(kinds, fanins, outputs)
    out = {}
    for r in roots:
        nodes, stack = [], [r]
        while stack:
            w = stack.pop()
            nodes.append(w)
            stack.extend(u for u in fanins[w] if kinds[u] != "in" and u not in roots)
        out[r] = nodes
    return out


def brute_tree_area(kinds, fanins, outputs) -> int:
    """Try every set of gate roots inside every tree; each region must be a whole gate."""
    roots = tree_roots(kinds, fanins, outputs)
    total = 0
    for r, nodes in trees(kinds, fanins, outputs).items():
        inner = [w for w in nodes if w != r]
        best = None
        for size in range(len(inner) + 1):
            for pick in combinations(inner, size):
                s = set(pick) | {r}
                stop = s | roots
                cost = 0
                for g in s:
                    shape = canon_region(kinds, fanins, g, stop - {g})
                    if shape not in CANON:
                        break
                    cost += CANON[shape]
                else:
                    best = cost if best is None else min(best, cost)
        total += best
    return total


def brute_dag_area(kinds, fanins, outputs) -> int:
    """Least area over every DAG cover: gates may span multiple fanout points."""
    gates = [v for v in range(len(kinds)) if kinds[v] != "in"]
    every = lambda u: kinds[u] != "in"  # noqa: E731
    opts = {v: [(area, set(lv)) for name, area, pat in LIBRARY
                for lv in matches(kinds, fanins, pat, v, every)] for v in gates}
    must = {o for o in outputs if kinds[o] != "in"}
    rest = [v for v in gates if v not in must]
    best = None
    for size in range(len(rest) + 1):
        for pick in combinations(rest, size):
            s = must | set(pick)
            cost = 0
            for v in s:
                ok = [a for a, lv in opts[v] if all(kinds[u] == "in" or u in s for u in lv)]
                if not ok:
                    break
                cost += min(ok)
            else:
                best = cost if best is None else min(best, cost)
    return best


def simulate(kinds, fanins, m, n_in) -> list:
    val = []
    for v, k in enumerate(kinds):
        if k == "in":
            val.append((m >> (n_in - 1 - v)) & 1)
        elif k == "inv":
            val.append(1 - val[fanins[v][0]])
        else:
            val.append(1 - (val[fanins[v][0]] & val[fanins[v][1]]))
    return val


def check_cover(kinds, fanins, outputs, cover) -> None:
    n_in = kinds.count("in")
    for m in range(1 << n_in):
        val = simulate(kinds, fanins, m, n_in)
        got = {v: val[v] for v in range(len(kinds)) if kinds[v] == "in"}

        def get(v):
            if v not in got:
                name, leaves = cover[v]
                got[v] = evaluate_pattern(PAT[name], iter([get(u) for u in leaves]))
            return got[v]

        for o in outputs:
            assert get(o) == val[o]


def random_subject(rng, n_in, n_gates, window):
    kinds, fanins = ["in"] * n_in, [[] for _ in range(n_in)]
    for v in range(n_in, n_in + n_gates):
        lo = max(0, v - window)
        if rng.random() < 0.35:
            kinds.append("inv")
            fanins.append([rng.randrange(lo, v)])
        else:
            kinds.append("nand")
            fanins.append(sorted(rng.sample(range(lo, v), 2)) if v - lo >= 2 else [0, 0])
    outs = sorted(set([len(kinds) - 1, rng.randrange(n_in, len(kinds))]))
    return kinds, fanins, outs


def test_example() -> None:
    area, cover = tree_cover(EX_KINDS, EX_FANINS, [7])
    assert area == 5 and cover == {7: ("AOI22", [0, 1, 2, 3])}
    # without AOI22 and NAND4 the best cover is AOI21 over a NAND2
    small = [g for g in LIBRARY if g[0] not in ("AOI22", "NAND4")]
    area, cover = tree_cover(EX_KINDS, EX_FANINS, [7], small)
    assert area == 10 and cover[7] == ("AND2", [4, 5])
    assert brute_tree_area(EX_KINDS, EX_FANINS, [7]) == 5


def test_sharing_loses_against_dag_cover() -> None:
    outs = [4, 7]
    area, cover = tree_cover(SH_KINDS, SH_FANINS, outs)
    # NAND2 for n, INV for o1, INV for c and AND2 for o2: 3 + 2 + 2 + 4
    assert area == 11 and set(cover) == {3, 4, 5, 7}
    assert brute_tree_area(SH_KINDS, SH_FANINS, outs) == 11
    # AND2(a, b) and AOI21(a, b, c), with nand(a, b) built twice: 4 + 4
    assert brute_dag_area(SH_KINDS, SH_FANINS, outs) == 8
    check_cover(SH_KINDS, SH_FANINS, outs, cover)


def test_against_exhaustive_tree_covers() -> None:
    rng = random.Random(21)
    done = 0
    while done < 300:
        kinds, fanins, outs = random_subject(rng, rng.randint(1, 5), rng.randint(1, 18), 6)
        if max(len(t) for t in trees(kinds, fanins, outs).values()) > 14:
            continue
        area, cover = tree_cover(kinds, fanins, outs)
        assert area == brute_tree_area(kinds, fanins, outs)
        check_cover(kinds, fanins, outs, cover)
        done += 1


def test_tree_cover_is_a_dag_cover() -> None:
    rng = random.Random(22)
    strict = 0
    for _ in range(150):
        kinds, fanins, outs = random_subject(rng, rng.randint(2, 4), rng.randint(2, 11), 4)
        area, _ = tree_cover(kinds, fanins, outs)
        dag = brute_dag_area(kinds, fanins, outs)
        assert dag <= area
        strict += dag < area
    assert strict > 0


def test_rejects_bad_graph() -> None:
    try:
        tree_cover(["in", "nand"], [[], [0]], [1])
    except ValueError:
        return
    raise AssertionError("a NAND with one fanin must be rejected")
