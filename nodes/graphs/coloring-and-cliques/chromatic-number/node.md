---
tag: CGCT6W
kind: concept
slug: chromatic-number
name: Chromatic number
aliases:
- chi(G)
area: graphs/coloring-and-cliques
level: intro
summary: Minimum number of colors in a proper coloring of a graph.
prereqs: [graph-coloring, independent-set, clique]
see_also: [clique-number, independence-number, delta-plus-one-bound, brooks-theorem, mycielski-graph, chromatic-index, chromatic-polynomial, perfect-graph]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Chapter 5, Colouring (Section 5.2, Colouring vertices), and Section 11.2 (Erdős's graphs of large girth and large chromatic number)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 5.1, Vertex colorings and upper bounds, and Section 5.2, Structure of k-chromatic graphs (Mycielski's construction)
  - paper: doi:10.2307/2306658
    title: E. A. Nordhaus and J. W. Gaddum, On complementary graphs, The American Mathematical Monthly 63(3), 175 to 177 (1956)
    locator: the whole paper (the bounds on χ(G) + χ(complement of G) and on their product)
  - paper: doi:10.4153/CJM-1959-003-9
    title: Paul Erdős, Graph theory and probability, Canadian Journal of Mathematics 11, 34 to 38 (1959)
    locator: the whole paper (graphs with large girth and large chromatic number exist)
---

The chromatic number $\chi(G)$ of a [graph](/graph/) $G$ is the least number of colors in a proper [coloring](/graph-coloring/) of its vertices, one in which the two ends of each edge get different colors. Equivalently, it is the least number of [independent sets](/independent-set/) that cover the vertex set. It lies between the [clique number](/clique-number/) $\omega(G)$ and $\Delta(G) + 1$, where $\Delta$ is the maximum [degree](/degree/), and both ends can be far from it. Computing it is NP-hard, and it cannot even be approximated well in polynomial time unless P = NP.

## In plain words

Some pairs of things in a set clash and must get different labels. The chromatic number is the least number of labels that you need. One label is enough when nothing clashes. Two labels are enough exactly when the things split into two groups with all clashes between the groups.

A group of things that all clash with each other needs one label each. So the size of the largest such group is a lower bound. The answer can still be much larger, because clashes can force colors in a long chain, without a big group of mutual clashes.

## The idea

Let $G = (V, E)$ be a finite simple undirected graph with $n$ vertices.

$$\chi(G) = \min \{ k : \exists\, c : V \to \{1, \ldots, k\} \text{ with } c(u) \ne c(v) \text{ for each } \{u, v\} \in E \}.$$

A graph is *$k$-colorable* when $\chi(G) \le k$, and *$k$-chromatic* when $\chi(G) = k$. A graph is *$k$-critical* when it is $k$-chromatic and each proper subgraph has a smaller chromatic number. Odd cycles are the 3-critical graphs.

**Lower bounds.**

- $\chi(G) \ge \omega(G)$, the size of a largest [clique](/clique/): the vertices of a clique need pairwise different colors.
- $\chi(G) \ge n / \alpha(G)$, where $\alpha(G)$ is the [independence number](/independence-number/): each color class is independent, so it has at most $\alpha(G)$ vertices, and $k$ classes cover $n$ vertices only if $k \alpha(G) \ge n$.
- $\chi(G) \ge 3$ exactly when $G$ has an odd cycle, by the [odd cycle theorem](/bipartite-odd-cycle-theorem/).

**Upper bounds.**

