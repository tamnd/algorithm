---
tag: BZ3HHG
kind: definition
slug: eulerian-graph
name: Eulerian graph
aliases:
- Euler graph
area: graphs/paths-and-cycles
level: intro
summary: A connected graph that admits an Eulerian circuit; equivalently, a connected graph in which every vertex has even degree.
prereqs: [eulerian-circuit, connected-graph, degree]
see_also: [eulers-theorem-eulerian-graphs, eulerian-path, eulerian-path-problem, hierholzer-algorithm, cycle-basis, chinese-postman-problem, hamiltonian-cycle]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 1.8, Euler tours (a graph is Eulerian if it admits an Euler tour; Theorem 1.8.1) and Section 1.9, Some linear algebra (the cycle space as the set of edge sets with all degrees even)
  - book: isbn:9781846289699
    title: J. A. Bondy and U. S. R. Murty, Graph Theory, Graduate Texts in Mathematics 244, Springer, 2008
    locator: Chapter 3, Connected graphs, Section 3.3, Euler tours (eulerian graphs and even graphs)
  - book: "Norman L. Biggs, E. Keith Lloyd and Robin J. Wilson, Graph Theory 1736-1936, Clarendon Press, Oxford, 1976"
    locator: Chapter 1, Paths (Euler's paper of 1736 and Hierholzer's paper of 1873, with commentary)
---

An Eulerian graph is a [connected graph](/connected-graph/) that has an [Eulerian circuit](/eulerian-circuit/), a closed trail through every edge exactly once. By [Euler's theorem](/eulers-theorem-eulerian-graphs/), a connected undirected graph is Eulerian exactly when every vertex has even [degree](/degree/), and a connected directed graph is Eulerian exactly when every vertex has in-degree equal to out-degree. So the property is a local degree test plus one connectivity test, and it takes linear time to check. The word has more than one meaning in the literature, so this page also fixes the conventions.

## Definition

Let $G = (V, E)$ be a finite graph with $V \ne \emptyset$. It may be directed or undirected, and it may have parallel edges and [self-loops](/self-loop/); a self-loop adds 2 to the degree of its vertex.

**Eulerian graph.** $G$ is *Eulerian* if it is connected (for a directed graph: its underlying undirected graph is connected) and it has an Eulerian circuit.

**Even graph.** $G$ is *even* if each vertex has even degree. A directed graph is *balanced* if $d^+(v) = d^-(v)$ for each vertex $v$.

**Equivalent forms.** For a connected undirected graph $G$, these are equivalent:

1. $G$ is Eulerian.
2. $G$ is even.
3. $E$ is the disjoint union of the edge sets of cycles, where a self-loop is a cycle of length 1 and two parallel edges form a cycle of length 2.

For a connected directed graph, the same holds with "balanced" in place of "even" and directed cycles in place of cycles. A balanced weakly connected directed graph is [strongly connected](/strongly-connected-graph/). The proofs of 1 if and only if 2 and of the cycle decomposition are on the page of [Euler's theorem](/eulers-theorem-eulerian-graphs/).

**Semi-Eulerian.** A connected graph with an open [Eulerian path](/eulerian-path/) and no Eulerian circuit is *semi-Eulerian* (also *traversable*). An undirected connected graph is semi-Eulerian exactly when it has exactly two vertices of odd degree.

**Other conventions.**

- Some authors drop the word "connected" and call $G$ Eulerian if it has an Eulerian circuit. Then isolated vertices are allowed, and a graph with no edges is Eulerian. The difference matters only for graphs with isolated vertices.
- Some authors call a graph Eulerian when all degrees are even, without any connectivity condition. In that sense two disjoint triangles are Eulerian, but they have no Eulerian circuit. On this site such a graph is called *even*.
- In the [cycle space](/cycle-basis/) of a graph, the even spanning subgraphs are sometimes called Eulerian subgraphs, again without connectivity.

A page that uses the word must say which of these it means.

## Examples and non-examples

| graph | degrees | Eulerian? |
|---|---|---|
| cycle $C_n$, $n \ge 3$ | all 2 | yes |
| complete graph $K_n$, $n \ge 3$ | all $n - 1$ | exactly when $n$ is odd |
| complete bipartite $K_{a,b}$, $a, b \ge 1$ | $b$ on one side, $a$ on the other | exactly when $a$ and $b$ are both even |
| hypercube $Q_d$, $d \ge 1$ | all $d$ | exactly when $d$ is even |
| octahedron $K_{2,2,2}$ | all 4 | yes |
| wheel $W_n$ (a hub joined to a cycle of $n \ge 3$ vertices) | rim vertices 3 | no |
| Petersen graph | all 3 | no |
| two triangles that share one vertex | 2, 2, 4, 2, 2 | yes |
| two disjoint triangles | all 2 | no: even, but not connected |
| a triangle plus one isolated vertex | 2, 2, 2, 0 | no under the connected convention; yes if connectivity is dropped |
| one vertex with a self-loop | 2 | yes, the circuit is the loop |
| two vertices with three parallel edges | 3, 3 | no, semi-Eulerian |

**Directed examples.** A directed cycle is Eulerian. A tournament on $2k + 1$ vertices in which each vertex beats the next $k$ vertices around a circle is balanced, with $d^+ = d^- = k$, and is Eulerian. The transitive triangle $0 \to 1$, $1 \to 2$, $0 \to 2$ is not: its underlying graph is an even cycle, but vertex 0 has out-degree 2 and in-degree 0.

**How many even graphs.** On the labeled vertex set $\{1, \ldots, n\}$ with $n \ge 1$ there are exactly $2^{\binom{n-1}{2}}$ simple even graphs. *Proof.* Take any simple graph $H$ on $\{1, \ldots, n-1\}$, and join vertex $n$ to the vertices of odd degree in $H$. By the [handshake lemma](/handshake-lemma/), $H$ has an even number of odd vertices, so vertex $n$ gets even degree, and each other vertex becomes even. Conversely, an even graph $G$ arises in this way from $H = G - n$ and from no other graph, because the neighbours of $n$ in $G$ are exactly the odd vertices of $G - n$. So even graphs on $n$ vertices are in bijection with all simple graphs on $n - 1$ vertices. $\square$ For $n = 1, \ldots, 6$ this gives 1, 1, 2, 8, 64 and 1024 even graphs, of which 1, 0, 1, 3, 38 and 720 are connected, and so Eulerian.

## Related definitions

- [Eulerian circuit](/eulerian-circuit/) and [Eulerian path](/eulerian-path/): the trails that the definition asks for.
- [Euler's theorem](/eulers-theorem-eulerian-graphs/): the degree characterization and its proof.
- [Eulerian path problem](/eulerian-path-problem/): find the circuit, in linear time, with [Hierholzer's algorithm](/hierholzer-algorithm/).
- [Hamiltonian cycle](/hamiltonian-cycle/): a closed walk through every vertex once. Being Hamiltonian is NP-complete to decide, while being Eulerian takes linear time.
- [Cycle basis](/cycle-basis/): the even spanning subgraphs form the cycle space, a vector space over $\mathrm{GF}(2)$.
- [Chinese postman problem](/chinese-postman-problem/): for a graph that is not Eulerian, the cheapest set of repeated edges that makes it Eulerian.

## References
