---
tag: C2SGBR
kind: technique
slug: prune-and-search
name: Prune and search
aliases:
- Megiddo's prune-and-search
- prune-and-search technique
- Megiddo-Dyer technique
area: geometry/geometric-optimization
level: advanced
summary: Technique that discards a fixed fraction of the input in each round by deciding on which side of a median the optimum lies; a geometric series then gives linear time.
prereqs: [median-of-medians, linear-programming-problem, geometric-series]
see_also: [megiddo-fixed-dimension-lp, minimum-enclosing-circle, median-of-medians, kirkpatrick-seidel, clarksons-algorithm, parametric-search, lp-type-problem, weighted-median]
sources:
  - paper: doi:10.1137/0212052
    title: Nimrod Megiddo, Linear-time algorithms for linear programming in R^3 and related problems, SIAM Journal on Computing 12(4), 1983
    locator: the pruning of pairs of constraints about a median for linear programming in two and three variables, and the smallest enclosing circle in O(n) time
  - paper: doi:10.1145/2422.322418
    title: Nimrod Megiddo, Linear programming in linear time when the dimension is fixed, Journal of the ACM 31(1), 1984
    locator: multidimensional search and the O(2^(2^d) n) algorithm for linear programming in d variables
  - paper: "Martin E. Dyer, Linear time algorithms for two- and three-variable linear programs, SIAM Journal on Computing 13(1), 1984"
    locator: the independent linear-time algorithm for two and three variables by pruning pairs of constraints
  - paper: doi:10.1016/S0022-0000(73)80033-9
    title: Manuel Blum, Robert W. Floyd, Vaughan Pratt, Ronald L. Rivest and Robert E. Tarjan, Time bounds for selection, Journal of Computer and System Sciences 7(4), 1973
    locator: linear-time selection by the median of medians, the median step used in every pruning round
  - paper: "David G. Kirkpatrick and Raimund Seidel, The ultimate planar convex hull algorithm?, SIAM Journal on Computing 15(1), 1986"
    locator: finding the bridge of the upper hull over a vertical line by pruning pairs of points in linear time
---

Prune and search is a technique for optimization problems whose answer depends on only a few input objects. Each round pairs or groups the objects, takes the [median](/median-of-medians/) of a key computed from each group, and asks a decision oracle on which side of the median the optimum lies. That answer shows that a fixed fraction $\alpha$ of the objects cannot determine the optimum, and they are discarded. The rounds cost $O(n)$, $O((1 - \alpha) n)$, $O((1 - \alpha)^2 n)$ and so on, a [geometric series](/geometric-series/) that sums to $O(n)$. Megiddo (1983) and Dyer (1984) introduced it for [linear programming](/linear-programming-problem/) in two and three variables and for the [minimum enclosing circle](/minimum-enclosing-circle/), and Megiddo (1984) extended it to [linear programming in any fixed dimension](/megiddo-fixed-dimension-lp/). It is deterministic, and it gives linear time where sorting would give $O(n \log n)$.

## In plain words

You look for the lowest point of a valley formed by many straight lines, where the valley floor is the highest of the lines at each place. Most lines never touch the bottom. Pair the lines up. Each pair crosses at one place. Take the middle one of these crossing places and check which way the ground slopes there. Say the bottom lies to the right. For every pair that crosses to the left of that place, one line of the pair is lower than the other everywhere to the right, so it can never touch the bottom. Throw it away.

Half of the crossings lie on the wrong side, so a quarter of the lines go away in every round. Each round looks at fewer lines than the last, and the total work is only a few times the number of lines.

## When it applies

The technique needs four parts.

- **Few objects matter.** The optimum is determined by a bounded number of input objects, and the others can be removed without changing it. In [LP-type](/lp-type-problem/) terms, the problem has a small combinatorial dimension.
- **A cheap decision oracle.** Given a candidate value $t$ of a parameter (a coordinate, a radius), decide in $O(n)$ time whether the optimum is below, at or above $t$. The oracle may run on the remaining objects only.
- **Keys that pair objects.** For a group of $O(1)$ objects there is a key $x$ such that, once the optimum is known to be on one side of $x$, at least one object of the group is useless. For two lines the key is their crossing point.
- **A linear-time median.** The median of the keys is found by [linear-time selection](/median-of-medians/), so each round is $O(n)$ without sorting.

