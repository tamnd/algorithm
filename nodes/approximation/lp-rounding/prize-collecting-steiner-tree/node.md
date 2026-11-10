---
tag: 95VAJ4
kind: problem
slug: prize-collecting-steiner-tree
name: Prize-collecting Steiner tree
aliases:
- PCST
- prize-collecting Steiner tree problem
area: approximation/lp-rounding
level: advanced
summary: Find a tree from a root that minimizes edge cost plus the penalties of the vertices it leaves out; LP rounding gives 3, primal-dual gives 2 - 1/(n - 1), and Archer et al. go below 2.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(2^m (n + m))}
prereqs: [steiner-tree-problem, lp-relaxation, threshold-rounding, primal-dual-schema]
see_also: [steiner-tree-problem, steiner-forest, goemans-williamson-steiner-forest, threshold-rounding, primal-dual-schema, lagrangian-relaxation, traveling-salesman-problem, steiner-tree-inapproximability]
sources:
  - title: Daniel Bienstock, Michel X. Goemans, David Simchi-Levi and David P. Williamson, A note on the prize collecting traveling salesman problem, Mathematical Programming 59, 1993
    locator: the LP and threshold rounding, ratio 3 for the tree and 5/2 for the tour
  - paper: doi:10.1137/S0097539793242618
    title: Michel X. Goemans and David P. Williamson, A general approximation technique for constrained forest problems, SIAM Journal on Computing 24(2), 1995
    locator: the primal-dual algorithm for prize-collecting Steiner tree, ratio 2 - 1/(n - 1)
  - title: Aaron Archer, MohammadHossein Bateni, MohammadTaghi Hajiaghayi and Howard Karloff, Improved approximation algorithms for prize-collecting Steiner tree and TSP, SIAM Journal on Computing 40(2), 2011
    locator: the first ratio below 2, about 1.9672
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 4.4 (deterministic rounding), Section 5.7 (randomized rounding) and Section 14.1 (primal-dual)
---

The prize-collecting Steiner tree problem (PCST) asks for a tree that contains a root vertex $r$, in a graph with edge costs and a penalty $\pi_v$ on each vertex. The cost of a tree is the cost of its edges plus the penalties of the vertices that it does not reach. So each vertex is either connected, at the price of the edges to it, or left out, at the price of its penalty. With very large penalties on terminals and zero on the other vertices, it is the [Steiner tree problem](/steiner-tree-problem/), so it is NP-hard and APX-hard. Three results mark the history. Bienstock, Goemans, Simchi-Levi and Williamson (1993) gave ratio 3 by [threshold rounding](/threshold-rounding/) of an LP. Goemans and Williamson (1995) gave ratio $2 - 1/(n - 1)$ with the [primal-dual](/goemans-williamson-steiner-forest/) method. Archer, Bateni, Hajiaghayi and Karloff (2011) went below 2.

## In plain words

A company lays cable from its central office. Each house would pay something to be connected, and each piece of cable has a cost. Leaving a house out means losing its payment. The task is to choose which houses to connect, and how, so that cable cost plus lost payments is as small as possible.

A house far away that pays little should be left out. A house near the cable that pays a lot should be connected. The hard part is that cable to one house can also serve the next, so the choices depend on each other.

## Definition

**Input.** An undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges, costs $c_e \ge 0$, a root $r \in V$, and penalties $\pi_v \ge 0$ for $v \in V$.

**Output.** A tree $T$ in $G$ that contains $r$, with the least value

$$c(T) + \pi(V \setminus V(T)) = \sum_{e \in T} c_e + \sum_{v \notin V(T)} \pi_v.$$

The tree may be the single vertex $r$, which pays all penalties.

**The LP.** For each vertex $v$, the variable $y_v$ says how much $v$ is connected, and $x_e$ how much edge $e$ is bought:

$$\min \sum_e c_e x_e + \sum_{v \ne r} \pi_v (1 - y_v) \ \text{ s.t. } \ x(\delta(S)) \ge y_v \ \text{ for } v \in S \subseteq V \setminus \{r\}, \quad 0 \le y_v \le 1, \ x \ge 0.$$

Each set $S$ that holds $v$ and not the root must be crossed as much as $v$ is connected. A tree gives the 0-1 point with $y_v = 1$ exactly for $v \in V(T)$, of value $c(T) + \pi(V \setminus V(T))$, so the LP value is at most OPT.

**Unrooted version.** If no root is given, the tree may be anywhere. Solving the rooted version once for each choice of root gives it.

## Variants

- **Net worth.** Maximize the prizes collected minus the edge cost. The optimal trees are the same, but the ratio is different, and this form is NP-hard to approximate within any constant factor (Feigenbaum, Papadimitriou and Shenker 2001).
- **Quota and budget.** Find the cheapest tree that collects at least a prize $Q$, or the most prize within a cost budget. The $k$-MST problem, with $k$ vertices to connect, is the unit-prize quota case. The algorithms of Garg and of Chudak, Roughgarden and Williamson use PCST as a subroutine with a [Lagrangian](/lagrangian-relaxation/) penalty.
- **Prize-collecting Steiner forest.** Pairs instead of vertices pay penalties if they are not connected. Hajiaghayi and Jain (2006) gave ratio 3 by primal-dual and $2.54$ by LP rounding.
- **Prize-collecting TSP.** The output is a tour instead of a tree. Bienstock et al. gave ratio $5/2$ by threshold rounding with [Christofides](/metric-tsp/), and Goemans and Williamson gave 2.
- **Node-weighted costs.** Costs are on vertices instead of edges. The ratio is then $\Theta(\log n)$, as for set cover.

