---
tag: B0093F
kind: definition
slug: arborescence
name: Arborescence
aliases:
- out-tree
- directed rooted tree
- spanning arborescence
area: graphs/tree-algorithms
level: intro
summary: A rooted directed spanning tree in which every vertex is reachable from the root by exactly one directed path.
prereqs: [directed-graph, tree, rooted-tree]
see_also: [minimum-arborescence, edmonds-arborescence, directed-acyclic-graph, matrix-tree-theorem, spanning-tree, in-degree-and-out-degree, reachability, dominator-tree]
sources:
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, Theory and Algorithms, sixth edition, Springer, 2018
    locator: Section 2.2 (Trees, Circuits, and Cuts), the definitions of branching and arborescence and the theorem that lists the equivalent conditions; Section 6.2 (Minimum Weight Arborescences)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix B.5 (Trees), rooted trees; Section 20.2 (Breadth-first search), breadth-first trees
  - paper: "Jack Edmonds, Optimum branchings, Journal of Research of the National Bureau of Standards 71B (1967), 233-240"
    locator: the definition of a branching and the algorithm for a branching of maximum weight
---

An arborescence is a directed graph with a vertex $r$, the root, such that for each vertex $v$ there is exactly one directed path from $r$ to $v$. It is the directed form of a [rooted tree](/rooted-tree/): forget the directions and it is a [tree](/tree/), and each arc points away from the root. When the arborescence uses all the vertices of a larger [directed graph](/directed-graph/) $G$, it is a *spanning arborescence* of $G$, the directed analogue of a [spanning tree](/spanning-tree/). Breadth-first and depth-first search trees of a directed graph are arborescences, and so are [dominator trees](/dominator-tree/).

## Definition

Let $T = (V, A)$ be a finite directed graph without loops and $r \in V$. Then $T$ is an *arborescence rooted at $r$* (an *out-arborescence*, or *out-tree*) if for every $v \in V$ there is exactly one directed path from $r$ to $v$. For $v = r$ that path is the empty path, so no directed cycle passes through $r$.

The following conditions on $T$ with $n = |V| \ge 1$ are equivalent, and each one can serve as the definition (Korte and Vygen, Section 2.2):

1. For every $v \in V$ there is exactly one directed path from $r$ to $v$.
2. Every vertex is reachable from $r$, and $|A| = n - 1$.
3. The root has in-degree 0, every other vertex has in-degree 1, and every vertex is reachable from $r$.
4. The underlying undirected graph is a tree, and every vertex other than $r$ has in-degree 1.
5. Every vertex is reachable from $r$, and $T$ is minimal with this property: removing any arc makes some vertex unreachable.

So an arborescence is stored by a parent array: $p(v)$ is the tail of the only arc that enters $v \ne r$. The arc $(p(v), v)$ is the last arc of the path from $r$ to $v$, and the path itself is $v, p(v), p(p(v)), \ldots, r$ read backwards.

A *branching* is a directed graph in which each vertex has in-degree at most 1 and whose underlying graph has no cycle; its connected parts are arborescences, so a branching is a forest of arborescences. An *in-arborescence* (or *anti-arborescence*) is an arborescence with all arcs reversed: every vertex has exactly one directed path *to* the root.

## Examples and non-examples

In the examples the vertices are numbered $0, \ldots, n-1$, the root is 0, and the arcs have no weights.

