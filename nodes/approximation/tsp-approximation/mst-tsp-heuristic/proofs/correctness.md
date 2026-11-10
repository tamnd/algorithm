---
title: The MST-based tours cost at most 2 OPT or 3/2 OPT, and 2-opt keeps the bound
proves: [correctness]
status: full
---

The costs $c$ on $V$, with $|V| = n \ge 2$, are symmetric, non-negative and satisfy the triangle inequality. For a walk $P = (p_0, \ldots, p_m)$, $c(P) = \sum_{i=1}^m c(p_{i-1}, p_i)$, and the cost of a tour includes its closing edge.

**Lemma 1 (shortcuts).** If a closed walk $W$ visits each vertex of a set $S$, then the vertices of $S$ in the order of their first visit, read as a cycle, cost at most $c(W)$.

*Proof.* For each walk, $c(p_0, p_m) \le c(p_0, \ldots, p_m)$ by induction on $m$ with the triangle inequality. The edges of the cycle replace parts of $W$ that do not overlap, the last one wrapping around from the last first visit to the end of $W$ and on to the first first visit. Sum the inequalities. $\square$

**Lemma 2 (lower bounds).** $c(T) \le \text{OPT}$. If $O$ is the set of odd-degree vertices of $T$ and $M$ is a minimum weight perfect matching on $O$, then $c(M) \le \text{OPT}/2$.

*Proof.* An optimal tour without one edge is a spanning tree, so $c(T) \le \text{OPT}$. The degree sum of $T$ is $2(n-1)$, so $|O|$ is even. By Lemma 1 with $S = O$, the optimal tour gives a cycle on $O$ of cost at most OPT. It has an even number of edges, so its odd-numbered edges and its even-numbered edges are two perfect matchings of $O$ whose costs add up to the cost of the cycle. One of them costs at most OPT$/2$, and $M$ costs no more. $\square$

**Lemma 3 (the circuit).** In both cases of lines L2 to L4, $T + A$ is connected and all its degrees are even, so it has an Euler circuit $W$ with $c(W) = c(T) + c(A)$.

*Proof.* $T + A$ contains $T$, so it is connected. With DOUBLE, each degree is $2\deg_T(v)$. With MATCHING, each vertex of $O$ gets exactly one edge of $A$ and the other vertices get none, so each degree becomes even. Euler's theorem gives the circuit, which uses each edge of the multigraph exactly one time. $\square$

**Lemma 4 (2-opt).** If $H$ is a tour and $(i, j)$ is an improving 2-opt move, then reversing $H[i+1 .. j]$ gives a tour $H'$ with $c(H') < c(H)$. The loop of lines L7 and L8 stops.

*Proof.* The reversal keeps the set of vertices, so $H'$ is a tour. All edges of $H$ stay in $H'$ except $\{h_i, h_{i+1}\}$ and $\{h_j, h_{j+1}\}$, which are replaced by $\{h_i, h_j\}$ and $\{h_{i+1}, h_{j+1}\}$; the edges inside the reversed part are the same edges, walked in the other direction, and the costs are symmetric. So $c(H') - c(H) = c(h_i, h_j) + c(h_{i+1}, h_{j+1}) - c(h_i, h_{i+1}) - c(h_j, h_{j+1}) < 0$. Each step strictly lowers the cost, so no tour repeats, and there are finitely many tours. $\square$

**Theorem.** MST-TSP returns a tour $H$. With DOUBLE, $c(H) \le 2 \cdot \text{OPT}$. With MATCHING, $c(H) \le \tfrac{3}{2} \cdot \text{OPT}$. This holds with and without the 2-opt loop.

*Proof.* $W$ uses each edge of the spanning tree $T$, so it visits each vertex, and line L6 makes a tour $H_0$. By Lemma 1 with $S = V$ and Lemma 3, $c(H_0) \le c(T) + c(A)$. With DOUBLE, $c(A) = c(T)$, so $c(H_0) \le 2c(T) \le 2 \cdot \text{OPT}$ by Lemma 2. With MATCHING, $A = M$, so $c(H_0) \le \text{OPT} + \text{OPT}/2$ by Lemma 2. By Lemma 4 the loop stops, and each tour that it makes costs less than the one before, so the final tour costs at most $c(H_0)$. $\blacksquare$
