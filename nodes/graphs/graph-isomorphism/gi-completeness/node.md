---
tag: TYQPXW
kind: concept
slug: gi-completeness
name: GI-completeness
aliases:
- GI-complete
- GI class
area: graphs/graph-isomorphism
level: advanced
summary: The class of problems polynomial-time equivalent to graph isomorphism; many natural problems are GI-complete.
prereqs: [graph-isomorphism-problem, polynomial-time-reduction, np-complete]
see_also: [graph-isomorphism-in-np, graph-automorphism, canonical-labeling, babai-quasipolynomial-algorithm, line-graph, subgraph-isomorphism]
sources:
  - paper: doi:10.1007/BF02104746
    title: V. N. Zemlyachenko, N. M. Korneenko and R. I. Tyshkevich, Graph isomorphism problem, Journal of Soviet Mathematics 29(4), 1426 to 1481 (1985)
    locator: Section 2 (isomorphism-complete classes of graphs and structures, and the reductions between them)
  - paper: "Kellogg S. Booth and Charles J. Colbourn, Problems polynomially equivalent to graph isomorphism, Technical Report CS-77-04, Department of Computer Science, University of Waterloo, 1979"
    locator: the whole report (a list of GI-complete problems with reductions)
  - paper: "Johannes Köbler, Uwe Schöning and Jacobo Torán, The Graph Isomorphism Problem: Its Structural Complexity, Birkhäuser, 1993"
    locator: Chapters 1 and 2 (the class GI, the reductions for counting and search, and lowness)
  - paper: doi:10.1016/0020-0190(79)90004-8
    title: Rudolf Mathon, A note on the graph isomorphism counting problem, Information Processing Letters 8(3), 131 to 132 (1979)
    locator: the whole note (counting isomorphisms is polynomial-time equivalent to deciding isomorphism)
---

A problem is GI-complete when it is polynomial-time equivalent to the [graph isomorphism problem](/graph-isomorphism-problem/): GI reduces to it, and it reduces to GI. The class GI consists of the problems that reduce to graph isomorphism in polynomial time. Many natural problems are GI-complete, such as isomorphism of bipartite graphs, regular graphs, directed graphs, line graphs, hypergraphs and finite automata, so a fast algorithm for any one of them would give a fast algorithm for all. GI is in NP but is not known to be in P or NP-complete, so GI-completeness marks a distinct level of difficulty. Babai's quasipolynomial algorithm applies to every problem in GI.

## In plain words

Some problems look different but are really the same puzzle in disguise. If you can change any instance of problem A into an instance of problem B quickly, without changing the answer, then a fast method for B also solves A. A problem is "as hard as graph isomorphism" when graph isomorphism can be changed into it, and "GI-complete" when the change also works the other way. Many questions about matching up structures, like two networks, two machines, or two families of sets, turn out to be GI-complete. Nobody knows a fast method for them, but nobody has proved they are as hard as the hardest problems in NP either.

## The idea

**Reductions.** A problem $A$ reduces to $B$, written $A \le_p B$, when a polynomial-time map $f$ sends instances of $A$ to instances of $B$ with the same answer. For isomorphism problems, $f$ maps a pair of structures $(X, Y)$ to a pair of graphs $(f(X), f(Y))$ with $X \cong Y$ exactly when $f(X) \cong f(Y)$; in most reductions $f$ is applied to each structure separately. Some results use Turing reductions, which may ask GI several times.

**The classes.** $\mathrm{GI}$ is the set of problems with $A \le_p$ graph isomorphism. A problem is GI-hard when graph isomorphism reduces to it, and GI-complete when it is GI-hard and in GI.

**Where GI sits.** Graph isomorphism is [in NP](/graph-isomorphism-in-np/), since an isomorphism is a short certificate, and in coAM, since non-isomorphism has an interactive proof. So if GI were NP-complete, the polynomial hierarchy would collapse to its second level (Boppana, Håstad and Zachos 1987; Schöning 1988). No polynomial-time algorithm is known. Babai (2015, published at STOC 2016) gave a quasipolynomial-time algorithm, $\exp((\log n)^{O(1)})$, which applies to every problem in the class.