## Examples

Take the root $r$ and vertices $a, b, c$, the edges $ra$ of cost 1, $ab$ of cost 3 and $rc$ of cost 4, and the penalties $\pi_a = 2$, $\pi_b = 2$, $\pi_c = 3$.

| tree vertices | edge cost | penalties | total |
|---|---|---|---|
| $\{r\}$ | 0 | 7 | 7 |
| $\{r, a\}$ | 1 | 5 | **6** |
| $\{r, a, b\}$ | 4 | 3 | 7 |
| $\{r, c\}$ | 4 | 4 | 8 |
| $\{r, a, c\}$ | 5 | 2 | 7 |
| $\{r, a, b, c\}$ | 8 | 0 | 8 |

The optimum connects only $a$. The vertex $b$ is left out, since the edge $ab$ costs 3 and saves only 2, and $c$ is left out, since $rc$ costs 4 and saves only 3. The graph is a tree, so the LP needs $x_{ra} \ge \max(y_a, y_b)$, $x_{ab} \ge y_b$ and $x_{rc} \ge y_c$, and its optimum is the same point $y_a = 1$, $y_b = y_c = 0$, of value 6.

## Known algorithms

| algorithm | type | guarantee |
|---|---|---|
| brute force over edge sets | exact | time $O(2^m (n + m))$ |
| Bienstock, Goemans, Simchi-Levi and Williamson (1993) | LP and [threshold rounding](/threshold-rounding/) | ratio 3 |
| randomized threshold (in Williamson and Shmoys, Section 5.7) | LP and random threshold | ratio $1/(1 - e^{-1/2}) \approx 2.54$ |
| [Goemans and Williamson](/goemans-williamson-steiner-forest/) (1995) | primal-dual with pruning | ratio $2 - 1/(n - 1)$ |
| Archer, Bateni, Hajiaghayi and Karloff (2011) | primal-dual plus a Steiner tree algorithm | ratio about $1.9672$ |

**Threshold rounding.** Solve the LP, let $U = \{v : y_v \ge \alpha\}$, and build a Steiner tree on $U \cup \{r\}$. The point $x / \alpha$ is feasible for the cut LP of this Steiner tree, and a tree within twice that LP exists and can be found, so the tree costs at most $(2/\alpha) \sum_e c_e x_e$. A vertex left out has $y_v < \alpha$, so $\pi_v \le \pi_v (1 - y_v)/(1 - \alpha)$. With $\alpha = 2/3$, both factors are 3. Choosing $\alpha$ at random lowers the ratio to about $2.54$.

**Primal-dual.** The Goemans-Williamson algorithm grows dual variables on components as in the [Steiner forest](/goemans-williamson-steiner-forest/) algorithm. A component stops growing when its dual reaches the sum of the penalties inside it, which means that leaving it out is paid for. A pruning step then removes the parts that died this way. The result satisfies the stronger *Lagrangian multiplier preserving* bound, in which the penalties also count twice against the dual, and this is why it is the subroutine for $k$-MST.

**Below 2.** Archer et al. run the primal-dual algorithm, find the vertices it connects, and then improve the tree on those vertices with a better Steiner tree algorithm. They also choose between this and other solutions. Their analysis shows the ratio is a constant below 2. The detailed analysis is long and is not given here.

## Bounds

- **Lower bound used.** The LP value above, or the dual packing of the primal-dual method.
- **Integrality gap.** At most $2 - 1/(n - 1)$, by the Goemans-Williamson analysis, since it compares with the dual of this LP. With all penalties infinite on terminals, it contains the Steiner tree cut LP, whose gap is at least $2 - 2/k$ on a cycle with $k$ terminals.
- **Hardness.** NP-hard to approximate within $96/95$, as for [Steiner tree](/steiner-tree-inapproximability/).
- **Open gap.** The best ratio is about $1.9672$, while Steiner tree has ratio below $1.39$.

## Reductions

- **From Steiner tree.** Give each terminal a penalty larger than the cost of all edges, and every other vertex the penalty 0. Then an optimal PCST tree reaches all terminals and is an optimal Steiner tree.
- **Unrooted to rooted.** Try each vertex as the root, and keep the best tree.
- **Metric closure.** Replacing $G$ with its shortest path closure keeps the optimum, as for Steiner tree.
- **To $k$-MST.** Scale all penalties by a factor $\lambda$ and run a Lagrangian multiplier preserving PCST algorithm. A binary search on $\lambda$ gives two trees, one with fewer and one with more than $k$ vertices, which are combined.

## Applications

- **Utility network expansion.** Johnson, Minkoff and Phillips (2000) studied PCST for the design of fiber and gas networks, where some customers are not worth connecting. Their version of the pruning step works well in practice.
- **Computational biology.** In protein interaction networks, PCST finds a connected group of proteins with high scores at a small edge cost, as a model of an active pathway.
- **A subroutine.** It is used inside algorithms for $k$-MST, $k$-TSP, orienteering and other quota problems.

## References
