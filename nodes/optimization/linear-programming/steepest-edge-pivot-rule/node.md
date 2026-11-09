---
tag: 5JPK9M
kind: concept
slug: steepest-edge-pivot-rule
name: Steepest-edge pivot rule
aliases:
- steepest edge
- steepest-edge pricing
area: optimization/linear-programming
level: advanced
summary: Pivot rule that normalizes reduced costs by edge length, usually reducing iteration counts.
prereqs: [simplex-method, reduced-cost, pivot-operation, revised-simplex-method]
see_also: [dantzig-pivot-rule, bland-rule, klee-minty-cube, dual-simplex-method, ratio-test, smoothed-simplex-analysis, simplex-method, lp-degeneracy]
sources:
  - paper: doi:10.1007/BF01593804
    title: Donald Goldfarb and John K. Reid, A practicable steepest-edge simplex algorithm, Mathematical Programming 12, 1977
    locator: pages 361 to 371, the update formulas for the edge norms
  - paper: doi:10.1007/BF01581089
    title: John J. Forrest and Donald Goldfarb, Steepest-edge simplex algorithms for linear programming, Mathematical Programming 57, 1992
    locator: pages 341 to 374, primal and dual steepest-edge rules and their computational comparison with Devex
  - paper: doi:10.1007/BF01580108
    title: Paula M. J. Harris, Pivot selection methods of the Devex LP code, Mathematical Programming 5, 1973
    locator: pages 1 to 28, the Devex approximate weights
  - paper: doi:10.1016/0166-218X(79)90004-0
    title: Donald Goldfarb and William Y. Sit, Worst case behavior of the steepest edge simplex method, Discrete Applied Mathematics 1(4), 1979
    locator: pages 277 to 285, deformed cubes on which the rule takes exponentially many pivots
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006
    locator: Chapter 13, The simplex method (pricing and the selection of the entering index)
---

The steepest-edge pivot rule chooses, in each iteration of the [simplex method](/simplex-method/), the edge from the current vertex along which the objective falls fastest per unit of distance, not per unit of the entering variable. In terms of the tableau it maximizes $r_j^2 / \gamma_j$ over the columns with negative [reduced cost](/reduced-cost/) $r_j$, where $\gamma_j$ is the squared length of the edge direction. Goldfarb and Reid (1977) showed how to update all $\gamma_j$ cheaply after each pivot, and steepest edge, in its primal and dual forms, is the standard rule of modern simplex codes. It still takes exponentially many pivots on some programs.

## In plain words

