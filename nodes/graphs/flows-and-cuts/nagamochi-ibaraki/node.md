---
tag: 6ZSTKE
kind: algorithm
slug: nagamochi-ibaraki
name: Nagamochi-Ibaraki algorithm
aliases:
- maximum adjacency ordering min cut
area: graphs/flows-and-cuts
level: research
summary: Deterministic min cut via maximum adjacency orderings and sparse certificates.
solves: [global-min-cut-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(n m log n)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
prereqs: [stoer-wagner, global-min-cut-problem, graph-contraction, edge-connectivity]
see_also: [karger-stein, karger-min-cut, hao-orlin, gomory-hu-tree, k-edge-connected-graph, fibonacci-heap, min-cut-problem]
sources:
  - paper: doi:10.1137/0405004
    title: Hiroshi Nagamochi and Toshihide Ibaraki, Computing edge-connectivity in multigraphs and capacitated graphs, SIAM Journal on Discrete Mathematics 5(1), 54 to 66 (1992)
    locator: the whole paper (the minimum cut algorithm by scan-first orderings and contraction, O(nm + n^2 log n) for capacitated graphs)
  - paper: doi:10.1007/BF01758778
    title: Hiroshi Nagamochi and Toshihide Ibaraki, A linear-time algorithm for finding a sparse k-connected spanning subgraph of a k-connected graph, Algorithmica 7, 583 to 596 (1992)
    locator: the whole paper (sparse certificates for k-edge-connectivity from one scan of the graph)
  - paper: doi:10.1145/263867.263872
    title: Mechthild Stoer and Frank Wagner, A simple min-cut algorithm, Journal of the ACM 44(4), 585 to 591 (1997)
    locator: the lemma that the last vertex of a maximum adjacency ordering gives a minimum cut between the last two vertices
---

The Nagamochi-Ibaraki algorithm finds a [global minimum cut](/global-min-cut-problem/) of an undirected graph with nonnegative weights deterministically and without flows. It was the first algorithm of this kind. Each round computes one *maximum adjacency* (MA) ordering, the same ordering that [Stoer-Wagner](/stoer-wagner/) uses, and reads from it a number $q(e)$ for every edge that is a lower bound on the connectivity between the ends of $e$. Every edge with $q(e)$ at least the best cut found so far can be [contracted](/graph-contraction/) at once, since no smaller cut separates its ends. A round costs $O(m \log n)$ with a binary heap or $O(m + n \log n)$ with a [Fibonacci heap](/fibonacci-heap/); there are at most $n - 1$ rounds, and often far fewer, because one round may contract many edges where Stoer-Wagner merges only one pair. The same scan gives the *sparse certificates* for $k$-edge-connectivity.

## In plain words

You want the cheapest way to cut a network into two parts. Keep the best cut you know; at the start, cutting off a single point.

Now list the points one by one, always taking next the point most strongly tied to those already listed. While listing, every link gets a score: how strongly its far end was tied to the listed points just after this link was counted. A fact about this listing says that the two ends of a link cannot be separated more cheaply than its score. So every link whose score is at least as high as your best cut joins points that the cheapest cut keeps together. Glue all of them, check the single points again, and repeat.

## The problem

The input is an undirected graph $G = (V, E)$ with $n \ge 2$ vertices, $m$ edges and weights $w(e) \ge 0$, integer or real. Parallel edges add up, self-loops are ignored, and edges of weight 0 are dropped. The graph may be disconnected; then the answer is 0. There is no source or sink and no direction. The output is a set $S$ with $\emptyset \ne S \subsetneq V$ of least cut weight $w(S, V \setminus S)$, written $\lambda(G)$. For vertices $x \ne y$, $\lambda(x, y)$ is the least weight of a cut that separates them.

## The algorithm

An MA ordering $v_1, \ldots, v_k$ of the current graph starts anywhere and always scans next an unscanned vertex $v$ with the largest $\mathrm{key}(v) = w(\{v_1, \ldots, v_{i-1}\}, v)$. When a vertex $u$ is scanned, each edge $e = \{u, v\}$ to an unscanned $v$ adds $w(e)$ to $\mathrm{key}(v)$, and $q(e)$ is the value of $\mathrm{key}(v)$ right after this addition.

```pseudo id=main
NAGAMOCHI-IBARAKI(G, w)
L1  β ← ∞; each vertex v starts as the group {v}
L2  while G has at least two vertices do
L3      for each vertex v: if its weighted degree d(v) < β then β ← d(v), S ← the group of v
L4      if β = 0 then leave the loop
L5      compute an MA ordering of G, and q(e) for every edge e
L6      contract every edge e with q(e) ≥ β; the group of a merged vertex is the union of the groups
L7  return β, S
```

The edge into the last vertex $v_k$ from the last of its neighbors to be scanned has $q(e) = d(v_k) \ge \beta$, so each round with $\beta > 0$ contracts at least one edge. Line L4 stops at once on a disconnected graph, whose components show up as vertices of degree 0 after enough contraction, or as a single vertex at the start.

## Example

The graph has the vertices $a, \ldots, f$; the triangles $abc$ and $def$ have edges of weight 2, and $c d$ and $b e$ have weight 1. The minimum cut is $\{a, b, c\}$, of weight 2.

**Round 1.** The degrees are 4, 5, 5, 5, 5, 4, so $\beta = 4$ with $S = \{a\}$. The MA ordering from $a$ is $a, b, c, e, d, f$. The values are $q(ab) = 2$, $q(ac) = 2$, $q(bc) = 4$, $q(be) = 1$, $q(cd) = 1$, $q(ed) = 3$, $q(ef) = 2$, $q(df) = 4$. The edges $bc$ and $df$ have $q \ge 4$ and are contracted.

**Round 2.** The vertices are $a$, $bc$, $e$, $df$, with degrees 4, 6, 5, 5, so $\beta$ stays 4. The ordering is $a, bc, e, df$, with $q(a, bc) = 4$, $q(bc, e) = 1$, $q(bc, df) = 1$, $q(e, df) = 5$. The edges $a$-$bc$ and $e$-$df$ are contracted.

**Round 3.** The vertices are $abc$ and $def$, each of degree 2, so $\beta = 2$ with $S = \{a, b, c\}$. The last edge has $q = 2 \ge \beta$ and is contracted, and the loop ends with one vertex.

The answer is 2 after 3 rounds, where Stoer-Wagner needs 5 phases on the same graph.

Edge cases. A disconnected graph has $\beta = 0$ in the first round in which a component is a single vertex, and line L4 stops. An edge of weight 0 is dropped. With $n = 2$, line L3 finds the cut at once.

## Correctness

The key lemma: for every edge $e = \{v_i, v_j\}$ with $i < j$ in an MA ordering, $q(e) \le \lambda(v_i, v_j)$. The reason is that $v_1, \ldots, v_i, v_j$ is an MA ordering of the subgraph induced by these vertices: when $v_l$ with $l \le i$ was scanned it beat $v_j$, and keys depend only on earlier vertices. By the Stoer-Wagner lemma, the last vertex of an MA ordering is cut off by a minimum cut between the last two vertices, so in that subgraph $\lambda(v_i, v_j)$ equals the degree of $v_j$, which is $q(e)$. A subgraph has no larger connectivity, so $q(e) \le \lambda_G(v_i, v_j)$.

So if $q(e) \ge \beta$, every cut of weight below $\beta$ keeps the ends of $e$ together, and contracting $e$ keeps all such cuts. Since $\beta$ is always the weight of a real cut, either $\beta = \lambda(G)$ already, or a cut of weight below $\beta$ survives every contraction until a later round finds it as a vertex degree. The proof file below gives the details.

## Complexity

The model is the [word RAM](/word-ram/); weights fit in a word.

- **One round.** An MA ordering is like [Prim's algorithm](/prim/) with a max-heap of keys: $O(m \log n)$ with a binary heap, as in the implementation, or $O(m + n \log n)$ with a Fibonacci heap, since keys only increase. For integer weights, buckets give $O(m + n)$ in the unweighted case. Line L3 and the contraction take $O(n + m)$.
- **Rounds.** Each round removes at least one vertex, so there are at most $n - 1$ rounds.
- **Total.** $O(nm \log n)$ with a binary heap, $O(nm + n^2 \log n)$ with a Fibonacci heap, and $O(nm)$ for unweighted multigraphs. Space is $\Theta(n + m)$.

## Properties

- **Deterministic and exact.** No randomness, no flows.
- **Real weights.** Only additions and comparisons are used.
- **Many contractions per round.** In practice the number of rounds is often much smaller than $n$, which is why this method, with further reduction rules, is the basis of fast practical minimum cut solvers.
- **Sparse certificates.** For an unweighted graph and an integer $k$, the edges with $q(e) \le k$ form a subgraph with at most $k(n - 1)$ edges that keeps every cut of size up to $k$; it is computed in linear time.
- **Undirected only.** The MA ordering lemma fails for directed graphs.

## Variants and improvements

- **Stoer-Wagner.** Contract only the last two vertices of each ordering, which gives a shorter proof and the same worst-case bound: [Stoer-Wagner](/stoer-wagner/).
- **Sparse certificates first.** Before any flow-based connectivity test, replace the graph by a $k$-certificate with $O(kn)$ edges; this speeds up [$k$-edge-connectivity](/k-edge-connected-graph/) tests.
- **Randomized.** [Karger-Stein](/karger-stein/) takes $O(n^2 \log^3 n)$, and later near-linear algorithms beat both on sparse graphs.
- **Directed graphs.** The directed global minimum cut needs flows: [Hao-Orlin](/hao-orlin/).

## When to use it

Use it for exact global minimum cuts of undirected weighted graphs, especially large sparse ones in practice, where the many contractions per round pay off. It is also the standard way to compute sparse certificates of edge-connectivity. For a short implementation with the same worst-case bound, Stoer-Wagner is simpler.

## Pitfalls

- **Contracting edges with $q(e) < \beta$.** Only edges whose bound reaches the current best cut may be contracted; a smaller cut may separate the others.
- **Taking $q(e)$ at the wrong time.** $q(e)$ is the key of the later end right after $e$ is added, not the final key of that vertex; the final key can be larger and is not a valid bound.
- **Forgetting the degree cuts.** The bound $\beta$ must come from cuts that were actually seen; line L3 looks at all vertex degrees in every round, including the degree of the last vertex of the ordering.
- **Ties in the ordering.** Any vertex of largest key may be chosen; the lemma holds for every such choice, so ties need no special rule.
- **Disconnected input.** Without the check at line L4, a round with $\beta = 0$ contracts every edge with $q \ge 0$, which is correct but wasteful; stopping early is simpler.

## Implementations

## History

Nagamochi and Ibaraki gave the first sparse certificate method for $k$-edge-connectivity and, in the same year, 1992, the first deterministic minimum cut algorithm for capacitated undirected graphs that does not use flows. Stoer and Wagner, and independently Frank, gave simpler proofs of the key lemma around 1994. Later work added reduction rules that make the method practical on very large graphs.

## References
