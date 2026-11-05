---
tag: M4E15F
kind: problem
slug: planar-separator-finding
name: Finding planar separators
aliases:
- balanced separator in planar graphs
area: graphs/planar-graphs
level: core
summary: Compute a balanced separator of a planar graph.
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: O(n)}
  space: {extra: O(n)}
prereqs: [planar-separator-theorem, breadth-first-search, planar-embedding]
see_also: [lipton-tarjan-separator, r-division, nested-dissection, planar-shortest-paths, treewidth, fundamental-cycle, divide-and-conquer-paradigm, planar-dual-graph]
sources:
  - paper: doi:10.1137/0136016
    title: Richard J. Lipton and Robert Endre Tarjan, A separator theorem for planar graphs, SIAM Journal on Applied Mathematics 36(2), 177 to 189 (1979)
    locator: the linear-time algorithm that follows the proof of the main theorem
  - paper: doi:10.1137/0209046
    title: Richard J. Lipton and Robert Endre Tarjan, Applications of a planar separator theorem, SIAM Journal on Computing 9(3), 615 to 627 (1980)
    locator: the divide-and-conquer applications, including the separator for weighted vertices and the approximation scheme for independent sets
  - paper: doi:10.1016/0022-0000(86)90030-9
    title: Gary L. Miller, Finding small simple cycle separators for 2-connected planar graphs, Journal of Computer and System Sciences 32(3), 265 to 279 (1986)
    locator: the linear-time algorithm for simple cycle separators
  - paper: doi:10.1006/jcss.1995.1076
    title: Michael T. Goodrich, Planar separators and parallel polygon triangulation, Journal of Computer and System Sciences 51(3), 374 to 389 (1995)
    locator: the linear-time construction of a complete recursive separator decomposition
  - paper: doi:10.1137/0216064
    title: Greg N. Frederickson, Fast algorithms for shortest paths in planar graphs, with applications, SIAM Journal on Computing 16(6), 1004 to 1022 (1987)
    locator: the r-division and its construction in O(n log n) time
---

Finding a planar separator means computing, for a given [planar graph](/planar-graph/) with $n$ vertices, a small vertex set $S$ whose removal leaves two sides $A$ and $B$ with no edge between them and with at most $2n/3$ vertices each. The [planar separator theorem](/planar-separator-theorem/) says that $|S| \le 2\sqrt{2}\sqrt{n}$ is always possible, and the [Lipton-Tarjan separator](/lipton-tarjan-separator/) algorithm finds such a set in $O(n)$ time. Finding a smallest balanced separator is a different and harder problem; the algorithms here aim for the $O(\sqrt{n})$ guarantee, not for the optimum.

## In plain words

You want to cut a large flat network into two halves by removing a few nodes, so that no link connects the two halves and neither half is much bigger than the other. For flat networks, a few nodes always suffice: about the square root of the number of nodes.

To find them, grow rings of nodes around a starting node, one ring at a time. Pick one or two rings that are thin and cut the network into an inner part, a band and an outer part. If the band is still too big, cut it with one short loop. Each step looks at each node only a fixed number of times, so the whole job is fast.

## Definition

**Input.** A planar graph $G = (V, E)$ with $n$ vertices, given by adjacency lists, and optionally nonnegative vertex weights $w$ with sum 1. Some algorithms also need a planar embedding, given as a [rotation system](/rotation-system/). If it is not given, it is computed in $O(n)$ time (see [planar embedding](/planar-embedding/)).

**Output.** A partition of $V$ into $A$, $B$ and $S$ such that

1. no edge joins $A$ and $B$,
2. $|A| \le 2n/3$ and $|B| \le 2n/3$ (or $w(A), w(B) \le 2/3$ in the weighted form), and
3. $|S| \le c\sqrt{n}$ for a fixed constant $c$; the Lipton-Tarjan bound is $c = 2\sqrt{2}$.

The output is checked in $O(n)$ time: count the sides and scan every edge.

## Variants

- **Balance.** The factor $2/3$ can be replaced by $1/2$ or any constant above $1/2$, at the cost of a larger constant $c$, by separating the larger side again.
- **Weighted vertices.** The sides must have weight at most $2/3$ each. The Lipton-Tarjan algorithm handles weights with the same bound on $|S|$.
- **Simple cycle separators.** $S$ must be the vertex set of a simple cycle, so that the two sides are its inside and its outside. Miller (1986) showed that a 2-connected plane graph whose faces have at most $d$ vertices has one with $O(\sqrt{dn})$ vertices, found in $O(n)$ time. Cycle separators keep the pieces in a form that recursion can use, with the cycle as a face.
- **Edge separators.** Remove edges instead of vertices. This needs bounded degree: in the star $K_{1,n-1}$ every balanced edge separator has at least $n/3$ edges, because the side without the center has at least $n/3$ vertices, all leaves, and each leaf is attached to the center by its own edge.
- **Recursive decompositions.** Separate the pieces again until they are small. The result is a separator tree, or an [r-division](/r-division/) into $O(n/r)$ pieces with $O(\sqrt{r})$ boundary vertices each.
- **Minimum separators.** Find a balanced separator of least size. The guarantee $O(\sqrt{n})$ says nothing about the optimum, which can be much smaller, as the examples show.

## Examples

The table gives the least size of a separator with sides of at most $2n/3$ vertices, found by trying all vertex sets, and the bound $2\sqrt{2}\sqrt{n}$.

