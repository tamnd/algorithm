---
tag: M17THE
kind: algorithm
slug: parallel-bfs
name: Parallel breadth-first search
aliases:
- level-synchronous BFS
- parallel frontier BFS
area: parallel/parallel-graph-algorithms
level: core
summary: Processes each BFS level's frontier in parallel, one synchronous round per level.
solves: [graph-reachability]
model: crcw-pram
complexity:
  vars: {n: the number of vertices, m: the number of edges, D: "the number of BFS levels, at most the eccentricity of the source plus one"}
  time: {worst: O(n + m)}
  depth: {worst: O(D log n)}
  space: {extra: O(n + m)}
properties: {deterministic: false, recursive: false}
prereqs: [breadth-first-search, frontier-based-processing, all-prefix-sums, parallel-pack, crcw-pram]
see_also: [direction-optimizing-bfs, multi-source-bfs, bfs-layers, work-span-model, ullman-yannakakis, delta-stepping, breadth-first-search-distributed, compressed-sparse-row]
sources:
  - url: https://sites.google.com/site/alphalambdabook/
    title: Umut A. Acar and Guy E. Blelloch, Algorithms, Parallel and Sequential, draft book for Carnegie Mellon course 15-210
    locator: part Graph Search, the chapter on breadth-first search (the parallel BFS with one frontier per round and its work and span); chapter numbers differ between drafts
  - paper: doi:10.1145/2442516.2442530
    title: Julian Shun and Guy E. Blelloch, Ligra, a lightweight graph processing framework for shared memory, PPoPP 2013
    locator: the BFS application (BFS by edgeMap with a compare-and-swap on the parent array); section number to be checked
  - paper: doi:10.1145/1810479.1810534
    title: Charles E. Leiserson and Tao B. Schardl, A work-efficient parallel breadth-first search algorithm (or how to cope with the nondeterminism of reducers), SPAA 2010
    locator: Sections 1 to 3 (layer-synchronous PBFS with the bag structure; work O(n + m)); exact span bound to be checked
  - paper: doi:10.5555/2388996.2389013
    title: Scott Beamer, Krste Asanović and David Patterson, Direction-optimizing breadth-first search, SC 2012
    locator: Section IV (bottom-up BFS) and Section V (the hybrid algorithm)
  - book: isbn:9780201548563
    title: Joseph JaJa, An Introduction to Parallel Algorithms, Addison-Wesley, 1992
    locator: Chapter 2, Section 2.1 (prefix sums) and Section 2.4 (the PRAM models and the concurrent write rules)
---

Parallel breadth-first search is the [breadth-first search](/breadth-first-search/) of a graph in which all vertices of one level are expanded at the same time. It runs in synchronous rounds: round $d$ takes the frontier (the vertices at distance $d - 1$ from the source), looks at all their edges in parallel, and builds the next frontier with a [prefix sum](/all-prefix-sums/) and a [pack](/parallel-pack/). On the [CRCW PRAM](/crcw-pram/) with the arbitrary write rule it does $O(n + m)$ work, the same as the sequential BFS, in $O(D \log n)$ time, where $D$ is the number of levels. It is the base case of [frontier-based processing](/frontier-based-processing/) and the starting point of [direction-optimizing BFS](/direction-optimizing-bfs/).

Notation on this page: $n$ is the number of vertices, $m$ the number of edges, $W$ the work, $S$ the span (the parallel time with unbounded processors), $T_p$ the time on $p$ processors, and $D$ the number of levels, that is, the largest finite distance from the source plus one. The model is the synchronous CRCW PRAM in which an arbitrary one of the concurrent writers to a cell succeeds.

## In plain words

Drop a stone into a pond. The first ring of waves reaches the points at distance one, then the next ring reaches the points at distance two. A ring does not care in which order its points get wet: they all get wet at the same time.

Parallel BFS works the same way. The current ring is the frontier. In one round, every vertex of the frontier looks at all its neighbours at the same time. Each neighbour that nobody has reached yet joins the next ring. Two frontier vertices can find the same new neighbour at the same moment. Only one of them may become its parent, so a write rule picks one winner, and the losers drop that neighbour. The number of rounds is the number of rings, not the number of vertices.

## The problem

The input is a graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$, directed or undirected, given as adjacency lists without parallel edges, and a source $s \in V$. The output is, for each vertex $v$, the distance $dist[v]$ (the least number of edges on a path from $s$ to $v$, or $\infty$), and a parent $parent[v]$ with $dist[parent[v]] = dist[v] - 1$ for each reachable $v \ne s$. The parents form a BFS tree. This solves [graph reachability](/graph-reachability/) and the unweighted [single-source shortest paths](/single-source-shortest-paths/) problem.

