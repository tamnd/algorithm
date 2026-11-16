---
tag: MT3Q9G
kind: problem
slug: parameterized-multicut
name: Parameterized multicut
aliases:
- k-multicut
area: complexity/parameterized-complexity
level: research
summary: "Delete at most k edges or vertices so that each of p given terminal pairs is separated. FPT in k alone (Marx and Razgon; Bousquet, Daligault and Thomassé), W[1]-hard in directed graphs."
prereqs: [multicut-problem, parameterized-multiway-cut, important-separators]
see_also: [multicut-problem, parameterized-multiway-cut, important-separators, randomized-contractions, kernel-lower-bounds, w-hardness, parameterized-vertex-cover, fixed-parameter-tractable]
sources:
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 8, Finding cuts and separators (important cuts and random sampling of important separators)
  - paper: doi:10.1016/j.tcs.2005.10.007
    title: "Daniel Marx, Parameterized graph separation problems, Theoretical Computer Science 351(3), 394-406 (2006)"
    locator: multicut is FPT parameterized by the cut size and the number of pairs together
  - paper: doi:10.1137/110855247
    title: "Daniel Marx and Igor Razgon, Fixed-parameter tractability of multicut parameterized by the size of the cutset, SIAM Journal on Computing 43(2), 355-388 (2014)"
    locator: edge and vertex multicut in 2^(O(k^3)) n^O(1) time, and W[1]-hardness of directed multicut (conference version STOC 2011)
  - paper: doi:10.1137/140961808
    title: "Nicolas Bousquet, Jean Daligault and Stéphan Thomassé, Multicut is FPT, SIAM Journal on Computing 47(1), 166-207 (2018)"
    locator: multicut is FPT parameterized by the cut size (conference version STOC 2011)
  - paper: doi:10.1145/2594439
    title: "Marek Cygan, Stefan Kratsch, Marcin Pilipczuk, Michal Pilipczuk and Magnus Wahlström, Clique cover and graph separation: new incompressibility results, ACM Transactions on Computation Theory 6(2), article 6 (2014)"
    locator: no polynomial kernel for edge or vertex multicut parameterized by the cut size unless NP is a subset of coNP/poly
  - url: https://arxiv.org/abs/1507.02178
    title: Marcin Pilipczuk and Magnus Wahlström, Directed multicut is W[1]-hard, even for four terminal pairs, arXiv:1507.02178
    locator: the main theorem (W[1]-hardness in the cut size for four pairs)
---

Parameterized multicut is the [multicut problem](/multicut-problem/) in its decision form, with the size $k$ of the cut as the [parameter](/parameter/). The input has $p$ terminal pairs, and $p$ is not part of the parameter. Marx showed in 2006 that the problem is [fixed-parameter tractable](/fixed-parameter-tractable/) in $k$ and $p$ together. Whether $k$ alone suffices was a main open problem of the area until 2011, when Marx and Razgon, and independently Bousquet, Daligault and Thomassé, proved that it does. In directed graphs the problem is W[1]-hard in $k$, even for four pairs. This page gives the parameterized view; the multicut page has the optimization problem, the LP and the approximation algorithms.

## In plain words

A network has several pairs of points, and each pair must be cut apart. Points from different pairs may stay connected. You may remove at most $k$ links, or at most $k$ ordinary points in the other version.

This is harder than separating every terminal from every other one. In multiway cut, each terminal must be cut away from all the rest, so you know what one side of each cut looks like. In multicut, a solution may leave large parts of the network connected, and it is not clear which side of a cut a vertex should be on. The algorithms that work for $k$ alone first remove, with good probability, all the parts that a solution would cut off, and then the remaining problem looks like multiway cut.

## Definition

**Edge multicut.**

- Instance: an undirected graph $G$, terminal pairs $(s_1, t_1), \ldots, (s_p, t_p)$ of vertices, and an integer $k \ge 0$.
- Parameter: $k$.
- Question: is there a set $S$ of at most $k$ edges such that, for each $i$, the graph $G - S$ has no path from $s_i$ to $t_i$?

**Vertex multicut.** The same, but $S$ is a set of at most $k$ vertices that are not terminals. The graph is given by adjacency lists, with $n$ vertices and $m$ edges.

The number $p$ of pairs is part of the input and can be as large as $\binom{n}{2}$.

## Variants

