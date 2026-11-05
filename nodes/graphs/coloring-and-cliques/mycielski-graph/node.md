---
tag: 15S0P9
kind: concept
slug: mycielski-graph
name: Mycielski construction
aliases:
- Mycielskian
area: graphs/coloring-and-cliques
level: advanced
summary: Builds triangle-free graphs with arbitrarily large chromatic number.
prereqs: [chromatic-number, clique-number, graph-coloring]
see_also: [perfect-graph, lovasz-theta-function, k-coloring, brooks-theorem, strong-perfect-graph-theorem, independence-number]
sources:
  - paper: "J. Mycielski, Sur le coloriage des graphs, Colloquium Mathematicum 3, 161 to 162 (1955)"
    locator: the whole note (the construction and the proof that it raises the chromatic number by one and keeps triangles out)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 5.2, Structure of k-chromatic graphs (Mycielski's construction)
  - paper: "V. Chvátal, The minimality of the Mycielski graph, in Graphs and Combinatorics, Lecture Notes in Mathematics 406, Springer, 243 to 246 (1974)"
    locator: the Grötzsch graph is the smallest triangle-free 4-chromatic graph
  - paper: "M. Larsen, J. Propp and D. Ullman, The fractional chromatic number of Mycielski's graphs, Journal of Graph Theory 19(3), 411 to 416 (1995)"
    locator: the formula for the fractional chromatic number of the Mycielskian
---

The Mycielski construction turns a graph $G$ into a larger graph $M(G)$ whose [chromatic number](/chromatic-number/) is one more than that of $G$, while the [clique number](/clique-number/) does not grow (as long as $G$ has an edge). Starting from a single edge, it gives the 5-cycle, then the 11-vertex Grötzsch graph, and then triangle-free graphs of every chromatic number. So the clique number, a lower bound on $\chi$, can be as weak as possible: a graph can need many colors without containing even a triangle.

## In plain words

A graph that needs many colors often has a big group of points all joined to each other. One might guess that this is the only reason a graph needs many colors. Mycielski's trick shows it is not.

Take a graph. For each point, add a shadow point joined to the same neighbors as the original, but not to the original or to other shadows. Then add one hub joined to all the shadows. The new graph needs one more color than the old one, but it has no new triangle. Repeat the trick, and the number of colors climbs while triangles never appear.

## The idea

**Construction.** Let $G$ have vertices $v_1, \ldots, v_n$. The Mycielskian $M(G)$ has $2n + 1$ vertices $v_1, \ldots, v_n$, $u_1, \ldots, u_n$ and $w$, and these edges:

- every edge $v_i v_j$ of $G$;
- $u_i v_j$ whenever $v_i v_j$ is an edge of $G$, so $u_i$ is joined to the neighbors of $v_i$;
- $w u_i$ for every $i$.

If $G$ has $m$ edges, $M(G)$ has $3m + n$ edges. The vertices $u_i$ form an [independent set](/independent-set/), and $w$ has no neighbor among the $v_i$.

**Theorem (Mycielski 1955).** If $G$ has at least one edge, then $\omega(M(G)) = \omega(G)$ and $\chi(M(G)) = \chi(G) + 1$.

*No new cliques.* A clique contains at most one $u_i$, since the $u_i$ are pairwise non-adjacent. A clique with $w$ has only $w$ and one $u_i$, so it has 2 vertices. A clique with $u_i$ and some $v_j$'s has its $v_j$'s in $N(v_i)$, so replacing $u_i$ by $v_i$ gives a clique of $G$ of the same size. So every clique of $M(G)$ has at most $\max(2, \omega(G))$ vertices, and this is $\omega(G)$ when $G$ has an edge.

*One more color is enough.* Given a proper coloring $c$ of $G$ with $k$ colors, give $v_i$ and $u_i$ the color $c(v_i)$, and give $w$ a new color $k + 1$. An edge $u_i v_j$ has $v_i v_j \in E(G)$, so $c(v_i) \ne c(v_j)$.

*One more color is needed.* Let $k = \chi(G)$ and suppose $M(G)$ has a proper coloring $f$ with $k$ colors, with $f(w) = k$. No $u_i$ has color $k$. Recolor each $v_i$ with $f(v_i) = k$ by $f(u_i)$. This is a proper coloring of $G$ with the colors $1, \ldots, k - 1$. Two vertices that had color $k$ are not adjacent. If $v_i$ was recolored and $v_j$ is a neighbor that was not, then $v_j$ is adjacent to $u_i$, so $f(v_j) \ne f(u_i)$. So $\chi(G) \le k - 1$, a contradiction. $\square$

**The sequence.** Let $M_2 = K_2$ and $M_{k+1} = M(M_k)$. Then $M_k$ is triangle-free with $\chi(M_k) = k$, and it has $3 \cdot 2^{k-2} - 1$ vertices.

## Examples

| graph | vertices | edges | $\omega$ | $\chi$ |
|---|---|---|---|---|
| $M_2 = K_2$ | 2 | 1 | 2 | 2 |
| $M_3 = C_5$ | 5 | 5 | 2 | 3 |
| $M_4$, the Grötzsch graph | 11 | 20 | 2 | 4 |
| $M_5$ | 23 | 71 | 2 | 5 |
| $M_6$ | 47 | 236 | 2 | 6 |

The chromatic numbers in the table agree with an exhaustive backtracking search. For $M_3$: from the edge $v_1 v_2$, the vertices $u_1$ and $u_2$ are joined to $v_2$ and $v_1$, and $w$ to both, which gives the cycle $v_1\, v_2\, u_1\, w\, u_2\, v_1$. Chvátal proved that the Grötzsch graph is the smallest triangle-free graph with $\chi = 4$.

The fractional chromatic number grows much more slowly: Larsen, Propp and Ullman showed $\chi_f(M(G)) = \chi_f(G) + 1/\chi_f(G)$, so $\chi_f(M_k)$ grows like $\sqrt{2k}$ while $\chi(M_k) = k$.

## Where it is used

- **Lower bounds for coloring.** It shows that no function of $\omega$ alone bounds $\chi$, so exact coloring algorithms cannot stop at the clique bound, and branch-and-bound gaps can be large. It also shows that the gap between $\omega$ and $\chi$ is unbounded even when $\omega = 2$.
- **Perfect graphs.** For $k \ge 3$, $M_k$ contains the odd hole $C_5$ and has $\chi > \omega$, so it is not a [perfect graph](/perfect-graph/). It is a standard test case for bounds such as the [Lovász theta function](/lovasz-theta-function/), since $\omega(G) \le \vartheta(\overline{G}) \le \chi(G)$.
- **Benchmarks.** The DIMACS coloring benchmarks include the graphs myciel3 to myciel7, which are hard for exact solvers because the clique lower bound is 2.

## References
