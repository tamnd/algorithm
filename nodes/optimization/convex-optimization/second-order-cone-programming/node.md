---
tag: Z8F63T
kind: problem
slug: second-order-cone-programming
name: Second-order cone programming
aliases:
- SOCP
- conic quadratic programming
- second-order cone program
area: optimization/convex-optimization
level: advanced
summary: Linear objective with constraints that each lie in a second-order (Lorentz) cone.
prereqs: [quadratic-programming, linear-programming-problem]
see_also: [linear-programming-problem, quadratic-programming, semidefinite-programming, interior-point-method, portfolio-optimization, geometric-median, minimum-enclosing-ball, self-concordant-function]
sources:
  - paper: doi:10.1016/S0024-3795(98)10032-0
    title: Miguel Sousa Lobo, Lieven Vandenberghe, Stephen Boyd and Hervé Lebret, Applications of second-order cone programming, Linear Algebra and its Applications 284, 1998
    locator: pages 193 to 228
  - paper: doi:10.1007/s10107-002-0339-5
    title: Farid Alizadeh and Donald Goldfarb, Second-order cone programming, Mathematical Programming 95(1), 2003
    locator: pages 3 to 51
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 4.4.2 (second-order cone programming), Section 5.9 (generalized inequalities and conic duality)
  - book: isbn:9780898714913
    title: Aharon Ben-Tal and Arkadi Nemirovski, Lectures on Modern Convex Optimization, SIAM, 2001
    locator: Lecture 3 (conic quadratic programming and its applications)
  - paper: doi:10.1287/moor.22.1.1
    title: Yurii Nesterov and Michael J. Todd, Self-scaled barriers and interior-point methods for convex programming, Mathematics of Operations Research 22(1), 1997
    locator: pages 1 to 42
  - paper: doi:10.1287/moor.26.2.193.10561
    title: Aharon Ben-Tal and Arkadi Nemirovski, On polyhedral approximations of the second-order cone, Mathematics of Operations Research 26(2), 2001
    locator: pages 193 to 205
  - paper: doi:10.1007/s10957-016-0892-3
    title: Brendan O'Donoghue, Eric Chu, Neal Parikh and Stephen Boyd, Conic optimization via operator splitting and homogeneous self-dual embedding, Journal of Optimization Theory and Applications 169(3), 2016
    locator: pages 1042 to 1068
---

A second-order cone program (SOCP) minimizes a linear function subject to linear equations and constraints of the form $\|A_ix + b_i\|_2 \le c_i^\top x + d_i$. Each such constraint says that an affine image of $x$ lies in the second-order cone, also called the Lorentz cone or the ice-cream cone. SOCP sits between [linear programming](/linear-programming-problem/) and [semidefinite programming](/semidefinite-programming/): it contains LP, convex [quadratic programming](/quadratic-programming/) and convex quadratically constrained QP, and it is a special case of SDP. It also covers sums and maxima of Euclidean norms, hyperbolic constraints $xy \ge z^2$ and robust linear constraints with ellipsoidal uncertainty. Primal-dual [interior-point methods](/interior-point-method/) solve it to accuracy $\varepsilon$ in $O(\sqrt{N}\log(1/\varepsilon))$ iterations for $N$ cones, at a cost per iteration close to that of an LP of the same size.

## In plain words

In a linear program, every rule is a flat wall: one side is allowed, the other is not. A second-order cone program also allows round walls. A rule can say that the straight-line distance between two points that depend on your choices is at most some amount. Such rules come up for real distances, for risk, for forces with friction and for uncertain data. The allowed region is still in one piece with no dents, so the problem stays easy. Good methods find the best point fast and also give a proof that no better point exists.

## Definition

**The cone.** The second-order cone of dimension $k$ is

$$\mathcal{Q}^k = \{(t, u) \in \mathbb{R} \times \mathbb{R}^{k-1} : \|u\|_2 \le t\}.$$

For $k = 1$ it is the half-line $t \ge 0$. The cone is closed, convex and pointed, has a nonempty interior, and is self-dual: $(s_0, v)^\top(t, u) \ge 0$ for all $(t, u) \in \mathcal{Q}^k$ exactly when $(s_0, v) \in \mathcal{Q}^k$. One direction is the Cauchy-Schwarz inequality, $s_0t + v^\top u \ge s_0t - \|v\|\,\|u\| \ge 0$.

