---
tag: H5RQYQ
kind: definition
slug: regular-graph
name: Regular graph
aliases:
- k-regular graph
area: graphs/graph-representation
level: intro
summary: Graph in which every vertex has the same degree.
prereqs: [degree, simple-graph, handshake-lemma]
see_also: [degree, complete-graph, bipartite-graph, handshake-lemma, edge-coloring, spectral-gap, line-graph, neighborhood]
sources:
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 1.3, regular graphs and k-regular graphs, and the existence of k-regular graphs; Section 3.1, the perfect matching in a regular bipartite graph
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Chapter 1, Section 1.2 (The degree of a vertex), k-regular and cubic graphs; Chapter 2, Section 2.1, Hall's theorem and regular bipartite graphs
  - book: isbn:9780387952208
    title: Chris Godsil and Gordon Royle, Algebraic Graph Theory, Graduate Texts in Mathematics 207, Springer, 2001
    locator: Chapter 8 (Matrix theory), the largest eigenvalue of the adjacency matrix of a k-regular graph
---

A regular graph is a [graph](/graph/) in which every [vertex](/vertex/) has the same [degree](/degree/). If that degree is $k$, the graph is $k$-regular: 0-regular graphs have no edges, 1-regular graphs are perfect matchings, 2-regular graphs are disjoint cycles, and 3-regular graphs are called cubic. Regular graphs are the uniform case of many results: their degree sum is $kn$, their adjacency spectrum starts at $k$, and a regular [bipartite graph](/bipartite-graph/) always has a perfect matching. Expander graphs, the [complete graph](/complete-graph/) and the hypercube are regular.

## Definition

Let $G = (V, E)$ be an undirected graph, [simple](/simple-graph/) unless said otherwise, with $n = |V|$. $G$ is **$k$-regular** if $d(v) = k$ for every $v \in V$, and **regular** if it is $k$-regular for some $k$. For a [multigraph](/multigraph/) the same definition is used, with a [self-loop](/self-loop/) adding 2 to the degree.

A directed graph is **$k$-regular** if $d^+(v) = d^-(v) = k$ for every vertex $v$; see [in-degree and out-degree](/in-degree-and-out-degree/).

**Basic facts.** Let $G$ be simple and $k$-regular on $n$ vertices.

- **Edge count.** By the [handshake lemma](/handshake-lemma/), $kn = 2m$, so $m = kn/2$. Hence $kn$ is even: there is no $k$-regular graph with both $k$ and $n$ odd. For example, no cubic graph has 5 vertices.
- **Existence.** For $0 \le k \le n - 1$, a simple $k$-regular graph on $n$ vertices exists if and only if $kn$ is even. *Construction.* Put the vertices $0, \ldots, n - 1$ on a circle. If $k$ is even, join each $i$ to $i \pm 1, \ldots, i \pm k/2 \pmod n$. If $k$ is odd, then $n$ is even; do the same for $k - 1$ and also join each $i$ to $i + n/2$. Each vertex gets degree $k$, and no pair is joined twice, because $k \le n - 1$.
- **Complement.** The [complement](/complement-graph/) of a $k$-regular graph is $(n - 1 - k)$-regular.
- **Spectrum.** The [adjacency matrix](/adjacency-matrix/) $A$ has $A\mathbf{1} = k\mathbf{1}$, so $k$ is an eigenvalue with the all-ones eigenvector. Every eigenvalue $\lambda$ satisfies $|\lambda| \le k$, and the multiplicity of $k$ is the number of components. The [Laplacian](/laplacian-matrix/) is $L = kI - A$, so its eigenvalues are $k - \lambda$; the difference $k - \lambda_2$ is the [spectral gap](/spectral-gap/).
- **Matchings and colorings.** A $k$-regular bipartite graph with $k \ge 1$ has a perfect matching, by Hall's theorem: for a set $S$ on one side, the $k|S|$ edges at $S$ end in $N(S)$, which can take at most $k|N(S)|$ edges, so $|N(S)| \ge |S|$. Removing the matching leaves a $(k - 1)$-regular bipartite graph, so the edges split into $k$ perfect matchings and the [edge chromatic number](/edge-coloring/) is $k$.
- **Line graphs.** If $G$ is $k$-regular, its [line graph](/line-graph/) is $(2k - 2)$-regular, since an edge $uv$ meets $k - 1$ other edges at $u$ and $k - 1$ at $v$.

**Testing.** Deciding whether a graph is regular costs $\Theta(n + m)$ time from an [adjacency list](/adjacency-list/), where the degrees are the list lengths ($\Theta(n)$ if the lengths are stored), and $\Theta(n^2)$ from an [adjacency matrix](/adjacency-matrix/).

## Examples and non-examples

| graph | $n$ | $k$ | $m = kn/2$ |
|---|---|---|---|
| $\overline{K_n}$, no edges | $n$ | 0 | 0 |
| perfect matching on $2r$ vertices | $2r$ | 1 | $r$ |
| cycle $C_n$ | $n \ge 3$ | 2 | $n$ |
| complete graph $K_n$ | $n$ | $n - 1$ | $n(n-1)/2$ |
| complete bipartite $K_{k,k}$ | $2k$ | $k$ | $k^2$ |
| hypercube $Q_d$, the $d$-bit strings joined when they differ in one bit | $2^d$ | $d$ | $d \, 2^{d-1}$ |
| Petersen graph | 10 | 3 | 15 |

**Non-examples.**

- The path $1\text{-}2\text{-}3$ has the degrees $1, 2, 1$. It is not regular.
- The star $K_{1,3}$ has the degrees $3, 1, 1, 1$. It is not regular, though its leaves all have the same degree.
- The directed cycle $1 \to 2 \to 3 \to 1$ is 1-regular as a directed graph. The directed graph with the edges $(1, 2)$ and $(1, 3)$ is not: $d^+(1) = 2$ and $d^-(1) = 0$.

**Construction.** For $n = 6$ and $k = 3$, join each $i$ to $i \pm 1$ and to $i + 3 \pmod 6$. This gives the 9 edges $01, 12, 23, 34, 45, 50, 03, 14, 25$, and the graph is $K_{3,3}$, with the sides $\{0, 2, 4\}$ and $\{1, 3, 5\}$.

## Related definitions

- **Degree.** The number of edge ends at a vertex. See [degree](/degree/).
- **Bounded degree.** A graph of maximum degree $\Delta$; many results for regular graphs hold with $\Delta$ in place of $k$. In [sparse graphs](/sparse-graph/) of bounded degree, $m \le \Delta n / 2$.
- **Strongly regular graph.** A $k$-regular graph in which each two adjacent vertices have $\lambda$ common neighbours and each two non-adjacent vertices have $\mu$ common neighbours. The Petersen graph has the parameters $(10, 3, 0, 1)$.
- **Expander.** A family of $k$-regular graphs with a spectral gap bounded away from 0. See [spectral gap](/spectral-gap/).
- **Vertex-transitive graph.** A graph whose [automorphism group](/graph-automorphism/) maps each vertex to each other vertex. Every vertex-transitive graph is regular, but not every regular graph is vertex-transitive.

## References
