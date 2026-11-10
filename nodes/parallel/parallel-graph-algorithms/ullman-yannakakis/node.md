---
tag: BAM5EM
kind: algorithm
slug: ullman-yannakakis
name: Ullman-Yannakakis transitive closure
aliases:
- hopset-based transitive closure
area: parallel/parallel-graph-algorithms
level: research
summary: Randomized parallel transitive closure. Sample vertices, search to depth t from them, and close the paths among the samples; it uses less work than repeated squaring.
solves: [transitive-closure]
model: work-span-model
complexity:
  vars: {n: the number of vertices, m: the number of arcs, t: the search depth, s: the number of sampled vertices}
  time: {worst: O(n (n + m) + s^3 log s + n^2 s)}
  depth: {worst: O(t log n + log^2 n)}
  space: {extra: O(n^2)}
properties: {deterministic: false, recursive: false}
prereqs: [transitive-closure, reachability, parallel-bfs, boolean-matrix-multiplication, union-bound, work-span-model]
see_also: [hopset, multi-source-bfs, warshall-algorithm, apsp-repeated-squaring, forward-backward-scc, delta-stepping, frontier-based-processing, coloring-scc]
sources:
  - paper: doi:10.1137/0220006
    title: Jeffrey D. Ullman and Mihalis Yannakakis, High-probability parallel transitive-closure algorithms, SIAM Journal on Computing 20(1), 100 to 125 (1991)
    locator: the random choice of distinguished vertices, the depth-bounded searches from them, and the processor and time bounds for the dense, sparse and single-source cases; section numbers to be checked
  - paper: "Jeffrey D. Ullman and Mihalis Yannakakis, High-probability parallel transitive closure algorithms, SPAA 1990"
    title: High-probability parallel transitive closure algorithms
    locator: the conference version; pages to be checked
  - url: https://arxiv.org/abs/1711.01700
    title: Jeremy T. Fineman, Nearly work-efficient parallel algorithm for digraph reachability, STOC 2018 (arXiv 1711.01700)
    locator: Section 1 and Table 1, which state the single-source bounds of the method as work Õ(mρ + ρ^4/n) and span Õ(n/ρ) with high probability, after Schudy, and footnote 4
  - paper: "Warren Schudy, Finding strongly connected components in parallel using O(log^2 n) reachability queries, SPAA 2008"
    title: Finding strongly connected components in parallel using O(log^2 n) reachability queries
    locator: the improved work bound for the sampling method, as cited by Fineman; section to be checked
---

The Ullman-Yannakakis algorithm computes the transitive closure of a directed graph in parallel with fewer rounds than a breadth-first search and less work than repeated matrix squaring. It picks a random sample of vertices, about $c\, n \ln n / t$ of them, and runs a breadth-first search of depth $t$ from every vertex. With high probability, every long shortest path has a sampled vertex in every $t$ consecutive vertices, so long paths can be put together from short pieces between sampled vertices. The closure of the small graph on the sample is computed by path doubling, that is, by repeated Boolean squaring, and the pieces are joined in two more matrix steps.

Notation on this page: $G = (V, A)$ is a directed graph with $n$ vertices and $m$ arcs; "$u$ reaches $v$" means a path of zero or more arcs, so the closure here is reflexive. $t \ge 1$ is the search depth and $c > 0$ a constant; each vertex joins the sample $S$ with probability $p = \min(1, c \ln n / t)$, and $s = |S|$. $R(v)$ is the set of vertices at most $t$ arcs from $v$. $W$ is the work and $S$ the span, in the [work-span model](/work-span-model/). The bounds in the front matter are worst case for a given $s$; $E[s] = np$. The output is always a subset of the closure and is exact with probability at least $1 - n^{3 - c}$ (Monte Carlo). These facts are proved here; the single-source bounds are cited.

## In plain words

You want to know which towns can reach which other towns by one-way roads, and some routes are very long. First pick some towns at random to be stations. From every town, explore only the next few road steps.

If the stations are dense enough, every long route passes a station within every few steps. So a long route is a short walk to a station, a ride from station to station, and a short walk from the last station.

Station-to-station links form a much smaller map, and its full set of connections is cheap to find by doubling: two hops, then four, then eight. Joining the short walks with the station map gives every route.

