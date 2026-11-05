---
tag: 3P33VT
kind: concept
slug: tree-decomposition
name: Tree decomposition
aliases:
- bag tree decomposition
area: graphs/tree-algorithms
level: advanced
summary: A tree of vertex bags that covers every edge and keeps each vertex's bags connected.
prereqs: [tree, connected-graph, clique]
see_also: [treewidth, path-decomposition, nice-tree-decomposition, tree-decomposition-construction, dp-on-tree-decompositions, chordal-graph, junction-tree, elimination-ordering]
sources:
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Łukasz Kowalik, Daniel Lokshtanov, Dániel Marx, Marcin Pilipczuk, Michał Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 7 (Treewidth), the section on path and tree decompositions, with the separation property of a bag and nice tree decompositions
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design, Addison-Wesley, 2006
    locator: Section 10.4 (Tree decompositions of graphs), the definition, the separation properties, and dynamic programming for independent sets
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Chapter 12 (Minors, trees and WQO), the section on tree-decompositions, with the separation lemma and the result that every clique lies in a bag
  - paper: Neil Robertson and Paul D. Seymour, Graph minors. II. Algorithmic aspects of tree-width, Journal of Algorithms 7(3), 309 to 322 (1986)
    locator: the definition of tree-decomposition and tree-width, and their first algorithmic uses
---

A tree decomposition of a graph $G$ is a [tree](/tree/) $T$ whose nodes carry sets of vertices of $G$, called *bags*, such that every edge of $G$ lies inside some bag and the bags that hold any one vertex form a connected subtree of $T$. Its *width* is the size of the largest bag minus one, and the least width over all tree decompositions of $G$ is the [treewidth](/treewidth/). A decomposition of small width shows that $G$ is built like a tree out of small pieces, glued along small separators, and many problems that are hard on general graphs become solvable by a [dynamic program over the tree](/dp-on-tree-decompositions/), in time exponential only in the width.

## In plain words

Some graphs are not trees but look like thick trees, such as a chain of triangles or a ring. A tree decomposition makes this visible. You cover the graph with small groups of vertices, the bags, and join the bags in a tree.

Two rules make the cover useful. Each link of the graph must sit inside one bag, so no link is lost. And each vertex must appear in a run of bags that hang together in the tree, so the vertex is not split into separate places.

Then each bag cuts the graph: what hangs on one side of it in the tree touches the other side only through the bag. So you can solve a problem bag by bag, from the leaves to the root, and remember only what happens inside the current bag. Small bags mean little to remember.

## The idea

**Definition.** Let $G = (V, E)$ be a graph. A tree decomposition of $G$ is a pair $(T, \{X_t\}_{t \in V(T)})$, where $T$ is a tree and each $X_t \subseteq V$ is a bag, such that:

1. every vertex is in some bag: $\bigcup_t X_t = V$;
2. for each edge $uv \in E$, some bag contains both $u$ and $v$;
3. for each vertex $v$, the nodes $t$ with $v \in X_t$ induce a connected subtree $T_v$ of $T$.

The width is $\max_t |X_t| - 1$. The tree $T$ is free; in algorithms it is usually rooted, and its nodes are numbered $0, \ldots, |V(T)| - 1$, apart from the vertices $0, \ldots, n-1$ of $G$. The graph $G$ is not weighted. If $T$ is a path, the decomposition is a [path decomposition](/path-decomposition/).

The minus one makes trees have width 1: the bags $\{u, v\}$, one per edge, joined as the edges are joined in the tree, form a decomposition of width 1.

**Separation.** Let $st$ be an edge of $T$. Removing it splits $T$ into two parts, and splits $V$ into the vertices that appear only in bags of the first part, $A$, those only in the second part, $B$, and the rest, which lie in $X_s \cap X_t$. No edge of $G$ joins $A$ to $B$: such an edge would lie in a bag of one part, and then one of its ends would appear in both parts, so in $X_s$ and $X_t$ by condition 3. So $X_s \cap X_t$ separates $A$ from $B$. In the same way, a single bag $X_t$ separates the vertices that appear only in different branches of $T$ at $t$. This is what makes dynamic programming work: the subproblem below a node talks to the rest only through one bag.

**Cliques lie in a bag.** If $K$ is a [clique](/clique/) of $G$, some bag contains all of $K$. The subtrees $T_v$ for $v \in K$ meet two by two, because each edge of $K$ is in a bag, and subtrees of a tree that meet two by two have a common node (the Helly property of subtrees). So the width is at least $|K| - 1$, and the [complete graph](/complete-graph/) $K_n$ has treewidth $n - 1$.

