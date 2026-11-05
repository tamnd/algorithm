---
tag: PRJ8N0
kind: theorem
slug: petersens-theorem
name: Petersen's theorem
aliases:
- Petersen's 2-factor theorem
area: graphs/matching
level: advanced
summary: Every bridgeless cubic graph has a perfect matching.
prereqs: [tutte-theorem, regular-graph, bridge]
see_also: [perfect-matching, edge-coloring, four-color-theorem, eulerian-circuit, hall-theorem, counting-perfect-matchings, edge-connectivity, f-factor-problem]
sources:
  - paper: doi:10.1007/BF02392606
    title: Julius Petersen, Die Theorie der regulären graphs, Acta Mathematica 15, 193 to 220 (1891)
    locator: the whole paper (the 2-factor theorem for even regular graphs and the perfect matching theorem for cubic graphs)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 3.3, Matchings in general graphs (Petersen's theorem from Tutte's theorem, and the 2-factor theorem)
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer
    locator: Section 2.2, Matching in general graphs (Corollary 2.2.2, Petersen 1891)
  - book: isbn:9780821847596
    title: László Lovász and Michael D. Plummer, Matching Theory, AMS Chelsea Publishing
    locator: Chapter 3 (Petersen's theorem and its extensions) and Chapter 8 (the number of perfect matchings)
  - paper: "Therese C. Biedl, Prosenjit Bose, Erik D. Demaine and Anna Lubiw, Efficient algorithms for Petersen's matching theorem, Journal of Algorithms 38(1), 110 to 134 (2001)"
    locator: the whole paper (finding the perfect matching of a bridgeless cubic graph in near-linear time)
---

Petersen's theorem says that every cubic graph without a [bridge](/bridge/) has a [perfect matching](/perfect-matching/). A cubic graph is a [regular graph](/regular-graph/) in which every vertex has degree 3. The same 1891 paper by Julius Petersen also proved the 2-factor theorem: every regular graph of even degree splits into spanning subgraphs in which every vertex has degree 2. The first theorem follows in a few lines from [Tutte's theorem](/tutte-theorem/), by counting edges; the second follows from an [Eulerian circuit](/eulerian-circuit/) and [Hall's theorem](/hall-theorem/).

## Statement

All graphs are finite and undirected, without weights and without self-loops. Parallel edges are allowed. A graph is general here, not necessarily bipartite; odd cycles are allowed. A *bridge* is an edge whose deletion increases the number of connected components. A *$k$-factor* is a spanning subgraph in which every vertex has degree $k$, so a 1-factor is a perfect matching.

**Theorem 1 (Petersen, 1891).** Every cubic graph without a bridge has a perfect matching.

**Theorem 2 (Petersen's 2-factor theorem, 1891).** Every $2k$-regular graph, with $k \ge 1$, is the union of $k$ edge-disjoint 2-factors.

A stronger form of Theorem 1, by Schönberger (1934), says that each edge of a bridgeless cubic graph lies in some perfect matching.

## In plain words

In a cubic graph, every point has exactly three lines. Theorem 1 says: if no single line holds the graph together, so that cutting any one line leaves the graph in one piece, then you can choose lines that touch every point exactly once.

Theorem 2 is about graphs where every point has an even number of lines. You can sort the lines into groups so that, in each group, every point has exactly two lines. Each group is then a set of closed loops that together pass through every point once.

## Proof

**Theorem 1.** Let $G = (V, E)$ be cubic and bridgeless. We check Tutte's condition: $q(G - S) \le |S|$ for every $S \subseteq V$, where $q(G - S)$ is the number of components of $G - S$ with an odd number of vertices.

Let $K$ be an odd component of $G - S$, and let $e(K, S)$ be the number of edges between $K$ and $S$. The degrees of the vertices of $K$ add up to $3|K|$, which is odd. Each edge inside $K$ adds 2 to this sum, and every other edge at $K$ goes to $S$, because $K$ is a component of $G - S$. So $e(K, S) = 3|K| - 2|E(K)|$ is odd.

If $e(K, S) = 1$, that single edge is a bridge of $G$: deleting it separates $K$ from the rest. When $S = \emptyset$, there is no edge at all from $K$, and $K$ is a component of $G$ with an odd number of vertices, where the degree sum $3|K|$ would have to be even; so this case cannot occur. Hence $e(K, S) \ge 3$ for each odd component $K$.

Each vertex of $S$ has only 3 edges. Adding over the odd components,
$$3\, q(G - S) \le \sum_{K \text{ odd}} e(K, S) \le 3|S|.$$
So $q(G - S) \le |S|$, and by [Tutte's theorem](/tutte-theorem/) $G$ has a perfect matching. $\blacksquare$

**Theorem 2.** It is enough to treat a connected $2k$-regular graph $G$, since the factors of the components combine. Every degree is even, so $G$ has an [Eulerian circuit](/eulerian-circuit/). Walk along it and direct each edge in the direction of the walk. Every vertex is entered and left the same number of times, so each vertex has $k$ incoming and $k$ outgoing edges.

Build a [bipartite graph](/bipartite-graph/) $H$ with a copy $v^-$ of each vertex $v$ on the left and a copy $v^+$ on the right, and an edge $u^- w^+$ for each directed edge $u \to w$. Then $H$ is $k$-regular. A $k$-regular bipartite graph with $k \ge 1$ has a perfect matching by [Hall's theorem](/hall-theorem/): the $k|X|$ edges at a set $X$ of left vertices end in $N(X)$, which receives at most $k|N(X)|$ edges, so $|N(X)| \ge |X|$. A perfect matching of $H$ gives each vertex of $G$ one outgoing and one incoming edge, so it is a 2-factor of $G$. Deleting it leaves a $(2k - 2)$-regular graph, and induction on $k$ gives $k$ edge-disjoint 2-factors. $\blacksquare$

**Example.** The Petersen graph is cubic and bridgeless, so it has a perfect matching: the five spokes between the outer 5-cycle and the inner pentagram. It has exactly 6 perfect matchings. The complement of a perfect matching in a cubic graph is a 2-factor; for the spokes it is the outer 5-cycle and the inner 5-cycle. The 3-cube $Q_3$ is cubic, bridgeless and bipartite, and has 9 perfect matchings.

## Consequences

- **Cubic graphs split into a 1-factor and a 2-factor.** In a bridgeless cubic graph, the edges outside a perfect matching form a 2-factor, a set of disjoint cycles through all vertices.
- **[Edge coloring](/edge-coloring/).** A bridgeless cubic graph has a 3-edge-coloring if and only if it has a 2-factor whose cycles are all even. The Petersen graph has no 3-edge-coloring: each of its 2-factors is two 5-cycles. Tait showed that the [four color theorem](/four-color-theorem/) is equivalent to the claim that every bridgeless cubic planar graph is 3-edge-colorable.
- **Regular graphs of higher degree.** By the same counting, every $k$-regular graph with an even number of vertices and edge connectivity at least $k - 1$ has a perfect matching.
- **Number of perfect matchings.** Lovász and Plummer conjectured that bridgeless cubic graphs have exponentially many perfect matchings. Esperet, Kardoš, King, Král' and Norine proved it in 2011: at least $2^{n/3656}$ of them for $n$ vertices.
- **Algorithms.** A perfect matching of a bridgeless cubic graph can be found by any [maximum matching](/maximum-matching/) algorithm in $O(n^{3/2})$ time, since $m = 3n/2$. Biedl, Bose, Demaine and Lubiw gave an $O(n \log^4 n)$ algorithm that uses the structure of the theorem.

## Tightness

The condition "bridgeless" cannot be dropped. Take a vertex $c$ and three disjoint copies of the following gadget: a complete graph $K_4$ on $x, y, a, b$ with the edge $xy$ removed, and a new vertex $w$ joined to $x$, $y$ and $c$. Each vertex of the gadget has degree 3, so the whole graph is cubic, with $1 + 3 \cdot 5 = 16$ vertices. The three edges at $c$ are bridges. For $S = \{c\}$, $G - S$ has three components with 5 vertices each, so $q(G - S) = 3 > 1$, and the graph has no perfect matching; its largest matching has 7 edges.

The bound is about bridges, not about the degree: a cubic graph with at most two bridges still has a perfect matching, because in the proof at most two odd components can have $e(K, S) = 1$, and the count becomes $3(q - 2) + 2 \le 3|S|$, which gives $q \le |S|$ once parity is used. With three bridges the example above shows failure.

## History

Julius Petersen published both theorems in 1891 in Acta Mathematica, in a paper on the theory of regular graphs. His proof of the cubic case was long and handled graphs with at most two bridges. Petersen also gave the graph now named after him, in 1898, as a bridgeless cubic graph with no 3-edge-coloring. Tutte's theorem of 1947 gave the short proof above. Schönberger proved in 1934 that every edge lies in a perfect matching.

## References
