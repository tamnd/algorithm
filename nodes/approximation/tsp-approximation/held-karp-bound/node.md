---
tag: 3WD93E
kind: concept
slug: held-karp-bound
name: Held-Karp lower bound
aliases:
- 1-tree bound
- Held-Karp relaxation bound
- Lagrangian 1-tree bound
area: approximation/tsp-approximation
level: advanced
summary: The best lower bound on a TSP tour from 1-trees with Lagrangian penalties on the vertex degrees; it equals the value of the subtour elimination LP.
prereqs: [mst-lower-bound-for-tsp, lagrangian-relaxation, subtour-elimination-lp, spanning-tree-polytope, lp-duality]
see_also: [subtour-elimination-lp, held-karp-algorithm, subgradient, lagrangian-duality, christofides-algorithm, karlin-klein-oveis-gharan-algorithm, integrality-gap]
sources:
  - paper: doi:10.1287/opre.18.6.1138
    title: Michael Held and Richard M. Karp, The traveling-salesman problem and minimum spanning trees, Operations Research 18(6), 1970
    locator: pages 1138 to 1162 (the 1-tree bound with penalties and its equality with the LP)
  - paper: doi:10.1007/BF01584070
    title: Michael Held and Richard M. Karp, The traveling-salesman problem and minimum spanning trees, Part II, Mathematical Programming 1, 1971
    locator: pages 6 to 25 (the subgradient method for the penalties)
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, sixth edition
    locator: Chapter 21, The Traveling Salesman Problem (lower bounds, the Held-Karp bound)
  - book: isbn:9780691129938
    title: David L. Applegate, Robert E. Bixby, Vašek Chvátal and William J. Cook, The Traveling Salesman Problem, A Computational Study
    locator: the chapters on LP bounds and on subtour cuts
  - title: David S. Johnson, Lyle A. McGeoch and Edward E. Rothberg, Asymptotic experimental analysis for the Held-Karp traveling salesman bound, Proceedings of SODA 1996
    locator: pages 341 to 350 (the gap between the bound and the optimum on random instances)
---

The Held-Karp bound is a lower bound on the optimal tour of the symmetric [traveling salesman problem](/traveling-salesman-problem/). It takes the best [1-tree bound](/mst-lower-bound-for-tsp/) after penalties $\pi_v$ are added to the costs of the edges at each vertex $v$, and it maximizes over all penalties. Held and Karp (1970) showed that this maximum equals the value LP* of the [subtour elimination LP](/subtour-elimination-lp/), so the bound can be computed with minimum spanning trees only. It is not the [Held-Karp dynamic program](/held-karp-algorithm/), which computes OPT exactly in exponential time.

## In plain words

A cheap way to estimate a round trip from below is a 1-tree: put one city aside, connect the others as cheaply as possible without loops, and join the city put aside by its two cheapest roads. Each round trip has this shape, so the cheapest 1-tree is never more than the best trip.

The cheapest 1-tree often has a city with many roads and cities with one road. A round trip has exactly two roads at each city. So make roads at the busy cities more costly and roads at the lonely cities cheaper, and then take back the same total that you added to each round trip. A round trip does not change, but the cheapest 1-tree goes up. The best choice of these extra charges gives the Held-Karp bound.

## The idea

Let $G = (V, E)$ be the complete graph on $n \ge 3$ vertices with costs $c_e \ge 0$, and fix a special vertex $1$. A *1-tree* is a spanning tree of $V \setminus \{1\}$ plus two edges at vertex 1. For a vector $\pi \in \mathbb{R}^V$ of penalties, let

$$L(\pi) = \min_{T \text{ a 1-tree}} \Bigl( c(T) + \sum_{v \in V} \pi_v \bigl(\deg_T(v) - 2\bigr) \Bigr).$$

The Held-Karp bound is $\text{HK} = \max_\pi L(\pi)$.

**Each $L(\pi)$ is a lower bound.** A tour $H$ is a 1-tree with $\deg_H(v) = 2$ at each $v$, so its penalty term is 0, and $L(\pi) \le c(H)$. So $L(\pi) \le \text{OPT}$ for each $\pi$. This is weak [Lagrangian duality](/lagrangian-duality/): the degree constraints $\deg(v) = 2$ are moved into the cost with the multipliers $\pi$. For $\pi = 0$, $L(0)$ is the plain 1-tree bound.

