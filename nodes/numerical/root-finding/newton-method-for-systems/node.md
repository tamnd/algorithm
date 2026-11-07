---
tag: EB6BTR
kind: algorithm
slug: newton-method-for-systems
name: Newton's method for systems
aliases:
- multidimensional Newton method
- Newton's method in several variables
- Newton-Raphson method for systems
area: numerical/root-finding
level: core
summary: "Solve F(x) = 0 in n unknowns by linearizing: solve J(x) s = -F(x) and set x to x + s. Quadratic convergence near a root with nonsingular Jacobian, no guarantee far from it."
solves: [systems-of-nonlinear-equations]
model: real-ram
complexity:
  vars: {n: the number of equations and unknowns, δ: the tolerance on the error, β: "a bound on the norm of the inverse Jacobian at the root", γ: "a Lipschitz constant of J near the root, with β γ |e_0| ≤ 1/2"}
  time: {local: "O(log log(1/(β γ δ)))", per_step: "O(n^3)"}
  space: {extra: Θ(n^2)}
  evaluations: {per_step: "2"}
properties: {deterministic: true, recursive: false, bracketing: false, derivative_free: false, local: true}
history:
  year: 1916
  people: [Isaac Newton, Thomas Simpson, Henri Fine, Leonid Kantorovich]
  note: Simpson applied the method to two equations in 1740; Fine gave a convergence proof for systems in 1916; Kantorovich proved the semilocal theorem in Banach spaces in 1948.