At a corner of the feasible region, several edges go downhill. [Dantzig's rule](/dantzig-pivot-rule/) measures each edge by how much the objective drops when one variable grows by one unit. But one unit of one variable can be a long step in space and one unit of another a short one, so this compares unlike things.

The steepest-edge rule measures the drop per unit of real distance along the edge, which is the slope of the edge in the direction of the objective. It picks the steepest edge. This choice does not change much when someone changes the units of a variable, and in practice it needs far fewer steps. The cost is the bookkeeping of the length of every edge, which a clever update keeps cheap.

## The idea

**Edge directions.** For minimize $c^\top x$ subject to $Ax = b$, $x \ge 0$ with basis $B$, entering a nonbasic $x_j$ moves the point along the direction $\eta_j \in \mathbb{R}^n$ with
$$(\eta_j)_j = 1, \qquad (\eta_j)_{B} = -B^{-1}A_j, \qquad (\eta_j)_k = 0 \text{ for the other nonbasic } k.$$
Since $A\eta_j = 0$, the change of the objective along the edge is $c^\top \eta_j = c_j - c_B^\top B^{-1} A_j = r_j$.

**The rule.** Let $\gamma_j = \|\eta_j\|^2 = 1 + \|B^{-1}A_j\|^2$. Enter
$$q \in \arg\max \left\{ \frac{r_j^2}{\gamma_j} : r_j < 0 \right\},$$
which is the column with the most negative $c^\top \eta_j / \|\eta_j\|$, the cosine of the angle between $-c$ and the edge, times $\|c\|$. The leaving variable comes from the [ratio test](/ratio-test/).

**The update.** Computing $\gamma_j$ from scratch needs $B^{-1}A_j$ for every nonbasic column, as costly as a full tableau. Goldfarb and Reid update the norms instead. Let $p$ be the pivot row, $d = B^{-1}A_q$, and $\bar\alpha_j = (B^{-1}A_j)_p / d_p$ the entries of the pivot row divided by the pivot element. After the pivot, for each nonbasic $j \ne q$,
$$\eta_j' = \eta_j - \bar\alpha_j \eta_q, \qquad \gamma_j' = \gamma_j - 2\bar\alpha_j\, A_j^\top w + \bar\alpha_j^2 \gamma_q, \quad w = B^{-\top} d,$$
and the leaving variable $\ell = B(p)$ gets $\gamma_\ell' = \gamma_q / d_p^2$. Proof of the first identity: in $\eta_j - \bar\alpha_j \eta_q$ the coefficient of $x_\ell$ is $-(B^{-1}A_j)_p + \bar\alpha_j d_p = 0$, the coefficient of $x_q$ is $-\bar\alpha_j$, which is minus the new tableau entry of column $j$ in the row of $x_q$, and the other basic coefficients are $-((B^{-1}A_j)_i - \bar\alpha_j d_i)$, minus the other new tableau entries. So it is the new edge direction. The second identity is its squared norm, with $\eta_j^\top \eta_q = (B^{-1}A_j)^\top (B^{-1}A_q) = A_j^\top w$. The pivot row is needed anyway to update the reduced costs, so the extra work per pivot is one solve with $B^\top$ and one inner product $A_j^\top w$ for each column with $\bar\alpha_j \ne 0$.

**Approximations and the dual form.** Harris's *Devex* rule (1973) keeps approximate weights relative to a reference set of variables and resets them from time to time; it needs no extra solve. The *dual steepest-edge* rule of Forrest and Goldfarb (1992) chooses the leaving row in the [dual simplex method](/dual-simplex-method/) by $x_{B(i)}^2 / \|e_i^\top B^{-1}\|^2$, with a similar update. The dual form is cheap enough that it is the usual default of dual simplex codes.

**Scaling.** If $x_j = s\,x_j'$, the reduced cost becomes $s\,r_j$ and $\gamma_j$ becomes $1 + s^2\|B^{-1}A_j\|^2$. When $\|B^{-1}A_j\|$ is not small, the ratio $r_j^2/\gamma_j$ hardly changes. The rule is less sensitive to the units than Dantzig's rule, though not fully invariant, since the "1" for the entering variable itself is not scaled.

## Examples

**The Klee-Minty cube in three variables.** Minimize $-100x_1 - 10x_2 - x_3$ subject to $x_1 \le 1$, $20x_1 + x_2 \le 100$, $200x_1 + 20x_2 + x_3 \le 10000$, $x \ge 0$, from the slack basis at the origin. The columns of $A$ are $(1, 20, 200)$, $(0, 1, 20)$ and $(0, 0, 1)$, so

| column | $r_j$ | $\gamma_j$ | $r_j^2/\gamma_j$ |
|---|---|---|---|
| $x_1$ | $-100$ | $1 + 1 + 400 + 40000 = 40402$ | $0.2475$ |
| $x_2$ | $-10$ | $1 + 1 + 400 = 402$ | $0.2488$ |
| $x_3$ | $-1$ | $1 + 1 = 2$ | $0.5$ |

Dantzig's rule enters $x_1$ and then visits all 8 vertices in 7 pivots. Steepest edge enters $x_3$, the ratio test gives $x_3 = 10000$, and this vertex $(0, 0, 10000)$ is already optimal: one pivot. On the same family it takes one pivot for every $n$ from 1 to 10.

**Units.** For minimize $-3x_1 - 2x_2$ subject to $x_1 + 2x_2 \le 4$, $3x_1 + x_2 \le 6$, the rule compares $9/11$ for $x_1$ with $4/6$ for $x_2$ and enters $x_1$. After the change $x_2 = 10x_2'$, the value for $x_2'$ is $400/501$, still less than $9/11$, while Dantzig's rule switches to $x_2'$.

**A bad case.** Goldfarb and Sit (1979) gave deformed cubes on which the steepest-edge rule visits $2^n$ vertices. So, as for every pivot rule studied so far, there is no polynomial bound on the number of pivots.

## Where it is used

- **Production solvers.** Primal steepest edge, dual steepest edge and Devex are the main pricing rules of large simplex codes. Forrest and Goldfarb report that on hard problems steepest edge needs much fewer iterations than Dantzig's rule, enough to pay for the extra solve.
- **The dual simplex method.** Dual steepest edge is the common default for the [dual simplex method](/dual-simplex-method/), which is the main method in branch and bound for integer programs.
- **Theory.** The rule is the natural "geometric" rule, and its exponential examples show that the worst-case problem of the simplex method is not one of units or scaling. The [smoothed analysis](/smoothed-simplex-analysis/) of Spielman and Teng uses a different rule, the shadow-vertex rule, because its path is easier to analyze.

## References
