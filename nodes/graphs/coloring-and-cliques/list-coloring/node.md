---
tag: 68Z1GZ
kind: problem
slug: list-coloring
name: List coloring
aliases:
- choosability
area: graphs/coloring-and-cliques
level: advanced
summary: Each vertex has its own list of allowed colors; find a proper coloring that picks each color from its list.
prereqs: [graph-coloring, k-coloring, chromatic-number]
see_also: [edge-coloring, planar-graph-coloring, five-color-theorem, degeneracy-ordering, 2-sat, brooks-theorem, kempe-chain, vizing-theorem]
sources:
  - paper: "P. Erdős, A. L. Rubin and H. Taylor, Choosability in graphs, Proceedings of the West Coast Conference on Combinatorics, Graph Theory and Computing, Congressus Numerantium 26, 125 to 157 (1979)"
    locator: the definition of choosability, the bound for K(m,m), the characterization of 2-choosable graphs, and the complexity of deciding choosability
  - paper: "V. G. Vizing, Coloring the vertices of a graph in prescribed colors (in Russian), Metody Diskretnogo Analiza 29, 3 to 10 (1976)"
    locator: the definition of list coloring and the list form of Brooks' theorem
  - paper: doi:10.1006/jctb.1994.1062
    title: Carsten Thomassen, Every planar graph is 5-choosable, Journal of Combinatorial Theory, Series B 62(1), 180 to 181 (1994)
    locator: the whole paper
  - paper: doi:10.1016/0012-365X(93)90579-I
    title: Margit Voigt, List colourings of planar graphs, Discrete Mathematics 120(1 to 3), 215 to 219 (1993)
    locator: the planar graph that is not 4-choosable
  - paper: doi:10.1006/jctb.1995.1011
    title: Fred Galvin, The list chromatic index of a bipartite multigraph, Journal of Combinatorial Theory, Series B 63(1), 153 to 158 (1995)
    locator: the main theorem (the list chromatic index equals the chromatic index for bipartite multigraphs)
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 5.4, List colouring
---

List coloring is [graph coloring](/graph-coloring/) in which each vertex $v$ comes with its own list $L(v)$ of allowed colors, and the task is a proper coloring that gives each vertex a color from its list. It contains [k-coloring](/k-coloring/) as the case where all lists are $\{1, \ldots, k\}$, so it is NP-complete, but it is solvable in linear time when all lists have at most 2 colors, by [2-SAT](/2-sat/). The related graph invariant is the choice number $\mathrm{ch}(G)$, the least $k$ such that every assignment of lists of size $k$ admits a coloring. It can be much larger than the [chromatic number](/chromatic-number/): bipartite graphs have unbounded choice number.

## In plain words

Each guest at a wedding names a few tables where they are willing to sit, and two guests who quarrel must not share a table. Can everyone be seated at a table they named?

If every guest names the same tables, this is the usual coloring question. With personal lists it gets harder, because a table that is easy to use for one guest may be forbidden for the next. A surprising fact is that two-sided groups, which need only two tables when everyone accepts every table, can need many choices per guest when the lists differ.

## Definition

**Input.** A finite simple graph $G = (V, E)$ and a list $L(v)$ of colors for each vertex $v$.

**Question.** Is there an $L$-coloring, a map $c$ with

$$c(v) \in L(v) \text{ for all } v \in V, \qquad c(u) \ne c(v) \text{ for all } uv \in E?$$

**Choosability.** $G$ is **$k$-choosable** if it has an $L$-coloring for every list assignment with $|L(v)| \ge k$ for all $v$. The **choice number** (or list chromatic number) $\mathrm{ch}(G)$ is the least such $k$. Taking all lists equal shows $\chi(G) \le \mathrm{ch}(G)$.

## Variants

- **Fixed list size.** All lists have size at most $k$. For $k = 2$ it is in polynomial time; for $k = 3$ it is NP-complete, since 3-coloring is the case with all lists $\{1, 2, 3\}$.
- **Precoloring extension.** Some vertices are already colored and the rest may use any of $k$ colors. This is list coloring where a precolored vertex has a list of one color and every other vertex loses the colors of its precolored neighbors.
- **Choosability.** Given $G$ and $k$, decide whether $G$ is $k$-choosable. The question has a "for all lists, there is a coloring" form, and Erdős, Rubin and Taylor showed it is $\Pi_2^p$-complete for $k = 3$, so it is harder than NP under standard assumptions.
- **List edge coloring.** Lists on the edges; the list chromatic index $\mathrm{ch}'(G)$. The list coloring conjecture says $\mathrm{ch}'(G) = \chi'(G)$ for every graph; see [edge coloring](/edge-coloring/).
- **Correspondence (DP) coloring.** A generalization in which each edge may match the colors of its ends by any bijection, not only by equality.

## Examples

