---
tag: M8KGT9
kind: algorithm
slug: dual-simplex-method
name: Dual simplex method
aliases:
- dual simplex
- Lemke's dual method
area: optimization/linear-programming
level: advanced
summary: Simplex on the dual, keeping dual feasibility and restoring primal feasibility; used after adding constraints.
solves: [linear-programming-problem]
model: real-ram
complexity:
  vars: {n: the number of variables, m: the number of equality constraints}
  time: {worst: O(2^n m n)}
  space: {extra: O(m n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1954
  people: [Carlton E. Lemke]
  note: Lemke published the dual simplex method in 1954.
prereqs: [simplex-method, dual-linear-program, reduced-cost]
see_also: [simplex-method, dual-linear-program, strong-duality, revised-simplex-method, gomory-cutting-plane-algorithm, lp-sensitivity-analysis, farkas-lemma, branch-and-cut]
sources:
  - paper: doi:10.1002/nav.3800010107
    title: C. E. Lemke, The dual method of solving the linear programming problem, Naval Research Logistics Quarterly 1(1), 1954
    locator: pages 36 to 47
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Section 4.5, Standard form problems and the dual simplex method
  - paper: doi:10.1002/nav.3800020406
    title: E. M. L. Beale, Cycling in the dual simplex algorithm, Naval Research Logistics Quarterly 2(4), 1955
    locator: pages 269 to 275
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006
    locator: Chapter 13, The simplex method (other simplex variants, the dual simplex method)
---

The dual simplex method solves a [linear program](/linear-programming-problem/) in [standard form](/lp-standard-form/) by moving through bases whose [reduced costs](/reduced-cost/) are all nonnegative, so that each basis gives a feasible solution of the [dual program](/dual-linear-program/), while its primal basic solution may have negative entries. Each pivot removes one negative basic variable and never lowers the dual objective. It stops when the basic solution is also nonnegative, which makes the basis optimal, or when a row proves that the program is infeasible. It is the method of choice after a constraint is added to a solved program, as in [branch and cut](/branch-and-cut/) and in [Gomory's cutting-plane algorithm](/gomory-cutting-plane-algorithm/).

## In plain words

The ordinary simplex method keeps a valid solution and works to make it the best. The dual simplex method does the reverse. It keeps a solution that is "too good to be true": every price test says it cannot be improved, but some variables have negative values, so it is not a valid solution yet. Each step picks one negative variable and moves it out of the basis, and brings in the variable that keeps all price tests true.

The bound that the method keeps can only go up. When no variable is negative any more, the solution is valid and also passes all price tests, so it is the best one. If a negative variable cannot be removed at all, its row is an equation that no valid solution can meet, and the method stops with that proof.

## The problem

The input is $A \in \mathbb{Q}^{m \times n}$ of rank $m$, $b \in \mathbb{Q}^m$, $c \in \mathbb{Q}^n$, for

$$\text{minimize } c^\top x \quad \text{subject to } Ax = b,\ x \ge 0,$$

and a *dual feasible* basis $B$: $A_B$ is nonsingular, and with $y = A_B^{-\top} c_B$ every reduced cost $r_j = c_j - y^\top A_j$ is $\ge 0$. Then $y$ is feasible for the dual $\max\{b^\top y : A^\top y \le c\}$. The basic solution $x_B = A_B^{-1} b$ may have negative entries.

A common source of such a basis: for $\min c^\top x$, $Gx \ge h$, $x \ge 0$ with $c \ge 0$, the rows $-Gx + s = -h$ and the slack basis have $r = (c, 0) \ge 0$ and $x_B = -h$.

The output is OPTIMAL with $x$ and $y$ ($c^\top x = b^\top y$), or INFEASIBLE with a [Farkas](/farkas-lemma/) vector $z$, $A^\top z \le 0$, $b^\top z > 0$. The answer "unbounded" cannot occur: the dual feasible $y$ gives the lower bound $b^\top y$ on the primal objective.

## The algorithm

```pseudo id=main
DUAL-SIMPLEX(A, b, c, B)                ▷ B is dual feasible: r ≥ 0
L1  loop
L2      x_B ← A_B⁻¹ b,  y ← A_B⁻ᵀ c_B,  r_j ← c_j − yᵀA_j for each j
L3      if x_B ≥ 0 then return OPTIMAL(x, y)
L4      choose a row p with x_B(p) < 0                  ▷ x_B(p) leaves
L5      α ← row p of A_B⁻¹ A
L6      if α ≥ 0 then return INFEASIBLE(−row p of A_B⁻¹)
L7      choose q with α_q < 0 that minimizes r_q / (−α_q)   ▷ the dual ratio test
L8      B(p) ← q                                         ▷ pivot on (p, q)
```

Line L4 chooses the leaving variable. The common choice is the most negative $x_{B(p)}$, the analogue of [Dantzig's rule](/dantzig-pivot-rule/). Solvers use the dual steepest-edge rule, which divides $x_{B(p)}^2$ by the squared norm of row $p$ of $A_B^{-1}$.

Line L6 is the infeasibility test. Row $p$ of the system $A_B^{-1} A x = A_B^{-1} b$ reads $\sum_j \alpha_j x_j = x_{B(p)}$. If every $\alpha_j \ge 0$, the left side is $\ge 0$ for each $x \ge 0$, but the right side is negative. With $g$ the row $p$ of $A_B^{-1}$, the vector $z = -g$ has $A^\top z = -\alpha \le 0$ and $b^\top z = -x_{B(p)} > 0$.

Line L7 is the *dual ratio test*. After the pivot on $(p, q)$, the new reduced costs are $r'_j = r_j - (r_q / \alpha_q) \alpha_j$. For $\alpha_j \ge 0$ this does not decrease $r_j$, since $r_q / \alpha_q \le 0$. For $\alpha_j < 0$ it stays $\ge 0$ exactly when $r_q / (-\alpha_q) \le r_j / (-\alpha_j)$. So the least ratio keeps the basis dual feasible. The dual objective changes by $b^\top y' - b^\top y = (r_q / (-\alpha_q)) \cdot (-x_{B(p)}) \ge 0$.

## Example

Minimize $2x_1 + 3x_2$ subject to $x_1 + x_2 \ge 4$, $x_1 + 3x_2 \ge 6$, $x \ge 0$; this is the example of the [two-phase method](/two-phase-simplex-method/). Write the rows as $-x_1 - x_2 + s_1 = -4$ and $-x_1 - 3x_2 + s_2 = -6$. The slack basis has $x_B = (-4, -6)$, not feasible, but $r = (2, 3, 0, 0) \ge 0$, so the dual simplex method starts there with no phase one. The leaving row is the most negative one.

| step | basis | $x_B$ | $b^\top y$ | $r$ of $x_1, x_2, s_1, s_2$ | leaving | $\alpha$ of the row | ratios | entering |
|---|---|---|---|---|---|---|---|---|
| 0 | $(s_1, s_2)$ | $(-4, -6)$ | $0$ | $2, 3, 0, 0$ | $s_2$ | $(-1, -3, 0, 1)$ | $x_1{:}\ 2$, $x_2{:}\ 1$ | $x_2$ |
| 1 | $(s_1, x_2)$ | $(-2, 2)$ | $6$ | $1, 0, 0, 1$ | $s_1$ | $(-2/3, 0, 1, -1/3)$ | $x_1{:}\ 3/2$, $s_2{:}\ 3$ | $x_1$ |
| 2 | $(x_1, x_2)$ | $(3, 1)$ | $9$ | $0, 0, 3/2, 1/2$ | | | | |

The dual objective rises $0, 6, 9$, and at step 2 the basic solution is nonnegative. So $x^* = (3, 1)$ is optimal with value $9$. The method took 2 pivots, against 2 pivots of phase one and 0 of phase two for the [two-phase method](/two-phase-simplex-method/) on the same program, and needed no artificial variables.

## Correctness

Three invariants hold at line L1: $B$ is a basis, it is dual feasible, and the dual value $b^\top y$ never decreases. At line L3 the basis is both primal and dual feasible, so $c^\top x = c_B^\top A_B^{-1} b = b^\top y$, and [weak duality](/weak-duality/) proves both optimal. At line L6 the row gives a Farkas certificate. Each pivot either raises the dual value or keeps it (a *dual degenerate* pivot, with $r_q = 0$). Without dual degenerate cycling the bases do not repeat, and the method stops after at most $\binom{n}{m}$ pivots. The proof file gives the details.

## Complexity

Model: arithmetic operations on rationals have unit cost (the [real RAM](/real-ram/)).

- **One pivot.** As in the primal method: $O(mn)$ for a tableau pivot, and in the revised form one BTRAN for row $p$ of $A_B^{-1}$, $O(mn)$ to form the row $\alpha$, and an update of the factorization.
- **The number of pivots.** At most $\binom{n}{m} \le 2^n$ if no basis repeats. This gives the bound $O(2^n mn)$ of the front matter. The method is the primal simplex method applied to the dual in disguise, so the exponential examples of the primal method carry over.
- **Space.** $O(mn)$ for the tableau.

In practice the dual simplex method is often faster than the primal method, and modern solvers use it as their default simplex method.

## Properties

- **Dual feasible at every step.** Each basis gives a lower bound $b^\top y$ on the optimum, so the run can stop early in branch and bound when the bound is already worse than the best known solution.
- **No phase one for $c \ge 0$.** Covering programs with nonnegative costs start at the slack basis.
- **Warm start after a new constraint.** Adding a constraint with its slack as a new basic variable keeps the old basis dual feasible.
- **Same pivots as the primal method on the dual.** It is the primal simplex method run on the dual program, with the tableau of the primal.

## Variants and improvements

- **Revised form.** In the [revised simplex method](/revised-simplex-method/) setting, line L5 needs only row $p$ of $A_B^{-1}$ and its products with the nonbasic columns.
- **Dual steepest-edge rule** for line L4, with the update formulas of Forrest and Goldfarb.
- **Bound flipping ratio test.** With boxed variables, the dual ratio test can pass over several breakpoints in one step, which helps a lot in practice.
- **Primal-dual and criss-cross methods.** They allow bases that are neither primal nor dual feasible.
- **Anti-cycling.** The least-index rule for the leaving row, with ties in line L7 going to the least index, and the dual lexicographic rule prevent cycling. Beale's 1955 example of cycling was given for the dual simplex method.

## When to use it

Use the dual simplex method when a dual feasible basis is at hand: after adding a cutting plane or a branching bound to a solved program, after a change of $b$ in [sensitivity analysis](/lp-sensitivity-analysis/), or for $\min c^\top x$, $Gx \ge h$ with $c \ge 0$. Use the primal method after a change of $c$ or after adding columns, since these keep primal feasibility.

## Pitfalls

- **The wrong sign in the ratio test.** Line L7 takes only columns with $\alpha_q < 0$, and divides by $-\alpha_q$. A column with $\alpha_q > 0$ would make the new $x_q$ negative.
- **A start that is not dual feasible.** If some $r_j < 0$, the method is not correct. Then use the primal method, or a composite method.
- **Reading an unbounded answer.** A row with no negative entry means that the primal program is infeasible, not unbounded. The dual is then unbounded or infeasible.
- **Dual degeneracy.** With many $r_j = 0$, long runs of pivots without progress in $b^\top y$ happen, and with a careless rule the method can cycle.

## Implementations

The Python version keeps a dense tableau of `Fraction` values, extended by $A_B^{-1}$ so that the Farkas vector is read off directly. `dual_simplex_method(a, b, c, basis, rule)` takes a dual feasible basis; the rule `"least-index"` picks the leaving row with the least basic index, and `"most-negative"` the most negative basic variable, with a check that reports a repeated basis. The tests compare the answer with an enumeration of all bases on 400 covering programs and 300 programs with random dual feasible starting bases, check the certificates, and check that $b^\top y$ never decreases.

## History

Carlton Lemke published the dual simplex method in 1954. Beale's 1955 paper on cycling was about the dual method. For decades the dual method was used mainly after the addition of constraints. From the 1990s on, with the dual steepest-edge rule and the bound flipping ratio test, it became the default simplex method of commercial solvers.

## References
