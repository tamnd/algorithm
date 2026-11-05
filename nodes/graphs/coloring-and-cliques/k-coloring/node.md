---
tag: CPNEV0
kind: problem
slug: k-coloring
name: k-coloring problem
aliases:
- 3-coloring
- k-colorability
area: graphs/coloring-and-cliques
level: core
summary: Decide whether a graph has a proper coloring with k colors; NP-complete for k at least 3.
prereqs: [graph-coloring, chromatic-number, np-complete]
see_also: [three-coloring, bipartite-graph-test, lawler-chromatic-number, bjorklund-chromatic-number, four-color-theorem, brooks-theorem, graph-coloring-inapproximability, list-coloring]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A1.1, problem GT4, Graph K-colorability
  - paper: doi:10.1016/0304-3975(76)90059-1
    title: Michael R. Garey, David S. Johnson and Larry Stockmeyer, Some simplified NP-complete graph problems, Theoretical Computer Science 1(3), 237 to 267 (1976)
    locator: the theorem on 3-colorability of planar graphs with maximum degree 4
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design, Addison-Wesley, 2006
    locator: Section 8.7, Graph coloring (3-coloring is NP-complete, by a reduction from 3-SAT)
  - paper: doi:10.1016/0020-0190(76)90065-X
    title: Eugene L. Lawler, A note on the complexity of the chromatic number problem, Information Processing Letters 5(3), 66 to 67 (1976)
    locator: the whole paper (3-colorability in O(1.4423^n) time through maximal independent sets)
  - paper: doi:10.1016/j.jalgor.2004.06.008
    title: Richard Beigel and David Eppstein, 3-coloring in time O(1.3289^n), Journal of Algorithms 54(2), 168 to 204 (2005)
    locator: the main theorem
  - paper: doi:10.1137/070683933
    title: Andreas Björklund, Thore Husfeldt and Mikko Koivisto, Set partitioning via inclusion-exclusion, SIAM Journal on Computing 39(2), 546 to 563 (2009)
    locator: the O*(2^n) algorithm for k-colorability and the chromatic number
  - paper: doi:10.1145/2157.2158
    title: Avi Wigderson, Improving the performance guarantee for approximate graph coloring, Journal of the ACM 30(4), 729 to 735 (1983)
    locator: the O(√n)-coloring of a 3-colorable graph
  - paper: doi:10.1137/S0895480100376794
    title: Venkatesan Guruswami and Sanjeev Khanna, On the hardness of 4-coloring a 3-colorable graph, SIAM Journal on Discrete Mathematics 18(1), 30 to 40 (2004)
    locator: the main theorem
---

The $k$-coloring problem asks whether the vertices of a graph can be colored with at most $k$ colors so that the two ends of each edge get different colors. For $k = 1$ and $k = 2$ it takes linear time; for each fixed $k \ge 3$ it is NP-complete, even for planar graphs of maximum degree 4 when $k = 3$. It is the decision version of [graph coloring](/graph-coloring/): $G$ is $k$-colorable exactly when its [chromatic number](/chromatic-number/) is at most $k$. The fastest known exact algorithm for every $k$ runs in $O^*(2^n)$ time, and for $k = 3$ in $O(1.3289^n)$ time.

## In plain words

You have a map of countries and a box of a few crayons. Countries that share a border must get different crayons. Can you color the whole map with the crayons in the box?

With one crayon, this works only if no two countries touch. With two crayons, there is a fast test: color one country, then each neighbor must take the other crayon, and so on, and you see at once if this fails. With three crayons the choices no longer force each other, and no fast method is known. A proposed coloring is still easy to check: look at each border once.

## Definition

**Input.** A finite simple undirected graph $G = (V, E)$, and a positive integer $k$. In the version "$k$-coloring" for a fixed $k$, only $G$ is the input.

**Question.** Is there a map $c : V \to \{1, \ldots, k\}$ such that

$$\forall \{u, v\} \in E: \quad c(u) \ne c(v)?$$

