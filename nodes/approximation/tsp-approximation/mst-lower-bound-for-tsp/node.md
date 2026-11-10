---
tag: RDM5ZH
kind: concept
slug: mst-lower-bound-for-tsp
name: MST lower bound for TSP
aliases:
- MST bound on optimal tour
- 1-tree lower bound
area: approximation/tsp-approximation
level: core
summary: Deleting one edge from an optimal tour gives a spanning tree, so the minimum spanning tree costs at most OPT; the 1-tree bound refines it.
prereqs: [minimum-spanning-tree, traveling-salesman-problem, spanning-tree]
see_also: [held-karp-bound, subtour-elimination-lp, double-tree-algorithm, christofides-algorithm, mst-tsp-heuristic, lagrangian-relaxation]
sources:
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 2, Section 2.4 (the cost of a minimum spanning tree is a lower bound on OPT)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 35.2.1 (the proof of Theorem 35.2)
  - paper: doi:10.1287/opre.18.6.1138
    title: Michael Held and Richard M. Karp, The traveling-salesman problem and minimum spanning trees, Operations Research 18(6), 1970
    locator: pages 1138 to 1162 (1-trees and the bound from them)
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, sixth edition
    locator: Chapter 21, The Traveling Salesman Problem (lower bounds, 1-trees and the Held-Karp bound)
---