## The algorithm

The arrays $dist$, $parent$ and $C$ live in shared memory. Each `for all ... in parallel` loop is one synchronous step: all processors read, then all processors write. Line L8 is a concurrent write: many frontier vertices can write $parent[v]$ in the same step, and one arbitrary writer wins. Lines L9 to L11 read the winner back, so that exactly one writer puts $v$ into $C$.

```pseudo id=main
PARALLEL-BFS(G, s)
L1  for all v in parallel do dist[v] ← ∞, parent[v] ← nil
L2  dist[s] ← 0, parent[s] ← s, F ← [s], d ← 0
L3  while F is not empty do
L4      d ← d + 1
L5      off ← EXCLUSIVE-SCAN([deg(u) for u in F])     ▷ slot off[j] + i is for the i-th edge of F[j]
L6      for all u in F in parallel do
L7          for all neighbours v of u in parallel do
L8              if parent[v] = nil then parent[v] ← u  ▷ concurrent write, an arbitrary writer wins
L9      for all j, u = F[j] in parallel do
L10         for all i, v = adj[u][i] in parallel do
L11             C[off[j] + i] ← v if parent[v] = u and dist[v] = ∞ else nil
L12     F ← PACK(C, the entries that are not nil)
L13     for all v in F in parallel do dist[v] ← d
L14 return dist, parent
```

Line L5 gives each edge out of the frontier its own slot in an array $C$ of length $k = \sum_{u \in F} \deg(u)$. Lines L6 to L8 let every such edge try to claim its head. A vertex that already has a parent is not touched. Lines L9 to L11 let each edge check if it won: it wrote the winning value and the head was not reached in an earlier round. The test $dist[v] = \infty$ matters only for a self-loop at $s$, where $parent[s] = s$ holds from line L2. Line L12 packs the winners into the new frontier, and line L13 gives them their level.

The pair of lines L8 and L11 is the CRCW form of a compare-and-swap: `CAS(parent[v], nil, u)` returns true for exactly one of the concurrent callers. On a multicore machine the code uses the CAS directly, as Ligra does.

## Example

The graph has 7 vertices and the 8 undirected edges $\{0,1\}$, $\{0,2\}$, $\{1,3\}$, $\{2,3\}$, $\{2,4\}$, $\{3,5\}$, $\{4,5\}$, $\{5,6\}$, with source 0. The degrees are 2, 2, 3, 3, 2, 3, 1.

| round $d$ | frontier $F$ | $k$ (edges looked at) | concurrent claims | next frontier |
|---|---|---|---|---|
| 1 | [0] | 2 | none | [1, 2] |
| 2 | [1, 2] | 5 | 3 is claimed by 1 and by 2 | [3, 4] |
| 3 | [3, 4] | 5 | 5 is claimed by 3 and by 4 | [5] |
| 4 | [5] | 3 | none | [6] |
| 5 | [6] | 1 | none | [] |

The result is $dist = [0, 1, 1, 2, 2, 3, 4]$. The parent of 3 is 1 or 2, and the parent of 5 is 3 or 4, as the write rule decides. Both trees are BFS trees. The rounds look at $2 + 5 + 5 + 3 + 1 = 16$ edge slots, which is $2m$: each undirected edge is looked at once from each end. There are $D = 5$ rounds.

## Correctness

The invariant of the loop of line L3 is: at the start of the round with counter value $d$ (before line L4), $F$ holds each vertex at distance $d$ exactly once, $dist[v]$ is correct for each $v$ with distance at most $d$, $dist[v] = \infty$ and $parent[v] = nil$ for each other $v$, and each $v \ne s$ with a finite $dist$ has a parent one level up. A vertex at distance $d + 1$ has a neighbour in $F$, so line L8 gives it a parent from $F$. Exactly one edge slot passes the test of line L11 for it, so it enters the next frontier once. No vertex at a smaller distance is claimed, because it already has a parent. The full proof, with the case of the concurrent writes, is in the proof file.

## Complexity

The model is the CRCW PRAM, arbitrary write. A round with frontier $F$ and $k = \sum_{u \in F} \deg(u)$ edge slots costs:

- line L5: a scan over $|F|$ items, $O(|F|)$ work and $O(\log n)$ time;
- lines L6 to L11: two steps with one processor for each slot, $O(k)$ work and $O(1)$ time;
- line L12: a pack of $k$ slots, which is a scan and a scatter, $O(k)$ work and $O(\log k) = O(\log n)$ time, because $k \le m \le n^2$;
- line L13: $O(|F|)$ work and $O(1)$ time.

