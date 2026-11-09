---
tag: 0XTBN3
kind: algorithm
slug: revised-simplex-method
name: Revised simplex method
aliases:
- revised simplex
- simplex method with multipliers
area: optimization/linear-programming
level: advanced
summary: Simplex variant that maintains a basis inverse, efficient for sparse large LPs.
solves: [linear-programming-problem]
model: real-ram
complexity:
  vars: {n: the number of variables, m: the number of equality constraints}
  time: {worst: O(2^n m n)}
  space: {extra: O(m^2)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
prereqs: [simplex-method, reduced-cost, lu-decomposition]
see_also: [simplex-method, pivot-operation, dual-simplex-method, column-generation, lu-decomposition, sherman-morrison-formula, steepest-edge-pivot-rule, ratio-test]
sources:
  - book: isbn:9780716715870
    title: Vašek Chvátal, Linear Programming, W. H. Freeman, 1983
    locator: Chapter 7, The revised simplex method (eta file, refactorization)
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Section 3.3, Implementations of the simplex method (naive implementation, revised simplex method, full tableau, comparison of their costs)
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006
    locator: Chapter 13, The simplex method (linear algebra in the simplex method, LU factors and their updates)
  - paper: doi:10.1090/s0025-5718-1954-0061469-8
    title: George B. Dantzig and William Orchard-Hays, The product form for the inverse in the simplex method, Mathematical Tables and Other Aids to Computation 8(46), 1954
    locator: pages 64 to 67, the product form of the inverse
  - paper: doi:10.1145/362946.362974
    title: Richard H. Bartels and Gene H. Golub, The simplex method of linear programming using LU decomposition, Communications of the ACM 12(5), 1969
    locator: pages 266 to 268, stable updates of LU factors of the basis
  - paper: doi:10.1007/bf01584548
    title: J. J. H. Forrest and J. A. Tomlin, Updated triangular factors of the basis to maintain sparsity in the product form simplex method, Mathematical Programming 2, 1972
    locator: pages 263 to 278
---

The revised simplex method is the [simplex method](/simplex-method/) organized so that each iteration does only the work that the pivot needs. It does not keep the whole tableau $A_B^{-1} A$. It keeps a representation of the basis inverse $A_B^{-1}$, an explicit matrix, a product of eta matrices, or an LU factorization, and from it computes the multipliers, the reduced costs and one column per iteration. For a program with many more columns than rows, or with sparse columns, this costs much less than the tableau, and it is the form of the simplex method in all serious LP solvers.

## In plain words

The tableau form of the simplex method rewrites every number of the problem at every step, but each step uses only one column of the rewritten table and one row of prices. The revised method keeps only a small key, the inverse of the current basis matrix. With the key it can compute the prices of the constraints, check each column against the prices, and rebuild only the one column that it needs for the next move.

After a move, the key changes by a simple update that touches one column of information. From time to time the key is rebuilt from scratch, which removes the build-up of rounding errors in floating point and keeps the key small for sparse problems.

## The problem

The problem is the same as for the [simplex method](/simplex-method/): minimize $c^\top x$ subject to $Ax = b$, $x \ge 0$, with $A \in \mathbb{Q}^{m \times n}$ of rank $m$, from a feasible basis $B$. The output is an optimal basic feasible solution with the dual vector $y$, or a ray of descent.

## The algorithm

```pseudo id=main
REVISED-SIMPLEX(A, b, c, B)
L1  B⁻¹ ← A_B⁻¹;  x_B ← B⁻¹ b
L2  loop
L3      yᵀ ← c_Bᵀ B⁻¹                                ▷ BTRAN: the simplex multipliers
L4      r_j ← c_j − yᵀA_j for j ∉ B;  if r ≥ 0 then return OPTIMAL(x, y)    ▷ pricing
L5      choose q with r_q < 0                         ▷ the pivot rule
L6      d ← B⁻¹ A_q;  if d ≤ 0 then return UNBOUNDED  ▷ FTRAN: one column
L7      p ← the ratio test on x_B and d;  θ ← x_B(p) / d_p
L8      x_B ← x_B − θ d;  x_B(p) ← θ;  B(p) ← q
L9      B⁻¹ ← E B⁻¹                                   ▷ E: the eta matrix of the pivot
```

Line L3 solves $y^\top A_B = c_B^\top$, called BTRAN (backward transformation). Line L4, *pricing*, computes a [reduced cost](/reduced-cost/) $r_j = c_j - y^\top A_j$ for each nonbasic column; this is the only step that touches all of $A$. Many solvers price only part of the columns per iteration (partial pricing). In [column generation](/column-generation/) the columns are not even stored: a separate optimization problem finds a column with $r_j < 0$.

Line L6 computes the entering column $d = A_B^{-1} A_q$, called FTRAN (forward transformation), and line L7 is the [ratio test](/ratio-test/) on it.

Line L9 updates the inverse. The new basis matrix is $A_{B'} = A_B + (A_q - A_{B(p)}) e_p^\top$, a rank-one change. Its inverse is $E A_B^{-1}$, where $E$ is the identity matrix with column $p$ replaced by the *eta vector*

$$\eta_p = \frac{1}{d_p}, \qquad \eta_i = -\frac{d_i}{d_p}\ (i \ne p).$$

So $E A_B^{-1}$ divides row $p$ of $A_B^{-1}$ by $d_p$ and subtracts $d_i$ times the new row $p$ from each row $i$. This is the [pivot operation](/pivot-operation/) on the $m \times m$ matrix $A_B^{-1}$ instead of the $m \times n$ tableau, and it is the [Sherman-Morrison formula](/sherman-morrison-formula/) for this rank-one change.

There are three common ways to store $A_B^{-1}$:

- **Explicit inverse.** An $m \times m$ matrix, updated by line L9 in $O(m^2)$ operations. This is the form of the implementation on this page.
- **Product form.** Keep $A_B^{-1} = E_k \cdots E_1 A_{B_0}^{-1}$ as a list of eta vectors (the *eta file*), and apply them one by one in BTRAN and FTRAN. Each pivot adds one eta vector.
- **LU factors.** Keep an [LU decomposition](/lu-decomposition/) of $A_B$ and update it after each pivot, by the method of Bartels and Golub or of Forrest and Tomlin. After some tens of pivots the solver *refactorizes* $A_B$ from scratch.

## Example

The program of the [simplex method](/simplex-method/) page: minimize $-3x_1 - 5x_2$ subject to $x_1 + x_3 = 4$, $2x_2 + x_4 = 12$, $3x_1 + 2x_2 + x_5 = 18$, from the slack basis $(x_3, x_4, x_5)$ with $A_B^{-1} = I$, and with Dantzig's rule.

| step | basis | $A_B^{-1}$ (rows) | $y$ | $r$ of the nonbasic columns | entering, $d$ | $\theta$, leaving |
|---|---|---|---|---|---|---|
| 0 | $(x_3, x_4, x_5)$ | $(1, 0, 0)$, $(0, 1, 0)$, $(0, 0, 1)$ | $(0, 0, 0)$ | $r_1 = -3$, $r_2 = -5$ | $x_2$, $(0, 2, 2)$ | $6$, $x_4$ |
| 1 | $(x_3, x_2, x_5)$ | $(1, 0, 0)$, $(0, 1/2, 0)$, $(0, -1, 1)$ | $(0, -5/2, 0)$ | $r_1 = -3$, $r_4 = 5/2$ | $x_1$, $(1, 0, 3)$ | $2$, $x_5$ |
| 2 | $(x_3, x_2, x_1)$ | $(1, 1/3, -1/3)$, $(0, 1/2, 0)$, $(0, -1/3, 1/3)$ | $(0, -3/2, -1)$ | $r_4 = 3/2$, $r_5 = 1$ | | |

At step 1 the eta update divides row 2 of $I$ by $d_2 = 2$ and subtracts $2$ times the new row 2 from row 3. At step 2 the update divides row 3 by $d_3 = 3$ and subtracts $1$ times the new row 3 from row 1. The final $x_B = (2, 6, 2)$ gives $x^* = (2, 6, 2, 0, 0)$ with value $-36$, and $y$ is the dual solution. The path and the pivots are those of the tableau method; only the bookkeeping differs.

## Correctness

The revised method makes the same choices as the tableau method from the same basis: lines L3 and L4 compute the same reduced costs, line L6 the same column $d$, and line L7 the same row. So the [correctness proof of the simplex method](/simplex-method/) applies, once we know that line L9 keeps the invariant that the stored matrix is the inverse of the current basis matrix. That holds because $E A_B^{-1} A_{B'} = I$, which the proof file checks column by column.

## Complexity

Model: arithmetic operations on rationals have unit cost (the [real RAM](/real-ram/)).

- **One iteration with an explicit inverse.** BTRAN, FTRAN and the update each take $O(m^2)$. Pricing all columns takes $O(mn)$, or $O(\text{nnz}(A))$ for a sparse $A$. So an iteration costs $O(m^2 + mn)$, against $O(mn)$ for the tableau, but with a much smaller constant when $n \gg m$, and with partial pricing the $O(mn)$ term shrinks too.
- **Sparse problems.** With LU factors, BTRAN and FTRAN cost about the number of nonzeros of the factors, which for real problems is often close to linear in $m$. The tableau, in contrast, fills in and becomes dense.
- **The number of pivots.** The same as for the tableau method with the same rule: at most $\binom{n}{m} \le 2^n$ without cycling, and exponential in the worst case. This gives the bound $O(2^n m n)$ of the front matter.
- **Space.** $O(m^2)$ for the inverse, besides the input.

## Properties

- **Same path as the tableau method.** It visits the same bases with the same rule; only the cost per step differs.
- **Works with implicit columns.** Only the pricing step needs the columns, so columns can be generated on demand.
- **Good for sparse input.** $A$ is never changed, so its sparsity is kept.
- **Numerically controllable.** Refactorization from time to time resets the rounding errors that the updates collect in floating point.

## Variants and improvements

- **Product form of the inverse** (Dantzig and Orchard-Hays, 1954): store the eta vectors instead of the inverse.
- **LU updates** (Bartels and Golub, 1969; Forrest and Tomlin, 1972): store sparse LU factors of $A_B$ and update them, which is stable and keeps the fill small.
- **Partial and multiple pricing.** Price only a part of the columns in each iteration, and keep a short list of candidates.
- **[Steepest-edge pricing](/steepest-edge-pivot-rule/).** It needs the norms $\|A_B^{-1} A_j\|$ of all columns; Goldfarb and Reid gave update formulas for them that fit the revised method.
- **Bounded variables.** Nonbasic variables sit at a lower or an upper bound, and the ratio test also stops at the bound of the entering variable.
- **[Dual simplex method](/dual-simplex-method/).** It uses the same factorization, with BTRAN for a row of $A_B^{-1}$ instead of FTRAN for a column.

## When to use it

Use the revised method whenever the program is large, sparse, or has many more columns than rows, and whenever the columns are generated as needed, as in [column generation](/column-generation/) and [Dantzig-Wolfe decomposition](/dantzig-wolfe-decomposition/). The full tableau is simpler for small dense programs and for hand calculation.

## Pitfalls

- **Forgetting the order of the eta matrices.** The update is $A_{B'}^{-1} = E A_B^{-1}$, with $E$ on the left. In the product form, FTRAN applies the eta vectors from the oldest to the newest, and BTRAN from the newest to the oldest.
- **No refactorization in floating point.** After many updates the stored inverse drifts from the true one. Solvers refactorize after a fixed number of updates, or when a check such as $\|A_B x_B - b\|$ grows.
- **Pricing with a stale $y$.** The multipliers must be recomputed (or updated) after each pivot; the reduced costs depend on the new basis.
- **The same cycling risks as the tableau method.** The revised method changes only the bookkeeping. Under Dantzig's rule it cycles on Beale's example; the tests check this.

## Implementations

The Python version keeps an explicit inverse of `Fraction` values and updates it by the eta matrix of each pivot. `revised_simplex_method(a, b, c, basis, rule)` starts from a feasible basis and supports Bland's rule and Dantzig's rule. It accepts a callback, which the tests use to check $A_B^{-1} A_B = I$ and $A_B^{-1} b \ge 0$ after each pivot. The tests also compare the result with an enumeration of all bases on 600 random programs with random feasible starting bases, check the certificates, check that Dantzig's rule cycles on Beale's example and takes $2^n - 1$ pivots on the [Klee-Minty cube](/klee-minty-cube/) for $n \le 6$.

## History

Dantzig and Orchard-Hays developed the revised simplex method at RAND around 1953, for the computers of the time, which had little memory: storing the inverse in product form took much less space than the tableau. Bartels and Golub (1969) replaced the product form by updates of an LU factorization, which is numerically stable, and Forrest and Tomlin (1972) gave the sparse update that many later codes used.

## References
