---
tag: BWFPKH
kind: definition
slug: perfect-graph
name: Perfect graph
aliases:
- perfect graphs
area: graphs/coloring-and-cliques
level: advanced
summary: A graph in which the chromatic number equals the clique number in every induced subgraph.
prereqs: [chromatic-number, clique-number, induced-subgraph]
see_also: [perfect-graph-theorem, strong-perfect-graph-theorem, lovasz-theta-function, chordal-graph, perfect-elimination-ordering, konig-theorem, mycielski-graph, independence-number]
sources:
  - paper: "C. Berge, Färbung von Graphen, deren sämtliche bzw. deren ungerade Kreise starr sind, Wissenschaftliche Zeitschrift der Martin-Luther-Universität Halle-Wittenberg, Mathematisch-Naturwissenschaftliche Reihe 10, 114 (1961)"
    locator: the definition of perfect graphs and the two perfect graph conjectures
  - paper: doi:10.1016/0012-365X(72)90006-4
    title: L. Lovász, Normal hypergraphs and the perfect graph conjecture, Discrete Mathematics 2(3), 253 to 267 (1972)
    locator: the proof that the complement of a perfect graph is perfect
  - paper: doi:10.4007/annals.2006.164.51
    title: Maria Chudnovsky, Neil Robertson, Paul Seymour and Robin Thomas, The strong perfect graph theorem, Annals of Mathematics 164(1), 51 to 229 (2006)
    locator: the main theorem
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 5.5, Perfect graphs
  - book: isbn:9780444515308
    title: Martin Charles Golumbic, Algorithmic Graph Theory and Perfect Graphs, second edition, Elsevier, 2004
    locator: Chapter 3, Perfect graphs
---

A graph is perfect when, in it and in each of its induced subgraphs, the [chromatic number](/chromatic-number/) equals the [clique number](/clique-number/). Bipartite graphs, chordal graphs, interval graphs and comparability graphs are perfect, while odd cycles of length at least 5 are not. By the [strong perfect graph theorem](/strong-perfect-graph-theorem/), a graph is perfect exactly when it has no odd hole and no odd antihole, and on perfect graphs coloring, maximum clique and maximum independent set can all be solved in polynomial time.

## Definition

Let $G$ be a finite simple graph. Write $\omega(H)$ for the clique number and $\chi(H)$ for the chromatic number of a graph $H$, and $G[S]$ for the [induced subgraph](/induced-subgraph/) on $S \subseteq V(G)$.

**Definition (Berge 1961).** $G$ is **perfect** if

$$\chi(G[S]) = \omega(G[S]) \quad \text{for every } S \subseteq V(G).$$

Since $\chi(H) \ge \omega(H)$ holds for every graph (the vertices of a clique need distinct colors), perfection says that the clique lower bound is always tight, not just for $G$ but for every induced subgraph.

The condition must hold for all induced subgraphs. The graph made of a 5-cycle and a disjoint triangle has $\chi = \omega = 3$, but its induced 5-cycle has $\chi = 3 > 2 = \omega$, so it is not perfect.

An **odd hole** is an induced cycle $C_{2k+1}$ with $k \ge 2$, and an **odd antihole** is an induced subgraph isomorphic to the complement $\overline{C_{2k+1}}$ with $k \ge 2$.

## Examples and non-examples

| graph | $\omega$ | $\chi$ | perfect? | reason |
|---|---|---|---|---|
| complete graph $K_n$ | $n$ | $n$ | yes | every induced subgraph is complete |
| bipartite graph with an edge | 2 | 2 | yes | induced subgraphs stay bipartite |
| complement of a bipartite graph | any | $= \omega$ | yes | [König's theorem](/konig-theorem/) on covers and matchings |
| line graph of a bipartite graph | any | $= \omega$ | yes | König's edge coloring theorem, $\chi' = \Delta$ |
| [chordal graph](/chordal-graph/) | any | $= \omega$ | yes | greedy coloring along a [perfect elimination ordering](/perfect-elimination-ordering/) |
| interval graph | any | $= \omega$ | yes | it is chordal |
| comparability graph of a poset | any | $= \omega$ | yes | Mirsky's theorem: a longest chain equals the least number of antichains that cover |
| $C_5$, $C_7$, any odd hole | 2 | 3 | no | an odd cycle needs 3 colors |
| $\overline{C_7}$ | 3 | 4 | no | $\alpha(\overline{C_7}) = 2$, so $\chi \ge \lceil 7/2 \rceil = 4$ |
| Petersen graph | 2 | 3 | no | its outer 5-cycle is an odd hole |
| [Mycielski graphs](/mycielski-graph/) $M_k$, $k \ge 3$ | 2 | $k$ | no | they contain $C_5$ |

Note that $\overline{C_5} \cong C_5$, so the smallest odd antihole that is not an odd hole is $\overline{C_7}$. Cographs and split graphs are further perfect classes.

## Related definitions

- **Perfect graph theorem (Lovász 1972).** $G$ is perfect if and only if its [complement](/complement-graph/) is perfect; equivalently, $\alpha(G[S])$ equals the least number of cliques that cover $S$, for every $S$. Lovász also proved that $G$ is perfect if and only if $\omega(G[S])\, \alpha(G[S]) \ge |S|$ for every $S$. See the [perfect graph theorem](/perfect-graph-theorem/).
- **Berge graph.** A graph with no odd hole and no odd antihole. Every perfect graph is Berge, and the strong perfect graph theorem (Chudnovsky, Robertson, Seymour and Thomas 2006) says that every Berge graph is perfect.
- **Recognition.** Chudnovsky, Cornuéjols, Liu, Seymour and Vušković gave a polynomial-time algorithm in 2005 that decides whether a graph is Berge, and so whether it is perfect.
- **Optimization.** On perfect graphs, $\omega(G) = \vartheta(\overline{G}) = \chi(G)$, where $\vartheta$ is the [Lovász theta function](/lovasz-theta-function/), computable to any precision by semidefinite programming. Grötschel, Lovász and Schrijver used this to find $\omega$, $\chi$, $\alpha$ and optimal colorings of perfect graphs in polynomial time, although each of these is NP-hard on general graphs.
- **$\chi$-bounded classes.** A class of graphs is $\chi$-bounded when $\chi$ is bounded by a function of $\omega$. Perfect graphs are the extreme case $\chi = \omega$; the Mycielski graphs show that the class of all graphs is not $\chi$-bounded.

## References
