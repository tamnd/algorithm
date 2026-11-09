---
tag: AJZNEC
kind: algorithm
slug: two-phase-simplex-method
name: Two-phase simplex method
aliases:
- two-phase method
- phase one and phase two
area: optimization/linear-programming
level: core
summary: First phase finds a feasible basis via an auxiliary LP; second phase optimizes.
solves: [linear-programming-problem]
model: real-ram
complexity:
  vars: {n: the number of variables, m: the number of equality constraints}
  time: {worst: O(2^(n+m) m (n+m))}
  space: {extra: O(m (n+m))}
properties: {deterministic: true, exact: true, online: false, recursive: false}
prereqs: [simplex-method, lp-standard-form, basic-feasible-solution]
see_also: [initial-basic-feasible-solution, big-m-method, simplex-method, farkas-lemma, linear-feasibility, bland-rule, lp-degeneracy, dual-simplex-method]
sources:
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Section 3.5, Finding an initial basic feasible solution (artificial variables, driving artificial variables out of the basis, the two-phase method)
  - book: isbn:9780716715870
    title: Vašek Chvátal, Linear Programming, W. H. Freeman, 1983
    locator: Chapter 3, Pitfalls and how to avoid them (initialization by an auxiliary problem)
  - book: isbn:9780691059136
    title: George B. Dantzig, Linear Programming and Extensions, Princeton University Press, 1963 (reprint 1998)
    locator: Chapter 5, The simplex method (Phase I and Phase II)
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006
    locator: Chapter 13, The simplex method (starting the simplex method, Phase I and Phase II)
---

The two-phase simplex method solves a [linear program](/linear-programming-problem/) in [standard form](/lp-standard-form/) when no feasible basis is known at the start. Phase one adds one artificial variable for each row and runs the [simplex method](/simplex-method/) to minimize the sum of the artificials. If this sum cannot reach zero, the program is [infeasible](/linear-feasibility/), and the phase-one duals give a [Farkas](/farkas-lemma/) certificate. If it reaches zero, phase one also removes the redundant rows and leaves a feasible basis, and phase two optimizes the real objective from that basis.

## In plain words

The simplex method must start at a corner of the feasible region, but often we do not know any corner, or even whether the region is empty. So we first solve an easier helper problem. We give each equation a helper variable that absorbs the error of that equation. Setting all real variables to zero and all helpers to the right-hand sides is a corner of the helper problem. Then we use the simplex method to push the total error down to zero.

If the error cannot reach zero, no point satisfies all equations, and the method stops with a proof. If it reaches zero, the helpers are all zero, so the corner found is a corner of the real problem. We delete the helpers and run the simplex method again, now with the real objective.

## The problem

The input is $A \in \mathbb{Q}^{m \times n}$, $b \in \mathbb{Q}^m$ and $c \in \mathbb{Q}^n$, for the program

$$\text{minimize } c^\top x \quad \text{subject to } Ax = b,\ x \ge 0.$$

No basis is given, and $A$ can have dependent rows. The output is one of three answers, each with a certificate:

- **optimal**: an optimal [basic feasible solution](/basic-feasible-solution/) $x$ and a dual vector $y$ with $A^\top y \le c$ and $b^\top y = c^\top x$.
- **unbounded**: a feasible $x$ and a direction $w \ge 0$ with $Aw = 0$ and $c^\top w < 0$.
- **infeasible**: a vector $z$ with $A^\top z \le 0$ and $b^\top z > 0$. For a feasible $x$ we would get $0 < b^\top z = x^\top A^\top z \le 0$, so such a $z$ proves that no feasible $x$ exists.

## The algorithm

Phase one solves the *auxiliary program*

$$\text{minimize } \textstyle\sum_{i=1}^m a_i \quad \text{subject to } Ax + a = b,\ x \ge 0,\ a \ge 0,$$

after a change of sign of each row with $b_i < 0$, so that $b \ge 0$. The artificial columns form an identity matrix, and $x = 0$, $a = b$ is a feasible basic solution. The auxiliary program has the lower bound $0$, so its optimum exists.

