---
tag: 7BAR3P
kind: concept
slug: book-embedding
name: Book embedding
aliases:
- book thickness
- page number
area: graphs/planar-graphs
level: advanced
summary: Embedding of a graph with vertices on a spine and edges assigned to pages; planar graphs have book thickness at most 4.
prereqs: [planar-graph, outerplanar-graph, hamiltonian-cycle, graph-coloring]
see_also: [graph-drawing, crossing-number, maximal-planar-graph, jordan-curve-theorem, bipartite-testing, stack, hamiltonian-cycle-problem, graph-genus]
sources:
  - paper: doi:10.1016/0095-8956(79)90021-2
    title: Frank Bernhart and Paul C. Kainen, The book thickness of a graph, Journal of Combinatorial Theory, Series B 27(3), 320 to 331 (1979)
    locator: the definitions, the characterizations of one-page and two-page graphs, and the book thickness of complete graphs
  - paper: doi:10.1016/0022-0000(89)90032-9
    title: Mihalis Yannakakis, Embedding planar graphs in four pages, Journal of Computer and System Sciences 38(1), 36 to 67 (1989)
    locator: the four-page algorithm for planar graphs
  - paper: doi:10.1137/0608002
    title: Fan R. K. Chung, Frank Thomson Leighton and Arnold L. Rosenberg, Embedding graphs in books, a layout problem with applications to VLSI design, SIAM Journal on Algebraic and Discrete Methods 8(1), 33 to 58 (1987)
    locator: the layout model, the applications, and the bounds for standard graph families
  - paper: "Michael A. Bekos, Michael Kaufmann, Fabian Klute, Sergey Pupyrev, Chrysanthi Raftopoulou and Torsten Ueckerdt, Four pages are indeed necessary for planar graphs, Journal of Computational Geometry 11(1), 332 to 353 (2020)"
    locator: the planar graph that needs four pages
---

A book embedding of a graph puts the vertices in order on a line, the *spine*, and puts each edge on one of several half-planes, the *pages*, that meet at the spine, so that edges on the same page do not cross. The **book thickness** (or page number) of a graph is the least number of pages that it needs. Graphs of book thickness 1 are the [outerplanar graphs](/outerplanar-graph/), graphs of book thickness at most 2 are the subgraphs of Hamiltonian [planar graphs](/planar-graph/), and every planar graph has book thickness at most 4 (Yannakakis, 1989), which is tight.

## In plain words

Think of an open book. The vertices sit in a row along the spine. Each edge is drawn as an arc on one page, from one vertex to another. Two arcs on the same page must not cross. The question is how many pages a graph needs.

A page cannot hold two arcs whose ends alternate along the spine, since such arcs always cross. So a page holds a set of arcs that nest or sit side by side, like matched brackets.

Some graphs fit on one page, such as trees and polygons with diagonals that do not cross. Planar graphs never need more than four pages. A complete graph on many vertices needs about half as many pages as it has vertices.

## The idea

**How the embedding is given.** A book embedding is purely combinatorial. It is given by a linear order $\sigma$ of the vertices (the spine order) and a page assignment $p : E \to \{1, \ldots, k\}$. No coordinates and no [rotation system](/rotation-system/) are needed. The algorithms that build book embeddings of planar graphs take a planar embedding, given as a rotation system, as their input.

**Definition.** Two edges $ab$ and $cd$ with $\sigma(a) < \sigma(b)$ and $\sigma(c) < \sigma(d)$ *conflict* if their ends alternate:

$$\sigma(a) < \sigma(c) < \sigma(b) < \sigma(d) \quad \text{or} \quad \sigma(c) < \sigma(a) < \sigma(d) < \sigma(b).$$

A $k$-page book embedding is a pair $(\sigma, p)$ such that no two edges with the same page conflict. The book thickness $\mathrm{bt}(G)$ is the least such $k$; a graph without edges has $\mathrm{bt}(G) = 0$.

**Why alternating arcs cross.** Draw the spine as the $x$-axis and each page as the upper half-plane. An arc from $a$ to $b$ splits the half-plane into an inside and an outside, and the spine points strictly between $a$ and $b$ are on the inside boundary. If $c$ lies between $a$ and $b$ and $d$ lies outside, the arc from $c$ to $d$ starts inside and ends outside, so by the [Jordan curve theorem](/jordan-curve-theorem/) it meets the first arc. If the ends do not alternate, the two arcs can be drawn as disjoint half-circles. So the drawing condition and the combinatorial condition agree.

**Pages as a coloring problem.** For a fixed spine order, the edges form a *conflict graph* with an edge between conflicting pairs, and a valid page assignment is exactly a proper [coloring](/graph-coloring/) of it. So:

- Checking a given $(\sigma, p)$ is a check of all pairs on each page, or, faster, one scan per page with a [stack](/stack/): walk the spine, and at each vertex first close the arcs that end there and then open the arcs that start there. A page is valid exactly when every closing arc is on top of the stack, as with balanced brackets.
- For a fixed order, deciding whether 2 pages suffice is [bipartiteness testing](/bipartite-testing/) of the conflict graph.
- For a fixed order and $k \ge 4$ pages, the problem is coloring a circle graph, which is NP-complete (Garey, Johnson, Miller and Papadimitriou, 1980).
- Without a fixed order, deciding $\mathrm{bt}(G) \le 2$ is NP-complete (Wigderson, 1982), because for a maximal planar graph it is the same as deciding whether the graph has a [Hamiltonian cycle](/hamiltonian-cycle/).