prereqs: [newton-raphson-method, systems-of-nonlinear-equations, quadratic-convergence, lu-decomposition]
see_also: [kantorovich-theorem, broyden-method, quasi-newton-method, homotopy-continuation, backtracking-line-search, gmres, backward-euler-method, condition-number]
sources:
  - book: isbn:9780898713640
    title: John E. Dennis Jr. and Robert B. Schnabel, Numerical Methods for Unconstrained Optimization and Nonlinear Equations, SIAM Classics in Applied Mathematics 16, 1996
    locator: Chapter 5, Newton's method for nonlinear equations and unconstrained minimization (Theorem 5.2.1 on local quadratic convergence; Lemma 4.1.12 on the Taylor remainder)
  - book: isbn:9780898714616
    title: J. M. Ortega and W. C. Rheinboldt, Iterative Solution of Nonlinear Equations in Several Variables, SIAM Classics in Applied Mathematics 30, 2000
    locator: Chapter 10, One-step stationary methods (Newton's method and the attraction theorem); Section 12.6, Newton-Kantorovich theorem
  - book: isbn:9780898713527
    title: C. T. Kelley, Iterative Methods for Linear and Nonlinear Equations, SIAM Frontiers in Applied Mathematics 16, 1995
    locator: Chapter 5, Newton's method (the standard assumptions, the local theorem, errors in the function and the Jacobian, finite-difference Jacobians)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 25, Nonlinear systems and Newton's method (limiting accuracy and limiting residual)
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 4, Simultaneous nonlinear equations (Newton's method)
  - paper: doi:10.1073/pnas.2.9.546
    title: "H. B. Fine, On Newton's method of approximation, Proceedings of the National Academy of Sciences 2(9) (1916) 546-552"
    locator: the convergence theorem for systems
  - paper: doi:10.1137/0719025
    title: "R. S. Dembo, S. C. Eisenstat and T. Steihaug, Inexact Newton methods, SIAM Journal on Numerical Analysis 19(2) (1982) 400-408"
    locator: the local convergence theorems for forcing terms
  - paper: doi:10.1137/1037125
    title: Tjalling J. Ypma, Historical development of the Newton-Raphson method, SIAM Review 37(4), 531-551, 1995
    locator: Simpson's treatment of two equations
---

Newton's method for systems solves $F(x) = 0$, where $F$ maps $\mathbb{R}^n$ to $\mathbb{R}^n$, by replacing $F$ at the current point $x_k$ with its linear model $F(x_k) + J(x_k)(x - x_k)$ and taking the zero of the model as the next point. Each step solves the linear system $J(x_k) s_k = -F(x_k)$ for the step $s_k$ and sets $x_{k+1} = x_k + s_k$. Near a root where the Jacobian $J$ is nonsingular and Lipschitz, it converges with [order 2](/quadratic-convergence/), as in one variable. Far from a root it has no guarantee, and at a root with singular Jacobian it is at best linear. It is the core of almost every solver for [systems of nonlinear equations](/systems-of-nonlinear-equations/), of implicit integrators such as the [backward Euler method](/backward-euler-method/), and of Newton's method for minimization, which applies it to the gradient.

## In plain words

With one equation, Newton's method follows the tangent line to the axis. With $n$ equations in $n$ unknowns, each equation is replaced by its tangent plane at the current guess. The $n$ planes are flat, so finding where they all meet is a linear system, which elimination solves exactly. The meeting point is the next guess. Close to a solution the planes fit the curved equations very well, and the number of correct digits about doubles in each step. Each step needs the values of all $n$ equations, all $n^2$ partial derivatives, and one linear solve.

## The problem

The input is a function $F$ from $\mathbb{R}^n$ to $\mathbb{R}^n$ and its Jacobian $J = F'$, the $n \times n$ matrix of partial derivatives $J_{ij} = \partial F_i / \partial x_j$, both given as procedures; a starting point $x_0$; a tolerance with an absolute part $\delta_a \ge 0$ and a relative part $\delta_r \ge 0$, not both zero; and a maximum number of steps $k_{\max}$. The output is a point $\hat x$ and a flag that says why the loop ended.

Notation on the root-finding pages: $F$ is the function and $J$ its Jacobian, $x^*$ a root, $x_k$ the iterates, $e_k = x_k - x^*$ the error, $s_k = x_{k+1} - x_k$ the step. Norms are any fixed vector norm and the induced matrix norm; the implementation uses $\|\cdot\|_\infty$. A method has order $q$ and rate constant $C$ when $\|e_{k+1}\| \approx C \|e_k\|^q$. The cost is counted in evaluations of $F$ and of $J$; with $w$ evaluations per step and order $q$, the efficiency index is $q^{1/w}$.

The **standard assumptions** (Dennis and Schnabel, Kelley) at a root $x^*$ are: $F$ is continuously differentiable on an open convex set containing the ball $B(x^*, r)$; $J(x^*)$ is nonsingular with $\|J(x^*)^{-1}\| \le \beta$; and $J$ is Lipschitz on the ball, $\|J(x) - J(y)\| \le \gamma \|x - y\|$.

## The algorithm

```pseudo id=main
NEWTON-SYSTEM(F, J, x0, δa, δr, kmax)
L1  x ← x0
L2  for k ← 1 to kmax do
L3      v ← F(x)
L4      if v = 0 then return (x, "root")
L5      if some entry of v is not finite then return (x, "failure")
L6      A ← J(x)
L7      solve A s = −v by elimination with partial pivoting; if a pivot is 0 then return (x, "singular")
L8      xnew ← x + s
L9      if xnew is not finite then return (x, "failure")
L10     if ‖s‖ ≤ δa + δr · ‖xnew‖ then return (xnew, "converged")
L11     x ← xnew
L12 return (x, "kmax reached")
```

Line L3 evaluates all $n$ components of $F$, and line L4 returns at once if they are all exactly zero. Line L6 evaluates the Jacobian, and line L7 solves the Newton equation $J(x_k) s_k = -F(x_k)$ by [Gaussian elimination](/gaussian-elimination/) with partial pivoting, that is by an [LU decomposition](/lu-decomposition/); the inverse $J^{-1}$ is never formed. A zero pivot means $J(x_k)$ is singular (exactly, in rational arithmetic), so the linear model has no unique zero and the step is undefined. Lines L5 and L9 stop on NaN or infinity. Line L10 is the relative step test of the [stopping criteria](/stopping-criteria/) page: for a quadratically convergent method $\|s_k\|$ estimates $\|e_k\|$, and $x_{k+1}$ is much better. Line L2 bounds the work, so the loop always ends, also in floating point.

The step is the zero of the linear model because $F(x_k) + J(x_k) s_k = 0$. Equivalently, $x_{k+1} = x_k - J(x_k)^{-1} F(x_k)$, the formula in one variable with the reciprocal of the derivative replaced by the inverse matrix.

## Example

Intersect the circle $x^2 + y^2 = 4$ with the hyperbola $xy = 1$. Here $F(x, y) = (x^2 + y^2 - 4,\; xy - 1)$ and
$$J(x, y) = \begin{pmatrix} 2x & 2y \\ y & x \end{pmatrix},$$
which is singular on the lines $y = \pm x$. The root in the first quadrant with $x > y$ is $x^* = (\sqrt{2 + \sqrt 3}, \sqrt{2 - \sqrt 3}) = (1.9318516525781366, 0.5176380902050415)$. Start from $x_0 = (2, 0)$. In exact rational arithmetic the errors $\|e_k\|_\infty$ are:

| $k$ | $x_k$ (rounded) | $\lVert e_k \rVert_\infty$ | $\lVert e_k \rVert / \lVert e_{k-1} \rVert^2$ |
|---|---|---|---|
| 0 | $(2,\ 0)$ | $5.176 \cdot 10^{-1}$ | |
| 1 | $(2,\ 0.5)$ | $6.815 \cdot 10^{-2}$ | $0.2543$ |
| 2 | $(1.9333333333333333,\ 0.5166666666666667)$ | $1.482 \cdot 10^{-3}$ | $0.3190$ |
| 3 | $(1.9318527410964386,\ 0.5176370548219288)$ | $1.089 \cdot 10^{-6}$ | $0.4958$ |
| 4 | $(1.9318516525789342,\ 0.5176380902042443)$ | $7.977 \cdot 10^{-13}$ | $0.6733$ |
| 5 | | $4.496 \cdot 10^{-25}$ | $0.7066$ |
| 6 | | $1.430 \cdot 10^{-49}$ | $0.7071$ |

The first step is $s_0 = (0, 0.5)$: at $(2, 0)$ the Newton equation is $4 s_1 = 0$, $2 s_2 = 1$. The number of correct digits doubles from step 2 on, and the ratio tends to $1/\sqrt 2 = 0.70711$ (observed). In binary64 with $\delta_a = 0$ and $\delta_r = 2^{-50}$, the program makes 6 passes, with 6 evaluations of $F$ and 6 of $J$; the step norms are $0.5$, $6.7 \cdot 10^{-2}$, $1.5 \cdot 10^{-3}$, $1.1 \cdot 10^{-6}$, $8.0 \cdot 10^{-13}$ and $1.2 \cdot 10^{-16}$, and the returned point $(1.9318516525781366, 0.5176380902050416)$ is within one unit in the last place of $x^*$ in each component. The same run with a [forward-difference](#variants-and-improvements) Jacobian also takes 6 passes.

## Correctness

Newton's method has no global guarantee. The claims are of three kinds; the first two are proved in [the correctness proof](proofs/correctness.md).

- **Always.** The loop ends after at most $k_{\max}$ passes. A result with the flag "root" is an exact zero of $F$, and one with the flag "converged" satisfies the step test of line L10.
- **Local (proved).** Under the standard assumptions, if $\|e_0\| \le \min(r, 1/(2\beta\gamma))$ then in exact arithmetic every $J(x_k)$ is nonsingular with $\|J(x_k)^{-1}\| \le 2\beta$, and
$$\|e_{k+1}\| \le \beta\gamma\,\|e_k\|^2 \le \tfrac12 \|e_k\|,$$
so the iterates converge to $x^*$ quadratically (Dennis and Schnabel, Theorem 5.2.1). The key facts are the Taylor bound $\|F(y) - F(x) - J(x)(y - x)\| \le \frac{\gamma}{2}\|y - x\|^2$ and the perturbation lemma for the inverse.
- **Semilocal (proved elsewhere).** The [Kantorovich theorem](/kantorovich-theorem/) assumes nothing about a root: conditions on $F(x_0)$, $J(x_0)^{-1}$ and the Lipschitz constant alone prove that a root exists, that it is unique in a ball, and that Newton's method converges to it.
- **Global (none).** From a general start the iterates can diverge, cycle, or hit a singular Jacobian. On the Freudenstein-Roth problem (see [systems of nonlinear equations](/systems-of-nonlinear-equations/)) the program needs 44 passes from $(0.5, -2)$, wandering for about 37 of them before the quadratic phase starts (observed).

## Complexity

The cost model is the number of evaluations of $F$ and $J$, plus the floating point operations of the linear solve.

- **Per step.** One evaluation of $F$ ($n$ scalar functions), one of $J$ ($n^2$ partial derivatives) and one LU solve of $\frac23 n^3 + O(n^2)$ flops. Counting $F$ and $J$ as one evaluation each, $w = 2$ and the efficiency index is $2^{1/2}$. With a forward-difference Jacobian each step costs $n + 1$ evaluations of $F$, and the index is $2^{1/(n+1)}$; this is why [Broyden's method](/broyden-method/), with one evaluation of $F$ per step and superlinear convergence, wins for large $n$ when $J$ is expensive.
- **Steps to the tolerance.** Under the local hypotheses, $\beta\gamma\|e_k\| \le (\beta\gamma\|e_0\|)^{2^k} \le 2^{-2^k}$, so $\|e_k\| \le \delta$ after $\lceil \log_2 \log_2 (1/(\beta\gamma\delta)) \rceil$ steps.
- **Total evaluations.** A run that stops at line L10 in pass $k$ makes exactly $k$ evaluations of $F$ and $k$ of $J$; a run that stops at line L4 in pass $k$ makes $k$ of $F$ and $k - 1$ of $J$.
- **Space.** $\Theta(n^2)$ for the Jacobian and its factors.

### Floating point

Suppose the computed $F$ has error at most $\psi$ in norm near $x^*$, the computed Jacobian has a relative error $\eta$ with $\beta\|J(x^*)\|\eta$ small, and the linear solver is backward stable. Then the iterates reach an error of about
$$\|e\| \lesssim \|J(x^*)^{-1}\|\,\psi + u\,\|x^*\|$$
and stop improving there, the limiting accuracy (Higham, Chapter 25; Kelley, Chapter 5). Errors in $J$, including the error of the solve and of a forward-difference Jacobian with step about $\sqrt u$, slow the convergence to linear with rate proportional to $\kappa(J)\eta$, but they do not change the limiting accuracy. So the Jacobian may be approximate, while $F$ must be accurate. With $\delta_r$ of a few units of roundoff the step test may never pass on an ill-conditioned problem, which is why line L2 is needed.

## Properties

- **Local.** Quadratic convergence holds only near a root with nonsingular Jacobian. The region of attraction is open but can be small and irregular.
- **Affine invariant.** Replacing $F$ by $AF$ for a nonsingular matrix $A$ does not change the iterates, and a linear change of variables $x = By + c$ changes them in the same way. The step test is not affine invariant, but the iteration is.
- **Exact for linear systems.** If $F(x) = Ax - b$ with $A$ nonsingular, one step from any start lands on the solution.
- **Self-correcting.** Rounding errors in one step, and errors in the Jacobian, are corrected by the following steps.
- **No merit function.** A step need not decrease $\|F\|$; the globalized variants below enforce that.

## Variants and improvements

- **Finite-difference Jacobian.** Column $j$ is $(F(x + h_j e_j) - F(x))/h_j$ with $h_j \approx \sqrt u \max(|x_j|, 1)$; the convergence becomes fast linear or superlinear, and the limiting accuracy is unchanged (Dennis and Schnabel, Section 5.4). The implementation includes this.
- **Chord and Shamanskii methods.** Keep one factored Jacobian for several steps: linear convergence for the chord method, and order $m + 1$ when the Jacobian is refreshed every $m$ steps (Kelley, Chapter 5).
- **Quasi-Newton.** [Broyden's method](/broyden-method/) updates an approximation of $J$ by a rank-one change per step, with one evaluation of $F$ per step and $q$-superlinear local convergence; see [quasi-Newton methods](/quasi-newton-method/).
- **Inexact and Newton-Krylov.** Solve the Newton equation only to a relative residual $\eta_k$ with an iterative method such as [GMRES](/gmres/), needing only products $J v$, which can be approximated by differences of $F$. The order is linear, superlinear or quadratic as $\eta_k$ is fixed, tends to $0$, or is $O(\|F(x_k)\|)$ (Dembo, Eisenstat and Steihaug, 1982).
- **Globalization.** Damp the step, $x_{k+1} = x_k + \lambda_k s_k$ with $\lambda_k$ from a [backtracking line search](/backtracking-line-search/) on $\|F\|^2$, or use a trust region (Powell's dogleg). These make convergence from far away likely, though not certain, since they can stop at a local minimum of $\|F\|$ that is not a root.
- **Continuation.** Follow a path from an easy system to the hard one ([homotopy continuation](/homotopy-continuation/)), using Newton's method as the corrector.

## When to use it

Use Newton's method when the Jacobian is available or cheap to approximate, $n$ is small or $J$ is sparse enough to factor, and a good start is known, as in the time steps of an implicit integrator or the refinement of a nearby solution. Use a globalized version from a poor start, Broyden's method when $J$ is expensive, and Newton-Krylov for large sparse systems.

## Pitfalls

- **Singular or ill-conditioned Jacobian.** At the root $(0, 0)$ of $F(x, y) = (x^2, y)$ the Jacobian is singular, and the iterates halve: $x_k = 2^{-k}$. The relative step test with $\delta_a = 0$ never passes, since $\|s_k\| = \|x_{k+1}\|$, and the program runs to $k_{\max}$; with $\delta_a = 10^{-8}$ it stops after 27 passes (observed).
- **Singular Jacobian on the path.** In the example, any iterate on $y = \pm x$ gives a zero pivot; from $(0, 0)$ the program stops at once with the flag "singular".
- **No solution.** For $x^2 + y^2 + 1 = 0$, $x - y = 0$ the iterates never converge, and only $k_{\max}$ ends the loop.
- **Inverting the Jacobian.** Forming $J^{-1}$ costs more and is less accurate than solving with an LU factorization.
- **Inaccurate $F$.** No Jacobian, however exact, recovers accuracy lost in the evaluation of $F$.
- **Scaling.** The step test and line searches depend on the scaling of $x$ and $F$; scale the variables and equations to similar magnitudes.

## Implementations

## History

Thomas Simpson applied Newton's method to two equations in two unknowns in 1740, using what are now partial derivatives (Ypma, 1995). Henri Fine gave a convergence proof for systems in 1916, and Leonid Kantorovich extended the method to operator equations in Banach spaces in 1948, with the semilocal theorem that carries his name. The standard local theory, the finite-difference and quasi-Newton variants and the globalized methods were developed in the 1960s and 1970s and are surveyed by Ortega and Rheinboldt (1970) and Dennis and Schnabel (1983).

## References
