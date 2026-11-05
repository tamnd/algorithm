---
tag: R006RZ
kind: algorithm
slug: compact-forward-algorithm
name: Compact-forward algorithm
aliases:
- forward triangle listing
area: graphs/network-analysis
level: advanced
summary: Counts triangles in O(m^1.5) by orienting edges along a degree ordering.
solves: [triangle-counting]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(n + m^(3/2)), best: Θ(n + m)}
  space: {extra: Θ(n + m)}
properties: {directed: false, weighted: false, deterministic: true, recursive: false}
prereqs: [triangle-counting, degree, adjacency-list, counting-sort]
see_also: [triangle-counting, clustering-coefficient, arboricity, degeneracy-ordering, batagelj-zaversnik-algorithm, clique, common-neighbors, adjacency-list]
sources:
  - paper: doi:10.1016/j.tcs.2008.07.017
    title: Matthieu Latapy, Main-memory triangle computations for very large (sparse (power-law)) graphs, Theoretical Computer Science 407(1-3), 458 to 473 (2008)
    locator: the sections on the algorithms forward and compact-forward (the numbering by degree, the merge of the sorted lists, the O(m^(3/2)) time and the space beyond the graph)
  - paper: doi:10.1007/11427186_54
    title: Thomas Schank and Dorothea Wagner, Finding, counting and listing all triangles in large graphs, an experimental study, WEA 2005, Lecture Notes in Computer Science 3503, 606 to 609
    locator: the whole paper (the algorithm forward and its comparison with the other listing methods)
  - paper: doi:10.1137/0214017
    title: Norishige Chiba and Takao Nishizeki, Arboricity and subgraph listing algorithms, SIAM Journal on Computing 14(1), 210 to 223 (1985)
    locator: the triangle listing algorithm in O(a(G) m) time, with a(G) the arboricity
  - paper: doi:10.1137/0207033
    title: Alon Itai and Michael Rodeh, Finding a minimum circuit in a graph, SIAM Journal on Computing 7(4), 413 to 423 (1978)
    locator: the O(m^(3/2)) method to find a triangle
---

The compact-forward algorithm lists all triangles of an undirected graph with $m$ edges in $O(m^{3/2})$ time and with $O(n + m)$ space, which also counts them. It numbers the vertices by non-increasing [degree](/degree/), and finds each triangle once, from its edge between the two vertices of largest number, as a common neighbour of smaller number. The common neighbours are found by a merge of two sorted [adjacency lists](/adjacency-list/), which stops early at the current vertex; this stop is what keeps the cost low on graphs with a few vertices of huge degree. Latapy gave it in 2008 as a version of the *forward* algorithm of Schank and Wagner that needs no extra lists. It solves [triangle counting](/triangle-counting/), the main step of the [clustering coefficient](/clustering-coefficient/).

## In plain words

A triangle is three people who all know each other. To find all of them, you could test every group of three, but in a network with a million people that is far too many.

The algorithm first lines the people up, with the best-connected first. A triangle has a first, a middle and a last person in this line. The algorithm looks for each triangle from its middle person: for each friend of the middle person who comes later in the line, it looks for a friend that both have and who comes earlier than the middle person.

Since the friend lists are kept in the same order as the line, this search is one pass over the start of two lists. The very popular people come first, so their long lists are rarely read to the end.

## The problem

The input is a simple undirected graph $G = (V, E)$ without weights, with $V = \{0, \ldots, n-1\}$ and $m$ edges, given by adjacency lists, each edge in both lists, with no self-loops and no repeated edges. The graph need not be connected.

A *triangle* is a set $\{a, b, c\}$ of three vertices that are pairwise adjacent. The output is the list of all triangles, each exactly once, and its length $T$. In this form there is no question of direction or weights; for a directed graph, see the variants.

## The algorithm

Write $\eta(v)$ for the position of $v$ when the vertices are sorted by non-increasing degree, ties by vertex number. So $\eta(u) < \eta(v)$ implies $d(u) \ge d(v)$.

