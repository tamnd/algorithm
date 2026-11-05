---
tag: E8XWKM
kind: definition
slug: acyclic-graph
name: Acyclic graph
aliases:
- Cyclic vs acyclic graphs
area: graphs/graph-representation
level: intro
summary: A graph that contains no cycles, with forests as the undirected case and directed acyclic graphs as the directed case.
prereqs: [graph, directed-graph]
see_also: [directed-acyclic-graph, tree, spanning-forest, cycle-detection-in-graph, dfs-cycle-detection, topological-sort, girth, free-tree-properties]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix B.4 (Graphs), cycles and acyclic graphs; Appendix B.5.1 (Free trees), Theorem B.2 on the properties of free trees; Section 20.4 (Topological sort), the lemma that a directed graph is acyclic if and only if depth-first search finds no back edge
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 1.3 (Paths and cycles) and Section 1.5 (Trees and forests)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Chapter 3, Section 3.6 (Directed acyclic graphs and topological ordering)
---

An acyclic graph is a [graph](/graph/) that has no cycle. An undirected acyclic graph is a *forest*, and a connected one is a [tree](/tree/). A [directed graph](/directed-graph/) with no directed cycle is a [directed acyclic graph](/directed-acyclic-graph/), or DAG. The two cases behave very differently: a forest on $n$ vertices has at most $n - 1$ edges, while a DAG can have $\binom{n}{2}$. Both are tested in $O(n + m)$ time by [depth-first search](/depth-first-search/).

## Definition

**Walks and cycles.** Let $G = (V, E)$ be a graph and $k \ge 1$.

- In an undirected simple graph, a *cycle* of length $k \ge 3$ is a sequence $v_0, v_1, \ldots, v_{k-1}$ of distinct vertices such that $\{v_{i}, v_{i+1}\} \in E$ for $0 \le i \le k - 2$ and $\{v_{k-1}, v_0\} \in E$. So it uses $k$ distinct edges. The length is at least 3, because a cycle may not use the same edge twice.
- In a directed graph, a *directed cycle* of length $k \ge 1$ is a sequence $v_0, \ldots, v_{k-1}$ of distinct vertices with $(v_i, v_{i+1}) \in E$ for $0 \le i \le k-2$ and $(v_{k-1}, v_0) \in E$. A self-loop is a cycle of length 1, and a pair of edges $(u, v), (v, u)$ is a cycle of length 2.
- In an undirected [multigraph](/multigraph/), a loop is a cycle of length 1, and two parallel edges form a cycle of length 2.

**Acyclic.** $G$ is *acyclic* when it has no cycle in the sense of its kind. Then:

- an acyclic undirected graph is a **forest**, and a connected forest is a **tree**;
- an acyclic directed graph is a **DAG**.

$G$ is *cyclic* when it has at least one cycle. The length of a shortest cycle of a cyclic graph is its [girth](/girth/); an acyclic graph has girth $\infty$ by convention.

**Equivalent forms for undirected graphs.** For a simple undirected graph $G$ with $n$ vertices, $m$ edges and $c$ connected components, these are equivalent:

1. $G$ is a forest.
2. Each two vertices are joined by at most one path.
3. $m = n - c$.
4. Removing any edge increases the number of components.

These follow from the properties of trees in CLRS Theorem B.2, applied to each component. In particular a forest has $m \le n - 1$ edges for $n \ge 1$, so a graph with $m \ge n$ edges has a cycle.

**Equivalent forms for directed graphs.** For a finite directed graph, these are equivalent: $G$ is a DAG; $G$ has a [topological order](/topological-ordering/), a numbering of the vertices in which each edge goes from a smaller number to a larger one; a depth-first search of $G$ finds no back edge. The [directed acyclic graph](/directed-acyclic-graph/) page proves the first equivalence.

**Directed versus undirected acyclicity.** A directed graph can be acyclic while its underlying undirected graph has cycles. The edges $(0, 1), (0, 2), (1, 2)$ form a DAG, and the undirected triangle $\{0, 1\}, \{0, 2\}, \{1, 2\}$ is a cycle. In the other direction, let a directed graph have no self-loop and no pair of edges $(u, v), (v, u)$. If its underlying undirected graph is a forest, then the directed graph is a DAG, because a directed cycle would have length at least 3 and would give an undirected cycle on the same vertices.

## Examples and non-examples

**A forest.** On $V = \{0, \ldots, 6\}$, the edges $01, 02, 13, 45$ form a forest with the components $\{0, 1, 2, 3\}$, $\{4, 5\}$ and $\{6\}$. So $n = 7$, $c = 3$ and $m = 4 = 7 - 3$. Adding the edge $23$ makes the cycle $0, 1, 3, 2$ of length 4.

**A DAG with many edges.** The directed graph on $\{0, \ldots, n-1\}$ with all edges $(i, j)$ for $i < j$ is a DAG with $\binom{n}{2}$ edges, the most a DAG on $n$ vertices can have. For $n = 5$ that is 10 edges. Each further edge $(j, i)$ with $i < j$ closes the cycle $i, j$ with the edge $(i, j)$.

**Trees.** Each [tree](/tree/) is acyclic. A [rooted tree](/rooted-tree/) with its edges directed from parents to children is a DAG in which each vertex but the root has in-degree 1.

**Non-examples.**

- The undirected graph with the edges $01, 12, 20$ is the triangle, a cycle of length 3. It is not a forest, and indeed $m = 3 > n - c = 2$.
- The directed graph with the edges $(0, 1), (1, 0)$ is not a DAG. Its underlying undirected graph is the single edge $\{0, 1\}$, which is a forest. So the undirected test does not decide the directed question.
- A directed graph with a self-loop $(v, v)$ is never a DAG.
- The undirected walk $0, 1, 0$ along one edge is not a cycle, so the single edge $01$ is a forest.

**The cost of the test.** With $n$ vertices and $m$ edges:

| graph and representation | test | time |
|---|---|---|
| undirected, [adjacency list](/adjacency-list/) | DFS or BFS that finds a non-tree edge | $O(n)$, see below |
| undirected, [edge list](/edge-list/) | [union-find](/disjoint-set/): an edge whose ends are already joined closes a cycle | $O(m\, \alpha(n))$ |
| directed, adjacency list | [DFS cycle detection](/dfs-cycle-detection/) by colors, or [Kahn's algorithm](/kahns-algorithm/) | $O(n + m)$ |
| either, [adjacency matrix](/adjacency-matrix/) | the same searches, with rows scanned | $O(n^2)$ |

The undirected test can stop after $n$ edges, because a graph with $n$ edges has a cycle. So on an adjacency list it reads $O(n)$ entries: the search stops at the first non-tree edge, and before that each edge it reads is a tree edge, of which there are at most $n - 1$, plus at most one copy of each tree edge from the other end. No such bound holds for directed graphs, where a DAG can have $\Theta(n^2)$ edges.

## Related definitions

- [Directed acyclic graph](/directed-acyclic-graph/): the directed case in detail.
- [Tree](/tree/), [rooted tree](/rooted-tree/), [spanning forest](/spanning-forest/) and [free tree properties](/free-tree-properties/): the undirected case.
- [Cycle detection](/cycle-detection-in-graph/) and [DFS cycle detection](/dfs-cycle-detection/): the algorithms of the test.
- [Topological sort](/topological-sort/): the order that exists exactly for DAGs.
- [Girth](/girth/): the length of a shortest cycle.

## References
