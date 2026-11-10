---
tag: QD2ADM
kind: theorem
slug: half-integrality
name: Half-integrality of the vertex cover LP
aliases:
- half-integral solution
- Nemhauser-Trotter half-integrality
- half-integrality of vertex cover
area: approximation/lp-rounding
level: core
summary: Every extreme point of the vertex cover LP has values in {0, 1/2, 1}, and some minimum vertex cover contains all the 1 vertices and none of the 0 vertices.
prereqs: [vertex-cover, lp-relaxation, extreme-point, basic-feasible-solution]
see_also: [lp-rounding-vertex-cover, nemhauser-trotter-theorem, lp-kernelization, parameterized-vertex-cover, crown-reduction, bipartite-double-cover, total-unimodularity, fractional-solution]
sources:
  - paper: doi:10.1007/BF01580444
    title: George L. Nemhauser and Leslie E. Trotter, Vertex packings, structural properties and algorithms, Mathematical Programming 8, 1975
    locator: pages 232 to 248 (half-integral extreme points and the persistency theorem)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 14, Section 14.3 (half-integrality of vertex cover)
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Łukasz Kowalik, Daniel Lokshtanov, Dániel Marx, Marcin Pilipczuk, Michał Pilipczuk and Saket Saurabh, Parameterized Algorithms
    locator: Chapter 2, Section 2.5 (LP-based kernel for vertex cover)
  - paper: "Jianer Chen, Iyad A. Kanj and Weijia Jia, Vertex cover, further observations and further improvements, Journal of Algorithms 41, 2001"
    locator: pages 280 to 301 (a kernel with at most 2k vertices from the Nemhauser-Trotter theorem)
---

Half-integrality is the fact that the [LP relaxation](/lp-relaxation/) of [vertex cover](/vertex-cover/) has only the values $0$, $1/2$ and $1$ at its [extreme points](/extreme-point/). So an optimal LP solution can be taken half-integral, and it can be computed with one minimum cut in place of a general LP solver. Nemhauser and Trotter also showed persistency: some minimum weight cover takes every vertex of value 1 and no vertex of value 0. This gives the threshold rounding of [LP rounding for vertex cover](/lp-rounding-vertex-cover/) and the kernel with at most $2k$ vertices of [LP-based kernelization](/lp-kernelization/).

## Statement

Let $G = (V, E)$ be a finite graph without self-loops, and let

$$P = \{x \in \mathbb{R}^V : x_u + x_v \ge 1 \text{ for each } uv \in E, \; x \ge 0\}, \qquad P_1 = P \cap [0, 1]^V.$$

For weights $w \ge 0$, the vertex cover LP is $\min \{ w \cdot x : x \in P \}$. A vector is *half-integral* when each entry is in $\{0, 1/2, 1\}$. For a half-integral $x$, let $V_0 = \{v : x_v = 0\}$, $V_{1/2} = \{v : x_v = 1/2\}$ and $V_1 = \{v : x_v = 1\}$.

**Theorem 1 (half-integrality).** Each extreme point of $P$, and each extreme point of $P_1$, is half-integral.

**Theorem 2 (persistency, Nemhauser and Trotter 1975).** Let $w \ge 0$ and let $x^*$ be a half-integral optimal solution of the vertex cover LP. Then some minimum weight vertex cover $S$ has $V_1 \subseteq S \subseteq V_1 \cup V_{1/2}$.

**Theorem 3 (double cover).** Let $H$ be the [bipartite double cover](/bipartite-double-cover/) of $G$, with vertices $v^L$ and $v^R$ for each $v \in V$, both of weight $w_v$, and edges $u^L v^R$ and $v^L u^R$ for each $uv \in E$. Then the LP optimum of $G$ is half the minimum weight of a vertex cover of $H$, and a minimum cover $C$ of $H$ gives the half-integral optimum $x_v = |C \cap \{v^L, v^R\}| / 2$.

## In plain words

Write the cover problem as a sum of shares, where each edge asks that its two ends hold at least one full share together. At a corner of this region of answers, each vertex holds nothing, one half, or one whole share. No other amount appears.

The answer at a corner also tells you much about the best real cover. Some best cover takes every vertex that holds a whole share and skips every vertex that holds nothing. Only the vertices that hold one half are still open. If you look for a cover of a given size, at most twice that many vertices stay open, and the rest of the graph can be dropped. A corner of this kind can be found with one minimum cut in a two-sided copy of the graph.

## Proof

**Proof of Theorem 1.** Let $x$ be an extreme point of $P$. First, $x_v \le 1$ for each $v$. If $x_v > 1$, let $\varepsilon = x_v - 1 > 0$. The points $x \pm \varepsilon e_v$ are in $P$: they are nonnegative, each edge at $v$ has $x_u + x_v - \varepsilon \ge 0 + 1$, and the other constraints do not change. Then $x$ is the midpoint of two different points of $P$, which is false for an extreme point. So $x \in [0, 1]^V$. An extreme point of $P_1$ is in $[0, 1]^V$ by definition, so the rest of the proof covers both polytopes.

