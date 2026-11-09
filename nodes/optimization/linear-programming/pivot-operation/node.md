---
tag: 42KVK6
kind: concept
slug: pivot-operation
name: Pivot operation
aliases:
- basis exchange
- Gauss-Jordan pivot
- simplex pivot
area: optimization/linear-programming
level: core
summary: Swap one basic and one nonbasic variable, moving to an adjacent vertex.
prereqs: [lp-standard-form, basic-feasible-solution, gauss-jordan-elimination]
see_also: [simplex-method, ratio-test, dantzig-pivot-rule, bland-rule, lp-degeneracy, revised-simplex-method, reduced-cost, sherman-morrison-formula]
sources:
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Section 3.2, Development of the simplex method (adjacent bases, one iteration) and Section 3.3, Implementations of the simplex method (the full tableau and the update of the inverse basis matrix)
  - book: isbn:9780716715870
    title: Vašek Chvátal, Linear Programming, W. H. Freeman, 1983
    locator: Chapter 2, How the simplex method works (pivoting on dictionaries), and Chapter 7, The revised simplex method (eta matrices)
  - book: isbn:9780471982326
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Chapter 11, The simplex method (the tableau form and the pivot step)
---

A pivot operation is the basic step of the [simplex method](/simplex-method/): one variable leaves the basis, one variable enters it, and the tableau is rewritten by one step of [Gauss-Jordan elimination](/gauss-jordan-elimination/). In the geometry of the [feasible region](/polyhedron/), a pivot moves from a [basic feasible solution](/basic-feasible-solution/) to an adjacent one along an edge, or stays at the same vertex when the step length is zero. Each pivot costs $O(mn)$ arithmetic operations on a full tableau with $m$ rows and $n$ columns.

## In plain words

A vertex of the feasible region is fixed by a set of equations, one for each basic variable. A pivot swaps one equation for another. One variable that was held at zero is allowed to grow, and one of the variables that were free to move is pushed down to zero and held there. The point slides along an edge of the region to the next corner.

To keep the bookkeeping right, the method rewrites the table of equations. It divides the row of the leaving variable so that the entering variable has coefficient one there, and subtracts multiples of that row from all other rows so that the entering variable disappears from them. This is the same step that school algebra uses to solve linear equations.

## The idea

**Setting.** The program is in [standard form](/lp-standard-form/): minimize $c^\top x$ subject to $Ax = b$, $x \ge 0$, with $A \in \mathbb{R}^{m \times n}$ of rank $m$. A basis is a list $B(1), \ldots, B(m)$ of column indices such that the matrix $B = [A_{B(1)} \cdots A_{B(m)}]$ is nonsingular. The tableau is $T = B^{-1}[A \mid b]$ together with the cost row of [reduced costs](/reduced-cost/) $r = c^\top - c_B^\top B^{-1} A$ and the value $z = c_B^\top B^{-1} b$. Row $i$ of $T$ expresses the basic variable $x_{B(i)}$ in terms of the nonbasic ones.

**The pivot.** Choose an entering column $q$ (nonbasic) and a pivot row $p$ with $t_{pq} \ne 0$. Write $d = B^{-1} A_q$, the column $q$ of the tableau, so $t_{pq} = d_p$. The pivot on $(p, q)$ does:

1. Divide row $p$ of $T$ by $d_p$.
2. For each row $i \ne p$, subtract $d_i$ times the new row $p$ from row $i$.
3. Subtract $r_q$ times the new row $p$ from the cost row.
4. Set $B(p) \leftarrow q$.

After the pivot, column $q$ is the unit vector $e_p$, $r_q = 0$, and the tableau is $B'^{-1}[A \mid b]$ for the new basis $B'$. The [pivot rule](/dantzig-pivot-rule/) picks $q$ with $r_q < 0$, and the [ratio test](/ratio-test/) picks $p$ so that the new basic solution stays feasible.

**The new inverse.** Since $B' = B + (A_q - A_{B(p)}) e_p^\top = B\,(I + (d - e_p) e_p^\top)$, the new inverse is $B'^{-1} = E\, B^{-1}$, where the *eta matrix* $E$ is the identity with column $p$ replaced by $\eta$, with $\eta_p = 1/d_p$ and $\eta_i = -d_i/d_p$ for $i \ne p$. Proof: $Ed = e_p$ by the definition of $\eta$, so $E(I + (d - e_p)e_p^\top) = E + (e_p - \eta)e_p^\top$, which is $E$ with column $p$ replaced by $e_p$, that is $I$. By the matrix determinant lemma, $\det B' = \det B \cdot (1 + e_p^\top(d - e_p)) = d_p \det B$, so $B'$ is a basis exactly when $d_p \ne 0$. The [revised simplex method](/revised-simplex-method/) stores the product of such eta matrices instead of the tableau; this is a rank-one update in the sense of the [Sherman-Morrison formula](/sherman-morrison-formula/).

**What a pivot does to the point.** Let $\theta = x_{B(p)}/d_p$ be the step length. The new basic solution is $x' = x + \theta\, \delta$, where $\delta_q = 1$, $\delta_{B(i)} = -d_i$ and $\delta_j = 0$ for the other nonbasic $j$. So $A\delta = 0$, and $\delta$ is the direction of an edge of the feasible region when the solution is nondegenerate. The value changes by $c^\top x' - c^\top x = \theta\, r_q$. If $\theta > 0$, the pivot moves to an adjacent vertex. If $\theta = 0$, which needs a basic variable at zero, the pivot changes the basis but not the point: a *degenerate pivot* (see [degeneracy](/lp-degeneracy/)).

