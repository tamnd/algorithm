---
title: Or-opt moves are 3-opt moves, and the search ends at an Or-optimal tour
proves: [correctness]
status: full
---

The costs $d$ on the city set $V$, with $|V| = n$, are symmetric and non-negative. The tour is a cycle $T$. An Or-opt move takes a *segment* $S = s_1, \ldots, s_L$ of $L \in \{1, 2, 3\}$ consecutive cities, with $L \le n - 3$, its tour neighbors $p$ (before $s_1$) and $q$ (after $s_L$), and a tour edge $\{u, v\}$, with $u$ before $v$, that does not touch $S$, other than the edge $\{p, s_1\}$. The move puts $S$ between $u$ and $v$, either in its old direction or reversed.

**Lemma 1 (the result is a tour, and the gain).** The move gives a tour, and the cost goes down by

$$g = d(p, s_1) + d(s_L, q) + d(u, v) - d(p, q) - d(u, h) - d(t, v),$$

where $(h, t) = (s_1, s_L)$ for the old direction and $(h, t) = (s_L, s_1)$ for the reversed one.

*Proof.* Removing $S$ and joining $p$ to $q$ leaves a cycle through the other $n - L \ge 3$ cities. This cycle holds every old tour edge that does not touch $S$, so it holds $\{u, v\}$. Replacing $\{u, v\}$ by the path $u, h, \ldots, t, v$ gives a cycle through all $n$ cities. The removed edges are $\{p, s_1\}$, $\{s_L, q\}$ and $\{u, v\}$, and the added edges are $\{p, q\}$, $\{u, h\}$ and $\{t, v\}$, so the cost goes down by $g$. $\square$

The implementation chooses $\{u, v\}$ as the edge from position $P$ to position $P + 1$, with $P$ outside $S$ and $P$ not the position of $p$. This leaves out exactly the edges that touch $S$. The test file checks Lemma 1 on all moves of seeded tours.

**Lemma 2 (Or-opt is inside 3-opt).** Each Or-opt move removes at most three edges and adds at most three, so it is a [3-opt](/three-opt/) move. A 3-optimal tour is Or-optimal.

*Proof.* By Lemma 1, the move removes the three tour edges $\{p, s_1\}$, $\{s_L, q\}$ and $\{u, v\}$ and gives a tour. Removing these three edges cuts the old tour into three paths: $S$, the path from $q$ to $u$, and the path from $v$ to $p$ (or the same with $u$ and $v$ exchanged, when $\{u, v\}$ lies on the other side). The new tour is made of the same three paths and three new edges. So it is one of the 8 ways to join three paths into a cycle that the [3-opt](/three-opt/) page lists, for the triple of positions of the three removed edges, and the 3-opt search tests it. A tour that no 3-opt move improves therefore has no Or-opt move that gains. $\square$

**Theorem.** The Or-opt search stops, and it returns an Or-optimal tour, that is, a tour on which no move of Lemma 1 has $g > 0$.

*Proof.* Each accepted move has $g > \varepsilon \ge 0$, so the cost goes down strictly. There are finitely many tours, so the search stops. It stops only when no move has $g > \varepsilon$. With $\varepsilon = 0$ this is an Or-optimal tour; the implementation uses $\varepsilon = 10^{-12}$ to protect against rounding. $\blacksquare$

**Remarks.**

- **No ratio is proved here.** An Or-optimal tour need not be 2-optimal. The test file checks the tour of 16 points in two rows, $(x, 10)$ and $(x, 0)$ for $x = 0, \ldots, 7$, that runs along the top row, crosses to the bottom left, runs along the bottom row and crosses back. No Or-opt move gains, but the two diagonals cross, so a 2-opt move gains. So the bound for 2-optimal tours on the [2-opt](/two-opt/) page does not apply to Or-opt alone. This page proves no worst-case ratio for Or-optimal tours.
- **Or-opt with 2-opt.** A tour that is both Or-optimal and 2-optimal satisfies the bound $4\sqrt{2}\,\sqrt{n} \cdot \text{OPT}$ of the 2-opt page for metric costs, because that proof uses only 2-optimality.
