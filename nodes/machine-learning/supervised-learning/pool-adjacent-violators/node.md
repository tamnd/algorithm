---
tag: 9PKVV8
kind: algorithm
slug: pool-adjacent-violators
name: Pool adjacent violators algorithm
aliases:
- PAVA
- pool adjacent violators
- pool-adjacent-violators algorithm
area: machine-learning/supervised-learning
level: advanced
summary: Solve weighted isotonic regression in O(n) time with a stack of blocks; merge two adjacent blocks while their means violate the order.
solves: [isotonic-regression]
model: real-ram
complexity:
  vars: {n: the number of observations}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: true, online: true, recursive: false}
history:
  year: 1955
  people: [Miriam Ayer, H. D. Brunk, G. M. Ewing, W. T. Reid, Edward Silverman]
  note: Ayer, Brunk, Ewing, Reid and Silverman gave the pooling method in 1955 for monotone estimates of a distribution function.
prereqs: [isotonic-regression, stack]
see_also: [isotonic-regression, kkt-conditions, quadratic-programming, regression]
sources:
  - paper: doi:10.1214/aoms/1177728423
    title: Miriam Ayer, H. D. Brunk, G. M. Ewing, W. T. Reid and Edward Silverman, An empirical distribution function for sampling with incomplete information, Annals of Mathematical Statistics 26(4), 1955
    locator: pp. 641 to 647 (the pooling of adjacent groups that violate the order)
  - book: isbn:9780471049708
    title: R. E. Barlow, D. J. Bartholomew, J. M. Bremner and H. D. Brunk, Statistical Inference under Order Restrictions, Wiley, 1972
    locator: Chapter 1 (isotonic regression on a totally ordered set, the pool adjacent violators algorithm and the max-min formulas)
  - book: isbn:9780471917878
    title: Tim Robertson, F. T. Wright and R. L. Dykstra, Order Restricted Statistical Inference, Wiley, 1988
    locator: Chapter 1 (isotonic regression, the pool adjacent violators algorithm and the min-max formulas)
  - paper: doi:10.1007/BF01580873
    title: Michael J. Best and Nilotpal Chakravarti, Active set algorithms for isotonic regression; a unifying framework, Mathematical Programming 47, 1990
    locator: pp. 425 to 439 (PAV as a dual feasible active set method, and its O(n) bound)
  - paper: doi:10.18637/jss.v032.i05
    title: Jan de Leeuw, Kurt Hornik and Patrick Mair, Isotone optimization in R, pool-adjacent-violators algorithm (PAVA) and active set methods, Journal of Statistical Software 32(5), 2009
    locator: Section 2 (the history of PAVA) and Section 3 (the algorithm)
---

The pool adjacent violators algorithm (PAV or PAVA) solves the [isotonic regression](/isotonic-regression/) problem on a sequence: given values $y_1, \dots, y_n$ with positive weights, it finds the non-decreasing sequence that is nearest in weighted squared error. It reads the values from left to right and keeps a [stack](/stack/) of blocks. When the mean of the top block is less than the mean of the block below it, the two blocks are a violating pair, and the algorithm pools them into one block with their weighted mean. The run takes $\Theta(n)$ arithmetic operations, and with exact numbers it returns the exact optimum.

## In plain words

You have a row of numbers, and you want a row that never goes down and stays as close as possible to the first one. Read the numbers one at a time. Each new number starts its own group. Each group shows the average of its numbers. If a group shows a smaller average than the group just before it, the row goes down there, so join the two groups into one and use their combined average. A join can make a new drop with the group before, so keep joining until there is no drop. At the end, write the average of each group in each place of the group.

Each number joins a larger group at most one time, so the total work grows in proportion to the length of the row.

## The problem

The input is $y = (y_1, \dots, y_n) \in \mathbb{R}^n$ and weights $\omega = (\omega_1, \dots, \omega_n)$ with each $\omega_i > 0$. The output is the unique solution of

$$\min_{z \in \mathbb{R}^n} \sum_{i=1}^{n} \omega_i (y_i - z_i)^2 \quad \text{subject to} \quad z_1 \le z_2 \le \dots \le z_n .$$