- $\chi(G) \le \Delta(G) + 1$, by [greedy coloring](/greedy-coloring/) ([the $\Delta + 1$ bound](/delta-plus-one-bound/)).
- $\chi(G) \le d + 1$, where $d$ is the [degeneracy](/degeneracy/), by greedy coloring in [smallest-last order](/degeneracy-ordering/).
- $\chi(G) \le \Delta(G)$ for a connected graph that is neither complete nor an odd cycle ([Brooks' theorem](/brooks-theorem/)).
- $\chi(G) \le 4$ for a planar graph ([four color theorem](/four-color-theorem/)).

**Rules of computation.**

- For a disjoint union, $\chi(G_1 \cup G_2) = \max(\chi(G_1), \chi(G_2))$: color each part on its own with the same palette.
- If $G$ is the union of two graphs $G_1$ and $G_2$ on the same vertex set, then $\chi(G) \le \chi(G_1) \chi(G_2)$: give $v$ the pair $(c_1(v), c_2(v))$; an edge of $G$ is an edge of $G_1$ or of $G_2$, so the pairs of its ends differ.
- For the [complement](/complement-graph/) $\overline G$: $\chi(G) \chi(\overline G) \ge n$, because a color class of $G$ is a clique of $\overline G$, so it has at most $\omega(\overline G) \le \chi(\overline G)$ vertices. Nordhaus and Gaddum (1956) proved $\chi(G) + \chi(\overline G) \le n + 1$ and $\chi(G) \chi(\overline G) \le \left( \frac{n+1}{2} \right)^2$.

**No local reason.** A large chromatic number does not need a large clique, or even a short cycle. Mycielski's construction turns a triangle-free $k$-chromatic graph into a triangle-free $(k+1)$-chromatic graph (see [Mycielski graph](/mycielski-graph/)). Erdős (1959) proved with the [probabilistic method](/probabilistic-method/) that for all $g$ and $k$ there are graphs with no cycle shorter than $g$ and with $\chi > k$.

**Complexity.** Deciding $\chi(G) \le 2$ takes $O(n + m)$ time ([bipartiteness testing](/bipartiteness-testing/)). Deciding $\chi(G) \le 3$ is NP-complete. The exact value can be computed in $O^*(2^n)$ time by [Björklund's algorithm](/bjorklund-chromatic-number/). The details and the hardness of approximation are on the page of the [graph coloring problem](/graph-coloring/).

## Examples

| graph | $n$ | $\omega$ | $\alpha$ | $\lceil n / \alpha \rceil$ | $\Delta + 1$ | $\chi$ |
|---|---|---|---|---|---|---|
| empty graph | 0 | 0 | 0 | not defined | 1 | 0 |
| tree with at least one edge | any | 2 | at least $n/2$ | 2 | any | 2 |
| even cycle $C_8$ | 8 | 2 | 4 | 2 | 3 | 2 |
| odd cycle $C_7$ | 7 | 2 | 3 | 3 | 3 | 3 |
| complete graph $K_5$ | 5 | 5 | 1 | 5 | 5 | 5 |
| $K_{3,3}$ | 6 | 2 | 3 | 2 | 4 | 2 |
| Petersen graph | 10 | 2 | 4 | 3 | 4 | 3 |
| Grötzsch graph | 11 | 2 | 5 | 3 | 6 | 4 |
| star $K_{1,9}$ | 10 | 2 | 9 | 2 | 10 | 2 |

The Petersen graph shows a case where $\omega$ is too low and $\lceil n/\alpha \rceil$ is right. The Grötzsch graph is a case where both lower bounds are too low. The star is a case where $\Delta + 1$ is far too high.

**A proof that $\chi(C_7) = 3$.** A 3-coloring is $1, 2, 1, 2, 1, 2, 3$ around the cycle. A 2-coloring would alternate, so the vertex $i$ would get the color of vertex $0$ exactly when $i$ is even; vertex 6 is then the same color as vertex 0, but they are adjacent.

**The Mycielski sequence.** Starting from $K_2$, the construction gives graphs with $n = 2, 5, 11, 23, 47, \ldots$ vertices ($n_{k+1} = 2 n_k + 1$), no triangle, and $\chi = 2, 3, 4, 5, 6, \ldots$. The second is $C_5$ and the third is the Grötzsch graph.

## Where it is used

- [Graph coloring](/graph-coloring/) is the problem of computing $\chi(G)$ and an optimal coloring; scheduling, register allocation and frequency assignment use it.
- [Perfect graphs](/perfect-graph/) are the graphs in which $\chi(H) = \omega(H)$ for each induced subgraph $H$. [Chordal graphs](/chordal-graph/) and [bipartite graphs](/bipartite-graph/) are perfect.
- The [chromatic polynomial](/chromatic-polynomial/) $P(G, k)$ counts the proper $k$-colorings, and $\chi(G)$ is the least positive integer $k$ with $P(G, k) > 0$.
- The [chromatic index](/chromatic-index/) is the chromatic number of the [line graph](/line-graph/).
- The [Lovász theta function](/lovasz-theta-function/) lies between $\omega(G)$ and $\chi(G)$ and is computable in polynomial time.
- [Hadwiger's conjecture](/hadwiger-conjecture/) relates $\chi(G)$ to the largest complete [graph minor](/graph-minor/) of $G$.

## References