If each round discards at least $\alpha n$ objects, the time is $T(n) \le T((1 - \alpha) n) + c n$, so $T(n) \le c n / \alpha = O(n)$.

## The template

Notation: $S$ is the set of objects still in play, with $|S| = n$ at the start; $\alpha \in (0, 1)$ is the fraction discarded per round; $c_0$ is a constant size at which brute force is used. The model is the [real RAM](/real-ram/).

```pseudo id=main
PRUNE-AND-SEARCH(S)
L1  while |S| > c₀ do
L2      split S into groups of O(1) objects
L3      x_g ← KEY(g) for every group g with a key
L4      m ← the median of the keys x_g          ▷ linear-time selection
L5      side ← ORACLE(S, m)                       ▷ below, at or above m
L6      if side = at then return the optimum found at m
L7      for each group g with x_g on the far side of m (and x_g = m) do
L8          remove from S the objects of g that cannot be optimal on side
L9  return BRUTE-FORCE(S)
```

The holes are the grouping on L2, KEY on L3, the ORACLE on L5 and the rule of L8. Half of the keys are at or beyond the median on either side, so L8 runs for at least half of the groups. If each such group loses at least one of its $k$ objects, at least $n/(2k)$ objects go in each round, so $\alpha \ge 1/(2k)$.

**Why it is correct.** An object is removed only when the rule of L8 shows that it cannot attain the optimum on the side that holds the optimum, so the optimum of the remaining set equals the optimum of the original set. The loop ends because $|S|$ drops by a constant fraction in each round.

**Cost.** Round $i$ works on at most $(1 - \alpha)^i n$ objects, and L2 to L8 take time linear in that number, so the total is $c n \sum_{i \ge 0} (1 - \alpha)^i = c n / \alpha$.

### Example: the lowest point of an upper envelope

Find the minimum of $f(x) = \max_i (a_i x + b_i)$ over the lines $y = a_i x + b_i$; this is a linear program in two variables, minimize $y$ subject to $y \ge a_i x + b_i$. Pair the lines. For a pair with equal slopes, drop the lower line. Otherwise the key is the crossing point $x_g$. The oracle evaluates $f(m)$ and looks at the slopes of the lines that attain it: if they are all positive, the optimum is left of $m$; if all are negative, it is right of $m$; otherwise $m$ is optimal. Left of a crossing the line with the smaller slope is higher, and right of it the line with the larger slope is higher. So if the optimum is right of $m$, then for each pair with $x_g \le m$ the line with the smaller slope is below its partner on the whole range that matters and is dropped. At least $\lceil k/2 \rceil$ of $k$ pairs lose a line, a quarter of the lines.

Take the eight lines $(a, b)$ = $(-3, 0)$, $(-1, 2)$, $(-2, -1)$, $(1, -1)$, $(2, -4)$, $(3, -8)$, $(0, -2)$, $(4, -15)$, paired in this order, with $m$ the lower median of the keys.

| round | lines | keys of the pairs | $m$ | $f(m)$ and the slopes there | optimum is | dropped |
|---|---|---|---|---|---|---|
| 1 | 8 | $-1, 0, 13/4, 4$ | $0$ | $2$, slope $-1$ | right | $(-3, 0)$, $(-2, -1)$ |
| 2 | 6 | $3/2, 13/4, 4$ | $13/4$ | $5/2$, slope $2$ | left | $(4, -15)$, $(3, -8)$ |
| 3 | 4 | $1, 3/2$ | $1$ | $1$, slope $-1$ | right | $(0, -2)$ |
| 4 | 3 | $2$ | $2$ | $1$, slope $1$ | left | $(2, -4)$ |

The two lines left, $y = x - 1$ and $y = -x + 2$, cross at $(3/2, 1/2)$, the optimum of all eight lines.

