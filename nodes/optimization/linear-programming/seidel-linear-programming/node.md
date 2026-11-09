---
tag: 8NCQG0
kind: algorithm
slug: seidel-linear-programming
name: Seidel's algorithm for linear programming
aliases:
- Seidel's randomized LP
- randomized incremental linear programming
area: optimization/linear-programming
level: advanced
summary: Randomized incremental LP algorithm with expected linear time for fixed dimension.
solves: [linear-programming-problem]
model: real-ram
complexity:
  vars: {n: the number of variables (fixed), m: the number of constraints}
  time: {expected: O(n! m)}
  space: {extra: O(n^2 m)}
properties: {deterministic: false, exact: true, online: false, recursive: true}
history:
  year: 1990
  people: [Raimund Seidel]
  note: Seidel presented the method at the Symposium on Computational Geometry in 1990 and published the journal version in 1991.
prereqs: [linear-programming-problem, randomized-incremental-construction, backwards-analysis]
see_also: [megiddo-fixed-dimension-lp, clarksons-algorithm, lp-type-problem, welzls-algorithm, half-plane-intersection, minimum-enclosing-circle, simplex-method, basic-feasible-solution]
sources:
  - paper: doi:10.1007/BF02574699
    title: Raimund Seidel, Small-dimensional linear programming and convex hulls made easy, Discrete and Computational Geometry 6(3), 1991
    locator: pages 423 to 434, the recursive incremental algorithm, the probability d/n that the last constraint changes the optimum, and the bound O(d! n)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, 3rd edition, Springer, 2008
    locator: Chapter 4, Sections 4.3 to 4.6 (incremental and randomized linear programming in the plane, unbounded programs, higher dimensions)
  - paper: doi:10.1007/3-540-55210-3_213
    title: Micha Sharir and Emo Welzl, A combinatorial bound for linear programming and related problems, STACS 92, Lecture Notes in Computer Science 577, Springer, 1992
    locator: pages 567 to 579, the remove-and-repair form of the method and LP-type problems
  - paper: doi:10.1007/BF01940877
    title: Jiří Matoušek, Micha Sharir and Emo Welzl, A subexponential bound for linear programming, Algorithmica 16, 1996
    locator: pages 498 to 516, the bound e^(O(sqrt(d log n))) for the same scheme with a better choice of the constraint to remove
---

Seidel's algorithm solves a [linear program](/linear-programming-problem/) with a fixed number $n$ of variables and $m$ constraints in expected $O(n!\, m)$ time. It adds the constraints one at a time in random order and keeps the optimum of the constraints so far. When a new constraint cuts off the current optimum, the new optimum lies on the boundary of that constraint, and a recursive call in $n - 1$ variables finds it. The method is short and exact, and for two or three variables it is a common choice in practice.

## In plain words

Think of the feasible region as a block that the constraints carve one cut at a time. Keep the best point of the block cut so far. When a new cut comes, two things can happen. If the best point is on the kept side, it stays the best point, and the step is cheap. If the cut removes it, then the new best point lies on the face of the cut. On that face the problem has one dimension less, so the same method solves it.

The expensive case is rare when the cuts come in random order. Only a few cuts hold the best point in place, and the newest cut is one of them with small probability. So most steps are cheap, and the total work grows linearly with the number of cuts.

## The problem

