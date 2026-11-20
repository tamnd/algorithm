# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterated-elimination-of-dominated-strategies/. The authors are listed in prov/M509ET.jsonl.
"""Iterated elimination of dominated strategies in a finite normal-form game.

A game is the pair (sizes, pay) of the helper agtgame: pay maps each profile to a tuple of
Fraction utilities, which the players maximize. The surviving strategies are returned as a
list of sorted lists, one per player.

Three dominance tests are given:
- strict dominance by a pure strategy (a direct comparison),
- strict dominance by a mixed strategy (one small linear program, solved here exactly by
  checking every vertex, which is only meant for the small games of the tests),
- weak dominance by a pure strategy, whose iterated result depends on the order.
"""

from fractions import Fraction
from itertools import combinations, product


def _contexts(alive, i):
    """The profiles of the other players that are still alive, as tuples with a hole at i."""
    return list(product(*(alive[k] if k != i else [None] for k in range(len(alive)))))


def _put(t, i, a):
    return t[:i] + (a,) + t[i + 1:]


def dominated_by_pure(game, alive, i, a):
    """Return a strategy b in alive[i] with u_i(b, t) > u_i(a, t) for every alive t, or None."""
    _, pay = game
    ctx = _contexts(alive, i)
    for b in alive[i]:
        if b != a and all(pay[_put(t, i, b)][i] > pay[_put(t, i, a)][i] for t in ctx):
            return b
    return None


def weakly_dominated_by_pure(game, alive, i, a):
    """Return b in alive[i] with u_i(b, t) >= u_i(a, t) for every alive t and > for one, or None."""
    _, pay = game
    ctx = _contexts(alive, i)
    for b in alive[i]:
        if b == a:
            continue
        d = [pay[_put(t, i, b)][i] - pay[_put(t, i, a)][i] for t in ctx]
        if all(x >= 0 for x in d) and any(x > 0 for x in d):
            return b
    return None


def _solve(M, rhs):
    """Solve the square system M x = rhs exactly; return None if M is singular."""
    k = len(M)
    A = [list(row) + [r] for row, r in zip(M, rhs)]
    for col in range(k):
        piv = next((r for r in range(col, k) if A[r][col] != 0), None)
        if piv is None:
            return None
        A[col], A[piv] = A[piv], A[col]
        for r in range(k):
            if r != col and A[r][col] != 0:
                f = A[r][col] / A[col][col]
                A[r] = [x - f * y for x, y in zip(A[r], A[col])]
    return [A[r][k] / A[r][r] for r in range(k)]


def maximin(D):
    """Return (z, x) with x in the simplex over the rows of D maximizing z = min_c sum_r x_r D[r][c].

    This is the linear program max z subject to sum_r x_r D[r][c] >= z for every column c,
    x >= 0 and sum_r x_r = 1. Its optimum is at a vertex, where R of the C + R inequalities are
    tight (R rows, C columns). The function tries every choice of R tight inequalities, which
    is exponential and only meant for small matrices.
    """
    R, C = len(D), len(D[0])
    best = None
    # Unknowns: x_0, ..., x_{R-1}, z. Inequality j < C: sum_r x_r D[r][j] - z >= 0.
    # Inequality C + r: x_r >= 0. The equality sum_r x_r = 1 is always tight.
    rows = [[D[r][c] for r in range(R)] + [Fraction(-1)] for c in range(C)]
    rows += [[Fraction(int(r == q)) for q in range(R)] + [Fraction(0)] for r in range(R)]
    eq = [Fraction(1)] * R + [Fraction(0)]
    for tight in combinations(range(C + R), R):
        sol = _solve([rows[j] for j in tight] + [eq], [Fraction(0)] * R + [Fraction(1)])
        if sol is None:
            continue
        x, z = sol[:R], sol[R]
        if all(v >= 0 for v in x) and all(sum(x[r] * D[r][c] for r in range(R)) >= z for c in range(C)):
            if best is None or z > best[0]:
                best = (z, x)
    return best


def mixed_dominance(game, alive, i, a):
    """Decide if a is strictly dominated by a mixed strategy on the alive strategies.

    Returns ("dominated", sigma), where sigma is a dict from the other alive strategies of
    player i to probabilities with sum_b sigma_b u_i(b, t) > u_i(a, t) for every alive t, or
    ("best response", q), where q is a dict from alive contexts t to probabilities such that a
    is a best response of player i to the belief q (Pearce's lemma, by LP duality).
    """
    _, pay = game
    ctx = _contexts(alive, i)
    rivals = [b for b in alive[i] if b != a]
    if not rivals:
        return "best response", {ctx[0]: Fraction(1)}
    D = [[pay[_put(t, i, b)][i] - pay[_put(t, i, a)][i] for t in ctx] for b in rivals]
    z, x = maximin(D)
    if z > 0:
        return "dominated", {b: p for b, p in zip(rivals, x) if p}
    # The dual: a belief q over the contexts with sum_t q_t D[b][t] <= 0 for every rival b.
    w, q = maximin([[-D[b][t] for b in range(len(rivals))] for t in range(len(ctx))])
    assert -w == z, "the primal and dual values differ"
    return "best response", {t: p for t, p in zip(ctx, q) if p}


def dominated_by_mixed(game, alive, i, a):
    """Return a mixed strategy (a dict) that strictly dominates a, or None."""
    kind, cert = mixed_dominance(game, alive, i, a)
    return cert if kind == "dominated" else None


TESTS = {"pure": dominated_by_pure, "mixed": dominated_by_mixed, "weak": weakly_dominated_by_pure}


def iterated_elimination(game, rule="pure", pick=None):
    """Remove dominated strategies until none is left, and return (alive, log).

    rule is "pure" or "mixed" (strict dominance) or "weak" (weak dominance by a pure strategy).
    pick chooses which dominated strategy to remove when several are: it gets the list of
    (player, strategy) pairs and returns one of them. By default the first pair in the order
    of players and strategies is removed. log lists (player, strategy, witness) in the order of
    removal.
    """
    test = TESTS[rule]
    sizes, _ = game
    alive = [list(range(k)) for k in sizes]  # @line L1
    log = []
    while True:  # @line L2
        found = []
        for i in range(len(sizes)):  # @line L3
            for a in alive[i]:
                w = test(game, alive, i, a)  # @line L4
                if w is not None:
                    found.append((i, a, w))
                    if pick is None:
                        break
            if found and pick is None:
                break
        if not found:  # @line L7
            return alive, log
        if pick is None:
            i, a, w = found[0]
        else:
            i, a = pick([(i, a) for i, a, _ in found])
            w = next(x for j, b, x in found if (j, b) == (i, a))
        alive[i].remove(a)  # @line L5
        log.append((i, a, w))  # @line L6
