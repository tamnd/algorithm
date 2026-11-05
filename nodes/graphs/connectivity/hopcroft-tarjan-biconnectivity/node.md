---
tag: B1ZMBY
kind: algorithm
slug: hopcroft-tarjan-biconnectivity
name: Hopcroft-Tarjan biconnectivity algorithm
aliases:
- Tarjan's biconnected components algorithm
- DFS low-point biconnectivity
area: graphs/connectivity
level: core
summary: One DFS computes low-points and yields articulation points, bridges and blocks in linear time.
solves: [articulation-point-finding, bridge-finding, biconnected-components]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m), best: Θ(n + m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: true}
history:
  year: 1973
  people: [John Hopcroft, Robert Tarjan]
  note: Hopcroft and Tarjan published the algorithm as Algorithm 447 in Communications of the ACM in 1973; Tarjan's 1972 paper on depth-first search gives the same method.
prereqs: [depth-first-search, low-link, biconnected-components]
see_also: [articulation-point, bridge, block-cut-tree, gabow-path-based-scc, tarjan-scc, edge-classification, two-edge-connected-components, biconnected-graph]
sources:
  - paper: doi:10.1145/362248.362272
    title: John Hopcroft and Robert Tarjan, Algorithm 447, Efficient algorithms for graph manipulation, Communications of the ACM 16(6), 372 to 378 (1973)
    locator: the biconnected components algorithm and its analysis
  - paper: doi:10.1137/0201010
    title: Robert E. Tarjan, Depth-first search and linear graph algorithms, SIAM Journal on Computing 1(2), 146 to 160 (1972)
    locator: Section 4, biconnectivity (low points, the test for articulation points, and the stack of edges)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 20, Problem 20-2, Articulation points, bridges, and biconnected components (Problem 22-2 in the third edition)
  - book: isbn:9780521736534
    title: Shimon Even, Graph Algorithms, second edition, edited by Guy Even, Cambridge University Press (2012)
    locator: Chapter 3, Depth-first search (the section on nonseparable components)
---

The Hopcroft-Tarjan algorithm finds the [articulation points](/articulation-point/), the [bridges](/bridge/) and the [biconnected components](/biconnected-components/) of an [undirected graph](/undirected-graph/) with one [depth-first search](/depth-first-search/), in $\Theta(n + m)$ time. For each vertex $v$ it computes a [low-link](/low-link/) value: the earliest discovery time that the subtree of $v$ reaches by one back edge. A vertex $u$ separates the subtree of its child $v$ from the rest exactly when $\mathrm{low}[v] \ge d[u]$, and the tree edge to $v$ is a bridge exactly when $\mathrm{low}[v] > d[u]$. A stack of edges gives the blocks as they close. The method is from 1972 and 1973, and it is a standard example of what depth-first search can do.

## In plain words

Walk through a network of towns and roads deep first, and number the towns in the order you first reach them. Each road you take into a new town is a tree road. Each other road leads back to a town you reached earlier, a short cut up.

For each town, find the smallest number that its part of the walk can reach by one short cut. If the part below a town can never climb above that town, the town is the only way in and out of that part: it is a weak point. If the part cannot even reach the town itself, the road into it is a weak link.

Keep the roads in a pile as you walk. When you find a weak point, the roads on top of the pile form one tightly knit piece. Take them off.

## The problem

**Input.** An undirected graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$ and edges $E = \{e_0, \ldots, e_{m-1}\}$, where $e_i = \{u_i, v_i\}$. Parallel edges and [self-loops](/self-loop/) are allowed, and each edge has its identifier $i$. The graph need not be connected.

**Output.** The set of [articulation points](/articulation-point-finding/), the set of [bridges](/bridge-finding/), and the blocks: the classes of the relation "equal, or on a common cycle" on $E$. Each loop is a block of one edge. See [biconnected components](/biconnected-components/).

## The algorithm

$d[u]$ is the discovery time of $u$, and $\mathrm{low}[u]$ is the least of $d[u]$ and the values $d[w]$ for back edges from the subtree of $u$ to $w$. $S$ is a stack of edges. The parameter $p$ of VISIT is the identifier of the tree edge into $u$, so that the search skips that one edge and not its parallel copies.

```pseudo id=main
BICONNECTIVITY(G)
L1  d[v] ← 0 for each v ∈ V, t ← 0, S ← an empty stack of edges
L2  output each loop as a block with one edge
L3  for each r ∈ V with d[r] = 0 do VISIT(r, nil)
L4      if r has at least two children then mark r as an articulation point

VISIT(u, p)                                ▷ p is the tree edge into u, or nil
L5  t ← t + 1, d[u] ← t, low[u] ← t
L6  for each edge e = {u, v} at u with e ≠ p and v ≠ u do
L7      if d[v] = 0 then                   ▷ e is a tree edge
L8          push e onto S, VISIT(v, e)
L9          low[u] ← min(low[u], low[v])
L10         if low[v] ≥ d[u] then          ▷ u cuts off the subtree of v
L11             pop S down to e, and output the popped edges as a block
L12             if p ≠ nil then mark u as an articulation point
L13             if low[v] > d[u] then mark e as a bridge
L14     else if d[v] < d[u] then           ▷ e is a back edge to an ancestor
L15         push e onto S, low[u] ← min(low[u], d[v])
```

