---
title: The component test decides point algebra consistency
proves: [correctness, termination]
status: full
---

The input is a point algebra network on the points $0, \ldots, n-1$: each pair $i < j$ has a label $R_{ij} \subseteq \{<, =, >\}$, a missing pair has the universal label, and $R_{ji} = R_{ij}^{\smile}$, where the converse swaps $<$ and $>$ and keeps $=$. A *solution* is a map $v$ from the points to the real numbers with $\mathrm{sign}(v_i - v_j)$ in $R_{ij}$ for every pair. The graph $G$ of line L3 has the edge $i \to j$ exactly when $R_{ij}$ is non-empty and $R_{ij} \subseteq \{<, =\}$.

**Lemma 1 (edges are order constraints).** If $i \to j$ is an edge of $G$, every solution has $v_i \le v_j$. If $i$ and $j$ are in the same strongly connected component, every solution has $v_i = v_j$.

*Proof.* The label of $(i, j)$ allows only $<$ and $=$, so $v_i \le v_j$. In one component there is a directed path from $i$ to $j$ and one from $j$ to $i$. Along each path the values do not decrease, so $v_i \le v_j \le v_i$. $\square$

**Lemma 2 (the numbering).** Tarjan's algorithm numbers the components so that every edge $u \to w$ of $G$ has $\mathrm{comp}(u) \ge \mathrm{comp}(w)$, with equality exactly when $u$ and $w$ are in the same component. So $v_u = t - \mathrm{comp}(u)$ at line L7, where $t$ is the largest number, gives $v_u \le v_w$ on every edge, with $v_u < v_w$ when the components differ.

*Proof.* Tarjan's algorithm outputs a component only after all components that can be reached from it, so a component reached by an edge gets a smaller number. This is the standard property of the algorithm; see [Tarjan's algorithm](/tarjan-scc/). $\square$

**Theorem.** The algorithm returns INCONSISTENT exactly when the network has no solution. When it returns $v$, $v$ is a solution with integer values in $0, \ldots, n-1$.

*Proof.* Suppose it returns INCONSISTENT. At line L1 some label is empty, and no value of $\mathrm{sign}(v_i - v_j)$ is allowed. At line L6 the points $i$ and $j$ are in the same component and $= \notin R_{ij}$; by Lemma 1 every solution has $v_i = v_j$, which the label forbids. In both cases there is no solution.

Suppose it returns $v$, and take a pair $(i, j)$ with the label $r = R_{ij}$, which is not empty.

- If $i$ and $j$ are in the same component, $v_i = v_j$, and line L6 checked that $= \in r$.
- Otherwise the components differ and $v_i \ne v_j$, because each component gets its own number. Say $v_i < v_j$. If $< \notin r$, then $r \subseteq \{=, >\}$, so $R_{ji} = r^{\smile} \subseteq \{<, =\}$ and $j \to i$ is an edge of $G$. By Lemma 2, $v_j < v_i$, a contradiction. So $< \in r$. The case $v_i > v_j$ is the same with the roles of $i$ and $j$ swapped.

So every label holds. The values are $t - \mathrm{comp}(u)$ with $0 \le \mathrm{comp}(u) \le t < n$. $\blacksquare$

**Termination and cost.** Line L1 reads each label once. Line L3 adds at most two edges for each labelled pair, so $G$ has at most $e \le \binom{n}{2}$ edges, and Tarjan's algorithm takes $O(n + e)$ time. Lines L5 and L6 read each label once more, and line L7 takes $O(n)$ time. The total is $O(n + e) = O(n^2)$.