**From an elimination order.** Take an order $v_1, \ldots, v_n$ of $V$. Eliminate the vertices in this order: when $v_i$ is eliminated, join its neighbours that come later into a clique, and let $N^+(v_i)$ be these later neighbours. Then the bags $X_i = \{v_i\} \cup N^+(v_i)$, with $X_i$ joined to $X_j$ where $v_j$ is the first vertex of $N^+(v_i)$ in the order, form a tree decomposition, a forest if $G$ is not connected, of width $\max_i |N^+(v_i)|$. Every tree decomposition of width $k$ gives an order with $|N^+(v_i)| \le k$, by eliminating, each time, a vertex that appears only in a leaf bag, after removing the bags that are subsets of a neighbour. So the treewidth is the least such maximum over all orders, and the graph with all the added edges is a [chordal graph](/chordal-graph/) that contains $G$. See [elimination ordering](/elimination-ordering/).

**Rooted form.** For algorithms, root $T$ and, if needed, make it a [nice tree decomposition](/nice-tree-decomposition/), in which each node adds one vertex, removes one vertex, or joins two equal bags. A decomposition with any number of nodes can be shrunk to at most $n$ nodes of the same width by merging each bag that is a subset of a neighbour into that neighbour.

## Examples

| graph | a tree decomposition | width |
|---|---|---|
| a tree with edges $u\,p(u)$ | one bag $\{u, p(u)\}$ per edge, joined like the edges | 1 |
| the path $0, 1, \ldots, n-1$ | the bags $\{i, i+1\}$ on a path | 1 |
| the star with centre $0$ | the bags $\{0, i\}$, all joined to $\{0, 1\}$ | 1 |
| the cycle $0, 1, \ldots, n-1$, $n \ge 3$ | the bags $\{0, i, i+1\}$ for $1 \le i \le n-2$ on a path | 2 |
| the $k \times k$ grid | a window of $k + 1$ consecutive vertices in row order, moved one step at a time | $k$ |
| $K_n$ | one bag $V$ | $n - 1$ |

The single vertex has the decomposition with one bag $\{0\}$, of width 0.

**A strip of triangles.** Let $G$ have the vertices $0, \ldots, 5$ and the edges $01, 02, 12, 13, 23, 24, 34, 35, 45$. The bags $\{0, 1, 2\}, \{1, 2, 3\}, \{2, 3, 4\}, \{3, 4, 5\}$, joined in this order on a path, form a decomposition of width 2. Each edge lies in a bag, and each vertex lies in consecutive bags: $2$ in the first three, $3$ in the last three. The middle edge of the path has the bags $\{1, 2, 3\}$ and $\{2, 3, 4\}$, whose intersection $\{2, 3\}$ separates $\{0, 1\}$ from $\{4, 5\}$ in $G$. The graph has triangles, so no decomposition has width 1.

**Not a decomposition.** On the cycle with the edges $01, 12, 23, 30$, take the path of bags $\{0, 1\}, \{1, 2, 3\}, \{3, 0\}$. Every edge lies in a bag, but $0$ is in the first and the last bag and not in the middle one, so condition 3 fails. The bags $\{0, 1, 3\}, \{1, 2, 3\}$ are a valid decomposition of width 2.

## Where it is used

- **Dynamic programming.** [Independent set](/maximum-independent-set/), [vertex cover](/vertex-cover/), [graph coloring](/graph-coloring/), [dominating set](/dominating-set/) and [Hamiltonian cycle](/hamiltonian-cycle/) are solved in $f(k) \cdot n$ time on graphs with a given decomposition of width $k$, by [dynamic programming over the decomposition](/dp-on-tree-decompositions/). [Courcelle's theorem](/courcelle-theorem/) extends this to every property expressible in monadic second-order logic.
- **Probabilistic inference.** The [junction tree](/junction-tree/) of a graphical model is a tree decomposition of its moral graph, and the cost of exact inference, as in [variable elimination](/variable-elimination/), is exponential in its width.
- **Sparse linear algebra.** Gaussian elimination on a sparse symmetric matrix follows an elimination order, and the [fill-in](/fill-in/) it creates is the chordal supergraph of that order.
- **Structural graph theory.** Tree decompositions are a main tool of the graph minors theory of Robertson and Seymour, through the [grid minor theorem](/grid-minor-theorem/).
- **Construction.** The [construction algorithm](/tree-decomposition-construction/) builds a decomposition of width at most $4k + 4$ or proves that the treewidth exceeds $k$.

## References
