---
tag: ZJJC0W
kind: concept
slug: ratio-test
name: Minimum ratio test
aliases:
- leaving variable rule
- ratio test
area: optimization/linear-programming
level: core
summary: Choose the leaving variable that keeps the next basic solution feasible.
prereqs: [lp-standard-form, basic-feasible-solution, pivot-operation]
see_also: [simplex-method, pivot-operation, bland-rule, lp-degeneracy, dual-simplex-method, dantzig-pivot-rule, steepest-edge-pivot-rule, simplex-termination]
sources:
  - book: isbn:9781886529199
    title: Dimitris Bertsimas and John N. Tsitsiklis, Introduction to Linear Optimization, Athena Scientific, 1997
    locator: Section 3.2, Development of the simplex method (the step length theta*), Section 3.4, Anticycling (the lexicographic rule and Bland's rule) and Section 4.5 (the dual simplex method)
  - book: isbn:9780716715870
    title: Vašek Chvátal, Linear Programming, W. H. Freeman, 1983
    locator: Chapter 2, How the simplex method works (the choice of the leaving variable) and Chapter 3, Pitfalls and how to avoid them (ties, degeneracy, the perturbation and smallest subscript rules)
  - paper: doi:10.2140/pjm.1955.5.183
    title: George B. Dantzig, Alex Orden and Philip Wolfe, The generalized simplex method for minimizing a linear form under linear inequality restraints, Pacific Journal of Mathematics 5(2), 1955
    locator: pages 183 to 195, the lexicographic choice of the leaving variable
  - paper: doi:10.1007/BF01580108
    title: Paula M. J. Harris, Pivot selection methods of the Devex LP code, Mathematical Programming 5, 1973
    locator: pages 1 to 28, the two-pass ratio test with a tolerance
---

The minimum ratio test is the rule that picks the leaving variable in a [pivot](/pivot-operation/) of the [simplex method](/simplex-method/). Once a column $q$ is chosen to enter, the entering variable grows from zero, and each basic variable changes linearly; the test finds the largest step for which no basic variable becomes negative, and the basic variable that first reaches zero leaves. If no basic variable decreases, there is no limit, and the program is unbounded.

## In plain words

Picture the current corner of the feasible region and one edge that leaves it. Walking along the edge improves the objective, so the method walks as far as it can. Each constraint that the walk moves toward gives a stopping distance: the distance at which that constraint would be broken. The method stops at the nearest one. That constraint becomes the new tight one, and its variable leaves the basis.

If the walk moves toward no constraint, it can go on for ever, and the objective improves without limit. If two constraints give the same nearest distance, the new corner touches both of them, and the method has to break the tie with care, or it can go round in circles.

## The idea

**Setting.** The program is in [standard form](/lp-standard-form/), minimize $c^\top x$ subject to $Ax = b$, $x \ge 0$, with a feasible basis $B$ and basic solution $x_B = B^{-1}b \ge 0$, $x_N = 0$. The entering column $q$ has [reduced cost](/reduced-cost/) $r_q < 0$. Let $d = B^{-1}A_q$. If $x_q$ grows to $\theta \ge 0$ and the other nonbasic variables stay at $0$, then $Ax = b$ forces
$$x_B(\theta) = x_B - \theta d, \qquad c^\top x(\theta) = c^\top x + \theta r_q.$$

**The test.** The point $x(\theta)$ is feasible exactly when $x_{B(i)} - \theta d_i \ge 0$ for all $i$. For $d_i \le 0$ this holds for every $\theta \ge 0$. For $d_i > 0$ it means $\theta \le x_{B(i)}/d_i$. So:

- If $d \le 0$, every $\theta \ge 0$ is feasible, and $c^\top x(\theta) \to -\infty$: the program is UNBOUNDED, with the ray $x(\theta)$ as a certificate.
- Otherwise the largest feasible step is
$$\theta^* = \min\left\{ \frac{x_{B(i)}}{d_i} : d_i > 0 \right\},$$
and the leaving row $p$ is a row that attains the minimum. Since $d_p > 0$, the new basis $B - \{B(p)\} + \{q\}$ is nonsingular (its determinant is $d_p \det B$), and its basic solution is $x(\theta^*) \ge 0$, so it is a feasible basis again.

Any larger step makes $x_{B(p)}$ negative, and any row with $d_i > 0$ that does not attain the minimum would give an infeasible basic solution if it left. So the test is the only choice of $p$ that keeps the next basis feasible, up to ties.

**Ties.** If several rows attain $\theta^*$, then after the pivot every tied row other than $p$ has the value $0$: the new basic solution is [degenerate](/lp-degeneracy/). Two tie rules prevent cycling:

- [Bland's rule](/bland-rule/): take the tied row whose basic variable has the smallest index (together with the smallest-index choice of $q$).
- The *lexicographic rule* of Dantzig, Orden and Wolfe (1955): divide each candidate row $(x_{B(i)}, (B^{-1})_{i,\cdot})$ by $d_i$ and take the lexicographically least. Two different rows $i \ne k$ cannot give the same vector, since then rows $i$ and $k$ of $B^{-1}$ would be proportional. So the choice is unique. If these rows are lexicographically positive at the start, as they are for a slack basis with $x_B \ge 0$ and $B = I$, they stay so. A pivot adds the positive multiple $-r_q/d_p$ of the lexicographically positive row $p$ to the vector $(-z, -c_B^\top B^{-1})$, so this vector increases strictly in the lexicographic order at each pivot, and no basis repeats (Bertsimas and Tsitsiklis, Section 3.4).

**Step length zero.** If $\theta^* = 0$, the basis changes and the point stays. This is a degenerate pivot. It happens exactly when some row with $d_i > 0$ has $x_{B(i)} = 0$.

## Examples

**The first pivot of a small program.** Minimize $-x_1 - x_2$ subject to $x_1 + 2x_2 + s_1 = 4$, $3x_1 + x_2 + s_2 = 6$, from the slack basis with $x_B = (4, 6)$. For $q = x_1$, $d = (1, 3)$, and the ratios are $4/1 = 4$ and $6/3 = 2$. So $\theta^* = 2$, $s_2$ leaves, and the new point is $x_1 = 2$, $s_1 = 4 - 2 \cdot 1 = 2$, $s_2 = 0$, with the value $0 + 2 \cdot (-1) = -2$. Choosing $s_1$ instead would give $x_1 = 4$ and $s_2 = 6 - 4 \cdot 3 = -6 < 0$.

**A tie.** Change the right side to $(4, 12)$. Now both ratios are $4$. Whichever row leaves, the other basic variable becomes $0$: with $s_2$ leaving, the new row of $s_1$ is $0 \cdot x_1 + \tfrac53 x_2 + s_1 - \tfrac13 s_2 = 0$. The next pivot with $x_2$ entering has ratio $0/(5/3) = 0$, a degenerate pivot.

**Unbounded.** Minimize $-x_1$ subject to $x_1 - x_2 + s_1 = 1$. The first pivot ($x_1$ enters, ratio $1/1$) gives $x_1 = 1 + x_2 - s_1$ and the cost $-1 - x_2 + s_1$. Then $x_2$ has reduced cost $-1$ and column $d = (-1) \le 0$, so the test finds no limit: the points $(x_1, x_2) = (1 + t, t)$ are feasible for all $t \ge 0$ with value $-1 - t$.

## Where it is used

- **The primal simplex method.** Every pivot of the [simplex method](/simplex-method/), of the [revised simplex method](/revised-simplex-method/) and of phase one of the [two-phase method](/two-phase-simplex-method/).
- **The dual ratio test.** The [dual simplex method](/dual-simplex-method/) first picks a leaving row $p$ with $x_{B(p)} < 0$ and then the entering column by $\min\{ r_j / |t_{pj}| : t_{pj} < 0 \}$, which keeps all reduced costs nonnegative. It is the same test applied to the dual.
- **Bounded variables.** With bounds $\ell \le x \le u$, each basic variable can hit its lower or its upper bound, and the entering variable can reach its own opposite bound (a *bound flip*, with no change of basis). The test takes the least of all these distances.
- **Floating point.** Codes ignore entries $d_i$ below a pivot tolerance, because a tiny pivot element makes the new basis nearly singular. Harris (1973) proposed a two-pass test: the first pass computes the bound $\min\{(x_{B(i)} + \delta)/d_i\}$ with a small feasibility tolerance $\delta$, and the second pass takes, among the rows whose ratio is within this bound, the one with the largest $|d_i|$. This trades a tiny infeasibility for a much safer pivot element, and most production codes use a version of it.
- **Network simplex.** On a network, $d$ is the cycle that the entering arc closes, and the ratio test is the least residual capacity on that cycle in the direction of flow, as in an augmenting path step.

## References
