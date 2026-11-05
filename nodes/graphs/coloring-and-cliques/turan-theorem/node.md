---
tag: 7NWGMT
kind: theorem
slug: turan-theorem
name: Turán's theorem
aliases:
- Turán graph theorem
area: graphs/coloring-and-cliques
level: core
summary: The most edges a K(r+1)-free graph can have is attained by the Turán graph.
prereqs: [clique, complete-graph, clique-number]
see_also: [ramsey-theorem, motzkin-straus-theorem, independence-number, maximum-clique]
sources:
  - paper: "P. Turán, Egy gráfelméleti szélsőértékfeladatról (On an extremal problem in graph theory), Matematikai és Fizikai Lapok 48, 436 to 452 (1941)"
    locator: the main theorem
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 7.1, Subgraphs (Turán's theorem, the Turán graphs and the Erdős-Stone theorem)
  - book: isbn:9783662572641
    title: Martin Aigner and Günter M. Ziegler, Proofs from THE BOOK, sixth edition, Springer, 2018
    locator: the chapter Turán's graph theorem (five proofs, including the symmetrization proof and the proof by weights on the simplex)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 5.2, Structure of k-chromatic graphs (Turán's theorem)
---

Turán's theorem gives the largest number of edges in a graph with $n$ vertices that has no [clique](/clique/) of $r + 1$ vertices: it is the number of edges of the Turán graph $T_r(n)$, the complete $r$-partite graph whose parts differ in size by at most one, and $T_r(n)$ is the only graph that reaches it. The number is at most $(1 - \frac1r)\frac{n^2}{2}$. The case $r = 2$, that a triangle-free graph has at most $\lfloor n^2/4 \rfloor$ edges, is Mantel's theorem of 1907. The theorem started extremal graph theory.

## Statement

Let $r \ge 1$ and $n \ge 0$ be integers. The **Turán graph** $T_r(n)$ has $n$ vertices split into $r$ parts of sizes $\lfloor n/r \rfloor$ or $\lceil n/r \rceil$ (some parts are empty when $n < r$), with an edge between every two vertices in different parts and no edge inside a part. Let $t_r(n)$ be its number of edges. With $n = qr + s$ and $0 \le s < r$,

$$t_r(n) = \frac{1}{2}\left(n^2 - s(q+1)^2 - (r - s)q^2\right) \le \left(1 - \frac{1}{r}\right)\frac{n^2}{2},$$

with equality on the right when $r$ divides $n$.

**Theorem (Turán 1941).** Let $G$ be a simple graph with $n$ vertices and no subgraph $K_{r+1}$. Then $|E(G)| \le t_r(n)$, and equality holds if and only if $G$ is isomorphic to $T_r(n)$.

The equivalent form by the [clique number](/clique-number/): if $|E(G)| > t_r(n)$, then $\omega(G) \ge r + 1$.

## In plain words

You draw a network on a fixed number of points, and you must avoid a group of a given size in which every two points are linked. How many links can you draw?

The best plan is to split the points into as many teams as one less than the forbidden group size, with the teams as equal as possible. Link every two points from different teams, and never link two points of the same team. Any group of linked points has at most one point from each team, so it is too small. Turán's theorem says that no other plan gives as many links.

## Proof

The proof is by Zykov symmetrization. Fix $n$ and $r$, and let $G$ be a graph with $n$ vertices, no $K_{r+1}$, and the largest possible number of edges. Write $d(v)$ for the degree of $v$. To *clone* $x$ onto $y$ (for non-adjacent $x, y$) means: delete $y$ and add a new vertex $y'$ with $N(y') = N(x)$. The new vertex is not adjacent to $x$.

**Cloning keeps $K_{r+1}$ out.** After a clone of $x$ onto $y$, a clique cannot contain both $x$ and $y'$, since they are not adjacent. A clique that contains $y'$ but not $x$ becomes a clique of the same size of the old graph when $y'$ is replaced by $x$, because $N(y') = N(x)$. So the new graph has no $K_{r+1}$. The same holds when $x$ is cloned onto two non-adjacent vertices in turn, because the first clone is again a vertex with the neighborhood of $x$.

**Step 1: non-adjacency is transitive.** Suppose that $y$ is adjacent to neither $x$ nor $z$, but $x$ and $z$ are adjacent.

