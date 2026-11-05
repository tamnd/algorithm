---
tag: 94JZ51
kind: algorithm
slug: triangle-listing-by-degree
name: Triangle listing by degree ordering
aliases:
- Chiba-Nishizeki
- forward algorithm
area: graphs/network-analysis
level: core
summary: Orient each edge from lower to higher degree and intersect neighborhoods; runs in O(m^(3/2)) time.
solves: [triangle-counting]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(n + m^(3/2)), best: Θ(n + m)}
  space: {extra: Θ(n + m)}
properties: {directed: false, weighted: false, deterministic: true, recursive: false}
prereqs: [triangle-counting, degree, adjacency-list, arboricity]
see_also: [compact-forward-algorithm, triangle-counting, clustering-coefficient, degeneracy-ordering, arboricity, k-core-decomposition, network-motif-enumeration, triadic-closure]
sources:
  - paper: doi:10.1137/0214017
    title: Norishige Chiba and Takao Nishizeki, Arboricity and subgraph listing algorithms, SIAM Journal on Computing 14(1), 210 to 223 (1985)
    locator: the lemma that the sum over the edges of the smaller end degree is at most 2a(G)m, and the triangle listing that marks the neighbours of each vertex in order of non-increasing degree
  - paper: doi:10.1016/j.tcs.2008.07.017
    title: Matthieu Latapy, Main-memory triangle computations for very large (sparse (power-law)) graphs, Theoretical Computer Science 407(1-3), 458 to 473 (2008)
    locator: the sections on the algorithms forward and compact-forward and their O(m^(3/2)) bound
  - paper: doi:10.1007/11427186_54
    title: Thomas Schank and Dorothea Wagner, Finding, counting and listing all triangles in large graphs, an experimental study, WEA 2005, Lecture Notes in Computer Science 3503, 606 to 609
    locator: the whole paper (the algorithm forward with a degree order, and the experiments)
  - paper: doi:10.1137/0207033
    title: Alon Itai and Michael Rodeh, Finding a minimum circuit in a graph, SIAM Journal on Computing 7(4), 413 to 423 (1978)
    locator: the O(m^(3/2)) bound for finding a triangle
---

Triangle listing by degree ordering lists all triangles of an undirected graph in $O(n + m^{3/2})$ time. It ranks the vertices by [degree](/degree/), orients each edge from the lower-ranked to the higher-ranked end, and finds each triangle exactly once, from its lowest-ranked vertex, by marking the out-neighbours of that vertex and scanning the out-neighbours of each of them. The orientation gives every vertex at most $\sqrt{2m}$ out-neighbours, which is what keeps the cost low even when a few vertices have a huge degree. The same bound is also $O(a(G)\, m)$ in terms of the [arboricity](/arboricity/). It solves [triangle counting](/triangle-counting/) and is the usual basis of the [clustering coefficient](/clustering-coefficient/).

## In plain words

A triangle is three people who all know each other. The slow way to find them is to take each person and test every pair of their friends. A person with ten thousand friends makes that hopeless.

The fix is to give every friendship a direction: from the person with fewer friends to the person with more. Now each person only looks "upward", at friends who are at least as popular. Popular people have few friends who are even more popular, so nobody looks at a long list.

For each person, the algorithm puts a mark on their upward friends. Then, for each marked friend, it looks at that friend's upward friends. Each marked one closes a triangle. Every triangle is found once, from its least popular member.

## The problem

The input is a simple undirected graph $G = (V, E)$ without weights, with $V = \{0, \ldots, n-1\}$ and $m$ edges, given as a list of edges or by adjacency lists. There are no self-loops and no repeated edges. The graph need not be connected. The output is the list of all triangles $\{a, b, c\}$, each exactly once. Its length is the count $T(G)$, and a counter per vertex gives the local counts $t(v)$.

## The algorithm

Let $d(v)$ be the degree of $v$. The *rank* of $v$ is the pair $r(v) = (d(v), v)$, compared in lexicographic order, so ties of degree are broken by the vertex number and every two vertices have different ranks. Write $u \prec v$ when $r(u) < r(v)$.

```pseudo id=main
TRIANGLES-BY-DEGREE(G)
L1  for each v ∈ V do d[v] ← |Adj[v]|
L2  for each v ∈ V do Out[v] ← the neighbours w of v with v ≺ w
L3  for each v ∈ V do mark[v] ← false
L4  T ← an empty list
L5  for each u ∈ V do
L6      for each v ∈ Out[u] do mark[v] ← true
L7      for each v ∈ Out[u] do
L8          for each w ∈ Out[v] do
L9              if mark[w] then append {u, v, w} to T
L10     for each v ∈ Out[u] do mark[v] ← false
L11 return T
```

