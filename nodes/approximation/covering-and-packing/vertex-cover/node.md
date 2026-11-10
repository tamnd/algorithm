---
tag: 34AFV7
kind: problem
slug: vertex-cover
name: Vertex cover problem
aliases:
- k-vertex cover
- minimum vertex cover
- node cover
area: approximation/covering-and-packing
level: core
summary: Find a smallest set of vertices that touches every edge; NP-hard, 2-approximable by a maximal matching, and 2 − ε is hard under the Unique Games Conjecture.
prereqs: [np-complete, lp-relaxation]
see_also: [vertex-cover-2-approximation, weighted-vertex-cover, konig-theorem, vertex-cover-inapproximability, parameterized-vertex-cover, nemhauser-trotter-theorem, independent-set, set-cover]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 34, Section 34.5 (the vertex cover problem is NP-complete), and Chapter 35, Sections 35.1 and 35.4
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability
    locator: Section 3.1 (vertex cover among the six basic NP-complete problems) and Appendix A1.1, problem GT1
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 1 (cardinality vertex cover) and Chapter 14 (half-integrality and LP rounding)
  - title: George L. Nemhauser and Leslie E. Trotter, Vertex packings, structural properties and algorithms, Mathematical Programming 8, 1975
    locator: pages 232 to 248 (half-integrality and persistence of the LP)
  - paper: doi:10.4007/annals.2005.162.439
    title: Irit Dinur and Samuel Safra, On the hardness of approximating minimum vertex cover, Annals of Mathematics 162(1), 2005
    locator: pages 439 to 485
  - paper: doi:10.1016/j.jcss.2007.06.019
    title: Subhash Khot and Oded Regev, Vertex cover might be hard to approximate to within 2 − ε, Journal of Computer and System Sciences 74(3), 2008
    locator: pages 335 to 349
---

The vertex cover problem asks for a smallest set of vertices of a graph that touches every edge. It is one of [Karp's 21 NP-complete problems](/karps-21-np-complete-problems/), and the standard first example in approximation algorithms: the endpoints of a [maximal matching](/maximal-matching/) give a [2-approximation](/vertex-cover-2-approximation/) in linear time, and no algorithm is known with ratio $2 - \varepsilon$ for a constant $\varepsilon > 0$. The complement of a vertex cover is an [independent set](/independent-set/), so the two problems have the same exact complexity but very different approximability. On [bipartite graphs](/bipartite-graph/) the problem is solved exactly by matching, by [König's theorem](/konig-theorem/). It is also the standard example of a fixed-parameter tractable problem.

## In plain words

A network has points and links. You must choose points so that each link touches at least one chosen point, like guards at the corners of a set of streets who must see every street. You want as few chosen points as possible.

Finding the true smallest choice is hard for large networks. But one fact helps: if some links share no point, each of them needs its own chosen point. So a set of links with no shared points gives a lower limit, and taking both ends of such links gives a choice at most twice that limit.

## Definition

**Input.** An undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges.

**Output.** A set $C \subseteq V$ such that each edge $\{u, v\} \in E$ has $u \in C$ or $v \in C$, a *vertex cover*.

**Goal.** Minimize $|C|$. OPT $= \tau(G)$ is the least size of a vertex cover, and the ratio convention is ALG $\le \rho \cdot$ OPT.

**Decision version.** Given $G$ and $k$, does $G$ have a vertex cover of at most $k$ vertices? This is the *$k$-vertex cover* problem, and it is NP-complete.

**Integer program and LP.** With $x_v = 1$ when $v \in C$:

$$\min \sum_{v \in V} x_v \quad \text{subject to} \quad x_u + x_v \ge 1 \text{ for each } \{u, v\} \in E, \quad x_v \in \{0, 1\}.$$

