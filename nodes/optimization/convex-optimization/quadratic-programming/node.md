---
tag: JJSGKG
kind: problem
slug: quadratic-programming
name: Quadratic programming
aliases:
- QP
- quadratic program
- convex quadratic programming
area: optimization/convex-optimization
level: core
summary: Minimize a quadratic objective subject to linear constraints.
prereqs: [convex-optimization-problem, kkt-conditions, positive-definite-matrix]
see_also: [linear-programming-problem, second-order-cone-programming, portfolio-optimization, support-vector-machine, interior-point-method, admm, motzkin-straus-theorem, least-squares-problem]
sources:
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006
    locator: Chapter 16, Quadratic programming (equality-constrained QP and the KKT system, active-set methods, interior-point methods, the gradient projection method)
  - book: isbn:9780521833783
    title: Stephen Boyd and Lieven Vandenberghe, Convex Optimization, Cambridge University Press, 2004
    locator: Section 4.4 (quadratic optimization problems, QCQP, the reduction of QP to SOCP), Chapter 5 (Lagrange duality and the KKT conditions)
  - paper: doi:10.1002/nav.3800030109
    title: Marguerite Frank and Philip Wolfe, An algorithm for quadratic programming, Naval Research Logistics Quarterly 3, 1956
    locator: pages 95 to 110 (the conditional gradient method, and the theorem that a quadratic bounded below on a nonempty polyhedron attains its minimum)
  - paper: doi:10.1016/0041-5553(80)90098-1
    title: M. K. Kozlov, S. P. Tarasov and L. G. Khachiyan, The polynomial solvability of convex quadratic programming, USSR Computational Mathematics and Mathematical Physics 20(5), 1980
    locator: pages 223 to 228
  - paper: doi:10.1137/0203021
    title: Sartaj Sahni, Computationally related problems, SIAM Journal on Computing 3(4), 1974
    locator: pages 262 to 279 (NP-hardness of quadratic programming with an indefinite matrix)
  - paper: doi:10.1007/BF00120662
    title: Panos M. Pardalos and Stephen A. Vavasis, Quadratic programming with one negative eigenvalue is NP-hard, Journal of Global Optimization 1, 1991
    locator: pages 15 to 22
  - paper: doi:10.1016/0020-0190(90)90100-C
    title: Stephen A. Vavasis, Quadratic programming is in NP, Information Processing Letters 36, 1990
    locator: pages 73 to 77
  - paper: doi:10.1007/BF01587076
    title: Renato D. C. Monteiro and Ilan Adler, Interior path following primal-dual algorithms. Part II, Convex quadratic programming, Mathematical Programming 44, 1989
    locator: pages 43 to 66
  - paper: doi:10.1007/BF02591962
    title: Donald Goldfarb and Ashok Idnani, A numerically stable dual method for solving strictly convex quadratic programs, Mathematical Programming 27, 1983
    locator: pages 1 to 33
  - paper: doi:10.1007/s12532-020-00179-2
    title: Bartolomeo Stellato, Goran Banjac, Paul Goulart, Alberto Bemporad and Stephen Boyd, OSQP, an operator splitting solver for quadratic programs, Mathematical Programming Computation 12, 2020
    locator: pages 637 to 672
---

Quadratic programming is the problem of minimizing a quadratic function of $n$ real variables subject to linear equality and inequality constraints. It is the next step up from [linear programming](/linear-programming-problem/): the objective gets a term $\tfrac12 x^\top Q x$. When $Q$ is [positive semidefinite](/positive-definite-matrix/) the problem is convex, the [KKT conditions](/kkt-conditions/) characterize its solutions, and it can be solved in polynomial time. When $Q$ has even one negative eigenvalue the problem is NP-hard. Convex QPs appear in least squares with constraints, [portfolio selection](/portfolio-optimization/), [support vector machines](/support-vector-machine/), model predictive control and as the subproblem of sequential quadratic programming.

## In plain words

A linear program asks for the lowest point of a flat, tilted plane over a region with straight sides. A quadratic program asks for the lowest point of a curved surface over the same kind of region. If the surface is shaped like a bowl, the problem is convex: there is only one lowest valley, and a point where no small move helps is the answer. Good methods find it fast and also give a proof that it is the best point.

If the surface is shaped like a saddle or a dome, there can be many valleys. A point where no small move helps can still be far from the best point. Then the problem is as hard as the hardest search problems, and no fast method is known.

## Definition

**Input.** A symmetric matrix $Q \in \mathbb{R}^{n \times n}$, a vector $c \in \mathbb{R}^n$, and linear constraints given by $A \in \mathbb{R}^{m \times n}$, $b \in \mathbb{R}^m$, $E \in \mathbb{R}^{p \times n}$, $d \in \mathbb{R}^p$.

**Problem.**

$$\min_{x \in \mathbb{R}^n}\ \tfrac12 x^\top Q x + c^\top x \quad \text{s.t.} \quad Ax \le b, \quad Ex = d.$$

