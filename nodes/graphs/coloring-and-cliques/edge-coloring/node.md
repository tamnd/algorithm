---
tag: 9PG84C
kind: problem
slug: edge-coloring
name: Edge coloring problem
aliases:
- edge-coloring
area: graphs/coloring-and-cliques
level: core
summary: Color edges so that incident edges differ, using as few colors as possible.
prereqs: [chromatic-index, graph-coloring, np-complete]
see_also: [chromatic-index, vizing-theorem, vizing-algorithm, konig-theorem, line-graph, bipartite-matching, distributed-edge-coloring, graph-coloring]
sources:
  - paper: doi:10.1137/0210055
    title: Ian Holyer, The NP-completeness of edge-coloring, SIAM Journal on Computing 10(4), 718 to 720 (1981)
    locator: the main theorem (3-edge-colorability of cubic graphs is NP-complete, by a reduction from 3-SAT)
  - paper: doi:10.1016/0020-0190(92)90041-S
    title: Jayadev Misra and David Gries, A constructive proof of Vizing's theorem, Information Processing Letters 41(3), 131 to 133 (1992)
    locator: the whole paper (fans and alternating paths, a (Delta + 1)-edge coloring in O(nm) time)
  - paper: doi:10.1007/s004930170002
    title: Richard Cole, Kirstin Ost and Stefan Schirra, Edge-coloring bipartite multigraphs in O(E log D) time, Combinatorica 21(1), 5 to 12 (2001)
    locator: the main theorem
  - paper: doi:10.1007/BF01456961
    title: Dénes Kőnig, Über Graphen und ihre Anwendung auf Determinantentheorie und Mengenlehre, Mathematische Annalen 77(4), 453 to 465 (1916)
    locator: the theorem that a bipartite graph has an edge coloring with Delta colors
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 5.3, Edge-colouring (Proposition 5.3.1 of Kőnig and Theorem 5.3.2 of Vizing)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A5, problem SS14, Open-shop scheduling (NP-complete without preemption for three or more machines; polynomial with preemption)
  - paper: doi:10.1006/jctb.1995.1011
    title: Fred Galvin, The list chromatic index of a bipartite multigraph, Journal of Combinatorial Theory, Series B 63(1), 153 to 158 (1995)
    locator: the main theorem
---

The edge coloring problem asks for a coloring of the [edges](/edge/) of a graph, with as few colors as possible, such that two edges with a common end get different colors. The least number of colors is the [chromatic index](/chromatic-index/) $\chi'(G)$, which is $\Delta$ or $\Delta + 1$ for a simple graph with maximum degree $\Delta$ by [Vizing's theorem](/vizing-theorem/). A $(\Delta + 1)$-coloring is found in polynomial time, but deciding whether $\Delta$ colors suffice is NP-complete already for cubic graphs (Holyer 1981). Bipartite graphs are easy: they always need exactly $\Delta$ colors.

## In plain words

Each line of a network gets a color. Two lines that meet at a point must get different colors. The goal is to use the fewest colors.

A point where many lines meet needs that many colors, so the busiest point gives a lower limit. One more color than that limit is always enough, and there is a fast method that uses at most one extra color. The hard part is to tell whether the extra color is needed at all.

A common use is a schedule. Lines are meetings between two people, colors are time slots, and nobody can be in two meetings at once.

## Definition

Let $G = (V, E)$ be a finite undirected graph without loops, with $n$ vertices, $m$ edges and maximum degree $\Delta$. A *proper edge coloring* with $k$ colors is a map $c : E \to \{1, \ldots, k\}$ such that $c(e) \ne c(f)$ for any two distinct edges $e, f$ with a common end. Each color class is a matching.

**Optimization version.** Input: $G$. Output: a proper edge coloring with $\chi'(G)$ colors.

**Decision version.** Input: $G$ and an integer $k$. Question: does $G$ have a proper edge coloring with $k$ colors?

Two edges clash exactly when they are adjacent in the [line graph](/line-graph/) $L(G)$, so an edge coloring of $G$ is a vertex [coloring](/graph-coloring/) of $L(G)$, and $\chi'(G) = \chi(L(G))$.

## Variants

