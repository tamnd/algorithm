---
tag: 3ZHRA5
kind: problem
slug: crossing-number
name: Crossing number
aliases:
- graph crossing number
area: graphs/planar-graphs
level: advanced
summary: Minimum number of edge crossings over all drawings of a graph; zero exactly when the graph is planar.
prereqs: [planar-graph, planar-edge-bound, np-complete]
see_also: [crossing-lemma, planarization-heuristic, kuratowski-theorem, hanani-tutte-theorem, book-embedding, graph-genus, fary-theorem, planarity-testing]
sources:
  - paper: "Michael R. Garey and David S. Johnson, Crossing number is NP-complete, SIAM Journal on Algebraic and Discrete Methods 4(3), 312 to 316 (1983)"
    locator: the main theorem, by reduction from optimal linear arrangement
  - paper: "Marcus Schaefer, The graph crossing number and its variants, a survey, Electronic Journal of Combinatorics, Dynamic Survey DS21"
    locator: the sections on the definitions of drawings, the variants (rectilinear, pair, odd) and their relations, and on complexity
  - paper: "János Pach and Géza Tóth, Which crossing number is it anyway?, Journal of Combinatorial Theory, Series B 80(2), 225 to 246 (2000)"
    locator: the pair and odd crossing numbers and their relations to the crossing number
  - paper: "Martin Grohe, Computing crossing numbers in quadratic time, Journal of Computer and System Sciences 68(2), 285 to 302 (2004)"
    locator: the fixed-parameter algorithm for crossing number at most k
  - paper: "Petr Hliněný, Crossing number is hard for cubic graphs, Journal of Combinatorial Theory, Series B 96(4), 455 to 471 (2006)"
    locator: NP-hardness for cubic graphs
  - paper: "Daniel Bienstock and Nathaniel Dean, Bounds for rectilinear crossing numbers, Journal of Graph Theory 17(3), 333 to 348 (1993)"
    locator: graphs with crossing number 4 and arbitrarily large rectilinear crossing number
  - paper: "Daniel J. Kleitman, The crossing number of K5,n, Journal of Combinatorial Theory 9(4), 315 to 323 (1970)"
    locator: Zarankiewicz's formula for K_(m,n) with min(m, n) at most 6
---

The crossing number $\mathrm{cr}(G)$ of a graph $G$ is the smallest number of edge crossings in a drawing of $G$ in the plane. It is 0 exactly for [planar graphs](/planar-graph/), so it measures how far a graph is from planar. Computing it is [NP-complete](/np-complete/) (Garey and Johnson, 1983), even for cubic graphs, but for each fixed $k$ one can decide $\mathrm{cr}(G) \le k$ in polynomial time. The exact value is unknown for most complete graphs, and the best general lower bound comes from the [crossing lemma](/crossing-lemma/).

## In plain words

Draw a network on paper with dots and lines. If the network cannot be drawn without lines crossing, try to make as few crossings as possible. The smallest number you can reach is the crossing number.

A network that can be drawn without crossings has crossing number zero. Five dots all linked to each other need one crossing. The problem is that the number of possible drawings is endless, so finding the best one is hard: no fast method is known for large networks, and most experts believe none exists. Even for the network where every pair of dots is linked, the answer is known only for a few small sizes.

## Definition

A **drawing** of a graph $G = (V, E)$ maps vertices to distinct points of the plane and each edge $uv$ to a simple curve from $u$ to $v$ that passes through no other vertex. We assume that two edges meet in finitely many points, that each meeting point other than a common end is a proper crossing (not a touching), and that no three edges pass through one crossing. A **crossing** is a pair of edges together with a common interior point.

**Crossing number.** $\mathrm{cr}(G)$ is the minimum number of crossings over all drawings of $G$.

A drawing with $\mathrm{cr}(G)$ crossings can be taken to be **good**: adjacent edges do not cross, and two edges cross at most once. If two edges cross twice, exchanging their pieces between the two crossings and smoothing removes both crossings; if adjacent edges cross, exchanging the pieces between the common end and the crossing removes it. Both moves lower the count, so an optimal drawing has neither.

**Decision problem.** CROSSING NUMBER: given $G$ and an integer $k$, is $\mathrm{cr}(G) \le k$?

**What is given and what is returned.** The input is an abstract graph, with no embedding. A drawing can be returned in two equivalent forms: coordinates and curves, or a **planarization**, the planar graph obtained by replacing each crossing by a new vertex of degree 4, together with a [rotation system](/rotation-system/) of that planar graph. So $\mathrm{cr}(G) \le k$ if and only if $G$ has a planarization with at most $k$ crossing vertices.

