---
tag: VWH63R
kind: definition
slug: degree
name: Degree
aliases:
- valency
area: graphs/graph-representation
level: intro
summary: Number of edges incident to a vertex in an undirected graph.
prereqs: [graph, edge]
see_also: [handshake-lemma, in-degree-and-out-degree, neighborhood, regular-graph, degree-distribution, degeneracy, self-loop, multigraph]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix B.4 (Graphs), the degree of a vertex, and the in-degree and out-degree in a directed graph
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 1.2 (The degree of a vertex), minimum, maximum and average degree
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 1.3 (Vertex degrees and counting), the degree-sum formula and degree sequences
---

The degree of a [vertex](/vertex/) $v$ in an undirected [graph](/graph/) is the number of [edges](/edge/) incident with $v$, written $d(v)$ or $\deg(v)$. In a simple graph it equals the number of neighbours of $v$, and in a [multigraph](/multigraph/) a [self-loop](/self-loop/) counts twice. The degrees of all vertices sum to twice the number of edges, by the [handshake lemma](/handshake-lemma/). In a directed graph the notion splits into the [in-degree and out-degree](/in-degree-and-out-degree/).

## Definition

**Simple graph.** Let $G = (V, E)$ be a simple undirected graph and $v \in V$. The *neighborhood* of $v$ is $N(v) = \{u \in V : \{u, v\} \in E\}$, and the **degree** of $v$ is

$$d(v) = |\{e \in E : v \in e\}| = |N(v)|.$$

The two counts are equal because the map $\{u, v\} \mapsto u$ is a bijection from the edges at $v$ to $N(v)$. So $0 \le d(v) \le n - 1$, where $n = |V|$.

**Multigraph.** In a multigraph with incidence function $\psi$, each edge $e$ adds to $d(v)$ the number of times $v$ is an end of $e$:

$$d(v) = |\{e : \psi(e) = \{v, u\},\ u \ne v\}| + 2\,|\{e : \psi(e) = \{v, v\}\}|.$$

So a loop at $v$ adds 2. This rule keeps the [handshake lemma](/handshake-lemma/) true for multigraphs. With parallel edges, $d(v)$ can be larger than $|N(v)|$.

**Directed graph.** For $G = (V, E)$ with $E \subseteq V \times V$, the *out-degree* $d^+(v) = |\{u : (v, u) \in E\}|$ and the *in-degree* $d^-(v) = |\{u : (u, v) \in E\}|$. Some authors call $d^+(v) + d^-(v)$ the degree of $v$. See [in-degree and out-degree](/in-degree-and-out-degree/).

**Words for special degrees and for the whole graph.**

- $v$ is *isolated* when $d(v) = 0$, and a *leaf* (or pendant vertex) when $d(v) = 1$.
- The *minimum degree* is $\delta(G) = \min_{v} d(v)$ and the *maximum degree* is $\Delta(G) = \max_{v} d(v)$, for $V \ne \emptyset$.
- The *average degree* is $\bar d(G) = \frac{1}{n} \sum_v d(v) = \frac{2m}{n}$, by the handshake lemma, with $m = |E|$.
- $G$ is *$k$-regular* when $d(v) = k$ for each $v$. See [regular graph](/regular-graph/).
- The *degree sequence* is the list of the degrees in non-increasing order. A list of integers is *graphic* when it is the degree sequence of some simple graph.

Since $\delta(G) \le \bar d(G) \le \Delta(G)$, the bound $\delta(G) \le 2m/n \le \Delta(G)$ holds in each graph with $n \ge 1$.

## Examples and non-examples

**A worked example.** Let $V = \{0, 1, 2, 3, 4, 5\}$ and

$$E = \{01, 02, 12, 13, 23, 34, 45\},$$

where $uv$ stands for $\{u, v\}$, so $m = 7$.

| vertex | $N(v)$ | $d(v)$ |
|---|---|---|
| 0 | 1, 2 | 2 |
| 1 | 0, 2, 3 | 3 |
| 2 | 0, 1, 3 | 3 |
| 3 | 1, 2, 4 | 3 |
| 4 | 3, 5 | 2 |
| 5 | 4 | 1 |

The degrees sum to $14 = 2m$. The degree sequence is $3, 3, 3, 2, 2, 1$. Here $\delta = 1$, $\Delta = 3$ and $\bar d = 14/6 = 7/3$. Vertex 5 is a leaf. Four vertices have odd degree, and four is even, as the [handshaking lemma](/handshaking-lemma/) requires.

**Special graphs.**

- In the [complete graph](/complete-graph/) $K_n$, each vertex has degree $n - 1$, so $K_n$ is $(n-1)$-regular.
- In a cycle on $n \ge 3$ vertices, each vertex has degree 2.
- In a [tree](/tree/) with $n \ge 2$ vertices, the degrees sum to $2(n - 1)$, and at least two vertices are leaves.
- In a star $K_{1, k}$, the centre has degree $k$ and the $k$ other vertices are leaves.

**A multigraph.** Take one vertex $v$ with one loop and two parallel edges to a vertex $u$. Then $d(v) = 2 + 2 = 4$ and $d(u) = 2$, and $|N(v)| = 2$ if we count $v$ as its own neighbour. The sum $6$ is twice the 3 edges.

**Non-examples.**

- The list $3, 3, 1$ is not a degree sequence: its sum is odd, and each degree sum is even.
- The list $3, 3, 1, 1$ has an even sum but is not graphic either. Two vertices of degree 3 among four vertices are each adjacent to all three others, so each of the other two vertices has degree at least 2.
- The number of neighbours is not the degree in a multigraph with parallel edges. Two parallel edges between $u$ and $v$ give $d(u) = 2$ but $|N(u)| = 1$.

**The cost of a degree query.** How fast a program finds $d(v)$ depends on the representation, with $n$ vertices and $m$ edges.

| representation | time of $d(v)$ | how |
|---|---|---|
| [adjacency list](/adjacency-list/) with stored lengths | $O(1)$ | the length of the list of $v$ |
| [compressed sparse row](/compressed-sparse-row/) | $O(1)$ | $\text{off}[v+1] - \text{off}[v]$ |
| [adjacency matrix](/adjacency-matrix/) | $\Theta(n)$ | sum of row $v$ |
| [bitset adjacency matrix](/bitset-adjacency-matrix/) | $O(n/w)$ | [population count](/population-count/) of row $v$, with $w$-bit words |
| [edge list](/edge-list/) | $\Theta(m)$ | count the edges with $v$ as an end |

All degrees at once take $\Theta(n + m)$ time from an edge list or an adjacency list, and $\Theta(n^2)$ time from an adjacency matrix.

## Related definitions

- [Neighborhood](/neighborhood/): the set $N(v)$.
- [In-degree and out-degree](/in-degree-and-out-degree/): degrees in a directed graph.
- [Handshake lemma](/handshake-lemma/) and [handshaking lemma](/handshaking-lemma/): the degree sum and the parity of the odd-degree vertices.
- [Regular graph](/regular-graph/): all degrees equal.
- [Degree distribution](/degree-distribution/) and [degree centrality](/degree-centrality/): degrees in network analysis.
- [Degeneracy](/degeneracy/): the largest minimum degree of a subgraph.
- [Dense graph](/dense-graph/) and [sparse graph](/sparse-graph/): the average degree compared with $n$.

## References