## The problem

The input is a directed graph. The output is its [transitive closure](/transitive-closure/): for every pair $(u, v)$, whether $u$ reaches $v$. A search from every vertex gives the closure with $O(n(n + m))$ work, but in parallel each search needs as many rounds as its depth, up to $n - 1$. Path doubling, $\lceil \log_2 n \rceil$ Boolean squarings of the adjacency matrix, needs only $O(\log^2 n)$ span but $\Theta(n^3 \log n)$ work with the cubic product. The sampling method trades between these two extremes with the depth $t$.

## The algorithm

```pseudo id=main
ULLMAN-YANNAKAKIS(G, t, c)
L1  p ← min(1, c ln n / t); S ← each vertex independently with probability p
L2  for all v in V in parallel do R(v) ← the vertices at most t arcs from v      ▷ t BFS rounds
L3  for all a, b in S in parallel do H(a, b) ← [b ∈ R(a)]
L4  repeat ⌈log₂ |S|⌉ times
L5      H ← H ∨ H·H      ▷ Boolean product: path doubling on the sample only
L6  for all u in V in parallel do B(u) ← {b ∈ S : H(a, b) for some a ∈ S ∩ R(u)}
L7  for all u in V in parallel do C(u) ← R(u) ∪ the union of R(b) over b ∈ B(u)
L8  return C
```

$H$ is reflexive from the start, since $a \in R(a)$, so after line L5 it is the reflexive closure of the sample graph. Lines L6 and L7 are two Boolean matrix products. For one source $u$, only $R(u)$ and the searches from the sample are needed, which is the single-source form of the method.

## Example

The graph is the path $0 \to 1 \to \cdots \to 7$, with $t = 3$ and the sample $S = \{2, 5\}$. Then $R(2) = \{2, 3, 4, 5\}$ and $R(5) = \{5, 6, 7\}$, so $H$ has the arc $2 \to 5$, and one squaring gives $H^*$.

| $u$ | $R(u)$ (L2) | $S \cap R(u)$ | $B(u)$ (L6) | $C(u)$ (L7) |
|---|---|---|---|---|
| 0 | 0, 1, 2, 3 | 2 | 2, 5 | 0 to 7 |
| 1 | 1, 2, 3, 4 | 2 | 2, 5 | 1 to 7 |
| 3 | 3, 4, 5, 6 | 5 | 5 | 3 to 7 |
| 6 | 6, 7 | none | none | 6, 7 |

Every set of 3 consecutive vertices on the path contains 2 or 5, so the result is exact. With the sample $\{4\}$ instead, the window $0, 1, 2$ has no sampled vertex, and $C(0) = \{0, 1, 2, 3\}$ misses 4 to 7: the output is a subset of the closure, but not all of it.

## Correctness

The proof file proves, in full:

1. after $\lceil \log_2 s \rceil$ squarings, $H$ is the reflexive transitive closure of the sample graph;
2. every pair in the output is a true pair, for every sample;
3. if every $t$ consecutive vertices on a shortest path from $u$ to $v$ contain a sampled vertex, then $v \in C(u)$: the path is a piece of at most $t - 1$ arcs to the first sampled vertex, pieces of at most $t$ arcs between sampled vertices, and a last piece of at most $t - 1$ arcs;
4. a fixed window misses the sample with probability at most $(1 - p)^t \le n^{-c}$, and a union bound over fewer than $n^3$ windows gives exactness with probability at least $1 - n^{3 - c}$.

The same argument shows that the arcs of $H^*$, added to $G$, form a [hopset](/hopset/) for reachability: every pair that is connected is connected by a path of at most $2t - 1$ arcs. This is the sense of the alias "hopset-based transitive closure". The alias "path doubling" names the squaring step in line L5; plain path doubling on the whole graph is the extreme case $t = 1$, where $p = 1$ for $c \ln n \ge 1$.

## Complexity

**Proved bounds.** Line L2 runs $n$ searches of depth $t$ at once, $O(n(n + m))$ work and $O(t \log n)$ span. The squarings cost $O(s^3 \log s)$ work and $O(\log^2 n)$ span, and lines L6 and L7 cost $O(n^2 s)$ work and $O(\log n)$ span. So