Lines L1 and L2 build the oriented graph: each edge $\{v, w\}$ appears once, as an arc from its lower-ranked end to its higher-ranked end. This graph has no directed cycle, because the ranks increase along each arc. For each vertex $u$, line L6 marks the out-neighbours of $u$, lines L7 to L9 look for an arc $v \to w$ between two of them, and line L10 clears the marks, so the array is clean for the next $u$. The order of the outer loop does not matter.

## Example

Take the vertices 0 to 5 and the 10 edges $\{0,1\}$, $\{0,2\}$, $\{0,3\}$, $\{0,4\}$, $\{0,5\}$, $\{1,2\}$, $\{1,5\}$, $\{2,3\}$, $\{2,4\}$, $\{3,4\}$. The degrees are $d = (5, 3, 4, 3, 3, 2)$, so the order by rank is $5 \prec 1 \prec 3 \prec 4 \prec 2 \prec 0$. The out-lists are

$$\mathrm{Out}[5] = \{1, 0\},\ \mathrm{Out}[1] = \{2, 0\},\ \mathrm{Out}[3] = \{4, 2, 0\},\ \mathrm{Out}[4] = \{2, 0\},\ \mathrm{Out}[2] = \{0\},\ \mathrm{Out}[0] = \emptyset.$$

The hub 0 has degree 5 but out-degree 0. We run the outer loop in rank order.

| $u$ | marked | $v$, then $\mathrm{Out}[v]$ | triangles found |
|---|---|---|---|
| 5 | 1, 0 | 1: $\{2, 0\}$; 0: $\emptyset$ | $\{5, 1, 0\}$ |
| 1 | 2, 0 | 2: $\{0\}$; 0: $\emptyset$ | $\{1, 2, 0\}$ |
| 3 | 4, 2, 0 | 4: $\{2, 0\}$; 2: $\{0\}$; 0: $\emptyset$ | $\{3, 4, 2\}$, $\{3, 4, 0\}$, $\{3, 2, 0\}$ |
| 4 | 2, 0 | 2: $\{0\}$; 0: $\emptyset$ | $\{4, 2, 0\}$ |
| 2 | 0 | 0: $\emptyset$ | none |
| 0 | none | | none |

The six triangles are found, each once, with 7 tests of line L9. The node iterator, which tests each pair of neighbours of each vertex, would test $\sum_v \binom{d(v)}{2} = 26$ pairs.

## Correctness

**Theorem.** TRIANGLES-BY-DEGREE$(G)$ stops and returns each triangle of $G$ exactly once, and nothing else.

The key fact is that each triangle $\{a, b, c\}$ has a unique order $a \prec b \prec c$ by rank, so it contains exactly the arcs $a \to b$, $a \to c$ and $b \to c$. It is found when $u = a$ and $v = b$, because $b$ and $c$ are both marked and $c \in \mathrm{Out}[b]$. It is not found at any other step: a report at $(u, v, w)$ needs $u \to v$, $u \to w$ and $v \to w$, so $u \prec v \prec w$ is that same unique order. And each report is a triangle, because the three arcs are edges. The invariant that only the out-neighbours of the current $u$ are marked keeps line L9 exact. The full proof is below.

## Complexity

The cost is in the [word RAM](/word-ram/) model, with the vertices numbered $0$ to $n - 1$.

**Out-degrees are small.** Let $d^+(v) = |\mathrm{Out}[v]|$. Each out-neighbour $w$ of $v$ has $d(w) \ge d(v)$. So $d^+(v) \le d(v)$, and since at most $2m/d(v)$ vertices have degree at least $d(v)$, also $d^+(v) \le 2m / d(v)$. Hence $d^+(v) \le \min(d(v), 2m/d(v)) \le \sqrt{2m}$.

**Total time.** Lines L1 to L4 take $O(n + m)$. For a fixed $u$, lines L6 and L10 take $O(d^+(u))$, and lines L7 to L9 take $O(d^+(u) + \sum_{v \in \mathrm{Out}[u]} d^+(v))$. Summing over $u$, the dominant term is

$$\sum_u \sum_{v \in \mathrm{Out}[u]} d^+(v) = \sum_{\text{arcs } u \to v} d^+(v) \le m \sqrt{2m}.$$

So the worst-case time is $O(n + m^{3/2})$. The clique $K_k$ has $\binom{k}{3} = \Theta(m^{3/2})$ triangles, so no listing algorithm can do better in the worst case.

