---
tag: P9H73F
kind: problem
slug: graph-coloring
name: Graph coloring
aliases:
- vertex coloring
- proper coloring
area: graphs/coloring-and-cliques
level: intro
summary: Assign labels to vertices so that adjacent vertices get different labels.
prereqs: [graph, undirected-graph, np-complete]
see_also: [chromatic-number, k-coloring, greedy-coloring, dsatur, bjorklund-chromatic-number, edge-coloring, clique-cover, graph-coloring-inapproximability]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A1.1, problem GT4, Graph K-colorability (NP-complete for each fixed K at least 3, also for planar graphs of degree at most 4; polynomial for K = 2)
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, Plenum (1972), 85 to 103
    locator: the list of 21 problems (Chromatic number, reduced from 3-SAT)
  - paper: doi:10.1016/0304-3975(76)90059-1
    title: Michael R. Garey, David S. Johnson and Larry Stockmeyer, Some simplified NP-complete graph problems, Theoretical Computer Science 1(3), 237 to 267 (1976)
    locator: the theorem on planar graph 3-colorability with maximum degree 4
  - paper: doi:10.1137/070683933
    title: Andreas Björklund, Thore Husfeldt and Mikko Koivisto, Set partitioning via inclusion-exclusion, SIAM Journal on Computing 39(2), 546 to 563 (2009)
    locator: the O*(2^n) algorithm for the chromatic number, and the O(2.2461^n) polynomial-space version
  - paper: doi:10.4086/toc.2007.v003a006
    title: David Zuckerman, Linear degree extractors and the inapproximability of Max Clique and Chromatic Number, Theory of Computing 3, 103 to 128 (2007)
    locator: the main theorem (no polynomial-time n^(1-ε)-approximation of the chromatic number unless P = NP)
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Chapter 5, Colouring (Section 5.2, Colouring vertices)
  - paper: doi:10.1006/jcss.1998.1587
    title: Uriel Feige and Joe Kilian, Zero knowledge and the chromatic number, Journal of Computer and System Sciences 57(2), 187 to 199 (1998)
    locator: the main theorem (no n^(1-ε)-approximation unless ZPP = NP)
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Łukasz Kowalik, Daniel Lokshtanov, Dániel Marx, Marcin Pilipczuk, Michał Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 14, Lower bounds based on the Exponential-Time Hypothesis (3-coloring has no 2^(o(n+m)) algorithm)
  - paper: doi:10.1016/0096-0551(81)90048-5
    title: Gregory J. Chaitin, Marc A. Auslander, Ashok K. Chandra, John Cocke, Martin E. Hopkins and Peter W. Markstein, Register allocation via coloring, Computer Languages 6(1), 47 to 57 (1981)
    locator: the whole paper (the interference graph and its coloring)
---

Graph coloring asks for a map from the vertices of an [undirected graph](/undirected-graph/) to a set of colors such that the two ends of each [edge](/edge/) get different colors, with as few colors as possible. The least number of colors is the [chromatic number](/chromatic-number/) $\chi(G)$. Deciding whether $\chi(G) \le k$ is [NP-complete](/np-complete/) for each fixed $k \ge 3$ and takes linear time for $k \le 2$. The best known exact algorithm runs in $O^*(2^n)$ time, and no polynomial algorithm approximates $\chi(G)$ within $n^{1-\varepsilon}$ unless P = NP.

## In plain words

You have a set of things and a list of pairs that clash. Two things that clash must not get the same label. The labels are called colors. You want to use as few colors as you can.

Think of exams at a school. Two exams that share a student cannot be at the same time. Each time slot is a color. The least number of time slots is the answer to the coloring problem.

With two colors the problem is easy, because each choice forces the next one. With three or more colors no fast method is known for all inputs, and most experts think none exists. So programs use fast rules that give a good coloring, not always the best one, or a slow exact search on small inputs.

## Definition

Let $G = (V, E)$ be a finite simple undirected graph with $n = |V|$ and $m = |E|$.

**Proper coloring.** A *$k$-coloring* of $G$ is a map $c : V \to \{1, \ldots, k\}$. It is *proper* if $c(u) \ne c(v)$ for each edge $\{u, v\} \in E$. Each set $c^{-1}(i)$ is a *color class*. A map is a proper coloring exactly when each color class is an [independent set](/independent-set/). So a proper $k$-coloring is the same as a partition of $V$ into at most $k$ independent sets.

**Optimization version.** Input: $G$. Output: a proper coloring with $\chi(G)$ colors, where

