---
tag: J2ZVG7
kind: problem
slug: multicut-problem
name: Multicut problem
aliases:
- minimum multicut
area: graphs/flows-and-cuts
level: research
summary: Remove minimum-weight edges to disconnect k given source-sink pairs.
prereqs: [multiway-cut-problem, multi-commodity-flow-problem, lp-relaxation, np-hard]
see_also: [min-cut-problem, sparsest-cut-problem, integrality-gap, primal-dual-schema, unique-games-conjecture, fixed-parameter-tractable, min-cut-max-flow-duality, lp-duality]
sources:
  - paper: doi:10.1137/S0097539793243016
    title: Naveen Garg, Vijay V. Vazirani and Mihalis Yannakakis, Approximate max-flow min-(multi)cut theorems and their applications, SIAM Journal on Computing 25(2), 235 to 251 (1996)
    locator: the whole paper (the region-growing rounding, the O(log k) approximation and the matching gap)
  - paper: doi:10.1007/BF02523685
    title: Naveen Garg, Vijay V. Vazirani and Mihalis Yannakakis, Primal-dual approximation algorithms for integral flow and multicut in trees, Algorithmica 18(1), 3 to 20 (1997)
    locator: the whole paper (NP-hardness on trees and the factor 2 primal-dual algorithm)
  - paper: doi:10.1137/S0097539792225297
    title: E. Dahlhaus, D. S. Johnson, C. H. Papadimitriou, P. D. Seymour and M. Yannakakis, The complexity of multiterminal cuts, SIAM Journal on Computing 23(4), 864 to 894 (1994)
    locator: the NP-hardness of multiway cut for three terminals, which is a special case of multicut
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms, Springer (2001)
    locator: Chapter 18, Multicut and integer multicommodity flow in trees, and Chapter 20, Multicut in general graphs
---

The multicut problem asks, in an undirected graph with nonnegative edge weights and $k$ pairs of vertices $(s_1, t_1), \ldots, (s_k, t_k)$, for a set of edges of least total weight whose removal leaves no path from $s_i$ to $t_i$ for any $i$. For $k = 1$ it is the [minimum $s$-$t$ cut](/min-cut-problem/). It contains the [multiway cut problem](/multiway-cut-problem/), where the pairs are all pairs of a terminal set, so it is [NP-hard](/np-hard/) for $k \ge 3$; it is NP-hard even on trees. Its LP relaxation is the dual of maximum [multicommodity flow](/multi-commodity-flow-problem/), and Garg, Vazirani and Yannakakis rounded it by region growing to get an $O(\log k)$ approximation, which also proves that the minimum multicut is at most $O(\log k)$ times the maximum multicommodity flow. That gap is tight for the LP.

## In plain words

A network has several pairs of points that must not be able to talk to each other: the first point of each pair must be cut off from the second. Points from different pairs may stay connected. You want the cheapest set of links to remove.

With one pair this is the classic cheapest cut. With many pairs it is hard, even when the network is a tree. A good approximate method thinks of each link as having a length, chosen so that each pair is far apart while the total cost stays small, and then grows a ball around each first point and cuts the links at its boundary, choosing the radius where few links cross.

## Definition

**Input.** An undirected graph $G = (V, E)$ with weights $w : E \to \mathbb{R}_{\ge 0}$, real or integer, and $k$ pairs $(s_i, t_i)$ with $s_i \ne t_i$. The pairs need not be disjoint. There is no direction, so there are no antiparallel edges; parallel edges add up.

**Output.** A set $F \subseteq E$ of least weight $w(F)$ such that, for each $i$, $G - F$ has no $s_i$-$t_i$ path.

**LP relaxation.** Let $\mathcal{P}_i$ be the set of $s_i$-$t_i$ paths. Give each edge a length $x_e \in [0, 1]$ and require each such path to have length at least 1:

$$\min \sum_{e} w(e)\, x_e \quad \text{s.t.} \quad \sum_{e \in P} x_e \ge 1 \ \ (P \in \mathcal{P}_i,\ 1 \le i \le k), \qquad x \ge 0.$$

A multicut $F$ gives the feasible point $x = \mathbf{1}_F$. The LP has exponentially many constraints, but a shortest-path computation for each pair separates them, and a compact form with one distance variable per pair of vertices also exists. Its [LP dual](/lp-duality/) is maximum total multicommodity flow with capacities $w$, so $\text{max flow} = \text{LP} \le \text{min multicut}$.

## Variants

- **Directed multicut.** Remove edges so that no $s_i$ reaches $t_i$ in a directed graph. Each edge of an antiparallel pair is separate. It is much harder to approximate than the undirected version.
- **Multicut in trees.** NP-hard, and MAX SNP-hard even for trees of height 1 with unit weights; a primal-dual algorithm gives factor 2.
- **Node multicut.** Remove vertices instead of edges.
- **Multiway cut** is the case where the pairs are all pairs from a set of terminals.
- **Steiner multicut.** Each of several vertex sets must be split, not necessarily fully.

## Examples

