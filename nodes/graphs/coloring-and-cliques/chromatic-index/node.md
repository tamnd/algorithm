---
tag: GBSZKN
kind: concept
slug: chromatic-index
name: Chromatic index
aliases:
- edge chromatic number
area: graphs/coloring-and-cliques
level: core
summary: Minimum number of colors needed to properly color the edges of a graph.
prereqs: [edge, degree, chromatic-number, line-graph]
see_also: [edge-coloring, vizing-theorem, konig-theorem, vizing-algorithm, line-graph, perfect-matching, four-color-theorem, regular-graph]
sources:
  - paper: doi:10.1007/BF01456961
    title: Dénes Kőnig, Über Graphen und ihre Anwendung auf Determinantentheorie und Mengenlehre, Mathematische Annalen 77(4), 453 to 465 (1916)
    locator: the theorem that the edges of a bipartite graph can be colored with Delta colors
  - paper: doi:10.1002/sapm1949281148
    title: Claude E. Shannon, A theorem on coloring the lines of a network, Journal of Mathematics and Physics 28, 148 to 151 (1949)
    locator: the whole paper (the bound 3 Delta / 2 for multigraphs)
  - paper: doi:10.1137/0210055
    title: Ian Holyer, The NP-completeness of edge-coloring, SIAM Journal on Computing 10(4), 718 to 720 (1981)
    locator: the main theorem (deciding whether a cubic graph has chromatic index 3 is NP-complete)
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 5.3, Edge-colouring (Kőnig's theorem and Vizing's theorem, with proofs)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 7.1, Line graphs and edge-coloring (the chromatic index, overfull graphs, Vizing's theorem)
---

The chromatic index $\chi'(G)$ of a [graph](/graph/) is the least number of colors in a coloring of its [edges](/edge/) such that edges with a common end get different colors. Each color class is a matching, so $\chi'(G)$ is the least number of matchings that cover the edges. Every vertex of [degree](/degree/) $\Delta$ forces $\Delta$ colors, and by [Vizing's theorem](/vizing-theorem/) $\Delta + 1$ colors always suffice for a simple graph, so $\chi'(G)$ takes one of only two values. Deciding which one is NP-complete.

## In plain words

Color the lines of a network instead of its points. Two lines that meet at a point must get different colors. The chromatic index is the fewest colors that make this work.

A point with many lines needs that many colors, since all its lines meet there. So the busiest point gives a lower limit. The surprise is that one more color than this limit is always enough. Every network needs either exactly the limit or one more.

Think of a sports league. Each line is a game between two teams, and each color is a round. A team plays at most one game per round. The chromatic index is the fewest rounds in which all games can be played.

## The idea

Let $G = (V, E)$ be a finite undirected graph without loops, with maximum degree $\Delta(G)$. A *proper edge coloring* with $k$ colors is a map $c : E \to \{1, \ldots, k\}$ with $c(e) \ne c(f)$ whenever $e \ne f$ share an end. The chromatic index is

$$\chi'(G) = \min \{ k : G \text{ has a proper edge coloring with } k \text{ colors} \}.$$

**Two views.** Each color class is a *matching*, a set of edges with no common end, so $\chi'(G)$ is the least number of matchings whose union is $E$. And two edges clash exactly when they are adjacent in the [line graph](/line-graph/) $L(G)$, so $\chi'(G) = \chi(L(G))$: the chromatic index is the [chromatic number](/chromatic-number/) of the line graph.

**Lower bounds.**

- $\chi'(G) \ge \Delta(G)$, since the edges at a vertex of degree $\Delta$ need distinct colors.
- $\chi'(G) \ge m / \lfloor n/2 \rfloor$ for a graph with $n$ vertices and $m$ edges, since a matching has at most $\lfloor n/2 \rfloor$ edges. A graph with $m > \Delta \lfloor n/2 \rfloor$ is called *overfull*. A $\Delta$-regular graph with $\Delta \ge 1$ and $n$ odd is overfull, since $m = \Delta n / 2 > \Delta (n-1)/2$.
- More generally, $\chi'(G) \ge |E(H)| / \lfloor |V(H)|/2 \rfloor$ for every subgraph $H$ with at least 2 vertices.

**Upper bounds.**

- $\chi'(G) \le 2\Delta - 1$ by greedy coloring of the edges: an edge $uv$ meets at most $2(\Delta - 1)$ other edges.
- $\chi'(G) \le \Delta + 1$ for simple graphs ([Vizing](/vizing-theorem/) 1964). For a multigraph with edge multiplicity at most $\mu$, $\chi'(G) \le \Delta + \mu$ (Vizing), and $\chi'(G) \le \lfloor 3\Delta/2 \rfloor$ (Shannon 1949).
- $\chi'(G) = \Delta$ for every bipartite multigraph ([Kőnig](/konig-theorem/) 1916).

**Class 1 and class 2.** A simple graph is *class 1* if $\chi'(G) = \Delta$ and *class 2* if $\chi'(G) = \Delta + 1$. Holyer (1981) proved that deciding whether a cubic graph is class 1, that is, 3-edge-colorable, is NP-complete. So the two-value range does not make the exact value easy. The proof of Vizing's theorem is constructive and gives a $(\Delta + 1)$-edge coloring in polynomial time, the [Misra and Gries algorithm](/vizing-algorithm/), so $\chi'$ can be approximated within an additive 1.

**Regular graphs and perfect matchings.** In a class 1 $\Delta$-regular graph, every color class meets every vertex, so it is a [perfect matching](/perfect-matching/). So a $\Delta$-regular graph is class 1 exactly when its edges split into $\Delta$ perfect matchings. A cubic graph with a bridge is class 2: each side of the bridge has $k$ vertices with degree sum $3k - 1$, which is even, so $k$ is odd, and every perfect matching must use the bridge. So three perfect matchings cannot be disjoint.

## Examples

| graph | $\Delta$ | $\chi'$ | class | reason |
|---|---|---|---|---|
| even cycle $C_6$ | 2 | 2 | 1 | alternate two colors |
| odd cycle $C_5$ | 2 | 3 | 2 | overfull: 5 edges, matchings of size at most 2 |
| star $K_{1,4}$ | 4 | 4 | 1 | all 4 edges meet at the center |
| $K_4$ | 3 | 3 | 1 | three perfect matchings $\{01, 23\}$, $\{02, 13\}$, $\{03, 12\}$ |
| $K_5$ | 4 | 5 | 2 | overfull: 10 edges, matchings of size at most 2 |
| $K_6$ | 5 | 5 | 1 | $K_{2k}$ splits into $2k - 1$ perfect matchings |
| $K_{3,3}$ | 3 | 3 | 1 | bipartite, so Kőnig's theorem applies |
| Petersen graph | 3 | 4 | 2 | cubic, but no 3 disjoint perfect matchings |

In general $\chi'(K_n) = n - 1$ for even $n$ and $n$ for odd $n \ge 3$, and $\chi'(K_{a,b}) = \max(a, b)$.

**The Petersen graph is class 2.** It is cubic with 10 vertices, so a 3-edge coloring would split its 15 edges into 3 perfect matchings, and any two of them would form a 2-factor made of even cycles. Every 2-factor of the Petersen graph is two 5-cycles, which are odd. So $\chi'$ is 4. Bridgeless cubic class 2 graphs are called *snarks* when they also meet some non-triviality conditions, usually girth at least 5 and cyclic 4-edge-connectivity. The Petersen graph is the smallest snark.

**The 1-factorization of $K_6$.** With vertices $\infty, 0, 1, 2, 3, 4$, color $i \in \{0, \ldots, 4\}$ takes the edge $\{\infty, i\}$ and the edges $\{i - j, i + j\}$ modulo 5 for $j = 1, 2$. These 5 matchings of size 3 cover all 15 edges once. This is the round-robin schedule of a tournament with 6 teams.

## Where it is used

- **Round-robin tournaments.** With $n$ teams, $n$ even, a schedule in $n - 1$ rounds is a $1$-factorization of $K_n$, an edge coloring with $\chi'(K_n) = n - 1$ colors.
- **Open shop scheduling.** Jobs and machines form a bipartite multigraph, with one edge per unit operation. Kőnig's theorem gives a schedule whose length equals the largest load of a job or machine. See [edge coloring](/edge-coloring/).
- **Switching and data migration.** Each port or disk takes part in one transfer per step, so the transfers of one step form a matching, and the least number of steps is a chromatic index.
- **The four color theorem.** Tait (1880) showed that the [four color theorem](/four-color-theorem/) is equivalent to the statement that every bridgeless cubic planar graph is class 1. So the search for snarks, class 2 graphs among cubic graphs, is linked to the theorem.
- **Bounds on matchings.** $\chi'(G) \le \Delta + 1$ gives a matching with at least $m / (\Delta + 1)$ edges, since one color class has at least the average size.

## References
