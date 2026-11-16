---
tag: TQKHMF
kind: problem
slug: minor-testing
name: Minor testing
aliases:
- H-minor testing
- graph minor testing
area: complexity/parameterized-complexity
level: advanced
summary: "Decide whether H is a minor of G, with parameter |V(H)|. NP-complete when H is part of the input. FPT: f(H) n^3 by Robertson and Seymour, f(H) n^2, and now almost linear time."
prereqs: [graph-minor, fixed-parameter-tractable, graph-minor-theorem]
see_also: [courcelle-theorem, grid-minor-theorem, irrelevant-vertex-technique, parameterized-disjoint-paths, subgraph-isomorphism, kuratowski-theorem, planarity-testing, meta-theorems]
sources:
  - paper: doi:10.1006/jctb.1995.1006
    title: "Neil Robertson and Paul D. Seymour, Graph minors. XIII. The disjoint paths problem, Journal of Combinatorial Theory, Series B 63(1), 65-110 (1995)"
    locator: the main algorithm, minor testing and disjoint paths in O(n^3) time for fixed H or fixed k
  - paper: doi:10.1016/j.jctb.2011.07.004
    title: "Ken-ichi Kawarabayashi, Yusuke Kobayashi and Bruce Reed, The disjoint paths problem in quadratic time, Journal of Combinatorial Theory, Series B 102(2), 424-435 (2012)"
    locator: the main theorem, O(n^2) time for fixed k, and the same bound for minor testing
  - paper: doi:10.1109/FOCS61266.2024.00014
    title: "Tuukka Korhonen, Michal Pilipczuk and Giannos Stamoulis, Minor containment and disjoint paths in almost-linear time, FOCS 2024, 53-61"
    locator: the main theorem, minor containment for fixed H in almost-linear time (arXiv 2404.03958)
  - paper: doi:10.1145/1993636.1993700
    title: "Martin Grohe, Ken-ichi Kawarabayashi, Daniel Marx and Paul Wollan, Finding topological subgraphs is fixed-parameter tractable, STOC 2011, 479-488"
    locator: the main theorem, topological minor testing in O(n^3) time for fixed H
  - book: isbn:9783319212746
    title: "Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015"
    locator: "Section 6.3, Graph minors and the Robertson-Seymour theorem (minor testing in f(H) n^3, membership in minor-closed classes, non-constructivity and the Fellows-Langston result)"
---

Minor testing asks whether a graph $H$ is a [minor](/graph-minor/) of a graph $G$. The parameter is the number of vertices $h = |V(H)|$ of the pattern. With $H$ part of the input the problem is NP-complete, but for the parameter $h$ it is [fixed-parameter tractable](/fixed-parameter-tractable/): Robertson and Seymour solved it in time $f(H) \cdot n^3$ in Graph Minors XIII. Together with the [graph minor theorem](/graph-minor-theorem/), this gives a polynomial membership test for every minor-closed graph class, but the test is not constructive.

## In plain words

You have a big graph and a small pattern graph. You may delete vertices and edges of the big graph, and you may merge two adjacent vertices into one. The question is whether some sequence of these steps turns the big graph into the pattern. When the pattern is part of the input, the question is as hard as finding a Hamiltonian cycle. When the pattern is small, the question has an algorithm whose time is a fixed polynomial in the size of the big graph, with a huge factor that depends only on the pattern. This is a main difference from subgraph search, where small patterns such as cliques are believed to stay hard.

## Definition

A graph $H$ is a minor of $G$ if there are disjoint vertex sets $B_v \subseteq V(G)$, one for each $v \in V(H)$, such that each $G[B_v]$ is connected and, for each edge $uv$ of $H$, some edge of $G$ joins $B_u$ and $B_v$. The sets $B_v$ are the *branch sets*, and together they form a *minor model* of $H$ in $G$.

- Instance: graphs $G$ and $H$, given as adjacency lists. Let $n = |V(G)|$.
- Parameter: $h = |V(H)|$.
- Question: Is $H$ a minor of $G$?

## Variants

