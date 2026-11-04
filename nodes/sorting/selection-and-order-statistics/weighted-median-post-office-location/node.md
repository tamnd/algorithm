---
tag: JYC00C
kind: problem
slug: weighted-median-post-office-location
name: Weighted median and post-office location
aliases:
- Post-office location problem
area: sorting/selection-and-order-statistics
level: core
summary: Finding the weighted median of weighted numbers, which also solves the one dimensional and Manhattan distance post-office location problems.
model: comparison-model
complexity:
  vars: {n: the number of points}
  time: {worst: Θ(n)}
prereqs: [weighted-median, median-of-medians]
see_also: [weighted-median, median-finding, geometric-median, prune-and-search, deterministic-linear-selection, selection-problem, k-means, quantile]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 9, end-of-chapter problem "Weighted median" (the weighted median in O(n lg n) and in Θ(n) worst-case time, the one-dimensional post-office location problem, and the two-dimensional problem with the Manhattan distance)
  - paper: doi:10.1016/S0022-0000(73)80033-9
    title: Manuel Blum, Robert W. Floyd, Vaughan Pratt, Ronald L. Rivest and Robert E. Tarjan, Time bounds for selection, Journal of Computer and System Sciences 7(4) (1973)
    locator: pages 448 to 461 (the linear-time median used in each round)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.3, Minimum-comparison selection
---

The weighted median problem asks, for $n$ distinct numbers with positive weights, for a [weighted median](/weighted-median/): an item such that the items below it weigh less than half the total and the items above it weigh at most half. Sorting and a running sum solve it in $O(n \log n)$ time, and a recursion that finds the plain [median](/median/), keeps the side that holds the half-weight point and throws the rest away solves it in $\Theta(n)$ worst-case time. The weighted median is the best place for a facility on a line, the post-office location problem, and with the Manhattan distance in the plane the problem splits into one weighted median per coordinate.

## In plain words

Villages lie along a straight road, and each village has a number of people. You want to build one post office on the road so that the total walking distance of all people is as small as possible.

Stand anywhere and count the people on your left and on your right. If more people are on your right, moving right a little makes more people walk less than walk more, so you should move right. You stop at a place where neither side holds more than half of the people. That place is the weighted median.

Finding it does not need a sort. Take the middle village by position, add up the people on each side, and keep only the side where the balance point must be.

## Definition

**Weighted median.** The input is $n$ distinct numbers $x_1, \ldots, x_n$ with positive weights $w_1, \ldots, w_n$ and $\sum_i w_i = 1$. The output is the lower weighted median, the item $x_k$ with

$$ \sum_{x_i < x_k} w_i < \frac12 \quad \text{and} \quad \sum_{x_i > x_k} w_i \le \frac12. $$

This item is unique: it is the smallest $x_k$ such that the items at most $x_k$ weigh at least $1/2$. For other totals $W$, replace $1/2$ by $W/2$.

**Post-office location on a line.** The input is $n$ points $p_1, \ldots, p_n$ on the real line with weights $w_i > 0$. The output is a point $p$ that minimizes

$$ f(p) = \sum_{i=1}^{n} w_i \, |p - p_i|. $$

**Post-office location in the plane, Manhattan distance.** The points are $p_i = (x_i, y_i)$, and $p = (x, y)$ minimizes $\sum_i w_i \bigl(|x - x_i| + |y - y_i|\bigr)$.

## Variants

- **Equal weights.** With $w_i = 1/n$ the lower weighted median is the lower median, and the post office goes at the median point.
- **Weighted quantiles.** Replace $1/2$ by a fraction $\tau$: the smallest item whose prefix weight is at least $\tau$. The algorithm below solves this for each $\tau$.
- **Euclidean distance.** With $\sum_i w_i \lVert p - p_i \rVert_2$ the problem is the [geometric median](/geometric-median/), or Fermat-Weber problem; its optimum has no closed form in general, and it is solved by iterative methods.
- **Several facilities.** Placing $j$ facilities on a line to minimize the weighted distance of each point to its nearest facility is a dynamic programming problem; in the plane with squared distances it becomes [k-means](/k-means/).
- **Repeated items.** If items repeat, merge equal items by adding their weights.

## Examples

**On a line.** Points $1, 3, 4, 7, 9$ with weights $0.1, 0.3, 0.1, 0.2, 0.3$. The prefix weights in sorted order are $0.1, 0.4, 0.5, 0.7, 1.0$, so the lower weighted median is $4$, the first item whose prefix weight reaches $1/2$. The item $7$ is the upper weighted median. The cost $f(p)$ is $2.7$ for each $p$ in $[4, 7]$, $2.9$ at $p = 3$ and $3.1$ at $p = 8$.

