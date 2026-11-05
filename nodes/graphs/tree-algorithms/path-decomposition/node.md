---
tag: KRCZQT
kind: concept
slug: path-decomposition
name: Path decomposition
area: graphs/tree-algorithms
level: advanced
summary: A path decomposition is a tree decomposition whose tree is a path, with its width measuring how path-like a graph is.
prereqs: [tree-decomposition, treewidth]
see_also: [tree-decomposition, treewidth, nice-tree-decomposition, treewidth-computation, dp-on-tree-decompositions, centroid, graph-minor, chordal-graph]
sources:
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Łukasz Kowalik, Daniel Lokshtanov, Dániel Marx, Marcin Pilipczuk, Michał Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 7 (Treewidth), the section on path and tree decompositions, with nice path decompositions and dynamic programming over them
  - paper: Neil Robertson and Paul D. Seymour, Graph minors. I. Excluding a forest, Journal of Combinatorial Theory, Series B 35(1), 39 to 61 (1983)
    locator: the definition of path-width and the theorem that excluding a forest as a minor bounds the path-width
  - paper: Nancy G. Kinnersley, The vertex separation number of a graph equals its path-width, Information Processing Letters 42(6), 345 to 350 (1992)
    locator: the equality of path-width and vertex separation number over linear orders of the vertices
---

A path decomposition of a graph $G$ is a [tree decomposition](/tree-decomposition/) whose tree is a path: a sequence of bags $X_1, \ldots, X_r$ such that every edge lies in a bag and each vertex appears in a block of consecutive bags. The *pathwidth* $\mathrm{pw}(G)$ is the least width, the largest bag size minus one, over all path decompositions. Since a path is a tree, $\mathrm{pw}(G) \ge \mathrm{tw}(G)$, and the gap is at most a factor $O(\log n)$. Pathwidth measures how well $G$ can be swept from left to right while keeping only a few vertices "open" at a time, which makes dynamic programs over it simple: they only add and remove vertices, never merge two branches.

## In plain words

Imagine you must walk past a graph from left to right, holding some vertices in your hands. You pick up a vertex when you first need it and put it down when you are done with it for good. Each link of the graph must be seen while both of its ends are in your hands. The fewest hands you need, minus one, is the pathwidth.

A path needs two hands: hold one vertex and the next, then move on. A star also needs two: hold the centre the whole time and pick up the leaves one by one. Some trees need more, because they branch in many directions at once, and a square grid with $k$ rows needs about $k$ hands, one row at a time. The walk is easier to use than a full tree of bags, since it never has to join two branches.

## The idea

**Definition.** Let $G = (V, E)$ be a graph with the vertices $0, \ldots, n-1$; it is not weighted. A path decomposition is a sequence $X_1, \ldots, X_r$ of subsets of $V$ such that:

1. every vertex is in some bag;
2. every edge has both ends in some bag;
3. if $v \in X_i$ and $v \in X_j$ with $i < j$, then $v \in X_l$ for every $l$ between them.

Its width is $\max_i |X_i| - 1$, and $\mathrm{pw}(G)$ is the least width. Condition 3 says that each vertex lives on an interval of positions.

**Equivalent forms.**

- **Interval supergraphs.** Give each vertex the interval of the bags that hold it. Two vertices whose intervals meet are in a common bag, so $G$ is a subgraph of the interval graph of these intervals, whose largest clique is the largest bag. So $\mathrm{pw}(G) + 1$ is the least clique number of an interval graph on $V$ that contains $G$, just as treewidth uses [chordal](/chordal-graph/) supergraphs.
- **Vertex separation.** For an order $v_1, \ldots, v_n$ of $V$ and a position $i$, count the vertices among $v_1, \ldots, v_i$ that have a neighbour among $v_{i+1}, \ldots, v_n$. The least, over all orders, of the largest such count is the vertex separation number, and Kinnersley proved that it equals the pathwidth.
- **Searching.** The pathwidth plus one equals the number of searchers needed to clear a graph of an invisible, fast fugitive by placing and removing searchers on vertices, with no cleared part ever infected again.