This is weighted [isotonic regression](/isotonic-regression/) on a total order. Unit weights give the plain least squares form. A weight $\omega_i = m$ has the same effect as $m$ copies of the point $y_i$. For a set $B$ of consecutive indices we write $W(B) = \sum_{i \in B} \omega_i$ and $\operatorname{Av}(B) = \sum_{i \in B} \omega_i y_i / W(B)$, the weighted mean.

## The algorithm

A block is a triple (value $v$, weight $W$, length $m$). It stands for $m$ consecutive indices with total weight $W$, and $v$ is their weighted mean.

```pseudo id=main
PAV(y[1 .. n], ω[1 .. n])                  ▷ each ω_i > 0
L1  S ← an empty stack of blocks (v, W, m)
L2  for i ← 1 to n do
L3      push (y_i, ω_i, 1) on S
L4      while |S| ≥ 2 and v(second block) > v(top block) do   ▷ adjacent violators
L5          pop the top block (v₂, W₂, m₂), then pop (v₁, W₁, m₁)
L6          push ((W₁v₁ + W₂v₂) / (W₁ + W₂), W₁ + W₂, m₁ + m₂)
L7  z ← an empty list
L8  for each block (v, W, m) of S, from the bottom to the top do
L9      append m copies of v to z
L10 return z
```

Line L3 makes each new value its own block. The loop of line L4 pools the top two blocks while their values are out of order. A pool can make the new top block smaller than the block below it, so the loop can pool many times after one push. Line L6 keeps the value of a block equal to the weighted mean of its values, because $W_1 v_1 + W_2 v_2$ is the weighted sum of the union. Lines L7 to L9 expand the blocks into the fitted sequence.

The test of line L4 is strict. Two adjacent blocks with equal values stay apart, and both are correct parts of the answer. A test with $\ge$ also gives the right answer, but it pools more often.

## Example

Take $y = (4, 5, 7, 2, 3, 8, 6, 9)$ with unit weights. The table shows the stack after each step, bottom first, as value and length.

| $i$ | $y_i$ | pools | stack after the step |
|---|---|---|---|
| 1 | 4 | 0 | (4, 1) |
| 2 | 5 | 0 | (4, 1) (5, 1) |
| 3 | 7 | 0 | (4, 1) (5, 1) (7, 1) |
| 4 | 2 | 2 | (4, 1) (14/3, 3) |
| 5 | 3 | 1 | (4, 1) (17/4, 4) |
| 6 | 8 | 0 | (4, 1) (17/4, 4) (8, 1) |
| 7 | 6 | 1 | (4, 1) (17/4, 4) (7, 2) |
| 8 | 9 | 0 | (4, 1) (17/4, 4) (7, 2) (9, 1) |

At step 4 the value 2 is below 7, so the algorithm pools $\{7, 2\}$ into the value $9/2$. This is below 5, so it pools again into $\{5, 7, 2\}$ with value $14/3$. That is above 4, so the loop stops. At step 5, $3 < 14/3$, and the pool gives $(5 + 7 + 2 + 3)/4 = 17/4$. The output is

$$z = (4, \tfrac{17}{4}, \tfrac{17}{4}, \tfrac{17}{4}, \tfrac{17}{4}, 7, 7, 9),$$

with the sum of squared errors $\sum (y_i - z_i)^2 = 67/4$. The run made 4 pools for 8 values.

## Correctness

The stack is a partition of $y_1, \dots, y_i$ into consecutive blocks. Each block $B$ has three properties: its value is $\operatorname{Av}(B)$; each prefix of $B$ has weighted mean at least $\operatorname{Av}(B)$; and after the loop of line L4 the values of the blocks do not decrease from the bottom to the top. A pool keeps the prefix property, because a violating pair joins a block with a larger mean before a block with a smaller mean.

At the end, these properties are exactly the [KKT conditions](/kkt-conditions/) of the problem, with the multiplier of the constraint $z_k \le z_{k+1}$ equal to the partial sum $\sum_{i \le k} \omega_i (y_i - z_i)$. The proof shows directly, by a summation by parts, that each other monotone $u$ has a larger error: $f(u) - f(z) \ge \tfrac{1}{2}\sum_i \omega_i (u_i - z_i)^2$ for the half error $f$. So the output is the unique optimum. The full proof is in the correctness proof below.

