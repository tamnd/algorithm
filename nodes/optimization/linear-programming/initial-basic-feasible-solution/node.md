---
tag: 1EQ5XZ
kind: algorithm
slug: initial-basic-feasible-solution
name: Finding an initial basic feasible solution
aliases:
- Finding an initial basic solution
- INITIALIZE-SIMPLEX
- auxiliary linear program
area: optimization/linear-programming
level: core
summary: Builds an auxiliary linear program to find a feasible starting basis for simplex, or to detect that the original program is infeasible.
solves: [linear-feasibility]
model: real-ram
complexity:
  vars: {n: the number of variables, m: the number of inequality constraints}
  time: {worst: O(2^(n+m) m (n+m))}
  space: {extra: O(m (n+m))}
properties: {deterministic: true, exact: true, online: false, recursive: false}
prereqs: [simplex-method, lp-slack-form, basic-feasible-solution]
see_also: [two-phase-simplex-method, big-m-method, linear-feasibility, farkas-lemma, lp-slack-form, slack-variables, dual-simplex-method, simplex-method]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 29.5, The initial basic feasible solution (the auxiliary program L_aux and INITIALIZE-SIMPLEX)
  - book: isbn:9780716715870
    title: Vašek Chvátal, Linear Programming, W. H. Freeman, 1983
    locator: Chapter 3, Pitfalls and how to avoid them (initialization with the auxiliary variable x0)
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Section 3.5, Finding an initial basic feasible solution
---

The simplex method needs a feasible basis to start. For constraints $Ax \le b$, $x \ge 0$ with $b \ge 0$ the slack variables give one at once, but if some $b_i < 0$ the origin is not feasible. This method adds a single artificial variable $x_0$ to every row, makes the program feasible with one pivot, and then minimizes $x_0$ with the [simplex method](/simplex-method/). If the least $x_0$ is $0$, the final basis without $x_0$ is a feasible basis of the original program; if not, the program is infeasible, and the duals give a [Farkas](/farkas-lemma/) certificate.

## In plain words

Suppose that some constraints are broken at the origin. Add one helper amount that loosens every constraint by the same quantity. If the helper is large enough, the origin satisfies all constraints, and the loosest point for the most broken constraint is a corner of the new problem. Now ask the simplex method to make the helper as small as possible.

If the helper can go down to zero, the constraints hold with no help, and the corner reached is a valid start for the real problem. If the helper must stay positive, the constraints cannot all hold together. The final prices of the constraints then show a weighted sum of them that reads "a nonnegative quantity is at most a negative number", which is a short proof of infeasibility.

## The problem

The input is $A \in \mathbb{Q}^{m \times n}$ and $b \in \mathbb{Q}^m$, for the system

$$Ax \le b, \qquad x \ge 0.$$

In [slack form](/lp-slack-form/) this is $Ax + s = b$, $x \ge 0$, $s \ge 0$, a system in standard form with the matrix $[A \mid I]$ of rank $m$. The output is one of two answers:

- **feasible**: a list $B$ of $m$ columns of $[A \mid I]$ such that $[A \mid I]_B$ is nonsingular and its basic solution is $\ge 0$. This is a valid start for the simplex method with any objective.
- **infeasible**: a vector $y \ge 0$ with $y^\top A \ge 0$ and $y^\top b < 0$. For a feasible $x$ we would get $0 \le y^\top A x \le y^\top b < 0$, so $y$ proves that no feasible $x$ exists.

## The algorithm

The *auxiliary program* has one more column, $x_0$, with coefficient $-1$ in every row:

$$\text{minimize } x_0 \quad \text{subject to } Ax - x_0 \mathbf 1 + s = b,\ x \ge 0,\ s \ge 0,\ x_0 \ge 0.$$