**Cost.** Steps 1 to 3 touch every entry of the tableau once: $O(mn)$ operations. The revised method computes only the column $d$ and one row, at a cost of $O(m^2 + mn)$ with an explicit inverse, and less with sparse LU factors.

## Examples

**Two pivots to the optimum.** Minimize $-x_1 - x_2$ subject to $x_1 + 2x_2 + s_1 = 4$, $3x_1 + x_2 + s_2 = 6$, $x \ge 0$. The slack basis $\{s_1, s_2\}$ is feasible at the vertex $(x_1, x_2) = (0, 0)$.

| basic | $x_1$ | $x_2$ | $s_1$ | $s_2$ | value |
|---|---|---|---|---|---|
| $s_1$ | 1 | 2 | 1 | 0 | 4 |
| $s_2$ | **3** | 1 | 0 | 1 | 6 |
| $r$ | $-1$ | $-1$ | 0 | 0 | $z = 0$ |

Column $x_1$ enters. The ratios are $4/1 = 4$ and $6/3 = 2$, so row $s_2$ leaves, and the pivot element is $3$. Divide row 2 by 3, then subtract it once from row 1 and add it once to the cost row:

| basic | $x_1$ | $x_2$ | $s_1$ | $s_2$ | value |
|---|---|---|---|---|---|
| $s_1$ | 0 | **5/3** | 1 | $-1/3$ | 2 |
| $x_1$ | 1 | 1/3 | 0 | 1/3 | 2 |
| $r$ | 0 | $-2/3$ | 0 | 1/3 | $z = -2$ |

The point moved to $(2, 0)$ with step $\theta = 2$, and the value fell by $\theta \cdot |r_q| = 2$. Now $x_2$ enters, with ratios $2/(5/3) = 6/5$ and $2/(1/3) = 6$, so $s_1$ leaves:

| basic | $x_1$ | $x_2$ | $s_1$ | $s_2$ | value |
|---|---|---|---|---|---|
| $x_2$ | 0 | 1 | 3/5 | $-1/5$ | 6/5 |
| $x_1$ | 1 | 0 | $-1/5$ | 2/5 | 8/5 |
| $r$ | 0 | 0 | 2/5 | 1/5 | $z = -14/5$ |

All reduced costs are now nonnegative, so $(8/5, 6/5)$ is optimal. Since the slack columns of $A$ form the identity, the slack columns of each tableau hold $B^{-1}$. After the first pivot this is $\begin{pmatrix} 1 & -1/3 \\ 0 & 1/3 \end{pmatrix}$, the eta matrix for $d = (1, 3)$ and $p = 2$, and $\det B' = 3 \cdot \det I = 3$. After the second pivot, $d = (5/3, 1/3)$ and $p = 1$, so $\det B'' = (5/3) \cdot 3 = 5$, which is $\det \begin{pmatrix} 2 & 1 \\ 1 & 3 \end{pmatrix}$ for the columns of $x_2$ and $x_1$.

**A pivot that does not move.** With $x_1 \le 1$, $x_2 \le 1$ and $x_1 + x_2 \le 2$, the vertex $(1, 1)$ makes all three slacks zero. The bases $\{x_1, x_2, s_1\}$, $\{x_1, x_2, s_2\}$ and $\{x_1, x_2, s_3\}$ all give this vertex, and a pivot from one to another has $\theta = 0$.

**A pivot on a negative element.** Pivoting on $t_{pq} < 0$ is legal algebra and gives a basis, but the new basic solution has $x_q = \theta < 0$ when $x_{B(p)} > 0$, so it leaves the feasible region. The primal simplex method never does this. The [dual simplex method](/dual-simplex-method/) does pivot on negative elements, on purpose, to keep the reduced costs nonnegative.

## Where it is used

- **The simplex method and its variants.** Every iteration of the primal, [dual](/dual-simplex-method/) and [two-phase](/two-phase-simplex-method/) methods is one pivot. Pivot rules such as [Dantzig's rule](/dantzig-pivot-rule/), [Bland's rule](/bland-rule/) and the [steepest-edge rule](/steepest-edge-pivot-rule/) differ only in the choice of $q$ (and of $p$ on ties).
- **Linear algebra.** [Gauss-Jordan elimination](/gauss-jordan-elimination/) is a sequence of pivots, one for each column; it computes $A^{-1}$ or the reduced row echelon form. In numerical work, the choice of a large pivot element for stability is [partial pivoting](/partial-pivoting/); the word "pivot" means the same entry there.
- **Exact arithmetic.** Integer pivoting, as in the [Bareiss algorithm](/bareiss-algorithm/), keeps all entries integral by dividing by the previous pivot.
- **Basis exchange.** In a [linear matroid](/linear-matroid/), a pivot is a basis exchange: $B - \{B(p)\} + \{q\}$ is a basis exactly when $d_p \ne 0$.
- **Other pivoting methods.** Lemke's method for the linear complementarity problem and the criss-cross method also move between bases by pivots, with other rules for the choice of $(p, q)$.

## References