- If $d(y) < d(x)$, clone $x$ onto $y$. The number of edges changes by $d(x) - d(y) > 0$, because $y$ is not adjacent to $x$, so $N(x)$ does not contain $y$. This contradicts the choice of $G$. So $d(y) \ge d(x)$, and in the same way $d(y) \ge d(z)$.
- Now clone $y$ onto $x$ and onto $z$. We delete $x$ and $z$, which removes $d(x) + d(z) - 1$ edges (the edge $xz$ is counted twice), and we add two copies of $y$, which are adjacent to neither $y$ nor each other and add $2 d(y)$ edges. The change is $2d(y) - d(x) - d(z) + 1 \ge 1$, again a contradiction.

So for all vertices $x, y, z$: if $x \not\sim y$ and $y \not\sim z$, then $x \not\sim z$ or $x = z$. Together with reflexivity, "equal or not adjacent" is an equivalence relation on $V$.

**Step 2: $G$ is complete multipartite.** The classes of this relation are independent sets, and two vertices of different classes are adjacent. So $G$ is a complete multipartite graph with parts $V_1, \ldots, V_p$. Choosing one vertex from each part gives a clique of $p$ vertices, so $p \le r$.

**Step 3: the parts are balanced.** If two parts have sizes $a \ge b + 2$, move one vertex from the larger part to the smaller. Its new edges number $n - (b + 1)$ and it loses $n - a$, so the count rises by $a - b - 1 \ge 1$, a contradiction. If $p < r$ and some part has at least 2 vertices, split one vertex off into a new part; the count rises and there is still no $K_{r+1}$, a contradiction. So either $p = r$ with parts of sizes that differ by at most one, or $p = n < r$ with parts of size 1. In both cases $G \cong T_r(n)$.

So the largest number of edges is $t_r(n)$, and each extremal graph is $T_r(n)$, which proves both the bound and the uniqueness.

**The closed bound.** For parts of sizes $n_1, \ldots, n_r$ with sum $n$, the number of edges is $\frac12(n^2 - \sum_i n_i^2)$. By the Cauchy-Schwarz inequality, $\sum_i n_i^2 \ge n^2/r$, so $t_r(n) \le (1 - \frac1r)\frac{n^2}{2}$, with equality exactly when all $n_i = n/r$. $\blacksquare$

## Consequences

- **Mantel's theorem.** For $r = 2$: a triangle-free graph on $n$ vertices has at most $\lfloor n^2/4 \rfloor$ edges, and only $K_{\lfloor n/2 \rfloor, \lceil n/2 \rceil}$ reaches it.
- **Independent sets.** Apply the theorem to the complement. A graph with $n$ vertices and average degree $\bar d$ has an [independent set](/independent-set/) of at least $n/(\bar d + 1)$ vertices; the [independence number](/independence-number/) page proves the stronger Caro-Wei form.
- **Clique number from the edge count.** A graph with $m$ edges and $n$ vertices has $\omega(G) \ge \frac{n^2}{n^2 - 2m}$, from $m \le (1 - \frac{1}{\omega})\frac{n^2}{2}$. This is a cheap lower bound for [maximum clique](/maximum-clique/) search.
- **Motzkin-Straus.** The [Motzkin-Straus theorem](/motzkin-straus-theorem/) gives a continuous version and another proof of the bound $(1 - \frac1r)\frac{n^2}{2}$.
- **Erdős-Stone.** For each graph $H$ with chromatic number $\chi(H) = r + 1 \ge 3$, the largest number of edges in an $H$-free graph is $(1 - \frac{1}{r} + o(1))\frac{n^2}{2}$. So Turán graphs are asymptotically extremal for every non-bipartite forbidden graph.

## Tightness

The bound is exact for every $n$ and $r$, since $T_r(n)$ has no $K_{r+1}$: a clique takes at most one vertex from each of the $r$ parts. Adding any edge to $T_r(n)$ joins two vertices of the same part, and with one vertex from each other part (when all parts are non-empty) it makes a $K_{r+1}$. For small cases:

| $n$ | $t_2(n)$ | $t_3(n)$ | $t_4(n)$ |
|---|---|---|---|
| 3 | 2 | 3 | 3 |
| 4 | 4 | 5 | 6 |
| 5 | 6 | 8 | 9 |
| 6 | 9 | 12 | 13 |

An exhaustive search over all graphs on up to 6 labeled vertices gives the same maxima. For $r = 3$ and $n = 6$, the extremal graph is $K_{2,2,2}$, the octahedron, with 12 edges.

## History

W. Mantel proved the triangle case in 1907. Pál Turán proved the general theorem in 1941, in Hungarian, and asked the general question of the largest number of edges with a forbidden subgraph, which became extremal graph theory. A. A. Zykov gave the symmetrization proof in 1949. Erdős and Stone extended the asymptotic form to all forbidden graphs in 1946. Aigner and Ziegler present five proofs.

## References