**In terms of the arboricity.** The same sum is $\sum_v d^-(v)\, d^+(v) = \sum_{\text{arcs } v \to w} d^-(v) \le \sum_{\text{arcs } v \to w} d(v)$, and along an arc $v \to w$, $d(v) \le d(w)$. So it is at most $\sum_{\{v, w\} \in E} \min(d(v), d(w))$, which Chiba and Nishizeki bounded by $2a(G)\, m$. Hence the time is also $O(n + a(G)\, m)$, which is $O(n + m)$ on planar graphs and on other graphs of bounded arboricity.

**Best case and space.** The time is at least $\Theta(n + m)$ to read the graph and build the lists; a star, for example, takes $\Theta(n + m)$, because each leaf has the hub as its only out-neighbour and the hub has none. The extra space is $\Theta(n)$ for the degrees and the marks, plus $\Theta(m)$ for the out-lists, which hold each edge once.

## Properties

- **Undirected and without weights.** Edge weights play no role. For a directed graph, run the algorithm on the underlying undirected graph.
- **Deterministic.** Ties of degree are broken by the vertex number. Another fixed tie rule gives the same set of triangles and the same bounds; only the order in which the three vertices of a triangle are reported changes.
- **Disconnected graphs.** The algorithm never crosses between components; an isolated vertex costs $O(1)$.
- **Order-free outer loop.** The vertices $u$ can be processed in any order, and in parallel: different values of $u$ only need their own mark arrays.
- **Lists and counts.** For counts only, replace line L9 with three counter increments, for $u$, $v$ and $w$.

## Variants and improvements

- **Compact-forward.** [Compact-forward](/compact-forward-algorithm/) uses the same idea with a merge of two sorted adjacency lists instead of a mark array, and needs no second copy of the lists.
- **Hash sets.** Put each $\mathrm{Out}[u]$ in a [hash table](/hash-table/) and test $w \in \mathrm{Out}[u]$ directly. This gives the same bounds in expectation and needs no clearing step.
- **Degeneracy order.** Rank the vertices by a [degeneracy ordering](/degeneracy-ordering/) instead of by degree. Then each out-degree is at most the degeneracy $\delta(G) \le 2a(G) - 1$, and the time is $O(n + \delta(G)\, m)$. The [Batagelj-Zaversnik algorithm](/batagelj-zaversnik-algorithm/) computes such an order in linear time.
- **Larger cliques.** The same orientation lists the $k$-cliques: Chiba and Nishizeki list them in $O(k\, a(G)^{k-2} m)$ time.
- **Fast matrix multiplication.** Alon, Yuster and Zwick split the vertices by degree and handle the high-degree part with a matrix product, for $O(m^{2\omega/(\omega+1)})$ time for counting. See [triangle counting](/triangle-counting/).

## When to use it

Use it to list or count the triangles of a large sparse graph in memory, for example for the [clustering coefficient](/clustering-coefficient/), for transitivity, or for [motif](/network-motif-enumeration/) counts. It is short, it handles graphs with a heavy-tailed [degree distribution](/degree-distribution/) well, and its outer loop is easy to run in parallel. When memory is tight, compact-forward avoids the copy of the lists. For dense graphs, the matrix method can be faster in theory. For graphs that do not fit in memory, use a streaming or an external-memory method.

## Pitfalls

- **Orienting by vertex number.** Building $\mathrm{Out}[v]$ in line L2 from the vertex numbers alone, with no degree, keeps the result correct but loses the bound. In a star whose hub has the middle number, about $n/2$ leaves have an arc to the hub, and the hub has about $n/2$ out-neighbours, so line L8 scans the out-list of the hub about $n/2$ times: $\Theta(n^2)$ time with $m = n - 1$. Line L2 must use the rank $r(v) = (d(v), v)$.
- **Ties of degree without a tie rule.** Comparing only degrees in line L2 either keeps both arcs of an edge between two vertices of equal degree, which reports a triangle more than once, or keeps neither, which loses triangles. The vertex number in the rank removes the ties.
- **Forgetting to clear the marks.** Without line L10, a mark from an earlier $u$ makes line L9 report three vertices that are not a triangle.
- **Self-loops and repeated edges.** A repeated edge puts a vertex twice into an out-list, and line L9 then reports the same triangle twice. Remove repeated edges and loops first.

## Implementations

## History

Itai and Rodeh gave an $O(m^{3/2})$ method to find a triangle in 1978. Chiba and Nishizeki listed all triangles in $O(a(G)\, m)$ time in 1985: they process the vertices in order of non-increasing degree, mark the neighbours of each, and delete it. This is a close relative of the orientation used here, and the analysis is the same. Schank and Wagner (2005) and Latapy (2008) studied the forward algorithms based on a degree order on large real graphs and showed that they are among the fastest methods in practice.

## References
