---
tag: 9DJE0Y
kind: concept
slug: central-path
name: Central path
aliases:
- barrier trajectory
- central trajectory
- path of analytic centers
area: optimization/convex-optimization
level: advanced
summary: The curve of minimizers of the barrier-penalized objective as the barrier weight varies.
prereqs: [barrier-method, lagrangian-duality]
see_also: [interior-point-method, self-concordant-function, complementary-slackness, karmarkar-algorithm, affine-scaling-method, semidefinite-programming, lp-duality, penalty-method]
sources:
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 11.2 (the logarithmic barrier and the central path, dual points from the central path, the gap m/t, the central path as modified KKT conditions), Section 11.6 (the central path for generalized inequalities)
  - book: isbn:9780898713824
    title: Stephen J. Wright, Primal-Dual Interior-Point Methods, SIAM, 1997
    locator: Chapter 1 (the central path and its neighborhoods), Chapter 2 (background on the existence and limit of the central path)
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006
    locator: Section 14.1 (primal-dual methods and the central path)
  - paper: doi:10.1007/978-1-4613-9617-8_8
    title: Nimrod Megiddo, Pathways to the optimal set in linear programming, in Progress in Mathematical Programming, Springer, 1989
    locator: pages 131 to 158 (the primal-dual central path, its existence and its limit)
  - paper: doi:10.1007/s10107-006-0044-x
    title: Antoine Deza, Eissa Nematollahi and Tamás Terlaky, How good are interior point methods? Klee-Minty cubes tighten iteration-complexity bounds, Mathematical Programming 113, 2008
    locator: pages 1 to 14
---

The central path of a convex program is the curve of points $x^*(t)$ that minimize $t f_0(x) + \phi(x)$, where $f_0$ is the objective, $\phi$ is a barrier for the feasible set and $t > 0$. For a [linear program](/linear-programming-problem/) in standard form it is, in primal-dual form, the set of strictly feasible pairs with $x_i s_i = \mu$ for every $i$. Each point of the path gives a dual feasible point with [duality gap](/lp-duality/) exactly $n\mu$, or $\nu/t$ for a barrier with parameter $\nu$, and the path goes to an optimal point as $\mu \to 0$. [Interior-point methods](/interior-point-method/) and the [barrier method](/barrier-method/) work by following it.

## In plain words

Picture the feasible region as a room and the optimum as a point on a wall. Each wall pushes you away with a force that is strong when you are close to it. The objective pulls you toward the optimum. For each strength of the pull there is one balance point. With a weak pull, the balance point is near the middle of the room. With a strong pull, it is near the optimum.

The central path is the line of these balance points. It runs from the middle of the room to the optimum. Along this line the walls are always far enough away, so a method that follows it can take long, safe steps. At each point, the strength of the pull also tells exactly how far the point is from the optimum in value.

## The idea

**Barrier form.** Take $\min f_0(x)$ subject to $f_i(x) \le 0$ for $i = 1, \ldots, m$ and $Ax = b$, with convex $f_i$, and the logarithmic barrier $\phi(x) = -\sum_i\log(-f_i(x))$. The central point $x^*(t)$ minimizes $t f_0(x) + \phi(x)$ subject to $Ax = b$. Its optimality condition is

$$t\nabla f_0(x^*) + \sum_{i=1}^m \frac{1}{-f_i(x^*)}\nabla f_i(x^*) + A^\top w = 0.$$

With $\lambda_i = 1/(-t f_i(x^*))$ and $\nu = w/t$, this says that $x^*$ minimizes the [Lagrangian](/lagrangian-function/) at $(\lambda, \nu)$, so $(\lambda, \nu)$ is dual feasible. The dual value is $f_0(x^*) - m/t$, so the gap is exactly $m/t$ and $f_0(x^*(t)) - f^* \le m/t$.

**Modified KKT conditions.** The same point solves the [KKT conditions](/kkt-conditions/) with complementary slackness replaced by $-\lambda_i f_i(x) = 1/t$. So the central path is a smooth version of the KKT system: it asks that each product of a multiplier and a slack equals the same small number, instead of $0$.

**Primal-dual form for LP.** For $\min c^\top x$ subject to $Ax = b$, $x \ge 0$, and its dual $\max b^\top y$ subject to $A^\top y + s = c$, $s \ge 0$, the central path is the set of solutions $(x(\mu), y(\mu), s(\mu))$ of

$$Ax = b, \quad A^\top y + s = c, \quad x_i s_i = \mu \ (i = 1, \ldots, n), \quad x > 0, \quad s > 0.$$

