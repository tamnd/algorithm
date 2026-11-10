---
tag: N8D9ER
kind: algorithm
slug: baker-planar-ptas
name: Baker's PTAS for planar graph problems
aliases:
- Baker's algorithm
- planar PTAS
- Baker's scheme for planar independent set
area: approximation/approximation-schemes
level: advanced
summary: Layering plus bounded-treewidth dynamic programming gives a PTAS for maximum independent set, vertex cover and dominating set on planar graphs.
solves: [maximum-independent-set, vertex-cover]
model: word-ram
complexity:
  vars: {n: the number of vertices, k: the layer period, c: an absolute constant}
  time: {worst: "O(c^k n)", average: "O(c^k n)", best: "O(c^k n)"}
  space: {extra: "O(c^k n)"}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1994
  people: [Brenda S. Baker]
  note: Baker gave linear-time approximation schemes for many NP-complete problems on planar graphs; a conference version appeared at FOCS 1983.
prereqs: [baker-technique, planar-graph, bfs-layers, tree-decomposition, maximum-independent-set, vertex-cover]
see_also: [shifting-technique, outerplanar-graph, treewidth, elimination-ordering, planar-separator-theorem, lipton-tarjan-separator, dominating-set, eptas]
sources:
  - paper: "B. S. Baker, Approximation algorithms for NP-complete problems on planar graphs, Journal of the ACM 41(1), 1994, pp. 153-180"
    title: Baker 1994
    locator: the scheme for maximum independent set, the k-outerplanar pieces and the list of other problems
  - paper: "H. L. Bodlaender, A partial k-arboretum of graphs with bounded treewidth, Theoretical Computer Science 209(1-2), 1998, pp. 1-45"
    title: Bodlaender 1998
    locator: treewidth at most 3k - 1 for k-outerplanar graphs
  - paper: "H. L. Bodlaender, A linear-time algorithm for finding tree-decompositions of small treewidth, SIAM Journal on Computing 25(6), 1996, pp. 1305-1317"
    title: Bodlaender 1996
    locator: the main theorem, a tree decomposition of width at most w in linear time for each fixed w
  - paper: "N. Robertson and P. D. Seymour, Graph minors. III. Planar tree-width, Journal of Combinatorial Theory, Series B 36(1), 1984, pp. 49-64"
    title: Robertson and Seymour 1984
    locator: the bound on the treewidth of a planar graph in terms of its radius
  - paper: "R. J. Lipton and R. E. Tarjan, Applications of a planar separator theorem, SIAM Journal on Computing 9(3), 1980, pp. 615-627"
    title: Lipton and Tarjan 1980
    locator: the earlier approximation scheme for planar independent set by separators
---

Baker's algorithm (1983, journal version 1994) is a [PTAS](/ptas/) for [maximum independent set](/maximum-independent-set/) and [minimum vertex cover](/vertex-cover/) on [planar graphs](/planar-graph/), and the same method works for dominating set and many other problems. For an integer $k$, it splits the graph into levels, deletes (or doubles) one class of levels modulo $k$, solves each remaining band of fewer than $k$ levels exactly by dynamic programming over a tree decomposition, and keeps the best of the $k$ classes. It returns an independent set of size at least $(1 - 1/k)\,\mathrm{OPT}$ and a vertex cover of size at most $(1 + 1/k)\,\mathrm{OPT}$, in time $2^{O(k)} n$. With $k = \lceil 1/\varepsilon \rceil$ this is linear for each fixed $\varepsilon$, and in fact an [EPTAS](/eptas/). The general method is on [Baker's technique](/baker-technique/); this page gives the algorithm with the dynamic program and its full proof.

## In plain words

Draw a planar graph like an onion, in rings around a start vertex. Every line of the graph stays in one ring or goes to the next ring.

To find many vertices with no line between them, remove every tenth ring, for example. The rest falls apart into thick bands with no lines between them. A band of a planar graph is thin: it can be cut into small overlapping pieces arranged like a tree. A table over these pieces finds the best answer in a band exactly. The union of the band answers is a valid answer for the whole graph.

The removed rings may hold some of the best answer. There are ten ways to choose which rings to remove, and they remove different vertices, so one of them loses at most a tenth. Try all ten ways and keep the best.

## The problem

The input is a planar graph $G = (V, E)$ with $n$ vertices and an integer $k \ge 1$ (or an accuracy $\varepsilon$, with $k = \lceil 1/\varepsilon \rceil$). For independent set, the output is a set of pairwise non-adjacent vertices, and $\mathrm{OPT}$ is the largest such size. For vertex cover, the output is a set that meets every edge, and $\mathrm{OPT}$ is the least such size. Both problems are NP-hard on planar graphs.