$$W = O(n(n + m) + s^3 \log s + n^2 s), \qquad S = O(t \log n + \log^2 n),$$

with $E[s] \le c\, n \ln n / t$. For $t = \sqrt{n}$, the sample has about $c \sqrt{n} \ln n$ vertices, and the squarings cost $O(n^{3/2} \log^4 n)$ work.

**Cited bounds.** Fineman (2018, Table 1) states the single-source form, after the improvement by Schudy (2008), as work $\tilde O(m\rho + \rho^4/n)$ and span $\tilde O(n/\rho)$ with high probability, for a parameter $1 \le \rho \le n$ that plays the role of $n/t$. He notes that the work bound in the original paper is worse for small $\rho$. With $\rho = 1$ this is a parallel BFS, and with $\rho = n$ it is transitive closure by squaring.

**Measured.** On a directed path with $n/8$ extra random arcs, $t = \lceil 2\sqrt{n} \rceil$ and $c = 4$, the tests measure one run each:

| $n$ | $t$ | sample $s$ | $c\, n \ln n / t$ | BFS rounds | squarings | depth of one BFS from vertex 0 |
|---|---|---|---|---|---|---|
| 64 | 16 | 64 | 66.5 (so $p = 1$) | 16 | 6 | 35 |
| 256 | 32 | 180 | 177.4 | 32 | 8 | 58 |
| 1,024 | 64 | 467 | 443.6 | 64 | 9 | 90 |

The tests assert that the closure is exact, that the rounds are at most $t + \log_2 n + 1 \le 3\sqrt{n}$, and that $s$ is at most twice its mean.

## Properties

- **Monte Carlo, one-sided.** The output never contains a false pair. With a small probability it misses true pairs. The tests use $c = 0.3$ to check that no false pair appears even when pairs are missed.
- **A trade-off with one parameter.** A small $t$ gives a large sample and much matrix work; a large $t$ gives a small sample and long searches.
- **Only short searches.** No search goes deeper than $t$, whatever the diameter of the graph is.
- **Checkable.** Since the output is a subset of the closure, a result can be checked with a further step: the closure is exact exactly when $C$ is closed under one more arc of $G$.

## Variants and improvements

- **Single source.** Searches of depth $t$ from the source and from the sample, then the closure of the sample graph, give the vertices reachable from one source. This is the form compared with other methods in the literature on parallel reachability.
- **Breadth-first search.** Ullman and Yannakakis also show how to get BFS distances with the same performance as their single-source closure.
- **Shortcuts for reachability.** Fineman (2018) adds $\tilde O(n)$ shortcut arcs to reduce the diameter to $\tilde O(n^{2/3})$, which gives single-source reachability with nearly linear work.
- **Strongly connected components.** Schudy (2008) uses reachability queries of this kind for a parallel SCC algorithm; [FW-BW](/forward-backward-scc/) is the simplest method of this type.

## When to use it

Use it when a parallel transitive closure or reachability is needed on a graph with a large diameter, where breadth-first search has too many rounds and full matrix squaring has too much work. For dense graphs and small $n$, plain squaring with a fast Boolean matrix product is simpler; for graphs with a small diameter, a [multi-source BFS](/multi-source-bfs/) from every vertex is enough.

## Pitfalls

- **Too small a constant.** The bound $1 - n^{3 - c}$ is useful only for $c > 3$. With a small $c$, long paths miss the sample and pairs are lost without notice.
- **A non-reflexive sample graph.** If $H$ does not contain $a \to a$, the squaring forgets the shorter paths, and $B(u)$ misses the first sampled vertex itself.
- **Choosing the paths after the sample.** The union bound needs one path per pair that is fixed before the sample is drawn. An argument that picks a path that suits the sample does not give the bound.
- **Memory.** The output has $n^2$ bits, and $R(v)$ for all $v$ also takes $O(n^2)$ space. For single-source queries, keep only the searches from the sample.

## Implementations

## History

Ullman and Yannakakis presented the method at SPAA 1990 and in the SIAM Journal on Computing in 1991. They asked whether reachability can be solved in sublinear parallel time without losing work efficiency. Schudy (2008) improved the work bound and used it for strongly connected components. Fineman (2018) gave the first algorithm for digraph reachability with nearly linear work and a span of $\tilde O(n^{2/3})$.

## References