**In the plane.** Points $(1, 5)$, $(4, 1)$, $(6, 6)$, $(3, 3)$, $(8, 2)$ with weights $2, 1, 3, 1, 1$, total $8$.

- The $x$-coordinates in order are $1, 3, 4, 6, 8$ with weights $2, 1, 1, 3, 1$ and prefix weights $2, 3, 4, 7, 8$. Each $x$ in $[4, 6]$ is optimal for the first sum.
- The $y$-coordinates in order are $1, 2, 3, 5, 6$ with weights $1, 1, 1, 2, 3$ and prefix weights $1, 2, 3, 5, 8$. The weighted median is $y = 5$, and it is the only optimum: the items below weigh $3 < 4$ and the items above weigh $3 < 4$.

So each point $(x, 5)$ with $4 \le x \le 6$ is an optimal post office, with total weighted Manhattan distance $29$. The point $(4, 4)$ costs $31$.

## Known algorithms

**Sort and sum, $O(n \log n)$.** Sort the items by value, then add the weights from the left until the sum reaches $1/2$. The item at which this happens is the lower weighted median.

**Linear time.** Let WSELECT$(S, \tau)$ return the smallest item $x$ of $S$ whose prefix weight $\sum_{y \in S, y \le x} w(y)$ is at least $\tau$, for $0 < \tau \le w(S)$.

```pseudo id=main
WSELECT(S, τ)                              ▷ 0 < τ ≤ w(S), items distinct
L1  if |S| = 1 then return the item of S
L2  m ← the lower median of S by value     ▷ by median of medians, O(|S|)
L3  L ← the items of S less than m;  G ← the items greater than m
L4  if w(L) ≥ τ then return WSELECT(L, τ)
L5  else if w(L) + w(m) ≥ τ then return m
L6  else return WSELECT(G, τ − w(L) − w(m))
```

The lower weighted median is WSELECT$(S, 1/2)$. *Correctness.* If $w(L) \ge \tau$, the answer has prefix weight at least $\tau$ inside $L$ already, and items of $L$ have the same prefix weight in $L$ as in $S$; so the answer is in $L$. If $w(L) < \tau \le w(L) + w(m)$, no item of $L$ reaches $\tau$ but $m$ does. Otherwise the answer is in $G$, and the prefix weight of an item of $G$ in $S$ is $w(L) + w(m)$ plus its prefix weight in $G$. *Time.* Line L2 takes $O(n)$ worst-case time by [median of medians](/median-of-medians/), lines L3 to L6 take $O(n)$ apart from the call, and $L$ and $G$ each have at most $\lfloor n/2 \rfloor$ items, so $T(n) \le T(\lfloor n/2 \rfloor) + O(n)$, which gives $T(n) = O(n)$. With [quickselect](/quickselect/) in line L2, or a random pivot in place of the median, the expected time is $O(n)$.

**The post office on a line.** Return the weighted median of the points with the normalized weights $w_i / W$. Since $f$ is convex and piecewise linear, with slope $W(\le p) - W(> p)$ just right of $p$, its minimum is at a point where the slope changes sign, which is the weighted median.

**Manhattan distance in the plane.** The cost $\sum_i w_i |x - x_i| + \sum_i w_i |y - y_i|$ is a sum of a function of $x$ alone and a function of $y$ alone, so it is minimized by the weighted median of the $x_i$ and the weighted median of the $y_i$, found independently in $O(n)$ time each. The same holds in $d$ dimensions with $d$ weighted medians.

## Bounds

- **Lower bound.** With equal weights the weighted median is the median, so each algorithm must solve [median finding](/median-finding/), and its lower bounds apply: $\Omega(n)$ time and at least $(2 + 2^{-80})n - o(n)$ comparisons in the worst case. The algorithm must also read each weight.
- **Upper bound.** The algorithm above is $O(n)$ in the worst case, so the problem takes $\Theta(n)$ time.

## Reductions

- **To selection.** Each round of WSELECT is one median selection and one pass. Weighted selection for a fraction $\tau$ is the weighted form of the [selection problem](/selection-problem/).
- **From median finding.** Give each item the weight $1/n$.
- **Post office to weighted median.** On a line directly, and with the Manhattan distance in $d$ dimensions by $d$ weighted medians.

## Applications

- **Facility location.** Placing a depot, a meeting point or a server on a line or in a city with a grid of streets, so as to minimize the weighted travel distance.
- **Robust regression.** Least absolute deviation fits are weighted median problems in one parameter, and weighted medians appear in the steps of algorithms for $L_1$ regression.
- **Prune and search.** Weighted median finding is a step of some [prune and search](/prune-and-search/) algorithms, which use it to drop a fixed fraction of the input weight in each round.
- **Statistics.** Weighted medians summarize survey data with sampling weights.

## References
