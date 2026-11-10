---
tag: AWBKWN
kind: algorithm
slug: goemans-williamson-steiner-forest
name: Goemans-Williamson primal-dual Steiner forest
aliases:
- primal-dual Steiner forest 2-approximation
- Agrawal-Klein-Ravi algorithm
- moat growing
area: approximation/lp-rounding
level: advanced
summary: Grow dual moats around all active components at the same rate, add each edge that goes tight, then reverse delete; the forest costs at most 2 - 2/k times the dual, with k terminals.
solves: [steiner-forest]
model: real-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, p: the number of terminal pairs}
  time: {worst: O(n(m + n p))}
  space: {extra: O(n + m + p)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1995
  people: [Michel X. Goemans, David P. Williamson, Ajit Agrawal, Philip Klein, R. Ravi]
  note: Agrawal, Klein and Ravi found the 2 - 2/k algorithm for Steiner forest (STOC 1991, SIAM Journal on Computing 1995); Goemans and Williamson gave the primal-dual proof and extended it to all proper constrained forest problems (SODA 1992, SIAM Journal on Computing 1995).
prereqs: [steiner-forest, primal-dual-schema, dual-linear-program, weak-duality, spanning-forest]
see_also: [primal-dual-approximation, steiner-tree-problem, prize-collecting-steiner-tree, jain-iterative-rounding-network-design, generalized-steiner-network, kou-markowsky-berman, reverse-delete, dijkstra]
sources:
  - paper: doi:10.1137/S0097539793242618
    title: Michel X. Goemans and David P. Williamson, A general approximation technique for constrained forest problems, SIAM Journal on Computing 24(2), 1995
    locator: pages 296 to 317 (the algorithm, the proof of 2 - 2/k, and proper functions)
  - paper: doi:10.1137/S0097539792236237
    title: Ajit Agrawal, Philip Klein and R. Ravi, When trees collide, an approximation algorithm for the generalized Steiner problem on networks, SIAM Journal on Computing 24(3), 1995
    locator: pages 440 to 456
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 7.4 (the generalized Steiner tree problem) and Section 7.3 (shortest s-t path by the same method)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 22 (Steiner forest), with the tight example
  - book: isbn:9780534949686
    title: Dorit S. Hochbaum (editor), Approximation Algorithms for NP-Hard Problems
    locator: Chapter 4, by Michel X. Goemans and David P. Williamson
---

The Goemans-Williamson algorithm is a [primal-dual](/primal-dual-schema/) 2-approximation for [Steiner forest](/steiner-forest/): given a graph with edge costs and pairs of terminals, find a cheap forest that connects each pair. It grows a dual variable, a *moat*, around each component that still has an unconnected terminal, all at the same rate, and adds each edge that becomes tight. At the end it deletes the edges that are not needed, in the reverse order of addition. The forest costs at most $2 - 2/k$ times the dual value, where $k$ is the number of terminals, so at most $(2 - 2/k) \cdot$ OPT.

## In plain words

Put a small circle of paint around each place that still needs a link to its partner, and let all these circles grow at the same speed. A road is paid for when the circles at its two ends have covered all of it. Build each road as soon as it is paid for, and treat the places it joins as one group. A group stops growing when every place in it is with its partner.

When all partners are linked, look at the roads in the reverse order of building, and remove each road that is not needed. The total paint is at most the cost of the best answer. Each growing circle touches fewer than two of the final roads on average, so the roads cost less than twice the paint.

## The problem

The input is a graph $G = (V, E)$ with $n$ vertices, $m$ edges and costs $c_e \ge 0$, and $p$ pairs $(s_i, t_i)$ of terminals. The terminals are the $k$ vertices that are in some pair. The output is a set $F \subseteq E$ such that each $s_i$ and $t_i$ are connected in $(V, F)$, of small cost $c(F) = \sum_{e \in F} c_e$. A vertex set $S$ *separates* a pair if it holds exactly one of $s_i, t_i$. With $\delta(S)$ the set of edges with one end in $S$, the LP relaxation and its dual are

$$\min \sum_{e} c_e x_e \ \text{ s.t. } \sum_{e \in \delta(S)} x_e \ge 1 \text{ for each separating } S,\ x \ge 0; \qquad \max \sum_{S} y_S \ \text{ s.t. } \sum_{S : e \in \delta(S)} y_S \le c_e \text{ for each } e,\ y \ge 0.$$

The sum $\sum_{S : e \in \delta(S)} y_S$ is the *load* of $e$, and $e$ is *tight* when its load is $c_e$. A component of $(V, F)$ is *active* if it separates some pair. OPT is the least cost of a feasible forest, and the ratio convention is ALG $\le \rho \cdot$ OPT.

## The algorithm

```pseudo id=main
GW-STEINER-FOREST(G, c, pairs)
L1  F ← empty list;  y ← 0;  each vertex is its own component
L2  while some component is active do
L3      for each edge e between two components, compute the time until e goes tight if each active component C raises y_C at rate 1
L4      ε ← the least such time;  e ← an edge that attains it
L5      y_C ← y_C + ε for each active component C
L6      append e to F;  merge the two components at the ends of e
L7  for each edge e of F, from the last added to the first do
L8      if F − e still connects every pair then F ← F − e
L9  return F, y
```

The load of an edge $uv$ between two components is $d_u + d_v$, where $d_v$ is the sum of $y_S$ over the raised sets $S$ that hold $v$: a raised set is a past component, so it lies inside one current component and cannot hold both ends. In line L3 the load grows at rate 2 if both ends are in active components, at rate 1 if one end is, and not at all otherwise. So the time for $uv$ is $(c_{uv} - d_u - d_v)$ divided by that rate. Line L4 may give $\varepsilon = 0$, when an edge is already tight; line L6 then still merges. Each pass of the loop merges two components, so there are at most $n - 1$ passes. Line L8 tests a pair by a [disjoint set](/disjoint-set/) scan of $F - e$.

## Example

The graph has the vertices $a, b, c, d, e, f$ and the pairs $(a, d)$ and $(c, f)$, so $k = 4$.

| edge | $ab$ | $af$ | $bd$ | $cd$ | $ce$ | $cf$ | $de$ | $df$ |
|---|---|---|---|---|---|---|---|---|
| cost | 5 | 4 | 2 | 5 | 3 | 3 | 2 | 5 |

The table follows the loop. The time is the total growth so far; ties go to the edge listed first above.

| pass | active components | $\varepsilon$ | time | edge added | merged component |
|---|---|---|---|---|---|
| 1 | $\{a\}, \{c\}, \{d\}, \{f\}$ | 3/2 | 3/2 | $cf$ | $\{c, f\}$, now inactive |
| 2 | $\{a\}, \{d\}$ | 1/2 | 2 | $bd$ | $\{b, d\}$ |
| 3 | $\{a\}, \{b, d\}$ | 0 | 2 | $de$ | $\{b, d, e\}$ |
| 4 | $\{a\}, \{b, d, e\}$ | 1/2 | 5/2 | $af$ | $\{a, c, f\}$ |
| 5 | $\{a, c, f\}, \{b, d, e\}$ | 1/2 | 3 | $cd$ | all six |

In pass 1, $cf$ has both ends active, so it is tight at time $3/2$, before $af$ at time 2. In pass 3, the vertex $d$ already carries load 2, which is the cost of $de$, so $\varepsilon = 0$. The dual is $y_{\{a\}} = 5/2$, $y_{\{c\}} = y_{\{f\}} = 3/2$, $y_{\{d\}} = 2$, $y_{\{b, d, e\}} = 1$ and $y_{\{a, c, f\}} = 1/2$, of total 9.

Reverse delete tries $cd$ (needed for $(a, d)$), $af$ (needed), $de$ (not needed, removed), $bd$ (not needed, since $a, f, c, d$ is a path; removed) and $cf$ (needed). The output is $\{cf, af, cd\}$ of cost 12. The bound is $(2 - 2/4) \cdot 9 = 13.5$. The LP optimum is $19/2$, and OPT $= 10$ with $\{ab, bd, cf\}$, so the ratio on this input is $1.2$. The phase bound of the proof is tight in passes 1 and 5: the final edges meet the four moats of pass 1 in $1 + 2 + 1 + 2 = 6 = 2 \cdot 4 - 2$ places, and the two moats of pass 5 in $1 + 1 = 2$ places.

## Correctness

The loop keeps three invariants: $y$ is feasible for the dual, each edge of $F$ is tight, and the components are the components of $(V, F)$. Feasibility holds because line L4 stops at the first edge that goes tight, and an edge inside a component gets no more load. When the loop ends, no component is active, so each pair is in one component of $F$. Line L8 keeps this property. If an active component has no edge to another component, its pair is not connected in $G$, and the implementation reports this.

**Theorem (Goemans and Williamson 1995; Agrawal, Klein and Ravi 1995).** GW-STEINER-FOREST returns a feasible forest $F'$ and a feasible dual $y$ with $c(F') \le (2 - 2/k) \sum_S y_S \le (2 - 2/k) \cdot \text{OPT}$.

