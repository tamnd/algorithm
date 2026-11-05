---
tag: TDTBHE
kind: algorithm
slug: union-find-connectivity
name: Connectivity by union-find
aliases:
- Union-find connected components
area: graphs/connectivity
level: intro
summary: Union each edge's endpoints in a disjoint-set structure; the sets at the end are the components.
solves: [connected-components]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, α: the inverse Ackermann function}
  time: {worst: O((n + m) α(n)), best: Θ(n + m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: true}
prereqs: [connected-components, disjoint-set, union-by-rank, path-compression]
see_also: [disjoint-set-forest, inverse-ackermann-function, incremental-connectivity, kruskal, weakly-connected-graph, generic-component-growing, union-find-lower-bound]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 19.1, Disjoint-set operations (the procedures CONNECTED-COMPONENTS and SAME-COMPONENT), Section 19.3, Disjoint-set forests, and Section 19.4 (the analysis with the inverse Ackermann function)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.5, Case study, union-find (dynamic connectivity, weighted quick-union with path compression)
  - paper: doi:10.1145/321879.321884
    title: Robert E. Tarjan, Efficiency of a good but not linear set union algorithm, Journal of the ACM 22(2), 215 to 225 (1975)
    locator: the whole paper (the bound with the inverse Ackermann function for union by rank with path compression)
  - book: isbn:9780898711875
    title: Robert E. Tarjan, Data Structures and Network Algorithms, SIAM (1983)
    locator: Chapter 2, Disjoint sets
  - paper: doi:10.1145/73007.73040
    title: Michael L. Fredman and Michael E. Saks, The cell probe complexity of dynamic data structures, Proceedings of the 21st ACM Symposium on Theory of Computing, 345 to 354 (1989)
    locator: the lower bound for the union-find problem
---

Connectivity by union-find computes the [connected components](/connected-components/) of an undirected graph by reading its edges one by one, in any order, and merging the sets of the two ends of each edge in a [disjoint-set](/disjoint-set/) structure. After the last edge, two vertices are in the same set exactly when they are joined by a path. With [union by rank](/union-by-rank/) and [path compression](/path-compression/), the whole run takes $O((n + m)\,\alpha(n))$ time, where $\alpha$ is the [inverse Ackermann function](/inverse-ackermann-function/), and only $\Theta(n)$ memory besides the edges. It needs no adjacency lists, and it can answer "are $u$ and $v$ connected?" at any moment while the edges arrive.

## In plain words

Give each vertex its own club at the start. Then read the edges. For each edge, ask the two ends which club they belong to. If the clubs differ, merge them into one club. If they are the same, the edge adds nothing new, so skip it.

Each club keeps a leader, and each member knows a way to reach its leader through a chain of members. Two vertices are in the same club exactly when their chains end at the same leader. Two tricks keep the chains very short: hang the smaller club under the larger one, and after walking a chain, point everyone on it straight at the leader. When all edges are read, the clubs are the components.

## The problem

The input is a number $n$ and a list $E$ of $m$ pairs $\{u, v\}$ with $u, v \in \{0, \ldots, n-1\}$, the edges of an undirected graph $G = (V, E)$. Parallel edges and [self-loops](/self-loop/) are allowed. The output is a label $comp[v]$ for each vertex such that $comp[u] = comp[v]$ exactly when $G$ has a path from $u$ to $v$. This is the [connected components](/connected-components/) problem. If the pairs are the arcs of a [directed graph](/directed-graph/), the algorithm ignores their direction and finds the components of the [weakly connected](/weakly-connected-graph/) kind. It cannot find [strongly connected components](/strongly-connected-components/).

## The algorithm

The structure is a [disjoint-set forest](/disjoint-set-forest/): each vertex has a parent, a root is its own parent, and the root names the set.

```pseudo id=main
UF-COMPONENTS(n, E)
L1  for v ← 0 to n − 1 do parent[v] ← v, rank[v] ← 0
L2  for each edge {u, v} ∈ E do
L3      a ← FIND(u), b ← FIND(v)
L4      if a ≠ b then LINK(a, b)
L5  for v ← 0 to n − 1 do comp[v] ← FIND(v)
L6  return comp

FIND(x)
L7  r ← x; while parent[r] ≠ r do r ← parent[r]
L8  while parent[x] ≠ r do (parent[x], x) ← (r, parent[x])   ▷ path compression
L9  return r

LINK(a, b)                                                   ▷ a ≠ b are roots
L10 if rank[a] < rank[b] then swap a and b
L11 parent[b] ← a
L12 if rank[a] = rank[b] then rank[a] ← rank[a] + 1
```

Line L3 finds the roots of the two ends. Line L4 merges the two trees only when the roots differ. A self-loop and a second copy of an edge always give $a = b$ and are skipped. FIND walks up to the root in line L7 and then, in line L8, points each vertex of the walked path straight at the root. LINK hangs the root of lower rank under the root of higher rank, and a rank grows only when two trees of equal rank meet. Line L5 gives each vertex the name of its root.

## Example

Take $n = 8$ and the edges, in this order: $\{0,1\}$, $\{2,3\}$, $\{1,2\}$, $\{4,5\}$, $\{3,0\}$, $\{6,6\}$, $\{5,4\}$, $\{1,3\}$. Vertex 7 has no edge.

| edge | roots $a, b$ | action | parent (after) | rank changes |
|---|---|---|---|---|
| start | | | 0 1 2 3 4 5 6 7 | all 0 |
| $\{0,1\}$ | 0, 1 | LINK: parent[1] ← 0 | 0 0 2 3 4 5 6 7 | rank[0] = 1 |
| $\{2,3\}$ | 2, 3 | LINK: parent[3] ← 2 | 0 0 2 2 4 5 6 7 | rank[2] = 1 |
| $\{1,2\}$ | 0, 2 | LINK: parent[2] ← 0 | 0 0 0 2 4 5 6 7 | rank[0] = 2 |
| $\{4,5\}$ | 4, 5 | LINK: parent[5] ← 4 | 0 0 0 2 4 4 6 7 | rank[4] = 1 |
| $\{3,0\}$ | 0, 0 | skip; FIND(3) walks 3, 2, 0 and sets parent[3] ← 0 | 0 0 0 0 4 4 6 7 | |
| $\{6,6\}$ | 6, 6 | skip (self-loop) | same | |
| $\{5,4\}$ | 4, 4 | skip (parallel to $\{4,5\}$) | same | |
| $\{1,3\}$ | 0, 0 | skip | same | |

Line L5 gives $comp = [0, 0, 0, 0, 4, 4, 6, 7]$. The components are $\{0, 1, 2, 3\}$, $\{4, 5\}$, $\{6\}$ and $\{7\}$. There were 4 successful links, and $8 - 4 = 4$ components. The 4 edges that caused a link, $\{0,1\}$, $\{2,3\}$, $\{1,2\}$ and $\{4,5\}$, form a [spanning forest](/spanning-forest/) of the graph.

## Correctness

Let $E_i$ be the first $i$ edges of the list, and $G_i = (V, E_i)$. The loop of line L2 keeps this invariant:

> After $i$ edges, $\mathrm{FIND}(x) = \mathrm{FIND}(y)$ if and only if $x$ and $y$ are joined by a path in $G_i$.

Before the loop, every vertex is its own root and $G_0$ has no edge, so the invariant holds. An edge $\{u, v\}$ joins the components of $u$ and $v$ in $G_{i-1}$ into one, and LINK joins the two trees of their roots into one, or nothing happens when they are already equal. Path compression and the rank rule change the shape of the trees but never the set of vertices below a root. The full proof is in [the proof page](proofs/correctness.md).

## Complexity

- **Operations.** Line L1 makes $n$ sets. The loop does $2m$ calls of FIND and at most $n - 1$ calls of LINK, because each LINK lowers the number of trees by one. Line L5 does $n$ more calls of FIND. So there are $O(n + m)$ operations on a structure with $n$ elements.
- **Worst case.** With union by rank and path compression, a sequence of $s$ operations on $n$ elements takes $O(s\,\alpha(n))$ time (Tarjan, 1975; CLRS, Section 19.4). With $s = O(n + m)$, the time is $O((n + m)\,\alpha(n))$. The function $\alpha(n)$ is at most 4 for every $n$ that fits in the memory of a real computer, so the run is linear in practice.
- **Best case.** Each edge needs two FIND calls and each vertex is touched in lines L1 and L5, so the time is $\Omega(n + m)$ on every input.
- **Space.** The arrays $parent$ and $rank$ take $\Theta(n)$ words. The edges are read once, in order, and need not be stored: the algorithm works on a stream of edges.
- **Without the tricks.** With neither union by rank nor path compression, a list of edges $\{1, 0\}, \{2, 0\}, \ldots, \{n-1, 0\}$ can build a path of height $n - 1$, and the time becomes $\Theta(n m)$ in the worst case. With union by rank alone, each tree has height at most $\lg n$, and the time is $O(n + m \log n)$.

Graph search finds the components in $\Theta(n + m)$ time, which is a little better than $O((n + m)\,\alpha(n))$. For the online problem, where queries come between the edges, union-find is optimal: Fredman and Saks proved an $\Omega(\alpha(n))$ amortized lower bound for each operation in the [cell-probe model](/cell-probe-model/) (see [the union-find lower bound](/union-find-lower-bound/)).

## Properties

- **Any edge order.** The final partition does not depend on the order of the edges, only the roots that name the sets do.
- **Online.** After any prefix of the edges, FIND answers whether two vertices are already connected. This is [incremental connectivity](/incremental-connectivity/).
- **No adjacency lists.** The input can be an [edge list](/edge-list/), a file or a stream. The memory is $\Theta(n)$, not $\Theta(n + m)$.
- **A spanning forest for free.** The edges that cause a LINK form a spanning forest. With the edges sorted by weight, this is [Kruskal's algorithm](/kruskal/).
- **Iterative.** The two loops of FIND need no recursion, so long chains do not overflow the stack.

## Variants and improvements

- **Union by size.** Hang the tree with fewer vertices under the other one. It has the same bounds as union by rank. See [union by size](/union-by-size/).
- **Path halving or path splitting.** Point each vertex on the walk to its grandparent in a single pass. They give the same bound with one loop. See [path halving](/path-halving/) and [path splitting](/path-splitting/).
- **Counting.** Keep a counter that starts at $n$ and drops by one in each LINK. It gives the number of components at every moment.
- **Bipartiteness and parity.** Store the parity of the path to the parent, as in [union-find with parity](/dsu-with-parity/), to test whether each component is bipartite.
- **Deletions.** Union-find cannot undo a union, so it cannot handle edge deletions. With a stack of changes and no path compression it can undo the last unions, as in [union-find with rollback](/union-find-with-rollback/), which is the base of [offline dynamic connectivity](/offline-dynamic-connectivity/). Fully [dynamic connectivity](/dynamic-connectivity/) needs other structures.

## When to use it

Use union-find when the edges come as a list or a stream, when the graph is too large to build adjacency lists, when edges arrive over time and connectivity questions come in between, or when the components are a step of a larger algorithm such as Kruskal's. If the graph is already in [adjacency lists](/adjacency-list/) and is fixed, a [graph search](/generic-component-growing/) is as simple and runs in $\Theta(n + m)$ time without the $\alpha$ factor. If edges are also deleted, use a dynamic connectivity structure.

## Pitfalls

- **Linking the ends instead of the roots.** Writing parent[v] ← u in line L4, instead of linking the roots $a$ and $b$, cuts $v$ out of its old tree and loses connections. LINK must work on the roots that line L3 returns.
- **Comparing parents instead of roots.** Testing parent[u] = parent[v] instead of FIND(u) = FIND(v) in line L4 is wrong as soon as a tree has height 2.
- **Reading comp before line L5.** The array $parent$ is not a label array: after the loop, a vertex can still point to a non-root. Call FIND for each vertex, as line L5 does.
- **Recursive FIND.** A recursive FIND with path compression is short, but on a long chain it can exceed the recursion limit of Python. Use the two loops of lines L7 and L8.
- **Strong components.** Union-find ignores direction. On a directed graph it gives weak components, not strong ones.

## Implementations

## History

Tarjan proved in 1975 that the two together take $O(s\,\alpha(n))$ time for $s$ operations, and that this bound is tight for the method: some sequences of operations make it take $\Omega(s\,\alpha(n))$ time. Fredman and Saks proved in 1989 that every structure for the problem needs $\Omega(\alpha(n))$ amortized time per operation in the cell-probe model.

## References
