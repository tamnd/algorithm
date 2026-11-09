---
tag: KB59FK
kind: technique
slug: crowding-distance
name: Crowding distance
aliases:
- crowding distance assignment
- crowded comparison operator
area: optimization/multi-objective
level: core
summary: Estimate how crowded each point of a front is by the normalized side lengths of the box between its neighbors in each objective. NSGA-II keeps the less crowded points. O(p N log N) time.
prereqs: [non-dominated-sorting, pareto-front]
see_also: [nsga-ii, pareto-ranking, spea2, nsga-iii, spread-indicator, hypervolume-indicator, multi-objective-evolutionary-algorithm]
sources:
  - paper: doi:10.1109/4235.996017
    title: Kalyanmoy Deb, Amrit Pratap, Sameer Agarwal and T. Meyarivan, A fast and elitist multiobjective genetic algorithm, NSGA-II, IEEE Transactions on Evolutionary Computation 6(2), 2002, 182-197
    locator: Section III-B, density estimation, the crowding distance assignment and the crowded comparison operator
  - book: isbn:9780471873396
    title: Kalyanmoy Deb, Multi-Objective Optimization Using Evolutionary Algorithms, Wiley, 2001
    locator: Chapter 6, the elitist non-dominated sorting genetic algorithm and its crowding distance
  - paper: "Saku Kukkonen and Kalyanmoy Deb, Improved pruning of non-dominated solutions based on crowding distance for bi-objective optimization problems, Proceedings of the IEEE Congress on Evolutionary Computation, 2006, 1179-1186"
    locator: removal of one solution at a time with a new crowding distance after each removal
  - paper: "Saku Kukkonen and Kalyanmoy Deb, A fast and effective method for pruning of non-dominated solutions in many-objective problems, Parallel Problem Solving from Nature IX, LNCS 4193, Springer, 2006, 553-562"
    locator: the weakness of the crowding distance for three or more objectives and a nearest neighbor replacement
---

The crowding distance is a density estimate for the points of one front: for each objective, sort the front and add the normalized gap between the two neighbors of a point. The extreme points of each objective get an infinite distance. [NSGA-II](/nsga-ii/) uses it to break ties among points of the same [non-dominated front](/non-dominated-sorting/): a larger distance means a less crowded point, and selection keeps it. For a front of $N$ points with $p$ objectives it takes $O(p N \log N)$ time, from $p$ sorts.

## In plain words

A front is a set of trade-offs, and we want them spread out, not bunched in one place. To see how lonely a point is, look at its two neighbors when the front is sorted by the first cost. Measure the gap between them. Do the same for each other cost, and add the gaps. Scale each gap by the full width of the front in that cost, so that a cost in meters and a cost in dollars count the same.

A point in a big gap gets a large value. A point squeezed between close neighbors gets a small value. The two end points of each sort have only one neighbor, so they get an infinite value, and the method always keeps them. When there are too many points, keep the ones with the largest values.

## When it applies

**Convention.** All objectives are minimized, $p$ is the number of objectives, $N$ is the population size, and $y = f(x)$ is the image of $x$.

Use the crowding distance when:

- the points to compare are already tied on a dominance rank, as inside one front of [Pareto ranking](/pareto-ranking/);
- the method must cut a front to a fixed size, as in the survivor selection of NSGA-II;
- there are two or three objectives, where the neighbors in each sort are close in the objective space;
- the cost must stay small. It needs no parameter, unlike fitness sharing, which needs a niche radius.

## The template

The input is one front $Y[1 \ldots l]$, a list of $l$ objective vectors. The output is the distance $d[i]$ of each point.

```pseudo id=main
CROWDING-DISTANCE(Y[1 .. l])
L1  for i ← 1 to l do d[i] ← 0
L2  for m ← 1 to p do
L3      sort the indices by Y[·]_m into I[1 .. l]
L4      d[I[1]] ← ∞, d[I[l]] ← ∞                         ▷ the extremes of objective m
L5      if Y[I[l]]_m = Y[I[1]]_m then skip to the next m   ▷ hole: a front flat in objective m
L6      for k ← 2 to l − 1 do
L7          d[I[k]] ← d[I[k]] + (Y[I[k+1]]_m − Y[I[k−1]]_m) / (Y[I[l]]_m − Y[I[1]]_m)
L8  return d
```

Line L7 normalizes by the range of objective $m$ on the front, so the objectives have equal weight. Deb et al. write the range as $f_m^{\max} - f_m^{\min}$; line L5 is a guard for a zero range, which the paper does not treat. The hole of line L5 is the choice for that case: skip the objective, as here, or use a fixed range given by the user.

**The crowded comparison.** NSGA-II orders two points $i$ and $j$ by $i \prec_n j$ when $\mathrm{rank}(i) < \mathrm{rank}(j)$, or when the ranks are equal and $d[i] > d[j]$. Its binary tournament and its survivor selection both use this order.

**Two objectives.** Let the front have $l \ge 3$ distinct, mutually non-dominated points with $p = 2$. Sort them by $y_1$. Two of them with $a_1 < b_1$ must have $a_2 > b_2$, or $a$ would dominate $b$. So the order by $y_2$ is the reverse of the order by $y_1$, and the two neighbors of a point are the same in both sorts. Let $a$ and $b$ be the neighbors of an inner point, with $a_1 < b_1$. Then

$$d = \frac{b_1 - a_1}{R_1} + \frac{a_2 - b_2}{R_2},$$

