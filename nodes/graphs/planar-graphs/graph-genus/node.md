---
tag: Y02DZQ
kind: concept
slug: graph-genus
name: Graph genus
aliases:
- orientable genus
area: graphs/planar-graphs
level: advanced
summary: Minimum genus of an orientable surface on which the graph embeds; planar graphs have genus zero.
prereqs: [planar-graph, euler-formula, rotation-system, planar-face, connected-graph]
see_also: [graph-genus-computation, kuratowski-theorem, graph-minor, graph-minor-theorem, four-color-theorem, crossing-number, planarity-testing, planar-embedding]
sources:
  - book: isbn:9780801866890
    title: Bojan Mohar and Carsten Thomassen, Graphs on Surfaces, Johns Hopkins University Press, 2001
    locator: Chapters 3 and 4 (rotation systems, the Euler formula for cellular embeddings, and the genus of a graph)
  - book: isbn:9780486417417
    title: Jonathan L. Gross and Thomas W. Tucker, Topological Graph Theory, Dover, 2001
    locator: Chapter 3, Surfaces and graph imbeddings (face tracing and the Euler formula); Chapter 5, Map colorings (the Heawood problem)
  - paper: doi:10.1073/pnas.60.2.438
    title: Gerhard Ringel and J. W. T. Youngs, Solution of the Heawood map-coloring problem, Proceedings of the National Academy of Sciences 60(2), 438 to 445 (1968)
    locator: the genus of the complete graph
  - paper: doi:10.1016/0196-6774(89)90006-0
    title: Carsten Thomassen, The graph genus problem is NP-complete, Journal of Algorithms 10(4), 568 to 576 (1989)
    locator: the main theorem
---

The genus of a graph $G$ is the least $g$ such that $G$ can be drawn without crossings on the orientable surface $S_g$, the sphere with $g$ handles. [Planar graphs](/planar-graph/) are the graphs of genus 0; $K_5$ and $K_{3,3}$ have genus 1, since both embed on the torus. For a connected graph the genus is a finite combinatorial quantity: it is read off from [rotation systems](/rotation-system/) with the [Euler formula](/euler-formula/), so no topology is needed to compute it. Computing it is [NP-hard](/np-hard/) in general, and see [graph genus computation](/graph-genus-computation/) for the algorithms.

## In plain words

A drawing on a sheet of paper may force two edges to cross. A drawing on the surface of a doughnut has more room: an edge can go around the hole. A surface with more holes has even more room. The genus of a graph is the smallest number of holes that a surface needs so that the graph fits on it without crossings.

You do not need to draw on surfaces to find it. At each vertex, choose a circular order of its edges. These choices fix the faces of a drawing on some surface. Count the faces, and a simple count of vertices, edges and faces tells you the number of holes. The genus is the smallest number that any choice gives.

## The idea

**How the embedding is given.** Everything on this page uses a rotation system: for each vertex $v$, a cyclic order $\pi_v$ of the neighbours of $v$. Coordinates or a drawing on a surface are not needed. A rotation system defines faces by *face tracing*: from a dart (directed edge) $(u, v)$, go to $(v, w)$ where $w$ is the neighbour of $v$ after $u$ in $\pi_v$, and repeat until the first dart comes back. Every dart lies on exactly one face. This is the same procedure as for [plane faces](/planar-face/).

**Euler's formula on surfaces.** An embedding of a connected graph in a surface is *cellular* if every face is an open disc. For a cellular embedding in $S_g$ with $n$ vertices, $m$ edges and $f$ faces,

$$n - m + f = 2 - 2g.$$

Conversely, for every rotation system of a connected graph, gluing a disc into each traced face gives a closed orientable surface in which the graph is cellularly embedded, and its genus is $g = (2 - n + m - f)/2$. This correspondence between rotation systems and cellular embeddings up to orientation-preserving homeomorphism is the Heffter-Edmonds rotation principle (Mohar and Thomassen, Chapter 3; Gross and Tucker, Chapter 3).

**Definition.** The **genus** $\gamma(G)$ of a graph $G$ is the least $g$ such that $G$ embeds in $S_g$. A minimum genus embedding of a connected graph is cellular (Youngs, 1963), so for connected $G$

$$\gamma(G) = \min_{\pi} \frac{2 - n + m - f(\pi)}{2},$$

the minimum over all rotation systems $\pi$, where $f(\pi)$ is the number of traced faces. In words, the genus is fixed by the rotation system with the most faces. A vertex of degree $d$ has $(d - 1)!$ cyclic orders, so the minimum ranges over $\prod_v (\deg v - 1)!$ rotation systems, a finite but large set.

**Lower bound from face lengths.** In a simple connected graph with $n \ge 3$, every face of a cellular embedding has length at least 3, and the face lengths add up to $2m$, so $3f \le 2m$. Putting this into the formula gives

$$\gamma(G) \ge \left\lceil \frac{m - 3n + 6}{6} \right\rceil.$$

If $G$ has no triangle, every face has length at least 4, and $\gamma(G) \ge \lceil (m - 2n + 4)/4 \rceil$. For $g = 0$ these are the [planar edge bounds](/planar-edge-bound/) $m \le 3n - 6$ and $m \le 2n - 4$.

