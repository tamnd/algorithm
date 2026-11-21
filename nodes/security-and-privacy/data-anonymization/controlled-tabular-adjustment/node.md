---
tag: P26HSK
kind: algorithm
slug: controlled-tabular-adjustment
name: Controlled tabular adjustment
aliases:
- CTA
area: security-and-privacy/data-anonymization
level: advanced
summary: Moves each sensitive cell out of its protection interval and fixes the other cells by a linear program that keeps the totals.
model: real-ram
complexity:
  vars: {n: the number of cells, m: the number of table relations, p: the number of sensitive cells, L: the time of one linear program with m rows and 2n columns}
  time: {worst: O(2^p L)}
  space: {extra: O(m (n + m))}
history:
  year: 2002
  people: [Ramesh A. Dandekar, Lawrence H. Cox]
  note: "Dandekar and Cox proposed the method in 2002 as an alternative to cell suppression. Castro (2006) studied the L1 and L2 forms for large tables."
prereqs: [cell-suppression-problem, linear-programming-problem, simplex-method]
see_also: [mixed-integer-programming, lp-duality, interior-point-method, branch-and-cut, post-randomization-method, data-swapping, differential-privacy-definition]
sources:
  - paper: doi:10.1016/j.ejor.2004.08.034
    title: "Jordi Castro, Minimum-distance controlled perturbation methods for large-scale tabular data protection, European Journal of Operational Research 171(1), 2006"
    locator: "pp. 39 to 52, minimum-distance adjustment of tables with the L1 and L2 distances, for large tables"
  - paper: "Ramesh A. Dandekar and Lawrence H. Cox, Synthetic tabular data, an alternative to complementary cell suppression, manuscript, Energy Information Administration, 2002"
    locator: the first statement of the method
  - book: isbn:9781119978152
    title: "Anco Hundepool, Josep Domingo-Ferrer, Luisa Franconi, Sarah Giessing, Eric Schulte Nordholt, Keith Spicer and Peter-Paul de Wolf, Statistical Disclosure Control, Wiley, 2012"
    locator: "Chapter 4, Magnitude tabular data, pp. 131 to 182, sensitivity rules and protection levels"
  - paper: doi:10.1080/01621459.1980.10477481
    title: "Lawrence H. Cox, Suppression methodology and statistical disclosure control, Journal of the American Statistical Association 75(370), 1980"
    locator: "pp. 377 to 385, protection of sensitive cells in tables with totals"
  - paper: doi:10.1287/moor.2.2.103
    title: "Robert G. Bland, New finite pivoting rules for the simplex method, Mathematics of Operations Research 2(2), 1977"
    locator: "pp. 103 to 107, the least-index rule and the proof that the simplex method then terminates"
---

Controlled tabular adjustment (CTA) protects a table of magnitudes with totals by changing numbers instead of hiding them. Each sensitive cell is moved up by at least its upper protection level or down by at least its lower protection level. The other cells are then changed as little as possible, so that every total still equals the sum of its parts and every cell stays within its bounds. For a fixed choice of directions, this is a [linear program](/linear-programming-problem/) that minimizes the weighted L1 distance to the true table. The exact method tries both directions for each of the $p$ sensitive cells, so it solves $2^p$ linear programs and keeps the cheapest. Unlike [cell suppression](/cell-suppression-problem/), CTA publishes every cell, but some published values are not the true ones.

## In plain words

A table shows sales by town and kind of shop, with sums for each row and each column. One number is secret, because it belongs to only two shops. Hiding it does not work well, because the sums give it back, and hiding more numbers loses a lot.

CTA prints all the numbers, but it prints a wrong value for the secret one: clearly higher or clearly lower than the true value. Then the sums do not add up. So it changes a few other numbers by small amounts until every sum is right again. It picks the changes that are as small as possible in total. A reader sees a normal table where every sum is right, but cannot know the true secret value.

## The problem

The input is a table of $n$ cells with values $a_1, \ldots, a_n$ that satisfy linear relations $M a = 0$, for example that a total minus its parts is 0. The totals are cells too. Each cell has bounds $lb_i \le a_i \le ub_i$, such as $0 \le a_i$. A set $P$ of $p$ sensitive cells is given, and each $p \in P$ has a lower and an upper protection level $LPL_p, UPL_p \ge 0$. The levels come from a sensitivity rule, as in [cell suppression](/cell-suppression-problem/), and they are policy choices. Each cell has a weight $w_i \ge 0$, such as 1, or $1 / a_i$ for a relative change.