**A star, where the LP is fractional.** Let $c$ be joined to $a$, $b$ and $d$ by edges of weight 1, with the pairs $(a, b)$, $(b, d)$ and $(a, d)$. Each pair's only path uses two of the three edges, so any multicut must remove at least two edges, and removing $ca$ and $cb$ works: the optimum is 2. The LP sets $x_e = \frac12$ on all three edges; each path has length 1, and the cost is $\frac32$. The maximum multicommodity flow, $\frac12$ for each pair, is also $\frac32$, so the gap here is $\frac43$.

**Two pairs.** Let $F$ be an optimal multicut for $k = 2$, let $A$ be the component of $s_1$ in $G - F$ and $B$ that of $s_2$; the boundary of each lies in $F$, and $t_1 \notin A$, $t_2 \notin B$. If $s_2 \in A$, the set $A$ holds $s_1, s_2$ and not $t_1, t_2$. If $s_2 \notin A$ and $t_2 \in A$, the set $A$ holds $s_1, t_2$ and not $t_1, s_2$. Otherwise $A$ and $B$ are disjoint and $t_2 \notin A \cup B$: if $t_1 \notin B$, the set $A \cup B$ holds $s_1, s_2$ and not $t_1, t_2$; if $t_1 \in B$, the set $V \setminus B$ holds $s_1, t_2$ and not $t_1, s_2$. In every case the boundary of the set lies in $F$, so one of the two minimum cuts in the table is optimal.

**One pair.** For $k = 1$ the LP has an integral optimum and its value is the maximum flow, by the [max-flow min-cut theorem](/max-flow-min-cut-theorem/).

**A zero-weight edge** can always be removed for free, so it never changes the optimum.

**Pairs already separated.** If $s_i$ has no path to $t_i$ in $G$, the pair imposes nothing. If this holds for all pairs, the empty set is optimal, of weight 0.

## Known algorithms

| setting | guarantee | method |
|---|---|---|
| $k = 1$ | exact | one maximum flow |
| $k = 2$, undirected | exact | the better of two minimum cuts, $\{s_1, s_2\}$ against $\{t_1, t_2\}$ and $\{s_1, t_2\}$ against $\{t_1, s_2\}$ |
| general undirected | $O(\log k)$ | LP rounding by region growing (Garg, Vazirani and Yannakakis) |
| trees | 2 | primal-dual (Garg, Vazirani and Yannakakis) |
| parameterized by the cut size | exact | fixed-parameter tractable |

**Region growing.** Solve the LP to get lengths $x$ and value $L$. While some pair is still connected, pick such an $s_i$ and grow a ball $B(s_i, r) = \{ v : \operatorname{dist}_x(s_i, v) \le r \}$ in the graph that remains. Define its volume as $L / k$ plus the LP weight $w(e) x_e$ of the edges inside the ball, plus the fractions of the boundary edges inside the ball. As $r$ grows from 0 to $\frac12$, the volume grows at rate equal to the weight of the boundary. If the boundary weight were always more than $c$ times the volume, the volume would grow by a factor $e^{c/2}$, and it cannot exceed $L + L/k$. With $c = 2 \ln(k + 1)$ this is a contradiction, so some radius $r < \frac12$ has boundary weight at most $c$ times the volume. Cut those edges and delete the ball. The ball holds no $t_i$ with $s_i$ inside, because $\operatorname{dist}_x(s_i, t_i) \ge 1 > 2r$. Each ball is charged its own volume, the LP weights of different balls are disjoint, and the extra $L/k$ terms add up to at most $L$, so the total is $O(\log k) \cdot L$. The constant depends on the presentation; the original paper and Vazirani's book give a bound of the form $c \ln(k + 1)$ with a small constant $c$.

## Bounds

- **NP-hardness.** For $k \ge 3$ the problem contains multiway cut with three terminals, which Dahlhaus et al. proved NP-hard; it is also NP-hard and MAX SNP-hard on trees.
- **Integrality gap.** The LP gap is $\Theta(\log k)$: on expanders with suitable pairs the minimum multicut is $\Omega(\log k)$ times the maximum flow. So $O(\log k)$ is the best that rounding this LP can give.
- **Approximation hardness.** Under the [unique games conjecture](/unique-games-conjecture/), no polynomial algorithm has a constant ratio.
- **Lower bound.** Any exact method reads the input, $\Omega(n + m + k)$.

## Reductions

- **Multiway cut to multicut**, with all pairs of terminals as the pairs.
- **Vertex cover to multicut in stars.** In a star with center $c$, a pair $(u, v)$ of leaves is separated exactly when $cu$ or $cv$ is removed, so multicut in a star with unit weights is vertex cover in the graph whose edges are the pairs. This shows NP-hardness on trees of height 1.
- **Multicut LP to maximum multicommodity flow**, by LP duality.
- **Multicut to sparsest cut**, as a subroutine: approximating the sparsest cut repeatedly helps with balanced cut problems, and the same metric rounding drives both.

## Applications

- Network security and reliability, where given pairs of sites must be cut off from each other.
- Clustering with "cannot-link" constraints, where pairs must end in different clusters.
- A subroutine in approximation algorithms for other cut and partitioning problems.
- Bounding the gap between flows and cuts for many commodities, an approximate max-flow min-cut theorem.

## References
