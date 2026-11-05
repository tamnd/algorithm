---
tag: 41WNMS
kind: definition
slug: edge
name: Edge
aliases:
- arc
- link
area: graphs/graph-representation
level: intro
summary: Pair of vertices joined in a graph; ordered in directed graphs.
prereqs: [graph]
see_also: [vertex, directed-graph, undirected-graph, self-loop, multigraph, weighted-graph, degree, edge-list]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix B.4 (Graphs), the definitions of directed and undirected edges, incidence and adjacency
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 1.1 (Graphs) for edges, ends and incidence; Section 1.10 (Other notions of graphs) for directed edges and multigraphs
  - book: isbn:9781846289699
    title: J. A. Bondy and U. S. R. Murty, Graph Theory, Graduate Texts in Mathematics 244, Springer, 2008
    locator: Chapter 1 (Graphs), Section 1.1, the incidence function, loops and parallel edges
---

An edge is one of the connections of a [graph](/graph/): it joins two [vertices](/vertex/), called its ends. In an [undirected graph](/undirected-graph/) an edge is an unordered pair $\{u, v\}$, and in a [directed graph](/directed-graph/) it is an ordered pair $(u, v)$ that goes from $u$ to $v$. A directed edge is also called an *arc*. Edges are what a graph algorithm walks along, and their number $m$ is one of the two size measures of every graph bound.

## Definition

Let $V$ be a finite set of vertices.

**Undirected edge.** In a simple undirected graph $G = (V, E)$, an edge is a set $e = \{u, v\}$ with $u, v \in V$ and $u \ne v$, and $E$ is a set of such pairs. So

$$E \subseteq \binom{V}{2} = \{\{u, v\} : u, v \in V,\ u \ne v\}, \qquad 0 \le |E| \le \binom{n}{2} = \frac{n(n-1)}{2},$$

where $n = |V|$. The vertices $u$ and $v$ are the *ends* of $e$. The edge is *incident* with $u$ and with $v$, and $u$ and $v$ are *adjacent*, or *neighbours*. We often write $uv$ for $\{u, v\}$, and $uv = vu$.

**Directed edge.** In a directed graph $G = (V, E)$, an edge is an ordered pair $e = (u, v) \in V \times V$, and $E \subseteq V \times V$. The vertex $u$ is the *tail* of $e$ and $v$ is its *head*. The edge *leaves* $u$ and *enters* $v$. Here $(u, v) \ne (v, u)$ when $u \ne v$, so both can be in $E$. CLRS allows the pair $(v, v)$, a [self-loop](/self-loop/). So

$$0 \le |E| \le n^2 \text{ with self-loops}, \qquad 0 \le |E| \le n(n-1) \text{ without them}.$$

**Edge in a multigraph.** A [multigraph](/multigraph/) $G = (V, E, \psi)$ has a set $E$ of edge names, disjoint from $V$, and an incidence function $\psi$ that maps each $e \in E$ to its ends: an unordered pair $\{u, v\}$, with $u = v$ allowed for a loop, or an ordered pair $(u, v)$ in the directed case. Two edges $e \ne f$ with $\psi(e) = \psi(f)$ are *parallel*. Here an edge is a name, not a pair, because two parallel edges have the same pair of ends.

**Weighted edge.** A [weighted graph](/weighted-graph/) has a function $w : E \to \mathbb{R}$, and $w(e)$ is the weight, length or cost of $e$. For a simple graph we write $w(u, v)$.

**Notation.** The letter $m$ stands for $|E|$ on all pages of this area. CLRS writes $|E|$, and Diestel writes $\|G\|$.

## Examples and non-examples

**An undirected example.** Let $V = \{0, 1, 2, 3\}$ and $E = \{\{0, 1\}, \{0, 2\}, \{1, 2\}, \{2, 3\}\}$. So $m = 4$, out of $\binom{4}{2} = 6$ possible edges. The edge $\{2, 3\}$ is incident with 2 and 3. The vertices 0 and 3 are not adjacent.

**A directed example.** Let $V = \{0, 1, 2\}$ and $E = \{(0, 1), (1, 0), (1, 2)\}$. The edges $(0, 1)$ and $(1, 0)$ are two different edges, and together they form a cycle of length 2. The edge $(1, 2)$ leaves 1 and enters 2. There is no edge from 2 to 1. Out of the $3^2 = 9$ ordered pairs, 3 are edges.

**A weighted example.** In a road map, the edge $\{A, B\}$ with $w(A, B) = 12$ is a road of 12 kilometres between towns $A$ and $B$.

**Non-examples.**

- In a simple undirected graph, $\{v, v\} = \{v\}$ has one element, so it is not an edge. A loop at $v$ needs a multigraph or a directed graph.
- In a simple graph, adding $\{0, 1\}$ a second time does not make a second edge, since $E$ is a set. Two roads between the same two towns need a multigraph.
- The pair $(u, v)$ with $u \notin V$ is not an edge of $G$. Each end of each edge must be a vertex of the graph.
- An edge joins exactly two ends (or one, for a loop). A set of three or more vertices is an edge of a [hypergraph](/hypergraph/), not of a graph.

**Counts.** The table gives the largest possible number of edges on $n$ vertices.

| $n$ | undirected simple, $\binom{n}{2}$ | directed, no loops, $n(n-1)$ | directed with loops, $n^2$ |
|---|---|---|---|
| 1 | 0 | 0 | 1 |
| 2 | 1 | 2 | 4 |
| 4 | 6 | 12 | 16 |
| 10 | 45 | 90 | 100 |
| 1000 | 499500 | 999000 | 1000000 |

## Related definitions

- [Vertex](/vertex/): the objects that the edges join.
- [Degree](/degree/): the number of edges incident with a vertex. In a directed graph, the [in-degree and out-degree](/in-degree-and-out-degree/).
- [Self-loop](/self-loop/) and [multigraph](/multigraph/): edges that a simple graph forbids.
- [Directed graph](/directed-graph/) and [undirected graph](/undirected-graph/), compared on [directed and undirected graphs](/directed-and-undirected-graphs/).
- [Weighted graph](/weighted-graph/): edges with numbers.
- [Edge list](/edge-list/): the representation that stores the edges as an array of pairs.
- [Incidence matrix](/incidence-matrix/): the $n \times m$ matrix of the relation "vertex is an end of edge".
- [Line graph](/line-graph/): the graph whose vertices are the edges of a graph.

## References
