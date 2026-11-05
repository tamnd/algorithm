---
tag: HTAYEM
kind: algorithm
slug: batagelj-zaversnik-algorithm
name: Batagelj-Zaversnik algorithm
aliases:
- bucket-based core decomposition
area: graphs/network-analysis
level: core
summary: Computes all core numbers in O(m) time by peeling minimum-degree nodes.
solves: [k-core-decomposition]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m), best: Θ(n + m)}
  space: {extra: Θ(n)}
properties: {directed: false, weighted: false, deterministic: true, recursive: false}
prereqs: [k-core, degree, bucket-queue, counting-sort]
see_also: [k-core-decomposition, k-core, degeneracy, degeneracy-ordering, greedy-coloring, arboricity, maximum-clique, triangle-counting]
sources:
  - paper: "Vladimir Batagelj and Matjaž Zaveršnik, An O(m) algorithm for cores decomposition of networks, arXiv:cs/0310049 (2003)"
    locator: Section 3, the algorithm (the arrays vert, pos, deg and bin, and the swap that moves a neighbour to the lower bin), and its proof of correctness and of the O(m) bound
  - paper: doi:10.1007/s11634-010-0079-y
    title: Vladimir Batagelj and Matjaž Zaveršnik, Fast algorithms for determining (generalized) core groups in social networks, Advances in Data Analysis and Classification 5(2), 129 to 145 (2011)
    locator: the sections on the core algorithm and on generalized cores with monotone vertex functions
  - paper: doi:10.1016/0378-8733(83)90028-X
    title: Stephen B. Seidman, Network structure and minimum degree, Social Networks 5(3), 269 to 287 (1983)
    locator: the definition of the k-core and its nesting
  - paper: doi:10.1145/2402.322385
    title: David W. Matula and Leland L. Beck, Smallest-last ordering and clustering and graph coloring algorithms, Journal of the ACM 30(3), 417 to 427 (1983)
    locator: the smallest-last ordering in O(n + m) time with buckets of vertices by degree
---

The Batagelj-Zaversnik algorithm computes the core number of every [vertex](/vertex/) of an undirected graph in $O(n + m)$ time. The core number of $v$ is the largest $k$ such that $v$ lies in the [$k$-core](/k-core/), the largest subgraph in which every vertex has [degree](/degree/) at least $k$. The algorithm removes a vertex of least current degree again and again. It keeps the vertices in one array sorted by degree, with the start of each degree block stored, so that lowering the degree of a neighbour is one swap and one increment. It solves [$k$-core decomposition](/k-core-decomposition/), and the order in which it removes the vertices is a [degeneracy ordering](/degeneracy-ordering/).

## In plain words

Think of a party where each guest stays only while enough friends are still there. Who stays?

The algorithm answers this for every $k$ at once. It sends home the guest with the fewest friends still present. Each friend of that guest now has one friend fewer. Then it sends home the next guest with the fewest friends, and so on, until no one is left. The number of friends a guest had at the moment of leaving, never less than the number of an earlier guest, is the guest's core number.

The trick is speed. The guests stand in a line sorted by their number of friends, with a marker at the start of each group. When a guest loses a friend, they swap places with the first guest of their group and the marker moves one step. That is a fixed amount of work.

## The problem

The input is a simple undirected graph $G = (V, E)$ without weights, with $V = \{0, 1, \ldots, n-1\}$ and $m$ edges, given by adjacency lists: each edge $\{u, v\}$ is in $\mathrm{Adj}[u]$ and in $\mathrm{Adj}[v]$, and there are no self-loops and no repeated edges. The graph need not be connected.

For $k \ge 0$, the $k$-core of $G$ is the largest set $C_k \subseteq V$ such that each vertex of $C_k$ has at least $k$ neighbours in $C_k$. It is unique, because the union of two such sets is again such a set, and it may be empty. The cores are nested: $C_0 = V \supseteq C_1 \supseteq C_2 \supseteq \cdots$. The **core number** of $v$ is $\mathrm{core}(v) = \max\{k : v \in C_k\}$, which equals the largest minimum degree of an induced subgraph that contains $v$.

The output is the array $\mathrm{core}[0..n-1]$. Ties among vertices of equal degree are broken by the order in which they sit in the array, which starts as the order of the vertex numbers. This order changes the removal order but not the core numbers.

## The algorithm