Let $V^+ = \{v : 1/2 < x_v < 1\}$ and $V^- = \{v : 0 < x_v < 1/2\}$, and assume, for a contradiction, that $V^+ \cup V^-$ is not empty. Let $\varepsilon > 0$ be smaller than each of these finitely many positive numbers: $|x_v - 1/2|$, $x_v$ and $1 - x_v$ for $v \in V^+ \cup V^-$, and $(x_u + x_v - 1)/2$ for each edge $uv$ with $x_u + x_v > 1$. Let $d$ be the vector with $d_v = 1$ on $V^+$, $d_v = -1$ on $V^-$, and $d_v = 0$ elsewhere, and let $y = x + \varepsilon d$ and $z = x - \varepsilon d$. Then $d \ne 0$, $y \ne z$, and $x = (y + z)/2$.

We show $y \in P_1$; the proof for $z$ is the same with the signs swapped. Entries outside $V^+ \cup V^-$ do not change. An entry in $V^+ \cup V^-$ moves by $\varepsilon$, so it stays in $(0, 1)$. Take an edge $uv$. If $x_u + x_v > 1$, then $y_u + y_v \ge x_u + x_v - 2\varepsilon > 1$. If $x_u + x_v = 1$, there are three cases, because $x_u, x_v \in [0, 1]$:

- $x_u = x_v = 1/2$: no entry changes.
- One value is 0 and the other is 1: no entry changes.
- Otherwise $x_u \in (0, 1/2)$ forces $x_v = 1 - x_u \in (1/2, 1)$, and $x_u \in (1/2, 1)$ forces $x_v \in (0, 1/2)$. So one end is in $V^-$ and the other is in $V^+$, and $y_u + y_v = x_u + x_v + \varepsilon - \varepsilon = 1$.

So $y, z \in P_1 \subseteq P$, and $x$ is the midpoint of two different points of $P_1$. This contradicts that $x$ is an extreme point of $P$ or of $P_1$. Hence $V^+ \cup V^- = \emptyset$, and $x$ is half-integral.

**Proof of Theorem 2.** Let $S$ be a minimum weight vertex cover, and let $S' = (S \setminus V_0) \cup V_1$.

*$S'$ is a cover.* Take an edge $uv$. If $u \in V_0$, then $x^*_v \ge 1$, so $x^*_v = 1$ and $v \in V_1 \subseteq S'$. The case $v \in V_0$ is the same. If neither end is in $V_0$, then an end in $S$, which exists because $S$ is a cover, is in $S \setminus V_0 \subseteq S'$.

*$w(S') \le w(S)$.* We have $w(S') = w(S) - w(S \cap V_0) + w(V_1 \setminus S)$, so it suffices to show $w(V_1 \setminus S) \le w(S \cap V_0)$. Let $x'$ be $x^*$ with the entries on $V_1 \setminus S$ lowered from 1 to $1/2$ and the entries on $V_0 \cap S$ raised from 0 to $1/2$. Then $x' \ge 0$. Take an edge $uv$. If no end is in $V_1 \setminus S$, then no entry of the edge goes down, and $x'_u + x'_v \ge x^*_u + x^*_v \ge 1$. Otherwise, say $u \in V_1 \setminus S$, so $x'_u = 1/2$. As $u \notin S$, $v \in S$, so $v \notin V_1 \setminus S$ and $x'_v \ge x^*_v$. If $x^*_v \ge 1/2$, then $x'_u + x'_v \ge 1$. If $x^*_v = 0$, then $v \in V_0 \cap S$ and $x'_v = 1/2$, so $x'_u + x'_v = 1$. So $x'$ is feasible, and since $x^*$ is optimal,

$$w \cdot x^* \le w \cdot x' = w \cdot x^* - \tfrac12 w(V_1 \setminus S) + \tfrac12 w(V_0 \cap S).$$

This gives $w(V_1 \setminus S) \le w(V_0 \cap S)$. So $S'$ is a cover with $w(S') \le w(S)$, so it is a minimum weight cover, and by its definition $V_1 \subseteq S' \subseteq V \setminus V_0 = V_1 \cup V_{1/2}$.

**Proof of Theorem 3.** Let $\text{LP}^*$ be the LP optimum of $G$ and $\tau_w(H)$ the minimum weight of a cover of $H$.

*$\text{LP}^* \le \tau_w(H)/2$.* Let $C$ be a cover of $H$ and $x_v = |C \cap \{v^L, v^R\}|/2$. For an edge $uv$ of $G$, the edges $u^L v^R$ and $v^L u^R$ of $H$ are covered by different vertices of $C$, since they have no common end. Both vertices are copies of $u$ or $v$, so $x_u + x_v \ge 2/2 = 1$. And $w \cdot x = w(C)/2$. With a minimum $C$, this $x$ is feasible, half-integral, and has value $\tau_w(H)/2$.