*Ratio convention.* Independent set is a maximization problem: $\mathrm{ALG} \ge (1 - 1/k)\,\mathrm{OPT}$. Vertex cover is a minimization problem: $\mathrm{ALG} \le (1 + 1/k)\,\mathrm{OPT}$. Both ratios are absolute. The proof does not use a numeric lower bound on $\mathrm{OPT}$; it compares each band with the part of a fixed optimum inside the band.

*Levels.* The level $\ell(v)$ is the breadth-first distance from a root (one root per component). Baker uses outerplanarity levels instead, where level 1 is the outer face, level 2 the outer face after deleting level 1, and so on; the proof below needs only that every edge joins equal or adjacent levels, which holds for both.

## The algorithm

```pseudo id=main
BAKER-IS(G, k)
L1  compute the breadth-first level ℓ(v) of each vertex
L2  for r ← 0 to k − 1
L3      delete the vertices with ℓ(v) ≡ r (mod k)
L4      group the other vertices into bands by ⌊(ℓ(v) − r)/k⌋
        for each band U:
L5          find an elimination order of G[U]; S_v ← the later neighbours of v when v is removed
L6          for v in elimination order, for each independent T ⊆ S_v:
                f_v(T) ← max over x ∈ {0, 1} (x = 1 only if v has no neighbour in T)
                         of x + Σ over children c of v of f_c((T ∪ {v if x = 1}) ∩ S_c)
L7          walk the order backwards and take v when the best choice for (v, chosen part of S_v) is x = 1
L8          add the chosen vertices to S_r
L9  keep the largest S_r
L10 return it
```

The *children* of $v$ are the vertices $c$ for which $v$ is the first-removed vertex of $S_c$. The sets $\{v\} \cup S_v$ are the bags of a tree decomposition, and $\max_v |S_v|$ is its width. For vertex cover, the loop uses for each $r$ the pieces of the $k + 1$ levels $r + jk, \ldots, r + (j+1)k$, which overlap in the levels $\equiv r \pmod k$, and takes the complement of a maximum independent set in each piece.

## Example

Take the $4 \times 4$ grid with vertices $0, \ldots, 15$ in rows, the grid edges, and the down-right diagonal of each cell. From root 0 the level of the vertex in row $i$ and column $j$ is $\max(i, j)$, so the levels have $1, 3, 5, 7$ vertices. The optimum independent set has 6 vertices. With $k = 2$:

| offset $r$ | deleted levels | bands | band optima | $\lvert S_r \rvert$ |
|---|---|---|---|---|
| 0 | 0 and 2 | level 1: $\{1, 4, 5\}$; level 3: $\{3, 7, 11, 12, 13, 14, 15\}$ | $\{1, 4\}$; $\{3, 11, 12, 14\}$ | 6 |
| 1 | 1 and 3 | level 0: $\{0\}$; level 2: $\{2, 6, 8, 9, 10\}$ | $\{0\}$; $\{2, 8, 10\}$ | 4 |

Each band here is a path, so the elimination order has width 1, and the tables of both offsets hold 28 entries in all. Offset 0 returns $\{1, 3, 4, 11, 12, 14\}$, which is optimal; the bound promises only $(1 - \frac12) \cdot 6 = 3$. For vertex cover with $k = 2$, offset 0 gives pieces of levels $\{0\}$, $\{0, 1, 2\}$ and $\{2, 3\}$ and a cover of size 12, and offset 1 gives pieces of levels $\{0, 1\}$, $\{1, 2, 3\}$ and $\{3\}$ and a cover of size 10, which is optimal ($16 - 6$).

## Correctness

The proof has three parts.

1. **The dynamic program is exact.** In an elimination order, every later neighbour of $v$ is an ancestor of $v$ in the forest of parents. So the vertices of the subtree $D_v$ of $v$ have edges to the outside only into $S_v$, and different child subtrees have no edges between them. The recurrence of line L6 is then the exact optimum of $D_v$ for each fixed choice $T$ on $S_v$.
2. **Bands combine.** Every edge joins equal or adjacent levels. Kept vertices in different bands have a deleted level between them, so the union of independent sets of the bands is independent. For vertex cover every edge lies in some piece.
3. **One offset loses little.** The classes $\ell \equiv r$ partition a fixed optimum, so for some $r$ the class holds at most $\mathrm{OPT}/k$ of its vertices. Deleting that class (or doubling it) costs at most $\mathrm{OPT}/k$.

