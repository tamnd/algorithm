---
tag: 2RCNV0
kind: definition
slug: undirected-graph
name: Undirected graph
aliases:
- undirected edges graph
area: graphs/graph-representation
level: intro
summary: Graph whose edges are unordered pairs of vertices.
prereqs: [graph, vertex, edge]
see_also: [directed-graph, directed-and-undirected-graphs, simple-graph, multigraph, degree, handshake-lemma, connected-components, adjacency-list]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix B.4 (Graphs), undirected graphs, connectivity, the directed version of an undirected graph and the undirected version of a directed graph; Section 20.1, the 2|E| entries of an undirected adjacency list
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Chapter 1, Section 1.1 (Graphs), graphs as pairs (V, E) with E a set of 2-element subsets of V
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.1 (Undirected graphs), the Graph API, and each edge appearing twice in the adjacency lists
---

An undirected graph is a [graph](/graph/) whose [edges](/edge/) have no direction: an edge is an unordered pair $\{u, v\}$, so it joins $u$ to $v$ and $v$ to $u$ at once. It models symmetric relations: two people who know each other, two cities joined by a two-way road, two atoms joined by a bond. On this site, as in CLRS, an undirected graph is [simple](/simple-graph/) unless the page says otherwise: no [self-loops](/self-loop/) and no parallel edges. A program stores it as a [directed graph](/directed-graph/) in which each edge appears in both directions.

## Definition

An **undirected graph** is a pair $G = (V, E)$ where $V$ is a finite set of [vertices](/vertex/) and

$$E \subseteq \{\{u, v\} : u, v \in V,\ u \ne v\}$$

is a set of unordered pairs of distinct vertices. The edge $\{u, v\}$ is written $uv$ or $(u, v)$; then $(u, v)$ and $(v, u)$ name the same edge. The vertices $u$ and $v$ are its *ends*; they are *adjacent*, and the edge is *incident* to each of them. Write $n = |V|$ and $m = |E|$.

**Variants.** Allowing $\{v\}$ as an edge gives loops. Replacing the set $E$ by a set of edge names with an incidence function gives the [multigraph](/multigraph/), which may have parallel edges. These are different definitions and must be stated.

**Degree and neighbourhood.** $N(v) = \{u : uv \in E\}$ is the [neighborhood](/neighborhood/) of $v$ and $d(v) = |N(v)|$ its [degree](/degree/). Since each edge has two ends, $\sum_v d(v) = 2m$ (the [handshake lemma](/handshake-lemma/)), and the number of vertices of odd degree is even.

**Connectivity.** A *path* from $u$ to $v$ is a sequence of vertices $u = x_0, x_1, \ldots, x_k = v$ with $x_{i-1} x_i \in E$. The relation "there is a path from $u$ to $v$" is an equivalence relation on $V$, because a path can be reversed. Its classes are the [connected components](/connected-components/). For directed graphs this fails: reachability is not symmetric, and its analogue is the [strongly connected component](/strongly-connected-components/).

**Directed and undirected versions.** CLRS give two maps between the kinds:

- The *directed version* of an undirected $G$ replaces each edge $\{u, v\}$ by the two edges $(u, v)$ and $(v, u)$. It has $2m$ edges, and its [adjacency matrix](/adjacency-matrix/) is the matrix of $G$.
- The *undirected version* of a directed $G$ drops the directions, removes loops, and merges $(u, v)$ and $(v, u)$ into $\{u, v\}$. It has at most as many edges as $G$.

**Representations.** The usual forms store the directed version:

| representation | space | `adjacent(u, v)` | list $N(v)$ | add edge |
|---|---|---|---|---|
| [adjacency list](/adjacency-list/) | $\Theta(n + m)$, $2m$ entries | $O(1 + \min(d(u), d(v)))$ | $\Theta(1 + d(v))$ | $O(1)$, two inserts |
| [adjacency matrix](/adjacency-matrix/) | $\Theta(n^2)$, symmetric | $O(1)$ | $\Theta(n)$ | $O(1)$, two writes |
| [edge list](/edge-list/) | $\Theta(m)$, each edge once | $O(m)$ | $O(m)$ | $O(1)$ |
| [incidence matrix](/incidence-matrix/) | $\Theta(nm)$ | $O(m)$ | $O(m)$ | a new column |

Removing an edge from an adjacency list costs $O(d(u) + d(v))$, since both copies must be found. An undirected matrix can be stored as the upper triangle alone, in $\binom{n}{2}$ bits.

## Examples and non-examples

**Example.** $V = \{1, 2, 3, 4\}$ and $E = \{12, 13, 23, 34\}$. The degrees are $2, 2, 3, 1$, which sum to $8 = 2 \cdot 4$. The adjacency lists are $1: [2, 3]$, $2: [1, 3]$, $3: [1, 2, 4]$, $4: [3]$, with $8$ entries. The graph is connected. The directed version has the 8 edges $(1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (3, 2), (3, 4), (4, 3)$.

**A disconnected example.** $V = \{1, \ldots, 5\}$ and $E = \{12, 34\}$ has the three components $\{1, 2\}$, $\{3, 4\}$, $\{5\}$.

**Non-examples.**

- The "follows" relation of a social network is not undirected: $u$ may follow $v$ without $v$ following $u$. It is a directed graph.
- The pair $(V, E)$ with $V = \{1, 2\}$ and $E = \{\{1, 2\}, \{1\}\}$ is not an undirected graph in the sense used here, since $\{1\}$ is a loop. It is a graph with loops.
- A directed graph whose edge set is symmetric, $(u, v) \in E \iff (v, u) \in E$, is not the same object, but it carries the same data: it is the directed version of an undirected graph if it has no loops.

## Related definitions

- **Directed graph.** Edges are ordered pairs. See [directed graph](/directed-graph/) and [directed and undirected graphs](/directed-and-undirected-graphs/).
- **Simple graph.** No loops and no parallel edges. See [simple graph](/simple-graph/).
- **Multigraph.** Parallel edges are allowed. See [multigraph](/multigraph/).
- **Tree.** A connected undirected graph with no cycle. See [tree](/tree/).
- **Weighted graph.** An undirected graph with a weight $w(\{u, v\})$ on each edge, stored as the same weight on both directions. See [weighted graph](/weighted-graph/).

## References