**Computing $L(\pi)$.** With the costs $c'_{uv} = c_{uv} + \pi_u + \pi_v$, each 1-tree $T$ has $c'(T) = c(T) + \sum_v \pi_v \deg_T(v)$. So $L(\pi) = \min_T c'(T) - 2\sum_v \pi_v$: a minimum spanning tree of $V \setminus \{1\}$ for the costs $c'$, plus the two edges at 1 of least $c'$. This takes $O(n^2)$ time with [Prim's algorithm](/prim/).

**Finding good penalties.** $L$ is the minimum of finitely many affine functions of $\pi$, one for each 1-tree, so it is concave and piecewise linear. If $T$ is a minimum 1-tree at $\pi$, the vector $g_v = \deg_T(v) - 2$ is a [subgradient](/subgradient/) of $L$ at $\pi$. Held and Karp (1971) used the step $\pi \leftarrow \pi + t_k\, g$ with a decreasing step size $t_k$: a vertex with degree above 2 gets a larger penalty, and a leaf gets a smaller one. If some minimum 1-tree has all degrees 2, it is an optimal tour and $L(\pi) = \text{OPT}$.

**Theorem (Held and Karp 1970).** $\text{HK} = \text{LP}^*$, the optimum of the subtour elimination LP

$$\min \sum_e c_e x_e \quad \text{subject to} \quad x(\delta(v)) = 2 \ \ (v \in V), \quad x(\delta(S)) \ge 2 \ \ (\emptyset \ne S \subsetneq V), \quad 0 \le x \le 1.$$

*Proof.* Write $V' = V \setminus \{1\}$, and $E(S)$ for the edges with both ends in $S$.