$$\chi(G) = \min \{ k \ge 0 : G \text{ has a proper } k\text{-coloring} \}.$$

The empty graph ($n = 0$) has $\chi = 0$. A graph with at least one vertex and no edge has $\chi = 1$.

**Decision version.** Input: $G$ and an integer $k \ge 0$. Question: does $G$ have a proper $k$-coloring? For a fixed $k$ this is the [$k$-coloring problem](/k-coloring/).

A graph with a self-loop has no proper coloring, so the problem is stated for graphs without loops. Parallel edges do not change the answer.

## Variants

- **$k$-coloring for fixed $k$.** For $k = 1$ the answer is yes exactly when $E = \emptyset$. For $k = 2$ it is the [bipartite test](/bipartite-graph-test/), solved in $O(n + m)$ time. For $k \ge 3$ it is NP-complete.
- **Search version.** Output a coloring with $\chi(G)$ colors. Given a decision oracle, add edges between non-adjacent pairs while the answer stays yes; at the end the color classes are the cliques of the complement, so $n^2$ oracle calls give the coloring.
- **Counting.** Count the proper $k$-colorings. The count is the [chromatic polynomial](/chromatic-polynomial/) $P(G, k)$. See [counting graph colorings](/counting-graph-colorings/).
- **Edge coloring.** Color the edges so that edges with a common end differ. See [edge coloring](/edge-coloring/) and the [chromatic index](/chromatic-index/).
- **List coloring.** Each vertex has its own list of allowed colors. See [list coloring](/list-coloring/).
- **Clique cover.** Partition $V$ into the fewest cliques. This is coloring of the [complement graph](/complement-graph/). See [clique cover](/clique-cover/).
- **Special graph classes.** Coloring is polynomial on [chordal graphs](/chordal-graph-coloring/), [perfect graphs](/perfect-graph/), [interval graphs](/interval-partitioning/) and graphs of bounded [treewidth](/treewidth/). Planar graphs need at most 4 colors by the [four color theorem](/four-color-theorem/), but deciding 3-colorability of a planar graph is NP-complete.
- **Online coloring.** The vertices arrive one at a time and each must get its color at once. See [online graph coloring](/online-graph-coloring-problem/).

## Examples

| graph | $n$ | $m$ | $\chi$ | why |
|---|---|---|---|---|
| empty graph | 0 | 0 | 0 | no vertex needs a color |
| $\overline{K_n}$, no edges, $n \ge 1$ | $n$ | 0 | 1 | one class holds all vertices |
| path or even cycle $C_6$ | 6 | 6 | 2 | [bipartite](/bipartite-graph/) |
| odd cycle $C_5$ | 5 | 5 | 3 | a 2-coloring must alternate, and 5 is odd |
| [complete graph](/complete-graph/) $K_4$ | 4 | 6 | 4 | all pairs clash |
| wheel: a hub joined to all of $C_5$ | 6 | 10 | 4 | $C_5$ needs 3, the hub a fourth |
| Petersen graph | 10 | 15 | 3 | no triangle, but it has odd cycles |
| Grötzsch graph, the [Mycielski graph](/mycielski-graph/) of $C_5$ | 11 | 20 | 4 | no triangle, yet 3 colors are not enough |

The last two rows show that the size of the largest [clique](/clique/) does not fix $\chi$: both graphs have [clique number](/clique-number/) 2.

**A small instance.** Take the 5-cycle with vertices $0, 1, 2, 3, 4$ and edges $\{i, i+1 \bmod 5\}$. The map $c = (1, 2, 1, 2, 3)$ is a proper 3-coloring. No proper 2-coloring exists, because going round the cycle the colors would alternate and come back to the start after 5 steps with the wrong color. The 5-cycle has exactly $2^5 - 2 = 30$ proper 3-colorings, and the Petersen graph has 120.

**Non-example.** The map $(1, 2, 1, 2, 1)$ on the 5-cycle is not proper, because the edge $\{4, 0\}$ joins two vertices of color 1.

## Known algorithms

