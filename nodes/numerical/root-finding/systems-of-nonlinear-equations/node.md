---
tag: GMK9FQ
kind: problem
slug: systems-of-nonlinear-equations
name: Systems of nonlinear equations
aliases:
- nonlinear system solving
- nonlinear equations in several variables
- F(x) = 0 in R^n
area: numerical/root-finding
level: core
summary: Given F from R^n to R^n, find x with F(x) = 0. Newton-type methods converge fast near a root with a nonsingular Jacobian; no method is guaranteed to find a root from an arbitrary start.
prereqs: [root-finding-problem, gaussian-elimination, condition-number]
see_also: [newton-method-for-systems, broyden-method, kantorovich-theorem, homotopy-continuation, fixed-point-iteration, interval-newton-method, backtracking-line-search, root-finding-problem]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 25, Nonlinear systems and Newton's method
  - book: isbn:9780898713640
    title: John E. Dennis Jr. and Robert B. Schnabel, Numerical Methods for Unconstrained Optimization and Nonlinear Equations, SIAM Classics in Applied Mathematics 16, 1996
    locator: Chapter 5, Newton's method for nonlinear equations and unconstrained minimization; Chapter 6, Globally convergent modifications of Newton's method; Chapter 8, Secant methods for systems of nonlinear equations
  - book: isbn:9780898714616
    title: J. M. Ortega and W. C. Rheinboldt, Iterative Solution of Nonlinear Equations in Several Variables, SIAM Classics in Applied Mathematics 30, 2000
    locator: Chapter 10, One-step stationary methods (local convergence of Newton's method); Chapter 12, Contractions and nonlinear majorants (the Newton-Kantorovich theorem)
  - book: isbn:9780898713527
    title: C. T. Kelley, Iterative Methods for Linear and Nonlinear Equations, SIAM Frontiers in Applied Mathematics 16, 1995
    locator: Chapter 4, Basic concepts and fixed-point iteration; Chapter 5, Newton's method; Chapter 8, Global convergence
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006
    locator: Chapter 11, Nonlinear equations
  - paper: "M. D. Hirsch, C. H. Papadimitriou and S. A. Vavasis, Exponential lower bounds for finding Brouwer fixed points, Journal of Complexity 5 (1989) 379-416"
    locator: the lower bound on the number of evaluations for Lipschitz maps
  - paper: doi:10.1145/355934.355936
    title: J. J. Moré, B. S. Garbow and K. E. Hillstrom, Testing unconstrained optimization software, ACM Transactions on Mathematical Software 7(1) (1981) 17-41
    locator: the Freudenstein and Roth function
---

A system of nonlinear equations asks for a point $x^* \in \mathbb{R}^n$ with $F(x^*) = 0$, where $F : D \subseteq \mathbb{R}^n \to \mathbb{R}^n$ has $n$ components $F_1, \ldots, F_n$. It is the [root-finding problem](/root-finding-problem/) in several variables, and the case $F(x) = Ax - b$ is a linear system. Two things are lost when $n \ge 2$. There is no bracket: a sign change of each component on a box does not shrink to a root by halving, as it does on a line. And the solution set can be anything from empty to a curve. The working methods are therefore local, built on the Jacobian $J(x) = F'(x)$, and made more robust by line searches, trust regions or continuation.

## In plain words

You have several unknowns and the same number of equations that connect them, and the equations are not straight lines or planes. You want values of the unknowns that make every equation hold at once. In one variable you could squeeze the answer between two points where the function has opposite signs. With two or more unknowns there is no such squeeze. Instead you guess, replace each equation by its tangent plane at the guess, solve the resulting linear system, and repeat. Near a good answer this is very fast. Far from it, the guess can wander off, so practical methods also check that the equations are getting closer to zero at each step.

## Definition

**Input.** A map $F : D \to \mathbb{R}^n$ on an open set $D \subseteq \mathbb{R}^n$, given by a procedure that evaluates $F(x)$ and possibly the Jacobian $J(x) = \big(\partial F_i/\partial x_j\big)_{i,j}$, together with information such as a starting point $x_0$ and a tolerance.

**Output.** A point $\hat x$ that is close to a solution $x^*$ of $F(x^*) = 0$, in the sense $\|\hat x - x^*\| \le \tau$, or with a small residual $\|F(\hat x)\| \le \tau_F$, or a report of failure.

**Regular root.** A solution $x^*$ is regular (or simple) if $F$ is differentiable at $x^*$ and $J(x^*)$ is nonsingular. A regular root is isolated, and by the inverse function theorem $F$ is a local diffeomorphism near it. The local theory of all Newton-type methods assumes a regular root and a Lipschitz continuous Jacobian near it.

Notation on the root-finding pages: $F$ is the map, $x^*$ a root, $x_k$ the iterates, $e_k = x_k - x^*$ the error, $\|\cdot\|$ a vector norm with its induced matrix norm, and $\kappa(J) = \|J\|\,\|J^{-1}\|$ the [condition number](/condition-number/). A method has order $q$ and rate $C$ when $\|e_{k+1}\| \approx C \|e_k\|^q$; its cost is counted in evaluations of $F$ and $J$ and in linear solves.

## Variants

- **Square, overdetermined and underdetermined.** With $m$ equations and $n$ unknowns, $m > n$ leads to nonlinear least squares, $\min \|F(x)\|_2$ (Gauss-Newton and Levenberg-Marquardt methods), and $m < n$ to a solution manifold, traced by continuation.
- **Fixed-point form.** $x = G(x)$, for example $G(x) = x - A F(x)$ with a nonsingular $A$; when $G$ is a contraction, [fixed-point iteration](/fixed-point-iteration/) converges by the [Banach fixed-point theorem](/banach-fixed-point-theorem/).
- **Polynomial systems.** Each $F_i$ is a polynomial. All isolated complex solutions can be found by [homotopy continuation](/homotopy-continuation/), or symbolically through [Gröbner bases](/groebner-basis/) and [resultants](/resultant/).
- **Parameter-dependent systems.** $F(x, \lambda) = 0$ for a range of $\lambda$; the solution curve is followed by predictor-corrector continuation.
- **Large and sparse.** $n$ in the millions, from discretized differential equations; the Newton equations are solved by Krylov methods such as [GMRES](/gmres/) (Newton-Krylov methods).
- **Verified solutions.** Prove that a box contains exactly one root, with the [interval Newton method](/interval-newton-method/).

## Examples

| system | solutions | remark |
|---|---|---|
| $x^2 + y^2 = 4$, $xy = 1$ | 4 real points $(\pm 1.9318516525781366, \pm 0.5176380902050416)$ and $(\pm 0.5176380902050416, \pm 1.9318516525781366)$, signs equal | from $x^4 - 4x^2 + 1 = 0$, $x^2 = 2 \pm \sqrt 3$; all regular |
| $x^2 = 0$, $y = 0$ | $(0, 0)$ | singular root: $J(0, 0) = \operatorname{diag}(0, 1)$; Newton is only linear in $x$ |
| $x^2 + y^2 + 1 = 0$, $x = y$ | none in $\mathbb{R}^2$ | every method must fail; $\|F\|$ has a positive minimum |
| $x - y = 0$, $2x - 2y = 0$ | the whole line $x = y$ | no root is isolated; $J$ is singular everywhere |
| Freudenstein and Roth: $-13 + x + ((5 - y)y - 2)y = 0$, $-29 + x + ((y + 1)y - 14)y = 0$ | $(5, 4)$ | $\|F\|_2^2$ also has a local minimum $48.984$ at about $(11.4128, -0.8968)$, where descent methods on $\|F\|^2$ can stop (Moré, Garbow and Hillstrom, 1981) |

The numbers in the table were checked in binary64: $F(5, 4) = (0, 0)$ exactly, and minimizing $\|F\|_2^2$ over $x$ for fixed $y$ and then over $y$ gives the local minimum.

## Known algorithms

| method | needs | local rate | cost per step | global behaviour |
|---|---|---|---|---|
| [Newton's method for systems](/newton-method-for-systems/) | $F$, $J$ | quadratic at a regular root | one $F$, one $J$, one $n \times n$ solve ($\tfrac23 n^3$ flops dense) | local; diverges or cycles from bad starts |
| finite-difference Newton | $F$ | quadratic if the difference step tends to $0$ with the error, linear otherwise | $n + 1$ evaluations of $F$ and a solve | local |
| [Broyden's method](/broyden-method/) | $F$ | superlinear | one $F$, a rank-one update, $O(n^2)$ | local |
| [fixed-point iteration](/fixed-point-iteration/) | $G$ | linear, rate $\|G'(x^*)\|$ | one $G$ | global if $G$ is a contraction on a closed set it maps into itself |
| Newton with a line search | $F$, $J$ | quadratic once full steps are taken | as Newton, plus extra $F$ for [backtracking](/backtracking-line-search/) | converges to a root or to a point where $J^T F = 0$ |
| trust region (Powell's hybrid, dogleg) | $F$, $J$ or a secant model | quadratic or superlinear | as Newton | same alternatives as the line search |
| [homotopy continuation](/homotopy-continuation/) | polynomial $F$ | path tracking with Newton corrector | many Newton steps per path | finds all isolated complex roots with probability 1 |
| [interval Newton](/interval-newton-method/) and Krawczyk | enclosures of $F$ and $J$ | quadratic contraction of a box | interval arithmetic and a solve | proves existence and uniqueness in a box |

## Bounds

- **Local convergence (proved).** If $J$ is Lipschitz near a regular root $x^*$, Newton's method converges quadratically from every start close enough to $x^*$ (Dennis and Schnabel, Theorem 5.2.1). [Kantorovich's theorem](/kantorovich-theorem/) gives a computable condition at $x_0$ that guarantees existence of a root and convergence.
- **No global guarantee from function values (proved).** For Lipschitz maps of the cube into itself, any algorithm that only evaluates the map needs, in the worst case, a number of evaluations exponential in the dimension to find a point $x$ with a small residual $\|G(x) - x\|$ (Hirsch, Papadimitriou and Vavasis, 1989). So no method for general $F$ has a worst-case cost like that of bisection.
- **Globalized methods (proved).** With a line search on $\tfrac12\|F\|_2^2$ and nonsingular Jacobians along the iterates, Newton's method converges to a root; without nonsingularity it can converge to a stationary point of $\|F\|^2$ that is not a root (Nocedal and Wright, Chapter 11).
- **Polynomial systems (proved).** A system of $n$ polynomial equations of degrees $d_1, \ldots, d_n$ in $n$ unknowns has at most $d_1 \cdots d_n$ isolated complex solutions (Bézout's bound), and homotopy continuation can be set up to follow exactly that many paths.
- **Limiting accuracy.** If $F$ is evaluated with an absolute error $\varepsilon_F$, a computed root can be no more accurate than about $\|J(x^*)^{-1}\|\,\varepsilon_F$, and the residual alone bounds the error only through $\|e\| \lesssim \|J(x^*)^{-1}\|\,\|F(\hat x)\|$ (Higham, Chapter 25, for Newton's method in floating point).

## Reductions

- **To minimization.** The roots of $F$ are the global minimizers of $\phi(x) = \tfrac12\|F(x)\|_2^2$ with value $0$; the stationary points satisfy $J(x)^T F(x) = 0$, which includes every root but also, as in the Freudenstein and Roth example, local minima with $F \ne 0$.
- **From minimization.** A smooth unconstrained minimization problem leads to the system $\nabla \phi(x) = 0$, and Newton's method for this system is Newton's method for minimization, with the Hessian as the Jacobian ([quasi-Newton methods](/quasi-newton-method/) such as [BFGS](/bfgs/) are the analogue of Broyden's method).
- **To linear systems.** Every Newton-type step solves a linear system $J(x_k) s = -F(x_k)$, usually by [LU decomposition](/lu-decomposition/) for dense $J$.
- **To one variable.** For $n = 1$ the problem is the scalar [root-finding problem](/root-finding-problem/), where brackets restore global guarantees.
- **Polynomial systems to eigenvalues.** Through resultants or Gröbner bases a zero-dimensional polynomial system becomes an eigenvalue problem for multiplication matrices.

## Applications

- **Implicit time stepping.** Each step of the [backward Euler method](/backward-euler-method/) and of implicit Runge-Kutta methods solves a nonlinear system, usually by a few Newton steps from the previous solution.
- **Steady states.** Discretized nonlinear differential equations (heat transfer, fluid flow, reaction-diffusion) at equilibrium.
- **Circuits and power networks.** The DC operating point of a nonlinear circuit, and the power-flow equations of an electric grid, are classic applications of Newton's method.
- **Chemical and economic equilibrium.** Mass-action equilibria and market-clearing prices.
- **Kinematics.** Inverse kinematics of robot arms and mechanism design lead to polynomial systems.

## References