**One page.** A graph has a one-page embedding exactly when it is outerplanar (Bernhart and Kainen). If $G$ is outerplanar, take the spine order along the boundary of the outer face; edges are chords of a convex polygon that do not cross, so they do not alternate. Conversely, from a one-page embedding, put the vertices on a circle in spine order and draw every edge as a straight chord; nonconflicting chords do not cross, and all vertices are on the outer face.

**Two pages.** A graph has a two-page embedding exactly when it is a subgraph of a planar graph with a Hamiltonian cycle (Bernhart and Kainen). One direction is short. Let $C = v_1 v_2 \cdots v_n v_1$ be a Hamiltonian cycle of a plane graph $H \supseteq G$, and use $v_1, \ldots, v_n$ as the spine order. Each edge of $H$ not on $C$ lies inside or outside $C$. Two edges inside $C$ do not cross, so by the Jordan curve argument above their ends do not alternate along $C$; the same holds outside. Put the inside edges and the edges of $C$ on page 1 and the outside edges on page 2. The edge $v_1 v_n$ spans all other vertices, so it conflicts with no edge. For the converse, add the spine edges $v_1 v_2, \ldots, v_{n-1} v_n, v_n v_1$; drawing page 1 above and page 2 below the spine gives a plane Hamiltonian supergraph.

**Planar graphs.** By the two-page result, a planar graph that is a subgraph of a Hamiltonian planar graph needs at most 2 pages. Not all planar graphs are: some maximal planar graphs are not Hamiltonian, and they need more pages. Whitney (1931) showed that a maximal planar graph without separating triangles is Hamiltonian, and Tutte (1956) that every 4-connected planar graph is Hamiltonian; such graphs have book thickness at most 2. For all planar graphs, Buss and Shor (1984) gave 9 pages, Heath (1984) 7 pages, and Yannakakis (1989) 4 pages, with a linear-time algorithm that works on the layers of an embedded graph. Yannakakis also announced a planar graph that needs 4 pages; a full proof was published by Bekos, Kaufmann, Klute, Pupyrev, Raftopoulou and Ueckerdt (2020).

**Complete graphs.** $\mathrm{bt}(K_n) = \lceil n/2 \rceil$ for $n \ge 4$ (Bernhart and Kainen). For the lower bound, call the $n$ edges between neighbours in the cyclic spine order (including the edge from the first to the last vertex) spine edges; they conflict with nothing. The other edges on one page are chords of a convex $n$-gon that do not cross, so a page holds at most $n - 3$ of them. $K_n$ has $n(n-1)/2 - n = n(n-3)/2$ such edges, so it needs at least $n/2$ pages. Bernhart and Kainen give a construction with $\lceil n/2 \rceil$ pages.

## Examples

The values were checked by computer with an exhaustive search over spine orders and page assignments.

| graph | $\mathrm{bt}$ | reason |
|---|---|---|
| a single vertex | 0 | no edges |
| a tree with an edge | 1 | trees are outerplanar |
| a cycle $C_n$ | 1 | the order along the cycle; the closing edge spans all others |
| $K_4$ | 2 | planar and Hamiltonian, but not outerplanar |
| octahedron $K_{2,2,2}$ | 2 | 4-connected planar, hence Hamiltonian |
| $K_5$ | 3 | not planar, so not 2 pages; $\lceil 5/2 \rceil = 3$ |
| $K_{3,3}$ | 3 | not planar, so not 2 pages; 3 pages suffice |
| Petersen graph | 3 | not planar; 3 pages suffice |
| $K_6$ | 3 | $\lceil 6/2 \rceil = 3$ |
| $K_7$ | 4 | $\lceil 7/2 \rceil = 4$, more than any planar graph needs |

**$K_4$ in two pages.** Use the spine order $1, 2, 3, 4$. The edges $12, 23, 34, 14, 13$ do not conflict with each other: $13$ and $14$ share an end, and $13$ nests inside $14$. The edge $24$ conflicts with $13$, since $1 < 2 < 3 < 4$, so it goes on page 2. The other spine orders of $K_4$ also have an alternating pair, because any four vertices in order $a < b < c < d$ give the conflicting edges $ac$ and $bd$. So one page is not enough.

**$K_5$ needs three pages.** If $K_5$ had a two-page embedding, adding the spine edges would give a planar supergraph of $K_5$, but $K_5$ is not planar ([Kuratowski's theorem](/kuratowski-theorem/)). The same argument works for $K_{3,3}$ and for every graph that is not planar: $\mathrm{bt}(G) \le 2$ implies that $G$ is planar.

## Where it is used

- **VLSI and fault-tolerant processor arrays.** Chung, Leighton and Rosenberg (1987) introduced book embeddings as a model for laying out a processor network with a row of processors and wiring layers, and for configuring processor arrays around faulty processors.
- **Stack layouts and sorting with stacks.** Each page behaves as a stack when the spine is scanned, so a $k$-page embedding is a *$k$-stack layout*. The dual notion, where each page behaves as a queue, is the queue layout. These layouts appear in the analysis of sorting with parallel stacks and in multi-layer printed circuit routing.
- **Graph drawing.** Two-page embeddings give [drawings](/graph-drawing/) with all vertices on a line and edges as half-circles above or below it, and arc diagrams are one-page or two-page layouts. Fixed-order layouts relate to the [crossing number](/crossing-number/): the minimum number of crossings in a two-page drawing is the two-page crossing number.
- **Structure of graph classes.** Graphs of bounded [genus](/graph-genus/) and graphs of bounded treewidth have bounded book thickness, and book thickness bounds the number of edges: a $k$-page graph with $n \ge 3$ vertices has fewer than $(k + 1) n$ edges, since each page is outerplanar.

## References
