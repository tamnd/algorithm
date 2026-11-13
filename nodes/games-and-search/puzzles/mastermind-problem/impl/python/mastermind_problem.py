# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mastermind-problem/. The authors are listed in prov/EHS84T.jsonl.
"""Mastermind: find a hidden code of n pegs in k colors from scored guesses.

Codes are tuples of colors 0..k-1. The score of a guess against the secret is
(black, white): black counts the places with the same color, and black + white
is the largest number of disjoint pairs (guess place, secret place) with the
same color.
"""

import itertools
from collections import Counter


def all_codes(pegs, colors):
    return list(itertools.product(range(colors), repeat=pegs))


def score(guess, secret, colors=6):
    """The score by the usual formula: total = sum over colors of the smaller count."""
    black = sum(g == s for g, s in zip(guess, secret))
    total = sum(min(guess.count(c), secret.count(c)) for c in range(colors))
    return black, total - black


def score_by_definition(guess, secret):
    """The score from its definition, by trying every matching of places."""
    n = len(guess)
    black = sum(g == s for g, s in zip(guess, secret))
    total = max(sum(guess[i] == secret[p[i]] for i in range(n))
                for p in itertools.permutations(range(n)))
    return black, total - black


def score_table(codes, colors):
    """table[g][s] = black * (n + 1) + white, for all pairs of codes, in one pass per guess.

    Black is a sum of per-place indicator lists; black + white depends only on
    the color counts of the two codes, and there are few distinct count vectors.
    """
    n = len(codes[0])
    m = len(codes)
    same = [[[int(code[p] == c) for code in codes] for c in range(colors)] for p in range(n)]
    vectors = {}
    kind = []
    for code in codes:
        v = tuple(code.count(c) for c in range(colors))
        kind.append(vectors.setdefault(v, len(vectors)))
    vecs = list(vectors)
    common = [[sum(map(min, u, v)) for v in vecs] for u in vecs]
    table = []
    for g in range(m):
        code = codes[g]
        cols = [same[p][code[p]] for p in range(n)]
        row_common = common[kind[g]]
        blacks = [sum(t) for t in zip(*cols)]
        # black * (n + 1) + (total - black) = black * n + total
        table.append([b * n + row_common[k] for b, k in zip(blacks, kind)])
    return table


def knuth_choice(table, live):
    """Knuth's rule: the guess whose largest answer class among the live codes is smallest.

    Ties go first to a guess that is still a live code, then to the lowest index.
    `live` is a sorted list of indices of the codes that fit all answers so far.
    """
    if len(live) <= 2:
        return live[0]
    in_live = set(live)
    best = None
    for g, row in enumerate(table):
        worst = max(Counter(map(row.__getitem__, live)).values())
        key = (worst, g not in in_live, g)
        if best is None or key < best:
            best = key
    return best[2]


def knuth_strategy(pegs=4, colors=6, first=(0, 0, 1, 1)):
    """Run Knuth's strategy on every secret code.

    Returns a list: entry s is the number of guesses used for secret s,
    counting the last, correct guess.
    """
    codes = all_codes(pegs, colors)
    table = score_table(codes, colors)
    win = pegs * pegs + pegs  # black = pegs, white = 0
    used = [0] * len(codes)
    stack = [(codes.index(tuple(first)), list(range(len(codes))), 1)]
    while stack:
        guess, live, depth = stack.pop()
        row = table[guess]
        classes = {}
        for s in live:
            classes.setdefault(row[s], []).append(s)
        for answer, part in classes.items():
            if answer == win:
                used[part[0]] = depth
            else:
                stack.append((knuth_choice(table, part), part, depth + 1))
    return used


def largest_class(guess, pegs=4, colors=6):
    """Size of the largest answer class when `guess` is the first guess."""
    codes = all_codes(pegs, colors)
    return max(Counter(score(guess, s, colors) for s in codes).values())


def most_codes_solvable(guesses, answers):
    """Most codes that `guesses` more guesses can always tell apart, with `answers` possible scores.

    One code is found when the guess is right; every other score must leave a
    set that the remaining guesses can solve.
    """
    if guesses <= 1:
        return guesses
    return 1 + (answers - 1) * most_codes_solvable(guesses - 1, answers)
