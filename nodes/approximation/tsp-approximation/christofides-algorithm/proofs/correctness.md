---
title: Christofides' algorithm returns a tour of cost at most 3/2 OPT
proves: [correctness]
status: full
---

The costs $c$ on $V$, with $|V| = n \ge 2$, are symmetric, non-negative and satisfy the triangle inequality. For a walk $P = (p_0, \ldots, p_m)$, $c(P) = \sum_{i=1}^{m} c(p_{i-1}, p_i)$, and for a tour the closing edge is included.

**Lemma 1 (shortcuts).** For each walk $(p_0, \ldots, p_m)$, $c(p_0, p_m) \le c(p_0, \ldots, p_m)$. So if a closed walk $W$ visits each vertex of a set $S$, the list of the first visits to the vertices of $S$, read as a cycle, costs at most $c(W)$.

*Proof.* The first claim is induction on $m$ with the triangle inequality $c(p_0, p_m) \le c(p_0, p_{m-1}) + c(p_{m-1}, p_m)$. For the second, let the first visits be at the indices $j_1 < \cdots < j_k$ of $W = (w_0, \ldots, w_L)$, with $w_0 = w_L$. Each edge of the cycle, from $w_{j_i}$ to $w_{j_{i+1}}$, costs at most the part of $W$ between these indices, and the closing edge from $w_{j_k}$ to $w_{j_1}$ costs at most the part from $j_k$ to $L$ followed by the part from 0 to $j_1$. These parts do not overlap, so the sum is at most $c(W)$. $\square$

**Lemma 2 (the tree).** $c(T) \le \text{OPT}$.

*Proof.* An optimal tour without one of its edges is a spanning path, so a spanning tree, and its cost is at most OPT because costs are non-negative. $T$ is a minimum spanning tree. $\square$

**Lemma 3 (parity).** The set $O$ of vertices of odd degree in $T$ has an even size.

*Proof.* $\sum_v \deg_T(v) = 2(n - 1)$ is even. The vertices of even degree add an even number to the sum, so the number of vertices of odd degree is even. $\square$

**Lemma 4 (the matching).** $c(M) \le \text{OPT}/2$.

*Proof.* If $O$ is empty, $c(M) = 0$. Otherwise let $H^*$ be an optimal tour. By Lemma 1 with $S = O$, the vertices of $O$ in the order of $H^*$ form a cycle $C_O = (o_1, \ldots, o_k)$ with $c(C_O) \le \text{OPT}$. By Lemma 3, $k$ is even. The edge sets $M_1 = \{o_1 o_2, o_3 o_4, \ldots, o_{k-1} o_k\}$ and $M_2 = \{o_2 o_3, \ldots, o_{k-2} o_{k-1}, o_k o_1\}$ are perfect matchings of $O$, and $c(M_1) + c(M_2) = c(C_O)$. So $\min(c(M_1), c(M_2)) \le \text{OPT}/2$, and $M$ is a perfect matching of minimum cost. $\square$

**Lemma 5 (the circuit).** The multigraph $T + M$ has an Euler circuit $W$, and $c(W) = c(T) + c(M)$.

*Proof.* A vertex not in $O$ has even degree in $T$ and no edge of $M$. A vertex in $O$ has odd degree in $T$ and exactly one edge of $M$. So all degrees in $T + M$ are even. $T + M$ contains the spanning tree $T$, so it is connected. By Euler's theorem it has a closed walk that uses each edge exactly one time, so $c(W) = c(T) + c(M)$, where an edge in both $T$ and $M$ is counted two times. $\square$

**Theorem.** CHRISTOFIDES returns a tour $H$ with $c(H) \le c(T) + c(M) \le \tfrac{3}{2} \cdot \text{OPT}$.

*Proof.* $W$ visits each vertex, because it uses each edge of $T$. Lines L5 to L8 keep the first visit of each vertex, so $H$ holds each vertex exactly one time, and it is a tour. By Lemma 1 with $S = V$, $c(H) \le c(W)$. By Lemma 5, $c(W) = c(T) + c(M)$, and by Lemmas 2 and 4 this is at most $\text{OPT} + \text{OPT}/2$. $\blacksquare$

The proof uses only the facts that $T$ is a minimum spanning tree and $M$ is a minimum perfect matching on $O$. The choice of the Euler circuit and the order of the shortcuts do not change the bound.