Line L14 skips the entry of a back edge seen from its upper end, since the edge was already pushed from its lower end. The test of line L13 is only reached when line L10 holds, and a bridge is always a block of its own: the block popped by line L11 is then the single edge $e$.

## Example

The graph has $n = 7$ vertices and 10 edges: $e_0 = \{0, 1\}$, $e_1 = \{0, 1\}$, $e_2 = \{1, 2\}$, $e_3 = \{2, 0\}$, $e_4 = \{2, 3\}$, $e_5 = \{3, 4\}$, $e_6 = \{4, 5\}$, $e_7 = \{5, 3\}$, $e_8 = \{5, 6\}$, and the loop $e_9$ at 6. The lists are in the order of the identifiers. Line L2 outputs $\{e_9\}$. The search from 0 goes down the path $0, 1, 2, 3, 4, 5, 6$, so $d[v] = v + 1$.

| step | event | $S$ after (bottom to top) |
|---|---|---|
| 1 | tree $e_0$ to 1; at 1, $e_0$ is skipped by identifier, $e_1$ is a back edge to 0: $\mathrm{low}[1] = 1$ | $e_0, e_1$ |
| 2 | tree $e_2$ to 2; back edge $e_3$ to 0: $\mathrm{low}[2] = 1$ | $\ldots, e_2, e_3$ |
| 3 | tree $e_4$ to 3, tree $e_5$ to 4, tree $e_6$ to 5 | $\ldots, e_4, e_5, e_6$ |
| 4 | at 5, back edge $e_7$ to 3: $\mathrm{low}[5] = 4$; tree $e_8$ to 6; at 6 the loop is skipped | $\ldots, e_7, e_8$ |
| 5 | 6 returns: $\mathrm{low}[6] = 7 \ge d[5] = 6$, pop $\{e_8\}$; 5 is an articulation point; $7 > 6$, so $e_8$ is a bridge | $e_0, \ldots, e_7$ |
| 6 | 5 returns: $\mathrm{low}[4] = 4$, and $4 < d[4] = 5$ | same |
| 7 | 4 returns: $\mathrm{low}[4] = 4 \ge d[3] = 4$, pop $\{e_5, e_6, e_7\}$; 3 is an articulation point | $e_0, \ldots, e_4$ |
| 8 | 3 returns: $\mathrm{low}[3] = 4 \ge d[2] = 3$, pop $\{e_4\}$; 2 is an articulation point; $e_4$ is a bridge | $e_0, \ldots, e_3$ |
| 9 | 2 returns: $\mathrm{low}[2] = 1 < d[1] = 2$ | same |
| 10 | 1 returns: $\mathrm{low}[1] = 1 \ge d[0] = 1$, pop $\{e_0, e_1, e_2, e_3\}$; 0 is a root, so line L12 does nothing | empty |

The root 0 has one child, so line L4 does not mark it. The output is the articulation points $\{2, 3, 5\}$, the bridges $e_4 = \{2, 3\}$ and $e_8 = \{5, 6\}$, and the five blocks $\{e_9\}$, $\{e_8\}$, $\{e_5, e_6, e_7\}$, $\{e_4\}$, $\{e_0, e_1, e_2, e_3\}$, in this order. If step 1 skipped every edge to the parent vertex 0, it would miss $e_1$, but the back edge $e_3$ would still give $\mathrm{low}[1] = 1$ here; in the graph with only $e_0$ and $e_1$, that mistake would report a bridge.

## Correctness

Every edge that is not a tree edge joins a vertex to one of its ancestors ([edge classification](/edge-classification/)). So the only edges that leave the subtree $T(v)$ of a child $v$ of $u$ are the tree edge $\{u, v\}$ and back edges from $T(v)$ to ancestors of $v$. If $\mathrm{low}[v] \ge d[u]$, all of these end at $u$, so removing $u$ cuts $T(v)$ off from the root; if $\mathrm{low}[v] < d[u]$, a back edge goes around $u$. In the same way, the tree edge $\{u, v\}$ lies on a cycle exactly when a back edge from $T(v)$ reaches $u$ or above, which is $\mathrm{low}[v] \le d[u]$. A root is a special case, since nothing lies above it: it is an articulation point when it has two subtrees, because no edge joins two subtrees.