The output is a table $x = a + y$ that satisfies $M x = 0$ and $lb \le x \le ub$, protects every sensitive cell, so that $x_p \ge a_p + UPL_p$ or $x_p \le a_p - LPL_p$, and has the least cost $\sum_i w_i |y_i|$. The "or" is what makes the problem hard: the set of protected tables is not convex. With a binary variable for each sensitive cell, it is a [mixed-integer program](/mixed-integer-programming/).

## The algorithm

Write $y = z^+ - z^-$ with $z^+, z^- \ge 0$, the moves up and down. For a fixed direction of each sensitive cell, the "or" goes away, and what is left is a linear program.

```pseudo id=main
CTA(a, M, lb, ub, w, P, LPL, UPL)
L1  best ← none
L2  for each direction vector d in {down, up}^P do
L3      bounds: 0 ≤ z+ ≤ ub - a and 0 ≤ z- ≤ a - lb
L4      for each p in P: if d_p = up then z+_p ≥ UPL_p and z-_p = 0, else z-_p ≥ LPL_p and z+_p = 0
L5      solve the LP: minimize Σ w_i (z+_i + z-_i) subject to M (z+ - z-) = 0 and the bounds
L6      if the LP is feasible and its value is less than that of best then best ← (a + z+ - z-, value, d)
L7  if best is none then return infeasible
L8  return best
```

Line L5 can use any LP solver. The implementation uses the [simplex method](/simplex-method/) with bounds on the variables and Bland's least-index rule, with exact fractions when all the inputs are rational. On a tie at line L6, the first direction vector in the order of line L2 is kept.

## Example

Take the table with three rows and three columns and its totals, 16 cells in all, with weight 1 for each cell and the bounds $x \ge 0$. Two cells are sensitive: (r2, c1) = 5 with $LPL = UPL = 3$, and (r3, c3) = 10 with $LPL = UPL = 2$.

| | c1 | c2 | c3 | total |
|---|---|---|---|---|
| r1 | 20 | 10 | 15 | 45 |
| r2 | **5** | 25 | 30 | 60 |
| r3 | 12 | 18 | **10** | 40 |
| total | 37 | 53 | 55 | 145 |

The four direction vectors give these optimal costs:

| (r2, c1) | (r3, c3) | least cost |
|---|---|---|
| down | down | 12 |
| down | up | 16 |
| up | down | 16 |
| up | up | 12 |

Two vectors tie at 12, and line L6 keeps the first, down and down. Its adjustment is

| | c1 | c2 | c3 | total |
|---|---|---|---|---|
| r1 | +1 | -1 | 0 | 0 |
| r2 | **-3** | +1 | +2 | 0 |
| r3 | +2 | 0 | **-2** | 0 |
| total | 0 | 0 | 0 | 0 |

and the published table is

| | c1 | c2 | c3 | total |
|---|---|---|---|---|
| r1 | 21 | 9 | 15 | 45 |
| r2 | 2 | 26 | 32 | 60 |
| r3 | 14 | 18 | 8 | 40 |
| total | 37 | 53 | 55 | 145 |

Check each sum: row r2 is $2 + 26 + 32 = 60$, column c1 is $21 + 2 + 14 = 37$, and column c3 is $15 + 32 + 8 = 55$. No total moved. The sensitive cells are at $2 = 5 - 3$ and $8 = 10 - 2$. The cost is $1 + 1 + 3 + 1 + 2 + 2 + 2 = 12$. Protecting (r2, c1) alone also costs 12: the move of $-2$ at (r3, c3) comes free with the moves that balance column c1 and row r3. The test file checks all these numbers with exact fractions.

## Correctness

For a fixed direction vector $d$, every feasible point of the LP gives a table that satisfies the relations and the bounds and moves each sensitive cell in its direction by at least its level, with a cost of at most the LP value. Every such table also gives an LP point of equal value, by splitting each change into its positive and negative part. So the LP optimum is the least cost among the tables with directions $d$. Every protected table has some direction vector, so the best of the $2^p$ optima is the optimum of the whole problem, and if no LP is feasible, no protected table exists. The simplex method with Bland's rule always ends, so each LP is solved. The full proof is in proofs/correctness.md.

## Complexity

