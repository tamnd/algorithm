---
tag: Q1RH1S
kind: algorithm
slug: greedy-fractional-knapsack
name: Greedy algorithm for fractional knapsack
aliases:
- ratio greedy knapsack
- Dantzig's greedy for the knapsack relaxation
area: optimization/combinatorial-optimization
level: intro
summary: Take items in decreasing value-to-weight ratio, splitting the last one.
solves: [fractional-knapsack]
model: word-ram
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1957
  people: [George B. Dantzig]
  note: Dantzig solved the linear relaxation of the knapsack problem by the ratio order in 1957.
prereqs: [fractional-knapsack, greedy-algorithm, weak-duality]
see_also: [fractional-knapsack, knapsack-problem, knapsack-dynamic-programming, knapsack-branch-and-bound, lp-relaxation, exchange-argument, weighted-median, matroid-greedy-algorithm]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 15.2, Elements of the greedy strategy (the fractional knapsack problem and its greedy solution)
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, Theory and Algorithms, sixth edition, Springer, 2018
    locator: Chapter 17, The Knapsack Problem (fractional knapsack in linear time with the weighted median)
  - book: isbn:9780471924203
    title: Silvano Martello and Paolo Toth, Knapsack Problems, Algorithms and Computer Implementations, Wiley, 1990
    locator: Chapter 2, 0-1 knapsack problem (the continuous relaxation, the critical item and the Dantzig upper bound)
  - paper: doi:10.1287/opre.5.2.266
    title: George B. Dantzig, Discrete-variable extremum problems, Operations Research 5(2), 266 to 288, 1957
    locator: the knapsack problem and the solution of its linear relaxation by the ratio order
  - paper: doi:10.1287/opre.28.5.1130
    title: Egon Balas and Eitan Zemel, An algorithm for large zero-one knapsack problems, Operations Research 28(5), 1130 to 1154, 1980
    locator: the linear-time computation of the critical item
---

The ratio greedy solves the [fractional knapsack problem](/fractional-knapsack/) exactly: sort the items by value per unit of weight, take them whole while they fit, and take the fitting part of the first item that does not fit. It runs in $\Theta(n \log n)$ time for the sort, or $O(n)$ with a [weighted median](/weighted-median/). Its value is the [LP relaxation](/lp-relaxation/) bound of the 0-1 [knapsack problem](/knapsack-problem/), the bound that [branch and bound](/knapsack-branch-and-bound/) uses, but the same rule without the split is not exact for the 0-1 problem.

## In plain words

You fill a bag with goods that you can cut, such as grain, sugar and salt. Each good has a price per kilogram. The best plan is easy: first take all of the most expensive good per kilogram, then all of the next one, and so on. When the next good does not fit completely, take as much of it as fits, and stop.

This works because every kilogram of space should hold the most valuable kilogram that is still left. If a plan uses space for a cheaper good while some of a more valuable one is left behind, you can swap a little of the one for the other and gain. The rule fails when goods cannot be cut, because then a light good with a good price can block a heavy good that is worth more in total.

## The problem

The input is $n$ items with weights $w_i > 0$ and values $v_i \ge 0$, and a capacity $W \ge 0$. The output is a vector $x \in [0,1]^n$ that maximizes $\sum_i v_i x_i$ subject to $\sum_i w_i x_i \le W$. This is the [fractional knapsack problem](/fractional-knapsack/), the linear relaxation of the 0-1 [knapsack problem](/knapsack-problem/):

$$ \max \sum_{i=1}^n v_i x_i \quad \text{subject to} \quad \sum_{i=1}^n w_i x_i \le W, \quad 0 \le x_i \le 1. $$

## The algorithm

```pseudo id=main
GREEDY-FRACTIONAL-KNAPSACK(w[1 .. n], v[1 .. n], W)
L1  sort the items so that v[1]/w[1] ≥ v[2]/w[2] ≥ … ≥ v[n]/w[n]
L2  r ← W, x[1 .. n] ← 0, total ← 0            ▷ r is the free capacity
L3  for i ← 1 to n do
L4      if w[i] ≤ r then
L5          x[i] ← 1, r ← r − w[i], total ← total + v[i]
L6      else
L7          x[i] ← r / w[i], total ← total + v[i] · x[i]
L8          return total, x                        ▷ i is the critical item
L9  return total, x                            ▷ all items fit
```

Line L1 fixes the order. The loop of lines L3 to L5 takes whole items while they fit. The first item that does not fit is the *critical item* $k$. Line L7 fills the rest of the capacity with a part of it, and line L8 stops, because the bag is now full. If no item is critical, all items fit and line L9 returns $x = (1, \ldots, 1)$. Ties in the ratio may be broken in any way; the total does not change.

## Example

Take $W = 10$, $w = (5, 4, 6, 3)$ and $v = (10, 40, 30, 50)$. The ratios are $2$, $10$, $5$ and $50/3 \approx 16.7$, so the order is items 4, 2, 3, 1.

| step | item | $w_i$ | $v_i$ | ratio | $r$ before | action | $x_i$ | total after |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 4 | 3 | 50 | 16.7 | 10 | take whole | 1 | 50 |
| 2 | 2 | 4 | 40 | 10 | 7 | take whole | 1 | 90 |
| 3 | 3 | 6 | 30 | 5 | 3 | critical, take 3/6 | 1/2 | 105 |

Item 1 is not examined, and $x = (0, 1, 1/2, 1)$ with value 105. The 0-1 optimum of the same instance is 90, so the relaxation bound is 105 against an integer optimum of 90.