For the blocks, call $v$ a *head* when line L10 succeeds for the tree edge into $v$. Each edge belongs to the nearest head above its lower end. The edges that belong to one head lie pairwise on common cycles, and no cycle uses edges of two heads, because every edge that leaves $T(v)$ for a head $v$ ends at the parent of $v$. When line L11 runs, the edges of the heads deeper in $T(v)$ are already popped, so the edges above $e$ on the stack are exactly the edges of $v$. The full proof is below.

## Complexity

**Time.** Line L1 costs $\Theta(n)$ and line L2 costs $\Theta(m)$. Each vertex is visited once. Each list entry is read once by line L6, and each of the two entries of a non-loop edge leads to $O(1)$ work, except for the pops of line L11. Each edge is pushed once (by line L8 from its upper end or by line L15 from its lower end) and popped once, so all pops cost $O(m)$ in total. The total time is $\Theta(n + m)$ in every case, and no algorithm can do better: [articulation point finding](/articulation-point-finding/) needs $\Omega(n + m)$ time.

**Space.** The arrays $d$ and $\mathrm{low}$, the call stack (or explicit stack) of at most $n$ frames, and the edge stack of at most $m$ edges: $\Theta(n + m)$ extra words. If you need only articulation points and bridges, drop the edge stack, and the extra space is $\Theta(n)$.

## Properties

- **One pass.** One search gives all three outputs, together with the [low-link](/low-link/) values and the [depth-first forest](/dfs-forest/).
- **Output order.** Blocks come out in the order in which their heads finish, so each block comes out before the blocks nearer to the root of the search.
- **Deterministic.** The output sets do not depend on the order of the lists; the forest, the times and the order of the blocks do.
- **Multigraphs.** Parallel edges and loops are handled by edge identifiers and by line L2, with no other change.

## Variants and improvements

- **Low as a time, or low as a vertex.** Some texts store in $\mathrm{low}[u]$ the vertex of least discovery time, or they let a child pass on $\mathrm{low}$ of a back edge's end instead of its $d$. For biconnectivity both forms give the same tests, because only comparisons with $d[u]$ matter.
- **Vertex stack.** Push vertices instead of edges, and on line L11 pop the vertices down to $v$ and add $u$. This gives the vertex sets of the blocks, with $\Theta(n)$ stack space.
- **Bridges only.** Drop the stack and line L12. A different test, with counts of back edges over each tree edge, also works; see [bridge finding](/bridge-finding/).
- **Gabow's path-based method.** Replace the low values by a second stack of the current path, as in [Gabow's strong components algorithm](/gabow-path-based-scc/).
- **Chain decomposition.** Schmidt's method splits the edges into chains along a depth-first search and reads off articulation points and bridges; see [ear decomposition](/ear-decomposition/).
- **Strong components.** The same use of low values on a directed graph gives [Tarjan's strongly connected components algorithm](/tarjan-scc/).
- **Triconnected components.** Hopcroft and Tarjan extended the method to split each block at separation pairs in linear time (1973), a much more complex algorithm.

## When to use it

Use it whenever you need articulation points, bridges, blocks, the [block-cut tree](/block-cut-tree/) or a test for [biconnectivity](/biconnected-graph/) or [2-edge-connectivity](/two-edge-connected-graph/) of a static graph. It is linear and needs no special data structure. For a graph that changes, use [online bridge finding](/online-bridge-finding/) or [dynamic biconnectivity](/dynamic-biconnectivity/) instead.

## Pitfalls

- **Skipping the parent vertex instead of the parent edge.** With parallel edges, a second edge to the parent is a real back edge. Skip only the tree edge, by its identifier.
- **The root.** The test $\mathrm{low}[v] \ge d[u]$ always holds at the root, so line L12 must not mark it. Count its children instead.
- **One vertex marked many times.** A vertex can pass the test of line L10 for several children. Mark it, do not append it to a list each time.
- **Recursion depth.** A path of $10^5$ vertices overflows the call stack in many languages. Use an explicit stack of (vertex, parent edge, next index) frames, as in the implementation.
- **Back edges seen twice.** Push a back edge only from its lower end (line L14), or it is popped into the wrong block.
- **Isolated vertices.** They are in no block of edges. If you want the vertex view of blocks, add each isolated vertex as a block of one vertex.

## Implementations

## History

Hopcroft and Tarjan published the method as Algorithm 447 in Communications of the ACM in 1973. Tarjan's paper "Depth-first search and linear graph algorithms" (1972) gives the same biconnectivity algorithm, together with the strong components algorithm, and made low points a standard tool. In 1973 Hopcroft and Tarjan also gave a linear-time algorithm for triconnected components, and in 1974 a linear planarity test that uses the same kind of depth-first search.

## References