## Variants

- **Rectilinear crossing number** $\overline{\mathrm{cr}}(G)$: edges must be straight segments. [Fáry's theorem](/fary-theorem/) says $\overline{\mathrm{cr}}(G) = 0$ when $\mathrm{cr}(G) = 0$, and the same holds for $\mathrm{cr}(G) \le 3$, but Bienstock and Dean gave graphs with $\mathrm{cr}(G) = 4$ and arbitrarily large $\overline{\mathrm{cr}}(G)$.
- **Pair crossing number** $\mathrm{pcr}(G)$: the number of pairs of edges that cross at least once. **Odd crossing number** $\mathrm{ocr}(G)$: the number of pairs that cross an odd number of times. Always $\mathrm{ocr}(G) \le \mathrm{pcr}(G) \le \mathrm{cr}(G) \le \overline{\mathrm{cr}}(G)$. The [Hanani-Tutte theorem](/hanani-tutte-theorem/) says $\mathrm{ocr}(G) = 0$ implies $\mathrm{cr}(G) = 0$; Pach and Tóth showed $\mathrm{cr}(G) \le 2\,\mathrm{ocr}(G)^2$, and Pelsmajer, Schaefer and Štefankovič found graphs with $\mathrm{ocr}(G) < \mathrm{cr}(G)$. Whether $\mathrm{pcr}(G) = \mathrm{cr}(G)$ always is open.
- **Crossing number on a surface**: drawings on a surface of [genus](/graph-genus/) $g$; it is 0 exactly when $G$ embeds in that surface.
- **Fixed embedding or fixed drawing style.** Bipartite two-layer drawings (one-sided crossing minimization), drawings with vertices on a line and edges on pages ([book embedding](/book-embedding/)), and inserting one edge into a fixed plane drawing with fewest crossings, which is a shortest path in the dual graph.
- **Skewness and k-planarity.** The minimum number of edges whose deletion makes $G$ planar, and the class of graphs that have a drawing where each edge is crossed at most $k$ times.

## Examples

| graph | $n$ | $m$ | $\mathrm{cr}$ | lower bound | drawing for the upper bound |
|---|---|---|---|---|---|
| single vertex, any tree, $K_4$ | | | 0 | | planar |
| $K_5$ | 5 | 10 | 1 | $m - (3n - 6) = 1$ | points $(0,0)$, $(6,0)$, $(3,6)$, $(1,1)$, $(2,1)$ |
| $K_{3,3}$ | 6 | 9 | 1 | $m - (2n - 4) = 1$ | sides $(0,0)$, $(2,3)$, $(4,0)$ and $(1,0)$, $(2,4)$, $(2,2)$ |
| $K_6$ | 6 | 15 | 3 | $m - (3n - 6) = 3$ | points $(5,3)$, $(7,8)$, $(0,1)$, $(3,2)$, $(5,2)$, $(7,0)$ |
| Petersen graph | 10 | 15 | 2 | girth 5 gives $m - \lfloor 5(n - 2)/3 \rfloor = 2$ | see below |

The lower bounds use one argument. If a graph in a class closed under deleting edges has at most $f(n)$ edges whenever it is planar, then deleting one edge per crossing of an optimal drawing leaves a planar graph, so $\mathrm{cr}(G) \ge m - f(n)$. For simple planar graphs $f(n) = 3n - 6$, for triangle-free ones $f(n) = 2n - 4$, and for girth 5 the face count gives $5f \le 2m$ and $m \le 5(n - 2)/3$ (see [planar edge bound](/planar-edge-bound/)).

For the Petersen graph with outer cycle $0, 1, 2, 3, 4$, spokes $i$ to $i + 5$, and inner edges $5\text{-}7$, $7\text{-}9$, $9\text{-}6$, $6\text{-}8$, $8\text{-}5$, the straight-line drawing with the points $0 = (2,1)$, $1 = (7,2)$, $2 = (3,0)$, $3 = (1,1)$, $4 = (0,7)$, $5 = (3,3)$, $6 = (7,6)$, $7 = (12,2)$, $8 = (1,8)$, $9 = (4,12)$ has exactly 2 crossings. In all these drawings no vertex lies on an edge that it does not belong to, and the crossing counts were checked by a script with exact integer orientation tests. These drawings are straight-line, so in each row $\overline{\mathrm{cr}} = \mathrm{cr}$ as well.

**Complete graphs.** Guy's conjecture says $\mathrm{cr}(K_n) = Z(n) = \frac{1}{4} \lfloor \frac{n}{2} \rfloor \lfloor \frac{n-1}{2} \rfloor \lfloor \frac{n-2}{2} \rfloor \lfloor \frac{n-3}{2} \rfloor$. Drawings with $Z(n)$ crossings exist for all $n$ (two concentric cycles on a cylinder), and the conjecture is proved for $n \le 12$. For $n = 5, 6, 7, 8$ it gives $1, 3, 9, 18$. The rectilinear crossing number is larger from $n = 8$ on: $\overline{\mathrm{cr}}(K_8) = 19$.

**Complete bipartite graphs.** Zarankiewicz's conjecture says $\mathrm{cr}(K_{m,n}) = \lfloor \frac{m}{2} \rfloor \lfloor \frac{m-1}{2} \rfloor \lfloor \frac{n}{2} \rfloor \lfloor \frac{n-1}{2} \rfloor$. The upper bound comes from a drawing with the two sides on the two axes; Kleitman proved equality when $\min(m, n) \le 6$.

## Known algorithms

- **Exhaustive search.** Try every planarization: choose which pairs of edges cross and in which order along each edge, and test the result for planarity. This is correct but exponential.
- **Fixed k.** Grohe showed that $\mathrm{cr}(G) \le k$ can be decided in $O(n^2)$ time for each fixed $k$, using that a graph with small crossing number and large treewidth has a large planar grid-like part. Kawarabayashi and Reed improved this to linear time. The dependence on $k$ is huge.
- **Exact optimization.** Integer linear programs over planarizations with branch and cut (Buchheim, Chimani, Ebner, Gutwenger, Jünger, Klau, Mutzel and Weiskircher) solve sparse graphs with up to a few hundred edges in practice.
- **Heuristics.** The [planarization heuristic](/planarization-heuristic/) takes a large planar subgraph, then inserts the remaining edges one by one along shortest paths in the dual graph. Inserting a single edge optimally over all embeddings of the planar part takes linear time (Gutwenger, Mutzel and Weiskircher).
- **Approximation.** For graphs of bounded degree, algorithms with approximation ratio polynomial in $n$ are known (the line of work by Chuzhoy and coauthors); no constant-factor approximation is known.

## Bounds

- **Trivial.** $0 \le \mathrm{cr}(G) \le \binom{m}{2}$, since a good drawing has at most one crossing per pair of edges.
- **Euler.** $\mathrm{cr}(G) \ge m - 3n + 6$ for $n \ge 3$, from the table argument.
- **Crossing lemma.** $\mathrm{cr}(G) \ge \frac{m^3}{64 n^2}$ when $m \ge 4n$; the constant has been improved. So dense graphs have crossing number $\Theta(m^3/n^2)$ at least, which is far above the Euler bound. See [crossing lemma](/crossing-lemma/).
- **Bisection width.** $\mathrm{cr}(G) \ge \frac{1}{40} b(G)^2 - \frac{1}{16}\sum_v \deg(v)^2$, where $b(G)$ is the bisection width (Pach, Shahrokhi and Szegedy; Sýkora and Vrt'o). This links crossings to separators.
- **Complexity.** NP-complete in general (Garey and Johnson), NP-complete for cubic graphs (Hliněný), and NP-hard even for a planar graph plus one edge (Cabello and Mohar). For the rectilinear crossing number, Bienstock's reduction from stretchability of pseudoline arrangements shows that it is as hard as the existential theory of the reals.

## Reductions

- **NP-hardness.** Garey and Johnson reduce from optimal linear arrangement: a weighted path-like gadget forces vertices onto a line, and crossings count the cost of the arrangement.
- **Membership in NP.** A planarization with at most $k$ crossing vertices, with the order of crossings along each edge, has size polynomial in $n + k$, and planarity of it is tested in linear time ([planarity testing](/planarity-testing/)). Since $\mathrm{cr}(G) \le \binom{m}{2}$, this is a polynomial certificate.
- **To planarity.** $\mathrm{cr}(G) = 0$ is planarity, decided in linear time; [Kuratowski's theorem](/kuratowski-theorem/) gives the obstruction.

## Applications

- **Readable drawings.** Crossings are the strongest measure of how hard a drawing is to read, so drawing systems minimize them heuristically.
- **VLSI layout.** Leighton showed that the area of a VLSI layout of a graph of bounded degree is at least of the order of $\mathrm{cr}(G) + n$, so crossing number lower bounds give area lower bounds.
- **Combinatorial geometry.** Through the crossing lemma, crossing numbers give the Szemerédi-Trotter bound on point-line incidences and bounds on unit distances and $k$-sets.

## References
