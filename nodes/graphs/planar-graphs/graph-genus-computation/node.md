---
tag: D7QYNF
kind: problem
slug: graph-genus-computation
name: Computing graph genus
aliases:
- genus testing
- graph genus problem
area: graphs/planar-graphs
level: research
summary: Decide whether a graph embeds on a surface of a given genus.
model: word-ram
complexity:
  vars: {n: the number of vertices, g: the genus that is tested, f: a function of g only}
  time: {worst: O(f(g) n)}
prereqs: [graph-genus, rotation-system, euler-formula, planarity-testing, np-complete]
see_also: [graph-genus, planarity-testing, graph-minor-theorem, kuratowski-theorem, planar-embedding, crossing-number, treewidth, biconnected-components]
sources:
  - paper: doi:10.1016/0196-6774(89)90006-0
    title: Carsten Thomassen, The graph genus problem is NP-complete, Journal of Algorithms 10(4), 568 to 576 (1989)
    locator: the main theorem, that deciding genus at most k is NP-complete when k is part of the input
  - paper: "Bojan Mohar, A linear time algorithm for embedding graphs in an arbitrary surface, SIAM Journal on Discrete Mathematics 12(1), 6 to 26 (1999)"
    locator: the main theorem, a linear-time algorithm for each fixed surface that returns an embedding or a forbidden subgraph
  - paper: "I. S. Filotti, Gary L. Miller and John Reif, On determining the genus of a graph in O(v^(O(g))) steps, Proceedings of the 11th ACM Symposium on Theory of Computing (STOC 1979), 27 to 37"
    locator: the first polynomial algorithm for each fixed genus
  - paper: "Ken-ichi Kawarabayashi, Bojan Mohar and Bruce Reed, A simpler linear time algorithm for embedding graphs into an arbitrary surface and the genus of graphs of bounded tree-width, Proceedings of the 49th IEEE Symposium on Foundations of Computer Science (FOCS 2008), 771 to 780"
    locator: the simpler linear-time algorithm for a fixed surface, and the genus of graphs of bounded tree-width
  - paper: doi:10.1016/j.jctb.2004.08.001
    title: Neil Robertson and Paul D. Seymour, Graph minors XX, Wagner's conjecture, Journal of Combinatorial Theory, Series B 92(2), 325 to 357 (2004)
    locator: the graph minor theorem, which gives a finite set of forbidden minors for each surface
  - book: isbn:9780801866890
    title: Bojan Mohar and Carsten Thomassen, Graphs on Surfaces, Johns Hopkins University Press, 2001
    locator: Chapter 3 (rotation systems and face tracing) and Chapter 4 (the genus of graphs and the complexity of computing it)
---

Computing the genus of a graph means finding the least $g$ such that the graph can be drawn without crossings on the orientable surface $S_g$, the sphere with $g$ handles; the decision form asks whether the [genus](/graph-genus/) is at most a given $k$. For $k = 0$ this is [planarity testing](/planarity-testing/), which takes linear time. For every fixed $k$ the problem still takes linear time, by an algorithm of Mohar, but the dependence on $k$ is large. When $k$ is part of the input, the problem is [NP-complete](/np-complete/), as Thomassen proved in 1989. **How the embedding is given:** the input has no embedding; it is an abstract graph by adjacency lists. A certificate for a yes answer is a [rotation system](/rotation-system/), a cyclic order of the neighbours at each vertex, whose face count gives the genus through the [Euler formula](/euler-formula/).

## In plain words

A network that cannot be drawn on paper without crossings may fit on the surface of a doughnut, where an edge can go around the hole. With more holes there is more room. The question is: what is the smallest number of holes that this network needs?

One way to answer is to try every way of ordering the edges around each point, trace the faces each time, and keep the best count. This works for tiny networks, but the number of orders grows very fast. For a fixed small number of holes, there are clever methods that run fast. When the number of holes is part of the question, no fast method is known, and none is expected.

## Definition

**Input.** A finite undirected graph $G = (V, E)$ by adjacency lists, with $n = |V|$ and $m = |E|$, and an integer $k \ge 0$. Loops and parallel edges do not change the answer and may be removed.

**Output.** YES if $G$ embeds in $S_k$, that is, if $\gamma(G) \le k$; NO otherwise. In the search form, output a rotation system that realizes the genus.

**The combinatorial form.** For a connected graph, embeddings of least genus are cellular, and cellular embeddings correspond to rotation systems (the Heffter-Edmonds principle; see [graph genus](/graph-genus/)). So

$$\gamma(G) = \min_{\pi} \frac{2 - n + m - f(\pi)}{2},$$

where $\pi$ runs over all rotation systems and $f(\pi)$ is the number of faces traced. A YES answer is checked in $O(n + m)$ time by tracing the faces of the given rotation system. For a graph with several components, the genus is the sum over the components, and also the sum over the blocks (Battle, Harary, Kodama and Youngs), so it is enough to solve the problem for [biconnected](/biconnected-components/) graphs.

**Certificate for NO.** For each fixed $k$, the graphs of genus at most $k$ are closed under taking [minors](/graph-minor/), so by the [graph minor theorem](/graph-minor-theorem/) there is a finite list of forbidden minors, and a NO answer is certified by one of them. For $k = 0$ the list is $K_5$ and $K_{3,3}$. For the torus the list is known to contain thousands of graphs, and it is not known to be complete. Mohar's algorithm returns such a forbidden subgraph.

## Variants

