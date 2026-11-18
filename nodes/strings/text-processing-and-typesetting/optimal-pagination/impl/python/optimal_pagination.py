# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimal-pagination/. The authors are listed in prov/VBW9VJ.jsonl.

"""Optimal pagination of text lines and figures by dynamic programming.

The model of the page. There are n lines of text with heights h_1 .. h_n
and m figures with heights f_1 .. f_m. Figure t is referenced from the
line r_t, with 1 <= r_1 <= r_2 <= ... <= r_m <= n. A page holds a block of
consecutive lines and a block of consecutive figures (both may be empty,
but not both), so the lines and the figures each keep their order. The
total height of a page is at most H. Figure t must be on the page of
line r_t or later.

The cost of a pagination is the sum over all pages but the last of

    (H - u)^2           the white space u of the page, squared
    + pi[i]             if the page holds lines and its last line is i
    + alpha * w         w = the number of figures referenced on this page
                        or earlier that are not yet placed

The sum of the w terms over the pages is the sum over the figures of
(page of figure t) - (page of line r_t), so alpha weighs how far each
figure floats from its reference. pi[i] is a penalty for a break after
line i (a widow or club penalty, say); pi[0] and pi[n] are not used.

Heights are ints or Fractions. Do not use floats.
"""

import math
from typing import Optional, Sequence


def ref_counts(n: int, refs: Sequence[int]) -> list[int]:
    """R[i] = the number of figures referenced from lines 1 .. i, for i = 0 .. n."""
    R = [0] * (n + 1)
    for r in refs:
        R[r] += 1
    for i in range(1, n + 1):
        R[i] += R[i - 1]
    return R


def check_input(lines: Sequence, figures: Sequence, refs: Sequence[int]) -> None:
    if len(refs) != len(figures):
        raise ValueError("one reference per figure")
    if any(h < 0 for h in lines) or any(f < 0 for f in figures):
        raise ValueError("heights must be >= 0")
    if any(not 1 <= r <= len(lines) for r in refs):
        raise ValueError("a reference must be a line number 1 .. n")
    if any(refs[t] > refs[t + 1] for t in range(len(refs) - 1)):
        raise ValueError("the references must be in order")


def page_cost(H, u, i: int, i2: int, j2: int, R: Sequence[int], alpha, pi: Sequence) -> object:
    """The cost of a page that is not the last one, from state (i, j) to (i2, j2) with height u."""
    c = (H - u) ** 2 + alpha * (R[i2] - j2)
    if i < i2 < len(R) - 1:
        c += pi[i2]
    return c


def optimal_pagination(
    lines: Sequence,
    figures: Sequence,
    refs: Sequence[int],
    H,
    alpha=1,
    pi: Optional[Sequence] = None,
    stats: Optional[dict] = None,
):
    """Return (cost, pages) of a pagination of least cost, or (math.inf, None).

    pages is the list of states (i, j) after each page: page k holds the
    lines i_{k-1}+1 .. i_k and the figures j_{k-1}+1 .. j_k. If stats is a
    dict, stats["relax"] counts the page candidates that were tried.
    """
    check_input(lines, figures, refs)
    n, m = len(lines), len(figures)
    if pi is None:
        pi = [0] * (n + 1)
    LH = [0] * (n + 1)
    for i, h in enumerate(lines):
        LH[i + 1] = LH[i] + h
    FH = [0] * (m + 1)
    for j, f in enumerate(figures):
        FH[j + 1] = FH[j] + f
    R = ref_counts(n, refs)
    relax = 0
    C = [[math.inf] * (m + 1) for _ in range(n + 1)]  # @line L1
    P = [[None] * (m + 1) for _ in range(n + 1)]
    C[0][0] = 0
    for i in range(n + 1):  # @line L2
        for j in range(m + 1):  # @line L3
            if C[i][j] == math.inf:  # @line L4
                continue
            for i2 in range(i, n + 1):  # @line L5
                if LH[i2] - LH[i] > H:
                    break
                for j2 in range(j, m + 1):  # @line L6
                    u = LH[i2] - LH[i] + FH[j2] - FH[j]
                    if j2 > R[i2] or u > H:
                        break
                    if i2 == i and j2 == j:  # @line L7
                        continue
                    relax += 1
                    last = i2 == n and j2 == m
                    d = C[i][j] + (0 if last else page_cost(H, u, i, i2, j2, R, alpha, pi))  # @line L8
                    if d < C[i2][j2]:  # @line L9
                        C[i2][j2] = d
                        P[i2][j2] = (i, j)
    if stats is not None:
        stats["relax"] = relax
    if C[n][m] == math.inf:  # @line L10
        return math.inf, None
    pages = []  # @line L11
    s = (n, m)
    while s != (0, 0):
        pages.append(s)
        s = P[s[0]][s[1]]
    pages.reverse()
    return C[n][m], pages


def pagination_cost(lines, figures, refs, H, pages, alpha=1, pi=None):
    """The cost of a pagination from the page numbers of its lines and figures.

    This does not use the split of the figure term over page breaks: it
    finds the page of every line and every figure and adds the distances.
    It returns math.inf if the pagination is not valid.
    """
    check_input(lines, figures, refs)
    n, m = len(lines), len(figures)
    if pi is None:
        pi = [0] * (n + 1)
    if not pages or pages[-1] != (n, m):
        return math.inf
    line_page = [0] * (n + 1)
    fig_page = [0] * (m + 1)
    cost = 0
    i, j = 0, 0
    for k, (i2, j2) in enumerate(pages, start=1):
        if i2 < i or j2 < j or (i2, j2) == (i, j):
            return math.inf
        u = sum(lines[i:i2]) + sum(figures[j:j2])
        if u > H:
            return math.inf
        for x in range(i + 1, i2 + 1):
            line_page[x] = k
        for t in range(j + 1, j2 + 1):
            fig_page[t] = k
        if k < len(pages):
            cost += (H - u) ** 2
        i, j = i2, j2
    for x in range(1, n):
        if line_page[x] < line_page[x + 1]:
            cost += pi[x]
    for t in range(1, m + 1):
        d = fig_page[t] - line_page[refs[t - 1]]
        if d < 0:
            return math.inf
        cost += alpha * d
    return cost


def all_paginations(n: int, m: int):
    """Every sequence of states from (0, 0) to (n, m), for tiny inputs only."""

    def rec(i, j):
        if (i, j) == (n, m):
            yield []
            return
        for i2 in range(i, n + 1):
            for j2 in range(j, m + 1):
                if (i2, j2) != (i, j):
                    for rest in rec(i2, j2):
                        yield [(i2, j2)] + rest

    return rec(0, 0)


def first_fit_pagination(lines, figures, refs, H):
    """A simple baseline, not optimal: each page first takes the waiting figures
    (referenced on an earlier page) that fit, in order, and then as many lines
    as fit. Returns the pages, or None if some item is taller than H."""
    check_input(lines, figures, refs)
    n, m = len(lines), len(figures)
    R = ref_counts(n, refs)
    pages = []
    i = j = 0
    while (i, j) != (n, m):
        u = 0
        i2, j2 = i, j
        while j2 < R[i] and u + figures[j2] <= H:
            u += figures[j2]
            j2 += 1
        while i2 < n and u + lines[i2] <= H:
            u += lines[i2]
            i2 += 1
        if (i2, j2) == (i, j):
            return None
        pages.append((i2, j2))
        i, j = i2, j2
    return pages