- [Bipartiteness testing](/bipartiteness-testing/): decides $\chi(G) \le 2$ and gives the 2-coloring in $O(n + m)$ time.
- [Greedy coloring](/greedy-coloring/): $O(n + m)$ time, at most $\Delta + 1$ colors, where $\Delta$ is the maximum [degree](/degree/) ([the $\Delta + 1$ bound](/delta-plus-one-bound/)).
- [Smallest-last ordering](/degeneracy-ordering/): greedy in this order uses at most $d + 1$ colors, where $d$ is the [degeneracy](/degeneracy/), in $O(n + m)$ time.
- [DSATUR](/dsatur/), [Welsh-Powell](/welsh-powell-algorithm/) and [recursive largest first](/recursive-largest-first/): heuristics with no guarantee better than $\Delta + 1$, often good in practice.
- [Coloring chordal graphs](/chordal-graph-coloring/): optimal in $O(n + m)$ time on chordal graphs.
- [Lawler's algorithm](/lawler-chromatic-number/): dynamic programming over subsets, $O^*(2.4423^n)$ time.
- [Björklund's algorithm](/bjorklund-chromatic-number/): inclusion-exclusion, $O^*(2^n)$ time and space, or $O(2.2461^n)$ time in polynomial space.
- Planar graphs: a 5-coloring in linear time by the [five color algorithm](/five-color-algorithm/).

Here $O^*(f(n))$ means $O(f(n) \cdot \mathrm{poly}(n))$.

## Bounds

- **Upper bound, exact.** $O^*(2^n)$ time and space (Björklund, Husfeldt and Koivisto 2009). This is the best known bound for the chromatic number of a general graph.
- **NP-hardness.** Karp (1972) proved the decision version NP-complete. It stays NP-complete for each fixed $k \ge 3$, and 3-coloring stays NP-complete on planar graphs with maximum degree 4 (Garey, Johnson and Stockmeyer 1976). So no polynomial algorithm exists unless P = NP.
- **Exponential lower bound.** Under the exponential-time hypothesis, 3-coloring has no $2^{o(n + m)}$-time algorithm (Cygan et al., Chapter 14).
- **Approximation.** For each $\varepsilon > 0$, no polynomial algorithm approximates $\chi(G)$ within a factor $n^{1 - \varepsilon}$ unless P = NP (Zuckerman 2007, after Feige and Kilian 1998 under a weaker assumption). See [inapproximability of graph coloring](/graph-coloring-inapproximability/).
- **Lower bounds on $\chi$.** $\chi(G) \ge \omega(G)$ and $\chi(G) \ge n / \alpha(G)$, where $\omega$ is the clique number and $\alpha$ the [independence number](/independence-number/). Both can be far from $\chi$: the Mycielski graphs have $\omega = 2$ and any $\chi$.

## Reductions

- **From 3-SAT.** Karp's chain of reductions shows that the chromatic number is NP-hard. A direct reduction from [3-SAT](/3-sat/) to 3-coloring uses a triangle of the colors TRUE, FALSE and BASE, one edge for each variable and its negation, and a gadget of six vertices for each clause that can be colored only if one of its literals is TRUE. The graph has $O(n + m)$ vertices for a formula with $n$ variables and $m$ clauses.
- **To SAT.** A $k$-coloring instance becomes a [SAT](/sat/) formula with the variables $x_{v,i}$ ("vertex $v$ has color $i$"): one clause $x_{v,1} \lor \cdots \lor x_{v,k}$ for each vertex, and the clause $\lnot x_{u,i} \lor \lnot x_{v,i}$ for each edge and each color. The formula has $nk$ variables and $n + mk$ clauses. SAT solvers handle many practical instances this way.
- **Clique cover.** $G$ has a partition into $k$ cliques exactly when the complement $\overline G$ has a proper $k$-coloring.
- **Independent sets.** A proper $k$-coloring is a cover of $V$ by $k$ independent sets. This view gives the exponential algorithms by [inclusion-exclusion](/inclusion-exclusion-principle/) and by subset [dynamic programming](/bitmask-dp/).

## Applications

- **Register allocation.** In a compiler, variables that are live at the same time cannot share a register. The interference graph has an edge for each such pair, and a $k$-coloring is an assignment to $k$ registers (Chaitin, Auslander, Chandra, Cocke, Hopkins and Markstein 1981).
- **Scheduling and timetables.** Exams, meetings or jobs that share a resource clash. Colors are time slots.
- **Frequency assignment.** Radio transmitters that are close must use different channels.
- **Puzzles.** A [Sudoku](/sudoku/) is a 9-coloring of a graph with 81 vertices that extends a given partial coloring.
- **Maps.** Countries that share a border get different colors. The graph is planar, so 4 colors are enough.
- **Parallel computing.** The vertices of one color class share no edge, so a computation on them can run in parallel without conflicts. See [distributed vertex coloring](/distributed-vertex-coloring/).

## References