*$\tau_w(H) \le 2 \, \text{LP}^*$.* Let $x$ be an optimal LP solution of $G$, and put $y_{v^L} = y_{v^R} = x_v$. Each edge $u^L v^R$ of $H$ has $y_{u^L} + y_{v^R} = x_u + x_v \ge 1$, so $y$ is feasible for the LP of $H$, of value $2 w \cdot x$. The constraint matrix of a bipartite graph is totally unimodular ([total unimodularity](/total-unimodularity/)), so the LP of $H$ has an integral optimum, which is a cover of $H$. Hence $\tau_w(H) \le 2 w \cdot x = 2 \, \text{LP}^*$.

The two bounds give $\text{LP}^* = \tau_w(H)/2$, and the vector $x$ of the first part is a half-integral optimum. $\blacksquare$

## Consequences

- **The 2-approximation.** Round a half-integral optimum up: take $V_1 \cup V_{1/2}$. This is a cover of weight at most $2 \, w \cdot x^*$, which is the algorithm of [LP rounding for vertex cover](/lp-rounding-vertex-cover/). Theorem 2 adds that the vertices of $V_1$ are never a mistake and those of $V_0$ are never needed, so all the loss is in $V_{1/2}$.
- **No general LP solver.** By Theorem 3, a half-integral optimum comes from a minimum weight vertex cover of the bipartite graph $H$, which is a minimum $s$-$t$ cut by [Kőnig's theorem](/konig-theorem/) and the [max-flow min-cut theorem](/max-flow-min-cut-theorem/). One max flow on a graph with $2n$ vertices and $2m$ edges solves the LP exactly.
- **A kernel with at most $2k$ vertices.** In [parameterized vertex cover](/parameterized-vertex-cover/), the question is whether $G$ has a cover of size at most $k$. Compute a half-integral optimum $x^*$ with unit weights. If $\text{LP}^* > k$, the answer is no. Otherwise, $G$ has a cover of size at most $k$ if and only if $G[V_{1/2}]$ has a cover of size at most $k - |V_1|$. One direction: add $V_1$ to such a cover; edges at $V_0$ have their other end in $V_1$, since $x^*_u + x^*_v \ge 1$. The other direction is Theorem 2. The new graph has $|V_{1/2}| = 2 \sum_{v \in V_{1/2}} x^*_v \le 2 \, \text{LP}^* \le 2k$ vertices. This is the [Nemhauser-Trotter theorem](/nemhauser-trotter-theorem/) as a [kernelization](/kernelization/) (Chen, Kanj and Jia 2001); see [LP-based kernelization](/lp-kernelization/) and the [crown reduction](/crown-reduction/).
- **Exact search.** By Theorem 2, an exact branching algorithm for vertex cover can fix $V_1$ and $V_0$ first and branch only on the vertices of $V_{1/2}$.

## Tightness

- **The value 1/2 is needed.** For the triangle, $(1/2, 1/2, 1/2)$ is an extreme point: its three edge constraints are tight, and the matrix with rows $(1,1,0)$, $(0,1,1)$, $(1,0,1)$ has determinant 2, so it is the only point where all three are tight. For an odd cycle $C_{2k+1}$ with unit weights, the all-$1/2$ point is the unique LP optimum, so no integral optimum of the LP exists. So the set $\{0, 1/2, 1\}$ in Theorem 1 cannot be made smaller.
- **Bipartite graphs.** For bipartite $G$ the constraint matrix is totally unimodular, so each extreme point is integral and $V_{1/2}$ can be taken empty.
- **The kernel bound.** For $K_{2k}$ with unit weights, the all-$1/2$ point is optimal, with value $k$, and $V_{1/2}$ is all $2k$ vertices, so the bound $2k$ of the kernel is reached. A minimum cover has $2k - 1$ vertices, so the answer for parameter $k$ is no in this case, but the LP rule does not see it.
- **Other covering LPs.** Half-integrality is special to constraints with two variables. For vertex cover in 3-uniform hypergraphs, the LP with all 3-element subsets of $\{1, 2, 3, 4\}$ as edges has the unique optimum $(1/3, 1/3, 1/3, 1/3)$; see [frequency rounding](/frequency-rounding-set-cover/).
- **The rounding.** Persistency does not fix the vertices of $V_{1/2}$. Rounding all of them up can cost twice the optimum, and by the [integrality gap](/integrality-gap/) $2 - 2/n$ of $K_n$, no rounding of this LP gives a ratio below $2 - 2/n$ against $\text{LP}^*$.

## History

Nemhauser and Trotter studied the fractional vertex packing polytope $\{x \ge 0 : x_u + x_v \le 1 \text{ for each } uv \in E\}$, the LP relaxation of maximum weight independent set, in two papers. The map $x \mapsto \mathbf{1} - x$ takes it onto $P_1$. The 1974 paper in Mathematical Programming gave the half-integrality of its extreme points, and the 1975 paper gave the persistency theorem and its use in exact algorithms. Balinski (1965) had shown related half-integrality results for matching polytopes. Hochbaum (1982) used the half-integral solution for the 2-approximation, and Chen, Kanj and Jia (2001) observed that the theorem gives a kernel with at most $2k$ vertices for vertex cover.

## References