```pseudo id=main
COMPACT-FORWARD(G)
L1  η ← the numbering of V by non-increasing degree, ties by vertex number
L2  for each v ∈ V do sort Adj[v] by η
L3  T ← an empty list
L4  for each v ∈ V in increasing order of η do
L5      for each u ∈ Adj[v] with η(u) > η(v) do
L6          i ← 0; j ← 0                                 ▷ positions in Adj[v] and Adj[u]
L7          while i < |Adj[v]| and j < |Adj[u]| and η(Adj[v][i]) < η(v) and η(Adj[u][j]) < η(v) do
L8              a ← Adj[v][i]; b ← Adj[u][j]
L9              if η(a) < η(b) then i ← i + 1
L10             else if η(a) > η(b) then j ← j + 1
L11             else append {a, v, u} to T; i ← i + 1; j ← j + 1
L12 return T
```

A triangle $\{a, v, u\}$ with $\eta(a) < \eta(v) < \eta(u)$ is found only at the edge $(v, u)$ of line L5, as an element $a$ of both lists before position $\eta(v)$, so it is found exactly once. Line L1 is a [counting sort](/counting-sort/) by degree. Line L2 also takes linear time: run through the vertices $w$ in the order of $\eta$ and append $w$ to the new list of each neighbour of $w$.

The name comes from the space. The forward algorithm of Schank and Wagner builds, for each vertex, a second list of the neighbours already processed. Compact-forward finds the same neighbours as the start of the sorted list, so it needs only the graph and the array $\eta$.

## Example

