---
tag: 88H26A
kind: problem
slug: steiner-forest
name: Steiner forest problem
aliases:
- minimum Steiner forest
- generalized Steiner tree problem
area: approximation/lp-rounding
level: advanced
summary: Given a graph with edge costs and pairs of terminals, find the cheapest set of edges that connects each pair; the classic algorithms give ratio 2 - 2/k, and no ratio below 2 is known.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(2^m (n + m))}
prereqs: [steiner-tree-problem, spanning-forest, lp-relaxation, np-hard]
see_also: [goemans-williamson-steiner-forest, steiner-tree-problem, survivable-network-design, generalized-steiner-network, prize-collecting-steiner-tree, jain-iterative-rounding-network-design, steiner-tree-inapproximability, primal-dual-schema]
sources:
  - paper: doi:10.1137/S0097539793242618
    title: Michel X. Goemans and David P. Williamson, A general approximation technique for constrained forest problems, SIAM Journal on Computing 24(2), 1995
    locator: the generalized Steiner tree problem as a proper function, and the 2 - 2/k bound
  - paper: doi:10.1137/S0097539792236237
    title: Ajit Agrawal, Philip Klein and R. Ravi, When trees collide, an approximation algorithm for the generalized Steiner problem on networks, SIAM Journal on Computing 24(3), 1995
    locator: the first 2 - 2/k approximation
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 22 (Steiner forest)
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 7.4 (the generalized Steiner tree problem)
---

The Steiner forest problem asks, for an undirected graph with nonnegative edge costs and a list of pairs of vertices $(s_1, t_1), \ldots, (s_p, t_p)$, for the cheapest set of edges that connects $s_i$ to $t_i$ for each $i$. Different pairs may be connected through each other or kept apart, so an optimal solution is a forest, not always a tree. The problem contains the [Steiner tree problem](/steiner-tree-problem/), so it is NP-hard and hard to approximate within some constant above 1. The primal-dual algorithm of [Goemans and Williamson](/goemans-williamson-steiner-forest/), like the earlier one of Agrawal, Klein and Ravi, gives ratio $2 - 2/k$ with $k$ terminals, and no polynomial algorithm with ratio below 2 is known. It is the $0$-$1$ case of [survivable network design](/survivable-network-design/).

## In plain words

You are given a map of roads, each with a building cost, and a list of pairs of towns. Each pair must be joined by built roads. Two pairs may share roads if that is cheaper, but they do not have to.

If all pairs share one town, this is the Steiner tree problem: join a set of towns as cheaply as possible. In general, it can pay to build several separate networks, one for each group of pairs that are close to each other.

The hard part is the choice of which pairs to group together, and which extra towns to pass through. The best known fast methods lose at most a factor of 2 against the best answer.

## Definition

**Input.** An undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges, a cost $c_e \ge 0$ for each edge, and pairs $(s_i, t_i)$ for $i = 1, \ldots, p$. The *terminals* are the vertices that appear in some pair; let $k$ be their number.

**Output.** A set $F \subseteq E$ such that $s_i$ and $t_i$ are in the same component of $(V, F)$ for each $i$, with the least cost $c(F) = \sum_{e \in F} c_e$. If some pair is in different components of $G$, there is no solution.

**Why a forest.** Removing an edge of a cycle in $F$ keeps all components the same, and the cost does not rise, since $c \ge 0$. So some optimal $F$ is a forest. Each of its trees joins one group of pairs.

**The cut LP.** A set $S \subseteq V$ *separates* a pair if it holds exactly one of its two vertices. Let $\delta(S)$ be the edges with one end in $S$. The relaxation is

$$\min \sum_e c_e x_e \ \text{ s.t. } \sum_{e \in \delta(S)} x_e \ge 1 \text{ for each } S \text{ that separates some pair}, \quad x \ge 0.$$

A set $F$ is feasible exactly when it meets each such cut, so the LP value is at most OPT. Its dual packs values $y_S \ge 0$ on the separating sets so that no edge is crossed by more than its cost; the Goemans-Williamson algorithm grows such a packing.

**Decision version.** Given a bound $B$, is there a feasible $F$ with $c(F) \le B$? It is NP-complete, since the Steiner tree problem is a special case.

## Variants

- **Steiner tree.** All pairs share a vertex $r$: $(r, t_1), \ldots, (r, t_p)$. Then the optimum is one tree.
- **Requirement function form.** Each vertex has a group label, and vertices with the same label must be connected. This is the same problem with the pairs inside each group.
- **Prize-collecting Steiner forest.** A pair may be left unconnected at a penalty $\pi_i$. The primal-dual method gives ratio 3 for it, and LP rounding gives $2.54$ (Hajiaghayi and Jain 2006).
- **Higher requirements.** If pair $i$ needs $r_i$ edge-disjoint paths, the problem is the [generalized Steiner network problem](/generalized-steiner-network/), with ratio 2 by [iterative rounding](/jain-iterative-rounding-network-design/).
- **Online.** The pairs arrive one at a time, and each must be connected at once; greedy is $O(\log^2 k)$-competitive and the method of Berman and Coulston is $O(\log k)$-competitive, matching the bound for the [online Steiner tree problem](/online-steiner-tree-problem/).
- **Planar and Euclidean.** On planar graphs and in the plane there are approximation schemes, by Bateni, Hajiaghayi and Marx (2011) and by Borradaile, Klein and Kenyon-Mathieu, like the [planar Steiner tree PTAS](/planar-steiner-tree-ptas/).

