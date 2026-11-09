---
tag: XN1HFE
kind: algorithm
slug: big-m-method
name: Big-M method
aliases:
- penalty method for LP
- M method
area: optimization/linear-programming
level: core
summary: Add artificial variables with a large penalty in the objective to find an initial feasible basis.
solves: [linear-programming-problem]
model: real-ram
complexity:
  vars: {n: the number of variables, m: the number of equality constraints}
  time: {worst: O(2^(n+m) m (n+m))}
  space: {extra: O(m (n+m))}
properties: {deterministic: true, exact: true, online: false, recursive: false}
prereqs: [simplex-method, lp-standard-form, basic-feasible-solution]
see_also: [two-phase-simplex-method, initial-basic-feasible-solution, simplex-method, farkas-lemma, dual-linear-program, complementary-slackness, bland-rule, linear-feasibility]
sources:
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Section 3.5, Finding an initial basic feasible solution (the big-M method)
  - book: isbn:9780691059136
    title: George B. Dantzig, Linear Programming and Extensions, Princeton University Press, 1963 (reprint 1998)
    locator: Chapter 5, The simplex method (artificial variables and the start of the method)
---

The big-M method solves a [linear program](/linear-programming-problem/) in [standard form](/lp-standard-form/) with no known feasible basis in one run of the [simplex method](/simplex-method/). It adds an artificial variable $a_i$ to each row and the penalty $M \sum_i a_i$ to the objective, where $M$ is very large, so the artificial basis is a valid start and the method drives the artificials to zero on its way to the optimum. If $M$ is a symbol that is larger than every number, the method is exact; if $M$ is a fixed number, it can be too small and give a wrong answer.

## In plain words

To start the simplex method we need a corner of the feasible region. The big-M method makes one by force. It gives each equation a helper variable that absorbs its error, and it charges a very high price $M$ for each unit of helper. The corner where the helpers carry all the error is then a valid start.

From there the usual simplex method runs on the new objective. Because the helpers are so expensive, the method first removes them, and then it improves the real objective. At the end, if some helper is still positive, the real problem has no feasible point. This needs care: if the price is a fixed number that is not large enough, a helper can stay positive only because it is cheaper than the real cost, and the answer is wrong.

## The problem

The input is $A \in \mathbb{Q}^{m \times n}$, $b \in \mathbb{Q}^m$ and $c \in \mathbb{Q}^n$, for

$$\text{minimize } c^\top x \quad \text{subject to } Ax = b,\ x \ge 0.$$

First each row with $b_i < 0$ is multiplied by $-1$, so that $b \ge 0$. The *penalized program* is

$$\text{minimize } c^\top x + M \mathbf 1^\top a \quad \text{subject to } Ax + a = b,\ x \ge 0,\ a \ge 0.$$

The output is optimal (with $x$ and $c^\top x$), unbounded (with a feasible $x$ and a ray $d \ge 0$, $Ad = 0$, $c^\top d < 0$), or infeasible (with a [Farkas](/farkas-lemma/) vector $z$, $A^\top z \le 0$, $b^\top z > 0$).

The implementation treats $M$ as a symbol. Each cost and reduced cost is $pM + q$, stored as the pair $(p, q)$, and $pM + q < 0$ means $(p, q) < (0, 0)$ in lexicographic order. These expressions form an ordered field, and the simplex method works over any ordered field.

## The algorithm

```pseudo id=main
BIG-M(A, b, c)
L1  for each row i with b_i < 0, multiply row i and b_i by −1; add the artificial a_i
L2  B ← the artificial columns                     ▷ x = 0, a = b is feasible
L3  run SIMPLEX on min cᵀx + M·1ᵀa from B          ▷ compare costs pM + q as pairs (p, q)
L4  if it returns UNBOUNDED with ray d
L5      if some a_i > 0 at the last basis
L6          run SIMPLEX on min 1ᵀa from that basis; if the optimum is > 0 then return INFEASIBLE
L7  if it returns OPTIMAL and some a_i > 0 then return INFEASIBLE   ▷ Farkas vector from the M-parts
L8  return the answer of line L3 (with the feasible x of line L6 if it ran)
```