- **One vertex.** The graph with the single vertex 0 and no arcs is an arborescence rooted at 0.
- **A directed path.** The arcs $0 \to 1 \to 2 \to \cdots \to n-1$ form an arborescence rooted at 0. The same arcs form an in-arborescence rooted at $n - 1$. They form no arborescence rooted at any other vertex, because vertex 0 is not reachable from it.
- **An out-star.** The arcs $0 \to v$ for $v = 1, \ldots, n-1$ form an arborescence rooted at 0. The in-star, with arcs $v \to 0$, is an in-arborescence and, for $n \ge 3$, not an arborescence for any root.
- **Search trees.** In a directed graph, the arcs $(\pi(v), v)$ found by [breadth-first search](/breadth-first-search/) or [depth-first search](/depth-first-search/) from $s$ form an arborescence rooted at $s$ on the vertices reachable from $s$. The shortest-path tree of [Dijkstra's algorithm](/dijkstra/) is another one.
- **Not an arborescence: two paths.** The arcs $0 \to 1$, $0 \to 2$, $1 \to 3$, $2 \to 3$ form a [directed acyclic graph](/directed-acyclic-graph/) in which 3 has two paths from 0. Condition 3 fails: 3 has in-degree 2.
- **Not an arborescence: a cycle away from the root.** The arcs $0 \to 1$, $2 \to 3$, $3 \to 2$ satisfy "in-degree 1 for each $v \ne 0$", with $n - 1 = 3$ arcs, but 2 and 3 are not reachable from 0. Condition 3 needs reachability, and condition 4 needs the underlying graph to be a tree; this one has a cycle on $\{2, 3\}$ and is not connected.
- **Not an arborescence: a wrong direction.** The arcs $0 \to 1$ and $2 \to 1$ have a tree as underlying graph, but 1 has in-degree 2 and 2 is not reachable from 0.

**Counting the spanning arborescences.** Take the directed graph $G$ on $\{0, 1, 2, 3\}$ with the arcs $0 \to 1$, $0 \to 2$, $1 \to 2$, $2 \to 1$, $1 \to 3$, $2 \to 3$. A spanning arborescence rooted at 0 picks one entering arc for each of 1, 2 and 3, which gives $2 \cdot 2 \cdot 2 = 8$ choices, and must avoid the two choices that pick both $2 \to 1$ and $1 \to 2$, since then neither 1 nor 2 is reachable. So $G$ has 6 spanning arborescences rooted at 0. The directed form of the [matrix-tree theorem](/matrix-tree-theorem/) gives the same count as a determinant: delete row and column 0 of the in-degree Laplacian $L = D_{in} - A$, which leaves
$$\det \begin{pmatrix} 2 & -1 & -1 \\ -1 & 2 & -1 \\ 0 & 0 & 2 \end{pmatrix} = 2 \cdot (4 - 1) = 6,$$
with rows and columns in the order 1, 2, 3 and $L_{uv} = -1$ for each arc $u \to v$.

## Related definitions

- **[Rooted tree](/rooted-tree/).** An undirected tree with a chosen root. Orienting every edge away from the root gives an arborescence, and forgetting the directions of an arborescence gives a rooted tree. The two are the same object in two notations.
- **[Spanning tree](/spanning-tree/).** The undirected analogue. Every connected undirected graph has a spanning tree, but a directed graph has a spanning arborescence rooted at $r$ if and only if every vertex is reachable from $r$.
- **[Minimum arborescence](/minimum-arborescence/).** The problem of finding a spanning arborescence of least total arc weight. Picking the cheapest entering arc of each vertex can create a cycle, so the greedy rule of Kruskal does not apply; [Edmonds' algorithm](/edmonds-arborescence/) contracts such cycles.
- **[Directed acyclic graph](/directed-acyclic-graph/).** Every arborescence is a DAG, but a DAG can have vertices with in-degree 2 or more.
- **[Dominator tree](/dominator-tree/).** For a flow graph with entry $r$, the arcs from each vertex's immediate dominator form an arborescence rooted at $r$, even though it is usually not a subgraph of the flow graph.
- **Branching.** A forest of arborescences, as defined above. Edmonds' 1967 paper finds a branching of maximum weight.

### History

Edmonds named the forests of arborescences *branchings* in his 1967 paper on optimum branchings, where he also gave the algorithm for the maximum-weight branching that Chu and Liu had found independently in 1965. Edmonds later proved that a directed graph has $k$ arc-disjoint spanning arborescences rooted at $r$ if and only if every set of vertices that does not contain $r$ has at least $k$ entering arcs.

## References