1. *The 1-tree polytope.* A 1-tree is a spanning tree of $V'$ (on the edges $E(V')$) and, independently, two edges of $\delta(1)$. By Edmonds' theorem on the [spanning tree polytope](/spanning-tree-polytope/), the convex hull of the spanning trees of $V'$ is $\{y \ge 0 : y(E(V')) = n - 2,\ y(E(S)) \le |S| - 1 \text{ for } \emptyset \ne S \subseteq V'\}$. The convex hull of the 0/1 vectors on $\delta(1)$ with two ones is $\{z : 0 \le z \le 1,\ z(\delta(1)) = 2\}$. So the convex hull $P_1$ of the 1-trees is the set of $x \ge 0$ with $x(E(V')) = n - 2$, $x(E(S)) \le |S| - 1$ for each nonempty $S \subseteq V'$, $x(\delta(1)) = 2$ and $x_e \le 1$ on $\delta(1)$.
2. *The subtour polytope is $P_1$ with the degree constraints.* Let $x$ satisfy $x(\delta(v)) = 2$ for all $v$. For each $S \subseteq V$, $\sum_{v \in S} x(\delta(v)) = 2x(E(S)) + x(\delta(S))$, so $x(\delta(S)) = 2|S| - 2x(E(S))$, and $x(\delta(S)) \ge 2$ holds exactly when $x(E(S)) \le |S| - 1$. Each cut $\delta(S)$ is also $\delta(V \setminus S)$, and one of $S$, $V \setminus S$ lies in $V'$, so the cut constraints are the constraints $x(E(S)) \le |S| - 1$ for $S \subseteq V'$. The same identity with $S = V'$ gives $x(E(V')) = (2(n - 1) - 2)/2 = n - 2$. For $|S| = 2$ the constraint gives $x_e \le 1$. So the subtour polytope is $P_1 \cap \{x : x(\delta(v)) = 2 \ \forall v\}$.
3. *Lagrangian duality for an LP.* Write $P_1 = \{x : Dx \le d\}$ and the degree constraints as $Ax = b$. The minimum of a linear function over the polytope $P_1$ is reached at a vertex, which is a 1-tree, so $L(\pi) = \min_{x \in P_1} \bigl(cx + \pi(Ax - b)\bigr)$. Weak duality gives $L(\pi) \le \text{LP}^*$. For the other direction, [LP duality](/lp-duality/) for $\min\{cx : Ax = b,\ Dx \le d\}$ gives $\mu^*$ and $y^* \ge 0$ with $A^{\mathsf T}\mu^* - D^{\mathsf T}y^* = c$ and $b\mu^* - dy^* = \text{LP}^*$. Take $\pi = -\mu^*$. For each $x \in P_1$, $cx + \pi(Ax - b) = -y^* Dx + b\mu^* \ge -y^* d + b\mu^* = \text{LP}^*$. So $L(-\mu^*) \ge \text{LP}^*$, and $\text{HK} = \text{LP}^*$. $\blacksquare$

**How strong is it?** HK $\le$ OPT always. For metric costs, OPT $\le \tfrac{3}{2} \cdot \text{HK}$ by Wolsey's analysis of [Christofides' algorithm](/christofides-algorithm/), and the worst ratio OPT/HK, the [integrality gap](/integrality-gap/) of the LP, is at least $4/3$; the [subtour elimination LP](/subtour-elimination-lp/) page gives the bad family. On random points in the plane the bound is usually within about one percent of OPT, in the experiments of Johnson, McGeoch and Rothberg (1996).

## Examples

**Six vertices.** The costs on $A, \ldots, F$ are the rows below; they are the shortest path distances of a small graph, so they are a metric.

|  | $A$ | $B$ | $C$ | $D$ | $E$ | $F$ |
|---|---|---|---|---|---|---|
| $A$ | 0 | 3 | 2 | 3 | 1 | 2 |
| $B$ | 3 | 0 | 2 | 2 | 2 | 1 |
| $C$ | 2 | 2 | 0 | 2 | 3 | 2 |
| $D$ | 3 | 2 | 2 | 0 | 3 | 3 |
| $E$ | 1 | 2 | 3 | 3 | 0 | 3 |
| $F$ | 2 | 1 | 2 | 3 | 3 | 0 |

| bound | value | why |
|---|---|---|
| minimum spanning tree | 8 | [MST lower bound](/mst-lower-bound-for-tsp/) |
| 1-tree, $\pi = 0$ | 10 | the same value for each special vertex |
| Held-Karp, $\pi^* = (0, \tfrac12, 0, -\tfrac12, -\tfrac12, 0)$ | $21/2$ | equals LP* |
| OPT | 11 | the tour $A\,C\,D\,B\,F\,E$ |

At $\pi = 0$ with special vertex $A$, a minimum 1-tree is $BC$, $BD$, $BE$, $BF$ plus $AC$, $AE$. Vertex $B$ has degree 4, and $D$ and $F$ are leaves, so the subgradient asks for a larger penalty at $B$ and smaller ones at $D$ and $F$. At $\pi^*$, the 1-tree $BD$, $BE$, $BF$, $CD$ plus $AC$, $AE$ has the penalized cost $19/2$, and $L(\pi^*) = 19/2 - 2 \cdot (-\tfrac12) = 21/2$. The value of the subtour LP on this instance is $21/2$, so by the theorem no penalties give more. The LP optimum is $x = 1$ on $AE$, $BF$, $CD$ and $x = 1/2$ on $AC$, $AF$, $BD$, $BE$, $CF$, $DE$. It is not a tour, and the gap $11 - 21/2$ is real.

**Seven cities.** On the seven cities $A(5,1)$, $B(6,5)$, $C(0,0)$, $D(8,0)$, $E(5,4)$, $F(0,4)$, $G(3,0)$ with the Manhattan distance, the tree costs 19, the best plain 1-tree costs 25, and HK $=$ OPT $= 28$. Here the penalties close the gap completely.

## Where it is used

- **Exact solvers.** Held and Karp used the bound in branch and bound. Modern codes such as Concorde compute the same value as the subtour LP and add more cuts; see [branch and cut](/branch-and-cut/).
- **Approximation algorithms.** [Christofides' algorithm](/christofides-algorithm/) costs at most $\tfrac32 \cdot \text{HK}$. The [Karlin-Klein-Oveis Gharan algorithm](/karlin-klein-oveis-gharan-algorithm/) samples trees from the LP solution and compares its cost with this bound, and the [Asadpour et al. algorithm](/asadpour-atsp-algorithm/) uses the directed version for the [asymmetric TSP](/asymmetric-tsp/).
- **Local search.** [Lin-Kernighan-Helsgaun](/lin-kernighan-helsgaun/) uses the penalized 1-trees to choose the candidate edges of its moves.
- **Quality certificates.** A heuristic tour can be compared with HK. A ratio near 1 proves that the tour is near optimal.

## References