The full proof is below.

## Complexity

- **Time.** Breadth-first search costs $O(n)$. For each of the $k$ offsets, the bands are disjoint, and a band of a planar graph has treewidth $O(k)$: a $k$-outerplanar graph has treewidth at most $3k - 1$ (Bodlaender 1998), and a band of breadth-first levels becomes a graph of radius at most $k$ after contracting the inner levels. A tree decomposition of width $w$ gives tables of $2^{w}$ entries per vertex, so the dynamic program costs $O(2^{w} w^2)$ per vertex and the total is $2^{O(k)} n$. With $k = \lceil 1/\varepsilon \rceil$ this is $2^{O(1/\varepsilon)} n$.
- **Space.** The tables of one band, $O(2^{w} n)$ entries.
- **The code.** The implementation uses the minimum-degree elimination heuristic, which is exact for the dynamic program but does not guarantee width $O(k)$. A guaranteed decomposition comes from Baker's construction for $k$-outerplanar graphs or from Bodlaender's linear-time algorithm for fixed width.

## Properties

| claim | statement | status |
|---|---|---|
| independent set | $\mathrm{ALG} \ge (1 - 1/k)\,\mathrm{OPT}$ | proved below |
| vertex cover | $\mathrm{ALG} \le (1 + 1/k)\,\mathrm{OPT}$ | proved below |
| exact bands | the dynamic program returns a maximum independent set of each band | proved below |
| time | $2^{O(k)} n$ on planar graphs | proved below, with the cited treewidth bounds |
| treewidth of $k$-outerplanar graphs | at most $3k - 1$ | cited (Bodlaender 1998) |
| no FPTAS | independent set on planar graphs is strongly NP-hard, so no FPTAS exists unless P = NP | standard |

## Variants and improvements

- **Other problems.** Baker's paper treats minimum dominating set, minimum edge dominating set, partition into triangles, maximum matchings of a fixed small graph and others, with the same layering and problem-specific dynamic programs.
- **Separators.** The earlier scheme of Lipton and Tarjan (1980) used the [planar separator theorem](/planar-separator-theorem/) recursively and gave ratio $1 - O(1/\sqrt{\log \log n})$ in $O(n \log n)$ time. Baker's layering gives a constant ratio $1 - 1/k$ in linear time.
- **Bounded local treewidth.** Eppstein (2000) showed that the scheme works on every minor-closed family in which treewidth is bounded by a function of the diameter, that is, the apex-minor-free families.
- **Contraction and edge problems.** For connectivity problems such as TSP and [Steiner tree](/steiner-tree-problem/), deleting vertices breaks feasibility. Klein and others contract the edges of one class of levels instead, after first building a spanner whose weight is $O(\mathrm{OPT})$; see the [planar Steiner tree scheme](/planar-steiner-tree-ptas/).

## When to use it

Use Baker's scheme as the standard way to prove that a local problem on planar graphs has a PTAS or an EPTAS. In practice, $k$ must stay small because of the $2^{3k}$ factor; for $k = 2$ or 3 it gives guarantees of $\frac12$ or $\frac23$ of the optimum for independent set with a practical running time. For larger instances with good structure, exact solvers on tree decompositions of the whole graph, or local search, often perform better.

## Pitfalls

- **Deleting levels for a covering problem.** For vertex cover or dominating set, deleted levels leave edges or vertices unhandled. The pieces must overlap, and the shared level is counted twice in the analysis.
- **Local levels.** The levels must come from breadth-first search (or outerplanarity), so that edges join only equal or adjacent levels. Depth-first levels or weighted distances do not work.
- **Heuristic decompositions.** An elimination heuristic gives a correct dynamic program, but its width can exceed $O(k)$ on some graphs, and then the time bound is lost.
- **Weights.** The scheme works for vertex weights, with the same proof, if the dynamic program maximizes weight instead of size.
- **Non-planar inputs.** On general graphs a band can contain any graph, and independent set has no constant-factor approximation unless P = NP.

## Implementations

## History

Brenda Baker presented the scheme at FOCS 1983, and the journal version appeared in 1994. It followed the separator-based scheme of Lipton and Tarjan (1980) and gave the first linear-time approximation schemes for a long list of planar problems. Bodlaender (1998) proved that $k$-outerplanar graphs have treewidth at most $3k - 1$, which makes the dynamic programming step a special case of dynamic programming on tree decompositions. Eppstein (2000) extended the scheme to families with bounded local treewidth, and Demaine and Hajiaghayi (2005) linked it to bidimensionality.

## References
