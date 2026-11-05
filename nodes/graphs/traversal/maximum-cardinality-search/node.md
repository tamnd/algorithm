---
tag: M2KXJV
kind: algorithm
slug: maximum-cardinality-search
name: Maximum cardinality search
aliases:
- MCS
area: graphs/traversal
level: advanced
summary: Visits next the vertex with the most already-visited neighbours; its reverse is a perfect elimination ordering of chordal graphs.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m), best: Θ(n + m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
prereqs: [chordal-graph, perfect-elimination-ordering]
see_also: [lexicographic-bfs, chordal-graph-coloring, maximal-clique, tree-decomposition, bucket-queue, hypergraph, elimination-ordering, certifying-algorithms]
sources:
  - paper: doi:10.1137/0213035
    title: Robert E. Tarjan and Mihalis Yannakakis, Simple linear-time algorithms to test chordality of graphs, test acyclicity of hypergraphs, and selectively reduce acyclic hypergraphs, SIAM Journal on Computing 13(3), 566 to 579 (1984)
    locator: the definition of maximum cardinality search, its implementation with sets indexed by the number of numbered neighbours, the proof that it gives a perfect elimination ordering of a chordal graph, and the linear-time zero fill-in test
  - paper: doi:10.1007/978-1-4613-8369-7_1
    title: Jean R. S. Blair and Barry Peyton, An introduction to chordal graphs and clique trees, in Graph Theory and Sparse Matrix Computation, The IMA Volumes in Mathematics and its Applications 56, 1 to 29 (1993)
    locator: the section on maximum cardinality search and the computation of clique trees from it
  - paper: doi:10.1007/s00453-004-1084-3
    title: Anne Berry, Jean R. S. Blair, Pinar Heggernes and Barry W. Peyton, Maximum cardinality search for computing minimal triangulations of graphs, Algorithmica 39(4), 287 to 298 (2004)
    locator: the algorithm MCS-M, which adds fill edges during the search and gives a minimal triangulation
---

Maximum cardinality search (MCS) orders the vertices of an undirected graph one by one, and at each step it visits an unvisited vertex with the largest number of visited neighbours. Tarjan and Yannakakis introduced it in 1984 as a simpler alternative to [lexicographic breadth-first search](/lexicographic-bfs/) for the recognition of [chordal graphs](/chordal-graph/): a graph is chordal if and only if the reverse of an MCS order is a [perfect elimination ordering](/perfect-elimination-ordering/), and this can be checked in linear time. With an array of buckets indexed by the count, MCS runs in $\Theta(n + m)$ time.

## In plain words

Pick any vertex to start. Then, again and again, look at the vertices that are not visited yet, count for each one how many of its neighbours are already visited, and visit one with the highest count. Ties may be broken in any way.

So the search always grows the visited part where it is most tightly joined to the rest. On a graph in which every long cycle has a shortcut, this order has a strong property: read backwards, each vertex is joined to a group of earlier vertices that are all joined to each other.

The search does not care which neighbours are visited, only how many. This makes it simpler than lexicographic breadth-first search, which compares the visited neighbours one by one.

## The problem

The input is a simple undirected graph $G = (V, E)$ given by adjacency lists, with $n$ vertices and $m$ edges. The output is an order $\sigma = (v_1, \ldots, v_n)$ of $V$ that obeys the MCS rule below. The main use is the recognition problem for [chordal graphs](/chordal-graph/): decide whether every cycle of length at least 4 has a chord, and if so give a [perfect elimination ordering](/perfect-elimination-ordering/).

**MCS rule.** Before step $i$, the vertices $v_1, \ldots, v_{i-1}$ are visited. The *weight* of an unvisited vertex $x$ is $w(x) = |N(x) \cap \{v_1, \ldots, v_{i-1}\}|$. At each step $i$, the vertex $v_i$ has the largest weight among the unvisited vertices. Ties may be broken in any way. Tarjan and Yannakakis number the vertices from $n$ down to 1, so their numbering is the reverse of $\sigma$, which is the elimination order itself.

## The algorithm

The algorithm keeps a bucket $B[k]$ for each weight $k$, which holds the unvisited vertices of weight $k$, and an index $j$ of the largest non-empty bucket.

```pseudo id=main
MCS(G)
L1  size[x] ← 0 for each x; B[0] ← V; B[k] ← ∅ for k ≥ 1; j ← 0
L2  for i ← 1 to n do
L3      v ← a vertex of B[j]; remove v from B[j]
L4      σ[i] ← v; mark v visited
L5      for each neighbour w of v that is not visited do
L6          move w from B[size[w]] to B[size[w] + 1]; size[w] ← size[w] + 1
L7      j ← j + 1
L8      while j ≥ 0 and B[j] = ∅ do j ← j − 1
L9  return σ
```

The implementation takes the vertex that entered $B[j]$ first, and $B[0]$ starts with $0, 1, \ldots, n - 1$, so the search starts at vertex 0.

**Chordal graph recognition.** Run MCS. Then the graph is chordal if and only if, for each vertex $x$, the neighbours of $x$ visited before $x$ form a clique. The same linear-time test as for LexBFS works: for each $x$, let $p(x)$ be the latest visited of these earlier neighbours, and test that all other earlier neighbours of $x$ are neighbours of $p(x)$. Tarjan and Yannakakis call this the zero fill-in test.

## Example

Take the chordal graph with vertices 0 to 6 and the edges $\{0,3\}$, $\{1,2\}$, $\{1,3\}$, $\{1,6\}$, $\{2,6\}$, $\{3,4\}$, $\{3,6\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$, with sorted lists. Each bucket is shown with its vertices in the order in which they entered it.

| step | non-empty buckets before the step | visit | weight changes |
|---|---|---|---|
| 1 | $B[0] = 0, 1, 2, 3, 4, 5, 6$ | 0 | $3 \to 1$ |
| 2 | $B[1] = 3$; $B[0] = 1, 2, 4, 5, 6$ | 3 | $1, 4, 6 \to 1$ |
| 3 | $B[1] = 1, 4, 6$; $B[0] = 2, 5$ | 1 | $2 \to 1$; $6 \to 2$ |
| 4 | $B[2] = 6$; $B[1] = 4, 2$; $B[0] = 5$ | 6 | $2, 4 \to 2$; $5 \to 1$ |
| 5 | $B[2] = 2, 4$; $B[1] = 5$ | 2 | none |
| 6 | $B[2] = 4$; $B[1] = 5$ | 4 | $5 \to 2$ |
| 7 | $B[2] = 5$ | 5 | |

The MCS order is $0, 3, 1, 6, 2, 4, 5$. At step 5, vertices 2 and 4 both have two visited neighbours, $\{1, 6\}$ and $\{3, 6\}$, and the tie goes to 2, which entered $B[2]$ first. [Lexicographic BFS](/lexicographic-bfs/) visits 4 here, because 4 is joined to 3, which was visited before 1. So the two searches give different orders.

The earlier neighbours of each vertex are: $3: \{0\}$; $1: \{3\}$; $6: \{3, 1\}$; $2: \{1, 6\}$; $4: \{3, 6\}$; $5: \{6, 4\}$. Each pair is an edge, so the reverse order $5, 4, 2, 6, 1, 3, 0$ is a perfect elimination ordering, and the graph is chordal.

**A graph that is not chordal.** On the 4-cycle $0, 1, 2, 3$, MCS visits $0, 1, 3, 2$. The earlier neighbours of 2 are 1 and 3, which are not adjacent, so the test reports that the graph is not chordal.

## Correctness

Lines L5 and L6 keep each unvisited vertex in the bucket of its weight, and line L8 finds the largest non-empty bucket, so each step takes a vertex of largest weight. For the chordal test, the key fact is a weaker form of the four-point property of LexBFS: if $a$, $b$, $c$ are visited in this order, $ac \in E$ and $ab \notin E$, then some $d$ visited before $b$ has $db \in E$ and $dc \notin E$. It holds because $b$ had at least as many visited neighbours as $c$, and $a$ was one of $c$'s but not of $b$'s. In a chordal graph this forbids two non-adjacent earlier neighbours of a vertex, because they would lead to a chordless cycle. The full proof is below.

## Complexity

The cost is in the [word RAM](/word-ram/) model. Each bucket is a doubly linked list, and each vertex points to its place in its bucket, so lines L3 and L6 take $O(1)$ time.

- **Lines L3 and L4.** One time per vertex: $\Theta(n)$.
- **Lines L5 and L6.** One time per list entry of a visited vertex: $\Theta(m)$ in total, counting both ends of each edge.
- **Lines L7 and L8.** After a step, the largest weight is at most one more than before, so line L7 never makes $j$ too small. Line L7 adds 1 to $j$ $n$ times, and line L8 subtracts 1 at most as often, plus 1 at the end, so all runs of line L8 take $O(n)$ time.

So the time is $\Theta(n + m)$, and the extra space is $\Theta(n)$ for the buckets, the weights and the marks. The chordal test adds $O(n + m)$. The algorithm is a [bucket queue](/bucket-queue/) in which keys only grow by 1.

## Properties

- **Not a BFS.** An MCS order need not visit the vertices by distance. On the chordal graph with the edges $\{0,1\}$, $\{0,2\}$, $\{0,4\}$, $\{1,2\}$, $\{1,3\}$, $\{2,3\}$, MCS visits $0, 1, 2, 3, 4$: vertex 3, at distance 2, has two visited neighbours and comes before vertex 4, at distance 1, which has one.
- **Weak four-point property.** If $a <_\sigma b <_\sigma c$, $ac \in E$ and $ab \notin E$, then there is $d <_\sigma b$ with $db \in E$ and $dc \notin E$. LexBFS gives the stronger $d <_\sigma a$.
- **Chordal graphs.** $G$ is chordal if and only if the reverse of one, or every, MCS order is a perfect elimination ordering. In particular, the last vertex of an MCS of a chordal graph is simplicial.
- **Clique sizes.** On a chordal graph, the weight of each vertex when it is visited is the size of its set of earlier neighbours, which is a clique. So the largest weight plus 1 is the size of a [maximum clique](/maximum-clique/).
- **Deterministic** once the tie-breaking rule is fixed, as in line L3.

## Variants and improvements

- **Hypergraphs.** Tarjan and Yannakakis also give a version for [hypergraphs](/hypergraph/) that alternately picks an edge with the most visited vertices and visits its vertices. It tests whether a hypergraph is acyclic in linear time.
- **MCS-M.** Berry, Blair, Heggernes and Peyton count a vertex $y$ as joined to $x$ also when a path through unvisited vertices of smaller weight joins them. This is not linear any more, $O(nm)$ time, but the edges that it adds give a minimal triangulation of any graph.
- **Clique trees.** Blair and Peyton show how to read the maximal cliques of a chordal graph, and a clique tree, which is a [tree decomposition](/tree-decomposition/), from the points of an MCS where the weight does not grow.
- **Lexicographic BFS.** [LexBFS](/lexicographic-bfs/) compares the sets of visited neighbours instead of their sizes. It has the same use for chordal graphs, and it is also a BFS, which the multi-sweep algorithms for interval graphs need.

## When to use it

Use MCS to test whether a graph is chordal and to get a perfect elimination ordering, for example before an optimal [colouring of a chordal graph](/chordal-graph-coloring/), before listing its [maximal cliques](/maximal-clique/), or before sparse [Gaussian elimination](/gaussian-elimination/) without fill-in. It is the simplest linear-time method for this, with an array of buckets and no partition refinement. As a heuristic [elimination ordering](/elimination-ordering/) for graphs that are not chordal, MCS and MCS-M are also used. When an algorithm needs a BFS order with LexBFS ties, as in interval graph recognition, use [lexicographic BFS](/lexicographic-bfs/) instead.

## Pitfalls

- **Counting all neighbours.** The weight counts only the visited neighbours. The degree in the whole graph gives a different order, which does not work.
- **Forgetting to lower $j$.** After a step, the largest bucket can be lower than $j + 1$, because the visited vertex left its bucket and few weights grew. Without line L8, the search reads an empty bucket.
- **Weights of visited vertices.** Line L5 must skip visited neighbours, or a visited vertex is put back into a bucket and visited twice.
- **Reading the order the wrong way.** The perfect elimination ordering is the *reverse* of the MCS order: the last visited vertex is eliminated first. Tarjan and Yannakakis number the vertices from $n$ down to 1 to avoid this.
- **Using MCS where LexBFS is needed.** Both orders work for chordality, but MCS is not a BFS order, and the algorithms that rely on properties of LexBFS orders do not work with it.

## Implementations

## History

Robert Tarjan and Mihalis Yannakakis introduced maximum cardinality search in 1984, as a simpler way than the lexicographic BFS of Rose, Tarjan and Lueker to test chordality, together with a version for the acyclicity of hypergraphs, which matters for relational database schemes. Blair and Peyton used MCS in their 1993 introduction to chordal graphs and clique trees for sparse matrix computation. Berry, Blair, Heggernes and Peyton extended it in 2004 to MCS-M, which computes minimal triangulations of any graph.

## References