Minimize $c^\top x$ subject to $a_i^\top x \le b_i$ for $i = 1, \ldots, m$, with $x \in \mathbb{R}^n$ and $n$ small. The answer is an optimal point, INFEASIBLE, or UNBOUNDED. The method needs a bounded problem, so the program is solved inside a box $-M \le x_j \le M$. For integer data with entries of absolute value at most $K$, a box with $M$ of order $n K H^2$, where $H = (nK)^n$, changes nothing for a bounded program, and makes an unbounded program show up as an optimal value below $-nKH$. The [proof](#correctness) gives the details.

## The algorithm

The method needs a unique optimum in every step. So it breaks ties with a lexicographic rule: among the optimal points, take the one with the least $x_1$, then the least $x_2$, and so on. Since the box is bounded and the rule ends with the coordinates, the box with any set of constraints has exactly one such point, or is empty.

```pseudo id=main
SEIDEL(H, c, M)     ▷ H: constraints in n variables; the box -M ≤ x_j ≤ M is always there
L1  if n = 1 then return the best end of the interval that H and the box leave, or INFEASIBLE if it is empty
L2  x ← the best corner of the box
L3  put the constraints of H in random order h_1, ..., h_m
L4  for i ← 1 to m
L5      if x satisfies h_i then continue
L6      x ← SEIDEL({h_1, ..., h_{i-1}} restricted to the hyperplane of h_i, c, M)     ▷ n - 1 variables
L7      if x = INFEASIBLE then return INFEASIBLE
L8  return x
```

Line L6 restricts the problem to the hyperplane $a_i^\top x = b_i$. Pick the variable $x_k$ with the largest $|a_{ik}|$ and substitute $x_k = (b_i - \sum_{j \ne k} a_{ij} x_j) / a_{ik}$ in the earlier constraints, in the objective, and in the two box constraints of $x_k$, which become two ordinary constraints of the smaller problem. The recursive call returns a point in $n - 1$ variables, and the substitution gives back $x_k$.

## Example

Minimize $-x_1 - x_2$ subject to $h_1: x_1 + 2x_2 \le 4$, $h_2: 3x_1 + x_2 \le 6$, $h_3: -x_1 \le 0$ and $h_4: -x_2 \le 0$, in the box $|x_j| \le 10$, with the order $h_1, h_2, h_3, h_4$.

| step | constraint | current point | satisfied? | new point |
|---|---|---|---|---|
| L2 | the box | | | $(10, 10)$ |
| 1 | $x_1 + 2x_2 \le 4$ | $(10, 10)$: $30 > 4$ | no | $(10, -3)$ |
| 2 | $3x_1 + x_2 \le 6$ | $(10, -3)$: $27 > 6$ | no | $(8/5, 6/5)$ |
| 3 | $-x_1 \le 0$ | $(8/5, 6/5)$ | yes | |
| 4 | $-x_2 \le 0$ | $(8/5, 6/5)$ | yes | |

In step 1 the call works on the line $x_1 + 2x_2 = 4$. It substitutes $x_2 = (4 - x_1)/2$, so the objective becomes $-x_1/2 - 2$, and the box on $x_2$ becomes $-16 \le x_1 \le 24$. With the box $-10 \le x_1 \le 10$, the best point is $x_1 = 10$, so $x_2 = -3$. In step 2 the call works on the line $3x_1 + x_2 = 6$ with $h_1$ only. It substitutes $x_1 = (6 - x_2)/3$, the objective becomes $-2 - 2x_2/3$, and $h_1$ becomes $x_2 \le 6/5$, which is the binding bound. So the answer is $(8/5, 6/5)$ with value $-14/5$, after two recursive calls. In the order $h_4, h_3, h_2, h_1$, the method passes through $(0, 6)$ instead and also makes two calls.

## Correctness

Let $Q_i$ be the box cut by $h_1, \ldots, h_i$, and $x_i$ its lexicographic optimum. If $x_{i-1}$ satisfies $h_i$, then $x_i = x_{i-1}$, since $Q_i \subseteq Q_{i-1}$. If not, then $x_i$ lies on the hyperplane of $h_i$: otherwise the segment from $x_i$ to $x_{i-1}$ crosses that hyperplane at a point of $Q_i$ that is better than $x_i$, because the objective is linear along the segment and $x_{i-1}$ is better than $x_i$. So line L6 finds $x_i$, or finds that $Q_i$ is empty. The [proof](/seidel-linear-programming/proofs/correctness/) also shows that the box decides UNBOUNDED correctly.

## Complexity

Model: arithmetic operations on reals have unit cost (the [real RAM](/real-ram/)).

- **Backwards analysis.** Fix the set of the first $i$ constraints. The order within the set is random, so $h_i$ is a random member of it. The optimum $x_i$ is fixed by at most $n$ of the constraints, a *basis*. A call at step $i$ happens only if $h_i$ is in the basis, with probability at most $n/i$. This is [backwards analysis](/backwards-analysis/).
- **Expected time.** A call at step $i$ costs $O(n i)$ for the substitution plus a call on $i + 1$ constraints in $n - 1$ variables. So $T_n(m) \le \sum_{i=1}^{m} \big(O(n) + \tfrac{n}{i} (O(n i) + T_{n-1}(i + 1))\big)$, which gives $T_n(m) \le C_n m$ plus lower-order terms, with $C_n = n C_{n-1} + O(n^2)$, so $C_n = O(n!)$.
- **Worst case.** A bad order makes a call at every step, and the time is then of order $m^n$. The random order makes this very unlikely.
- **Space.** $O(n m)$ for each level of the recursion, so $O(n^2 m)$ in total.

## Properties

- **Las Vegas.** The answer is always correct; only the time is random.
- **Exact.** With rational input and rational arithmetic, the answer is an exact vertex of the box-cut region.
- **Incremental.** It can take the constraints as they come, if they come in random order.
- **Combinatorial.** It uses only two primitives: a test of whether a point violates a constraint, and a solution of the problem on a hyperplane. This is why it extends to [LP-type problems](/lp-type-problem/).

## Variants and improvements

- **Remove and repair.** Sharir and Welzl (1992) write the method as: remove a random constraint $h$, solve the rest recursively, and if the answer violates $h$, solve again with $h$ as a fixed constraint. This form works for every [LP-type problem](/lp-type-problem/).
- **Subexponential bounds.** Matoušek, Sharir and Welzl (1996) choose the constraint to remove with more care and get an expected $e^{O(\sqrt{n \log m})}$ time. Kalai (1992) found a similar bound by a randomized simplex method.
- **[Clarkson's algorithm](/clarksons-algorithm/).** Random sampling cuts the problem to $O(n^2)$ constraints and calls a method such as Seidel's on the samples. This gives $O(n^2 m)$ plus a term that does not depend much on $m$.
- **[Welzl's algorithm](/welzls-algorithm/).** The same scheme finds the [smallest enclosing circle](/minimum-enclosing-circle/) and ball.
- **Unbounded programs without a box.** De Berg et al. first test for a direction of unboundedness by a program in $n - 1$ variables, and then use the constraints that bound the optimum as the start.

## When to use it

Use it for linear programs with few variables and many constraints: two or three variables in geometry, such as [half-plane intersection](/half-plane-intersection/) and separation of point sets, or a few more variables when $n!$ is still small. For a worst-case bound with no randomness, use [Megiddo's algorithm](/megiddo-fixed-dimension-lp/). For many variables, use the [simplex method](/simplex-method/) or an [interior-point method](/interior-point-method/), since the factor $n!$ grows fast.

## Pitfalls

- **Ties.** With several optimal points, the analysis fails, because the optimum then depends on the order and not only on the set. Use the lexicographic rule, or a symbolic perturbation of $c$.
- **The box.** A box that is too small cuts off the true optimum. A safe box has very large numbers, which is fine in exact arithmetic but not in floating point. Floating-point code uses a symbolic box, or the separate test for unbounded programs.
- **Empty constraints.** A constraint $0^\top x \le b$ with $b < 0$ comes up in the recursion when two constraints are parallel. It makes the program infeasible.
- **Shuffle once per call.** Each recursive call must use a fresh random order, or a random order of its own constraints.

## Implementations

The Python version works in exact fractions for any $n$, with the lexicographic rule and the safe box for integer data. The tests compare it with a brute force over all vertices of the box-cut region and a separate ray test on 600 random programs in one to three variables, with optimal, unbounded and infeasible cases, and on 100 degenerate programs with many constraints through one point. They also check that the answer does not depend on the random order, solve programs in four and five variables with a known optimum, and show that a bad order of 400 constraints makes 399 calls while random orders make about 11.

## History

Seidel presented the method at the Symposium on Computational Geometry in 1990, and the journal version appeared in 1991 together with a randomized convex hull algorithm, as an early example of what he later called backwards analysis. Welzl used the same scheme for the smallest enclosing disk in 1991. Sharir and Welzl (1992) turned it into the framework of [LP-type problems](/lp-type-problem/), and with Matoušek (1996) they gave the subexponential bound. Together with [Clarkson's algorithm](/clarksons-algorithm/), this gives the best known randomized bound for linear programming in the unit-cost model.

## References
