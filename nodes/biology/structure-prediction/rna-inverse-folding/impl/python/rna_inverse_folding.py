# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rna-inverse-folding/. The authors are listed in prov/C0K6PX.jsonl.
"""RNA inverse folding in the base pair maximization (Nussinov) model.

The model:
  - allowed pairs AU, UA, GC, CG, GU, UG; at least m = 3 bases inside each pair; no pseudoknots;
  - energy -1 per base pair, so the optimal structures are those with the most pairs.

A sequence s is a design for a target structure T if T is a structure of s and T is the unique
optimal structure of s. The tools:
  - fold_count(s): the largest number of pairs and the number of optimal structures, by an
    unambiguous interval dynamic program;
  - cost(s, T): a number that is 0 exactly when s is a design for T;
  - adaptive_walk: a local search in the style of RNAinverse (Hofacker and others 1994);
  - exact_designs: a complete search over the sequences that are compatible with T.
"""

from __future__ import annotations

import itertools
import random

PAIRS = frozenset({("A", "U"), ("U", "A"), ("G", "C"), ("C", "G"), ("G", "U"), ("U", "G")})
PAIR_LIST = sorted(PAIRS)
BASES = "ACGU"


def parse_dot_bracket(db: str) -> list[tuple[int, int]]:
    stack, out = [], []
    for x, ch in enumerate(db):
        if ch == "(":
            stack.append(x)
        elif ch == ")":
            if not stack:
                raise ValueError("unbalanced structure")
            out.append((stack.pop(), x))
        elif ch != ".":
            raise ValueError("unknown symbol " + ch)
    if stack:
        raise ValueError("unbalanced structure")
    return sorted(out)


def fold_count(s: str, m: int = 3) -> tuple[int, int]:
    """(largest number of nested pairs, number of structures with that many pairs).

    N[i][j] and C[i][j] are the optimum and the number of optima on s[i..j]. Base j is unpaired,
    or pairs with exactly one k; these cases are disjoint, so the counts add up.
    """
    n = len(s)
    if n == 0:
        return 0, 1
    N = [[0] * n for _ in range(n)]
    C = [[1] * n for _ in range(n)]

    def val(i, j):
        return (N[i][j], C[i][j]) if i <= j else (0, 1)

    for span in range(m + 2, n + 1):
        for i in range(n - span + 1):
            j = i + span - 1
            best, cnt = val(i, j - 1)
            for k in range(i, j - m):
                if (s[k], s[j]) in PAIRS:
                    a, ca = val(i, k - 1)
                    b, cb = val(k + 1, j - 1)
                    v = a + 1 + b
                    if v > best:
                        best, cnt = v, ca * cb
                    elif v == best:
                        cnt += ca * cb
            N[i][j], C[i][j] = best, cnt
    return N[0][n - 1], C[0][n - 1]


def cost(s: str, target: list[tuple[int, int]], m: int = 3) -> int:
    """0 if and only if s is a design for the target; otherwise a positive penalty.

    bad is the number of target pairs that s cannot form, gap the number of pairs by which the
    optimum exceeds the formable target pairs, and the last term counts the other optima.
    """
    bad = sum(1 for i, j in target if (s[i], s[j]) not in PAIRS)
    best, count = fold_count(s, m)
    gap = best - (len(target) - bad)
    if bad == 0 and gap == 0:
        return count - 1
    return bad + gap + count


def is_design(s: str, target: list[tuple[int, int]], m: int = 3) -> bool:
    return cost(s, target, m) == 0


def _positions(n: int, target: list[tuple[int, int]]):
    paired = {x for pr in target for x in pr}
    return target, [x for x in range(n) if x not in paired]


def random_compatible(n: int, target: list[tuple[int, int]], rng: random.Random) -> str:
    pairs, free = _positions(n, target)
    s = [""] * n
    for i, j in pairs:
        s[i], s[j] = rng.choice(PAIR_LIST)
    for x in free:
        s[x] = rng.choice(BASES)
    return "".join(s)


def adaptive_walk(n: int, target: list[tuple[int, int]], rng: random.Random, m: int = 3,
                  max_steps: int = 2000, restarts: int = 20) -> str | None:
    """Local search in the style of RNAinverse.

    Start from a random sequence that can form the target; mutate one unpaired base or one pair
    (both bases together, to another allowed pair); keep the mutant if the cost does not increase.
    Stop at cost 0. Return a design, or None if none was found within the budget.
    """
    pairs, free = _positions(n, target)
    units = [("pair", pr) for pr in pairs] + [("base", x) for x in free]
    if not units:
        return "" if n == 0 else None
    for _ in range(restarts):
        s = list(random_compatible(n, target, rng))
        c = cost("".join(s), target, m)
        for _ in range(max_steps):
            if c == 0:
                return "".join(s)
            kind, where = rng.choice(units)
            t = s[:]
            if kind == "pair":
                i, j = where
                t[i], t[j] = rng.choice([p for p in PAIR_LIST if p != (s[i], s[j])])
            else:
                t[where] = rng.choice([b for b in BASES if b != s[where]])
            ct = cost("".join(t), target, m)
            if ct <= c:
                s, c = t, ct
        if c == 0:
            return "".join(s)
    return None


def exact_designs(n: int, target: list[tuple[int, int]], m: int = 3, first_only: bool = False) -> list[str]:
    """All designs, by a complete search over the sequences that can form the target.

    A design must form every target pair, so only 6 ** p * 4 ** u sequences need a test, where p is
    the number of pairs and u the number of unpaired bases.
    """
    pairs, free = _positions(n, target)
    out = []
    for pchoice in itertools.product(PAIR_LIST, repeat=len(pairs)):
        s = [""] * n
        for (i, j), (a, b) in zip(pairs, pchoice):
            s[i], s[j] = a, b
        for fchoice in itertools.product(BASES, repeat=len(free)):
            for x, b in zip(free, fchoice):
                s[x] = b
            seq = "".join(s)
            if is_design(seq, target, m):
                out.append(seq)
                if first_only:
                    return out
    return out


def to_dot_bracket(n: int, structure) -> str:
    out = ["."] * n
    for i, j in structure:
        out[i], out[j] = "(", ")"
    return "".join(out)