```pseudo id=main
BZ(G)
L1  for each v ∈ V do deg[v] ← |Adj[v]|
L2  md ← the largest deg[v], or 0 if V is empty
L3  bin[0..md] ← 0; for each v ∈ V do bin[deg[v]] ← bin[deg[v]] + 1
L4  turn bin into prefix sums: bin[d] ← the number of vertices of degree less than d
L5  for each v ∈ V do pos[v] ← bin[deg[v]]; vert[pos[v]] ← v; bin[deg[v]] ← bin[deg[v]] + 1
L6  for d ← md downto 1 do bin[d] ← bin[d − 1]; bin[0] ← 0
L7  for i ← 0 to n − 1 do
L8      v ← vert[i]                               ▷ a vertex of least current degree
L9      for each u ∈ Adj[v] do
L10         if deg[u] > deg[v] then
L11             du ← deg[u]; pu ← pos[u]; pw ← bin[du]; w ← vert[pw]
L12             if u ≠ w then swap: pos[u] ← pw; vert[pu] ← w; pos[w] ← pu; vert[pw] ← u
L13             bin[du] ← bin[du] + 1; deg[u] ← du − 1
L14 return deg
```

Lines L3 to L6 are a [counting sort](/counting-sort/) of the vertices by degree. After them, $\mathrm{vert}$ lists the vertices in order of degree, $\mathrm{pos}$ is its inverse, and $\mathrm{bin}[d]$ is the index of the first vertex of degree at least $d$. This is a [bucket queue](/bucket-queue/) stored in one array.

The main loop removes $\mathrm{vert}[0], \mathrm{vert}[1], \ldots$ in turn. When $v$ is removed, each neighbour $u$ that has a larger current degree loses one. Line L12 swaps $u$ with the first vertex $w$ of its degree block, and line L13 moves the start of the block one step to the right, so $u$ is now the last vertex of the block below. The test of line L10 keeps the degree of a neighbour from falling below $\mathrm{deg}[v]$: such a neighbour already has the core number $\mathrm{deg}[v]$, and its entry must not move into the part of the array already passed. When $v$ is removed, $\mathrm{deg}[v]$ never changes again, and it is the core number of $v$.

## Example