- **$K_{3,3}$ is not 2-choosable.** Give the lists $\{1, 2\}$, $\{1, 3\}$, $\{2, 3\}$ to the three vertices on each side. One side uses at least two colors from the three, and then some vertex of the other side has both of those colors in its list, so it has no color left. So $\mathrm{ch}(K_{3,3}) = 3$, while $\chi(K_{3,3}) = 2$.
- **$K_{2,4}$ is not 2-choosable.** Give the lists $\{1, 2\}$ and $\{3, 4\}$ to the two vertices on the small side and the lists $\{1, 3\}$, $\{1, 4\}$, $\{2, 3\}$, $\{2, 4\}$ to the four on the other side. Each choice of colors for the small side is a full list of one vertex on the other side.
- **2-choosable graphs.** Even cycles and $K_{2,3}$ are 2-choosable; odd cycles are not even 2-colorable. Erdős, Rubin and Taylor proved that a connected graph is 2-choosable if and only if, after repeatedly deleting vertices of degree 1, what remains is a single vertex, an even cycle, or the theta graph $\theta_{2,2,2m}$ (two vertices joined by three paths of lengths 2, 2 and $2m$).
- **Large bipartite graphs.** $K_{m,m}$ with $m = \binom{2k - 1}{k}$ is not $k$-choosable: give the two sides all $k$-subsets of $\{1, \ldots, 2k - 1\}$. In general $\mathrm{ch}(K_{n,n}) = (1 + o(1)) \log_2 n$.
- **Planar graphs.** Every planar graph is 5-choosable (Thomassen 1994), and some planar graphs are not 4-choosable (Voigt 1993). So the list version of the [four color theorem](/four-color-theorem/) fails, while the list version of the [five color theorem](/five-color-theorem/) holds.

All of the small cases above agree with an exhaustive search over the colorings.

## Known algorithms

- **Lists of size at most 2.** Make a Boolean variable for each pair (vertex, color in its list). The constraints "the vertex takes one of its two colors" and "two adjacent vertices do not both take color $a$" are 2-clauses, so [2-SAT](/2-sat/) solves the instance in $O(n + m)$ time. A vertex with an empty list makes the instance infeasible, and one with a single color is a unit clause.
- **Greedy along a degeneracy order.** If $G$ is $d$-degenerate, color the vertices in reverse [degeneracy order](/degeneracy-ordering/): each vertex has at most $d$ colored neighbors, so a list of size $d + 1$ always has a free color. Hence $\mathrm{ch}(G) \le d + 1 \le \Delta + 1$.
- **Planar graphs.** Thomassen's proof is a short induction that colors a near-triangulation with lists of size 3 on the outer face and 5 inside; it turns into a linear-time algorithm for 5-list-coloring planar graphs.
- **Trees and bounded treewidth.** Dynamic programming over a [tree decomposition](/tree-decomposition/) of width $t$, with states the colorings of a bag, runs in time polynomial in $n$ for fixed $t$ and bounded list sizes.
- **Exact search.** Backtracking over the colors in the lists, choosing the vertex with the fewest remaining colors first as in [DSatur](/dsatur/), is the common exact method. The trivial bound is $\prod_v |L(v)|$ colorings.

## Bounds

- $\chi(G) \le \mathrm{ch}(G) \le \mathrm{degeneracy}(G) + 1$.
- **Brooks for lists (Vizing 1976; Erdős, Rubin and Taylor 1979).** A connected graph that is neither complete nor an odd cycle is $\Delta$-choosable, like [Brooks' theorem](/brooks-theorem/).
- **Galvin's theorem (1995).** For every bipartite multigraph, $\mathrm{ch}'(G) = \chi'(G) = \Delta$. It settled the Dinitz problem: an $n \times n$ array with a list of $n$ symbols in each cell has a Latin-square choice of symbols.
- **Hardness.** The search problem is NP-hard already for lists of size 3 on planar graphs, as 3-coloring is NP-complete there, and the choosability question is $\Pi_2^p$-complete.

## Reductions

- **From $k$-coloring.** Give every vertex the list $\{1, \ldots, k\}$.
- **To 2-SAT** for lists of size at most 2, as above.
- **To $k$-coloring.** Let $C = \bigcup_v L(v)$ with $|C| = k$. Add a clique $K$ on $k$ new vertices, one for each color, and join $v$ to the clique vertex of every color not in $L(v)$. Then $G$ has an $L$-coloring if and only if the new graph is $k$-colorable, since the clique vertices get $k$ distinct colors that can be named after the colors of $C$.

## Applications

- **Frequency assignment.** Each transmitter may use only the channels licensed at its site, and interfering transmitters need different channels.
- **Scheduling.** Each exam may take place only in the time slots in which its examiner is free.
- **Register allocation.** Some variables must sit in particular registers because of calling conventions, which restricts their lists.
- **Puzzles.** A partly filled Sudoku is a precoloring extension, and so a list coloring of its 81-vertex graph.
- **Proof technique.** Stronger induction hypotheses with lists, as in Thomassen's proof, give short proofs of ordinary coloring results.

## References