- **Class decision.** For a simple graph the only question is whether $\chi'(G) = \Delta$ (class 1) or $\Delta + 1$ (class 2). For cubic graphs this is 3-edge-colorability.
- **Multigraphs.** With parallel edges, $\chi'(G)$ can be as large as $\lfloor 3\Delta / 2 \rfloor$ (Shannon), as for three vertices joined pairwise by $\Delta/2$ parallel edges.
- **Bipartite edge coloring.** Always $\Delta$ colors, by [Kőnig's theorem](/konig-theorem/). This is the core of open shop scheduling.
- **List edge coloring.** Each edge has its own list of allowed colors. The list coloring conjecture says the list version needs no more colors than $\chi'$; Galvin (1995) proved it for bipartite multigraphs.
- **Total coloring.** Color vertices and edges together, so that adjacent or incident elements differ.
- **Distributed and online edge coloring.** Each vertex knows only its neighborhood, or edges arrive one by one. See [distributed edge coloring](/distributed-edge-coloring/).

## Examples

Let $K_4$ have vertices $0, 1, 2, 3$. The coloring $c(01) = c(23) = 1$, $c(02) = c(13) = 2$, $c(03) = c(12) = 3$ is proper: each class is a perfect matching. It uses $\Delta = 3$ colors, so $\chi'(K_4) = 3$.

The 5-cycle with edges $01, 12, 23, 34, 40$ has $\Delta = 2$, but a 2-coloring would have to alternate round the cycle and return after 5 steps to the wrong color. The coloring $1, 2, 1, 2, 3$ is proper, so $\chi'(C_5) = 3$.

| graph | $\Delta$ | $\chi'$ |
|---|---|---|
| $C_n$, $n$ even | 2 | 2 |
| $C_n$, $n$ odd | 2 | 3 |
| $K_n$, $n$ even | $n - 1$ | $n - 1$ |
| $K_n$, $n \ge 3$ odd | $n - 1$ | $n$ |
| $K_{a,b}$ | $\max(a, b)$ | $\max(a, b)$ |
| Petersen graph | 3 | 4 |

**Open shop example.** Jobs $A, B$ and machines $x, y$, where $A$ needs one hour on $x$ and one on $y$, and $B$ needs one hour on $x$. The bipartite graph has edges $Ax$, $Ay$, $Bx$ and $\Delta = 2$ (vertices $A$ and $x$). The coloring $Ax \mapsto 1$, $Bx \mapsto 2$, $Ay \mapsto 2$ is a 2-hour schedule.

## Known algorithms

- **Greedy.** Color the edges in any order with the smallest free color: at most $2\Delta - 1$ colors, $O(m \Delta)$ time.
- **Vizing's algorithm.** The proof of Vizing's theorem with fans and alternating two-colored paths gives a $(\Delta + 1)$-edge coloring of a simple graph. The version of Misra and Gries (1992) runs in $O(nm)$ time. See [Vizing's algorithm](/vizing-algorithm/).
- **Bipartite graphs.** Kőnig's proof colors one edge at a time with one alternating path swap, in $O(nm)$ time. Cole, Ost and Schirra (2001) find a $\Delta$-edge coloring of a bipartite multigraph in $O(m \log \Delta)$ time.
- **Exact.** Color the line graph with an exact vertex coloring algorithm. [Björklund's algorithm](/bjorklund-chromatic-number/) on $L(G)$ takes $O^*(2^m)$ time. For cubic graphs, a backtracking search that gives each edge one of the 3 colors and propagates forced colors at each vertex decides 3-edge-colorability on small inputs.

## Bounds

- **Range.** $\Delta \le \chi'(G) \le \Delta + 1$ for simple graphs (Vizing 1964), so Vizing's algorithm is within an additive 1 of optimal.
- **NP-completeness.** Deciding $\chi'(G) = 3$ for cubic $G$ is NP-complete (Holyer 1981). So computing $\chi'$ exactly is NP-hard, and no polynomial algorithm approximates $\chi'$ within a factor less than $4/3$ unless P = NP, because such an algorithm would separate 3 from 4 on cubic graphs.
- **Polynomial cases.** Bipartite graphs ($\chi' = \Delta$) and graphs with $\Delta \le 2$ (unions of paths and cycles, class 2 exactly when there is an odd cycle).
- **Lower bound by counting.** $\chi'(G) \ge \lceil m / \lfloor n/2 \rfloor \rceil$, since each color class is a matching.

## Reductions

- **To vertex coloring.** $\chi'(G) = \chi(L(G))$, and $L(G)$ has $m$ vertices and $\sum_v \binom{\deg v}{2}$ edges.
- **From 3-SAT.** Holyer's reduction builds a cubic graph from a [3-SAT](/3-sat/) formula with gadgets that copy and negate a value carried by the colors of edge pairs. The graph is 3-edge-colorable exactly when the formula is satisfiable.
- **Bipartite case to matching.** A $\Delta$-regular bipartite multigraph has a perfect matching (Hall's theorem). Removing it leaves a $(\Delta - 1)$-regular one, so $\Delta$ rounds of [bipartite matching](/bipartite-matching/) give a $\Delta$-edge coloring. A bipartite graph that is not regular is first padded to a regular one with the same $\Delta$.

## Applications

- **Open shop scheduling.** With preemption allowed, the optimal length of an open shop schedule equals the largest total load of a job or machine, and a bipartite edge coloring of the unit operations gives the schedule.
- **Round-robin tournaments.** A tournament schedule for $n$ teams in $n - 1$ rounds, $n$ even, is an edge coloring of $K_n$.
- **Communication networks.** In switches, optical networks and data migration, each node takes part in one transfer per time step, so a step is a matching and the number of steps is the number of colors.
- **Wireless link scheduling.** Links that share a radio cannot transmit together, so time slots are edge colors.

## References