**Input.** A vector $f \in \mathbb{R}^n$, and for $i = 1, \dots, N$ a matrix $A_i \in \mathbb{R}^{(k_i - 1) \times n}$, vectors $b_i$ and $c_i$, and a number $d_i$. Optionally, linear equations $Fx = g$.

**Problem.**

$$\min_{x}\ f^\top x \quad\text{s.t.}\quad \|A_ix + b_i\|_2 \le c_i^\top x + d_i \quad (i = 1, \dots, N), \qquad Fx = g.$$

**Output.** An optimal $x^*$, or a certificate that the problem is infeasible or unbounded. In general only an approximation to a given accuracy can be computed, because optimal points can be irrational even for integer data.

**Conic form and duality.** With a cone $K = \mathcal{Q}^{k_1} \times \dots \times \mathcal{Q}^{k_N}$, every SOCP can be written as

$$\text{(P)}\ \min\ c^\top x \ \text{ s.t. } Ax = b,\ x \in K, \qquad \text{(D)}\ \max\ b^\top y \ \text{ s.t. } s = c - A^\top y \in K.$$

For feasible $x$ and $(y, s)$, the gap is $c^\top x - b^\top y = x^\top s \ge 0$, by self-duality. If both (P) and (D) have strictly feasible points, both optima are attained and the gap is $0$. At an optimal pair, each block satisfies $x_i^\top s_i = 0$, which for nonzero blocks means that $x_i$ and $s_i$ are on the boundary of the cone with $u$ and $v$ pointing in opposite directions. Unlike LP, without strict feasibility a finite optimal value need not be attained, and the two optimal values can differ.

## Variants

- **Rotated cone.** $\{(x, y, z) : 2xy \ge \|z\|^2,\ x, y \ge 0\}$, which is the image of $\mathcal{Q}^{k}$ under a linear map. It writes $x^\top Qx \le s$, $xy \ge 1$ and $\|z\|^2/y \le x$ directly.
- **Convex QCQP.** Constraints $x^\top P_ix + q_i^\top x + r_i \le 0$ with $P_i \succeq 0$. With $P_i = L_iL_i^\top$, each one is a rotated cone constraint.
- **Sums and maxima of norms.** $\min\sum_j\|A_jx - b_j\|$ and $\min\max_j\|A_jx - b_j\|$, with one epigraph variable per norm.
- **Powers and means.** $\|x\|_p \le t$ for rational $p \ge 1$, $x^{3/2} \le t$ and the geometric mean $(x_1x_2\cdots x_{2^k})^{1/2^k} \ge t$ all have SOCP descriptions with extra variables.
- **Mixed-integer SOCP.** Some variables are integers. This is NP-hard, and solvers use branch and bound with SOCP or LP relaxations.

## Examples

**The closest point on a line.** Minimize $\|x\|_2$ over $x \in \mathbb{R}^2$ with $3x_1 + 4x_2 = 25$. In conic form, the variable is $(t, x_1, x_2) \in \mathcal{Q}^3$, the objective is $t$ and the equation is $3x_1 + 4x_2 = 25$. The answer is $x^* = (3, 4)$ with $t^* = 5$. The dual is $\max 25y$ subject to $s = (1, -3y, -4y) \in \mathcal{Q}^3$, that is, $5|y| \le 1$, so $y^* = \tfrac15$ with the value $5$. The gap is $(5, 3, 4)^\top(1, -\tfrac35, -\tfrac45) = 5 - \tfrac95 - \tfrac{16}{5} = 0$. Both vectors are on the boundary of the cone, with $(3, 4)$ and $(-\tfrac35, -\tfrac45)$ in opposite directions.

**An LP as an SOCP.** With only cones of dimension $1$, the cone constraint is $x \ge 0$. For $\min x_1 + 2x_2$ subject to $x_1 + x_2 = 1$ and $x \ge 0$, the answer is $x^* = (1, 0)$ with value $1$. The dual $\max y$ subject to $s = (1 - y, 2 - y) \ge 0$ gives $y^* = 1$ and $s = (0, 1)$, and the gap $x^{*\top}s = 0$.

**An optimum that is not attained.** Minimize $x$ subject to $xy \ge 1$, $x \ge 0$, $y \ge 0$, a rotated cone constraint on $(x, y, \sqrt{2})$. The infimum is $0$, approached by $(\varepsilon, 1/\varepsilon)$, but no feasible point has $x = 0$. The dual is feasible with value $0$, and it is not strictly feasible.