For each $\mu > 0$ this system has exactly one solution if and only if both programs have a strictly feasible point and $A$ has full row rank. The point $x(\mu)$ minimizes $c^\top x - \mu\sum_i\log x_i$ on $\{Ax = b, x > 0\}$. The gap is $c^\top x - b^\top y = x^\top s = n\mu$.

**The limit.** As $\mu \to 0$, $(x(\mu), s(\mu))$ converges to a strictly complementary optimal pair: for each $i$, exactly one of $x_i$ and $s_i$ is positive. The primal limit is the analytic center of the optimal face, the point of the face that maximizes $\sum\log x_i$ over the variables that are not forced to $0$ (Megiddo, 1989). As $\mu \to \infty$, the path goes to the analytic center of the feasible set, when that set is bounded.

**Neighborhoods.** Methods do not stay exactly on the path. Short-step methods use $\mathcal{N}_2(\theta) = \{\|XSe - \mu e\|_2 \le \theta\mu\}$, and long-step methods use the wider $\mathcal{N}_{-\infty}(\gamma) = \{x_i s_i \ge \gamma\mu \text{ for all } i\}$. For a general [self-concordant](/self-concordant-function/) barrier, closeness is measured by the Newton decrement of $t f_0 + \phi$.

## Examples

**An interval.** For $\min x$ subject to $0 \le x \le 1$, the central point minimizes $tx - \log x - \log(1 - x)$, so $x^*(t) = \big((t + 2) - \sqrt{t^2 + 4}\big)/(2t)$. At $t = 0^+$ it is $\tfrac12$, the analytic center of $[0, 1]$. At $t = 1$ it is $(3 - \sqrt5)/2 \approx 0.382$, and for large $t$ it is about $1/t$. The gap is $2/t$, for two constraints.

**A small LP.** Take $\min x_1 + 2x_2 + 3x_3$ subject to $x_1 + x_2 + x_3 = \tfrac{11}{6}$, $x \ge 0$. Here $s = c - y(1, 1, 1)$, and $x_i = \mu/s_i$, so $y(\mu)$ is the root below $1$ of $\sum_i \mu/(c_i - y) = \tfrac{11}{6}$:

| $\mu$ | $y(\mu)$ | $x(\mu)$ | $s(\mu)$ | gap $3\mu$ |
|---|---|---|---|---|
| 1 | 0 | (1, 0.5, 0.3333) | (1, 2, 3) | 3 |
| 0.1 | 0.94084 | (1.6904, 0.09441, 0.04856) | (0.05916, 1.0592, 2.0592) | 0.3 |
| 0.01 | 0.99450 | (1.8184, 0.009945, 0.004986) | (0.005499, 1.0055, 2.0055) | 0.03 |
| 0.001 | 0.99945 | (1.8318, 0.0009995, 0.0004999) | (0.0005459, 1.0005, 2.0005) | 0.003 |

The limit is $x^* = (\tfrac{11}{6}, 0, 0)$, $y^* = 1$, $s^* = (0, 1, 2)$, which is strictly complementary.

**A whole optimal face.** For $\min x_1$ over the unit square $[0, 1]^2$, the barrier separates and gives $x_2^*(t) = \tfrac12$ for every $t$. The limit $(0, \tfrac12)$ is the center of the optimal edge, not a vertex. If the LP above had $c = (1, 1, 1)$, every feasible point would be optimal, and the whole path would be the single point $(\tfrac{11}{18}, \tfrac{11}{18}, \tfrac{11}{18})$.

**Semidefinite programs.** For $\min\operatorname{tr}(CX)$ subject to $\operatorname{tr}(A_iX) = b_i$, $X \succeq 0$, the central path is given by $XZ = \mu I$ with $Z = C - \sum_i y_iA_i \succ 0$, and the gap is $\operatorname{tr}(XZ) = n\mu$ for $n \times n$ matrices.

## Where it is used

- **Path-following [interior-point methods](/interior-point-method/).** They take Newton steps toward the point with a smaller $\mu$ and stay in a neighborhood of the path. This gives the $O(\sqrt{n}\log(1/\varepsilon))$ bound for LP.
- **The [barrier method](/barrier-method/).** It computes central points for an increasing sequence of $t$ and reads the gap $m/t$ as its stopping test.
- **Potential-reduction methods.** [Karmarkar's algorithm](/karmarkar-algorithm/) and its successors use a potential that combines the gap with a measure of distance to the path.
- **Strictly complementary solutions.** The limit of the path gives an optimal pair that shows which variables are zero in every optimal solution, which is useful for sensitivity analysis and for rounding to an exact vertex.
- **Lower bounds for interior-point methods.** Deza, Nematollahi and Terlaky (2008) built LPs on a Klee-Minty cube, with many redundant constraints, whose central path bends close to many vertices, so a method that follows the path closely needs many steps.

## References