Line L3 is the [simplex method](/simplex-method/) with [Bland's rule](/bland-rule/). A reduced cost $pM + q$ is negative if $p < 0$, or if $p = 0$ and $q < 0$. So a column that lowers the sum of the artificials always counts as improving, whatever its real cost.

Line L7: at a symbolic optimum each reduced cost has $p \ge 0$. So the basis is also optimal for the program $\min \mathbf 1^\top a$ alone, which is phase one of the [two-phase method](/two-phase-simplex-method/). If the sum of the artificials is still positive there, no feasible $x$ exists, and the M-parts of the dual give the Farkas vector, just as in phase one.

Lines L4 to L6 handle a case that is easy to miss. The simplex method can find a ray of descent before the artificials reach zero. The M-part of the cost of the ray is $\mathbf 1^\top d_a \ge 0$ and also $\le 0$, so the ray has $d_a = 0$: it is a ray of the original program. But the original program can still be infeasible. Line L6 decides this: it continues with the M-part of the objective alone, from the same basis.

## Example

Minimize $2x_1 + 3x_2$ subject to $x_1 + x_2 - x_3 = 4$, $x_1 + 3x_2 - x_4 = 6$ and $x \ge 0$. This is the example of the [two-phase method](/two-phase-simplex-method/). Add $a_1$ and $a_2$ with the cost $M$ each.

| step | basis | basic values | objective | reduced costs of $x_1, x_2, x_3, x_4$ | entering | leaving |
|---|---|---|---|---|---|---|
| 0 | $(a_1, a_2)$ | $4, 6$ | $10M$ | $2 - 2M$, $3 - 4M$, $M$, $M$ | $x_1$ | $a_1$ (ratios $4, 6$) |
| 1 | $(x_1, a_2)$ | $4, 2$ | $2M + 8$ | $0$, $1 - 2M$, $2 - M$, $M$ | $x_2$ | $a_2$ (ratios $4, 1$) |
| 2 | $(x_1, x_2)$ | $3, 1$ | $9$ | $0, 0, 3/2, 1/2$ | | |

Bland's rule takes the least index with a negative reduced cost, so $x_1$ enters first, then $x_2$. At step 2 the reduced costs of the artificials are $M - 3/2$ and $M - 1/2$, both positive, so $x^* = (3, 1)$ is optimal with value $9$, the same as with two phases.

Now take $M = 1$ as a number. The point $x_2 = 2$, $a_1 = 2$ (with $x_1 = x_3 = x_4 = 0$, $a_2 = 0$) costs $6 + 2M = 8 < 9$, so the penalized optimum keeps $a_1 = 2$, and the method reports that the program is infeasible. That is wrong. The optimal dual vector of the original program is $y^* = (3/2, 1/2)$, and the numeric method is exact here exactly when $M$ is large enough, see the correctness section.

## Correctness

With a symbolic $M$, line L3 is the simplex method over an ordered field, so it is correct and stops under Bland's rule. If it ends optimal with $a = 0$, then $x$ is optimal for the original program, since each feasible $x'$ gives the penalized point $(x', 0)$ with cost $c^\top x'$. If it ends optimal with some $a_i > 0$, the basis is optimal for $\min \mathbf 1^\top a$, so the program is infeasible. If it ends with a ray, the ray has $d_a = 0$, and line L6 decides feasibility. The proof file gives the details.

With a number $M$: the dual of the penalized program is $\max\{b^\top y : A^\top y \le c,\ y \le M \mathbf 1\}$. If the original program has an optimal dual vector $y^*$ with $y^*_i < M$ for each $i$ (after the sign changes of line L1), then $y^*$ is also optimal for this dual, and [complementary slackness](/complementary-slackness/) with $y_i < M$ forces $a_i = 0$ at every penalized optimum. So the numeric method is correct for $M > \max_i y^*_i$. A bound on $y^*$ in terms of the bit length of the input exists, but it gives a number $M$ with very many digits.

## Complexity

Model: arithmetic operations on rationals have unit cost (the [real RAM](/real-ram/)).

- **One pivot.** The tableau has $m$ rows and $n + m + 1$ columns, and two cost rows for the pair $(p, q)$, so a pivot takes $O(m(n + m))$ operations.
- **The number of pivots.** Lines L3 and L6 visit distinct bases of a matrix with $n + m$ columns, so each makes at most $\binom{n+m}{m} \le 2^{n+m}$ pivots. This gives the bound $O(2^{n+m} m(n+m))$ of the front matter.
- **Space.** $O(m(n + m))$ entries.

## Properties

- **One run.** In the common case there is no second phase: the run that removes the artificials also optimizes $c^\top x$.
- **Exact only with a symbolic or a large enough $M$.** A fixed numeric $M$ can be too small, and a very large numeric $M$ causes rounding problems in floating point.
- **Same final basis as the two-phase method** in many cases, but the path can differ, because the real costs take part in the choices of the early pivots.

## Variants and improvements

- **[Two-phase method](/two-phase-simplex-method/).** It separates the two parts of the objective: first $\mathbf 1^\top a$ alone, then $c^\top x$ alone. It needs no choice of $M$.
- **One artificial variable.** For constraints $Ax \le b$ a single artificial column is enough, as in the [initial basic feasible solution](/initial-basic-feasible-solution/) method; the penalty is then $M x_0$.
- **Composite and weighted phase one.** Some solvers minimize the weighted sum $\mathbf 1^\top a + \epsilon\, c^\top x$ with a small $\epsilon$, which is the big-M objective divided by $M$.
- **Exact penalty in nonlinear optimization.** The same idea, a penalty that is exact once its weight passes the size of the optimal multipliers, is the $\ell_1$ exact penalty method.

## When to use it

Use the big-M method for hand calculation or teaching, where one table is easier than two, and in exact arithmetic with a symbolic $M$. In floating-point code the [two-phase method](/two-phase-simplex-method/) is safer, since it needs no large constant. If you know a bound on the optimal dual vector, a numeric $M$ just above that bound is enough.

## Pitfalls

- **A numeric $M$ that is too small.** In the example, $M = 1$ makes a feasible program look infeasible. The method is exact only if $M$ is larger than each entry of some optimal dual vector.
- **A ray with a positive artificial.** For $-x_1 = 2$ with the objective $\min -x_2$, the column of $x_2$ is a ray of cost $-1$ at the first basis, where $a_1 = 2$. A method that stops there reports "unbounded", but the program is infeasible. With any numeric $M$, even $M = 10^6$, the implementation shows this wrong answer. Line L6 is needed.
- **A very large $M$ in floating point.** Costs such as $10^{12} + 3$ lose the real part $3$ to rounding, so the method cannot see the real objective. Keep the two parts apart as a pair.
- **Forgetting the sign changes of line L1.** Without them, the artificial basis is not feasible for rows with $b_i < 0$.

## Implementations

The Python version keeps a dense tableau of `Fraction` values and two cost rows, one for the M-parts and one for the constants. `big_m_method(a, b, c)` uses a symbolic $M$; `big_m_method(a, b, c, M=...)` uses a number, which is there to show the failure for a small $M$. The tests compare the symbolic method with an enumeration of all bases on 800 random programs, check the ray and the Farkas certificate, and check that line L6 is needed in both directions: some runs find a ray with a positive artificial and end infeasible, and some end unbounded.

## History

The method of a large penalty on artificial variables is usually credited to Abraham Charnes and his coworkers in the early 1950s, at about the same time as the first phase-one methods of Dantzig. It became a standard textbook way to start the simplex method by hand, together with the two-phase method.

## References