The graph has the vertices 0 to 8 and the 11 edges of a [clique](/clique/) on $\{0, 1, 2, 3\}$ plus $\{3,4\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$ and $\{4,7\}$. Vertex 8 has no edge, so the graph is not connected. The degrees are $3, 3, 3, 4, 4, 2, 2, 1, 0$, and the counting sort gives

$$\mathrm{vert} = [8, 7, 5, 6, 0, 1, 2, 3, 4], \qquad \mathrm{bin} = [0, 1, 2, 4, 7].$$

The adjacency lists are in increasing order.

| $i$ | removed $v$ | $\mathrm{deg}[v]$ | changes at lines L11 to L13 | $\mathrm{vert}$ after the step |
|---|---|---|---|---|
| 0 | 8 | 0 | none | 8 7 5 6 0 1 2 3 4 |
| 1 | 7 | 1 | vertex 4 goes from 4 to 3, swapped with 3 | 8 7 5 6 0 1 2 4 3 |
| 2 | 5 | 2 | vertex 4 goes from 3 to 2, swapped with 0; vertex 6 has degree 2, not more | 8 7 5 6 4 1 2 0 3 |
| 3 | 6 | 2 | none: vertices 4 and 5 have degree 2, not more | same |
| 4 | 4 | 2 | vertex 3 goes from 4 to 3, no swap since it is first in its block | same |
| 5 to 8 | 1, 2, 0, 3 | 3 each | none | same |

The result is $\mathrm{core} = [3, 3, 3, 3, 2, 2, 2, 1, 0]$. The 3-core is the clique, the 2-core adds the triangle $\{4, 5, 6\}$, the 1-core adds vertex 7, and the isolated vertex 8 has core number 0. In step 2, the edge $\{5, 6\}$ is not counted against 6: once the removal reaches degree 2, the degrees of the others stay at 2 or more.

## Correctness

**Theorem.** BZ$(G)$ stops, and it returns $\mathrm{deg}[v] = \mathrm{core}(v)$ for every vertex $v$.

Let $v_1, \ldots, v_n$ be the vertices in the order of removal and $D_i$ the value of $\mathrm{deg}[v_i]$ when $v_i$ is removed. The array part is a sorted array with block starts, and a swap inside a block followed by a step of the block start keeps it sorted, so $v_i$ always has the least current degree among the vertices not yet removed. The arithmetic part is the invariant that, for each vertex $u$ not yet removed, $\mathrm{deg}[u]$ is the larger of $D_{i-1}$ and the number of neighbours of $u$ not yet removed. So $D_1 \le D_2 \le \cdots \le D_n$, the process is the classic peeling, and the vertices $v_j, \ldots, v_n$ from the first $j$ with $D_j = D_i$ form a set of minimum degree $D_i$ that contains $v_i$. No set of larger minimum degree contains $v_i$, since its first removed vertex would have had a larger degree. The full proof is below.

## Complexity

The cost is in the [word RAM](/word-ram/) model, with the graph as adjacency lists.

- **The counting sort.** Lines L1 to L6 take $O(n + \mathrm{md})$ time, and $\mathrm{md} \le n - 1$.
- **The main loop.** Line L8 runs $n$ times. Lines L9 to L13 run once for each pair of a vertex and a neighbour, so $2m$ times in total, and each run does $O(1)$ work, since the swap and the step of the block start are constant time.

The time is $\Theta(n + m)$ for every input, since each list is read. Batagelj and Zaveršnik state it as $O(m)$, which is the same when $m \ge n$, for example on a connected graph. The extra space is $\Theta(n)$ for $\mathrm{deg}$, $\mathrm{pos}$, $\mathrm{vert}$ and $\mathrm{bin}$, since $\mathrm{bin}$ has $\mathrm{md} + 1 \le n$ entries.

## Properties

- **Undirected and without weights.** Each edge counts once at each end. The algorithm needs a simple graph: a self-loop would lower the degree of $v$ while $v$ is removed, and repeated edges count with their multiplicity.
- **Deterministic.** The output is the same for every order of the adjacency lists and of the vertex numbers. Only the removal order depends on them.
- **Not recursive.** Two loops and four arrays; the depth of the graph does not matter.
- **A degeneracy ordering.** The final array $\mathrm{vert}$ is a smallest-first removal order. Each vertex has at most $\max_v \mathrm{core}(v)$ neighbours later in it, and this maximum is the [degeneracy](/degeneracy/) of the graph.
- **Disconnected graphs.** Each component is handled as if it were alone: the core number depends only on the component of the vertex. Isolated vertices get 0.

## Variants and improvements

- **Directed graphs.** With in-degrees or out-degrees in place of degrees, the same code gives the in-cores and out-cores.
- **Generalized cores.** In the 2011 paper, Batagelj and Zaveršnik replace the degree by any monotone vertex function, such as the sum of the weights of the edges to the remaining vertices. The buckets no longer work for real values, and a [priority queue](/priority-queue/) keyed by the current value takes their place, at a logarithmic cost per change.
- **Smallest-last ordering.** Matula and Beck gave the same peeling with buckets of vertices by degree in 1983, to order the vertices for [greedy colouring](/greedy-coloring/). The colouring then uses at most $\mathrm{degeneracy} + 1$ colours.
- **Linked buckets.** Many implementations keep a doubly linked list for each degree. The single array of this algorithm does the same with less memory and better locality.
- **Large graphs.** For graphs that do not fit in memory or that change over time, there are external, distributed and incremental versions, which recompute only the core numbers that an edge change can affect.

## When to use it

Use it whenever you need the core numbers of a graph that fits in memory: it is linear, simple, and has no constant beyond a few array accesses. The core numbers rank vertices by how deep they sit in the dense part of a network, and they are used to find a dense centre, to filter a graph before a costly step such as [maximum clique](/maximum-clique/) search (a clique of size $q$ lies in the $(q-1)$-core), to order vertices for [triangle counting](/triangle-counting/), and to bound the [arboricity](/arboricity/). If only one $k$-core is needed, the simpler queue-based peeling for that $k$ is enough.

## Pitfalls

- **Missing the test of line L10.** Without it, the degree of a neighbour can fall below $\mathrm{deg}[v]$, and the vertex would move into a block that the loop has already passed. The result is wrong core numbers and a corrupted array.
- **Wrong block starts.** After line L5, each $\mathrm{bin}[d]$ points to the end of its block. Line L6 must shift them back, from the top down, before the main loop.
- **Self-loops and repeated edges.** Remove them first, or the degrees are wrong.
- **Re-sorting.** Re-sorting after each removal, or using a [binary heap](/binary-heap/), gives $O(m \log n)$ time and loses the point of the algorithm.

## Implementations

## History

Seidman defined the $k$-cores of a social network in 1983, as a way to find dense groups by the minimum degree. In the same year, Matula and Beck gave the smallest-last ordering, which is the same peeling, in linear time with buckets of vertices. Batagelj and Zaveršnik published the array version with the swap in 2003 as a short report. In 2011 they extended it to generalized cores.

## References
