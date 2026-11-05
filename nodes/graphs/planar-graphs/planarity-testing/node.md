---
tag: HDX3B0
kind: problem
slug: planarity-testing
name: Planarity testing
aliases:
- planarity test
- planarity recognition
area: graphs/planar-graphs
level: intro
summary: Decide whether a given graph is planar.
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: Θ(n)}
prereqs: [planar-graph, planar-embedding]
see_also: [hopcroft-tarjan-planarity-test, boyer-myrvold-planarity-test, lempel-even-cederbaum-st-numbering, kuratowski-theorem, wagner-theorem, planar-edge-bound, dynamic-planarity-testing, graph-genus-computation]
sources:
  - paper: doi:10.1145/321850.321852
    title: John Hopcroft and Robert Tarjan, Efficient planarity testing, Journal of the ACM 21(4), 549 to 568 (1974)
    locator: the whole paper (the first linear-time planarity test)
  - paper: doi:10.7155/jgaa.00091
    title: John M. Boyer and Wendy J. Myrvold, On the cutting edge, simplified O(n) planarity by edge addition, Journal of Graph Algorithms and Applications 8(3), 241 to 273 (2004)
    locator: the whole paper (edge addition, and the extraction of a Kuratowski subgraph)
  - paper: doi:10.1016/S0022-0000(76)80045-1
    title: Kellogg S. Booth and George S. Lueker, Testing for the consecutive ones property, interval graphs, and graph planarity using PQ-tree algorithms, Journal of Computer and System Sciences 13(3), 335 to 379 (1976)
    locator: the linear-time implementation of the vertex addition test of Lempel, Even and Cederbaum
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 6.2, Characterization of planar graphs (Kuratowski's theorem and the path addition planarity algorithm)
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 4.4, Planar graphs (Kuratowski's theorem) and Section 4.5, Algebraic planarity criteria
  - paper: "Carsten Thomassen, The graph genus problem is NP-complete, Journal of Algorithms 10(4), 568 to 576 (1989)"
    locator: the whole paper
  - paper: "Bojan Mohar, A linear time algorithm for embedding graphs in an arbitrary surface, SIAM Journal on Discrete Mathematics 12(1), 6 to 26 (1999)"
    locator: the whole paper
---

Planarity testing is the problem of deciding whether a given [graph](/graph/) is [planar](/planar-graph/), that is, whether it can be drawn in the plane with no two edges crossing. Hopcroft and Tarjan solved it in linear time in 1974, and several other linear-time tests followed. A good test also gives a certificate: a [planar embedding](/planar-embedding/) when the answer is yes, and a subdivision of $K_5$ or $K_{3,3}$ ([Kuratowski's theorem](/kuratowski-theorem/)) when the answer is no.

## In plain words

You are given a network as a list of connections. The question is yes or no: can you draw it on paper without any crossing lines? Trying drawings by hand does not work for large networks, because the number of possible drawings grows very fast.

Good algorithms answer in time proportional to the size of the network. They also explain the answer. For yes, they give the drawing order around each point. For no, they point to a small part of the network that cannot be drawn without a crossing: five points that are all joined, or two groups of three points with every point of one group joined to every point of the other.

## Definition

**Input.** A finite undirected graph $G = (V, E)$ given by adjacency lists, with $n = |V|$ and $m = |E|$. Loops and parallel edges may be present; they do not change the answer.

**Output.** YES if there is a planar drawing of $G$: points for the vertices and arcs for the edges such that two arcs meet only at a common end. NO otherwise.

**Equivalent conditions.** By [Kuratowski's theorem](/kuratowski-theorem/) and [Wagner's theorem](/wagner-theorem/), the answer is YES if and only if $G$ contains no subdivision of $K_5$ or $K_{3,3}$, if and only if $G$ has no $K_5$ or $K_{3,3}$ [minor](/graph-minor/). By the combinatorial form of [Euler's formula](/euler-formula/), it is YES if and only if some [rotation system](/rotation-system/) of $G$ has $f = m - n + 2c$ faces, with $c$ the number of components.

**Certifying output.**

- For YES, a rotation system with the face count above. A checker verifies it with [planar face finding](/planar-face-finding/) in $O(n + m)$ time.
- For NO, a subgraph $H \subseteq G$ that is a subdivision of $K_5$ or $K_{3,3}$. A checker verifies it by suppressing the vertices of degree 2 of $H$ and comparing with the two graphs.

## Variants

- **Embedding.** Output the embedding itself: the [planar embedding](/planar-embedding/) problem.
- **Online and dynamic.** Edges arrive one by one, or are inserted and deleted, and the test is repeated after each change: see [dynamic planarity testing](/dynamic-planarity-testing/).
- **Other surfaces.** Does $G$ embed on the surface of genus $g$? For each fixed $g$ this is decidable in linear time (Mohar), but deciding the [genus](/graph-genus/) when $g$ is part of the input is NP-complete (Thomassen). See [graph genus computation](/graph-genus-computation/).
- **Restricted classes.** [Outerplanarity](/outerplanar-graph/) (no $K_4$ or $K_{2,3}$ minor) is tested in linear time by adding one vertex adjacent to all others and testing planarity. Upward planarity of a directed graph is NP-complete in general.
- **Maximum planar subgraph.** Delete as few edges as possible to make $G$ planar. This is NP-hard; see the [planarization heuristic](/planarization-heuristic/).

## Examples

| graph | $n$ | $m$ | answer | certificate |
|---|---|---|---|---|
| a single vertex | 1 | 0 | YES | the empty rotation |
| any [tree](/tree/) | $n$ | $n - 1$ | YES | any rotation system |
| $K_4$ | 4 | 6 | YES | a triangle with the fourth vertex inside |
| the wheel $W_5$ (a 5-cycle and a hub) | 6 | 10 | YES | the hub inside the cycle |
| the cube $Q_3$ | 8 | 12 | YES | a square inside a square |
| $K_{3,3} - e$ | 6 | 8 | YES | 2 of its 16 rotation systems are planar |
| $K_5$ | 5 | 10 | NO | $K_5$ itself |
| $K_{3,3}$ | 6 | 9 | NO | $K_{3,3}$ itself |
| the Petersen graph | 10 | 15 | NO | the graph minus any one vertex is a subdivision of $K_{3,3}$; contracting the 5 spokes gives a $K_5$ minor |
| $K_{3,3}$ plus 3 isolated vertices | 9 | 9 | NO | $K_{3,3}$; the edge count $9 \le 21$ does not help |

The edge test $m \le 3n - 6$ (the [planar edge bound](/planar-edge-bound/)) proves NO for $K_5$ at once, and the bound $m \le 2n - 4$ for triangle-free graphs proves NO for $K_{3,3}$. For the Petersen graph the girth-5 bound $m \le \frac{5}{3}(n - 2)$ gives $15 > 13.3$. The last row shows that counting edges is not a complete test.

**A walk through a path addition test on $K_{3,3}$.** Let the sides be $\{a_1, a_2, a_3\}$ and $\{b_1, b_2, b_3\}$. Embed the cycle $a_1 b_1 a_2 b_2 a_3 b_3$; it has an inside and an outside face. The three remaining edges $a_1 b_2$, $a_2 b_3$ and $a_3 b_1$ each join two vertices of the cycle. Any two of them have ends that alternate around the cycle, so they cannot lie in the same face. Three chords and only two faces means two chords share a face, so the graph is not planar.

## Known algorithms

| algorithm | time | method |
|---|---|---|
| test the edge bound | $O(1)$ after counting | proves NO when $m > 3n - 6$; never proves YES |
| brute force over rotation systems | $\prod_v (\deg v - 1)!$ face traces | for tiny graphs and for testing other code |
| path addition (Demoucron, Malgrange and Pertuiset) | $O(n^2)$ | add paths of fragments into faces that can hold them |
| [Hopcroft-Tarjan](/hopcroft-tarjan-planarity-test/) | $O(n)$ | path addition in the order of a depth-first search |
| [Lempel-Even-Cederbaum](/lempel-even-cederbaum-st-numbering/) with PQ-trees (Booth and Lueker) | $O(n)$ | vertex addition in an [st-numbering](/st-numbering/) order |
| [Boyer-Myrvold](/boyer-myrvold-planarity-test/) | $O(n)$ | edge addition along a DFS tree, with a Kuratowski subgraph on failure |
| left-right planarity of de Fraysseix and Rosenstiehl | $O(n)$ | a DFS tree is planar-compatible if and only if a 2-coloring of its back edges exists |

All the linear tests reduce first to the [biconnected components](/biconnected-components/), since a graph is planar if and only if each block is planar, and first check the edge bound, so that the rest of the run costs $O(n)$.

## Bounds

- **Upper bound.** $O(n)$ time on a [word RAM](/word-ram/), with $n$ the number of vertices, after an $O(\min(m, 3n))$ scan of the input.
- **Lower bound.** $\Omega(n)$ reads of the adjacency lists in the worst case. Let $G$ be a [maximal planar graph](/maximal-planar-graph/) on $n$ vertices; adding any edge $uw$ between non-adjacent vertices makes it non-planar. If on input $G$ an algorithm reads neither the list of $u$ nor the list of $w$ to its end, it runs the same on $G + uw$ (with $uw$ placed at the end of both lists) and gives the same answer, which is wrong for one of the two inputs. So the vertices whose lists are not read to the end are pairwise adjacent in $G$, and a planar graph has no clique of more than 4 vertices. The algorithm reads the full lists of at least $n - 4$ vertices. The linear algorithms are therefore optimal up to a constant factor.
- **Space.** $\Theta(n)$ words.

## Reductions

- **To embedding.** A constructive test (embedding or refusal) answers the decision question.
- **To the blocks.** $G$ is planar if and only if every biconnected component is planar. So a test for 2-connected graphs, run on the blocks from the [Hopcroft-Tarjan biconnectivity algorithm](/hopcroft-tarjan-biconnectivity/), gives a test for all graphs.
- **Outerplanarity to planarity.** $G$ is outerplanar if and only if $G$ plus a new vertex joined to all vertices is planar.
- **Planarity as a matroid property.** $G$ is planar if and only if its cycle matroid is cographic (Whitney's duality theorem). This is a characterization, not a fast algorithm.

## Applications

- **Circuit layout.** A circuit that is planar can be laid out on one layer with no crossing wires. A non-planar one needs vias or more layers.
- **Graph drawing.** The first step of the planarization method of [graph drawing](/graph-drawing/) is a planarity test, then a maximal planar subgraph, then edge insertion ([planarization heuristic](/planarization-heuristic/)).
- **A gate for planar algorithms.** Before running a [planar separator](/lipton-tarjan-separator/), a [planar shortest path](/planar-shortest-paths/) algorithm or a planar isomorphism test, a program tests planarity and computes the embedding.
- **Chemistry and biology.** Planarity of molecular graphs and of RNA secondary structures (which are [outerplanar](/outerplanar-graph/) when drawn on a circle) is used to classify structures.

## References
