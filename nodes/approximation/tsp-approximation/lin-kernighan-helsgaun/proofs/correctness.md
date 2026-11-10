---
title: The 1-tree bound, the ascent direction and the formula for alpha-nearness
proves: [correctness]
status: full
---

The costs $d$ on the city set $V$, with $|V| = n \ge 3$, are symmetric. One city $s$ is special, and $V' = V \setminus \{s\}$. A *1-tree* is a spanning tree on $V'$ plus two edges at $s$. For a vector $\pi$ of real numbers, one per city, the transformed cost is $d_\pi(i, j) = d(i, j) + \pi_i + \pi_j$. $T_\pi$ is a minimum 1-tree for $d_\pi$, $L(T_\pi)$ is its cost, and $w(\pi) = L(T_\pi) - 2 \sum_i \pi_i$.

This file proves the facts that the candidate part of LKH rests on. It does not prove anything about the quality of LKH tours; those claims are measured.

**Lemma 1 (the transform does not change the order of tours).** For each tour $H$, $d_\pi(H) = d(H) + 2 \sum_i \pi_i$.

*Proof.* Each city has degree 2 in $H$, so each $\pi_i$ is added twice. $\square$

So a search on $d$ and a search on $d_\pi$ compare tours in the same way. The implementation searches on $d$.

**Theorem 1 (the 1-tree bound).** For each $\pi$, $w(\pi) \le \text{OPT}$. If $T_\pi$ is a tour, it is an optimal tour.

*Proof.* Let $H$ be an optimal tour. Removing $s$ from $H$ leaves a Hamiltonian path on $V'$, which is a spanning tree of $V'$, and $s$ has two edges in $H$. So $H$ is a 1-tree, and $L(T_\pi) \le d_\pi(H) = \text{OPT} + 2 \sum_i \pi_i$ by Lemma 1. This gives $w(\pi) \le \text{OPT}$. If $T_\pi$ is a tour, then by Lemma 1 its cost under $d$ is $L(T_\pi) - 2 \sum_i \pi_i = w(\pi) \le \text{OPT}$, so it is optimal. $\square$

**Lemma 2 (the ascent direction).** $w$ is concave, and $g_i = \deg_{T_\pi}(i) - 2$ is a subgradient at $\pi$: for each $\pi'$, $w(\pi') \le w(\pi) + \sum_i (\pi'_i - \pi_i) g_i$.

*Proof.* For a fixed 1-tree $T$, $d_\pi(T) - 2 \sum_i \pi_i = d(T) + \sum_i \pi_i (\deg_T(i) - 2)$, which is affine in $\pi$. $w$ is the minimum of these affine functions over all 1-trees, so it is concave. For $T = T_\pi$, $w(\pi') \le d(T_\pi) + \sum_i \pi'_i g_i = w(\pi) + \sum_i (\pi'_i - \pi_i) g_i$. $\square$

So the step $\pi \leftarrow \pi + t g$ raises $\pi_i$ at cities of degree above 2 and lowers it at leaves. The implementation keeps the best $w$ it sees, so by Theorem 1 its result is a valid lower bound for any step sizes.

The *alpha-nearness* of a pair is $\alpha(i, j) = L(T^{+}(i, j)) - L(T)$, where $T$ is a minimum 1-tree and $T^{+}(i, j)$ is a minimum 1-tree that holds the edge $\{i, j\}$. The costs here are the transformed ones; write $d$ for them.

**Theorem 2 (the formula for alpha).** Let $M$ be the spanning tree on $V'$ in the minimum 1-tree $T$.

1. If $\{i, j\}$ is an edge of $T$, then $\alpha(i, j) = 0$.
2. If $i, j \in V'$ and $\{i, j\}$ is not in $M$, then $\alpha(i, j) = d(i, j) - \beta(i, j)$, where $\beta(i, j)$ is the largest cost of an edge on the path from $i$ to $j$ in $M$.
3. If $\{s, j\}$ is not in $T$, then $\alpha(s, j) = d(s, j) - d(s, u_2)$, where $\{s, u_1\}$ and $\{s, u_2\}$ are the two edges of $T$ at $s$ and $d(s, u_1) \le d(s, u_2)$.

In each case $\alpha \ge 0$.

*Proof.* Part 1 is clear, since $T$ itself holds the edge.

A 1-tree is a spanning tree on $V'$ and two edges at $s$, and the two parts can be chosen apart. So a minimum 1-tree is a minimum spanning tree on $V'$ plus the two cheapest edges at $s$.

Part 2. The edge $\{i, j\}$ does not touch $s$, so $T^{+}(i, j)$ is a minimum spanning tree $S$ of $V'$ among those that hold $e = \{i, j\}$, plus the two cheapest edges at $s$. Thus $\alpha(i, j) = d(S) - d(M)$.

- *Upper bound.* Let $f$ be an edge of largest cost on the path from $i$ to $j$ in $M$. Then $M + e - f$ is a spanning tree that holds $e$, so $d(S) \le d(M) + d(i, j) - \beta(i, j)$.
- *Lower bound.* Removing $e$ from $S$ cuts $V'$ into a part $X$ with $i$ and a part $Y$ with $j$. The path from $i$ to $j$ in $M$ starts in $X$ and ends in $Y$, so one of its edges $f'$ goes from $X$ to $Y$. Then $S - e + f'$ is a spanning tree of $V'$, so $d(M) \le d(S) - d(i, j) + d(f')$. Since $d(f') \le \beta(i, j)$, this gives $d(S) \ge d(M) + d(i, j) - \beta(i, j)$.

Also $M + e - f$ is a spanning tree, so $d(M) \le d(M) + d(i, j) - \beta(i, j)$, which gives $\alpha(i, j) \ge 0$.

Part 3. Here $T^{+}(s, j)$ is $M$ plus $\{s, j\}$ plus the cheapest other edge at $s$. Since $\{s, j\}$ is not in $T$, the cheapest other edge costs $d(s, u_1)$. So $\alpha(s, j) = d(s, j) + d(s, u_1) - d(s, u_1) - d(s, u_2) = d(s, j) - d(s, u_2)$. Because $T$ uses the two cheapest edges at $s$ and $\{s, j\}$ is not one of them, $d(s, j) \ge d(s, u_2)$, so $\alpha(s, j) \ge 0$. $\blacksquare$

**Computing alpha.** For each $i \in V'$, one walk over $M$ from $i$ gives $\beta(i, j)$ for all $j$ in $O(n)$ time, since $\beta$ along the walk is the maximum of $\beta$ at the parent and the cost of the edge to the parent. All values cost $O(n^2)$ time. The test file checks Theorem 2 against an enumeration of all 1-trees for $n \le 6$.

**The search part.** The implementation runs the Lin-Kernighan search of the [Lin-Kernighan](/lin-kernighan/) page with the alpha lists as candidates. The proof there of exact steps and of termination does not depend on the candidate lists, so it holds here too. LKH itself uses sequential 5-opt basic steps, which this file does not cover.