Let $n$ be the number of cells, $m$ the number of relations and $p$ the number of sensitive cells. The model is the [real RAM](/real-ram/).

- The exact method solves $2^p$ linear programs, each with $m$ rows and $2n$ columns. So the time is $O(2^p L)$, where $L$ is the time of one LP.
- An LP can be solved in time polynomial in its size by an [interior-point method](/interior-point-method/). The simplex method of the implementation takes $O(m (n + m))$ operations per pivot, and its number of pivots is exponential in the worst case.
- The extra space is the simplex tableau, $O(m (n + m))$.

The factor $2^p$ is the price of exactness. With one LP for a good choice of directions, CTA scales to large tables.

## Properties

- **Relations hold.** Every relation holds in the published table, by the constraint $M y = 0$. This is a theorem. A total cell can still change. To keep a total at its true value, set its bounds to $lb_i = ub_i = a_i$.
- **All cells are published.** No cell is blank. Analysts can use the table as it is, but some values are wrong by design.
- **Protection is by the published value.** Each sensitive value is at least its level away from the truth. This is a theorem about the published value only. What a reader can infer depends on what the agency publishes about the method.
- **Optimal over all directions.** The exact method finds the least weighted L1 distance. This is a theorem. A fixed rule for the directions gives a feasible table, if one exists for those directions, and an upper bound on the optimum.
- **Loss by measurement.** The quality of the table for analysts, such as changes in correlations, is a measured property on test data.

## Variants and improvements

- **The mixed-integer form.** Instead of the $2^p$ loop, use one binary variable for the direction of each sensitive cell and solve one [mixed-integer program](/mixed-integer-programming/) by [branch-and-cut](/branch-and-cut/). The optimum is the same, and the solver can skip directions whose [LP relaxation](/lp-relaxation/) is already too costly.
- **Fixed directions.** Choose the directions by a rule, for example all down or alternating, and solve one LP. This is a heuristic, often used for large tables.
- **The L2 distance.** Minimize $\sum_i w_i y_i^2$ for fixed directions. This is a convex quadratic program. Castro (2006) studies it together with the L1 form.
- **Constraints on statistics.** Add linear constraints that keep chosen means, or bounds on the change of each cell. They make the LP larger and can make it infeasible.
- **Integer tables.** For tables of counts, ask for integer $y$. For a two-dimensional table with totals the relations are totally unimodular, so with integer data the vertex optimum of each LP is already integer.

## When to use it

Use CTA for a magnitude table with totals when cell suppression would hide too many cells, and when the users accept that some published values are not true values. It suits tables that are published with exact totals for the main relations, such as business statistics by region and industry. If there are many sensitive cells, use the mixed-integer form or a fixed rule for the directions. If the users need every published value to be true, use [cell suppression](/cell-suppression-problem/). If the release must be safe against any background knowledge or many releases, neither method gives a guarantee, and methods based on [differential privacy](/differential-privacy-definition/) are the alternative.

## Pitfalls

- **Writing the protection as one LP constraint.** The condition "$y_p \ge UPL_p$ or $y_p \le -LPL_p$" is not convex. A single LP with $|y_p| \ge$ a level, or with $y_p$ free, does not protect the cell. The direction must be fixed at line L4 or chosen by a binary variable.
- **Free $z^+$ and $z^-$ at a sensitive cell.** If both parts are free at line L4, the LP can set $z^+_p = z^-_p = UPL_p$ and leave $y_p = 0$. One of the two parts must be fixed to 0.
- **Publishing the levels and the sensitive cells.** At the optimum, a sensitive cell often sits exactly at the edge of its interval, as both cells do in the example. A reader who knows which cells are sensitive and the levels then has two candidates for each true value. Keep the levels and the list of sensitive cells confidential.
- **Bounds that are too tight at line L3.** If the cells near a sensitive cell cannot move, the LP is infeasible in every direction. Check line L7 and relax the bounds or the levels.
- **Floating-point tolerance.** With floats, a sensitive cell can end a little inside its interval. Check the result with exact arithmetic, or with a margin.

## Implementations

## History

Cox (1980) set up the protection of sensitive cells in tables with totals by suppression. Dandekar and Cox proposed controlled tabular adjustment in 2002 as an alternative that publishes every cell and keeps the totals. Castro (2006) studied minimum-distance adjustment of large tables with the L1 and L2 distances.

## References
