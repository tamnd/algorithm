# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/label-cover/. The authors are listed in prov/N3TWC8.jsonl.
"""Label cover with projection constraints: the value, the clause-variable game and parallel repetition.

A game is (nu, nw, su, sw, edges). Left vertices are 0 .. nu-1 with labels 0 .. su-1, right vertices are
0 .. nw-1 with labels 0 .. sw-1, and each edge is (u, w, proj) with proj[a] the right label that the left
label a requires. For small instances only: value() tries every right labeling.
"""

from fractions import Fraction
from itertools import product

Game = tuple[int, int, int, int, list[tuple[int, int, tuple[int, ...]]]]


def satisfied(game: Game, left: list[int], right: list[int]) -> int:
    return sum(proj[left[u]] == right[w] for u, w, proj in game[4])


def best_left(game: Game, right: list[int]) -> list[int]:
    """For a fixed right labeling, each left vertex takes the label that satisfies most of its edges."""
    nu, _, su, _, edges = game
    score = [[0] * su for _ in range(nu)]
    for u, w, proj in edges:
        for a in range(su):
            score[u][a] += proj[a] == right[w]
    return [max(range(su), key=lambda a: score[u][a]) for u in range(nu)]


def value(game: Game) -> Fraction:
    """The largest fraction of satisfied edges."""
    _, nw, _, sw, edges = game
    best = 0
    for right in product(range(sw), repeat=nw):
        best = max(best, satisfied(game, best_left(game, list(right)), list(right)))
    return Fraction(best, len(edges))


def value_all_labelings(game: Game) -> Fraction:
    """The same value, by trying both sides; only for very small games."""
    nu, nw, su, sw, edges = game
    best = max(
        satisfied(game, list(lt), list(rt))
        for lt in product(range(su), repeat=nu)
        for rt in product(range(sw), repeat=nw)
    )
    return Fraction(best, len(edges))


def majority_labeling(game: Game) -> tuple[list[int], list[int]]:
    """Label every left vertex 0, then give each right vertex the most frequent required label."""
    nu, nw, _, sw, edges = game
    left = [0] * nu
    count = [[0] * sw for _ in range(nw)]
    for u, w, proj in edges:
        count[w][proj[left[u]]] += 1
    right = [max(range(sw), key=lambda b: count[w][b]) for w in range(nw)]
    return left, right


def clause_variable_game(nvars: int, clauses: list[tuple[int, int, int]]) -> Game:
    """The game of a 3-CNF formula whose clauses have three distinct variables.

    Literal +i or -i means x_i or not x_i, with 1 <= i <= nvars. A clause label is one of the 7 assignments
    to its three variables that satisfy it, and the edge to a variable projects it to that variable's bit.
    """
    edges = []
    for c, clause in enumerate(clauses):
        assert len({abs(lit) for lit in clause}) == 3
        sat = [bits for bits in product((0, 1), repeat=3) if any((b == 1) == (lit > 0) for b, lit in zip(bits, clause))]
        for pos, lit in enumerate(clause):
            edges.append((c, abs(lit) - 1, tuple(bits[pos] for bits in sat)))
    return len(clauses), nvars, 7, 2, edges


def max_sat_fraction(nvars: int, clauses: list[tuple[int, int, int]]) -> Fraction:
    best = 0
    for x in product((0, 1), repeat=nvars):
        best = max(best, sum(any((x[abs(lit) - 1] == 1) == (lit > 0) for lit in cl) for cl in clauses))
    return Fraction(best, len(clauses))


def repeat(game: Game, k: int) -> Game:
    """The k-fold parallel repetition: tuples of vertices, tuples of labels and tuples of edges."""
    nu, nw, su, sw, edges = game

    def index(t: tuple[int, ...], base: int) -> int:
        out = 0
        for x in t:
            out = out * base + x
        return out

    left_labels = list(product(range(su), repeat=k))
    new_edges = []
    for es in product(edges, repeat=k):
        u = index(tuple(e[0] for e in es), nu)
        w = index(tuple(e[1] for e in es), nw)
        proj = tuple(index(tuple(es[i][2][a[i]] for i in range(k)), sw) for a in left_labels)
        new_edges.append((u, w, proj))
    return nu**k, nw**k, su**k, sw**k, new_edges