**Output.** An optimal point $x^*$ and the optimal value $f^*$, or a report that the feasible set is empty or that the objective is unbounded below on it. By the theorem of Frank and Wolfe (1956), if the feasible set is not empty and the objective is bounded below on it, then the minimum is attained. This is not true for general convex functions: $e^{-x}$ on $x \ge 0$ has no minimizer.

**Convexity.** The problem is a [convex optimization problem](/convex-optimization-problem/) if and only if $Q \succeq 0$. In that case $x^*$ is optimal if and only if there are multipliers $\lambda \in \mathbb{R}^m$ and $\nu \in \mathbb{R}^p$ with

$$Qx^* + c + A^\top\lambda + E^\top\nu = 0, \quad Ax^* \le b, \quad Ex^* = d, \quad \lambda \ge 0, \quad \lambda_i (Ax^* - b)_i = 0.$$

No constraint qualification is needed, because all constraints are linear. If $Q \succ 0$, the optimal point is unique and the Lagrange dual is

$$\max_{\lambda \ge 0,\ \nu}\ -\tfrac12 (c + A^\top\lambda + E^\top\nu)^\top Q^{-1} (c + A^\top\lambda + E^\top\nu) - b^\top\lambda - d^\top\nu,$$

with zero duality gap whenever the primal is feasible.

## Variants

- **Equality-constrained QP.** Only $Ex = d$. The KKT conditions are one linear system, $\begin{bmatrix} Q & E^\top \\ E & 0 \end{bmatrix}\begin{bmatrix} x \\ \nu \end{bmatrix} = \begin{bmatrix} -c \\ d \end{bmatrix}$.
- **Box-constrained QP.** Only $l \le x \le u$. Projection onto the box is cheap, so [projected gradient descent](/projected-gradient-descent/) works well.
- **Standard QP.** Minimize $x^\top Q x$ over the unit simplex. It is NP-hard for indefinite $Q$, by the [Motzkin-Straus theorem](/motzkin-straus-theorem/).
- **Quadratically constrained QP (QCQP).** The constraints are also quadratic. With all matrices positive semidefinite it is a [second-order cone program](/second-order-cone-programming/). In general it contains [max-cut](/maximum-cut/) and is NP-hard.
- **Nonconvex QP.** $Q$ indefinite. Find a global minimum, or settle for a KKT point.
- **Least-squares form.** $Q = M^\top M$ and $c = -M^\top y$, that is, minimize $\tfrac12\|Mx - y\|^2$ subject to linear constraints. Nonnegative least squares is the case $x \ge 0$.

## Examples

**An inequality-constrained QP.** Minimize $\tfrac12\|x - (3, 2)\|^2$ subject to $x_1 + x_2 \le 2$, $x_1 \ge 0$, $x_2 \ge 0$. In the form above, $Q = I$ and $c = (-3, -2)$, and the constant $13/2$ is dropped. The answer is the closest point to $(3, 2)$ in a triangle. Only the first constraint is active, and the KKT conditions give

$$x^* = (\tfrac32, \tfrac12), \qquad \lambda = (\tfrac32, 0, 0), \qquad Qx^* + c + \lambda_1 (1, 1) = (\tfrac32 - 3 + \tfrac32,\ \tfrac12 - 2 + \tfrac32) = (0, 0).$$

The primal value is $\tfrac12(\tfrac94 + \tfrac14) - \tfrac92 - 1 = -\tfrac{17}{4}$. The dual function at $\lambda$ is $-\tfrac12\|c + A^\top\lambda\|^2 - b^\top\lambda = -\tfrac12(\tfrac94 + \tfrac14) - 3 = -\tfrac{17}{4}$, the same number, so the duality gap is $0$ and $x^*$ is certified optimal.

**An equality-constrained QP.** Minimize $\tfrac12(x_1^2 + 2x_2^2 + 3x_3^2)$ subject to $x_1 + x_2 + x_3 = 1$. The KKT system gives $x_i = -\nu/q_i$, so $x^*$ is proportional to $(1, \tfrac12, \tfrac13)$, that is, $x^* = (\tfrac{6}{11}, \tfrac{3}{11}, \tfrac{2}{11})$, with $\nu = -\tfrac{6}{11}$ and $f^* = \tfrac{3}{11}$.

**A nonconvex QP.** Minimize $-x^2$ subject to $-1 \le x \le 2$. Both endpoints satisfy the KKT conditions, but $x = -1$ has value $-1$ and $x = 2$ has value $-4$. The point $x = 0$ also satisfies them, with both multipliers $0$, and it is the global maximum. For an indefinite $Q$, the KKT conditions are necessary but not sufficient.

## Known algorithms