Such a map is a proper $k$-coloring, and its color classes $c^{-1}(1), \ldots, c^{-1}(k)$ are [independent sets](/independent-set/). So $G$ is $k$-colorable if and only if $V$ is the union of $k$ independent sets, and if and only if $\chi(G) \le k$.

## Variants

- **Search.** Find a $k$-coloring when one exists. By self-reducibility, a decision algorithm finds one with $O(n^2)$ calls. For each pair of non-adjacent vertices, add the edge between them, and keep it when the graph stays $k$-colorable. At the end, each further edge would destroy all $k$-colorings, so the graph is complete multipartite with at most $k$ parts, and the parts are the color classes.
- **Optimization.** Find $\chi(G)$, the least $k$; see [graph coloring](/graph-coloring/).
- **Counting.** Count the $k$-colorings, which is the [chromatic polynomial](/chromatic-polynomial/) at $k$; see [counting graph colorings](/counting-graph-colorings/).
- **Lists.** Each vertex has its own list of allowed colors; see [list coloring](/list-coloring/).
- **Promise problems.** Given a graph that is promised to be 3-colorable, find a coloring with few colors. This is the approximate version.
- **Edges.** Color edges so that edges with a common end differ; see [edge coloring](/edge-coloring/). Deciding whether $\chi' = 3$ for a cubic graph is NP-complete (Holyer 1981).

## Examples

- **$k = 2$.** A graph is 2-colorable if and only if it is [bipartite](/bipartite-graph/), that is, it has no odd cycle. The cycle $C_6$ is 2-colorable; $C_5$ is not.
- **Odd cycles and wheels.** $C_5$ is 3-colorable. The wheel $W_5$, a hub joined to the 5 vertices of $C_5$, is not: the rim needs 3 colors and the hub a fourth, so $\chi(W_5) = 4$.
- **Complete graphs.** $K_n$ is $k$-colorable if and only if $k \ge n$. So $K_4$ is the smallest graph that is not 3-colorable.
- **Petersen graph.** It is 3-colorable and not 2-colorable, since its outer 5-cycle is odd.
- **No triangle is not enough.** The Grötzsch graph, the [Mycielski graph](/mycielski-graph/) on 11 vertices, has no triangle and is not 3-colorable.
- **Planar graphs.** Every planar graph is 4-colorable by the [four color theorem](/four-color-theorem/), so 4-coloring is trivial on planar graphs as a decision problem, while planar 3-coloring is NP-complete.

## Known algorithms