- **Nonorientable genus.** Embed in the sphere with $k$ crosscaps instead of handles. Embeddings are given by a rotation system with a sign on each edge. Fixed surfaces are again handled in linear time by Mohar's algorithm.
- **Euler genus.** The least $2 - \chi$ over all surfaces, orientable or not, where $\chi$ is the Euler characteristic of the surface.
- **Fixed surface.** $k$ is a constant, not part of the input. This is the form that has linear-time algorithms.
- **Maximum genus.** The largest genus of a cellular embedding. Unlike the minimum, it can be computed in polynomial time, by a reduction to a matroid parity problem (Furst, Gross and McGeoch, 1988).
- **Approximation.** Find an embedding whose genus is close to the minimum; for general graphs no good approximation is known, and this is an active research area.

## Examples

The table counts all rotation systems of small graphs by their number of faces; it was computed by tracing the faces of every rotation system. A vertex of degree $d$ has $(d - 1)!$ cyclic orders.

| graph | rotation systems | faces: how many systems | $\gamma$ |
|---|---|---|---|
| a single vertex | 1 | 1 face (the whole sphere) | 0 |
| a tree | $\prod_v (\deg v - 1)!$ | always 1 face | 0 |
| $K_4$ | $2^4 = 16$ | 4 faces: 2; 2 faces: 14 | 0 |
| $K_{3,3}$ | $2^6 = 64$ | 3 faces: 40; 1 face: 24 | 1 |
| $K_5$ | $6^5 = 7776$ | 5 faces: 462; 3 faces: 4974; 1 face: 2340 | 1 |

For $K_4$, $n - m = -2$, so 4 faces give genus $(2 + 2 - 4)/2 = 0$; only the 2 planar rotation systems (one per orientation of the plane drawing) reach it. For $K_{3,3}$, $n - m = -3$, and the best rotation systems have 3 faces, so $\gamma = (2 + 3 - 3)/2 = 1$. For $K_5$, $n - m = -5$, and the best have 5 faces, so $\gamma = 1$; the worst have 1 face, so $K_5$ also has a cellular embedding in $S_3$. A tree has one face for every rotation system, since face tracing walks once around the whole tree, so its genus is $(2 - n + (n - 1) - 1)/2 = 0$.

The counts grow fast: $K_7$ has $120^7 \approx 3.6 \cdot 10^{14}$ rotation systems, so brute force is hopeless already there, although $\gamma(K_7) = 1$ is known from the formula of Ringel and Youngs.

## Known algorithms

| algorithm | time | what it does |
|---|---|---|
| brute force over rotation systems | $O(m) \cdot \prod_v (\deg v - 1)!$ | exact; only for tiny graphs or for testing other code |
| edge bound from the Euler formula | $O(1)$ after counting | proves $\gamma \ge \lceil (m - 3n + 6)/6 \rceil$; never proves an upper bound |
| [planarity tests](/planarity-testing/) | $O(n)$ | the case $k = 0$ |
| Filotti, Miller and Reif (1979) | $n^{O(k)}$ | first polynomial algorithm for each fixed $k$ |
| forbidden minors and minor testing | $O(n^3)$ for each fixed $k$ | polynomial by the graph minor theorem, but the list of minors is not known, so this is not an algorithm one can write down |
| Mohar (1999) | $O(f(k) \, n)$ | linear for each fixed surface; returns an embedding or a forbidden subgraph |
| Kawarabayashi, Mohar and Reed (2008) | $O(f(k) \, n)$ | a simpler linear algorithm; also the exact genus of graphs of bounded [treewidth](/treewidth/) in linear time |
| integer programming and SAT models | exponential | exact in practice for graphs with a few dozen vertices |

The function $f$ in the linear algorithms grows very fast with $k$, so for $k$ beyond small values these algorithms are of theoretical interest; for practical work on small graphs, exact search with pruning by the face-length bounds, or a solver, is used.

## Bounds

- **NP-completeness.** Deciding $\gamma(G) \le k$, with $k$ in the input, is NP-complete (Thomassen, 1989). It is in NP because a rotation system is a certificate that is checked by face tracing. Thomassen later showed that it stays NP-complete for cubic graphs.
- **Fixed parameter.** For each fixed $k$, $O(f(k) \, n)$ time, so the problem is fixed-parameter tractable in $k$.
- **Lower bound for each $k$.** $\Omega(n + m)$ reads in the worst case, as for planarity.
- **Exact values for families.** For complete graphs $\gamma(K_n) = \lceil (n - 3)(n - 4)/12 \rceil$ (Ringel and Youngs, 1968), and for complete bipartite graphs $\gamma(K_{a,b}) = \lceil (a - 2)(b - 2)/4 \rceil$ (Ringel, 1965). These formulas are the Euler lower bound, which these graphs attain.

## Reductions

- **To blocks.** Genus is additive over blocks, so a solver for 2-connected graphs gives a solver for all graphs, with the blocks found by the [Hopcroft-Tarjan biconnectivity algorithm](/hopcroft-tarjan-biconnectivity/).
- **Planarity as the base case.** $\gamma(G) = 0$ if and only if $G$ is planar, so the problem contains planarity testing.
- **Hardness.** Thomassen's proof reduces an NP-complete problem to the question of whether a graph built from the instance has a triangular embedding, an embedding in which every face is a triangle, which is the case where the Euler lower bound is attained.

## Applications

- **Algorithms for graphs on surfaces.** Separators, shortest paths, flows and approximation schemes for planar graphs extend to graphs of bounded genus, but most of them need the embedding as input. Computing it is the first step.
- **Map colouring.** The genus of $K_n$ settles the Heawood map colour problem: the largest number of countries on $S_g$ that pairwise touch.
- **Graph drawing.** Drawing a non-planar graph on a torus or with few handles is one way to show its structure without crossings.
- **Structure theory.** Bounded genus is one of the building blocks of the structure theorem of Robertson and Seymour for graphs without a fixed minor.

## References