**Typical reductions.** Graphs are simple and undirected unless stated.

- **Colored graphs to graphs.** Attach to each vertex of color $i$ a gadget, such as a path or a clique of a size that encodes $i$ and cannot occur elsewhere; isomorphisms of the result must keep the gadgets and so the colors.
- **Directed graphs to undirected graphs.** Replace each arc $u \to v$ by a path $u - x - y - v$ and mark the end at $u$ with a pendant vertex, or by colored subdivision vertices; the direction can be read back.
- **Graphs to bipartite graphs.** Subdivide each edge once to get $S(G)$. An isomorphism of $S(G)$ and $S(H)$ that maps original vertices to original vertices gives an isomorphism of $G$ and $H$, and conversely. For graphs of minimum degree at least 3 every isomorphism does this, since the subdivision vertices are exactly those of degree 2; in general, color the two sides.
- **Graphs to line graphs.** By Whitney's theorem, connected graphs other than $K_3$ and $K_{1,3}$ are isomorphic exactly when their [line graphs](/line-graph/) are, so isomorphism of line graphs is GI-complete, after handling the one exception.
- **Counting and search.** Counting the isomorphisms between two graphs (Mathon 1979), finding an isomorphism, and computing generators of the automorphism group all reduce to deciding GI by polynomially many queries, using colors to fix vertices one at a time.

## Examples

| problem | status |
|---|---|
| isomorphism of directed graphs, bipartite graphs, regular graphs, split graphs, chordal graphs, comparability graphs, line graphs, self-complementary graphs | GI-complete |
| isomorphism of hypergraphs, of finite automata, of semigroups, of finite structures with one binary relation | GI-complete |
| counting isomorphisms; finding an isomorphism; generators of $\mathrm{Aut}(G)$ | GI-complete under Turing reductions |
| deciding whether a graph has a non-trivial automorphism ([graph automorphism](/graph-automorphism/)) | in GI; not known to be GI-hard |
| group isomorphism, given multiplication tables | in GI; not known to be GI-hard; solvable in $n^{O(\log n)}$ time by a simple method |
| isomorphism of trees, planar graphs, interval graphs, graphs of bounded degree or bounded treewidth | in P |
| strongly regular graph isomorphism | in GI; not known to be GI-hard or in P |
| [subgraph isomorphism](/subgraph-isomorphism/) | NP-complete, so GI-hard but not in GI unless NP is in GI |

A computed example of the subdivision reduction: $C_6$ and $2K_3$ have 6 vertices and 6 edges each; their subdivisions are $C_{12}$ and $2C_6$, both bipartite, with 24 and 288 automorphisms, and they are not isomorphic, as $C_6$ and $2K_3$ are not. On 768 random pairs of graphs with the same numbers of vertices and edges and at most 6 vertices, the subdivided pair was isomorphic exactly when the original pair was.

## Where it is used

- **Classifying problems.** Showing that a new isomorphism question is GI-complete tells you not to expect a polynomial algorithm soon, and also not to expect NP-hardness.
- **Transferring algorithms.** Every problem in GI inherits Babai's quasipolynomial bound and the practical speed of tools such as [nauty](/nauty/) and [bliss](/bliss/), through the reduction to colored graphs.
- **Restricted classes.** For each class of graphs one asks whether isomorphism is in P or GI-complete. The dichotomies known for classes defined by forbidden induced subgraphs separate, for example, interval graphs (P) from chordal graphs (GI-complete).
- **Structural complexity.** GI is low for $\Sigma_2^p$ (Schöning 1988) and for $\mathrm{PP}$ (Köbler, Schöning and Torán 1992), facts used as evidence that GI is not NP-complete.

## References