- **Solve the KKT system.** For an equality-constrained QP, one factorization of the KKT matrix, in $O((n + p)^3)$ time for dense data.
- **Active-set methods.** Guess which inequalities are active, solve the equality-constrained QP, and add or drop one constraint per step, as the [simplex method](/simplex-method/) does for LP. Wolfe (1959) gave a simplex-like method for QP, and Goldfarb and Idnani (1983) a dual active-set method for strictly convex QPs. These methods warm-start well. Their worst case is exponential.
- **[Interior-point methods](/interior-point-method/).** The primal-dual path-following method extends to convex QP with the same $O(\sqrt{n}\log(1/\varepsilon))$ iteration bound (Monteiro and Adler, 1989). Each step solves one linear system with the matrix $Q + A^\top D A$.
- **First-order methods.** [Projected gradient descent](/projected-gradient-descent/) and its accelerated form for simple constraints, the Frank-Wolfe (conditional gradient) method of 1956 over a polytope, and [ADMM](/admm/), which is the method of the OSQP solver.
- **Special structure.** [Sequential minimal optimization](/sequential-minimal-optimization/) for the dual of the [SVM](/svm-training/) problem, and the closed-form projection onto a simplex.
- **Nonconvex QP.** Branch and bound with convex relaxations, for example the [semidefinite relaxation](/convex-relaxation/).

## Bounds

- **Convex QP is in polynomial time.** With rational data, Kozlov, Tarasov and Khachiyan (1980) solved convex QP exactly in polynomial time with the [ellipsoid method](/ellipsoid-method/). Interior-point methods need $O(\sqrt{n}\,L)$ iterations for input bit length $L$. As for LP, no strongly polynomial algorithm is known.
- **Nonconvex QP is NP-hard.** Sahni (1974) showed that QP with an indefinite $Q$ is NP-hard. Pardalos and Vavasis (1991) showed that it stays NP-hard when $Q$ has only one negative eigenvalue. The standard QP over a simplex is strongly NP-hard, by the reduction from maximum clique below. Even to decide whether a given point is a local minimum is NP-hard in general (Murty and Kabadi, 1987).
- **The decision version is in NP.** Vavasis (1990) showed that if a QP has an optimal solution, it has one whose size is polynomial in the input size, so "is the optimal value at most $k$?" is in NP and the problem is [NP-complete](/np-complete/).
- **[First-order lower bound](/first-order-lower-bound/).** A method that only uses gradients needs $\Omega(\sqrt{L/\mu}\log(1/\varepsilon))$ steps on a $\mu$-strongly convex quadratic with largest eigenvalue $L$ in the worst case, and accelerated gradient methods reach this rate.

## Reductions

- **LP to QP.** A linear program is a QP with $Q = 0$.
- **Convex QP to SOCP.** With $Q = LL^\top$, the epigraph constraint $\tfrac12 x^\top Q x \le s$ is the cone constraint $\|(L^\top x,\ (1 - s)/\sqrt2)\| \le (1 + s)/\sqrt2$. So convex QP is a special case of [second-order cone programming](/second-order-cone-programming/), and of [semidefinite programming](/semidefinite-programming/).
- **Convex QP to linear complementarity.** The KKT conditions of $\min \tfrac12 x^\top Q x + c^\top x$, $Ax \le b$, $x \ge 0$ form a linear complementarity problem: find $z \ge 0$ with $w = Mz + q \ge 0$ and $z^\top w = 0$, for $M = \begin{bmatrix} Q & A^\top \\ -A & 0 \end{bmatrix}$. Lemke's method solves it.
- **Maximum clique to standard QP.** By the [Motzkin-Straus theorem](/motzkin-straus-theorem/), the maximum of $x^\top A_G x$ over the simplex is $1 - 1/\omega(G)$, where $A_G$ is the adjacency matrix and $\omega(G)$ is the [clique number](/maximum-clique/). So a standard QP solver finds $\omega(G)$.
- **Max-cut to QP.** [Max-cut](/maximum-cut/) is $\max \tfrac14\sum_{ij} w_{ij}(1 - x_i x_j)$ over $x \in \{-1, 1\}^n$. The objective has no term $x_i^2$, so it is linear in each $x_i$ alone, and its maximum over the box $[-1, 1]^n$ is attained at a vertex. So max-cut is a nonconvex QP over a box.

## Applications

- **Portfolio selection.** The Markowitz model minimizes the variance $x^\top\Sigma x$ of a portfolio subject to a target return and a budget, with a [covariance matrix](/covariance-matrix/) $\Sigma$. See [portfolio optimization](/portfolio-optimization/).
- **Machine learning.** The training problem of the [support vector machine](/support-vector-machine/) and its dual are convex QPs. The [lasso](/lasso-regression/) is a QP after splitting $x$ into positive and negative parts.
- **Least squares with constraints.** Fitting with bounds, nonnegativity or monotonicity constraints is a convex QP.
- **Control.** Model predictive control solves a convex QP over a finite horizon at each sampling time.
- **Nonlinear programming.** Sequential quadratic programming solves a QP model of a smooth nonlinear program at each step.

## References
