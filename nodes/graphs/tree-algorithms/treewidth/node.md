---
tag: F530RK
kind: concept
slug: treewidth
name: Treewidth
aliases:
- tree-width
area: graphs/tree-algorithms
level: advanced
summary: The minimum width of a tree decomposition, minus one; a measure of how tree-like a graph is.
prereqs: [tree-decomposition, graph-minor]
see_also: [treewidth-computation, path-decomposition, grid-minor-theorem, courcelle-theorem, dp-on-tree-decompositions, chordal-graph, planar-separator-theorem, fixed-parameter-tractable]
sources:
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Łukasz Kowalik, Daniel Lokshtanov, Dániel Marx, Marcin Pilipczuk, Michał Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 7 (Treewidth), the definition, the balanced separator lemma, the treewidth of grids and of planar graphs, and dynamic programming on graphs of bounded treewidth
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Chapter 12 (Minors, trees and WQO), the sections on tree-decompositions and on tree-width and forbidden minors, with brambles and the duality theorem
  - paper: Neil Robertson and Paul D. Seymour, Graph minors. II. Algorithmic aspects of tree-width, Journal of Algorithms 7(3), 309 to 322 (1986)
    locator: the definition of tree-width
  - paper: Paul D. Seymour and Robin Thomas, Graph searching and a min-max theorem for tree-width, Journal of Combinatorial Theory, Series B 58(1), 22 to 33 (1993)
    locator: the duality between tree-width and brambles, and the game of cops and a visible robber
---

The treewidth $\mathrm{tw}(G)$ of a graph $G$ is the least width of a [tree decomposition](/tree-decomposition/) of $G$, where the width is the size of the largest bag minus one. It measures how far $G$ is from a tree: forests have treewidth at most 1, cycles 2, the $k \times k$ grid $k$, and the complete graph $K_n$ has $n - 1$. Many NP-hard problems take time $f(k) \cdot n$ on graphs of treewidth $k$, so treewidth is the main structural parameter of [parameterized algorithms](/fixed-parameter-tractable/). It does not grow when edges or vertices are deleted or edges are contracted, and by the [grid minor theorem](/grid-minor-theorem/) a graph of large treewidth contains a large grid as a [minor](/graph-minor/).

## In plain words

Some graphs are trees, some are almost trees, and some are tangled everywhere. Treewidth is a number that says which. A graph has small treewidth if you can take it apart, again and again, by removing only a few vertices at a time, and the pieces hang together like the branches of a tree.

A tree needs only one vertex removed to fall into pieces, and so do all its pieces, so its treewidth is 1. A ring needs two. A square grid with $k$ rows needs about $k$, since any cut that splits it in half must cross a whole row or column. A graph in which every vertex is linked to every other cannot be split at all, so its treewidth is as large as it can be. Problems that are hard in general are often easy when this number is small.

## The idea

**Definition.** For a graph $G = (V, E)$ with $n \ge 1$ vertices,

$$\mathrm{tw}(G) = \min \{\, \max_t |X_t| - 1 \;:\; (T, \{X_t\}) \text{ a tree decomposition of } G \,\}.$$

The graph is simple, undirected and not weighted. Vertex numbers play no role. The minus one gives the value 1 to trees with at least one edge, and 0 to graphs with no edges.

**Equivalent forms.**

- **Elimination orders.** $\mathrm{tw}(G)$ is the least, over all orders of $V$, of the largest number of later neighbours a vertex has when the vertices are eliminated in order and the later neighbours of each eliminated vertex are joined into a clique. See [elimination ordering](/elimination-ordering/).
- **Chordal supergraphs.** $\mathrm{tw}(G) + 1$ is the least clique number of a [chordal graph](/chordal-graph/) on $V$ that contains $G$. The maximal cliques of a chordal graph are the bags of a tree decomposition.
- **$k$-trees.** A $k$-tree is built from a clique of $k + 1$ vertices by adding vertices one at a time, each joined to a clique of $k$ old vertices. The graphs of treewidth at most $k$ are exactly the subgraphs of $k$-trees, the partial $k$-trees.
- **Brambles and a game.** Seymour and Thomas proved that $\mathrm{tw}(G) + 1$ equals the largest order of a bramble, a family of connected vertex sets that touch two by two, and the number of cops needed to catch a visible, fast robber.

**Basic facts.**