The MST lower bound says that a [minimum spanning tree](/minimum-spanning-tree/) costs at most the optimal tour of the [traveling salesman problem](/traveling-salesman-problem/): delete one edge of an optimal tour, and what is left is a spanning tree. It needs only non-negative costs, not the triangle inequality, and the deleted edge gives the slightly better bound $(1 - 1/n) \cdot \text{OPT}$. The *1-tree* bound is a stronger version of the same idea, and with penalties on the degrees it becomes the [Held-Karp bound](/held-karp-bound/). The analyses of the [double-tree algorithm](/double-tree-algorithm/) and of [Christofides' algorithm](/christofides-algorithm/) start from it.

## In plain words

Take the best round trip through all cities. Remove one leg of it. What is left is a single line that visits every city, and a line is one way to connect all cities without a loop.

The cheapest network that connects all cities without a loop can only be cheaper than this line. So it is also cheaper than the best round trip. We can compute this cheapest network quickly, so we get a fast and safe estimate from below of a cost that is hard to compute.

A better estimate comes from a small change: put one city aside, connect the others as cheaply as possible, and then join the city that you put aside by its two cheapest roads. Each round trip also has this shape.

## The idea

Let $G = (V, E)$ be a complete graph on $n \ge 2$ vertices with costs $c_e \ge 0$. OPT is the least cost of a Hamiltonian cycle (a tour), and $T^*$ is a minimum spanning tree.

**Theorem.** $c(T^*) \le (1 - 1/n) \cdot \text{OPT} \le \text{OPT}$.

*Proof.* Let $H$ be an optimal tour, and $e$ its most costly edge. $H$ has $n$ edges of total cost OPT, so $c_e \ge \text{OPT}/n$. The graph $H - e$ is a path through all vertices, so it is a spanning tree, and $c(T^*) \le c(H - e) = \text{OPT} - c_e \le (1 - 1/n) \cdot \text{OPT}$. $\blacksquare$

The proof uses neither the triangle inequality nor symmetry beyond an undirected graph, so the bound holds for each instance of the symmetric TSP with non-negative costs. The bound $(1 - 1/n)$ is tight: when all costs are 1, the tree costs $n - 1$ and each tour costs $n$.

**How good is the bound?** With the triangle inequality, the [double-tree algorithm](/double-tree-algorithm/) makes a tour of cost at most $2c(T^*)$, so

$$\tfrac{1}{2} \cdot \text{OPT} \le c(T^*) \le \text{OPT} \quad \text{(metric costs)}.$$

The factor 2 can be nearly reached. Take a star with $k$ leaves, spokes of cost 1 and cost 2 between any two leaves. The costs are a metric, $c(T^*) = k$, and each tour has at most two edges at the center, so OPT $= 2 + 2(k - 1) = 2k$. Without the triangle inequality the gap has no bound: the tree can cost 0 while each tour must use an edge of huge cost.

**The 1-tree.** Fix a special vertex $s$. A *1-tree* is a spanning tree of $V \setminus \{s\}$ together with two edges at $s$. Each tour is a 1-tree: remove $s$ from the tour, and the rest is a spanning path of $V \setminus \{s\}$, plus the two tour edges at $s$. So the least cost of a 1-tree is a lower bound on OPT. It is easy to compute: a minimum spanning tree of $V \setminus \{s\}$ plus the two cheapest edges at $s$. A 1-tree without its more costly edge at $s$ is a spanning tree of $V$, so

$$c(T^*) \le c(T^*) + \bigl(\text{the second edge at } s\bigr) \le \min_{1\text{-tree}} c \le \text{OPT}.$$

The best special vertex gives the largest bound. A minimum 1-tree is a tour exactly when each vertex has degree 2 in it. This is the start of the method of Held and Karp: add penalties $\pi_v$ to the costs, $c'_{uv} = c_{uv} + \pi_u + \pi_v$. Each tour changes by the constant $2\sum_v \pi_v$, but the minimum 1-tree changes in a different way, and the best penalties give the [Held-Karp bound](/held-karp-bound/), which equals the value of the [subtour elimination LP](/subtour-elimination-lp/).

## Examples

**Seven cities.** The cities $A(5,1)$, $B(6,5)$, $C(0,0)$, $D(8,0)$, $E(5,4)$, $F(0,4)$ and $G(3,0)$ with the Manhattan distance have a unique minimum spanning tree $AE$, $EB$, $AG$, $GC$, $AD$, $CF$ of cost 19. An optimal tour is $A\,B\,E\,F\,C\,G\,D$ with cost 28. Its most costly edges ($AB$, $EF$ and $GD$) cost 5, and $28 - 5 = 23 \ge 19$.

| special vertex | tree on the other six | two cheapest edges at it | 1-tree cost |
|---|---|---|---|
| $A$ | $BE$, $CF$, $CG$, $DG$, $EF$ (cost 19) | $AE$, $AG$ (cost 6) | 25 |
| $B$ | $AD$, $AE$, $AG$, $CF$, $CG$ (cost 17) | $BE$, $BA$ (cost 7) | 24 |
| $C$ to $G$ | | | 24 each |

So the bounds are: tree 19, best 1-tree 25, and OPT 28. The value of the subtour LP is 28 here, so the Held-Karp bound closes the gap on this instance.

**Six vertices with a gap.** On the six-vertex instance of the [Held-Karp bound](/held-karp-bound/) page, the tree costs 8, each 1-tree costs at least 10, the Held-Karp bound is $21/2$ and OPT is 11. Each refinement gains on this instance, and none of them reaches OPT.

**The star.** On the star with $k$ leaves above, the tree costs $k$ and OPT $= 2k$. A 1-tree with a leaf as special vertex costs $(k - 1) + 1 + 2 = k + 2$. A ratio of nearly 2 between OPT and the tree bound is therefore possible, and the 1-tree does not repair it; the penalties of Held and Karp do better.

## Where it is used

- **Approximation algorithms.** The ratio 2 of the [double-tree algorithm](/double-tree-algorithm/) and of the [MST preorder walk](/mst-preorder-walk-tsp/), and half of the ratio 3/2 of [Christofides' algorithm](/christofides-algorithm/), come from $c(T^*) \le \text{OPT}$. The [MST TSP heuristic](/mst-tsp-heuristic/) page compares them.
- **A certificate for each run.** A program that computes a tour and a tree can report the ratio ALG$/c(T^*)$, which bounds the true ratio on that instance.
- **Branch and bound.** Held and Karp (1970, 1971) used 1-trees with penalties as the bound in a branch and bound search for exact tours; see [branch and cut](/branch-and-cut/) for the modern method with LP bounds.
- **Steiner trees.** The same argument in the other direction shows that a minimum spanning tree on the terminals is a 2-approximation for the [Steiner tree problem](/steiner-tree-problem/).
- **Lagrangian relaxation.** The 1-tree bound with penalties is a standard example of [Lagrangian relaxation](/lagrangian-relaxation/) with a [subgradient](/subgradient/) method.

## References