**From a tree decomposition to a path decomposition.** Let $(T, \{X_t\})$ have width $k$. Some bag $X_c$ is a balanced separator: every component of $G - X_c$ has at most $n/2$ vertices (this is the balanced separator lemma proved for the [construction algorithm](/tree-decomposition-construction/), with $W = V$). Take a path decomposition of each component, recursively, put them one after another, and add $X_c$ to every bag. This is a path decomposition, since each component touches the others only through $X_c$, and its width is at most $k + 1$ more than the widths of the parts. The size halves at each level, so

$$\mathrm{tw}(G) \le \mathrm{pw}(G) \le (\mathrm{tw}(G) + 1) \log_2 n.$$

For a tree, with $c$ a centroid vertex, this gives $\mathrm{pw}(T) \le 1 + \log_2 n$, and complete ternary trees show that the pathwidth of trees can indeed grow like $\log n$.

**Excluding a forest.** Robertson and Seymour proved that for each forest $F$, the graphs with no $F$ [minor](/graph-minor/) have pathwidth bounded by a function of $F$, and that a class of graphs closed under minors has bounded pathwidth if and only if it excludes some forest. For the class of graphs with pathwidth at most 1, the components are caterpillars: trees that become a path, or a single vertex, when all leaves are removed.

**Computation.** Deciding $\mathrm{pw}(G) \le k$ is NP-complete when $k$ is part of the input. For each fixed $k$ it takes linear time, and on trees the pathwidth can be computed in linear time.

## Examples

| graph | a path decomposition | width |
|---|---|---|
| a single vertex | $\{0\}$ | 0 |
| the path $0, \ldots, n-1$ | $\{0, 1\}, \{1, 2\}, \ldots, \{n-2, n-1\}$ | 1 |
| the star with centre $0$ | $\{0, 1\}, \{0, 2\}, \ldots, \{0, n-1\}$ | 1 |
| the cycle $0, \ldots, n-1$ | $\{0, 1, 2\}, \{0, 2, 3\}, \ldots, \{0, n-2, n-1\}$ | 2 |
| the strip of triangles $01, 02, 12, 13, 23, 24, 34, 35, 45$ | $\{0, 1, 2\}, \{1, 2, 3\}, \{2, 3, 4\}, \{3, 4, 5\}$ | 2 |
| the $k \times k$ grid | windows of $k + 1$ consecutive vertices in row order | $k$ |

**The tree of the site.** The tree with the edges $01, 02, 13, 14, 25, 46, 47$ loses its leaves $3, 5, 6, 7$ and becomes the path $2, 0, 1, 4$, so it is a caterpillar. Walking along that spine gives the decomposition

$$\{2, 5\},\ \{2, 0\},\ \{0, 1\},\ \{1, 3\},\ \{1, 4\},\ \{4, 6\},\ \{4, 7\}$$

of width 1. Each spine vertex is held for a block of bags: $0$ in the second and third, $1$ in the third to fifth, $4$ in the last three.

**A tree with pathwidth 2.** Subdivide each edge of the star with three leaves: the centre $c$ is joined to $a_1, a_2, a_3$, and each $a_i$ to a leaf $b_i$. Removing the leaves leaves the star $c, a_1, a_2, a_3$, not a path, so it is not a caterpillar and its pathwidth is at least 2. The bags $\{c, a_1, b_1\}, \{c, a_2, b_2\}, \{c, a_3, b_3\}$ give width 2. Its treewidth is 1, so pathwidth and treewidth differ already on 7 vertices.

## Where it is used

- **Dynamic programming.** On a path decomposition of width $k$, the programs of [dynamic programming over tree decompositions](/dp-on-tree-decompositions/) need only introduce and forget steps, with no join step, which makes them simpler and often faster. The [nice](/nice-tree-decomposition/) form of a path decomposition has only these two kinds of nodes.
- **Layout problems.** Gate matrix layout in chip design, and other problems that place vertices on a line, are equivalent to pathwidth or close to it.
- **Graph searching and games.** Pathwidth is the number of searchers needed to catch an invisible fugitive, a model for clearing tunnels or networks.
- **Structural graph theory.** The forest-exclusion theorem is the first result of the graph minors series, and it is the path analogue of the [grid minor theorem](/grid-minor-theorem/) for treewidth.
- **Bounds for treewidth algorithms.** The bound $\mathrm{pw} \le (\mathrm{tw} + 1)\log_2 n$ turns any algorithm over path decompositions into one over tree decompositions, with a loss of a $\log n$ factor in the width.

## References