where $R_1, R_2$ are the ranges of the front. This is half the perimeter of the box with corners $a$ and $b$, after the scaling. For $p \ge 3$ the neighbors differ from one objective to the next, and the sum is no longer the size of one box.

**Cost.** Each objective needs one sort, $O(l \log l)$, and one scan, $O(l)$. The total is $O(p\, l \log l)$ time and $O(l)$ extra space. In NSGA-II the fronts of one generation have $2N$ points in total, so this step costs $O(p N \log N)$, which is less than the $O(p N^2)$ of the sort into fronts.

### A worked example

Take the first front $A = (1, 8)$, $B = (2, 5)$, $D = (4, 2)$, $G = (7, 1)$ from the [non-dominated sorting](/non-dominated-sorting/) page. The ranges are $R_1 = 7 - 1 = 6$ and $R_2 = 8 - 1 = 7$.

| point | gap in $y_1$ | gap in $y_2$ | crowding distance |
|---|---|---|---|
| A (1, 8) | end | end | $\infty$ |
| B (2, 5) | $(4 - 1)/6 = 1/2$ | $(8 - 2)/7 = 6/7$ | $19/14 \approx 1.357$ |
| D (4, 2) | $(7 - 2)/6 = 5/6$ | $(5 - 1)/7 = 4/7$ | $59/42 \approx 1.405$ |
| G (7, 1) | end | end | $\infty$ |

If NSGA-II must keep three of these four points, it keeps $A$, $G$ and $D$, and drops $B$.

## Classic examples

- **[NSGA-II](/nsga-ii/).** The crowding distance breaks ties in the binary tournament and cuts the last front that fits in the next population. This is the use for which Deb et al. defined it.
- **[Pareto ranking](/pareto-ranking/) with a density term.** Any rank rule leaves the points of a front tied, and the crowding distance is one choice for the density hole of the template.
- **Archive truncation.** Bounded archives of multi-objective particle swarm and differential evolution methods often drop the archive member with the smallest crowding distance.
- **Comparison with [SPEA2](/spea2/) and [NSGA-III](/nsga-iii/).** SPEA2 uses the distance to the $k$-th nearest neighbor, and NSGA-III counts the members near each reference direction. Both replace the crowding distance where it is weak.

## Variations

- **Recompute after each removal.** NSGA-II removes all surplus points in one pass. Kukkonen and Deb (2006) remove the most crowded point, recompute the distances of the rest, and repeat. On the front $(0, 10)$, $(1, 8)$, $(5, 7)$, $(6, 6)$, $(8, 3)$, $(10, 0)$ the distances of the four inner points are $4/5$, $7/10$, $7/10$ and $1$. To keep four points, the one-pass rule drops both $(5, 7)$ and $(6, 6)$ and leaves a gap from $(1, 8)$ to $(8, 3)$. The rule with recomputation drops $(6, 6)$, then gives $(5, 7)$ the new distance $6/5$, and drops $(1, 8)$ instead; it keeps $(0, 10)$, $(5, 7)$, $(8, 3)$ and $(10, 0)$.
- **Normalization.** Some codes divide by the range of the whole population or by fixed bounds, not by the range of the front. This changes the values when the fronts have different widths.
- **Nearest neighbor distances.** For $p \ge 3$, Kukkonen and Deb (2006) replace the sum of gaps with a product of distances to the nearest neighbors. SPEA2 uses the $k$-th nearest neighbor.

## Pitfalls

- **Copies of a point.** Two equal points do not get distance zero. On the front $(0, 4)$, $(1, 3)$, $(1, 3)$, $(4, 0)$ each copy of $(1, 3)$ gets $1$, half of the $2$ that a single $(1, 3)$ would get. So copies can survive in place of a distinct point. Remove copies before the truncation, or give them a distance of zero.
- **A zero range.** If all points of the front have the same value in objective $m$, line L7 divides by zero. Line L5 skips that objective. Which points get $\infty$ in line L4 then depends on how the sort breaks ties.
- **Comparing distances across fronts.** The values are normalized inside one front. A distance in front 1 and a distance in front 2 are not on the same scale. Compare them only for points of equal rank.
- **Many objectives.** For $p \ge 3$ the neighbors in each sort can be far apart in the space, and the sum of gaps is a poor density estimate. Kukkonen and Deb report this weakness in their experiments with three and more objectives.
- **Infinite values in arithmetic.** Code that adds to $\infty$ or sorts by $-d$ must keep $\infty$ as the largest value. With integer types, use a separate flag for the extremes.

## Exercises

1. Show that with the one-pass rule and $p = 2$, the two extreme points of a front of distinct, mutually non-dominated points always survive when at least two points are kept. *Answer:* they are the only points with $d = \infty$, because the order by $y_2$ is the reverse of the order by $y_1$.
2. Prove that at most $2p$ points of a front get $d = \infty$, and give a front with $p = 3$ where six points out of six get $\infty$, so that the distance does not rank them at all. *Answer:* line L4 sets two values for each objective. The front $(0, 5, 7)$, $(1, 3, 8)$, $(2, 8, 2)$, $(5, 7, 0)$, $(7, 1, 4)$, $(9, 2, 1)$ has the sum $12$ in each point, so no point dominates another, and each point is the smallest or the largest in one objective.
3. Prove that scaling objective $m$ by a positive constant does not change any crowding distance.

## References
