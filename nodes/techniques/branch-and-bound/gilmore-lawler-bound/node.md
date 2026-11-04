---
tag: V6VPQA
kind: concept
slug: gilmore-lawler-bound
name: Gilmore-Lawler bound
aliases:
- GLB
- Gilmore-Lawler lower bound
area: techniques/branch-and-bound
level: advanced
summary: Lower bound for the quadratic assignment problem obtained from a linear assignment relaxation.
prereqs: [quadratic-assignment-problem, assignment-problem, bounding-function]
see_also: [quadratic-assignment-problem, assignment-problem, hungarian-algorithm, bounding-function, best-first-branch-and-bound, depth-first-branch-and-bound, lagrangian-relaxation, facility-location-problem]
sources:
  - paper: doi:10.1137/0110022
    title: P. C. Gilmore, Optimal and suboptimal algorithms for the quadratic assignment problem, Journal of the Society for Industrial and Applied Mathematics 10(2), 1962
    locator: pp. 305 to 313
  - paper: doi:10.1287/mnsc.9.4.586
    title: Eugene L. Lawler, The quadratic assignment problem, Management Science 9(4), 1963
    locator: pp. 586 to 599
  - book: isbn:9780898716634
    title: Rainer Burkard, Mauro Dell'Amico and Silvano Martello, Assignment Problems
    locator: Chapter 7, Quadratic assignment problems (Gilmore-Lawler bound)
---

The Gilmore-Lawler bound is a lower bound on the cost of a [quadratic assignment problem](/quadratic-assignment-problem/). It replaces each quadratic cost by the smallest cost that one facility at one location can have, whatever the other facilities do, and then solves a linear [assignment problem](/assignment-problem/) on these costs. Gilmore gave it in 1962 and Lawler in 1963, and it is a common [bounding function](/bounding-function/) in branch and bound for the quadratic assignment problem.

## In plain words

Some factories must be put at some sites, one factory per site. Goods flow between each pair of factories, and the cost is flow times distance, summed over all pairs. The hard part is that the cost of one factory depends on where all the others are.

The bound asks a simpler question for each factory and each site: if this factory is at this site, what is the least it can pay, if the others are put in the best way for this one factory only? The answer is easy: send the largest flows over the shortest distances. This gives a table of costs, one for each factory and site. The cheapest way to match factories to sites in this table can never cost more than the true best plan.

## The idea

In the Koopmans-Beckmann form, the problem has an $n \times n$ flow matrix $F$ and an $n \times n$ distance matrix $D$, and asks for a permutation $p$ that minimizes

$$C(p) = \sum_{i=1}^{n} \sum_{j=1}^{n} f_{ij} \, d_{p(i) p(j)} .$$

Fix facility $i$ at location $k$. The terms of $C(p)$ that belong to row $i$ are $f_{ii} d_{kk} + \sum_{j \ne i} f_{ij} d_{k p(j)}$, and $p$ maps the $n - 1$ other facilities one to one onto the $n - 1$ other locations. Write $\langle a, b \rangle^-$ for the *minimum scalar product* of two vectors, the smallest value of $\sum_t a_t b_{\sigma(t)}$ over all permutations $\sigma$. By the rearrangement inequality, it is reached when $a$ is sorted up and $b$ is sorted down. Let

$$l_{ik} = f_{ii} d_{kk} + \langle \hat{f}_i, \hat{d}_k \rangle^- ,$$

where $\hat{f}_i$ is row $i$ of $F$ without $f_{ii}$ and $\hat{d}_k$ is row $k$ of $D$ without $d_{kk}$. Then row $i$ of $C(p)$ is at least $l_{i p(i)}$ for every $p$, so

$$C(p) \ge \sum_{i=1}^{n} l_{i p(i)} \ge \min_{q} \sum_{i=1}^{n} l_{i q(i)} = \mathrm{GLB}.$$

The last minimum is a linear assignment problem, which the [Hungarian algorithm](/hungarian-algorithm/) solves in $O(n^3)$ time. Sorting the rows of $F$ and $D$ once takes $O(n^2 \log n)$ time, and each $l_{ik}$ then takes $O(n)$ time, so the whole bound takes $O(n^3)$ time.

**Inside branch and bound.** A node of the search fixes a partial assignment: facilities in a set $A$ are placed at locations $p(A)$. The cost then splits into three parts: the fixed cost among the facilities of $A$, which is known exactly; the cost between a free facility and a fixed one, which is linear in the location of the free facility; and the cost among the free facilities, which is bounded as above on the free rows and columns. Adding the linear part to $l_{ik}$ and solving one assignment problem on the free facilities and locations gives the bound at the node. Lawler's paper states the problem in a more general form with a cost $c_{ijkl}$ for each pair of assignments and bounds it in the same way.

The bound is weak in one clear way: each facility chooses the best order of the other facilities for itself, and these choices need not agree with one permutation.

## Examples

Four facilities must be placed at four points on a line, at positions 0, 1, 2 and 3, so $d_{kl} = |k - l|$. The flows are

$$F = \begin{pmatrix} 0 & 5 & 2 & 4 \\ 5 & 0 & 3 & 1 \\ 2 & 3 & 0 & 2 \\ 4 & 1 & 2 & 0 \end{pmatrix}.$$

For facility 1, the flows to the others sorted up are $(2, 4, 5)$. Location 0 has distances $(3, 2, 1)$ sorted down, so $l_{1,0} = 6 + 8 + 5 = 19$. Location 1 has distances $(2, 1, 1)$, so $l_{1,1} = 4 + 4 + 5 = 13$. The full table, with rows for facilities 1 to 4 and columns for positions 0 to 3, is

| | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| facility 1 | 19 | 13 | 13 | 19 |
| facility 2 | 14 | 10 | 10 | 14 |
| facility 3 | 13 | 9 | 9 | 13 |
| facility 4 | 11 | 8 | 8 | 11 |

The two middle positions save 6 for facility 1, 4 for facilities 2 and 3, and 3 for facility 4. The best assignment puts facility 1 and one of facilities 2 and 3 in the middle, and costs $19 + 14 + 13 + 11 - 6 - 4 = 47$. So $\mathrm{GLB} = 47$.

The 24 permutations have costs from 48 to 68. The optimum 48 puts facilities 4, 1, 2, 3 at positions 0, 1, 2, 3: the unordered pairs cost $5 \cdot 1 + 2 \cdot 2 + 4 \cdot 1 + 3 \cdot 1 + 1 \cdot 2 + 2 \cdot 3 = 24$, and each pair is counted twice. The bound is 1 below the optimum, and it is below the cost of every one of the 24 permutations, as it must be.

If the flows from facility 2 to 4 and from 3 to 4 are set to 0, the same steps give a bound of 32, and the optimum is also 32. Here the bound proves optimality at the root, and a branch and bound search stops at once.

## Where it is used

- As the bound in [depth-first](/depth-first-branch-and-bound/) and [best-first](/best-first-branch-and-bound/) branch and bound for the quadratic assignment problem, where it is cheap enough to compute at every node.
- As a baseline for stronger bounds, such as bounds from eigenvalues, from [Lagrangian relaxation](/lagrangian-relaxation/) or from linear and semidefinite relaxations, which are compared with it in the literature surveyed by Burkard, Dell'Amico and Martello.
- In [facility location](/facility-location-problem/) and layout problems of quadratic assignment type, such as placing units on a circuit board or departments in a building.
- In the same pattern for other quadratic problems: bound each quadratic row by its best linear completion, then solve one linear problem.

## References
