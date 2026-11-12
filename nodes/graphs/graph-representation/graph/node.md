---
tag: 0MSSM6
kind: abstract-type
slug: graph
name: Graph
aliases:
- graph ADT
- vertex-edge structure
area: graphs/graph-representation
level: intro
summary: Abstract type of vertices and edges supporting adjacency and neighbourhood queries.
see_also: [adjacency-list, adjacency-matrix, edge-list, compressed-sparse-row, hash-based-adjacency, adjacency-query, directed-graph, directed-and-undirected-graphs]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix B.4 (Graphs), and Section 20.1 (Representations of graphs)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.1 (Undirected graphs), the Graph API and the table of representation costs; Section 4.2 (Directed graphs)
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Chapter 1, Section 1.1 (Graphs) and Section 1.10 (Other notions of graphs)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Chapter 3 (Graphs), Section 3.1 (basic definitions) and Section 3.3 (representing graphs)
---

A graph is a set of [vertices](/vertex/) together with a set of [edges](/edge/), where each edge joins two vertices. As an abstract data type, a graph is a value $G = (V, E)$ with operations that ask whether two vertices are adjacent, list the neighbours of a vertex, and add or remove vertices and edges. The type fixes what these operations return, and the representations, such as the [adjacency list](/adjacency-list/) and the [adjacency matrix](/adjacency-matrix/), fix what they cost. Almost every algorithm on networks, maps, schedules and state spaces reads its input through this type.

## In plain words

Draw some dots on paper and connect some pairs of them with lines. The dots are the vertices and the lines are the edges. That drawing is a graph. A road map is one: towns are dots and roads are lines. A social network is one: people are dots and friendships are lines.

Sometimes the lines are arrows, because a one-way street or a web link goes in one direction only. Then the graph is directed.

A program that works with a graph needs only a few questions answered. Are these two dots connected? Which dots are connected to this one? Can I add or remove a dot or a line? The graph type is the list of these questions and the rules for their answers. How fast each answer comes depends on how the program stores the drawing.

## Operations

**The values.** A graph is a pair $G = (V, E)$ of a finite set $V$ of vertices and a set $E$ of edges. We write $n = |V|$ and $m = |E|$. This page uses the conventions of CLRS, Appendix B.4:

- In a **directed graph**, $E \subseteq V \times V$. An edge is an ordered pair $(u, v)$ from its tail $u$ to its head $v$. A [self-loop](/self-loop/) $(v, v)$ is allowed, and each ordered pair occurs at most once. See [directed graph](/directed-graph/).
- In an **undirected graph**, $E \subseteq \{\{u, v\} : u, v \in V,\ u \ne v\}$. An edge is an unordered pair of two distinct vertices, so there are no self-loops and no parallel edges. This is a [simple graph](/simple-graph/). See [undirected graph](/undirected-graph/).
- A **weighted graph** adds a function $w : E \to \mathbb{R}$. See [weighted graph](/weighted-graph/).
- A [multigraph](/multigraph/) allows two or more edges with the same ends. It needs edge names and is not a set of pairs. This page treats simple graphs; the representations extend to multigraphs by storing each edge once per copy.

The two vertices $u$ and $v$ are *adjacent* when $(u, v) \in E$ (directed) or $\{u, v\} \in E$ (undirected). The *out-neighbours* of $u$ are $N^+(u) = \{v : (u, v) \in E\}$. In an undirected graph, $N(u) = \{v : \{u, v\} \in E\}$ is the [neighborhood](/neighborhood/) of $u$, and $|N(u)|$ is its [degree](/degree/) $d(u)$.

The operations, for a directed graph:

| operation | signature | what it does |
|---|---|---|
| `new` | $\text{new}(V) \to G$ | the graph $(V, \emptyset)$ with no edges |
| `adjacent` | $\text{adjacent}(G, u, v) \to \text{bool}$ | true if and only if $(u, v) \in E$, for $u, v \in V$ |
| `neighbors` | $\text{neighbors}(G, u) \to$ sequence | lists each $v \in N^+(u)$ exactly once, in some order |
| `add-edge` | $\text{add-edge}(G, u, v) \to G$ | $E$ becomes $E \cup \{(u, v)\}$ |
| `remove-edge` | $\text{remove-edge}(G, u, v) \to G$ | $E$ becomes $E \setminus \{(u, v)\}$ |
| `add-vertex` | $\text{add-vertex}(G) \to (v, G)$ | adds a new vertex $v \notin V$ with no edges, and returns it |
| `remove-vertex` | $\text{remove-vertex}(G, v) \to G$ | removes $v$ and each edge with $v$ as an end |
| `vertices` | $\text{vertices}(G) \to$ sequence | lists $V$ |
| `edges` | $\text{edges}(G) \to$ sequence | lists $E$, each edge once |

