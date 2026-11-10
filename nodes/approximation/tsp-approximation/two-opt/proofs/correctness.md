---
title: Every 2-optimal tour costs O(√n) OPT on metric instances, and has no crossings in the plane
proves: [correctness]
status: full
---

The costs $d$ on the city set $V$, with $|V| = n \ge 4$, are symmetric, non-negative and satisfy the triangle inequality. A tour $T$ is *2-optimal* if no 2-opt move makes it shorter. Orient $T$, and write $a \to b$ for a tour edge from $a$ to its successor $b$. For two edges $a \to b$ and $c \to e$, the 2-opt move removes them and adds $\{a, c\}$ and $\{b, e\}$, and it reverses the path from $b$ to $c$. The bound below is the bound of Chandra, Karloff and Tovey (1999) with a different constant, $4\sqrt{2}$ instead of 4, and with a self-contained proof.

**Termination.** Each move makes the tour strictly shorter (by more than a fixed $\varepsilon$ in the implementation), and there are finitely many tours, so the search stops. When it stops, no move gains, so the tour is 2-optimal. The number of moves is not bounded by a polynomial; see the page.

**Lemma 1 (the 2-opt inequality).** If $T$ is 2-optimal, then for all tour edges $a \to b$ and $c \to e$,

$$d(a, b) + d(c, e) \le d(a, c) + d(b, e).$$

*Proof.* If the edges are not adjacent, this is the statement that the move does not gain. If they are the same edge, both sides are $2d(a, b)$ because $a = c$, $b = e$, and $d(a, a) = 0$. If $b = c$, the right side is $d(a, b) + d(b, e)$, which is the left side. The case $e = a$ is the same. $\square$

**Lemma 2 (few long edges).** Let $T$ be 2-optimal, and let $0 < \Lambda < \text{OPT}/2$. Then fewer than $8\, (\text{OPT}/\Lambda)^2$ edges of $T$ are longer than $\Lambda$.

*Proof.* Let $a_1 \to b_1, \ldots, a_k \to b_k$ be the edges of $T$ longer than $\Lambda$, with $k \ge 1$, and let $r = \Lambda/2$ and $x = \text{OPT}/r > 4$. The tails $a_1, \ldots, a_k$ are different cities, and so are the heads.

*Step 1: tails and heads cannot both be close.* If $d(a_i, a_j) \le r$ and $d(b_i, b_j) \le r$ for some $i \ne j$, then by Lemma 1, $d(a_i, b_i) + d(a_j, b_j) \le 2r = \Lambda$. This is false, since both edges are longer than $\Lambda$.

*Step 2: group the tails.* Shortcut an optimal tour to the tails. This gives a cycle through $a_1, \ldots, a_k$ of length at most OPT. Remove one edge of the cycle, and walk along the remaining path. Cut the path into groups of consecutive tails: a new group starts when the path length from the first tail of the current group to the next tail would be more than $r$. In each group, any two tails are joined by a part of the path of length at most $r$, so they are at distance at most $r$. For each group except the last, its path length plus the edge to the next group is more than $r$, and these parts of the path are disjoint. So (the number of groups $- 1$) $\cdot\, r < \text{OPT}$, and there are fewer than $x + 1$ groups.

*Step 3: the heads of one group are spread out.* Let a group have $s$ tails. By Step 1, the heads of these tails are at distance more than $r$ from each other. If $s \ge 2$, shortcut an optimal tour to these $s$ heads. The cycle has $s$ edges, each longer than $r$, so $s r < \text{OPT}$ and $s < x$. If $s = 1$, then $s < x$ since $x > 4$.

So $k < (x + 1) \cdot x < 2 x^2 = 8 (\text{OPT}/\Lambda)^2$, using $x > 1$. $\square$

**Lemma 3 (one edge).** Each edge of a tour has cost at most $\text{OPT}/2$.

*Proof.* An optimal tour holds two paths between the ends of the edge, with no common edge, and each costs at least the cost of the edge, by the triangle inequality. $\square$

**Theorem 1 (the ratio of a 2-optimal tour).** For metric costs, every 2-optimal tour $T$ satisfies

$$\text{ALG} \le 2\sqrt{2} \left(\sum_{i=1}^{n} \frac{1}{\sqrt{i}}\right) \text{OPT} < 4\sqrt{2}\, \sqrt{n} \cdot \text{OPT}.$$

*Proof.* Sort the edge costs of $T$ as $\ell_1 \ge \ell_2 \ge \cdots \ge \ell_n$. Fix $i$ with $\ell_i > 0$, and take any $\Lambda < \ell_i$. By Lemma 3, $\Lambda < \text{OPT}/2$. At least $i$ edges are longer than $\Lambda$, so by Lemma 2, $i < 8 (\text{OPT}/\Lambda)^2$, that is $\Lambda < \sqrt{8/i}\; \text{OPT}$. This holds for all $\Lambda < \ell_i$, so $\ell_i \le \sqrt{8/i}\; \text{OPT}$. Add over $i$, and use $\sum_{i \le n} i^{-1/2} < 2\sqrt{n}$. $\blacksquare$

**Theorem 2 (no crossings in the plane).** Let the cities be points in the plane with the Euclidean distance. If two edges $\{a, b\}$ and $\{c, e\}$ of a tour cross at a point $p$ that is inside both segments, and the segments are not on one line, then a 2-opt move on these two edges makes the tour strictly shorter. So a 2-optimal tour has no such crossing.

*Proof.* Orient the tour so that the edges are $a \to b$ and $c \to e$; the move adds $\{a, c\}$ and $\{b, e\}$. By the triangle inequality, $d(a, c) \le d(a, p) + d(p, c)$ and $d(b, e) \le d(b, p) + d(p, e)$. The sum of the right sides is $d(a, b) + d(c, e)$, because $p$ lies on both segments. Equality in the first inequality needs $p$ on the segment from $a$ to $c$; then $c$ is on the line through $a$ and $p$, which is the line of the first segment, and the segments are on one line. So the first inequality is strict, and the move gains. $\blacksquare$

**Remarks.**

- Theorem 1 uses only Lemma 1, so it holds for every tour that is a local optimum of a neighborhood that contains the 2-opt moves: 3-opt, Lin-Kernighan and the others.
- The order $\sqrt{n}$ is right for metric costs. Chandra, Karloff and Tovey gave instances with 2-optimal tours of ratio $\frac{1}{4}\sqrt{n}$, and Hougardy, Zaiser and Zhong (2020) showed that the exact worst-case ratio is $\sqrt{n/2}$. These results are quoted, not proved, here. The test file checks Theorem 1 and Lemma 2 on all 2-optimal tours of small seeded instances.
