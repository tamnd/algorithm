---
title: The greedy edge tour costs at most (1/2)(⌈lg n⌉ + 1) OPT on metric instances
proves: [correctness]
status: full
---

The costs $d$ on the city set $V$, with $|V| = n \ge 3$, are symmetric, non-negative and satisfy the triangle inequality. The algorithm scans the pairs $\{u, v\}$ in an order $e_1, e_2, \ldots$ of non-decreasing cost. It keeps a pair if both ends have degree less than 2 in the kept set and the pair does not close a cycle, except that the last pair may close a cycle through all $n$ cities. It stops when it has kept $n$ pairs. The bound is due to Ong and Moore (1984); the proof below goes through the charging lemma of Rosenkrantz, Stearns and Lewis (1977).

**Lemma 1 (the result is a tour).** The kept pairs form a cycle through all cities.

*Proof.* Until the closing pair, the kept set has all degrees at most 2 and no cycle, so it is a set of disjoint paths; a city with no kept pair is a path of length 0. Degrees only go up during the scan, and components only merge. Suppose that the scan ends and the kept set $K$ is not a Hamiltonian cycle. Then $K$ is a set of paths.

If $K$ has two or more paths, let $x$ be an end of one and $y$ an end of another. When the pair $\{x, y\}$ was scanned, $x$ and $y$ had degree at most 1 and were in different components, because this is true at the end. So the pair was kept, and $x$ and $y$ are in one path of $K$, which is false.

If $K$ is one path through all cities, with ends $x \ne y$, then when $\{x, y\}$ was scanned, both had degree at most 1. If they were in different components, the pair was kept, and the ends of the final path are adjacent, which is false for $n \ge 3$. So they were the two ends of one path $P$. If $P$ held all cities at that time, the pair was kept as the closing pair, which is false. Otherwise $P$ grew later, and a path grows only at an end, so $x$ or $y$ got degree 2, which is false.

So the scan ends with a cycle through all $n$ cities. $\square$

Orient the final cycle in one of its two directions. For a city $p$, let $\ell_p$ be the cost of the kept pair that leaves $p$ in this direction. Each kept pair leaves exactly one city, so ALG $= \sum_p \ell_p$.

**Lemma 2 (the greedy property).** For two cities $p \ne q$, $d(p, q) \ge \min(\ell_p, \ell_q)$.

*Proof.* Let $e$ be the closing pair, which is scanned last among the kept pairs, so $d(e) \ge \ell_x$ for each city $x$. If the pair $\{p, q\}$ comes after $e$ in the scan order, then $d(p, q) \ge d(e) \ge \ell_p$. Otherwise $\{p, q\}$ was scanned before or at the time of $e$, and one of these cases holds.

1. *The pair was kept.* Then it leaves $p$ or $q$ in the orientation, so $d(p, q) = \ell_p$ or $d(p, q) = \ell_q$.
2. *The pair was skipped because $p$ (or $q$) had degree 2.* Both kept pairs at $p$ were scanned before $\{p, q\}$, so both cost at most $d(p, q)$. One of them is $\ell_p$.
3. *The pair was skipped because $p$ and $q$ were in one path and the pair would close a short cycle.* Both have degree at most 1, so $p$ and $q$ are the two ends of a path $P$ of kept pairs, and each pair of $P$ was scanned before $\{p, q\}$, so it costs at most $d(p, q)$. In the final cycle, $P$ is one arc from $p$ to $q$. The orientation runs along $P$ either from $p$ to $q$ or from $q$ to $p$. In the first case the pair that leaves $p$ is the first pair of $P$; in the second case the pair that leaves $q$ is the first pair of $P$ from $q$. So $\ell_p \le d(p, q)$ or $\ell_q \le d(p, q)$.

In each case $\min(\ell_p, \ell_q) \le d(p, q)$. $\square$

**Lemma 3 (one edge).** For each city $p$, $\ell_p \le \text{OPT}/2$.

*Proof.* The pair that leaves $p$ goes to a city $q \ne p$. An optimal tour holds two paths from $p$ to $q$ with no common edge, and each costs at least $d(p, q)$ by the triangle inequality. $\square$

**Lemma 4 (the charging bound of Rosenkrantz, Stearns and Lewis).** Let $\ell$ be a non-negative function on $V$ with $d(p, q) \ge \min(\ell_p, \ell_q)$ for all $p \ne q$ and $\ell_p \le \text{OPT}/2$ for all $p$. Then $\sum_p \ell_p \le \frac{1}{2}(\lceil \lg n \rceil + 1) \cdot \text{OPT}$.

*Proof.* Sort the values so that $\ell_1 \ge \cdots \ge \ell_n$. For $1 \le k < n$, let $S$ be the $m = \min(2k, n)$ cities with the largest values. Shortcuts along an optimal tour give a tour of $S$ with cost at most OPT and with $m$ edges. Charge each edge to its end with the smaller value; the edge costs at least that value, and each city takes at most two charges. The $m - k$ smallest values of $S$ can take at most $2(m - k) \le m$ charges, so $\text{OPT} \ge 2 \sum_{i=k+1}^{m} \ell_i$. Use $k = 1, 2, 4, \ldots, 2^{L-1}$ with $L = \lceil \lg n \rceil$: the ranges are disjoint and cover $2, \ldots, n$, so $L \cdot \text{OPT} \ge 2 \sum_{i \ge 2} \ell_i$. Add $\text{OPT} \ge 2 \ell_1$. $\square$

**Theorem (Ong and Moore 1984).** For metric costs, the greedy edge tour satisfies ALG $\le \frac{1}{2}(\lceil \lg n \rceil + 1) \cdot \text{OPT}$.

*Proof.* By Lemmas 2 and 3 the values $\ell_p$ satisfy the conditions of Lemma 4, and ALG $= \sum_p \ell_p$. $\blacksquare$

The bound holds for each order of the pairs with equal cost. It is the same bound as for the [nearest-neighbor heuristic](/nearest-neighbor-tsp/), and the proof is the same after Lemma 2. Frieze (1979) gave instances with ratio of order $\log n / \log \log n$, and Brecklinghaus and Hougardy (2015) gave instances with ratio of order $\log n$, so the ratio of the greedy edge heuristic on metric instances is $\Theta(\log n)$. Those families are quoted, not proved, here.
