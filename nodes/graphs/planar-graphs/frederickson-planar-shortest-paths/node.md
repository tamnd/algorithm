---
tag: 0AZZWY
kind: algorithm
slug: frederickson-planar-shortest-paths
name: Frederickson's planar shortest-path algorithm
aliases:
- Frederickson's algorithm
area: graphs/planar-graphs
level: research
summary: Single-source shortest paths in planar directed graphs in O(n sqrt(log n)) time using r-divisions.
solves: [planar-shortest-paths]
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: O(n (log n)^(1/2))}
  space: {extra: O(n)}
properties: {deterministic: true, needs_embedding: true, recursive: false}
history:
  year: 1987
  people: [Greg N. Frederickson]
  note: Frederickson introduced r-divisions in 1987 and used them to beat Dijkstra's algorithm with a heap on planar graphs, the first single-source algorithm for planar graphs faster than O(n log n).
prereqs: [r-division, dijkstra, planar-separator-theorem, single-source-shortest-paths, binary-heap]
see_also: [planar-shortest-paths, lipton-tarjan-separator, planar-separator-finding, distance-oracle, monge-property, frederickson-topology-trees, fibonacci-heap, planar-graph]
sources:
  - paper: doi:10.1137/0216064
    title: Greg N. Frederickson, Fast algorithms for shortest paths in planar graphs, with applications, SIAM Journal on Computing 16(6), 1004 to 1022 (1987)
    locator: the suitable r-division and how to find it, the search over boundary vertices with a heap organized by regions, and the O(n (log n)^(1/2)) single-source bound
  - paper: doi:10.1137/0136016
    title: Richard J. Lipton and Robert Endre Tarjan, A separator theorem for planar graphs, SIAM Journal on Applied Mathematics 36(2), 177 to 189 (1979)
    locator: the separator theorem with O(n^(1/2)) vertices on which the divisions are built
  - paper: doi:10.1006/jcss.1997.1493
    title: Monika R. Henzinger, Philip Klein, Satish Rao and Sairam Subramanian, Faster shortest-path algorithms for planar graphs, Journal of Computer and System Sciences 55(1), 3 to 23 (1997)
    locator: the comparison with Frederickson's algorithm and the linear-time algorithm with a recursive division of many levels
  - paper: doi:10.1007/BF01386390
    title: Edsger W. Dijkstra, A note on two problems in connexion with graphs, Numerische Mathematik 1, 269 to 271 (1959)
    locator: the single-source algorithm that is run inside the pieces and on the boundary vertices
---

Frederickson's algorithm finds the distances from one source to all vertices of a [planar](/planar-graph/) directed graph with nonnegative arc lengths in $O(n \sqrt{\log n})$ time. [Dijkstra's algorithm](/dijkstra/) with a binary heap takes $O(n \log n)$ on such a graph, because it must keep all $n$ vertices in one heap. Frederickson cuts the graph into an [r-division](/r-division/): pieces of about $r = \log n$ vertices, each touching the rest of the graph at only $O(\sqrt{r})$ *boundary vertices*. Distances inside each piece are computed first. Then Dijkstra's algorithm runs only over the $O(n / \sqrt{\log n})$ boundary vertices, with one heap entry per piece instead of one per vertex. **How the embedding is given:** the algorithm needs a planar embedding as a [rotation system](/rotation-system/), for two steps that come before the search: making every degree at most 3, and finding the separators of the division. The search itself uses only the arcs. The implementation on this page takes a plain list of arcs, with no embedding, and finds its divisions with a simple breadth-first rule; its answers are always correct, and the time bound holds when that rule gives small boundaries.

## In plain words

Think of a country cut into many small districts, each with a few border towns. First, inside every district, work out the shortest drive between each pair of its border towns. This is cheap because districts are small.

Now plan the trip from the start. A long route goes from border town to border town, and between two border towns it stays inside one district, so the table of that district already knows that part. So the search only looks at border towns, and there are few of them. It keeps one "next town to visit" per district instead of one per town, which makes the waiting list short. At the end, each district fills in its inner towns from the distances of its border towns.

## The problem

Input: a directed graph $G$ on the vertices $0, \ldots, n - 1$ whose underlying undirected graph is planar, a length $\ell(a) \ge 0$ for each arc $a$, and a source $s$. Output: $d(x) = \mathrm{dist}(s, x)$ for every vertex $x$, the least total length of a directed path from $s$ to $x$, or $\infty$ if there is none. This is the [single-source shortest path](/single-source-shortest-paths/) problem restricted to [planar graphs](/planar-shortest-paths/). A planar simple graph has $m \le 3n - 6$ edges, so $m = O(n)$.