- **$k = 1$.** $G$ is 1-colorable if and only if $E = \emptyset$.
- **$k = 2$.** [Breadth-first search](/breadth-first-search/) colors each component by the parity of the distance from a start vertex, in $O(n + m)$ time; see [bipartite graph test](/bipartite-graph-test/).
- **$k = 3$ by maximal independent sets (Lawler 1976).** If $G$ is 3-colorable, one color class $I_1$ extends to a [maximal independent set](/maximal-independent-set/) $I \supseteq I_1$, and $G - I$ is a subgraph of the union of the other two classes, so it is bipartite. Conversely, if $G - I$ is bipartite for an independent set $I$, then $G$ is 3-colorable. So it suffices to list all maximal independent sets, at most $3^{n/3}$ of them by the Moon-Moser bound, and test each $G - I$ in linear time. The total is $O^*(3^{n/3}) = O(1.4423^n)$.
- **$k = 3$, Beigel and Eppstein (2005).** A reduction to a constraint satisfaction problem with domains of size at most 3 and a careful branching give $O(1.3289^n)$ time.
- **Any $k$.** [Björklund, Husfeldt and Koivisto](/bjorklund-chromatic-number/) count the covers of $V$ by $k$ independent sets with inclusion-exclusion, in $O^*(2^n)$ time and space. [Lawler's dynamic program](/lawler-chromatic-number/) runs in $O(2.4423^n)$ time and finds $\chi$ itself.
- **Bounded treewidth.** A dynamic program over a [tree decomposition](/tree-decomposition/) of width $t$ runs in $O(k^{t+1} \cdot n)$ time, up to polynomial factors in $t$.
- **Maximum degree 3.** By [Brooks' theorem](/brooks-theorem/), a graph with $\Delta \le 3$ is 3-colorable if and only if no component is $K_4$, and a 3-coloring can be found in linear time.

## Bounds

- **NP-completeness.** 3-colorability is NP-complete (Karp's *Chromatic number* in 1972, and Stockmeyer for $k = 3$), and it stays NP-complete for planar graphs of maximum degree 4 (Garey, Johnson and Stockmeyer 1976). For each fixed $k \ge 3$, $k$-colorability is NP-complete: add a vertex adjacent to all others to go from $k$ to $k + 1$.
- **Exponential time.** Under the exponential time hypothesis, 3-coloring has no $2^{o(n)}$ algorithm, since the reduction below produces $O(N + q)$ vertices from a formula with $N$ variables and $q$ clauses.
- **Approximate coloring.** Given a 3-colorable graph, Wigderson's algorithm uses $O(\sqrt n)$ colors: while some vertex $v$ has degree at least $\sqrt n$, its neighborhood is bipartite (it lies in two color classes), so color it with 2 new colors and remove it; then color the rest greedily with at most $\sqrt n$ colors. Semidefinite programming improves this to $n^c$ colors for a constant $c$ below $0.2$. On the hardness side, it is NP-hard to color a 3-colorable graph with 4 colors, so the gap between upper and lower bounds is very large. See [graph coloring inapproximability](/graph-coloring-inapproximability/).

## Reductions

**From 3-SAT to 3-coloring.** The reduction of [three-coloring](/three-coloring/) in Kleinberg and Tardos, Section 8.7, uses three kinds of gadgets.

1. A *palette* triangle with vertices $T$, $F$ and $B$. In each 3-coloring they get three distinct colors, which we call true, false and base.
2. For each variable $x$, a triangle on $x$, $\neg x$ and $B$. So $\{c(x), c(\neg x)\} = \{T, F\}$: each coloring encodes an assignment.
3. For each clause $(\ell_1 \lor \ell_2 \lor \ell_3)$, two copies of an OR gadget and a check. An OR gadget with inputs $a, b$ is a triangle $x, y, o$ with the edges $ax$ and $by$. If $c(a) = c(b) = F$, then $x$ and $y$ use $T$ and $B$, so $c(o) = F$. If $c(a) = T$ or $c(b) = T$, there is a coloring with $c(o) = T$. Chain $o_1 = \mathrm{OR}(\ell_1, \ell_2)$ and $o_2 = \mathrm{OR}(o_1, \ell_3)$, and join $o_2$ to $F$ and $B$, which forces $c(o_2) = T$.

A clause with three false literals forces $c(o_1) = F$ and then $c(o_2) = F$, a contradiction. A clause with a true literal lets $o_1$ take $T$ when $\ell_1$ or $\ell_2$ is true and $F$ otherwise, and then $o_2$ takes $T$. So the formula is satisfiable if and only if the graph is 3-colorable. The graph has $3 + 2N + 6q$ vertices, a linear size. For one clause, all 7 satisfying patterns of the literals extend to a 3-coloring and the pattern with three false literals does not.

**Other reductions.** $G$ is $k$-colorable if and only if $G + K_1$ (a new vertex joined to all) is $(k+1)$-colorable. $G$ is $k$-colorable if and only if the Cartesian product $G \,\square\, K_k$ has an independent set of size $n$, which reduces coloring to [maximum independent set](/maximum-independent-set/).

## Applications

- **Register allocation.** Variables that are live at the same time conflict; $k$ registers mean a $k$-coloring of the interference graph.
- **Scheduling and timetables.** Exams with a common student cannot share a time slot; $k$ slots mean a $k$-coloring.
- **Frequency assignment.** Nearby transmitters need different channels.
- **Puzzles.** A Sudoku is a 9-coloring of a fixed graph with 81 vertices that extends a given partial coloring.

## References