## Complexity

Count the arithmetic operations and comparisons on a [real RAM](/real-ram/).

- Line L3 runs $n$ times, so there are $n$ pushes.
- Each pool of lines L5 and L6 lowers the number of blocks on the stack by one. The stack never has fewer than one block after line L3, and it gains one block per push. So the total number of pools in the whole run is at most $n - 1$.
- Each test of line L4 either leads to a pool or ends the loop. So there are at most $n + (n - 1)$ tests.
- Lines L7 to L9 write $n$ values.

The time is $\Theta(n)$ in the best and the worst case. A sorted input makes no pool, and a strictly decreasing input makes $n - 1$ pools that end in one block. The extra memory is the stack of at most $n$ blocks, $\Theta(n)$ in the worst case, plus the output.

The algorithm reads each value once. So $\Theta(n)$ is also a lower bound: each $y_i$ can change the answer.

## Properties

- **Exact.** With rational inputs and exact arithmetic, each value is a weighted mean of input values, so the output is exact. In floating point, each block value has the rounding error of one weighted mean.
- **Online.** After step $i$, the stack holds the isotonic fit of $y_1, \dots, y_i$. A new value changes only the top blocks. A value that was already fitted can still go down later, when a pool reaches its block.
- **Not recursive.** The cascade of pools uses the explicit stack.
- **Order of the input matters.** The algorithm needs the values in the order of the constraint. For data $(x_i, y_i)$, sort by $x$ first, and keep ties of $x$ in one place (see Pitfalls).

## Variants and improvements

- **Non-increasing fit.** Reverse the test of line L4, or negate $y$, fit, and negate the result.
- **Other losses.** The same pooling with the weighted median in place of the mean solves the $L_1$ isotonic problem, but the pooled value is no longer a simple update of two numbers. For any loss $\sum_i \ell_i(z_i)$ with convex $\ell_i$, pooling with the minimizer of the summed loss of the block also works.
- **Other orders of pooling.** The first descriptions pool adjacent violating pairs in no fixed order. The stack order of line L4 is the one that gives the $O(n)$ bound with a short proof.
- **Partial orders.** On a tree or on a grid, the pooling idea does not directly work, and isotonic regression becomes a general [quadratic program](/quadratic-programming/) with special structure.
- **Active set view.** Best and Chakravarti (1990) show that PAV is a dual feasible active set method for the quadratic program. The blocks are the sets of active constraints $z_k = z_{k+1}$.

## When to use it

Use PAV whenever the constraint is a total order: monotone calibration of classifier scores (the isotonic calibration of probability estimates), monotone dose response curves, and the inner step of methods such as monotone single index models. It is optimal in time and needs no tuning and no tolerance. A general quadratic programming solver gives the same answer, with more time and with a tolerance, so it is only needed for partial orders.

## Pitfalls

- **Comparing only adjacent input values.** A single pass that pools $y_i$ with $y_{i+1}$ when $y_i > y_{i+1}$ and never looks back is wrong: on $(4, 5, 7, 2)$ it pools 7 and 2 into $9/2$ and stops, below the 5. The loop of line L4 must run again after each pool.
- **Unweighted means in a pool.** Line L6 must weight each block by its total weight $W$, not by 1. The mean of the means $(4 + 9/2)/2$ is not the mean of the pooled values.
- **Ties in the input order.** With repeated $x$ values, the order of $y$ within a tie is arbitrary, and different orders give different fits. The usual fix is to replace each tie group by one point with its mean $y$ and the sum of the weights, before the run.
- **Zero or negative weights.** The problem needs $\omega_i > 0$. A zero weight makes the fit at that index not unique, and a negative weight makes the problem non-convex.

## Implementations

## History

Ayer, Brunk, Ewing, Reid and Silverman described the pooling in 1955, to find a monotone maximum likelihood estimate of a distribution function from incomplete data. The book of Barlow, Bartholomew, Bremner and Brunk (1972) made isotonic regression and the algorithm a standard tool, with the max-min formulas for the solution. Best and Chakravarti (1990) placed PAV in the frame of active set methods for quadratic programs. De Leeuw, Hornik and Mair (2009) give a history of the method and its many names.

## References