- **Fixed $H$.** For each fixed $H$, the problem "is $H$ a minor of $G$?" is a separate problem with input $G$ only. Each of these problems is in P. The parameterized form asks for one algorithm with time $f(H) \cdot n^c$ for all $H$.
- **Topological minor testing.** $H$ is a topological minor of $G$ if $G$ has a subgraph that is a subdivision of $H$. Every topological minor is a minor, but not the reverse: a graph with maximum degree 3 can have $K_{1,4}$ as a minor but not as a topological minor. When $H$ has maximum degree at most 3, the two notions agree. Grohe, Kawarabayashi, Marx and Wollan (2011) proved that topological minor testing is also FPT in $|V(H)|$, in time $f(H) \cdot n^3$.
- **Minor-closed class membership.** For a class $\mathcal{C}$ closed under minors, decide whether $G \in \mathcal{C}$. By the graph minor theorem, $\mathcal{C}$ is defined by a finite set of excluded minors, so membership is a finite number of minor tests.
- **Rooted minors.** Some vertices of $H$ must map to given vertices of $G$. The [disjoint paths problem](/parameterized-disjoint-paths/) is a rooted minor problem: $k$ disjoint edges must be realized between given roots.
- **Bounded treewidth.** When $G$ has [treewidth](/treewidth/) at most $t$, "$H$ is a minor of $G$" is an MSO2 property, and [Courcelle's theorem](/courcelle-theorem/) decides it in time $f(H, t) \cdot n$.

## Examples

All answers below come from an exhaustive search over branch-set labelings of $G$, followed by a check that the quotient graph contains $H$.

| $G$ | $H$ | $H$ a minor of $G$? | reason |
|---|---|---|---|
| 3 by 3 grid | $K_4$ | yes | contract the border cycle into 3 paths around the center |
| 3 by 3 grid | $K_5$ | no | the grid is planar, and planar graphs have no $K_5$ minor ([Wagner](/wagner-theorem/)) |
| Petersen graph | $K_5$ | yes | contract the 5 spokes |
| Petersen graph | $K_{3,3}$ | yes | the Petersen graph is not planar |
| Petersen graph | $C_9$ | yes | it has a cycle of length 9 |
| Petersen graph | $C_{10}$ | no | a $C_{10}$ minor of a 10-vertex graph is a Hamiltonian cycle, and the Petersen graph has none |
| Petersen graph | $K_6$ | no | |

The $C_{10}$ row shows the reduction from Hamiltonian cycle in the Reductions section below.

## Known algorithms

- Robertson and Seymour (Graph Minors XIII, 1995) decide whether $H$ is a minor of $G$ in time $f(H) \cdot n^3$ on a RAM, by the [irrelevant vertex technique](/irrelevant-vertex-technique/).
- Kawarabayashi, Kobayashi and Reed (2012) lower the time to $f(H) \cdot n^2$ on a RAM.
- Korhonen, Pilipczuk and Stamoulis (FOCS 2024) give an algorithm with time almost linear in the size of $G$ for each fixed $H$.
- On graphs of treewidth $t$, [Courcelle's theorem](/courcelle-theorem/) gives time $f(H, t) \cdot n$, with a tree decomposition from [treewidth computation](/treewidth-computation/).
- For planarity, that is, testing for $K_5$ and $K_{3,3}$ minors at once, [planarity testing](/planarity-testing/) takes linear time with small constants.
- When $H$ is part of the input, trying every labeling of the vertices of $G$ with branch-set labels takes time $(h + 1)^n \cdot n^{O(1)}$.

The function $f$ in the general algorithms is enormous and is not written out in the sources. These algorithms show that the problem is FPT; they are not used in practice.

## Bounds

- **NP-complete when $H$ is part of the input**, under polynomial-time many-one reductions, by the reduction from Hamiltonian cycle below. Membership in NP: the certificate is the minor model, checked in polynomial time.
- **FPT in $h$**, by the algorithms above. Compare [subgraph isomorphism](/subgraph-isomorphism/) with the same parameter: its special case $H = K_h$ is [p-Clique](/parameterized-clique/), so it is [W[1]-hard](/w-hardness/) and not FPT unless $\mathsf{FPT} = \mathsf{W}[1]$.
- **Non-constructive membership tests.** For a minor-closed class $\mathcal{C}$, the graph minor theorem says that a finite obstruction set exists, and then the test runs in time $c_{\mathcal{C}} \cdot n^3$ (or faster with the newer algorithms). But the proof does not say how to find the obstruction set. Fellows and Langston showed that the obstruction set cannot be computed from a membership oracle alone (Cygan et al., Section 6.3). Obstruction sets can also be large: for graphs embeddable in the torus, more than 16,000 excluded minors are known (Cygan et al., Section 6.3).

## Reductions

- **Hamiltonian cycle to minor testing.** Map a graph $G$ with $n$ vertices to the pair $(G, C_n)$. A minor of $G$ with $n$ vertices uses every vertex as a one-vertex branch set, so it is a subgraph. So $C_n$ is a minor of $G$ if and only if $G$ has a [Hamiltonian cycle](/hamiltonian-cycle-problem/). This is a polynomial-time many-one reduction of linear cost, and it shows NP-hardness. The parameter $h = n$ is not bounded, so this does not contradict FPT.
- **Minor-closed classes to minor testing.** Membership in a minor-closed class reduces to a finite number of minor tests, one for each graph in the obstruction set.
- **Minor testing and disjoint paths.** Graph Minors XIII solves both problems by one method. A minor model of $H$ can be guessed as a set of roots, after which the edges of $H$ become a [disjoint paths](/parameterized-disjoint-paths/) instance. In the other direction, disjoint paths is a rooted minor problem.

## Applications

- **Non-constructive FPT results.** For each fixed $k$, the graphs with a [vertex cover](/vertex-cover/) of size at most $k$, or with a [feedback vertex set](/parameterized-feedback-vertex-set/) of size at most $k$, form a minor-closed class. So both problems are FPT through minor testing, but the argument does not give the algorithm. Fellows and Langston used this method in the 1980s. Direct algorithms are now known for both problems.
- **Graph classes.** Graphs of genus at most $g$ ([graph genus](/graph-genus/)), linklessly embeddable graphs, and graphs of treewidth at most $t$ are minor-closed, so each has a polynomial membership test.
- **Win/win algorithms.** Minor tests are a step in algorithms that use the [grid minor theorem](/grid-minor-theorem/): test for a large grid minor, and if there is none, use the small treewidth.

## References
