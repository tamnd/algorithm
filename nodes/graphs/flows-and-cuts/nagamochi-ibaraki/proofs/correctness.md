---
title: The Nagamochi-Ibaraki algorithm returns a global minimum cut
proves: [correctness, termination]
status: full
---

**Setting.** $G = (V, E)$ is undirected with weights $w > 0$ (zero-weight edges are dropped), parallel edges summed, no self-loops, and $n \ge 2$. For a set $X$ and a vertex $v \notin X$, $w(X, v)$ is the weight of the edges between them, and $d(v) = w(V \setminus \{v\}, v)$. For $x \ne y$, $\lambda_G(x, y)$ is the least weight of a cut that separates $x$ and $y$, and $\lambda(G)$ is the least weight of any cut. A vertex of a contracted graph is a group of original vertices, and a cut of a contracted graph is a cut of $G$ of the same weight.

**Lemma 1 (Stoer and Wagner).** If $v_1, \ldots, v_k$ is an MA ordering of a graph $H$ with $k \ge 2$, then $\lambda_H(v_{k-1}, v_k) = d_H(v_k)$.

*Proof.* This is Lemma 2 of the proof on the [Stoer-Wagner](/stoer-wagner/) page: the cut $\{v_k\}$ has weight $d_H(v_k)$, and every cut that separates $v_{k-1}$ and $v_k$ has weight at least $w(\{v_1, \ldots, v_{k-1}\}, v_k) = d_H(v_k)$. That proof uses only the choice rule of the ordering, so it holds for every way of breaking ties. $\square$

**Lemma 2 (the bound $q$).** Let $v_1, \ldots, v_k$ be the MA ordering of a round, and let $e = \{v_i, v_j\}$ with $i < j$. Then $q(e) = w(\{v_1, \ldots, v_i\}, v_j)$ and $q(e) \le \lambda_G(v_i, v_j)$, where $G$ here is the current graph.

*Proof.* $\mathrm{key}(v_j)$ grows by $w(v_l, v_j)$ when $v_l$ is scanned, for each $l < j$, so right after $v_i$ is scanned it is $w(\{v_1, \ldots, v_i\}, v_j)$. Let $H$ be the subgraph induced by $\{v_1, \ldots, v_i, v_j\}$. The sequence $v_1, \ldots, v_i, v_j$ is an MA ordering of $H$: for $l \le i$, the key of a vertex of $H$ when $v_l$ is chosen is the same in $H$ as in $G$, since it counts only edges to $v_1, \ldots, v_{l-1}$, and $v_l$ had a key at least as large as every unscanned vertex of $G$, which includes the unscanned vertices of $H$. By Lemma 1, $\lambda_H(v_i, v_j) = d_H(v_j) = q(e)$. Every cut $C$ of $G$ that separates $v_i$ and $v_j$ gives the cut $C \cap V(H)$ of $H$, which also separates them, and the edges of $H$ that cross it cross $C$; so $w_G(C) \ge w_H(C \cap V(H)) \ge q(e)$. $\square$

**Lemma 3 (progress).** In a round with $\beta > 0$, at least one edge is contracted.

*Proof.* Let $v_k$ be the last vertex of the ordering. After line L3, $\beta \le d(v_k)$. Since $\beta > 0$, $d(v_k) > 0$, so $v_k$ has a neighbor; let $v_i$ be the neighbor scanned last. By Lemma 2, the edge $e = \{v_i, v_k\}$ has $q(e) = w(\{v_1, \ldots, v_i\}, v_k) = d(v_k) \ge \beta$, so it is contracted. $\square$

**Theorem.** The algorithm stops after at most $n - 1$ rounds and returns $\beta = \lambda(G)$ with a set $S$ whose cut has weight $\beta$.

*Proof.* By Lemma 3 every round either stops at line L4 or lowers the number of vertices, so there are at most $n - 1$ rounds. Each value of $\beta$ is the weight of the cut of a group, so $\beta \ge \lambda(G)$ and $w(S) = \beta$ at all times.

Suppose the result is larger than $\lambda(G)$, and let $C$ be a minimum cut of $G$, so $w(C) < \beta$ at all times. We show that $C$ survives every contraction: whenever an edge $e$ is contracted in a round, $q(e) \ge \beta > w(C)$, so by Lemma 2 $C$ does not separate the ends of $e$, if $C$ is a cut of the current graph. By induction, $C$ is a cut of every graph of the run, as a union of groups, so every graph of the run has at least two vertices, one inside $C$ and one outside. So the loop of line L2 never ends by running out of vertices, and it must stop at line L4, with $\beta = 0 \le w(C)$. This contradicts $w(C) < \beta$. So the result is $\lambda(G)$. $\blacksquare$