For an undirected graph, `add-edge`$(G, u, v)$ with $u \ne v$ adds $\{u, v\}$, and `neighbors` lists $N(u)$. The [adjacency query](/adjacency-query/) is the problem that `adjacent` solves. A weighted graph adds `weight`$(G, u, v)$, which returns $w(u, v)$ for an edge.

Most graph algorithms need only `vertices` and `neighbors`. [Breadth-first search](/breadth-first-search/) and [depth-first search](/depth-first-search/) call `neighbors` once for each vertex they reach, so they run in $O(n + m)$ time on a representation where `neighbors`$(u)$ takes $O(1 + |N^+(u)|)$ time.

### Example

Start with $\text{new}(\{0, 1, 2, 3\})$ for an undirected graph and run these operations.

| step | operation | result | $E$ after |
|---|---|---|---|
| 1 | add-edge 0 1 | | $\{01\}$ |
| 2 | add-edge 1 2 | | $\{01, 12\}$ |
| 3 | add-edge 2 0 | | $\{01, 02, 12\}$ |
| 4 | adjacent 0 2 | true | $\{01, 02, 12\}$ |
| 5 | adjacent 0 3 | false | $\{01, 02, 12\}$ |
| 6 | add-edge 3 1 | | $\{01, 02, 12, 13\}$ |
| 7 | neighbors 1 | 0, 2, 3 in some order | $\{01, 02, 12, 13\}$ |
| 8 | remove-edge 1 0 | | $\{02, 12, 13\}$ |
| 9 | adjacent 0 1 | false | $\{02, 12, 13\}$ |

Here $01$ is short for $\{0, 1\}$. Step 3 adds the edge as $\{2, 0\}$, which is the same set as $\{0, 2\}$. Step 8 removes $\{1, 0\} = \{0, 1\}$.

## Laws

Each implementation of a directed graph meets these equations, for each graph $G = (V, E)$ and vertices $u, v, x, y \in V$:

$$\begin{aligned}
&(\text{G1})\quad \text{adjacent}(\text{new}(V), x, y) = \text{false},\\
&(\text{G2})\quad \text{adjacent}(\text{add-edge}(G, u, v), x, y) = \big((x, y) = (u, v)\big) \lor \text{adjacent}(G, x, y),\\
&(\text{G3})\quad \text{adjacent}(\text{remove-edge}(G, u, v), x, y) = \big((x, y) \ne (u, v)\big) \land \text{adjacent}(G, x, y),\\
&(\text{G4})\quad \text{set}(\text{neighbors}(G, x)) = \{y \in V : \text{adjacent}(G, x, y)\}, \text{ with no vertex listed twice},\\
&(\text{G5})\quad \text{add-edge}(\text{add-edge}(G, u, v), u, v) = \text{add-edge}(G, u, v),\\
&(\text{G6})\quad \text{add-edge}(\text{add-edge}(G, u, v), x, y) = \text{add-edge}(\text{add-edge}(G, x, y), u, v).
\end{aligned}$$

An undirected graph also meets the symmetry law

$$(\text{G7})\quad \text{adjacent}(G, x, y) = \text{adjacent}(G, y, x),$$

and in (G2) and (G3) the test $(x, y) = (u, v)$ becomes $\{x, y\} = \{u, v\}$. Law (G5) says that $E$ is a set: adding an edge that is already there changes nothing. A multigraph breaks (G5), because a second `add-edge` makes a parallel edge. Law (G4) with (G7) gives $y \in N(x) \iff x \in N(y)$, so each undirected edge appears in two neighbour lists, and the lengths of all lists sum to $2m$. This is the [handshake lemma](/handshake-lemma/).

## Implementations