Take the undirected graph with the vertices 0 to 6 and the 9 edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{1,3\}$, $\{2,3\}$, $\{3,4\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$. The degrees are $2, 3, 3, 3, 3, 2, 2$, so the order by $\eta$ is $1, 2, 3, 4, 0, 5, 6$. The sorted lists are $\mathrm{Adj}[0] = (1, 2)$, $\mathrm{Adj}[1] = (2, 3, 0)$, $\mathrm{Adj}[2] = (1, 3, 0)$, $\mathrm{Adj}[3] = (1, 2, 4)$, $\mathrm{Adj}[4] = (3, 5, 6)$, $\mathrm{Adj}[5] = (4, 6)$ and $\mathrm{Adj}[6] = (4, 5)$.

| $v$ | $u$ | start of $\mathrm{Adj}[v]$ before $v$ | start of $\mathrm{Adj}[u]$ before $v$ | found |
|---|---|---|---|---|
| 1 | 2, 3, 0 | empty | | none |
| 2 | 3 | 1 | 1 | $\{1, 2, 3\}$ |
| 2 | 0 | 1 | 1 | $\{1, 2, 0\}$ |
| 3 | 4 | 1, 2 | empty | none |
| 4 | 5 | 3 | empty | none |
| 4 | 6 | 3 | empty | none |
| 0 | none | | | |
| 5 | 6 | 4 | 4 | $\{4, 5, 6\}$ |

The graph has $T = 3$ triangles. For $v = 1$, the first vertex, nothing comes before it, so its three edges cost one test each. For $v = 0$, both neighbours come earlier, so line L5 skips them. The 9 edges give 6 merges, and the longest merge reads 2 entries of one list.

## Correctness

**Theorem.** COMPACT-FORWARD$(G)$ stops and returns each triangle of $G$ exactly once, and nothing else.

Each pair $(v, u)$ at line L5 is an edge with $\eta(v) < \eta(u)$, so each edge is taken once. The loop of lines L7 to L11 is a merge of the two lists cut at $\eta(v)$; since both are sorted by $\eta$, it finds exactly their common elements $a$ with $\eta(a) < \eta(v)$. A found $a$ is adjacent to $v$ and $u$, so $\{a, v, u\}$ is a triangle. Conversely a triangle with $\eta(a) < \eta(v) < \eta(u)$ is found at the edge $(v, u)$, and at no other edge, because the other two edges would need a common neighbour before their smaller end, and $a$, $v$ are the smaller ends. The full proof is below.

## Complexity

The cost is in the [word RAM](/word-ram/) model.

- **Preparation.** Lines L1 and L2 take $O(n + m)$ with a counting sort and the rebuilding of the lists.
- **The merges.** For an edge $(v, u)$ with $\eta(v) < \eta(u)$, the merge reads only neighbours $x$ of $v$ or $u$ with $\eta(x) < \eta(v)$. Each such $x$ has $d(x) \ge d(v)$. There are at most $d(v)$ of them in $\mathrm{Adj}[v]$, and at most $d(u) \le d(v)$ in $\mathrm{Adj}[u]$. There are also at most $2m / d(v)$ vertices with degree at least $d(v)$. So each merge reads at most $2 \min(d(v), 2m/d(v)) \le 2\sqrt{2m}$ entries, and the $m$ merges cost $O(m^{3/2})$.

The time is $O(n + m^{3/2})$. The bound is tight in general: a [clique](/clique/) on $k$ vertices has $m \approx k^2/2$ edges and $\binom{k}{3} = \Theta(m^{3/2})$ triangles, all of which are listed. The best case is $\Theta(n + m)$, for example a graph without triangles in which each vertex has few earlier neighbours. The extra space is $\Theta(n)$ for $\eta$, plus $\Theta(n + m)$ if the sorted lists are a new copy.

## Properties

- **Undirected and without weights.** Edge weights play no role in the existence of a triangle.
- **Deterministic.** The degree order with ties by vertex number fixes the output order. Any other tie rule lists the same triangles in another order, with the same time bound.
- **Not recursive.** Three nested loops.
- **Lists, not only counts.** Each triangle is produced explicitly, which is needed for the local clustering coefficient of each vertex: add 1 to a counter of $a$, $v$ and $u$ for each triangle found.
- **Disconnected graphs.** The loops never cross between components, so each component is handled on its own; isolated vertices cost $O(1)$.

## Variants and improvements

- **Forward.** The algorithm of Schank and Wagner keeps a growing list $A(u)$ of the processed neighbours of each vertex and intersects $A(u)$ and $A(v)$. It has the same time, with $O(m)$ extra space.
- **Edge iterator and node iterator.** Without the degree order, merging the full lists of the ends of each edge takes $O(\sum_v d(v)^2)$ time, which is much worse on graphs with vertices of very large degree.
- **Hashing.** Put the forward neighbours of $v$ in a [hash table](/hash-table/) and test each forward neighbour of $u$, which gives the same bound in expectation and is common in practice.
- **Fast matrix multiplication.** Alon, Yuster and Zwick count triangles in $O(m^{2\omega/(\omega+1)})$ time with matrix products for the high-degree part, where $\omega$ is the exponent of [matrix multiplication](/matrix-multiplication-exponent/). This is faster in theory but is not used on sparse graphs in practice.
- **Directed triangles.** For directed graphs, run the algorithm on the underlying undirected graph and check the directions of the three arcs of each triangle found, to classify it as a cycle or as transitive.
- **Approximate counts.** Sampling of wedges or edges, and streaming algorithms, estimate $T$ in sublinear time or space.

## When to use it

Use it to list or count the triangles of a large sparse graph in main memory, for example to compute the [clustering coefficient](/clustering-coefficient/) or the transitivity of a social network. Its memory beyond the graph is one array, and its merges read short prefixes even on graphs with a heavy-tailed degree distribution. For dense graphs, the matrix method may win; for graphs that do not fit in memory, use a streaming or external-memory method.

## Pitfalls

- **An arbitrary order.** The bound needs the degree order. Take a path $v_1, \ldots, v_k$ plus a hub $h$ joined to every $v_i$, numbered $v_1, \ldots, v_k, h$. At the edge $(v_i, h)$, the prefix of $\mathrm{Adj}[v_i]$ is just $v_{i-1}$, but the merge runs through the $i - 2$ entries of $\mathrm{Adj}[h]$ before it. The total is $\Theta(k^2)$ with $m = \Theta(k)$, more than $m^{3/2}$. With the hub first, each merge takes one step.
- **Self-loops and repeated edges.** A self-loop or a repeated edge can make a pair look like a triangle or report a triangle twice. Clean the graph first.
- **Lists not sorted by $\eta$.** The merge needs both lists in the same order. Sorting by vertex number is not enough, since the cut at $\eta(v)$ must be a prefix.
- **Counting by $\binom{d}{2}$.** The number of wedges is not the number of triangles. The ratio of 3 times the triangles to the wedges is the transitivity.

## Implementations

## History

Itai and Rodeh found a triangle in $O(m^{3/2})$ time in 1978, and Chiba and Nishizeki listed all triangles in $O(a(G)\, m)$ time in 1985, using the [arboricity](/arboricity/). Schank and Wagner compared triangle listing methods on large graphs in 2005 and proposed the forward algorithm. Latapy studied triangle computations for very large power-law graphs in 2008, and introduced compact-forward to save the space of the extra lists while keeping the time of forward.

## References
