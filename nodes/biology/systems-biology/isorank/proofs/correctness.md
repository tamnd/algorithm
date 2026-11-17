---
title: The IsoRank iteration converges to a personalized PageRank, and the greedy matching is within one half
proves: [correctness]
status: full
---

**Setup.** Let $G_1$ have nodes $1, \ldots, n$ and $G_2$ have nodes $1, \ldots, m$, with neighbor sets $N(\cdot)$ and degrees $d(\cdot) = |N(\cdot)|$. Let $E \ge 0$ be an $n \times m$ matrix with entries adding up to 1, and $\alpha \in [0, 1)$. For a matrix $R$, read as a vector indexed by pairs, define

$$(A R)_{ij} = \sum_{u \in N(i)} \sum_{v \in N(j)} \frac{R_{uv}}{d(u) \, d(v)}, \qquad F(R) = \alpha A R + (1 - \alpha) E.$$

Write $\lVert R \rVert_1 = \sum_{i, j} |R_{ij}|$.

**Lemma 1 (column sums).** For every pair $(u, v)$, $\sum_{(i, j)} A_{(i, j), (u, v)}$ is 1 if $d(u) d(v) > 0$ and 0 otherwise. Hence $\lVert A R \rVert_1 \le \lVert R \rVert_1$ for every $R$, with equality for $R \ge 0$ supported on pairs with no isolated node.

*Proof.* The entry $A_{(i, j), (u, v)}$ is $1/(d(u) d(v))$ when $i \in N(u)$ and $j \in N(v)$, which holds for exactly $d(u) d(v)$ pairs $(i, j)$ because the graphs are undirected, and 0 otherwise. So the column sum is $d(u) d(v) / (d(u) d(v)) = 1$, or 0 when the column has no non-zero entry. Then $\lVert A R \rVert_1 \le \sum_{(i, j)} \sum_{(u, v)} A_{(i, j), (u, v)} |R_{uv}| = \sum_{(u, v)} |R_{uv}| \cdot (\text{column sum}) \le \lVert R \rVert_1$, with equality in the stated case because every term is non-negative and every column sum used is 1. $\square$

**Lemma 2 (the two passes).** With $S_{uv} = R_{uv} / (d(u) d(v))$ (and 0 when a degree is 0) and $P_{iv} = \sum_{u \in N(i)} S_{uv}$, $(A R)_{ij} = \sum_{v \in N(j)} P_{iv}$.

*Proof.* $\sum_{v \in N(j)} P_{iv} = \sum_{v \in N(j)} \sum_{u \in N(i)} S_{uv}$. A node $u \in N(i)$ has $d(u) \ge 1$, and $v \in N(j)$ has $d(v) \ge 1$, so $S_{uv} = R_{uv}/(d(u) d(v))$ for every term, which is the definition of $(A R)_{ij}$. $\square$

So line L4, as computed in the code, is $R \leftarrow F(R)$.

**Theorem 1 (fixed point and convergence).** $F$ has exactly one fixed point $R^\ast$. It equals $(1 - \alpha) \sum_{k \ge 0} \alpha^k A^k E$, it is non-negative, and the iterates $R_0 = E$, $R_{t+1} = F(R_t)$ satisfy $\lVert R_t - R^\ast \rVert_1 \le \alpha^t \lVert E - R^\ast \rVert_1$. If no node of either graph is isolated, the entries of $R^\ast$ add up to 1 and $\lVert E - R^\ast \rVert_1 \le 2$.

*Proof.* By Lemma 1, $\lVert F(R) - F(R') \rVert_1 = \alpha \lVert A (R - R') \rVert_1 \le \alpha \lVert R - R' \rVert_1$. So $F$ is a contraction of the complete space $(\mathbb{R}^{n \times m}, \lVert \cdot \rVert_1)$, and by the Banach fixed point theorem it has exactly one fixed point $R^\ast$, and $\lVert R_t - R^\ast \rVert_1 = \lVert F(R_{t-1}) - F(R^\ast) \rVert_1 \le \alpha \lVert R_{t-1} - R^\ast \rVert_1$, which gives the bound by induction.

The series $Q = (1 - \alpha) \sum_{k \ge 0} \alpha^k A^k E$ converges, since $\lVert \alpha^k A^k E \rVert_1 \le \alpha^k$ by Lemma 1. It satisfies $\alpha A Q + (1 - \alpha) E = (1 - \alpha) \sum_{k \ge 1} \alpha^k A^k E + (1 - \alpha) E = Q$, so $Q$ is a fixed point and $Q = R^\ast$ by uniqueness. Every term is non-negative because $A \ge 0$ and $E \ge 0$, so $R^\ast \ge 0$.

If no node is isolated, every column sum of $A$ is 1 by Lemma 1, so the sum of the entries of $A^k E$ is the sum of the entries of $E$, which is 1. Then the sum of the entries of $R^\ast$ is $(1 - \alpha) \sum_k \alpha^k = 1$, and $\lVert E - R^\ast \rVert_1 \le \lVert E \rVert_1 + \lVert R^\ast \rVert_1 = 2$. $\square$

**Theorem 2 (personalized PageRank on the product graph).** Let $H$ be the graph on the pairs $(i, j)$ with $(i, j) \sim (u, v)$ when $i \sim u$ in $G_1$ and $j \sim v$ in $G_2$, and let $W$ be its random walk matrix, $W_{z, w} = 1 / \deg_H(w)$ for $z \sim w$. Then $W = A$ on the columns of pairs with no isolated node, and $R^\ast$ is the personalized PageRank $x = \alpha W x + (1 - \alpha) E$ of $H$ with restart law $E$.

*Proof.* The neighbors of $(u, v)$ in $H$ are the pairs $(i, j)$ with $i \in N(u)$ and $j \in N(v)$, so $\deg_H(u, v) = d(u) d(v)$, and $W_{(i, j), (u, v)} = 1/(d(u) d(v)) = A_{(i, j), (u, v)}$ for these pairs; both are 0 otherwise. A pair with an isolated node has no neighbor in $H$, and its column is 0 in both. So $W = A$, the two equations are the same, and by Theorem 1 they have the same unique solution. $\square$

**Theorem 3 (greedy matching).** Let $M$ be the matching of line L7 for scores $R \ge 0$, and $M^\ast$ a matching of largest total score. Then $\sum_{(i, j) \in M} R_{ij} \ge \frac12 \sum_{(i, j) \in M^\ast} R_{ij}$.

*Proof.* Take a pair $p = (i, j) \in M^\ast$. If $p \in M$, charge it to itself. Otherwise line L7 skipped $p$, so when $p$ was visited, $i$ or $j$ was already in a pair $q \in M$ taken earlier, and $R_q \ge R_p$ because the pairs are visited by decreasing score; charge $p$ to such a $q$. A pair $q = (u, v) \in M$ receives a charge only from pairs of $M^\ast$ that contain $u$ or $v$, and since $M^\ast$ is a matching there are at most two such pairs, each with score at most $R_q$. So $\sum_{M^\ast} R_p \le \sum_{q \in M} 2 R_q$. $\square$

**Remark.** The bound of Theorem 3 is tight: for $R = \begin{pmatrix} 1 + \epsilon & 1 \\ 1 & 0 \end{pmatrix}$ the greedy matching has score $1 + \epsilon$ and the best has score 2. None of the three theorems says that $M$ is a good alignment for a measure of conserved edges; that part of IsoRank is a heuristic.
