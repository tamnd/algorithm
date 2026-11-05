---
tag: T3TVBA
kind: theorem
slug: delta-plus-one-bound
name: Delta plus one coloring bound
aliases:
- greedy coloring bound
area: graphs/coloring-and-cliques
level: intro
summary: Greedy coloring always uses at most Delta plus one colors, where Delta is the maximum degree.
prereqs: [greedy-coloring, degree, chromatic-number]
see_also: [brooks-theorem, degeneracy, degeneracy-ordering, vizing-theorem, chromatic-index, graph-coloring]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 5.2, Colouring vertices (the greedy bound χ(G) ≤ Δ(G) + 1, the colouring number, and Brooks' theorem)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 5.1, Vertex colorings and upper bounds (the greedy bound, the Szekeres-Wilf bound and Brooks' theorem)
  - paper: doi:10.1016/S0021-9800(68)80081-X
    title: G. Szekeres and H. S. Wilf, An inequality for the chromatic number of a graph, Journal of Combinatorial Theory 4(1), 1 to 3 (1968)
    locator: the whole paper (χ(G) ≤ 1 + the maximum over subgraphs H of the minimum degree of H)
  - paper: doi:10.1017/S030500410002168X
    title: R. L. Brooks, On colouring the nodes of a network, Proceedings of the Cambridge Philosophical Society 37(2), 194 to 197 (1941)
    locator: the whole paper (the characterization of the cases with χ = Δ + 1)
---

The $\Delta + 1$ bound says that each graph with maximum [degree](/degree/) $\Delta$ has a proper coloring with $\Delta + 1$ colors, and that [greedy coloring](/greedy-coloring/) finds one in any vertex order. So the [chromatic number](/chromatic-number/) satisfies $\chi(G) \le \Delta(G) + 1$. The bound is tight for complete graphs and odd cycles, and [Brooks' theorem](/brooks-theorem/) shows that these are the only connected graphs that reach it. The same proof with a better order gives the stronger bound $\chi(G) \le d + 1$, where $d$ is the [degeneracy](/degeneracy/).

## Statement

Let $G = (V, E)$ be a finite simple undirected graph with maximum degree $\Delta = \max_{v \in V} \deg(v)$ (with $\Delta = 0$ when $V = \emptyset$).

**Theorem.** For every order $\sigma$ of $V$, greedy coloring in the order $\sigma$ gives a proper coloring $c$ with $c(v) \le \deg(v) + 1 \le \Delta + 1$ for each vertex $v$. In particular $\chi(G) \le \Delta + 1$.

**Stronger form (Szekeres and Wilf 1968).** Let $d = \max_{H} \delta(H)$, where $H$ runs over the subgraphs of $G$ and $\delta(H)$ is the minimum degree of $H$. Then $\chi(G) \le d + 1$.

## In plain words

Give the vertices their colors one at a time. When a vertex gets its turn, at most as many of its neighbors already have a color as it has neighbors. Those neighbors can block at most that many colors. If you have one color more than the largest number of neighbors that any vertex has, there is always a free color left. So you never get stuck, whatever order you use.

## Proof

**Greedy bound.** Let $\sigma = (v_1, \ldots, v_n)$. Greedy coloring gives $v_i$ the smallest positive integer that is not the color of a neighbor $v_j$ with $j < i$. We show by induction on $i$ that after step $i$ the colored vertices form a proper coloring and $c(v_j) \le \deg(v_j) + 1$ for each $j \le i$. For $i = 0$ nothing is colored. At step $i$, let $N^-$ be the set of neighbors of $v_i$ that come before it; $|N^-| \le \deg(v_i)$. The colors of $N^-$ are at most $|N^-|$ distinct values. So at least one of the $\deg(v_i) + 1$ values $1, \ldots, \deg(v_i) + 1$ is free, and the smallest free value is at most $\deg(v_i) + 1$. The color of $v_i$ differs from each color in $N^-$. Each edge between colored vertices is either an old edge, proper by the induction hypothesis, or an edge from $v_i$ to $N^-$, proper by the choice. This completes the induction. At $i = n$ all vertices are colored, the coloring is proper, and it uses colors in $\{1, \ldots, \Delta + 1\}$. So $\chi(G) \le \Delta + 1$.

**Stronger form.** Build an order backwards. Let $G_n = G$. For $i = n, n - 1, \ldots, 1$, let $v_i$ be a vertex of minimum degree in $G_i$, and let $G_{i-1} = G_i - v_i$. Each $G_i$ is a subgraph of $G$, so $\deg_{G_i}(v_i) = \delta(G_i) \le d$. The neighbors of $v_i$ that come before it in $(v_1, \ldots, v_n)$ are exactly its neighbors in $G_i$, because $G_i$ has the vertex set $\{v_1, \ldots, v_i\}$. So $v_i$ has at most $d$ earlier neighbors. The induction of the greedy bound, with $\deg(v_i)$ replaced by the number of earlier neighbors, gives a proper coloring with at most $d + 1$ colors. $\blacksquare$

## Consequences

- **Greedy is safe.** [Greedy coloring](/greedy-coloring/) in any order stays within $\Delta + 1$ colors, in $O(n + m)$ time. Online algorithms use this: a vertex can always get a color from a palette of $\Delta + 1$ colors at arrival.
- **Degeneracy.** The stronger form says $\chi(G) \le d + 1$, where $d$ is the [degeneracy](/degeneracy/); the backward order of the proof is the [smallest-last ordering](/degeneracy-ordering/).
- **Planar graphs.** A planar graph has a vertex of degree at most 5, and so has each of its subgraphs, so $d \le 5$ and $\chi \le 6$. The [five color theorem](/five-color-theorem/) and the [four color theorem](/four-color-theorem/) improve this.
- **Edge coloring.** Applied to the [line graph](/line-graph/), which has maximum degree at most $2\Delta - 2$, the bound gives $\chi'(G) \le 2\Delta - 1$. [Vizing's theorem](/vizing-theorem/) improves this to $\Delta + 1$.
- **Distributed and parallel coloring.** $(\Delta + 1)$-coloring is the standard target of [distributed vertex coloring](/distributed-vertex-coloring/), because the theorem guarantees that a vertex can always pick a free color.

## Tightness

- **Complete graphs.** $K_{\Delta + 1}$ has maximum degree $\Delta$ and needs $\Delta + 1$ colors, since all its vertices are pairwise adjacent.
- **Odd cycles.** An odd cycle has $\Delta = 2$ and needs 3 colors.
- **Nothing else that is connected.** By [Brooks' theorem](/brooks-theorem/), a connected graph that is neither complete nor an odd cycle has $\chi \le \Delta$.
- **Far from tight in general.** The star $K_{1, n-1}$ has $\Delta = n - 1$ but $\chi = 2$ (for $n \ge 2$), and its degeneracy is 1. So the bound can be off by a factor of order $n$, and the degeneracy bound fixes this case.
- **The degeneracy bound is also tight.** $K_{d+1}$ has degeneracy $d$ and $\chi = d + 1$. It can also be far off: the complete bipartite graph $K_{t, t}$ has degeneracy $t$ and $\chi = 2$.

## History

The greedy argument is folklore, and its first appearance is not clear. Szekeres and Wilf published the bound by the largest minimum degree of a subgraph in 1968. Brooks characterized the connected graphs that need $\Delta + 1$ colors in 1941; that result is on the page of [Brooks' theorem](/brooks-theorem/).

## References