## Classic examples

- **Selection.** The [median of medians](/median-of-medians/) algorithm is prune and search in one dimension: the median of group medians splits the input, a count decides on which side the $k$-th element lies, and at least $3n/10$ elements go.
- **Linear programming in two and three variables.** Megiddo (1983) and Dyer (1984) prune pairs of constraints as in the example. In three variables, the oracle is itself a two-variable linear program on a plane.
- **Linear programming in fixed dimension.** [Megiddo's algorithm](/megiddo-fixed-dimension-lp/) uses multidimensional search: to place many hyperplanes against the optimum, it asks a few oracle calls, each a linear program in one dimension less. The time is $O(2^{2^d} n)$; Dyer (1986) and Clarkson (1986) improved the constant to $3^{d^2}$.
- **[Minimum enclosing circle](/minimum-enclosing-circle/).** Megiddo (1983) pairs points, uses their perpendicular bisectors as the lines to place, and solves the constrained problem of the smallest circle with its center on a given line as the oracle. A constant fraction of the points (one sixteenth in Megiddo's count) is dropped in each round, which gives $O(n)$ time.
- **Bridges of the convex hull.** [Kirkpatrick and Seidel](/kirkpatrick-seidel/) find the edge of the upper hull above a vertical line by pairing points and pruning about the median slope, in $O(n)$ time; this gives their output-sensitive $O(n \log h)$ [convex hull](/convex-hull/) algorithm.
- **[Weighted median](/weighted-median/) and the 1-center on a line or a tree.** The same pattern solves location problems whose objective is a maximum or a sum of simple functions.

## Variations

- **Randomized pruning.** Take a random object or a random key instead of the median. Each round discards a constant fraction in expectation, which is simpler and gives the same expected bound; this is the step of [quickselect](/quickselect/).
- **Random sampling.** Instead of pruning a fixed fraction, solve a random sample and keep only the violators, as in [Clarkson's algorithm](/clarksons-algorithm/), or prune by a recursive randomized order as in [Seidel's algorithm](/seidel-linear-programming/). These have a smaller dependence on the dimension.
- **[Parametric search](/parametric-search/).** When the keys are not available, simulate a parallel decision algorithm at the unknown optimum; Megiddo's multidimensional search is related in spirit.
- **Derandomized sampling.** Deterministic $\varepsilon$-approximations replace the median and give deterministic linear time for many [LP-type problems](/lp-type-problem/).

## Pitfalls

- **Ties at the median.** A key equal to $m$ must be handled: either the oracle reports that $m$ is optimal, or the groups with $x_g = m$ are treated as on the far side. Otherwise the fraction of pruned groups can drop below one half.
- **Keys that do not exist.** Parallel lines have no crossing point. Settle such pairs at once (drop the lower one), or the count of keys in the median step is wrong.
- **An oracle on the full set.** The oracle must run on the remaining set only, or in time $O(|S|)$, or each round costs $O(n)$ and the total becomes $O(n \log n)$.
- **Sorting the keys.** Sorting instead of selection costs $O(n \log n)$ per round. Use linear-time selection, or a random key.
- **Large constants.** The fraction $\alpha$ can be small (one sixteenth for the circle, far less in higher dimension), so for small inputs a randomized incremental algorithm such as [Welzl's](/welzls-algorithm/) is faster in practice.

## Exercises

1. Show that $T(n) \le T(\lceil 3n/4 \rceil) + cn$ for $n > 2$ and $T(2) = c$ give $T(n) \le 4cn + O(1)$.
2. In the example, prove that the oracle rule is right: if all lines attaining $f(m)$ have positive slope, every minimizer of $f$ is less than $m$.
3. Give a prune and search algorithm for the smallest circle that contains $n$ points and has its center on the $x$-axis. What are the keys, and what is the oracle?
4. Show that the median of medians with groups of five discards at least $3n/10 - 6$ elements, and explain why groups of three do not give linear time.
5. Modify the example to maximize $\min_i (a_i x + b_i)$, and to detect that the problem is unbounded.

## References