A certificate of optimality: take $\lambda = 5$, the ratio of the critical item, and $\mu_i = v_i - \lambda w_i$ for the whole items, so $\mu_4 = 35$, $\mu_2 = 20$, $\mu_1 = \mu_3 = 0$. Then $\lambda w_i + \mu_i \ge v_i$ for every item, and $\lambda W + \sum_i \mu_i = 50 + 35 + 20 = 105$. By [weak duality](/weak-duality/) no feasible $x$ has a value above 105.

## Correctness

The output is feasible: lines L5 and L7 never use more than the free capacity $r$, so $\sum_i w_i x_i \le W$, and each $x_i$ is in $[0, 1]$ because line L7 runs only when $r < w_i$. For optimality, the proof builds a dual solution of the linear program with the same value. With $\lambda$ the ratio of the critical item (or 0 if there is none) and $\mu_i = \max(0, v_i - \lambda w_i)$, the dual constraints $\lambda w_i + \mu_i \ge v_i$ hold because the items before $k$ have a ratio of at least $\lambda$ and the items after $k$ have a ratio of at most $\lambda$, and the dual value equals the greedy total. The full proof, with an exchange argument as a second proof, is in the proof file below.

## Complexity

- **Sort.** Line L1 sorts $n$ ratios in $\Theta(n \log n)$ comparisons in the worst case with a [merge sort](/merge-sort/) or a heap sort. Compare $v_i / w_i$ with $v_j / w_j$ as $v_i w_j$ against $v_j w_i$, so each comparison is exact on integers.
- **Scan.** Lines L2 to L9 take $O(n)$ time.
- **Total.** $\Theta(n \log n)$ in each case for a [comparison sort](/comparison-sort-lower-bound/), and $\Theta(n)$ extra space for the order and for $x$.
- **Linear time.** The scan needs only the critical item and the set of items with a larger ratio. A [weighted median](/weighted-median/) of the ratios, with the weights $w_i$, finds them in $O(n)$ worst-case time by linear-time [selection](/median-of-medians/): pick the median ratio, compare the total weight of the items above it with $W$, and recurse into one half. Balas and Zemel (1980) used this to solve large instances. Korte and Vygen give the method in Chapter 17.

## Properties

- **Exact for the fractional problem**, by the dual certificate.
- **At most one fractional item.** Every $x_i$ is 0 or 1 except possibly $x_k$. This is a basic solution of the linear program, with one constraint and so at most one basic variable strictly between its bounds.
- **Value = Dantzig bound.** For the 0-1 problem, the total is an upper bound $U$ with $f^* \le U$, and the whole items before $k$ give a lower bound. So $f^* \in [\sum_{i<k} v_i, \ U]$.
- **Greedy, with no look-back.** Each decision is final. The order does not depend on $W$, so one sort answers all capacities: the optimal value as a function of $W$ is concave and piecewise linear, with slopes equal to the ratios in decreasing order.

## Variants and improvements

- **Greedy for the 0-1 problem, repaired.** First remove the items with $w_i > W$. Take the whole items $1, \ldots, k-1$ and compare with the best single item. The better one has value at least $f^*/2$, because $f^* \le U \le \sum_{i<k} v_i + v_k$ and $v_k$ is at most the best single item. Without the comparison the ratio greedy can be arbitrarily bad.
- **Critical item without sorting.** As above, $O(n)$ by weighted median selection. The "core" algorithms for the 0-1 problem sort only the items with ratios near that of the critical item.
- **Several constraints.** With two or more knapsack constraints the relaxation is a general linear program, and no ratio order solves it.
- **Matroid view.** The greedy rule for whole items is exact on a [matroid](/matroid/) ([matroid greedy algorithm](/matroid-greedy-algorithm/)), but the sets of items that fit in a knapsack do not form a matroid, which is another way to see why the 0-1 version fails.

## When to use it

Use it when the items are divisible: bulk goods, bandwidth, time on a machine. Use it as the bound inside a [branch and bound](/knapsack-branch-and-bound/) search for the 0-1 problem, where it is cheap and often tight. For the 0-1 problem itself, use [dynamic programming](/knapsack-dynamic-programming/) when the capacity is small, the [FPTAS](/knapsack-fptas/) for a guaranteed approximation, or the repaired greedy for a quick factor of 2.

## Pitfalls

- **Floating-point ratios.** Sorting by the float $v_i / w_i$ can put two items in the wrong order when their ratios differ in the last bits. In line L1 compare $v_i w_j$ with $v_j w_i$ in integers.
- **Zero weights.** The ratio $v_i / 0$ is not defined. Take items with $w_i = 0$ first and whole, before line L1, or reject them.
- **Using it for the 0-1 problem.** With $W = 100$, $w = (1, 100)$ and $v = (2, 100)$, the ratio order takes item 1, and the item of value 100 no longer fits whole. Line L7 then takes 99/100 of it for a fractional total of 101, but a 0-1 version that skips line L7 gets only 2 against $f^* = 100$.
- **Continuing after the critical item.** Line L7 uses all of the free capacity but does not set $r$ to 0. Code that keeps scanning after line L7 still sees the old $r$ and can take more items, which goes over the capacity. Stop at line L8.
- **Sorting by value or by weight alone.** Neither order is correct. On the example, the order by value takes item 4 and then item 2 and gives 105 by chance, but on $w = (10, 1)$, $v = (10, 9)$ and $W = 10$, the order by value gives 10 and the ratio order gives $9 + 9/10 \cdot 10 = 18$.

## Implementations

## History

Dantzig (1957) described the knapsack problem and solved its linear relaxation by taking the items in the order of their ratios, with the first item that does not fit split. The value of this solution is still called the Dantzig bound. Balas and Zemel (1980) found the critical item in linear time without sorting, and used it to solve large 0-1 instances.

## References