The [LP relaxation](/lp-relaxation/) replaces $x_v \in \{0, 1\}$ by $x_v \ge 0$, with optimum LP* $\le$ OPT. Its dual is the fractional matching LP: maximize $\sum_e y_e$ with $\sum_{e \ni v} y_e \le 1$ and $y \ge 0$. So each matching $M$ gives $|M| \le \text{LP}^* \le \text{OPT}$.

**Half-integrality.** The LP has an optimal solution with each $x_v \in \{0, 1/2, 1\}$ (Nemhauser and Trotter 1975). Moreover, some optimal cover contains each vertex with $x_v = 1$ and no vertex with $x_v = 0$; see the [Nemhauser-Trotter theorem](/nemhauser-trotter-theorem/) and [half-integrality](/half-integrality/).

**Relations.** $C$ is a vertex cover if and only if $V \setminus C$ is an independent set, so $\tau(G) + \alpha(G) = n$ (Gallai). $C$ is a vertex cover of $G$ if and only if $V \setminus C$ is a clique of the [complement graph](/complement-graph/).

## Variants

- **Weighted vertex cover.** Each vertex has a weight, and the goal is a cover of least weight. See [weighted vertex cover](/weighted-vertex-cover/); the ratio 2 still holds.
- **Bipartite graphs.** $\tau(G) = \nu(G)$, the size of a maximum matching, by [König's theorem](/konig-theorem/), so the problem is in P. The weighted case reduces to a minimum cut.
- **Parameterized $k$-vertex cover.** For a parameter $k$, a cover of size at most $k$ can be found in $O(1.2738^k + kn)$ time (Chen, Kanj and Xia 2010). See [parameterized vertex cover](/parameterized-vertex-cover/), [vertex cover branching](/vertex-cover-branching/) and the [crown reduction](/crown-reduction/), which gives a kernel of at most $3k$ vertices; the LP gives one of $2k$.
- **Hypergraph vertex cover.** Each edge has up to $r$ vertices. This is [hitting set](/hitting-set/) with sets of size $r$, and the ratio becomes $r$.
- **Partial vertex cover.** Cover at least $t$ edges with few vertices. The dual budget version, maximum vertex coverage, is a case of [maximum coverage](/max-coverage/).
- **Connected vertex cover.** The cover must induce a connected subgraph. The internal vertices of a DFS tree give ratio 2.
- **Online and distributed.** A maximal matching is easy to keep online and to find in few rounds; see [distributed minimum vertex cover](/distributed-minimum-vertex-cover/).

## Examples

**A small graph.** The graph has the vertices 1 to 7 and the edges 1-2, 1-3, 2-3, 2-4, 3-5, 4-5, 4-6, 5-7 and 6-7. A cover must take two vertices of the triangle 1, 2, 3, and two vertices of the path 4-6-7-5, which uses the edges 4-6, 6-7 and 7-5 and avoids the triangle. So OPT $\ge 4$, and $\{1, 2, 5, 6\}$ is a cover, so OPT $= 4$. The LP gives $x_v = 1/2$ for all $v$, a value of $7/2$, and LP* $= 7/2$. The maximal matching $\{1\text{-}2, 3\text{-}5, 4\text{-}6\}$ gives the lower bound 3 and the cover $\{1, \ldots, 6\}$ of size 6.

**Exact values for standard graphs.**

| graph | $n$ | $\tau$ | LP* | largest matching |
|---|---|---|---|---|
| star $K_{1,n-1}$ | $n$ | 1 | 1 | 1 |
| path with $n$ vertices | $n$ | $\lfloor n/2 \rfloor$ | $\lfloor n/2 \rfloor$ | $\lfloor n/2 \rfloor$ |
| cycle $C_n$ | $n$ | $\lceil n/2 \rceil$ | $n/2$ | $\lfloor n/2 \rfloor$ |
| complete graph $K_n$ | $n$ | $n - 1$ | $n/2$ | $\lfloor n/2 \rfloor$ |
| $K_{k,k}$ | $2k$ | $k$ | $k$ | $k$ |
| Petersen graph | 10 | 6 | 5 | 5 |

The complete graph shows the integrality gap: OPT/LP* $= 2(n - 1)/n$, which tends to 2. On bipartite graphs, all three columns agree.

## Known algorithms

| algorithm | ratio | lower bound used |
|---|---|---|
| [Maximal matching](/vertex-cover-2-approximation/) | 2 | the size of a matching |
| [Primal-dual](/primal-dual-weighted-vertex-cover/) (weighted) | 2 | a feasible dual solution |
| [LP rounding](/lp-rounding-vertex-cover/): take each $v$ with $x_v \ge 1/2$ | 2 | LP* |
| [Local ratio](/bar-yehuda-even-vertex-cover/) (weighted) | 2 | the local ratio theorem |
| SDP rounding (Karakostas 2009) | $2 - \Theta(1/\sqrt{\log n})$ | an SDP value |
| Bipartite: maximum matching and [König's theorem](/konig-theorem/) | 1 | the matching |
| [Branching](/vertex-cover-branching/) | exact, $O(1.2738^k + kn)$ | none |

All ratios hold in the worst case. The LP has one constraint per edge and is solved in polynomial time; because of half-integrality, it can also be solved by a bipartite matching or flow computation.

## Bounds

- **NP-completeness.** The decision version is NP-complete (Karp 1972), even on planar graphs of degree at most 3 (Garey and Johnson).
- **Upper bound (proved on the linked page).** Ratio 2 by the [maximal matching algorithm](/vertex-cover-2-approximation/).
- **NP-hardness of approximation (cited).** A $1.3606$-approximation is NP-hard (Dinur and Safra 2005), and a $(\sqrt{2} - \varepsilon)$-approximation is NP-hard for each $\varepsilon > 0$ (Khot, Minzer and Safra 2018).
- **Under the Unique Games Conjecture (cited).** A $(2 - \varepsilon)$-approximation is hard for each $\varepsilon > 0$ (Khot and Regev 2008). See [vertex cover inapproximability](/vertex-cover-inapproximability/).
- **Integrality gap.** The LP has gap $2 - 2/n$ on $K_n$, so LP-based analyses cannot prove a ratio below 2.
- **Exact time.** Unless the exponential time hypothesis fails, no algorithm runs in $2^{o(n)}$ time; the best parameterized bound is about $1.2738^k$.
- **Special classes.** [Planar graphs](/planar-graph/) have a PTAS by [Baker's technique](/baker-planar-ptas/); graphs of bounded treewidth are solved exactly by dynamic programming.

## Reductions

- **From independent set and clique.** $C$ is a vertex cover of $G$ if and only if $V \setminus C$ is an independent set of $G$, and a [clique](/clique-problem/) of the complement graph. This gives the NP-completeness from [clique](/clique-problem/), as in Karp (1972) and CLRS. The reduction keeps exact optima but not ratios: $\tau = n - \alpha$.
- **From 3-SAT.** The textbook reduction of Garey and Johnson builds a triangle for each clause and an edge for each variable from a [3-SAT](/3-sat/) formula.
- **To set cover.** The edges are the elements and each vertex is the set of its edges. Each element has [frequency](/element-frequency/) 2, so vertex cover is set cover with $f = 2$, and the $f$-approximations of [set cover](/set-cover/) give 2.
- **To hitting set.** The edges are sets of two vertices, so vertex cover is 2-[hitting set](/hitting-set/).

## Applications

- **Monitoring networks.** Place monitors on routers so that each link has a monitored endpoint.
- **Conflict resolution.** In a conflict graph, removing a vertex cover leaves a conflict-free set; this is the standard use in computational biology, where removing few sequences removes all conflicts in a sample.
- **Kernels for exact solvers.** Vertex cover is the testbed of [kernelization](/kernelization/) and fixed-parameter algorithms, and the same techniques solve real instances with small covers.
## References