The proof writes the cost through the tight edges as $c(F') = \sum_S y_S |F' \cap \delta(S)|$, and splits $y$ into the passes: pass $j$ adds $\varepsilon_j$ to each of its $a_j$ active components. The key lemma bounds each pass: the active components of pass $j$ meet $F'$ in at most $2a_j - 2$ edges in total. To prove it, contract each component of pass $j$ to a node. The edges of $F'$ between components form a forest on these nodes, and no inactive node is a leaf. An inactive node with one edge $e$ would make $e$ redundant: a path in $F'$ between a pair crosses the boundary of an inactive set an even number of times, so it cannot use $e$ alone, and then line L8 would have removed $e$. So the sum of the degrees of the active nodes is at most $2a_j - 2$, and

$$c(F') = \sum_j \varepsilon_j \sum_{C \text{ active in pass } j} |F' \cap \delta(C)| \le \sum_j \varepsilon_j (2a_j - 2) \le \Big(2 - \frac{2}{k}\Big) \sum_j \varepsilon_j a_j = \Big(2 - \frac{2}{k}\Big) \sum_S y_S.$$

The last inequality uses $a_j \le k$: each active component holds a terminal. The full proof is in the proof file below.

**The lower bound used.** The dual value $\sum_S y_S$, which is at most the LP optimum by [weak duality](/weak-duality/), and so at most OPT.

**Tight example.** Put $k$ terminals on a cycle with edges of cost $2 - \varepsilon$, add a hub joined to each terminal at cost 1, and ask that all terminals be connected. OPT $= k$ (the star). In pass 1 all terminals grow, the cycle edges go tight at time $1 - \varepsilon/2$, before the hub edges, and $k - 1$ of them make one component. The output costs $(k - 1)(2 - \varepsilon)$, which tends to $(2 - 2/k) \cdot$ OPT, and it equals $(2 - 2/k)$ times the dual $k(1 - \varepsilon/2)$. The cut LP has integrality gap at least $2 - 2/k$ by the same graph, so no analysis against this LP gives less.

## Complexity

- **Time.** Each of the at most $n - 1$ passes scans all $m$ edges in line L3, tests each component for activity against the $p$ pairs, and updates $d_v$ for the vertices of the active components, which is $O(m + np)$. Reverse delete makes at most $n - 1$ tests, each a disjoint set scan of $O(n + m + p)$ time. The total is $O(n(m + np))$ in the worst case, counting each arithmetic operation as one step. Goemans and Williamson implement the growth with a priority queue in $O(n^2 \log n)$ time.
- **Space.** The edges, the pairs, the labels and $d_v$ take $O(n + m + p)$ extra space. Storing the dual $y$ adds one entry for each pass.

## Properties

- **A certificate.** The dual $y$ comes with the forest, so $c(F') / \sum_S y_S$ bounds the error of each run.
- **Deterministic.** Ties in line L4 change the output but not the bound.
- **Minimal output.** After line L8, each edge of $F'$ lies on the path of some pair.
- **Laminar dual.** The sets with $y_S > 0$ are past components, so any two are disjoint or nested.

## Variants and improvements

- **Proper functions.** The same algorithm works for each problem whose cut requirement is a 0-1 *proper function*: symmetric, and with $f(A \cup B) \le \max(f(A), f(B))$ for disjoint $A$ and $B$. This covers Steiner tree, T-joins and point-to-point connection, all with ratio 2 (Goemans and Williamson 1995).
- **Steiner tree.** With all terminals in one tree, the algorithm is a 2-approximation for the [Steiner tree problem](/steiner-tree-problem/), like the [MST heuristic](/kou-markowsky-berman/). Better ratios for Steiner tree come from other methods; see [Steiner tree inapproximability](/steiner-tree-inapproximability/).
- **Prize-collecting.** With penalties for unconnected terminals, the moats also pay for the penalties; this gives [prize-collecting Steiner tree](/prize-collecting-steiner-tree/) with ratio $2 - 1/(n - 1)$.
- **Higher connectivity.** For requirements above 1, see [Jain's iterative rounding](/jain-iterative-rounding-network-design/) for the [generalized Steiner network](/generalized-steiner-network/) problem.
- **Shortest path.** With one pair and one moat, the algorithm is [Dijkstra's algorithm](/dijkstra/) and the bound is exact.

## When to use it

Use the algorithm for Steiner forest and other connectivity problems with 0-1 requirements, when a combinatorial method with a proven ratio is wanted. It needs no LP solver, and its dual value gives a lower bound with each answer. For large graphs, use a priority queue on the edge times instead of the full scan of line L3. For Steiner tree alone, local search or LP-based methods give better ratios, and the dual bound of this algorithm is still a useful check.

## Pitfalls

- **Skipping reverse delete.** Without lines L7 and L8 the ratio is not bounded. Take one pair $s, t$ joined by an edge of cost $2 + \delta$, and $N$ other vertices, each joined to $s$ at cost 1. At time 1 all $N$ edges at $s$ go tight and are added, so the forest costs $N + 2 + \delta$, while OPT $= 2 + \delta$.
- **The order of deletion.** The proof on this page needs only that each edge of the output is needed for some pair, so for Steiner forest each order of deletion keeps the bound. The general analysis of Goemans and Williamson for proper functions is written for the reverse order, and most texts use it.
- **Growing inactive components.** An inactive component that grows would put load on edges that the optimum does not need to cross, and the dual would not be a valid bound for the forest.
- **Floating-point times.** Ties in line L4 are common, and rounding errors can make an edge look slightly overloaded. Use exact rationals or integer costs scaled by 2.

## Implementations

## History

Agrawal, Klein and Ravi gave the first 2-approximation for the generalized Steiner tree problem, which is Steiner forest, at STOC 1991, with the ratio $2 - 2/k$; the journal version is from 1995. Goemans and Williamson (SODA 1992, SIAM Journal on Computing 1995) recast the algorithm as a primal-dual method with uniform growth of all minimal violated sets, and extended it to all constrained forest problems with proper functions. Their analysis, with the reverse delete step, became the model for many later primal-dual algorithms, including [facility location](/jain-vazirani-facility-location/) and [prize-collecting](/prize-collecting-steiner-tree/) problems. The survey of Goemans and Williamson in Hochbaum's book (1997) and the books of Vazirani (2001) and Williamson and Shmoys (2011) present it as a standard example.

## References
