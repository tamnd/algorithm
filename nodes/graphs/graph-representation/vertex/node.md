---
tag: HAY9Y7
kind: definition
slug: vertex
name: Vertex
aliases:
- node
area: graphs/graph-representation
level: intro
summary: Basic element of a graph that edges connect.
prereqs: [graph]
see_also: [edge, degree, neighborhood, labeled-graph, symbol-graph, adjacency-list, in-degree-and-out-degree, induced-subgraph]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix B.4 (Graphs), vertices, adjacency, degree, isolated vertices; Section 20.1, vertices numbered 1 to |V| and attributes on vertices
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Chapter 1, Section 1.1 (Graphs), vertices, incidence and adjacency; Section 1.2, degree, isolated vertices
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.1 (Undirected graphs), vertices named by the integers 0 to V-1, and symbol graphs for vertices named by strings
---

A vertex, or node, is one of the objects that a [graph](/graph/) relates. A graph $G = (V, E)$ is a set $V$ of vertices with a set $E$ of [edges](/edge/), each of which joins two vertices. A vertex has no structure of its own: everything about it, its [degree](/degree/), its [neighborhood](/neighborhood/), its place on a path, comes from the edges. In programs a vertex is an integer in $\{0, \ldots, n - 1\}$ that indexes arrays, and a [symbol graph](/symbol-graph/) maps outside names such as strings to those integers.

## Definition

Let $G = (V, E)$ be a graph. The elements of $V$ are its **vertices**. $V$ is a finite set, written $V(G)$ when several graphs are in play, and $n = |V|$ is the *order* of $G$. Most books require $V \ne \emptyset$; some allow the empty graph.

The basic relations between vertices and edges:

- **Incidence.** A vertex $v$ and an edge $e$ are *incident* when $v$ is an end of $e$. In a [directed graph](/directed-graph/), the edge $(u, v)$ *leaves* $u$ and *enters* $v$; $u$ is its *tail* and $v$ its *head*.
- **Adjacency.** Two vertices $u$ and $v$ are *adjacent*, or *neighbours*, when $\{u, v\} \in E$ (undirected) or when $(u, v) \in E$ (directed; then $v$ is adjacent *from* $u$ and is a *successor* of $u$). The set of neighbours is the [neighborhood](/neighborhood/) $N(v)$.
- **Degree.** $d(v)$ is the number of edge ends at $v$, with a [self-loop](/self-loop/) counted twice. In a directed graph, $d^+(v)$ and $d^-(v)$ count the edges that leave and that enter $v$; see [in-degree and out-degree](/in-degree-and-out-degree/).

Special vertices, by their degree:

| name | condition | example |
|---|---|---|
| isolated vertex | $d(v) = 0$ | a vertex with no edges |
| leaf, or pendant vertex | $d(v) = 1$ | an end of a path |
| universal, or dominating, vertex | $N(v) = V \setminus \{v\}$ | the centre of a star |
| source (directed) | $d^-(v) = 0$ | the first vertex of a topological order |
| sink (directed) | $d^+(v) = 0$ | the last vertex of a topological order |
| [universal sink](/universal-sink/) (directed) | $d^-(v) = n - 1$ and $d^+(v) = 0$ | a vertex all others point to |

**Vertices in a program.** The usual form is $V = \{0, 1, \ldots, n - 1\}$ (or $\{1, \ldots, n\}$, as in CLRS), so that data about a vertex is an entry of an array indexed by it: $\text{Adj}[v]$ in an [adjacency list](/adjacency-list/), a row of an [adjacency matrix](/adjacency-matrix/), and attributes like $v.d$ and $v.\pi$ in [breadth-first search](/breadth-first-search/). Then reading or writing one attribute of a vertex costs $O(1)$, and an array of attributes costs $\Theta(n)$ space. When vertices have outside names, a [symbol graph](/symbol-graph/) keeps a table from names to integers, so each lookup costs the time of the table, for example $O(1)$ expected with a [hash table](/hash-table/). Adding a vertex costs $O(1)$ amortized in an adjacency list built on a [dynamic array](/dynamic-array/), but $\Theta(n)$ or more in an adjacency matrix, which must grow a row and a column. Removing a vertex costs $\Theta(1 + d(v))$ plus the cost of removing $v$ from each list it occurs in.

## Examples and non-examples

In $G = (\{1, 2, 3, 4, 5\}, \{12, 13, 23, 34\})$, where $12$ means $\{1, 2\}$:

- 3 has the neighbours $1, 2, 4$ and degree 3. It is universal on $\{1, 2, 3, 4\}$, but not in $G$, since it is not adjacent to 5.
- 4 is a leaf, with the one neighbour 3.
- 5 is isolated. It is still a vertex: $n = 5$. An algorithm that builds $V$ from the edge list alone would lose it, which is a common bug.

**Directed.** In the graph with the edges $(1, 2), (1, 3), (2, 3)$, the vertex 1 is a source, 3 is a sink, and 3 is a universal sink, since both other vertices point to it and it points to none.

**Non-examples.**

- An edge is not a vertex. In the [line graph](/line-graph/) $L(G)$ the edges of $G$ become vertices, but that is a different graph.
- The "nodes" of a [linked list](/linked-list/) or of a search tree are records in memory. They are vertices of the graph of pointers, but most of their fields, keys and values, are data that a graph vertex does not have. A graph may attach such data to a vertex as an attribute.

## Related definitions

- **Edge.** An unordered or ordered pair of vertices. See [edge](/edge/).
- **Labeled vertex.** A vertex with a fixed name, as opposed to a position in a shape up to isomorphism. See [labeled graph](/labeled-graph/).
- **Vertex-induced subgraph.** $G[S]$ for a set $S$ of vertices. See [induced subgraph](/induced-subgraph/).
- **Cut vertex.** A vertex whose removal increases the number of components. See [articulation point](/articulation-point/).
- **Vertex weight.** A number on each vertex, as in maximum weight independent set; the edge case is the [weighted graph](/weighted-graph/).

## References
