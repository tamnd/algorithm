---
tag: BQ3B9A
kind: problem
slug: hypervolume-computation
name: Hypervolume computation
aliases:
- hypervolume calculation
- S-metric computation
- computing the hypervolume indicator
area: optimization/multi-objective
level: advanced
summary: Compute the volume that a finite set of N points dominates up to a reference point. O(N log N) for two and three objectives, #P-hard when the number of objectives is part of the input.
prereqs: [hypervolume-indicator, klee-measure-problem, pareto-dominance]
see_also: [overmars-yap-algorithm, sweep-line-technique, segment-tree, area-of-union-of-rectangles, epsilon-indicator, igd-indicator, multi-objective-evolutionary-algorithm, kung-algorithm]
sources:
  - paper: doi:10.1109/TEVC.2009.2015575
    title: Nicola Beume, Carlos M. Fonseca, Manuel López-Ibáñez, Luís Paquete and Jan Vahrenhold, On the complexity of computing the hypervolume indicator, IEEE Transactions on Evolutionary Computation 13(5), 2009, 1075-1082
    locator: the dimension-sweep algorithm with O(N log N) time for three objectives and the Ω(N log N) lower bound
  - paper: doi:10.1016/j.comgeo.2010.03.004
    title: Karl Bringmann and Tobias Friedrich, Approximating the volume of unions and intersections of high-dimensional geometric objects, Computational Geometry 43(6-7), 2010, 601-610
    locator: the #P-hardness of the hypervolume and the randomized approximation scheme for the volume of a union
  - paper: doi:10.1109/FOCS.2013.51
    title: Timothy M. Chan, Klee's measure problem made easy, 54th IEEE Symposium on Foundations of Computer Science, FOCS 2013, 410-419
    locator: O(n^(d/2)) time for Klee's measure problem and O(n^(d/3) polylog n) time for orthants, which includes the hypervolume
  - paper: doi:10.1145/3453474
    title: Andreia P. Guerreiro, Carlos M. Fonseca and Luís Paquete, The hypervolume indicator, computational problems and algorithms, ACM Computing Surveys 54(6), 2021, article 119
    locator: the survey of exact and approximate algorithms, contributions and subset selection
  - paper: "Carlos M. Fonseca, Luís Paquete and Manuel López-Ibáñez, An improved dimension-sweep algorithm for the hypervolume indicator, IEEE Congress on Evolutionary Computation, CEC 2006, 1157-1163"
    locator: the three-objective sweep and the recursion on the last objective with O(N^(p-2) log N) time
---