## Examples

Take vertices $a, b, c, d, e, f$, the pairs $(a, d)$ and $(c, f)$, and these edges.

| edge | $ab$ | $af$ | $bd$ | $cd$ | $ce$ | $cf$ | $de$ | $df$ |
|---|---|---|---|---|---|---|---|---|
| cost | 5 | 4 | 2 | 5 | 3 | 3 | 2 | 5 |

The optimum is $\{ab, bd, cf\}$, of cost $5 + 2 + 3 = 10$. It has two trees: $a b d$ and $c f$. A single tree on all four terminals costs at least 12. Such a tree needs an edge at $a$. With $af$, it also needs $cf$ or another path to $c$, and a path to $d$, so it costs at least $4 + 3 + 5 = 12$. With $ab$ and not $af$, it also needs $bd$, $cf$ and a link of cost 5 between $\{c, f\}$ and $d$, so it costs at least 15. So the forest beats every tree here. The cut LP has value $19/2$, and the Goemans-Williamson algorithm returns $\{cf, af, cd\}$ of cost 12, within $2 - 2/4 = 3/2$ of its dual bound 9.

## Known algorithms

| algorithm | type | guarantee |
|---|---|---|
| brute force over edge sets | exact | time $O(2^m (n + m))$ |
| partitions of the pairs plus the Dreyfus-Wagner Steiner tree DP for each part | exact | time exponential in $k$, polynomial in $n$ for fixed $k$ |
| [Agrawal-Klein-Ravi](/goemans-williamson-steiner-forest/) (1995) | primal-dual | ratio $2 - 2/k$ |
| [Goemans-Williamson](/goemans-williamson-steiner-forest/) (1995) | primal-dual with reverse delete | ratio $2 - 2/k$, against the cut LP |
| [Jain](/jain-iterative-rounding-network-design/) (2001) | iterative rounding | ratio 2, against the cut LP |
| Gupta and Kumar (2015) | greedy, gluing paths of pairs | a constant ratio |

Exact methods are practical only for small instances; integer programming with the cut LP and cut separation solves many moderate ones.

## Bounds

- **Lower bound used.** The cut LP value, or any feasible dual packing $\sum_S y_S$.
- **Integrality gap.** The gap of the cut LP is at most $2 - 2/k$, by the Goemans-Williamson analysis. It is at least $2 - 2/k$: on a cycle of $k$ vertices, all terminals, with unit costs and the pairs $(v_1, v_i)$, the LP has value $k/2$ by $x_e = 1/2$, while every solution needs $k - 1$ edges.
- **Hardness.** The Steiner tree problem is NP-hard to approximate within $96/95$ (Chlebík and Chlebíková 2008), so the same holds for Steiner forest; see [Steiner tree inapproximability](/steiner-tree-inapproximability/).
- **Open gap.** The best Steiner tree ratio is below $1.39$, by LP methods that do not extend to forests. For Steiner forest, no polynomial algorithm with ratio $2 - \varepsilon$ for a fixed $\varepsilon > 0$ is known.
- **Bounded treewidth.** The problem is NP-hard even on planar graphs of treewidth 3, and polynomial for treewidth 2 (Bateni, Hajiaghayi and Marx 2011), unlike Steiner tree, which is polynomial for each fixed treewidth.

## Reductions

- **From Steiner tree.** A Steiner tree instance with root $r$ and terminals $t_1, \ldots, t_p$ is the Steiner forest instance with pairs $(r, t_i)$, with the same optimum.
- **Metric closure.** Replacing $G$ with the complete graph on $V$ with shortest path costs gives the same optimum, since each edge of a solution of the closure can be replaced by a shortest path in $G$.
- **To survivable network design.** Set $r_{s_i t_i} = 1$ and all other requirements to 0. The cut LP of [SNDP](/survivable-network-design/) is then the cut LP above, with $x_e \le 1$, which changes nothing at the optimum.
- **Proper functions.** Goemans and Williamson describe the problem with the function $f(S) = 1$ if $S$ separates a pair and $0$ otherwise. This function is symmetric, and it satisfies $f(A \cup B) \le \max(f(A), f(B))$ for disjoint $A, B$. The same algorithm works for each such *proper* function.

## Applications

- **Telecommunication and transport networks.** Several pairs of sites each need a link, and links can be shared. This is the base model of multicommodity network design with fixed costs.
- **VLSI routing.** Each net of pins on a chip must be connected, and wires for different nets share a routing grid.
- **A building block.** Steiner forest appears inside algorithms for prize-collecting problems, for buy-at-bulk design, and as the cost of connecting groups in clustering models.

## References
