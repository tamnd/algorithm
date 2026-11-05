---
tag: 8NJ7TJ
kind: problem
slug: planar-embedding
name: Planar embedding
aliases:
- combinatorial embedding
- planar drawing
area: graphs/planar-graphs
level: intro
summary: Find a planar drawing or a rotation system describing one.
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: Θ(n)}
prereqs: [planar-graph, rotation-system]
see_also: [planarity-testing, boyer-myrvold-planarity-test, hopcroft-tarjan-planarity-test, planar-face-finding, planar-straight-line-drawing, kuratowski-theorem, graph-genus-computation, euler-formula]
sources:
  - paper: doi:10.1145/321850.321852
    title: John Hopcroft and Robert Tarjan, Efficient planarity testing, Journal of the ACM 21(4), 549 to 568 (1974)
    locator: the whole paper (the linear-time test by path addition)
  - paper: doi:10.7155/jgaa.00091
    title: John M. Boyer and Wendy J. Myrvold, On the cutting edge, simplified O(n) planarity by edge addition, Journal of Graph Algorithms and Applications 8(3), 241 to 273 (2004)
    locator: the whole paper (the embedding and the Kuratowski subgraph in linear time)
  - paper: doi:10.1016/0022-0000(85)90004-2
    title: Norishige Chiba, Takao Nishizeki, Shigenobu Abe and Takao Ozawa, A linear algorithm for embedding planar graphs using PQ-trees, Journal of Computer and System Sciences 30(1), 54 to 76 (1985)
    locator: the whole paper (the embedding phase after a PQ-tree planarity test)
  - book: isbn:9780801866890
    title: Bojan Mohar and Carsten Thomassen, Graphs on Surfaces, Johns Hopkins University Press, 2001
    locator: Chapter 2, Planar graphs (the planarity algorithm), and Chapters 3 and 4 (embeddings described by rotation systems)
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 4.3, Drawings (equivalent embeddings, and Whitney's theorem that 3-connected planar graphs have a unique embedding)
  - paper: "G. Demoucron, Y. Malgrange and R. Pertuiset, Graphes planaires: reconnaissance et construction de représentations planaires topologiques, Revue Française de Recherche Opérationnelle 8, 33 to 47 (1964)"
    locator: the path addition algorithm
  - paper: doi:10.1016/S0022-0000(76)80045-1
    title: Kellogg S. Booth and George S. Lueker, Testing for the consecutive ones property, interval graphs, and graph planarity using PQ-tree algorithms, Journal of Computer and System Sciences 13(3), 335 to 379 (1976)
    locator: the PQ-tree and its use in the vertex addition planarity test
  - paper: "Kurt Mehlhorn and Petra Mutzel, On the embedding phase of the Hopcroft and Tarjan planarity testing algorithm, Algorithmica 16(2), 233 to 242 (1996)"
    locator: the whole paper
  - paper: doi:10.1137/S0097539794277123
    title: Ashim Garg and Roberto Tamassia, On the computational complexity of upward and rectilinear planarity testing, SIAM Journal on Computing 31(2), 601 to 625 (2001)
    locator: the NP-completeness of upward planarity testing
---

The planar embedding problem asks, for a given [graph](/graph/), for a planar embedding of it: a [rotation system](/rotation-system/) (the cyclic order of the neighbours at each vertex) that a crossing-free drawing realizes, or a proof that none exists. It is the constructive form of [planarity testing](/planarity-testing/), and it is solvable in $\Theta(n)$ time. Most algorithms for [planar graphs](/planar-graph/) need this embedding as input, not only the graph.

## In plain words

You are given a network as a list of who is connected to whom. You want to draw it with no crossing lines. Before choosing exact positions, it is enough to decide, around each point, in which circular order its lines leave it. If these orders are right, the regions of the drawing are fixed, and a drawing program can then place the points.

So the problem is: find such a circular order for each point that gives a crossing-free drawing, or show that no drawing without crossings exists. Fast algorithms do this in time proportional to the size of the network.

## Definition

**Input.** A finite undirected graph $G = (V, E)$, given by adjacency lists, with $n = |V|$ and $m = |E|$.

**Output.** One of:

- **an embedding**: a rotation system $\rho = (\rho_v)_{v \in V}$, where $\rho_v$ is a cyclic order of the edges at $v$, such that the number $f$ of cycles of the face map $\varphi(u, v) = (v, \rho_v^{-1}(u))$ satisfies
$$n - m + f = 2c,$$
where $c$ is the number of connected components and the faces are traced in each component on its own. By the combinatorial form of [Euler's formula](/euler-formula/), this holds if and only if each component of $\rho$ describes a drawing on the sphere. Any face of each component can then be chosen as the outer face of a plane drawing.
- **a refusal**, usually with a certificate: a subgraph of $G$ that is a subdivision of $K_5$ or of $K_{3,3}$ ([Kuratowski's theorem](/kuratowski-theorem/)).

Two rotation systems describe the same embedding on the sphere when they are equal, and the same embedding up to a mirror when one is the reverse of the other at every vertex. The output is one embedding, not all of them.

**How the answer is given and checked.** The rotation system is a list of $2m$ darts in cyclic order around each vertex, or the equivalent [doubly connected edge list](/doubly-connected-edge-list/). A checker traces the faces in $O(n + m)$ time ([planar face finding](/planar-face-finding/)) and tests the equation above. A Kuratowski subgraph is checked by contracting its vertices of degree 2 and testing for $K_5$ or $K_{3,3}$.

## Variants

- **Decision only.** Is $G$ planar? This is [planarity testing](/planarity-testing/).
- **Straight-line drawing.** Output coordinates such that straight segments for the edges do not cross. Each planar graph has one ([Fáry's theorem](/fary-theorem/)), and one on an $O(n) \times O(n)$ integer grid exists and can be found in linear time ([de Fraysseix-Pach-Pollack](/de-fraysseix-pach-pollack/), [Schnyder drawing](/schnyder-drawing/)). See [planar straight-line drawing](/planar-straight-line-drawing/).
- **Fixed outer face or fixed edge order.** Ask for an embedding in which given vertices lie on the outer face. For one vertex or one edge this costs nothing extra, because any face can be made the outer face.
- **All embeddings.** For a 2-connected graph, the SPQR tree encodes all its planar embeddings in linear space. A 3-connected planar graph has exactly one embedding up to mirror image (Whitney; Diestel, Section 4.3).
- **Embedding on other surfaces.** Find a rotation system with $n - m + f = 2 - 2g$ for the least $g$: this is [graph genus computation](/graph-genus-computation/), and it is NP-hard in general.
- **Upward planarity.** For a directed graph, ask for a planar drawing in which each edge goes upward. This is NP-complete (Garg and Tamassia, 2001).
- **Dynamic embedding.** Keep an embedding while edges are inserted and deleted; see [dynamic planarity testing](/dynamic-planarity-testing/).

## Examples

The table counts rotation systems by brute force. A vertex of degree $d$ has $(d-1)!$ cyclic orders.

| graph | $n$ | $m$ | rotation systems | planar ones | answer |
|---|---|---|---|---|---|
| a single vertex | 1 | 0 | 1 | 1 | the empty rotation |
| a star with 3 leaves (a tree) | 4 | 3 | 2 | 2 | every rotation system of a tree is planar |
| $K_4$ | 4 | 6 | 16 | 2 | one embedding and its mirror |
| $K_{2,4}$ | 6 | 8 | 36 | 6 | three embeddings, each with its mirror |
| $K_5 - e$ | 5 | 9 | 864 | 2 | one embedding and its mirror |
| $K_5$ | 5 | 10 | 7776 | 0 | not planar; the best rotation gives $f = 5$, genus 1 |
| $K_{3,3}$ | 6 | 9 | 64 | 0 | not planar; the best rotation gives $f = 3$, genus 1 |

**$K_4$ in full.** With vertex 3 inside the triangle $0, 1, 2$, a planar answer is $\rho_0 = (1, 3, 2)$, $\rho_1 = (2, 3, 0)$, $\rho_2 = (0, 3, 1)$, $\rho_3 = (0, 1, 2)$. Its faces are $(0, 1, 3)$, $(0, 3, 2)$, $(1, 2, 3)$ and $(0, 2, 1)$, so $f = 4$ and $4 - 6 + 4 = 2$. The rotation system with $\rho_v$ in increasing order at every vertex has only $f = 2$ faces, and it is rejected.

**A tree** on any number of vertices: each rotation system has one facial walk of length $2(n-1)$, so $n - (n - 1) + 1 = 2$. Any order of the neighbours is a valid answer.

**$K_{3,3}$:** the algorithm refuses, and the certificate is the whole graph, which is itself a Kuratowski subgraph.

## Known algorithms

| algorithm | time | notes |
|---|---|---|
| exhaustive search over rotation systems | $\prod_v (\deg v - 1)!$ face traces | only for tiny graphs |
| path addition of Demoucron, Malgrange and Pertuiset (1964) | $O(n^2)$ | embeds a cycle, then adds paths of fragments into faces |
| [Hopcroft-Tarjan planarity test](/hopcroft-tarjan-planarity-test/) (1974) | $O(n)$ | path addition in DFS order; the embedding phase was worked out later (Mehlhorn and Mutzel, 1996) |
| [Lempel-Even-Cederbaum](/lempel-even-cederbaum-st-numbering/) vertex addition with PQ-trees (Booth and Lueker, 1976) | $O(n)$ | needs an [st-numbering](/st-numbering/); embedding by Chiba, Nishizeki, Abe and Ozawa (1985) |
| [Boyer-Myrvold edge addition](/boyer-myrvold-planarity-test/) (2004) | $O(n)$ | outputs the embedding or a Kuratowski subgraph directly |
| left-right (Trémaux) planarity test of de Fraysseix and Rosenstiehl | $O(n)$ | a characterization of planarity by a DFS tree |

Every linear algorithm first checks $m \le 3n - 6$ (for $n \ge 3$, after removing loops and parallel edges) and refuses if it fails, so that $m = O(n)$ in the rest of the run.

## Bounds

- **Upper bound.** $O(n)$ time on a [word RAM](/word-ram/), by the algorithms above, where $n$ is the number of vertices. The edge test makes the bound independent of $m$ beyond reading the input.
- **Lower bound.** $\Omega(n)$, because the output names every edge. When the input has $m > 3n - 6$ edges, the answer "not planar" follows from reading $3n - 5$ of them.
- **Space.** $\Theta(n)$ words.

## Reductions

- **From planarity testing.** Testing reduces to embedding: run the embedding algorithm and report whether it refused. The converse also holds in practice, because the linear tests are constructive.
- **To face finding.** From an embedding, [planar face finding](/planar-face-finding/) gives the faces and the [planar dual graph](/planar-dual-graph/) in $O(n)$ time.
- **To straight-line drawing.** Triangulate the embedding (add edges inside each face until all faces are triangles), then apply a grid drawing algorithm and delete the added edges: $O(n)$ in total.
- **Blocks.** A graph is planar if and only if each of its [biconnected components](/biconnected-components/) is planar. Embeddings of the blocks combine into an embedding of the graph: at a cut vertex, place the rotation of each block as one contiguous interval.

## Applications

- The first step of nearly every planar graph algorithm: [separators](/lipton-tarjan-separator/), [planar shortest paths](/planar-shortest-paths/), [r-divisions](/r-division/), the [five-color algorithm](/five-color-algorithm/) in its linear form, and [planar graph isomorphism](/planar-graph-isomorphism/).
- [Graph drawing](/graph-drawing/): VLSI layout, schematic diagrams and map labeling use a planar embedding when the graph is planar, and a [planarization](/planarization-heuristic/) of it when it is not.
- Mesh processing: a triangle mesh of a surface patch is stored as an embedding, as a [doubly connected edge list](/doubly-connected-edge-list/) or a similar structure.

## References