**An irrational answer.** Minimize $\|x\|_2$ subject to $x_1 + x_2 = 1$. The answer has the value $\sqrt{2}/2$, so an exact rational output is not possible.

## Known algorithms

- **Primal-dual [interior-point methods](/interior-point-method/).** The function $-\log(t^2 - \|u\|^2)$ is a [self-concordant](/self-concordant-function/) barrier for $\mathcal{Q}^k$ with the parameter $2$, for every $k$. So a path-following method needs $O(\sqrt{N}\log(1/\varepsilon))$ Newton steps for $N$ cones, independent of the cone dimensions. The cone is self-scaled, so the symmetric Nesterov-Todd scaling applies (Nesterov and Todd, 1997). Each step solves one linear system with the matrix $AW^{-2}A^\top$, where the scaling $W^2$ has one block per cone and each block is a diagonal matrix plus a rank-one matrix. So a step costs about as much as an LP step. Practical solvers need a few tens of steps.
- **First-order splitting methods.** [ADMM](/admm/) on the homogeneous self-dual embedding (O'Donoghue, Chu, Parikh and Boyd, 2016) only needs projections onto $\mathcal{Q}^k$, which have a closed form, and one factorization. It scales to very large problems at modest accuracy.
- **The [ellipsoid method](/ellipsoid-method/).** It gives polynomial-time approximate solutions given bounds on the size of the solution, but it is slow in practice.
- **Polyhedral approximation.** Replace each cone by an LP of the size below, and use an LP solver. This is useful inside mixed-integer solvers.

## Bounds

- **Polynomial time to any accuracy.** For a problem with a strictly feasible point and a known bound $R$ on the size of the solutions, interior-point methods reach accuracy $\varepsilon$ in time polynomial in the input size and $\log(R/\varepsilon)$.
- **No exact rational answer in general.** The examples show irrational optimal values for integer data. So the complexity is stated for approximate solutions, as for SDP.
- **Iteration bound.** The barrier parameter of $K$ is $2N$, which gives the $O(\sqrt{N}\log(1/\varepsilon))$ bound above. It does not grow with the cone dimensions.
- **LP approximation.** Ben-Tal and Nemirovski (2001) showed that $\mathcal{Q}^k$ can be approximated to relative accuracy $\varepsilon$ by the projection of a polyhedron with $O(k\log(1/\varepsilon))$ variables and constraints. So an SOCP reduces to an LP of nearly the same size at the cost of an approximation.

## Reductions

- **LP to SOCP.** Take all cones of dimension $1$.
- **Convex QP to SOCP.** With $Q = LL^\top$, the epigraph constraint $\tfrac12x^\top Qx \le s$ is $\|(L^\top x, (1 - s)/\sqrt2)\| \le (1 + s)/\sqrt2$. See [quadratic programming](/quadratic-programming/).
- **SOCP to SDP.** $\|u\| \le t$ holds exactly when the arrow matrix $\begin{bmatrix} tI & u \\ u^\top & t \end{bmatrix}$ is positive semidefinite, by the [Schur complement](/schur-complement/). So each SOCP is an SDP, but the SDP has matrices of order $k$ for a cone of dimension $k$, and interior-point methods for SDP are much slower on it than SOCP methods.
- **Robust LP to SOCP.** The constraint $a^\top x \le b$ for all $a$ in the ellipsoid $\{\bar a + Pu : \|u\| \le 1\}$ is the cone constraint $\bar a^\top x + \|P^\top x\| \le b$.

## Applications

- **Location and geometry.** The [geometric median](/geometric-median/), the Fermat-Weber problem, the [minimum enclosing ball](/minimum-enclosing-ball/) and the distance between convex sets are SOCPs.
- **Finance.** [Portfolio optimization](/portfolio-optimization/) with a bound on the standard deviation $\|\Sigma^{1/2}w\| \le \sigma$, and value-at-risk constraints for normal returns.
- **Robust optimization.** Linear programs with ellipsoidal uncertainty in the data become SOCPs (Ben-Tal and Nemirovski).
- **Engineering.** Antenna array and FIR filter design, truss design, grasping force optimization with friction cones, and control (Lobo, Vandenberghe, Boyd and Lebret, 1998).
- **Statistics and learning.** Robust least squares, the group lasso and some forms of the [support vector machine](/support-vector-machine/).

## References