```pseudo id=main
TWO-PHASE(A, b, c)
L1  for each row i with b_i < 0, multiply row i and b_i by −1
L2  add an artificial column e_i for each row i; B ← the artificial columns
L3  run SIMPLEX on min 1ᵀa from B; let B be the optimal basis
L4  if the optimum is > 0 then return INFEASIBLE(the phase-one duals)
L5  for each row i whose basic variable is an artificial (at level 0)
L6      if row i of the tableau has an entry ≠ 0 in an original column j then pivot on (i, j)
L7      else delete row i                            ▷ the constraint is redundant
L8  delete the artificial columns
L9  return SIMPLEX(A, b, c, B)                       ▷ phase two
```

Line L3 is the [simplex method](/simplex-method/) on the auxiliary program. This implementation uses [Bland's rule](/bland-rule/) in both phases, so neither phase can cycle.

Line L4 decides feasibility. If $Ax = b$, $x \ge 0$ has a solution $x$, then $(x, 0)$ is feasible for the auxiliary program with value $0$, so the optimum is $0$. If the optimum is positive, no such $x$ exists. The phase-one optimal dual vector $u$ satisfies $u^\top A \le 0$ (the reduced costs of the original columns are $0 - u^\top A_j \ge 0$) and $u^\top b$ equals the positive optimum. After the sign changes of line L1 are undone, $u$ is a Farkas certificate.

Lines L5 to L7 handle a degenerate end of phase one: the optimum is $0$, but an artificial variable is still basic at value $0$. If its row has a nonzero entry in some original column $j$, a pivot on that entry exchanges the artificial for $x_j$. The step has length zero because the right-hand side of the row is $0$, so the sign of the pivot entry does not matter. If the row is zero on all original columns, then this row of the tableau shows that one original constraint is a linear combination of the others, and the row can go.

Line L8 is safe because every artificial is now nonbasic at $0$. Line L9 starts phase two from a feasible basis of the remaining rows, which now have full row rank. Before phase two the reduced costs are recomputed from $c$.

## Example

Minimize $2x_1 + 3x_2$ subject to $x_1 + x_2 \ge 4$, $x_1 + 3x_2 \ge 6$ and $x \ge 0$. With the surplus variables $x_3$ and $x_4$ the standard form is

$$x_1 + x_2 - x_3 = 4, \qquad x_1 + 3x_2 - x_4 = 6.$$

The columns of $x_3$ and $x_4$ are $-e_1$ and $-e_2$, so the slack basis is not feasible: it gives $x_3 = -4$. Phase one adds $a_1$ and $a_2$ and minimizes $a_1 + a_2$ with Bland's rule.

| phase | step | basis | basic values | objective | entering | ratios | leaving |
|---|---|---|---|---|---|---|---|
| 1 | 0 | $(a_1, a_2)$ | $a_1 = 4$, $a_2 = 6$ | $10$ | $x_1$ (reduced cost $-2$) | $4, 6$ | $a_1$ |
| 1 | 1 | $(x_1, a_2)$ | $x_1 = 4$, $a_2 = 2$ | $2$ | $x_2$ (reduced cost $-2$) | $4, 1$ | $a_2$ |
| 1 | 2 | $(x_1, x_2)$ | $x_1 = 3$, $x_2 = 1$ | $0$ | | | |
| 2 | 0 | $(x_1, x_2)$ | $x_1 = 3$, $x_2 = 1$ | $9$ | | | |

At step 0 the reduced costs of phase one are $-(1 + 1) = -2$ for $x_1$ and $-(1 + 3) = -4$ for $x_2$. Bland's rule takes $x_1$, the least index with a negative reduced cost, not the most negative one. Phase one ends with value $0$ and no artificial in the basis, so lines L5 to L7 do nothing.

Phase two recomputes the multipliers from $y^\top A_B = c_B$: $y_1 + y_2 = 2$ and $y_1 + 3y_2 = 3$ give $y = (3/2, 1/2)$. The reduced costs of $x_3$ and $x_4$ are $y_1 = 3/2$ and $y_2 = 1/2$, both nonnegative. So phase two needs no pivot: $x^* = (3, 1)$ is optimal with value $9 = 4 \cdot 3/2 + 6 \cdot 1/2 = b^\top y$.

## Correctness

The auxiliary program is feasible and bounded below by $0$, so phase one stops with an optimal basis (Bland's rule excludes cycling). Its optimum is $0$ if and only if the original program is feasible, and when it is positive the phase-one duals form a Farkas certificate. If the optimum is $0$, each pivot of line L6 has length zero and keeps a feasible basis. A row deleted at line L7 is a combination of the kept rows, with a consistent right-hand side, so the feasible set does not change. The kept rows are independent and the basis is feasible for them, so phase two is the simplex method from a feasible basis, which is correct. The proof file gives the details.

## Complexity

Model: arithmetic operations on rationals have unit cost (the [real RAM](/real-ram/)).

- **One pivot.** The phase-one tableau has $m + 1$ rows and $n + m + 1$ columns, so one pivot takes $O(m(n + m))$ operations. Phase two works on $n + 1$ columns.
- **The number of pivots.** Phase one visits distinct bases of a program with $n + m$ columns, at most $\binom{n+m}{m} \le 2^{n+m}$ of them. Phase two visits at most $\binom{n}{m}$ bases. This gives the bound $O(2^{n+m} m(n+m))$ of the front matter.
- **Lines L5 to L7.** At most $m$ pivots, each $O(m(n+m))$.
- **Space.** The tableau has $O(m(n + m))$ entries.

In practice phase one often takes about as many pivots as phase two. The exponential bound comes from the same examples as for the simplex method, such as the [Klee-Minty cube](/klee-minty-cube/).

## Properties

- **Complete.** It decides each of the three cases and returns a certificate for each of them.
- **No rank assumption.** Redundant rows are found and removed during the run.
- **Exact.** With rational input and exact arithmetic, all three certificates are exact.
- **Two separate objectives.** Phase one ignores $c$, so it can end at a vertex that is far from the optimum.

## Variants and improvements

- **[Big-M method](/big-m-method/).** One run with the objective $c^\top x + M \sum a_i$ for a large $M$ instead of two phases.
- **One artificial variable.** For constraints $Ax \le b$, one extra variable $x_0$ is enough: subtract $x_0$ from each row, pivot $x_0$ into the row with the most negative $b_i$, and minimize $x_0$. This is the method of the [initial basic feasible solution](/initial-basic-feasible-solution/) page and of CLRS.
- **Fewer artificials.** Rows with a slack column and $b_i \ge 0$ need no artificial; the slack is already a basic column.
- **Composite objective.** Some solvers minimize the sum of infeasibilities directly in the original basis, with a piecewise linear phase one, and so skip the artificial columns.
- **Dual start.** If a basis with $r \ge 0$ is known, the [dual simplex method](/dual-simplex-method/) needs no phase one.

## When to use it

Use the two-phase method to solve a program in standard form from scratch with the simplex method, or to test whether a system $Ax = b$, $x \ge 0$ is feasible with a certificate either way. It does not need a choice of $M$ as the big-M method does, so it is the safe default for exact arithmetic. If a feasible basis is already known, for example the slack basis of $Ax \le b$ with $b \ge 0$, skip phase one.

## Pitfalls

- **Stopping when the artificial sum is zero but an artificial is still basic.** Deleting its column then leaves a basis with fewer than $m$ columns. Lines L5 to L7 must run.
- **Pivoting only on positive entries at line L6.** The pivot entry may be negative. The right-hand side of the row is $0$, so the step keeps feasibility for each sign.
- **Testing the optimum with a tolerance of zero in floating point.** A phase-one value of $10^{-12}$ is not proof of infeasibility. Exact arithmetic or a tolerance and a check of the certificate is necessary.
- **Using the phase-one reduced costs in phase two.** Phase two must recompute them from $c$ and the current basis.
- **Forgetting the sign changes of line L1** when the Farkas certificate or the dual vector is mapped back to the original rows.

## Implementations

The Python version keeps a dense tableau of `Fraction` values and uses Bland's rule in both phases. `two_phase_simplex_method(a, b, c)` returns the status, $x$, the value, the dual vector $y$, the ray for an unbounded program, the Farkas vector for an infeasible one, and the rows that phase one kept. The tests compare the status and the value with an enumeration of all bases on 800 random programs, with infeasible, unbounded, degenerate and redundant cases, and check each certificate.

## History

The simplex method of George Dantzig needs a feasible basis to start, and the use of artificial variables for this goes back to the early work of Dantzig and his coworkers around 1950. The split into Phase I, which minimizes the sum of the artificial variables, and Phase II, which optimizes the real objective, is the form of Dantzig's 1963 book and of the later textbooks.

## References