The table gives the worst-case time of each operation on a directed graph with $n$ vertices and $m$ edges, where $d = |N^+(u)|$ is the out-degree of the vertex $u$ of the call. The bounds for the [hash-based adjacency](/hash-based-adjacency/) are expected, with a hash function from a [universal family](/universal-hashing/). A [bitset adjacency matrix](/bitset-adjacency-matrix/) on the [word RAM](/word-ram/) with $w$-bit words is listed for comparison.

| structure | space | adjacent | neighbors | add-edge | remove-edge | add-vertex |
|---|---|---|---|---|---|---|
| [adjacency matrix](/adjacency-matrix/) | $\Theta(n^2)$ | $O(1)$ | $\Theta(n)$ | $O(1)$ | $O(1)$ | $\Theta(n^2)$ copy |
| [bitset adjacency matrix](/bitset-adjacency-matrix/) | $\Theta(n \lceil n/w \rceil)$ words | $O(1)$ | $O(n/w + d)$ | $O(1)$ | $O(1)$ | $\Theta(n^2/w)$ copy |
| [adjacency list](/adjacency-list/) | $\Theta(n + m)$ | $O(d)$ | $\Theta(d)$ | $O(1)$ amortized, no duplicate test | $O(d)$ | $O(1)$ amortized |
| [hash-based adjacency](/hash-based-adjacency/) | $\Theta(n + m)$ | $O(1)$ expected | $\Theta(d)$ | $O(1)$ expected amortized | $O(1)$ expected | $O(1)$ amortized |
| [edge list](/edge-list/) | $\Theta(m)$ | $O(m)$ | $\Theta(m)$ | $O(1)$ amortized, no duplicate test | $O(m)$ | $O(1)$ |
| [compressed sparse row](/compressed-sparse-row/) | $n + 1 + m$ words | $O(\log d)$ with sorted rows | $\Theta(d)$ | $\Theta(n + m)$ rebuild | $\Theta(n + m)$ rebuild | $\Theta(n + m)$ rebuild |

The adjacency list is the default for sparse graphs, where $m$ is much less than $n^2$, and for each algorithm that only walks the edges. The adjacency matrix is the default for [dense graphs](/dense-graph/) and for algorithms that test many pairs. The [compressed sparse row](/compressed-sparse-row/) form and the [forward star](/forward-star/) are static adjacency lists packed into two arrays, used when the graph does not change. An [implicit graph](/implicit-graph/) stores no edges at all and computes `neighbors` from a rule.

## Lower bounds

**Space.** There are $2^{\binom{n}{2}}$ undirected graphs on the fixed vertex set $\{0, \ldots, n-1\}$, one for each subset of the $\binom{n}{2}$ possible edges. A representation that tells all of them apart needs $2^{\binom{n}{2}}$ different bit strings, so some graph needs at least $\binom{n}{2}$ bits. The adjacency matrix uses $n^2$ bits, and its upper triangle uses exactly $\binom{n}{2}$, so it is optimal for the class of all graphs. For graphs with exactly $m$ edges, the same count gives $\lceil \lg \binom{\binom{n}{2}}{m} \rceil$ bits. For $1 \le m \le \binom{n}{2}/2$ this is $m \lg(n^2/m) + O(m)$. This is $\Theta(m \log n)$, the order of the bits of an adjacency list, when $m \le n^{2 - \varepsilon}$ for a constant $\varepsilon > 0$, and it is only $\Theta(m)$ when $m$ is a constant fraction of $n^2$. [Graph compression](/graph-compression/) and the [succinct graph representation](/succinct-graph-representation/) work near this bound.

**Probes in the matrix.** Assume the only access to $G$ is `adjacent`. Then deciding whether an undirected graph on $n \ge 2$ vertices has at least one edge needs $\binom{n}{2}$ calls in the worst case. *Proof.* An adversary answers false to each call. If an algorithm stops after fewer than $\binom{n}{2}$ calls, some pair $\{x, y\}$ was never asked. The empty graph and the graph with the single edge $\{x, y\}$ give the same answers to all the calls, but they need different outputs, so the algorithm is wrong on one of them. $\square$ With `neighbors` instead, the same question takes $O(n)$ time: call `neighbors` on each vertex and stop at the first non-empty list. This is why the choice of representation changes the cost of an algorithm, and not only its constant factor.

**Output size.** Each algorithm that must look at all edges takes $\Omega(n + m)$ time on an adjacency list, because it must at least read the input. On an adjacency matrix the same algorithms usually take $\Omega(n^2)$ time, for the reason of the previous paragraph.

## References
