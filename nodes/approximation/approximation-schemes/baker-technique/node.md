---
tag: 2A03SS
kind: technique
slug: baker-technique
name: Baker's technique (layering)
aliases:
- Baker's layering technique
- k-outerplanar decomposition
- layering technique
area: approximation/approximation-schemes
level: advanced
summary: Decompose a planar graph into k-outerplanar layers, solve each bounded-treewidth piece exactly, and combine them for a PTAS.
prereqs: [planar-graph, bfs-layers, treewidth, ptas, shifting-technique]
see_also: [baker-planar-ptas, outerplanar-graph, tree-decomposition, planar-separator-theorem, maximum-independent-set, vertex-cover, dominating-set, planar-steiner-tree-ptas]
sources:
  - paper: "B. S. Baker, Approximation algorithms for NP-complete problems on planar graphs, Journal of the ACM 41(1), 1994, pp. 153-180"
    title: Baker 1994
    locator: the decomposition into k-outerplanar pieces, the choice of the deleted levels and the list of problems
  - paper: "H. L. Bodlaender, A partial k-arboretum of graphs with bounded treewidth, Theoretical Computer Science 209(1-2), 1998, pp. 1-45"
    title: Bodlaender 1998
    locator: the bound treewidth at most 3k - 1 for k-outerplanar graphs
  - paper: "D. Eppstein, Diameter and treewidth in minor-closed graph families, Algorithmica 27(3-4), 2000, pp. 275-291"
    title: Eppstein 2000
    locator: treewidth bounded by a function of the diameter, and the layering with breadth-first levels in minor-closed families
  - paper: "E. D. Demaine and M. Hajiaghayi, Bidimensionality: new connections between FPT algorithms and PTASs, SODA 2005, pp. 590-601"
    title: Demaine and Hajiaghayi 2005
    locator: the extension of layering schemes beyond planar graphs
---

Baker's technique (1994) gives approximation schemes for many NP-hard problems on [planar graphs](/planar-graph/). Split the vertices into levels, by breadth-first search or by peeling the outer face again and again. Every edge joins two vertices of the same level or of adjacent levels. Delete every $k$-th level, starting at one of $k$ offsets. What remains falls apart into bands of fewer than $k$ consecutive levels, and in a planar graph such a band has [treewidth](/treewidth/) $O(k)$, so it can be solved exactly by dynamic programming. The $k$ offsets delete disjoint vertex sets, so one offset deletes at most a $1/k$ part of the optimum. For maximum independent set this gives $(1 - 1/k)\,\mathrm{OPT}$ in time $2^{O(k)} n$. It is the graph form of the [shifting technique](/shifting-technique/) of Hochbaum and Maass. The full algorithm, with the dynamic program, is on [Baker's planar PTAS](/baker-planar-ptas/).

## In plain words

A planar graph can be drawn like an onion, in rings around a centre. Each line of the drawing stays inside one ring or goes to the next ring, never further.

Pick a whole number, say ten, and remove every tenth ring. The graph then breaks into thick bands with no lines between them. Each band is thin in a precise sense, so a careful search solves it exactly and fast. Combine the answers of the bands.

Removing rings throws away part of the best answer. But there are ten ways to choose which rings to remove, and they remove different vertices. So at least one way throws away at most a tenth of the best answer. Try all ten ways and keep the best. A larger number gives a better answer and a slower search.

## When it applies

The technique needs four things.

- **A layering with local edges.** A partition of the vertices into levels $L_0, L_1, \ldots$ in which every edge joins equal or adjacent levels. Breadth-first levels from a root (in each component) have this property in every graph. Baker uses outerplanarity levels: $L_0$ is the outer face, $L_1$ the outer face after deleting $L_0$, and so on.
- **Thin bands are easy.** A band of $k$ consecutive levels of a planar graph has treewidth $O(k)$. For outerplanarity levels the band is $k$-outerplanar, with treewidth at most $3k - 1$ (Bodlaender 1998). For breadth-first levels, contracting the levels below the band to one vertex gives a planar graph of radius at most $k$, whose treewidth is $O(k)$ (Eppstein 2000).
- **An exact algorithm on bounded treewidth.** The problem is solved exactly in time $f(w)\,n$ on graphs of treewidth $w$, by [dynamic programming over a tree decomposition](/tree-decomposition/).
- **A local objective.** Removing or duplicating a level changes the value by at most the part of the optimum inside that level. This holds for independent set, vertex cover, dominating set, matching-like problems and others, but not for problems with global constraints such as connectivity of a spanning structure without extra work.