Hypervolume computation asks for the [hypervolume indicator](/hypervolume-indicator/) of a finite set of $N$ points in $\mathbb{R}^p$: the volume of the union of the boxes between each point and a reference point. It is the special case of [Klee's measure problem](/klee-measure-problem/) in which all boxes share one corner. For $p = 2$ and $p = 3$ a sweep solves it in $O(N \log N)$ time, which is optimal in the algebraic decision tree model (Beume et al., 2009). When $p$ is part of the input the problem is #P-hard (Bringmann and Friedrich, 2010), and the best general bound, $O(N^{p/3} \operatorname{polylog} N)$, is due to Chan (2013).

## In plain words

You have a set of solutions, each with several costs, and a corner point that is worse than all of them. Each solution marks a box between itself and the corner. You want the total size of the area or volume that the boxes cover, with each overlap counted once. With two costs the boxes form a staircase, and you can add up its steps after one sort. With three costs you cut the boxes into thin layers and keep the staircase of each layer up to date. With many costs the overlaps become so complex that no fast exact method is known.

## Definition

**Convention.** All objectives are minimized, $p$ is the number of objectives, $N$ is the population size (here the number of points), and $y = f(x)$ is the image of $x$.

**Input.** A finite set $A \subset \mathbb{R}^p$ of $N$ points and a reference point $r \in \mathbb{R}^p$.

**Output.** $\mathrm{HV}(A; r) = \lambda\big(\bigcup_{a \in A,\ a < r} [a_1, r_1] \times \cdots \times [a_p, r_p]\big)$, where $\lambda$ is the Lebesgue measure and $a < r$ means $a_m < r_m$ for all $m$. Points that do not strictly dominate $r$ add nothing and can be dropped in $O(p N)$ time. With rational input the answer is rational, and the implementation computes it exactly with integers or `Fraction`.

## Variants

- **Exclusive contributions.** For each $a \in A$, $\mathrm{HV}(A) - \mathrm{HV}(A \setminus \{a\})$. Selection in SMS-EMOA needs the point with the smallest contribution.
- **Hypervolume subset selection.** Choose $k$ of the $N$ points with the largest hypervolume. For $p = 2$ dynamic programming solves it in polynomial time; for larger $p$ it is NP-hard.
- **Approximation.** Compute $\mathrm{HV}$ within a factor $1 \pm \varepsilon$ with high probability.
- **Expected improvement.** The expected gain in hypervolume when a new point is random, used in Bayesian optimization.

## Examples

**Two objectives.** For $A = \{(1, 4), (2, 2), (4, 1)\}$ and $r = (5, 5)$, sorted by the first objective, the steps are $(5 - 1)(5 - 4) = 4$, $(5 - 2)(4 - 2) = 6$ and $(5 - 4)(2 - 1) = 1$, so $\mathrm{HV} = 11$.

**Three objectives, by inclusion and exclusion.** For $C = \{(1, 2, 3), (2, 3, 1), (3, 1, 2)\}$ and $r = (4, 4, 4)$, the three boxes have volume $6$ each, each pair meets in volume $2$, and all three meet in $[(3, 3, 3), r]$ of volume $1$, so $\mathrm{HV} = 18 - 6 + 1 = 13$.

**Three objectives, by the sweep below.** The points in order of the third objective are $(2, 3, 1)$, $(3, 1, 2)$ and $(1, 2, 3)$.

| $q$ | $V$ after line L4 | staircase after line L7 | area after line L7 |
|---|---|---|---|
| (2, 3, 1) | 0 | (2, 3) | (4 − 2)(4 − 3) = 2 |
| (3, 1, 2) | 2 · (2 − 1) = 2 | (2, 3), (3, 1) | 2 + (4 − 3)(3 − 1) = 4 |
| (1, 2, 3) | 2 + 4 · (3 − 2) = 6 | (1, 2), (3, 1) | 4 + (2 − 1)(4 − 2) + (3 − 2)(3 − 2) = 7 |

Line L8 returns $6 + 7 \cdot (4 - 3) = 13$. In the last row, $(1, 2)$ removes $(2, 3)$, and the new area is a strip of width $1$ and height $2$ before $(2, 3)$, then a strip of width $1$ and height $1$ up to $(3, 1)$.

## Known algorithms

**Inclusion and exclusion.** $\mathrm{HV} = \sum_{\emptyset \ne S \subseteq A} (-1)^{\lvert S \rvert + 1} \prod_m (r_m - \max_{a \in S} a_m)$, in $O(2^N p N)$ time. The tests use it as the reference.

**Two objectives.** Sort by the first objective and keep the running minimum $h$ of the second; each point with $y_2 < h$ adds $(r_1 - y_1)(h - y_2)$. This is $O(N \log N)$ time and $O(N)$ space.

**Three objectives: the dimension sweep.** Fonseca, Paquete and López-Ibáñez (2006) gave this sweep, and Beume et al. (2009) proved its $O(N \log N)$ bound.

```pseudo id=main
HV3D(A, r)
L1  sort the points of A that strictly dominate r by the third objective
L2  S ← an empty staircase sorted by the first objective; area ← 0; V ← 0; z ← the third objective of the first point
L3  for each point q in this order do
L4      V ← V + area · (q_3 − z); z ← q_3
L5      if a point of S weakly dominates (q_1, q_2) then continue
L6      remove from S the points that (q_1, q_2) weakly dominates, and add to area the strips that (q_1, q_2) newly covers
L7      insert (q_1, q_2) into S
L8  return V + area · (r_3 − z)
```

*Why it is correct.* For $t$ in $[z, r_3)$, the cross-section of the dominated region at height $t$ is the 2D dominated region of the projections $(q_1, q_2)$ of the points with $q_3 \le t$. Invariant: after line L7, $S$ is the set of non-dominated projections of the points processed so far, sorted by the first objective with the second falling, and `area` is their 2D hypervolume. Line L5 keeps both when the new projection is weakly dominated. Otherwise the new region is cut into vertical strips at the first coordinates of the removed points: in a strip that starts at $x$, the old staircase covers heights from the second coordinate of the last point at or before $x$ up to $r_2$, so the new part is that height minus $q_2$. After the next point of $S$, whose second coordinate is below $q_2$, nothing is new. Between two consecutive heights the cross-section does not change, so line L4 adds the exact volume of each slab, and line L8 adds the last slab. With a balanced search tree for $S$, each search is $O(\log N)$, each point enters and leaves $S$ once, so the time is $O(N \log N)$ and the space $O(N)$. The implementation uses a Python list with `bisect`, which is correct but moves $O(N)$ entries per insertion.

**Any $p$: slicing.** Sort by the last objective; between consecutive values of it the cross-section is the $(p-1)$-dimensional hypervolume of the points below. With the 3D sweep as the base, this gives $O(N^{p-2} \log N)$ time (Fonseca et al., 2006). The implementation uses this recursion for $p \ge 4$.

**Via Klee's measure problem.** Any algorithm for the union of boxes applies. The [Overmars and Yap](/overmars-yap-algorithm/) method gives $O(N^{p/2} \log N)$. Yildiz and Suri (2012) gave $O(N^{(p-1)/2} \log N)$ for boxes grounded in two coordinates, which covers the hypervolume. Chan (2013) gave $O(N^{p/3} \operatorname{polylog} N)$ for orthants, the best general bound known.

**Methods used in practice.** HSO, WFG and the box decomposition methods have worse worst-case bounds but are often fast on the fronts that arise in benchmarks; the survey of Guerreiro, Fonseca and Paquete (2021) compares them.

**Approximation.** Bringmann and Friedrich (2010) gave a fully polynomial randomized approximation scheme for the volume of a union of boxes: sample a box with probability proportional to its volume, sample a point in it, and count how often the sampled box is the first that contains the point. Plain Monte Carlo sampling in the bounding box has an additive error.

## Bounds

- **Lower bound.** For $p \ge 2$, $\Omega(N \log N)$ in the algebraic decision tree model (Beume et al., 2009). So the 2D and 3D sweeps are optimal in that model.
- **Upper bounds.** $O(N \log N)$ for $p \le 3$; $O(N^{p/3} \operatorname{polylog} N)$ in general (Chan, 2013).
- **Hardness.** Bringmann and Friedrich (2010) proved that computing the hypervolume is #P-hard when $p$ is part of the input. So no algorithm polynomial in both $N$ and $p$ exists unless every #P function is computable in polynomial time.
- **Approximation.** A $1 \pm \varepsilon$ approximation with high probability takes time polynomial in $N$, $p$ and $1/\varepsilon$ (Bringmann and Friedrich, 2010).

## Reductions

- **To Klee's measure problem.** The boxes $[a, r]$ for $a \in A$ form an instance whose union has volume $\mathrm{HV}(A; r)$. Every bound for Klee's problem holds here.
- **From a #P-complete counting problem.** The #P-hardness proof of Bringmann and Friedrich encodes a counting problem for Boolean formulas as the volume of a union of boxes that share a corner.
- **Contributions to hypervolumes.** All $N$ exclusive contributions take $N + 1$ hypervolume computations; for $p = 2$ they follow from the sorted staircase in $O(N \log N)$ time, as on the [hypervolume indicator](/hypervolume-indicator/) page.
- **Non-dominated points first.** Removing dominated points does not change the value; [Kung's algorithm](/kung-algorithm/) finds them in $O(N \log^{p-1} N)$ time, and for $p = 2, 3$ the sweep does it on the way.

## Applications

- **Quality indicator.** Benchmarks of [multi-objective evolutionary algorithms](/multi-objective-evolutionary-algorithm/) report the hypervolume of each output set.
- **Selection.** SMS-EMOA, MO-CMA-ES and HypE select by hypervolume contributions, so they compute many hypervolumes per generation; this cost limits them for large $p$.
- **Bayesian optimization.** The expected hypervolume improvement is an acquisition function whose evaluation uses the same box decompositions.
- **Archiving.** Bounded archives can keep the subset with the largest hypervolume, which needs subset selection or contributions.

## References