Each vertex is in at most one frontier, so $\sum |F| \le n$, and each vertex's edge list is looked at in one round only, so $\sum k$ is $m$ for a directed graph and $2m$ for an undirected one. With line L1 this gives

$$W = O(n + m), \qquad S = O(D \log n).$$

The work matches the $O(n + m)$ of the sequential BFS, so the algorithm is [work-efficient](/work-efficiency/). By [Brent's theorem](/brent-theorem/), $T_p = O((n + m)/p + D \log n)$. The parallelism is $W/S = \Theta((n + m)/(D \log n))$, so the method is fast on graphs with a small diameter (social graphs, web graphs, random graphs) and no faster than the sequential BFS on a path, where $D = n$.

The factor $\log n$ in each round comes from the scan and the pack. On the CRCW PRAM a round can be cheaper: the pack can be replaced by a dense array of $n$ flags, with one processor for each vertex and each edge. Then each round takes $O(1)$ time, but each round touches all vertices and edges, so the work rises to $O((n + m)D)$ in total. This is the dense frontier of [frontier-based processing](/frontier-based-processing/).

## Properties

- **Nondeterministic tree, deterministic distances.** The distances do not depend on the write rule. The BFS tree does: with an arbitrary write, two runs can give two different trees.
- **Work-efficient.** It does the same work as the sequential BFS, up to a constant factor.
- **Span bound by the levels.** No version of this method takes fewer rounds than $D$, because each round reaches only one more level.
- **No locks.** One concurrent write per vertex and per round replaces the visited flag and its lock.

## Variants and improvements

- **Compare-and-swap.** On shared memory machines, line L8 is `CAS(parent[v], nil, u)`, and the CAS result decides line L11 in the same step. This is the version in Ligra.
- **Direction optimization.** When the frontier is large, let each unvisited vertex look for a parent in the frontier instead. See [direction-optimizing BFS](/direction-optimizing-bfs/).
- **Bags instead of packs.** Leiserson and Schardl (2010) store the frontier in a "bag" (a set of pennants) that a fork-join program can split and merge, and get work $O(n + m)$ without a global scan.
- **Many sources.** Start with all sources in $F$: this gives [multi-source BFS](/multi-source-bfs/). Ullman and Yannakakis run many depth-bounded BFS at the same time to get [transitive closure](/ullman-yannakakis/) with fewer rounds.
- **Weighted graphs.** With weights, a frontier is a range of distances, not one level. See [Δ-stepping](/delta-stepping/).

## When to use it

Use parallel BFS on a graph with a small diameter, where $D \log n$ is much less than $n + m$. On a road network or a mesh, $D$ is about $\sqrt{n}$ or more, the frontiers are small, and the rounds do too little work to pay for their synchronization; then a sequential BFS or a multi-source variant is better. If you need only reachability and not the levels, [connected components](/connected-components/) algorithms such as [Shiloach-Vishkin](/shiloach-vishkin/) take $O(\log n)$ rounds on any graph.

## Pitfalls

- **Test, then set.** If line L8 is replaced by "if $parent[v] = nil$ then add $v$ to $C$" with no winner, two frontier vertices that read $nil$ at the same time both add $v$. The next frontier then holds $v$ twice, and the work can grow far past $O(m)$. Each vertex must have exactly one winner, as lines L8 and L11 make sure.
- **Reading the new frontier inside the round.** All reads of line L8 must see the state from before the round. A code that marks $v$ as visited and lets other vertices of the same round expand $v$ computes wrong distances, because $v$ then acts as a level $d$ vertex in the round of level $d$.
- **Reading the winner in the same step as the write.** Lines L8 and L11 must be two steps. If an edge reads $parent[v]$ in the step that writes it, the PRAM gives it the old value $nil$, and no edge sees itself as the winner.
- **A pack per vertex.** Packing the neighbours of each frontier vertex in its own small pack costs $O(\log n)$ for each vertex, in sequence if the code is written as a loop. Use one scan over the whole frontier, as line L5 does.

## Implementations

## History

Leiserson and Schardl (2010) gave a work-efficient fork-join version with reducers. Shun and Blelloch (2013) made the frontier and the CAS on the parent array the base of the Ligra framework. Beamer, Asanović and Patterson (2012) added the bottom-up step, which changes the work on low-diameter graphs.

## References