For $x_0 \ge \max_i (-b_i)$ the point $x = 0$, $s = b + x_0 \mathbf 1$ is feasible. A point $(x, s)$ is feasible for the original system if and only if $(x, 0, s)$ is feasible for the auxiliary program, so the original system is feasible if and only if the least $x_0$ is $0$.

```pseudo id=main
INITIAL-BFS(A, b)
L1  if b ≥ 0 then return the slack basis
L2  add the column x0 = −1 to every row; the objective is min x0
L3  k ← a row with the least b_k; pivot x0 into row k        ▷ s_k leaves
L4  run SIMPLEX on min x0 from this basis
L5  if the optimal x0 is > 0 then return INFEASIBLE(y)
L6  if x0 is basic (at level 0) then pivot it out on a nonzero entry of its row
L7  delete the column x0 and return the basis
```

Line L3 is the key step. The pivot on row $k$ makes $x_0 = -b_k$ and changes every other slack to $s_i = b_i - b_k \ge 0$, because $b_k$ is the least entry. So after one pivot the basis is feasible, with no search.

Line L4 is the simplex method on a program that is bounded below by $0$, so it ends at an optimal basis. This implementation uses [Bland's rule](/bland-rule/), so it cannot cycle.

Line L5 returns $y = -u$, where $u$ is the optimal dual vector of the auxiliary program. Dual feasibility at the slack columns gives $u \le 0$, at the $x$ columns $u^\top A \le 0$, and strong duality gives $u^\top b = x_0^* > 0$. So $y \ge 0$, $y^\top A \ge 0$ and $y^\top b < 0$. In the tableau, $y_i$ is the reduced cost of the slack $s_i$.

Line L6 handles a degenerate end. If $x_0$ is still basic at value $0$, its row has a nonzero entry in some column of $[A \mid I]$, because the matrix $[A \mid I]$ has rank $m$. The pivot on that entry has length zero, since the right-hand side of the row is $0$, so the basis stays feasible and $x_0$ becomes nonbasic. CLRS also uses one degenerate pivot for this case.

## Example

This is the example of CLRS: $2x_1 - x_2 \le 2$, $x_1 - 5x_2 \le -4$, $x \ge 0$. The slack basis gives $s_2 = -4$, which is not feasible. The auxiliary rows are $2x_1 - x_2 + s_1 - x_0 = 2$ and $x_1 - 5x_2 + s_2 - x_0 = -4$.

| step | action | basis | basic values | $x_0$ | reduced costs of $x_1, x_2, s_1, s_2, x_0$ |
|---|---|---|---|---|---|
| 0 | start | $(s_1, s_2)$ | $s_1 = 2$, $s_2 = -4$ | $0$ | (not feasible) |
| 1 | line L3: $x_0$ enters row 2, $s_2$ leaves | $(s_1, x_0)$ | $s_1 = 6$, $x_0 = 4$ | $4$ | $1, -5, 0, 1, 0$ |
| 2 | line L4: $x_2$ enters, ratios $6/4$ and $4/5$, $x_0$ leaves | $(s_1, x_2)$ | $s_1 = 14/5$, $x_2 = 4/5$ | $0$ | $0, 0, 0, 0, 1$ |

After step 1 the rows are $x_1 + 4x_2 + s_1 - s_2 = 6$ and $-x_1 + 5x_2 - s_2 + x_0 = 4$. Only $x_2$ has a negative reduced cost. The ratio test picks row 2, since $4/5 < 6/4$, so $x_0$ leaves and the least $x_0$ is $0$. The basis $(s_1, x_2)$ gives $x = (0, 4/5)$ with $s = (14/5, 0)$, which satisfies both constraints. The simplex method can now start from it with any objective.

For an infeasible system, take $x_1 + x_2 \le -1$. Line L3 gives $x_0 = 1$, no column has a negative reduced cost, and the method returns $y = (1)$: indeed $y^\top A = (1, 1) \ge 0$ and $y^\top b = -1 < 0$.

## Correctness

After line L3 the basis is feasible, because each new right-hand side is $b_i - b_k \ge 0$ and $x_0 = -b_k > 0$. The auxiliary program is bounded below by $0$, so line L4 ends at an optimum. If it is positive, the original system has no solution, and $y$ is a valid Farkas certificate by duality. If it is $0$, line L6 makes $x_0$ nonbasic with a step of length zero, so the remaining $m$ columns form a feasible basis of $[A \mid I]$. The proof file gives the details.

## Complexity

Model: arithmetic operations on rationals have unit cost (the [real RAM](/real-ram/)).

- **One pivot.** The tableau has $m$ rows and $n + m + 2$ columns, so a pivot takes $O(m(n + m))$ operations.
- **The number of pivots.** Line L4 visits distinct bases of a matrix with $n + m + 1$ columns, and at most $\binom{n+m+1}{m}$ of them, which is $O(2^{n+m})$. With line L3 and line L6, two more pivots. This gives the bound $O(2^{n+m} m(n+m))$ of the front matter.
- **Space.** The tableau has $O(m(n + m))$ entries.

The worst case is the worst case of the simplex method. In practice the run is short.

## Properties

- **One artificial variable.** It adds one column, not $m$ as the [two-phase method](/two-phase-simplex-method/) does.
- **One pivot to feasibility.** The auxiliary basis is feasible after the single pivot of line L3.
- **Certificates.** Both answers come with a proof: a basis that the caller can check, or a Farkas vector.
- **Inequality form.** It needs the slack columns: it assumes $Ax \le b$, not $Ax = b$.

## Variants and improvements

- **[Two-phase method](/two-phase-simplex-method/).** For equality constraints $Ax = b$ with no slack columns, one artificial per row is the common start.
- **[Big-M method](/big-m-method/).** It adds $M x_0$ to the real objective and so finds feasibility and the optimum in one run.
- **A tie rule for $x_0$.** If the row of $x_0$ ties in the ratio test, choose it to leave. The value of $x_0$ can reach $0$ only at such a tie, so $x_0$ is never basic at the end with value $0$, and line L6 is not needed.
- **[Dual simplex method](/dual-simplex-method/).** If $c \ge 0$, the slack basis is dual feasible even when $b \not\ge 0$, so the dual simplex method can start from it with no auxiliary program.

## When to use it

Use this method to start the simplex method on a program in inequality form $Ax \le b$, $x \ge 0$ with some $b_i < 0$, or to decide whether such a system is feasible with a certificate. For programs in equality form with no slack columns, use the [two-phase method](/two-phase-simplex-method/).

## Pitfalls

- **Pivoting $x_0$ into a row other than the most negative one.** Then some other slack becomes negative, and the start is not feasible.
- **Forgetting line L6.** If $x_0$ stays basic at level $0$ and its column is deleted, the basis has only $m - 1$ columns.
- **Keeping the auxiliary objective.** The caller must compute the reduced costs of the real objective from the returned basis.
- **Reading the certificate with the wrong sign.** The tableau holds $-u$ in the slack columns. The certificate is $y \ge 0$ with $y^\top A \ge 0$ and $y^\top b < 0$.

## Implementations

The Python version keeps a dense tableau of `Fraction` values with the columns $x$, $s$ and $x_0$, and uses Bland's rule. `initial_basic_feasible_solution(a, b)` returns a basis of $[A \mid I]$ and its basic solution, or the Farkas vector $y$. The tests check each basis (independent columns and a basic solution $\ge 0$) and each certificate, and they compare the answer with an enumeration of all bases of $[A \mid I]$ on 600 random systems, with many degenerate ones where $x_0$ ends basic at level $0$.

## History

The use of one artificial variable for a phase one with inequality constraints is a textbook form of the start of the simplex method. Chvátal (1983) presents it with the auxiliary variable $x_0$, and CLRS presents it as the procedure INITIALIZE-SIMPLEX, with the same example as on this page.

## References