**Divisions.** A *division* of a graph splits its arcs into *pieces*: every arc is in exactly one piece, and a piece contains the ends of its arcs. A vertex is a *boundary vertex* of a piece $P$, written $b \in B(P)$, if it is also in another piece, or if it is a *terminal* that we add on purpose (the source, for instance). An $r$-division of an $n$-vertex graph has $O(n / r)$ pieces, each with $O(r)$ vertices and $O(\sqrt{r})$ boundary vertices. By the [separator theorem](/planar-separator-theorem/), every planar graph of bounded degree has one. For a piece $P$, $T_P[b][b']$ is the distance from $b$ to $b'$ using only arcs of $P$.

## The algorithm

```pseudo id=main
FREDERICKSON-SSSP(G, ℓ, s)                   ▷ G planar, ℓ ≥ 0, s the source
L1  r1 ← ⌈log n⌉; r2 ← ⌈log r1⌉²
L2  D1 ← an r1-division of G; make s a terminal of the pieces that contain it
L3  for each piece P of D1 do
L4      D2 ← an r2-division of P; make the vertices of B(P) terminals of the small pieces that contain them
L5      for each small piece Q of D2 and each b ∈ B(Q) do
L6          run Dijkstra in Q from b; T_Q[b][b'] ← its distance to b', for each b' ∈ B(Q)
L7      for each b ∈ B(P) do
L8          δ ← BOUNDARY-SEARCH(D2, T, {b ↦ 0}); T_P[b][b'] ← δ(b'), for each b' ∈ B(P)
L9  d ← BOUNDARY-SEARCH(D1, T, {s ↦ 0})
L10 for each piece P of D1 do
L11     run Dijkstra in P with the start label d(b) at every b ∈ B(P); each other vertex x of P gets d(x)
L12 return d

BOUNDARY-SEARCH(D, T, start)                 ▷ Dijkstra on the boundary vertices of D
L13 d(b) ← start(b) for the start vertices, ∞ for the other boundary vertices; H ← an empty min-heap of pieces
L14 for each piece P that contains a start vertex do key(P) ← min of d over B(P); insert P into H
L15 while H is not empty do
L16     extract P with the least key; if a scan of B(P) gives a larger minimum, reinsert P with it and go to L15
L17     b ← a vertex of B(P) not settled with d(b) = key(P); settle b
L18     for each piece Q with b ∈ B(Q) do
L19         for each b' ∈ B(Q) not settled do d(b') ← min(d(b'), d(b) + T_Q[b][b'])
L20         key(Q) ← min of d over the vertices of B(Q) not settled, by a scan; insert Q into H with this key
L21 return d
```

**The heap of pieces.** BOUNDARY-SEARCH is Dijkstra's algorithm on the *dense distance graph*: its vertices are the boundary vertices, and each piece $Q$ contributes an arc $b \to b'$ of length $T_Q[b][b']$ for every pair in $B(Q)$. The heap does not hold vertices. It holds pieces, keyed by the least label of a vertex in the piece that is not settled yet, and the vertex itself is found by a scan of the piece's $O(\sqrt{r})$ boundary vertices. An entry can be out of date: too high is harmless, because the piece whose arc lowered a label is always updated in line L20, and too low is caught by the scan in line L16.

**Two levels.** Line L6 computes distances in pieces of size $r_2$ with plain Dijkstra. Line L8 combines them into distances in a piece of size $r_1$ by the same boundary search, which is faster than Dijkstra on the whole piece. Line L9 does the same once more for the whole graph. The terminals of lines L2 and L4 make sure that the vertices whose distances are needed at one level are boundary vertices of the level below.

**Before the search.** Frederickson's bounds need two more steps that do not change any distance. First, every vertex of degree more than 3 is replaced by a cycle of new vertices joined by arcs of length 0 in both directions, one new vertex per edge, in the order of the rotation system; the result is still planar, and now every vertex is in $O(1)$ pieces. Second, the r-division is found in $O(n \log r + (n / r) \log n)$ time: Frederickson groups the vertices into connected clusters of about $r$ vertices along a spanning tree, applies the separator recursion to the much smaller graph of clusters, and then splits the clusters. The plain recursion with the [Lipton-Tarjan separator](/lipton-tarjan-separator/) would take $O(n \log n)$, which is too slow here.

## Example

Take the $3 \times 3$ grid with vertices $3i + j$ for row $i$ and column $j$, each edge usable in both directions, with these lengths:

| edge | 0-1 | 1-2 | 3-4 | 4-5 | 6-7 | 7-8 | 0-3 | 3-6 | 1-4 | 4-7 | 2-5 | 5-8 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| length | 2 | 7 | 1 | 3 | 4 | 1 | 5 | 1 | 1 | 6 | 1 | 2 |

The source is $s = 0$, and $r_1 = 5$ with one level, as the implementation does when $r_2 \ge r_1$. The breadth-first order from 0 is $0, 1, 3, 2, 4, 6, 5, 7, 8$; cutting it in the middle gives the regions $\{0, 1, 3, 2\}$ and $\{4, 6, 5, 7, 8\}$. Each edge goes to one piece, the crossing edges $1 - 4$, $3 - 4$, $3 - 6$ and $2 - 5$ to the second region's piece. So piece $A$ has the vertices $1, \ldots, 8$ and $B(A) = \{1, 2, 3\}$, and piece $B$ has the edges $0 - 1$, $0 - 3$, $1 - 2$ and $B(B) = \{0, 1, 2, 3\}$, with 0 as a terminal.

Line L6 gives the tables. In $A$: $T_A[1][3] = 2$ (by $1 - 4 - 3$), $T_A[1][2] = 5$ (by $1 - 4 - 5 - 2$), $T_A[3][2] = 5$. In $B$: $T_B[0][1] = 2$, $T_B[0][3] = 5$, $T_B[0][2] = 9$, $T_B[1][3] = 7$, $T_B[1][2] = 7$.

| step | line | action | labels $d(0), d(1), d(2), d(3)$ | keys $A$, $B$ |
|---|---|---|---|---|
| 1 | L14 | start at 0 | $0, \infty, \infty, \infty$ | $-$, 0 |
| 2 | L17 | extract $B$, settle 0 | | |
| | L19 | relax in $B$: $d(1) = 2$, $d(2) = 9$, $d(3) = 5$ | $0, 2, 9, 5$ | $-$, 2 |
| 3 | L17 | extract $B$, settle 1 | | |
| | L19 | relax in $A$: $d(2) = \min(9, 2 + 5) = 7$, $d(3) = \min(5, 2 + 2) = 4$; in $B$ nothing improves | $0, 2, 7, 4$ | 4, 4 |
| 4 | L17 | extract $A$, settle 3; nothing improves | | 7, 7 |
| 5 | L16 | the old entry of $B$ with key 4 is out of date: skip | | |
| 6 | L17 | extract $A$, settle 2 | $0, 2, 7, 4$ | |

Line L11 then runs Dijkstra in $A$ from the labels $d(1) = 2$, $d(2) = 7$, $d(3) = 4$: $d(4) = 3$, $d(6) = 5$, $d(5) = 6$, $d(8) = 8$ and $d(7) = 9$. The answer is $(0, 2, 7, 4, 3, 6, 5, 9, 8)$, the same as plain Dijkstra on the whole grid. Note the step that matters: the best route to 3 is $0 - 1 - 4 - 3$ of length 4, which leaves piece $B$ and comes back; the search finds it through the table of $A$.

**Small cases.** A single vertex returns $(0)$. In $K_4$ with all lengths 2, every other vertex is at distance 2. A path of $10^5$ vertices with arcs forward only gives $d(x) = x$ from vertex 0, and from the last vertex every other distance is $\infty$. A tree is cut by the division like any other graph. $K_5$ and $K_{3,3}$ are not planar, but the algorithm still returns correct distances, because correctness never uses planarity; only the size of the boundaries, and so the time, does.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It rests on one fact about divisions: a vertex that is not a boundary vertex lies in one piece only, so all its arcs are in that piece. Hence every path splits at its boundary vertices into parts that each stay inside one piece, and the distance between two boundary vertices is their distance in the dense distance graph. BOUNDARY-SEARCH is Dijkstra on that graph; the only new point is that the vertex settled in line L17 has the least label among all vertices not settled, which follows from an invariant on the keys. Lines L6 and L8 compute the tables correctly by induction on the level, and line L11 is correct because a shortest path to a vertex inside $P$ enters $P$ for the last time at a boundary vertex of $P$.

## Complexity

Write $|B(Q)|$ for the boundary size of a piece. Two sums bound everything. The pieces of an $r$-division have $\sum_Q |B(Q)| = O(n / \sqrt{r})$ boundary vertices in all, and $\sum_Q |B(Q)|^2 = O(n / r) \cdot O(r) = O(n)$. The terminals added in lines L2 and L4 do not change these bounds by more than a constant factor.

- **One boundary search** over a division of a graph with $N$ vertices into pieces of size $r$: each settled vertex costs one heap operation, $O(\log N)$, and a scan; each relaxation round of lines L19 and L20 costs $O(|B(Q)|)$. Each boundary vertex is settled once, and it is in $O(1)$ pieces after the degree reduction. The total is $O(N + (N / \sqrt{r}) \log N)$.
- **Line L6.** $\sum_Q |B(Q)| \cdot O(r_2 \log r_2) = O(n \sqrt{r_2} \log r_2) = O(n \log r_1 \log \log r_1)$, which is $O(n \log \log n \log \log \log n)$.
- **Line L8.** A piece $P$ of size $r_1$ gets $O(\sqrt{r_1})$ searches, each $O(r_1 + (r_1 / \sqrt{r_2}) \log r_1) = O(r_1)$, since $\sqrt{r_2} = \log r_1$. Over the $O(n / r_1)$ pieces this is $O(n \sqrt{r_1}) = O(n \sqrt{\log n})$.
- **Line L9.** One search: $O(n + (n / \sqrt{r_1}) \log n) = O(n \sqrt{\log n})$.
- **Line L11.** Dijkstra in each piece: $O(r_1 \log r_1)$ each, $O(n \log \log n)$ in all.
- **Divisions and degree reduction.** $O(n \log \log n)$ with Frederickson's method for finding the division.

The total is $O(n \sqrt{\log n})$ time. The choice $r_1 = \log n$ balances line L8, which grows with $r_1$, against line L9, which shrinks with it. The tables have $\sum |B(Q)|^2 = O(n)$ entries, so the space is $O(n)$.

The implementation finds its divisions by cutting a breadth-first order in half again and again. This is correct for every graph, takes $O(n \log n)$ time, and gives boundaries of size $O(\sqrt{r})$ on grids but not on every planar graph. So the code shows the method and checks the answers; it does not prove the $O(n \sqrt{\log n})$ bound.

## Properties

- **Nonnegative lengths only.** Like Dijkstra's algorithm, the boundary search settles a vertex once. With negative lengths, other methods are needed (see Variants).
- **Directed.** Arcs may go one way. The divisions are made on the underlying undirected graph; the tables are not symmetric.
- **Correct on any graph.** Planarity is used only to bound the boundary sizes, so the method is a correct shortest-path algorithm on every graph, and fast on graphs with good divisions.
- **Deterministic and iterative.** No randomness and no recursion; long paths do not overflow the call stack.

## Variants and improvements

- **Linear time.** Henzinger, Klein, Rao and Subramanian (1997) use a division with many levels, from pieces of constant size up to the whole graph, and run a Dijkstra-like search that is allowed to settle vertices out of order and fix them later. This gives $O(n)$ time for nonnegative lengths. Klein, Mozes and Sommer (2013) showed how to build the divisions for all levels together in linear time.
- **All pairs.** In the same paper, Frederickson gave an all-pairs algorithm for planar graphs in $O(n^2)$ time, also built on r-divisions. With the tables built once, each further source costs only one boundary search and the final fill-in.
- **Negative lengths.** With negative lengths, Fakcharoenphol and Rao (2006) use dense distance graphs and the [Monge property](/monge-property/) of distances along a face to get near-linear time.
- **Distance oracles.** Keeping the tables of an r-division and answering each query with a small search gives planar [distance oracles](/distance-oracle/) with a trade-off between space and query time.
- **Other heaps.** With a [Fibonacci heap](/fibonacci-heap/), Dijkstra already takes $O(n \log n)$ on planar graphs; the gain here comes from the smaller number of vertices in the heap, not from a better heap.

## When to use it

The algorithm is mainly of theoretical interest: it was the first to beat $O(n \log n)$ for planar shortest paths, and its r-division became a basic tool. For a single query on a road network or a mesh, plain Dijkstra with a binary heap is simpler and fast in practice. The structure pays off when many searches run on the same graph, because the tables of lines L5 to L8 are built once: for many sources, for all pairs, or for an oracle that answers queries later.

## Pitfalls

- **Missing terminals.** If the source, or a vertex of $B(P)$ at the lower level, is not made a boundary vertex, its distance is never computed by the boundary search, and the parts of paths that start there are lost.
- **Stale heap keys.** A piece keyed by a vertex that has since been settled through another piece has a key that is too low. Without the rescan of line L16, the search settles a vertex that is not the global minimum.
- **Pieces sharing a vertex.** A boundary vertex can be in many pieces. Relaxing only in the piece from which it was extracted misses paths that continue in another piece; line L18 must visit all of them.
- **Degree.** Without the degree reduction, a vertex of high degree can be in $\Theta(n / r)$ pieces, and the cost of settling it grows with that number.
- **Divisions are not pieces of size r.** A region of at most $r$ vertices can get more vertices in its piece through the crossing edges assigned to it, as piece $A$ in the example. The bounds count vertices up to a constant factor, which is enough.

## Implementations

## History

Before 1987 the best single-source algorithm for planar graphs with nonnegative lengths was Dijkstra's algorithm with a heap, in $O(n \log n)$ time. Lipton and Tarjan (1979) had proved the [separator theorem](/planar-separator-theorem/) and used it for many divide and conquer algorithms on planar graphs. Frederickson's 1987 paper introduced the r-division, built from separators, and with it gave the $O(n \sqrt{\log n})$ single-source algorithm and an $O(n^2)$ all-pairs algorithm. Ten years later, Henzinger, Klein, Rao and Subramanian reached linear time with recursive divisions, and r-divisions have since become the standard tool for planar distance problems.

## References