- **Minors.** If $H$ is a [minor](/graph-minor/) of $G$, then $\mathrm{tw}(H) \le \mathrm{tw}(G)$. So for each $k$ the graphs of treewidth at most $k$ form a minor-closed class, defined by finitely many forbidden minors, by the [graph minor theorem](/graph-minor-theorem/). For $k = 1$ the forbidden minor is the triangle, and for $k = 2$ it is $K_4$.
- **Cliques.** Every clique lies in a bag, so $\mathrm{tw}(G) \ge \omega(G) - 1$.
- **Sparsity.** A graph of treewidth $k$ has a vertex of degree at most $k$, so it is $k$-degenerate, has at most $kn$ edges, and can be colored with $k + 1$ colours.
- **Separators.** A graph of treewidth $k$ has, for every vertex set $W$, a set of at most $k + 1$ vertices whose removal leaves no component with more than half of $W$. A converse holds up to a constant factor, which is what the [construction algorithm](/tree-decomposition-construction/) uses.
- **Deleting a vertex** lowers the treewidth by at most 1, and the treewidth of a graph is the largest treewidth of its components.
- **Path decompositions.** The pathwidth satisfies $\mathrm{tw}(G) \le \mathrm{pw}(G) = O(\mathrm{tw}(G) \log n)$; see [path decomposition](/path-decomposition/).

## Examples

| graph | treewidth | why |
|---|---|---|
| a single vertex, or no edges | 0 | one bag per vertex |
| a tree or forest with an edge, such as a path or a star | 1 | one bag per edge; an edge needs a bag of size 2 |
| a cycle $C_n$, $n \ge 3$ | 2 | bags $\{0, i, i+1\}$; a cycle is not a forest |
| an outerplanar graph, or a series-parallel graph | at most 2 | no $K_4$ minor |
| the complete bipartite graph $K_{a,b}$, $a \le b$ | $a$ | bags of the $a$ side plus one vertex of the other side |
| the $k \times k$ grid, $k \ge 2$ | $k$ | a window of $k + 1$ vertices in row order; a balanced cut needs $k$ vertices |
| the complete graph $K_n$ | $n - 1$ | the whole vertex set is a clique |
| a [planar graph](/planar-graph/) with $n$ vertices | $O(n^{1/2})$ | [planar separators](/planar-separator-theorem/) of size $O(n^{1/2})$, used again and again |

**A worked case.** The strip of triangles with the edges $01, 02, 12, 13, 23, 24, 34, 35, 45$ has the decomposition $\{0,1,2\}, \{1,2,3\}, \{2,3,4\}, \{3,4,5\}$ of width 2. It contains the triangle $\{0, 1, 2\}$, so its treewidth is at least $3 - 1 = 2$. Hence it is exactly 2. The elimination order $0, 1, 2, 3, 4, 5$ gives the later neighbours $\{1, 2\}, \{2, 3\}, \{3, 4\}, \{4, 5\}, \{5\}, \emptyset$, with at most 2 each, which is the same bound.

**The tree of the site.** The tree with the edges $01, 02, 13, 14, 25, 46, 47$ has treewidth 1: its bags are its seven edges.

## Where it is used

- **Fixed-parameter algorithms.** [Maximum independent set](/maximum-independent-set/), [vertex cover](/vertex-cover/), [graph coloring](/graph-coloring/) with a fixed number of colours, [Hamiltonian cycle](/hamiltonian-cycle/) and [dominating set](/dominating-set/) take $2^{O(k)} n$ or $2^{O(k \log k)} n$ time given a decomposition of width $k$, by [dynamic programming](/dp-on-tree-decompositions/). [Courcelle's theorem](/courcelle-theorem/) gives linear time for every property expressible in monadic second-order logic, for each fixed $k$.
- **Planar graphs.** With treewidth $O(n^{1/2})$ and these dynamic programs, many NP-hard problems on planar graphs take $2^{O(n^{1/2})}$ time; with the grid minor theorem, many parameterized problems on planar graphs take $2^{O(k^{1/2})} n^{O(1)}$ time.
- **Inference and constraints.** The cost of exact inference in graphical models, through a [junction tree](/junction-tree/), and of solving constraint problems is exponential in the treewidth of the underlying graph.
- **Compilers and databases.** The control-flow graphs of structured programs have small treewidth, which register allocation can use, and a conjunctive query whose graph has small treewidth can be evaluated by a dynamic program over a decomposition of that graph.
- **Graph theory.** Treewidth is the central parameter of the graph minors project; a minor-closed class has bounded treewidth if and only if it excludes some planar graph.

## References