**Exact values.** Ringel and Youngs (1968) completed the proof that the bound for triangles is attained by complete graphs:

$$\gamma(K_n) = \left\lceil \frac{(n - 3)(n - 4)}{12} \right\rceil \quad (n \ge 3).$$

For complete bipartite graphs, Ringel (1965) proved $\gamma(K_{a,b}) = \lceil (a - 2)(b - 2)/4 \rceil$ for $a, b \ge 2$, which is the triangle-free bound.

**Components and blocks.** Genus is additive: if $G$ has blocks (maximal 2-connected pieces, or bridges) $B_1, \ldots, B_k$, then $\gamma(G) = \gamma(B_1) + \cdots + \gamma(B_k)$ (Battle, Harary, Kodama and Youngs, 1962). For components the inequality $\le$ is clear, since each component can be put on its own surface and the surfaces joined by a tube; the theorem says that nothing is gained by sharing handles.

**Minors.** If $H$ is a [minor](/graph-minor/) of $G$, then $\gamma(H) \le \gamma(G)$: deleting an edge or contracting an edge of an embedded graph keeps it embedded in the same surface. So for each $g$, the graphs of genus at most $g$ form a minor-closed class. By the [graph minor theorem](/graph-minor-theorem/), each such class is described by a finite list of forbidden minors. For $g = 0$ the list is $K_5$ and $K_{3,3}$ ([Kuratowski's theorem](/kuratowski-theorem/)); for the torus the list is known to be very long and is not known completely.

## Examples

The values below were checked by computer, by face tracing over all rotation systems for the small graphs.

| graph | $n$ | $m$ | lower bound | $\gamma$ | reason |
|---|---|---|---|---|---|
| a single vertex | 1 | 0 | 0 | 0 | it is planar; its one face is the whole sphere |
| a tree | $n$ | $n - 1$ | 0 | 0 | each rotation system gives one face, and $n - (n - 1) + 1 = 2$ |
| $K_4$ | 4 | 6 | 0 | 0 | planar; the best rotation system has 4 faces |
| $K_5$ | 5 | 10 | 1 | 1 | not planar; the best rotation system has 5 faces, and $5 - 10 + 5 = 0$ |
| $K_{3,3}$ | 6 | 9 | 1 | 1 | not planar; the best rotation system has 3 faces, and $6 - 9 + 3 = 0$ |
| Petersen graph | 10 | 15 | 1 | 1 | girth 5 gives $f \le 6$, so $\gamma \ge 1$; the best rotation system has 5 faces |
| $K_7$ | 7 | 21 | 1 | 1 | the rotation below has 14 triangular faces, and $7 - 21 + 14 = 0$ |
| $K_8$ | 8 | 28 | 2 | 2 | Ringel and Youngs formula, $\lceil 20/12 \rceil = 2$ |

For the Petersen graph the face lengths are at least 5, so $5f \le 2m = 30$ and $f \le 6$. Then $2 - 2g = 10 - 15 + f \le 1$, which forces $g \ge 1$.

**$K_7$ on the torus.** Number the vertices $0, \ldots, 6$ and give vertex $i$ the rotation

$$\pi_i = (i+1,\ i+3,\ i+2,\ i+6,\ i+4,\ i+5) \pmod 7.$$

Face tracing gives 14 faces, all triangles. So $K_7$ triangulates the torus: it is a toroidal graph with $3n$ edges, the most that the face-length bound allows on the torus. As a map, the 7 vertices are 7 countries on the torus that pairwise touch.

**A tree.** For a tree, face tracing walks around the whole tree once, so every rotation system has exactly one face. The formula gives $g = (2 - n + (n - 1) - 1)/2 = 0$, as it must be.

## Where it is used

- **Map coloring on surfaces.** Heawood (1890) showed with the Euler formula that every graph of genus $g \ge 1$ has chromatic number at most $H(g) = \lfloor (7 + \sqrt{1 + 48 g})/2 \rfloor$. The genus of $K_n$ shows that $K_{H(g)}$ embeds in $S_g$, so the bound is tight; this is the Heawood map color theorem of Ringel and Youngs. For $g = 1$, $H(1) = 7$, attained by $K_7$ above. For $g = 0$ the formula gives 4, which is the [four color theorem](/four-color-theorem/), the one case that needs a different proof.
- **Algorithms on graphs of bounded genus.** Many results for planar graphs extend to graphs of genus $g$ with a loss that depends on $g$: separators of size $O((g n)^{1/2})$ (Gilbert, Hutchinson and Tarjan, 1984), [treewidth](/treewidth/) and grid minor bounds, and bidimensionality. These algorithms take an embedding as input, so they first need [genus computation](/graph-genus-computation/).
- **Testing and certifying non-planarity.** A graph has genus 0 exactly when it is planar, which [planarity testing](/planarity-testing/) decides in linear time. Higher genus is a measure of how far a graph is from planar, next to the [crossing number](/crossing-number/).
- **Computational complexity.** Thomassen (1989) proved that deciding $\gamma(G) \le k$ is [NP-complete](/np-complete/) when $k$ is part of the input. For each fixed $k$ it takes linear time (Mohar, 1999).

## References