## The template

For a maximization problem whose solutions stay feasible under deleting vertices, like independent set, delete one class of levels.

```pseudo id=template
BAKER-MAX(G, k, SOLVE)
L1  compute the breadth-first level ℓ(v) of each vertex (from a root in each component)
L2  for r ← 0 to k − 1
L3      delete the vertices with ℓ(v) ≡ r (mod k)
L4      group the other vertices into bands by ⌊(ℓ(v) − r)/k⌋; each band has at most k − 1 levels
L5      S_r ← the union of SOLVE(band) over the bands
L6  keep the largest S_r
L7  return it
```

**Theorem (layer lemma, maximization).** Let $G$ be a graph, $k \ge 1$, and let SOLVE return a maximum independent set of the subgraph induced by its band. Then BAKER-MAX returns an independent set of size at least $(1 - 1/k)\,\mathrm{OPT}$.

*Proof.* *Edges are local.* If $uv$ is an edge and $u$ is reached first by the search, then $\ell(v) \le \ell(u) + 1$ when $u$ is processed, and $\ell(u) \le \ell(v)$ because the search reaches vertices in order of level. So $|\ell(u) - \ell(v)| \le 1$.

*Bands are independent of each other.* Fix $r$. Two kept vertices in different bands have levels on different sides of a deleted level $\ell \equiv r$, so their levels differ by at least 2 and they are not adjacent. A union of independent sets, one per band, is therefore independent.

*One offset loses little.* Let $I^*$ be a maximum independent set and $I^*_r$ its vertices with $\ell(v) \equiv r \pmod k$. The sets $I^*_0, \ldots, I^*_{k-1}$ partition $I^*$, so some $r$ has $|I^*_r| \le \mathrm{OPT}/k$. For this $r$, the set $I^* \setminus I^*_r$ is independent and lies in the kept vertices, and its part in each band is independent there. So SOLVE returns at least that part in each band, and
$$|S_r| \ge |I^* \setminus I^*_r| \ge \Bigl(1 - \frac1k\Bigr) \mathrm{OPT}.$$
Line L6 keeps a set at least as large. $\blacksquare$

**Minimization.** For a covering problem like vertex cover, deletion can leave edges uncovered. Use instead, for each offset $r$, the pieces $P_j$ made of the $k + 1$ levels $r + jk, \ldots, r + (j+1)k$, which overlap in the levels $\equiv r$. Each edge joins equal or adjacent levels, so it lies inside some piece, and the union of covers of the pieces is a cover of $G$. A minimum cover $C^*$ restricts to a cover of each piece, and a vertex of $C^*$ is in two pieces only if its level is $\equiv r$. So the union costs at most $\mathrm{OPT} + |C^*_r|$, and the best offset gives at most $(1 + 1/k)\,\mathrm{OPT}$.

**The scheme.** For a target $\varepsilon$, choose $k = \lceil 1/\varepsilon \rceil$. A band of fewer than $k$ levels has treewidth $O(k)$, and a tree decomposition of that width can be found in linear time for fixed $k$. The dynamic program for independent set costs $2^{O(k)}$ per bag, so the whole scheme runs in time $2^{O(1/\varepsilon)}\,n$, which is an [EPTAS](/eptas/) and a linear-time [PTAS](/ptas/) for each fixed $\varepsilon$.

## Classic examples

**Maximum independent set, with a small graph.** Take the $3 \times 3$ grid with vertices $0, \ldots, 8$ in rows, the grid edges, and the four diagonals at the centre vertex 4. From root 0 the levels are $L_0 = \{0\}$, $L_1 = \{1, 3, 4\}$, $L_2 = \{2, 5, 6, 7, 8\}$. With $k = 2$:

| offset $r$ | deleted levels | bands | best set per band | size |
|---|---|---|---|---|
| 0 | $L_0$, $L_2$ | $\{1, 3, 4\}$ | $\{1, 3\}$ | 2 |
| 1 | $L_1$ | $\{0\}$ and $\{2, 5, 6, 7, 8\}$ | $\{0\}$ and $\{2, 6, 8\}$ | 4 |

The optimum $\{0, 2, 6, 8\}$ has 4 vertices, all in even levels. Offset 0 deletes all of them; offset 1 deletes none, and recovers the optimum. The lemma promises only $\max_r |S_r| \ge (1 - \frac12) \cdot 4 = 2$.

**Minimum vertex cover.** The overlapping pieces above give $(1 + 1/k)\,\mathrm{OPT}$. On the same graph with $k = 2$ both offsets give covers of size 5, which is optimal.

**Minimum dominating set.** Here a vertex can be dominated from the next level, so the pieces must overlap, and the dynamic program must allow vertices near the piece boundary to be dominated from outside the piece. With these changes the overlap argument gives $(1 + O(1/k))\,\mathrm{OPT}$. Baker treats this and several other problems in the paper.

**Subgraph isomorphism and minor-closed families.** Eppstein (2000) uses the same layering to decide whether a fixed pattern graph $H$ is a subgraph of a planar graph in linear time, and to extend the technique to graph families where treewidth is bounded by a function of the diameter.

## Variations

- **Outerplanarity levels or breadth-first levels.** Baker's original uses outerplanarity levels and the bound $3k - 1$ for $k$-outerplanar graphs. Breadth-first levels are easier to compute and give treewidth $O(k)$ for bands of $k$ levels after the contraction above; the constant is slightly worse.
- **Beyond planar graphs.** The scheme works on any graph class where bands of $k$ breadth-first levels have treewidth bounded by a function of $k$; Eppstein calls this bounded local treewidth. Demaine and Hajiaghayi (2005) extend it further with bidimensionality.
- **Edge layering and contraction.** For problems where deleting vertices is wrong, such as TSP or [Steiner tree](/steiner-tree-problem/), one can delete or contract edges of the levels instead. This needs a spanner of weight $O(\mathrm{OPT})$ first, as in the [planar Steiner tree scheme](/planar-steiner-tree-ptas/) of Borradaile, Klein and Mathieu.
- **Separators instead of layers.** Lipton and Tarjan used the [planar separator theorem](/planar-separator-theorem/) for an earlier scheme for independent set, with ratio $1 - O(1/\sqrt{\log \log n})$. Baker's layering gives a constant $1 - 1/k$ with a linear running time.

## Pitfalls

- **Levels must be local.** The proof needs every edge to join equal or adjacent levels. Levels from a depth-first search, or from distances in a weighted graph, do not have this property.
- **Disconnected graphs.** Run the search from a root in each component; vertices not reached would get no level.
- **Planarity carries the treewidth bound.** In a general graph a single level can hold a large clique or a large grid, so a band has no bounded treewidth. Without planarity or a similar property, the exact step is not polynomial.
- **Minimization needs overlap.** Deleting levels for vertex cover leaves the edges between a deleted level and its neighbours uncovered. Use the overlapping pieces, and count the shared level twice in the analysis.
- **The constant in the exponent.** The width $3k - 1$ enters as $2^{3k}$ or more in the dynamic program, so the scheme is practical only for small $k$.

## Exercises

1. In the example, take the root 4 instead of 0. What are the levels, and what do the two offsets give for $k = 2$?
2. Prove that a graph whose breadth-first levels all lie in $\{0, \ldots, k - 1\}$, with one root, is a graph of radius at most $k - 1$.
3. Give the analysis for vertex cover in full, and show that the pieces must have $k + 1$ levels rather than $k$.
4. Show that the ratio $1 - 1/k$ for independent set is tight for the analysis: find a graph and a $k$ where every offset loses exactly $\mathrm{OPT}/k$ before the bands are solved.
5. Why does the technique fail for maximum clique in general graphs, and why is it not needed for maximum clique in planar graphs?

## References
