---
tag: VGG0JH
kind: problem
slug: planar-graph-coloring
name: Planar graph coloring
aliases:
- coloring planar graphs
- map coloring
area: graphs/planar-graphs
level: core
summary: Color the vertices of a planar graph with few colors so adjacent vertices differ.
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: O(n^2)}
prereqs: [planar-graph, graph-coloring, planar-edge-bound]
see_also: [four-color-theorem, five-color-theorem, five-color-algorithm, kempe-chain, chromatic-number, planar-dual-graph, list-coloring, degeneracy]
sources:
  - paper: doi:10.1006/jctb.1997.1750
    title: Neil Robertson, Daniel P. Sanders, Paul Seymour and Robin Thomas, The four-colour theorem, Journal of Combinatorial Theory, Series B 70(1), 2 to 44 (1997)
    locator: the main theorem and the quadratic-time 4-coloring algorithm
  - paper: doi:10.1016/0304-3975(76)90059-1
    title: M. R. Garey, D. S. Johnson and L. Stockmeyer, Some simplified NP-complete graph problems, Theoretical Computer Science 1(3), 237 to 267 (1976)
    locator: the NP-completeness of 3-coloring planar graphs, also with maximum degree 4
  - paper: "Norishige Chiba, Takao Nishizeki and Nobuji Saito, A linear 5-coloring algorithm of planar graphs, Journal of Algorithms 2(4), 317 to 327 (1981)"
    locator: the whole paper
  - paper: doi:10.1006/jctb.1994.1062
    title: Carsten Thomassen, Every planar graph is 5-choosable, Journal of Combinatorial Theory, Series B 62(1), 180 to 181 (1994)
    locator: the whole paper
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 5.1, Colouring maps and planar graphs (the five colour theorem, the four colour theorem, and Grötzsch's theorem)
  - paper: doi:10.1215/ijm/1256049011
    title: Kenneth Appel and Wolfgang Haken, Every planar map is four colorable. Part I. Discharging, Illinois Journal of Mathematics 21(3), 429 to 490 (1977)
    locator: the whole paper (with Part II, the first proof of the four color theorem)
  - paper: doi:10.1016/0012-365X(93)90579-I
    title: Margit Voigt, List colourings of planar graphs, Discrete Mathematics 120(1-3), 215 to 219 (1993)
    locator: the planar graph that is not 4-choosable
  - paper: "Zdeněk Dvořák, Ken-ichi Kawarabayashi and Robin Thomas, Three-coloring triangle-free planar graphs in linear time, ACM Transactions on Algorithms 7(4), article 41 (2011)"
    locator: the whole paper
---

Planar graph coloring asks for a proper coloring of a [planar graph](/planar-graph/) with as few colors as possible: each vertex gets a color, and the two ends of each edge get different colors. Four colors always suffice, by the [four color theorem](/four-color-theorem/), and a 4-coloring can be found in $O(n^2)$ time. Five colors can be found in $O(n)$ time. But deciding whether three colors suffice is NP-complete, even for planar graphs of maximum degree 4.

## In plain words

You have a map and want to paint each country so that two countries with a common border never get the same paint. How many paints do you need? Turn the map into a graph: one point per country and a line between neighbours. The graph has no crossings, so it is planar.

Four paints are always enough. This was a famous open question for more than a century, and its proof needed a computer. Finding a painting with five paints is easy and fast. Finding one with four is slower but still practical. Asking whether three paints are enough for a given map is a hard question: no fast method is known.

## Definition

**Input.** A [simple](/simple-graph/) planar graph $G = (V, E)$ with $n$ vertices, given by adjacency lists, and in some variants an integer $k$.

**Output.** A proper $k$-coloring, that is, a map $c : V \to \{1, \ldots, k\}$ with $c(u) \ne c(v)$ for every edge $uv \in E$.

- **Optimization.** Find a proper coloring with $\chi(G)$ colors, where the [chromatic number](/chromatic-number/) $\chi(G)$ is the least $k$ for which one exists.
- **Decision.** Given $k$, is $\chi(G) \le k$?
- **Search for fixed $k$.** Given that $G$ is planar, output a proper $k$-coloring, for $k = 4, 5$ or $6$.

The embedding is not part of the input. The algorithms that need one compute it first in linear time ([planar embedding](/planar-embedding/)), as a [rotation system](/rotation-system/).

**Faces instead of vertices.** Coloring the faces of a plane graph so that faces sharing an edge differ is coloring the vertices of the [planar dual](/planar-dual-graph/). A map with no country that touches itself across a border has a loopless dual, so the vertex version covers it.

## Variants

- **Fixed number of colors.** $k = 1$: $G$ has no edge. $k = 2$: $G$ is [bipartite](/bipartite-graph/), tested by [BFS](/breadth-first-search/). $k = 3$: NP-complete. $k \ge 4$: always yes.
- **Triangle-free planar graphs.** Grötzsch's theorem says they are 3-colorable (Diestel, Section 5.1), and a 3-coloring can be found in linear time.
- **List coloring.** Each vertex has its own list of allowed colors. Every planar graph is 5-choosable (Thomassen, 1994), but not every planar graph is 4-choosable (Voigt, 1993). See [list coloring](/list-coloring/).
- **Edge coloring.** Color the edges so that edges at a vertex differ; see [edge coloring](/edge-coloring/).
- **Counting colorings.** Count the proper $k$-colorings; this is the [chromatic polynomial](/chromatic-polynomial/) evaluated at $k$.
- **Graphs on surfaces.** On a surface of Euler genus $g \ge 1$, the Heawood bound gives $\chi \le \lfloor (7 + \sqrt{1 + 24 g}) / 2 \rfloor$ colors.

## Examples

| planar graph | $n$ | $\chi$ | why |
|---|---|---|---|
| a single vertex | 1 | 1 | no edge |
| a tree with an edge | $n$ | 2 | bipartite |
| the cycle $C_5$ | 5 | 3 | an odd cycle; also triangle-free, so Grötzsch gives 3 |
| the octahedron | 6 | 3 | opposite vertices share a color, and it has triangles |
| the wheel $W_4$ (a 4-cycle and a hub) | 5 | 3 | the cycle needs 2, the hub a third |
| the wheel $W_5$ (a 5-cycle and a hub) | 6 | 4 | the odd cycle needs 3, the hub a fourth |
| $K_4$ | 4 | 4 | four pairwise adjacent vertices |
| the icosahedron | 12 | 4 | each vertex has a 5-cycle as its neighbourhood, like $W_5$ |
| $K_5$ | 5 | 5 | not planar, so the four color theorem does not apply |

The planar graphs that need exactly 4 colors are common. Every planar graph that contains $K_4$ or an odd wheel needs 4, so a 3-color test must look at the whole graph.

**Greedy 6-coloring of $K_4$.** Order the vertices by repeatedly removing a vertex of degree at most 5, which always exists by the [planar edge bound](/planar-edge-bound/). Color them in the reverse order, each with the smallest color unused by its colored neighbours. On $K_4$ this uses colors 1, 2, 3, 4, which is optimal here; in general it only guarantees 6.

## Known algorithms

| colors | algorithm | time |
|---|---|---|
| 6 | greedy in reverse [degeneracy order](/degeneracy-ordering/): remove a vertex of degree at most 5, recurse, give it a free color | $O(n)$ |
| 5 | the [five-color algorithm](/five-color-algorithm/): as above, but a vertex of degree 5 with all colors used is fixed by a [Kempe chain](/kempe-chain/) swap or by contracting two non-adjacent neighbours | $O(n)$ (Chiba, Nishizeki and Saito, 1981) |
| 4 | the algorithm of Robertson, Sanders, Seymour and Thomas, from their proof of the [four color theorem](/four-color-theorem/): find a reducible configuration, reduce, recurse | $O(n^2)$ |
| 3 | exact exponential search; no polynomial algorithm is known | NP-complete |
| 3, triangle-free | Grötzsch's theorem, made algorithmic (Dvořák, Kawarabayashi and Thomas) | $O(n)$ |
| 2 | test bipartiteness with BFS | $O(n)$ |

The [five color theorem](/five-color-theorem/) page gives the proof that the five-color step works.

## Bounds

- **Upper bounds.** $\chi(G) \le 4$ for every planar $G$ (Appel and Haken, announced in 1976 and published in 1977; Robertson, Sanders, Seymour and Thomas, 1997). A 4-coloring takes $O(n^2)$ time, a 5-coloring $O(n)$.
- **Lower bounds.** The bound 4 is tight: $K_4$ is planar. Each algorithm needs $\Omega(n)$ time to write its output.
- **Hardness.** Deciding $\chi(G) \le 3$ for planar $G$ is NP-complete, also for maximum degree 4 (Garey, Johnson and Stockmeyer, 1976). So computing $\chi(G)$ for a planar graph is NP-hard, although the answer is always one of 1, 2, 3, 4. The difficulty is only to tell 3 from 4.

## Reductions

- **From 3-coloring of general graphs.** Garey, Johnson and Stockmeyer replace each crossing of a drawing of a general graph by a planar gadget that forces equal colors on opposite corners. The result is a polynomial reduction from 3-coloring to planar 3-coloring.
- **Planar 3-coloring to degree at most 4.** A further gadget replaces each vertex of high degree, which gives NP-completeness for maximum degree 4.
- **Map coloring to vertex coloring.** Coloring the faces of a plane graph reduces to coloring the vertices of its dual in $O(n)$ time.
- **Coloring to triangulations.** Adding edges never makes coloring easier, so a coloring algorithm may first triangulate the graph to a [maximal planar graph](/maximal-planar-graph/) and then delete the extra edges.

## Applications

- **Maps.** Coloring political or geographical maps, the origin of the problem.
- **Frequency assignment.** Conflicts between neighbouring regions, such as frequency assignment for transmitters with planar interference graphs, are planar coloring problems.
- **Parallel computing.** A coloring with few colors splits the vertices into independent sets that can be processed in parallel rounds, for example in mesh computations.
- **Theory.** Planar coloring was the source of [Kempe chains](/kempe-chain/), discharging, and the use of computers in proofs, and it motivates the [Hadwiger conjecture](/hadwiger-conjecture/).

## References