- **Parameter $k + p$.** FPT by Marx (2006), with important separators. This is the easier case, and it was known five years before the result for $k$ alone.
- **Parameter $p$ only.** For $p = 1$ the problem is a minimum $s$-$t$ cut, in polynomial time. For $p = 3$ the edge version is already NP-hard, because multiway cut with three terminals is the case with the three pairs $(t_1, t_2)$, $(t_1, t_3)$, $(t_2, t_3)$. So $p$ alone is no useful parameter.
- **Directed multicut.** Delete at most $k$ arcs or vertices so that no $s_i$ reaches $t_i$. Marx and Razgon showed that it is W[1]-hard in $k$, and Pilipczuk and Wahlström showed that this holds even for $p = 4$ pairs.
- **Trees.** Edge multicut is NP-hard on trees, and even on stars (see Reductions), so a simple graph shape alone does not make the problem easy.
- **Multiway cut.** The special case where the pairs are all pairs of a terminal set $T$. See [parameterized multiway cut](/parameterized-multiway-cut/).

## Examples

A scratch script solved edge multicut by brute force on the 6-cycle with vertices $0, \ldots, 5$ and the opposite pairs.

| pairs | least multicut | number of optimal solutions |
|---|---|---|
| $(0, 3)$ | 2 | 9 |
| $(0, 3), (1, 4)$ | 2 | 5 |
| $(0, 3), (1, 4), (2, 5)$ | 2 | 3 |

With three pairs, deleting the edges $\{0, 1\}$ and $\{3, 4\}$ leaves the paths $1, 2, 3$ and $4, 5, 0$, and each pair has one vertex on each path. A multiway cut of all six vertices would need all 6 edges. With the terminals $\{0, 2, 4\}$, the least multiway cut has 3 edges, but the multicut with the single pair $(0, 2)$ needs only 2.

For the reduction from vertex cover below, take the graph $H$ with edges $12$, $23$, $31$, $34$. The star with center $c$ and leaves $1, 2, 3, 4$, with one pair per edge of $H$, has a least edge multicut of size 2: $\{c1, c3\}$ or $\{c2, c3\}$. These match the two least vertex covers $\{1, 3\}$ and $\{2, 3\}$ of $H$.

## Known algorithms

- **Marx (2006).** FPT in $k + p$, with [important separators](/important-separators/).
- **Marx and Razgon (2014; STOC 2011).** Edge and vertex multicut in $2^{O(k^3)} n^{O(1)}$ time. The algorithm uses iterative compression and random sampling of important separators to remove the *shadow* of a solution, that is, the parts of the graph that the solution cuts away from all terminals. A solution with no shadow is then found by a separate step.
- **Bousquet, Daligault and Thomassé (2018; STOC 2011).** Multicut is FPT in $k$, with a different, structural approach.
- **Directed graphs.** No FPT algorithm in $k$ exists unless FPT = W[1] (see Bounds).

## Bounds

- **Classical complexity.** NP-complete under polynomial-time many-one reductions, already for $p = 3$ in general graphs and for edge multicut in stars. See the [multicut problem](/multicut-problem/) page.
- **W-hardness.** Directed multicut is W[1]-hard in $k$, even for four pairs (Pilipczuk and Wahlström). So it is not FPT unless FPT = W[1]. See [W-hardness](/w-hardness/).
- **Lower bound in time.** Edge multicut has no $2^{o(k)} n^{O(1)}$ algorithm unless the exponential time hypothesis (ETH) fails. The reduction from vertex cover below keeps $k$ and has linear size.
- **Kernels.** Edge and vertex multicut have no polynomial kernel in $k$ unless NP is a subset of coNP/poly (Cygan, Kratsch, Pilipczuk, Pilipczuk and Wahlström). See [kernel lower bounds](/kernel-lower-bounds/).

## Reductions

- **From vertex cover to edge multicut in stars.** Given $H$, build a star with a center $c$ and one leaf per vertex of $H$, and add the pair $(u, v)$ for each edge $uv$ of $H$. Keep $k$. A pair $(u, v)$ is separated exactly when the edge $cu$ or $cv$ is deleted, so the deleted leaves form a vertex cover, and a vertex cover gives a multicut of the same size. This is a parameterized reduction with $k' = k$ and linear size.
- **From multiway cut.** Multiway cut with terminals $T$ is multicut with all pairs of $T$, with $p = \binom{|T|}{2}$ and the same $k$.
- **From edge to vertex multicut.** Subdivide every edge by a new vertex, and replace each original vertex that is not a terminal by $k + 1$ copies with the same neighbors. A solution of size at most $k$ cannot delete all copies of a vertex, so it deletes only subdivision vertices, which are edges. The cut size stays $k$.

## Applications

Multicut is the common generalization of the minimum $s$-$t$ cut and of multiway cut, and it models network problems where only some pairs of sites must be separated. The shadow removal step that Marx and Razgon introduced for it became a general tool: Chitnis, Hajiaghayi and Marx used it for the FPT algorithm for directed [multiway cut](/parameterized-multiway-cut/).

## References