| graph | $n$ | least $\lvert S \rvert$ | one least separator | sides | $2\sqrt{2}\sqrt{n}$ |
|---|---|---|---|---|---|
| a single vertex | 1 | 1 | the vertex | both empty | 2.8 |
| the path $P_7$ | 7 | 1 | the third vertex | 2 and 4 | 7.5 |
| the star $K_{1,5}$ | 6 | 1 | the center | 5 single vertices, grouped 3 and 2 | 6.9 |
| the cycle $C_6$ | 6 | 2 | two adjacent vertices | 4 and 0 | 6.9 |
| $K_4$ | 4 | 2 | any two vertices | 2 and 0 | 5.7 |
| the $3 \times 3$ grid | 9 | 2 | the two neighbours of a corner | 1 and 6 | 8.5 |
| the $4 \times 4$ grid | 16 | 3 | a diagonal of 3 vertices next to a corner | 10 and 3 | 11.3 |
| the $5 \times 5$ grid | 25 | 4 | a staircase of 4 vertices next to a corner | 16 and 5 | 14.1 |

$K_5$ and $K_{3,3}$ are not planar, but small: both have least separators of size 2. The table shows that a side may be empty, and that the least separator often cuts off a corner rather than splitting the graph through its middle.

**A Lipton-Tarjan run on the $3 \times 3$ grid.** Start the breadth-first search at the center. The levels are $L_0 = \{\text{center}\}$, $L_1$ the four middle-side vertices, and $L_2$ the four corners. The median level is $\ell_1 = 1$, since $L_0$ has 1 vertex and $L_0 \cup L_1$ has $5 \ge 9/2$ vertices. The algorithm first checks whether this level alone is small enough: $|L_1| = 4 \le 2\sqrt{2}\sqrt{9} \approx 8.5$. So $S = L_1$, with the sides $A = \{\text{center}\}$ and $B$ the four corners, which are 1 and 4 vertices. The cycle step is not needed here. The result is within the bound, but it is not the least size 2.

## Known algorithms

| algorithm | time | output |
|---|---|---|
| try all vertex sets in order of size | $O(2^n \cdot n)$ | a least balanced separator, for tests on tiny graphs |
| [Lipton-Tarjan](/lipton-tarjan-separator/): BFS levels, then a fundamental cycle of a triangulation | $O(n)$ | $\lvert S \rvert \le 2\sqrt{2}\sqrt{n}$, balance $2/3$ |
| one BFS level near the median | $O(n)$ | balance $1/2$, but no bound on $\lvert S \rvert$ in terms of $\sqrt{n}$ |
| Miller's cycle separator | $O(n)$ | a simple cycle of $O(\sqrt{dn})$ vertices |
| repeated separation of the larger side | $O(n)$ in total | balance $1/2$, $\lvert S \rvert = O(\sqrt{n})$ |
| Frederickson's r-division | $O(n \log n)$ | $O(n/r)$ pieces of $O(r)$ vertices and $O(\sqrt{r})$ boundary vertices |
| Goodrich's recursive decomposition | $O(n)$ | a complete separator tree |

A single BFS level is the simplest heuristic, but its size has no $O(\sqrt{n})$ bound. In the fan, a path of $n - 1$ vertices plus a hub joined to all of them, a search from the hub puts $n - 1$ vertices into level 1. Lipton and Tarjan combine two levels with a cycle to get the guarantee for every start vertex.

## Bounds

- **Size.** Some separator with $|S| \le 2\sqrt{2}\sqrt{n}$ always exists ([planar separator theorem](/planar-separator-theorem/)). For the $k \times k$ grid, every balanced separator has at least $k/3 = \sqrt{n}/3$ vertices, so the order $\sqrt{n}$ is tight.
- **Time.** $\Theta(n)$: the Lipton-Tarjan algorithm is linear, and every algorithm must read the input, since a single unread edge can join $A$ and $B$.
- **Without planarity.** For general graphs no sublinear guarantee exists: $K_n$ needs $|S| \ge n/3$.

## Reductions

- **Separator from levels and a cycle.** The problem reduces to [breadth-first search](/breadth-first-search/), triangulation of a plane graph to a [maximal planar graph](/maximal-planar-graph/), and a search for a balanced [fundamental cycle](/fundamental-cycle/) in the tree of non-tree edges of the [planar dual](/planar-dual-graph/). All four steps take $O(n)$ time.
- **Supergraphs.** A separator of a planar supergraph on the same vertices is a separator of $G$, so algorithms may add edges freely, for example to make $G$ connected or triangulated.
- **Disconnected graphs.** If a component has more than $2n/3$ vertices, separate that component and put the others with the smaller side; otherwise group the components directly, without any separator vertex.
- **Balance $1/2$ from balance $2/3$.** Separate the larger side again, $O(\log n)$ times; the separator sizes form a geometric series.

## Applications

- **Divide and conquer.** Many problems on planar graphs split into independent subproblems on $A \cup S$ and $B \cup S$, with work on $S$ only ([divide and conquer](/divide-and-conquer-paradigm/); Lipton and Tarjan, 1980).
- **Sparse linear algebra.** [Nested dissection](/nested-dissection/) orders the unknowns by recursive separators, which bounds the fill of [Gaussian elimination](/gaussian-elimination/) on planar systems.
- **Shortest paths.** [r-divisions](/r-division/) give the fast [planar shortest path](/planar-shortest-paths/) algorithms and [distance oracles](/distance-oracle/).
- **Tree decompositions.** Recursive separators give a [tree decomposition](/tree-decomposition/) of width $O(\sqrt{n})$, and with it $2^{O(\sqrt{n})}$-time exact algorithms for NP-hard problems.
- **Approximation schemes.** Cutting into pieces of size $O(\log n)$ and solving each exactly gives approximation schemes for maximum independent set.
- **Parallel and external memory.** Separators split a planar graph into parts with little communication between them, for parallel computation and for graph layouts in memory.

## References
