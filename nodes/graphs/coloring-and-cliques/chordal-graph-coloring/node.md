---
tag: JWQZ4N
kind: algorithm
slug: chordal-graph-coloring
name: Coloring chordal graphs
aliases:
- perfect elimination coloring
area: graphs/coloring-and-cliques
level: core
summary: Greedy coloring in reverse perfect elimination order is optimal for chordal graphs.
solves: [graph-coloring]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m), best: Θ(n + m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
prereqs: [chordal-graph, perfect-elimination-ordering, maximum-cardinality-search, greedy-coloring]
see_also: [chordal-graph, perfect-elimination-ordering, maximum-cardinality-search, lexicographic-bfs, perfect-graph, greedy-coloring, interval-partitioning, certifying-algorithms]
sources:
  - paper: doi:10.1137/0201013
    title: Fănică Gavril, Algorithms for minimum coloring, maximum clique, minimum covering by cliques, and maximum independent set of a chordal graph, SIAM Journal on Computing 1(2), 180 to 187 (1972)
    locator: the whole paper (coloring and maximum clique from a perfect elimination ordering)
  - paper: doi:10.1137/0213035
    title: Robert E. Tarjan and Mihalis Yannakakis, Simple linear-time algorithms to test chordality of graphs, test acyclicity of hypergraphs, and selectively reduce acyclic hypergraphs, SIAM Journal on Computing 13(3), 566 to 579 (1984)
    locator: maximum cardinality search, the proof that its reverse order is a perfect elimination ordering of a chordal graph, and the linear-time check of the order
  - paper: doi:10.1137/0205021
    title: Donald J. Rose, R. Endre Tarjan and George S. Lueker, Algorithmic aspects of vertex elimination on graphs, SIAM Journal on Computing 5(2), 266 to 283 (1976)
    locator: the linear-time test whether an order is a perfect elimination ordering (each vertex against its first later neighbor)
  - book: isbn:9780444515308
    title: Martin Charles Golumbic, Algorithmic Graph Theory and Perfect Graphs, second edition, Annals of Discrete Mathematics 57, Elsevier, 2004
    locator: Chapter 4, Triangulated graphs (perfect elimination orderings, recognition, and the optimization algorithms of Gavril)
---

A [chordal graph](/chordal-graph/) has a [perfect elimination ordering](/perfect-elimination-ordering/): an order of its vertices in which the later neighbors of each vertex form a clique. [Greedy coloring](/greedy-coloring/) in the reverse of such an order is optimal: when a vertex is colored, its colored neighbors form a clique, so the number of colors used never exceeds the clique number $\omega(G)$, which is a lower bound. This page finds the order with [maximum cardinality search](/maximum-cardinality-search/), checks it in linear time, and colors; the whole algorithm takes $\Theta(n + m)$ time and either returns an optimal coloring or reports that the graph is not chordal.

## In plain words

Visit the points of a network one at a time, always choosing next a point with as many already visited neighbors as possible. If the network is chordal, every point meets, at its visit, a group of visited neighbors who all know each other.

Color the points in the order of the visit, each with the first color its visited neighbors do not use. Those neighbors all know each other, so they already need different colors, and the new point needs just one more. The largest such group plus the new point is a tight group of the network, and every coloring needs that many colors. So the result is the best possible.

## The problem

The input is a simple undirected graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$, as adjacency lists. The output is a proper coloring $c : V \to \{1, \ldots, \chi(G)\}$ if $G$ is chordal, and the answer NOT CHORDAL otherwise. Graph coloring is NP-hard in general; on chordal graphs, which are [perfect](/perfect-graph/), it is solvable in linear time.

## The algorithm

```pseudo id=main
CHORDAL-COLOR(G)
L1  σ ← MAXIMUM-CARDINALITY-SEARCH(G), pos[v] ← the index of v in σ
L2  for each vertex v in the order σ do
L3      Earlier(v) ← {w ∈ N(v) : pos[w] < pos[v]}
L4      if Earlier(v) ≠ ∅ then p(v) ← the w ∈ Earlier(v) with the largest pos[w]; ask that Earlier(v) \ {p(v)} ⊆ N(p(v))
L5  check all requests of line L4, one vertex u = p(v) at a time with N(u) marked; if one fails then return NOT CHORDAL
L6  for each vertex v in the order σ do
L7      c[v] ← the smallest k ≥ 1 with k ≠ c[w] for all w ∈ Earlier(v)
L8  return c
```

Maximum cardinality search (Tarjan and Yannakakis) visits next a vertex with the most visited neighbors, with buckets indexed by that number. The reverse of the visit order $\sigma$ is the candidate perfect elimination ordering, so $\mathrm{Earlier}(v)$, the neighbors visited before $v$, are the later neighbors of $v$ in that ordering. Lines L2 to L5 are the test of Rose, Tarjan and Lueker: it only checks each set against one vertex, $p(v)$, and this is enough. Line L7 is greedy coloring in the visit order.

## Example

The graph has the vertices $0, \ldots, 6$ and the 12 edges $01, 02, 12, 13, 23, 24, 34, 35, 45, 26, 36, 46$: the strip of triangles $\{0,1,2\}$, $\{1,2,3\}$, $\{2,3,4\}$, $\{3,4,5\}$ and a vertex 6 joined to 2, 3 and 4. Maximum cardinality search breaks ties by taking the vertex that entered its bucket last, and vertex 6 is taken first.

| step | visited counts of unvisited vertices before the step | visited $v$ | Earlier$(v)$ | $p(v)$ | color |
|---|---|---|---|---|---|
| 1 | all 0 | 6 | {} | | 1 |
| 2 | 2:1, 3:1, 4:1, others 0 | 4 | {6} | 6 | 2 |
| 3 | 2:2, 3:2, 5:1, others 0 | 3 | {6, 4} | 4 | 3 |
| 4 | 2:3, 5:2, 1:1, 0:0 | 2 | {6, 4, 3} | 3 | 4 |
| 5 | 1:2, 5:2, 0:1 | 1 | {3, 2} | 2 | 1 |
| 6 | 0:2, 5:2 | 0 | {2, 1} | 1 | 2 |
| 7 | 5:2 | 5 | {4, 3} | 3 | 1 |

The requests of line L4 are $6 \in N(4)$, $\{6, 4\} \subseteq N(3)$, $3 \in N(2)$, $2 \in N(1)$ and $4 \in N(3)$, and all hold, so the graph is chordal. The coloring is $c = (2, 1, 4, 3, 2, 1, 1)$ for the vertices $0, \ldots, 6$, with 4 colors. It is optimal, because $\{2, 3, 4, 6\}$ is a clique: it is $\{2\} \cup \mathrm{Earlier}(2)$.

**A graph that is not chordal.** Take the strip $01, 02, 12, 13, 23, 24, 34, 35, 45$ with a vertex 6 and the edges $06$ and $56$. The search visits $6, 5, 4, 3, 2, 1, 0$. For $v = 0$, $\mathrm{Earlier}(0) = \{1, 2, 6\}$ and $p(0) = 1$, and line L5 finds that $6 \notin N(1)$. The answer is NOT CHORDAL; indeed $0, 2, 4, 5, 6$ is an induced 5-cycle.

## Correctness

**Theorem.** CHORDAL-COLOR returns NOT CHORDAL exactly when $G$ is not chordal. Otherwise it returns a proper coloring with $\omega(G) = \chi(G)$ colors.

Three facts combine. (1) If $G$ is chordal, the reverse of a maximum cardinality search order is a perfect elimination ordering (Tarjan and Yannakakis 1984). (2) An order is a perfect elimination ordering if and only if, for each $v$, $\mathrm{Earlier}(v) \setminus \{p(v)\} \subseteq N(p(v))$ (Rose, Tarjan and Lueker): by induction from the end of $\sigma$, $p(v)$ has all of $\mathrm{Earlier}(v) \setminus \{p(v)\}$ in its own $\mathrm{Earlier}$ set, which is a clique, so $\mathrm{Earlier}(v)$ is a clique. (3) A graph with a perfect elimination ordering is chordal. So line L5 fails exactly when $G$ is not chordal. If it passes, each $\mathrm{Earlier}(v)$ is a clique; its vertices have distinct colors, and greedy gives $v$ a color at most $|\mathrm{Earlier}(v)| + 1$, the size of the clique $\{v\} \cup \mathrm{Earlier}(v)$. So the number of colors is at most $\omega(G) \le \chi(G)$. The full proof is below.

## Complexity

The cost is in the [word RAM](/word-ram/) model, with adjacency lists.

- Line L1: maximum cardinality search with buckets runs in $\Theta(n + m)$ time, like the [smallest-last ordering](/degeneracy-ordering/): the maximum bucket index rises by at most 1 per step, so the scans of empty buckets cost $O(n)$ in total.
- Lines L2 to L4 scan each adjacency list once and record at most $\sum_v |\mathrm{Earlier}(v)| \le m$ requests.
- Line L5 marks $N(u)$ for each $u$ and tests its requests in $O(1)$ each: $O(n + m)$.
- Lines L6 and L7 are greedy coloring with a time-stamped array: $O(n + m)$.

The time is $\Theta(n + m)$ and the extra space is $\Theta(n + m)$ for the sets $\mathrm{Earlier}(v)$ and the requests.

## Properties

- **Certifying.** A YES answer comes with the coloring and the clique $\{v\} \cup \mathrm{Earlier}(v)$ of the vertex with the largest color, which proves optimality. A NO answer comes with a failed request $w \notin N(p(v))$; Tarjan and Yannakakis show how to extract an induced cycle of length at least 4 from it, so the algorithm can be made a full [certifying algorithm](/certifying-algorithms/).
- **Any perfect elimination ordering works.** Greedy coloring in the reverse of any perfect elimination ordering is optimal; [lexicographic BFS](/lexicographic-bfs/) gives one as well.
- **Maximum clique for free.** $\omega(G) = \max_v |\mathrm{Earlier}(v)| + 1$, and the maximal cliques are among the $n$ sets $\{v\} \cup \mathrm{Earlier}(v)$.
- **Interval graphs.** For intervals sorted by left end, the visit order of the left ends is a reverse perfect elimination ordering, and this algorithm becomes [interval partitioning](/interval-partitioning/).

## Variants and improvements

- **Lexicographic BFS.** Rose, Tarjan and Lueker use [lexicographic BFS](/lexicographic-bfs/) with partition refinement in place of maximum cardinality search, with the same check and the same time.
- **Weighted problems.** Gavril (1972) also gives maximum weight clique, maximum independent set and minimum [clique cover](/clique-cover/) from a perfect elimination ordering, all in linear time.
- **Coloring perfect graphs in general.** All perfect graphs can be colored in polynomial time with the ellipsoid method and the Lovász theta function (Grötschel, Lovász and Schrijver), but no combinatorial polynomial algorithm is known for the whole class.
- **Near-chordal graphs.** For a graph that is not chordal, a chordal supergraph (a triangulation) gives a coloring with $\omega$ of the supergraph colors; minimizing that over triangulations is the [treewidth](/treewidth/) problem, which is NP-hard.

## When to use it

Use it when the graph is known or expected to be chordal: interval and register-interference graphs of programs in SSA form, conflict graphs of tasks on a tree, and graphs of sparse matrix elimination. Since it also tests chordality, it can be run first on any graph, and falls back to a heuristic such as [DSATUR](/dsatur/) when the answer is NOT CHORDAL.

## Pitfalls

- **Coloring in the wrong direction.** Greedy in the perfect elimination ordering itself, not reversed, is not optimal: a vertex's colored neighbors are then the earlier ones in the ordering, which need not form a clique. On the path $0 - 1 - 2 - 3$ with the perfect elimination ordering $0, 3, 1, 2$, it gives $0 \mapsto 1$, $3 \mapsto 1$, $1 \mapsto 2$, $2 \mapsto 3$: three colors for a bipartite graph.
- **Skipping the check.** On a graph that is not chordal, maximum cardinality search still returns an order, and greedy still returns a proper coloring, but it need not be optimal. Without line L5 the algorithm silently gives a wrong claim of optimality.
- **Choosing the wrong $p(v)$.** The test of line L4 uses the neighbor visited last before $v$. Testing against another vertex of $\mathrm{Earlier}(v)$ does not prove that $\mathrm{Earlier}(v)$ is a clique in linear time.
- **Plain BFS or DFS orders.** Ordinary breadth-first or depth-first search orders are not perfect elimination orderings of chordal graphs in general. The search must prefer vertices with many visited neighbors (maximum cardinality search) or lexicographically largest labels (lexicographic BFS).

## Implementations

## History

Fulkerson and Gross (1965) characterized chordal graphs by perfect elimination orderings. Gavril (1972) showed how to find a minimum coloring, a maximum clique, a minimum clique cover and a maximum independent set of a chordal graph from such an ordering. Rose, Tarjan and Lueker (1976) gave the first linear-time recognition, with lexicographic BFS and the linear check of the ordering, and Tarjan and Yannakakis (1984) gave the simpler maximum cardinality search.

## References
