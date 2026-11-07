---
tag: MK4APS
kind: algorithm
slug: broyden-method
name: Broyden's method
aliases:
- Broyden's good method
- quasi-Newton method
- Broyden's first method
- multidimensional secant method
area: numerical/root-finding
level: advanced
summary: Newton's method for F(x) = 0 in R^n with the Jacobian replaced by a matrix B updated by a rank-one secant correction. One F evaluation per step, local superlinear convergence.
solves: [systems-of-nonlinear-equations]
model: real-ram
complexity:
  vars: {n: "the number of equations and unknowns", K: "the cap on the steps", δ: "the tolerance on the step"}
  time: {worst: "O(K n^3)", average: "O(n^3 log(1/δ))"}
  space: {extra: Θ(n^2)}
  evaluations: {worst: "K + n + 1", step: "1"}
properties: {deterministic: true, recursive: false, bracketing: false, derivative_free: true}
prereqs: [newton-method-for-systems, secant-method, systems-of-nonlinear-equations]
see_also: [quasi-newton-method, bfgs, sherman-morrison-formula, kantorovich-theorem, homotopy-continuation, backtracking-line-search, gaussian-elimination, stopping-criteria]
sources:
  - paper: doi:10.1090/S0025-5718-1965-0198670-6
    title: C. G. Broyden, A class of methods for solving nonlinear simultaneous equations, Mathematics of Computation 19(92), 577-593, 1965
    locator: the rank-one update of the Jacobian approximation (the good and the bad formulas) and the numerical tests, including the tridiagonal test function
  - paper: "C. G. Broyden, J. E. Dennis Jr. and Jorge J. Moré, On the local and superlinear convergence of quasi-Newton methods, Journal of the Institute of Mathematics and its Applications 12, 223-245, 1973"
    locator: the local and superlinear convergence theorem for Broyden's method
  - paper: "J. E. Dennis Jr. and Jorge J. Moré, A characterization of superlinear convergence and its application to quasi-Newton methods, Mathematics of Computation 28(126), 549-560, 1974"
    locator: the Dennis-Moré condition on (B_k - J(x*)) s_k
  - paper: "David M. Gay, Some convergence properties of Broyden's method, SIAM Journal on Numerical Analysis 16(4), 623-630, 1979"
    locator: termination in at most 2n steps on linear systems and 2n-step quadratic convergence
  - book: isbn:9780898713640
    title: J. E. Dennis Jr. and Robert B. Schnabel, Numerical Methods for Unconstrained Optimization and Nonlinear Equations, SIAM Classics in Applied Mathematics, 1996
    locator: Chapter 8, Secant Methods for Systems of Nonlinear Equations (Broyden's update as the least change secant update, bounded deterioration and the local superlinear convergence proof)
  - book: "C. T. Kelley, Iterative Methods for Linear and Nonlinear Equations, SIAM Frontiers in Applied Mathematics 16, 1995"
    locator: Chapter 7, Broyden's method (local convergence and the limited memory implementation)
---

Broyden's method solves a system $F(x) = 0$ of $n$ nonlinear equations in $n$ unknowns like [Newton's method](/newton-method-for-systems/), but without Jacobians. It keeps a matrix $B_k$ in place of $J(x_k)$, takes the step $s_k = -B_k^{-1}F(x_k)$, and then corrects $B_k$ by the smallest change that makes it match the new information: $B_{k+1}s_k = y_k = F(x_{k+1}) - F(x_k)$. That correction is rank one, $B_{k+1} = B_k + (y_k - B_ks_k)s_k^T/(s_k^Ts_k)$. Each step costs one evaluation of $F$ instead of $n + 1$ for a difference Jacobian, and near a root with nonsingular Jacobian, from a good enough start and starting matrix, the convergence is superlinear: $\|e_{k+1}\|/\|e_k\| \to 0$. For $n = 1$ it is the [secant method](/secant-method/). It is the root-finding member of the [quasi-Newton](/quasi-newton-method/) family, whose optimization member is [BFGS](/bfgs/).

## In plain words

Newton's method needs the matrix of all partial derivatives at every step, which is expensive. Broyden's method guesses that matrix once and then keeps a running estimate. After each step it knows how $F$ changed along the direction it just moved, so it fixes the estimate along that one direction and leaves it alone in every direction it learned nothing about. The estimate never needs to become exact: it only has to be right along the directions the iteration actually travels, and that is enough for fast convergence.

## The problem

Notation on the root-finding pages: $f$ is the function, $x^*$ a root, $x_k$ the iterates and $e_k = x_k - x^*$ the error. A method has [order](/order-of-convergence/) $q$ and rate constant $C$ when $|e_{k+1}| \approx C |e_k|^q$, with $0 < C < 1$ when $q = 1$. A root has [multiplicity](/multiplicity-of-roots/) $m$ when $f(x^*) = \cdots = f^{(m-1)}(x^*) = 0 \ne f^{(m)}(x^*)$. The cost is the number of evaluations of $f$ (and of $f'$ where a method uses it). A method of order $q$ that needs $w$ evaluations in each step has efficiency index $q^{1/w}$.

Here $f = F : \mathbb{R}^n \to \mathbb{R}^n$, $x^* \in \mathbb{R}^n$ with $F(x^*) = 0$, $J$ the Jacobian of $F$ and $J_* = J(x^*)$; errors are measured in a vector norm, $\|e_k\|$. The analogue of a simple root is a root with $J_*$ nonsingular. One evaluation is one vector $F(x)$. The input is $F$, a start $x_0$, an optional starting matrix $B_0$ (default: a forward difference Jacobian, $n$ extra evaluations), a tolerance $\delta$ and a cap $K$. The stopping rule is the step test $\|s_k\|_\infty \le \delta(1 + \|x_{k+1}\|_\infty)$, or $F(x_k) = 0$ exactly, or a singular $B_k$, or $K$ steps.

## The algorithm

```pseudo id=main
BROYDEN(F, x0, B0, delta, K):
L1   x <- x0;  Fx <- F(x);  B <- B0, or a forward difference Jacobian at x0 (n evaluations)
L2   for k = 1, 2, ..., K:
L3       if Fx = 0 then return x, "exact"
L4       solve B s = -Fx by Gaussian elimination with partial pivoting;  if B is singular then return x, "singular"
L5       x <- x + s;  Fnew <- F(x);  fail if it is not finite
L6       y <- Fnew - Fx;   B <- B + (y - B s) s^T / (s^T s)
L7       Fx <- Fnew
L8       if ||s|| <= delta (1 + ||x||) then return x, "converged"
L9   return x, "max-iter"
```

Line L4 is Newton's linear system with $B$ in place of $J(x)$. Line L6 is Broyden's update. After it, $Bs = y$ (the secant equation), and $Bz$ is unchanged for every $z$ orthogonal to $s$; among all matrices satisfying the secant equation it is the one closest to the old $B$ in the Frobenius norm. Line L8 tests the step: near the root the steps of a superlinear method are asymptotically equal in size to the errors, so a small step means a small error there, though not far from the root.

## Example

Take $F(x_1, x_2) = (x_1 + x_2 - 3,\ x_1^2 + x_2^2 - 9)$, with roots $(0, 3)$ and $(3, 0)$, start $x_0 = (1, 5)$ and $B_0 = J(x_0) = \begin{pmatrix} 1 & 1 \\ 2 & 10 \end{pmatrix}$. The first step is Newton's; after that only $F$ is evaluated. The iterates satisfy $x_1 + x_2 = 3$ from step 1 on, since the first equation is linear, and the error $\|e_k\|_\infty$ is:

| $k$ | Broyden $\|e_k\|$ | ratio $\|e_k\|/\|e_{k-1}\|$ | Newton $\|e_k\|$ |
|---|---|---|---|
| 1 | $6.25 \times 10^{-1}$ | | $6.25 \times 10^{-1}$ |
| 2 | $7.58 \times 10^{-2}$ | 0.121 | $9.19 \times 10^{-2}$ |
| 3 | $1.28 \times 10^{-2}$ | 0.169 | $2.65 \times 10^{-3}$ |
| 4 | $3.14 \times 10^{-4}$ | 0.0245 | $2.34 \times 10^{-6}$ |
| 5 | $1.33 \times 10^{-6}$ | 0.00425 | $1.83 \times 10^{-12}$ |
| 6 | $1.39 \times 10^{-10}$ | 0.000105 | $1.2 \times 10^{-16}$ |
| 7 | $7.4 \times 10^{-17}$ | | |

The ratios tend to 0, the signature of superlinear convergence, but the errors do not square as Newton's do. Broyden needs 7 steps and 8 evaluations of $F$ plus the starting Jacobian; Newton needs 6 steps, each with an evaluation of $F$ and of the $2 \times 2$ Jacobian. On Broyden's tridiagonal test function $F_i = (3 - 2x_i)x_i - x_{i-1} - 2x_{i+1} + 1$ from $x_0 = (-1, \dots, -1)$ with a difference Jacobian at the start, the method converged in 13, 14 and 14 steps for $n = 5, 20, 100$, that is $n + 14$ or $n + 15$ evaluations in all.

## Correctness

Let $F$ be continuously differentiable on an open convex set containing $x^*$, with $F(x^*) = 0$, $J_*$ nonsingular, and $\|J(x) - J(z)\| \le \gamma\|x - z\|$. Then there are $\varepsilon, \eta > 0$ such that if $\|e_0\| \le \varepsilon$ and $\|B_0 - J_*\|_F \le \eta$, every $B_k$ is nonsingular, $\|e_{k+1}\| \le \frac12\|e_k\|$, and $\|e_{k+1}\|/\|e_k\| \to 0$. The proof has three parts: the update is the least change secant update, its error in the Frobenius norm deteriorates by at most $O(\|e_k\| + \|e_{k+1}\|)$ per step, and the part of the error along $s_k$ is square summable, which by the Dennis-Moré argument gives superlinearity. This is a local result: from a poor start or with a poor $B_0$ the iteration can diverge. The loop stops after at most $K$ steps. The proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

Each step costs one evaluation of $F$, $O(n^2)$ for the update and, as written, $O(n^3)$ for solving with $B$ by elimination. Updating an inverse $H = B^{-1}$ with the [Sherman-Morrison formula](/sherman-morrison-formula/), or updating a QR factorization of $B$, brings the linear algebra down to $O(n^2)$ per step. Storage is $\Theta(n^2)$ for $B$; limited memory versions store only the last few $s_k$ and corrections. The order is not an integer: for $n = 1$ it is the golden ratio $1.618$, and for $n > 1$ the convergence is superlinear without a fixed order in general, though Gay showed $\|e_{k+2n}\| = O(\|e_k\|^2)$, so $2n$ steps do at least as well as one Newton step. When an evaluation of $F$ costs much more than the linear algebra and a Jacobian costs $n$ evaluations, Broyden's method is usually cheaper than Newton's for moderate and large $n$.

## Properties

- Needs no derivatives after $B_0$; one evaluation of $F$ per step.
- Local and q-superlinear at a root with nonsingular, Lipschitz Jacobian (proved), not quadratic.
- $B_k$ need not converge to $J_*$; it only has to be right along the steps.
- On an affine $F(x) = Ax - b$ with $A$ nonsingular it finds the root in at most $2n$ steps in exact arithmetic (Gay 1979); the tests check this with fractions.
- Invariant under a change of the equations $F \mapsto AF$ with $A$ nonsingular (then $B_k \mapsto AB_k$ and the iterates are the same), but not under a general change of the variables, because the update uses the Euclidean inner product of the steps; scaling the variables matters.
- For $n = 1$ it reduces to the secant method.

## Variants and improvements

- **Inverse update ("good" in inverse form).** Update $H_k = B_k^{-1}$ directly by Sherman-Morrison: $H_{k+1} = H_k + (s_k - H_ky_k)s_k^TH_k/(s_k^TH_ky_k)$. Same iterates, $O(n^2)$ per step.
- **Broyden's second ("bad") method.** Update $H$ by the least change in the Frobenius norm, $H_{k+1} = H_k + (s_k - H_ky_k)y_k^T/(y_k^Ty_k)$. It is also locally superlinear but usually less effective in practice.
- **Globalization.** Combine with a [backtracking line search](/backtracking-line-search/) or a trust region on $\|F\|^2$; since $B_k$ is not the Jacobian, the step need not be a descent direction, which complicates this.
- **Limited memory.** Store the update vectors and apply them as a product, as in Kelley's book; this suits large sparse problems.
- **Optimization.** For $\nabla g = 0$ the symmetric updates SR1, DFP and [BFGS](/bfgs/) keep $B$ symmetric, and BFGS keeps it positive definite.
- **Homotopy.** [Homotopy continuation](/homotopy-continuation/) gives good starts and good $B_0$ for each stage.

## When to use it

Use it for small to medium systems where Jacobians are not available or are expensive, and a decent start is known, for example in implicit time stepping where the previous step gives both $x_0$ and $B_0$. If the Jacobian is cheap, [Newton's method](/newton-method-for-systems/) converges in fewer steps. For very large systems use a Jacobian-free Newton-Krylov method or limited memory Broyden.

## Pitfalls

- L1: a poor $B_0$ can ruin the local theory; the identity matrix is a bad default unless $F$ is scaled so that $J_*$ is near the identity. A difference Jacobian costs $n$ evaluations but is usually worth it.
- L4: $B_k$ can become singular or badly conditioned even when $J_*$ is not; report "singular" rather than dividing by zero, and restart with a fresh Jacobian.
- L6: when $s$ is tiny, $y - Bs$ is dominated by rounding in $F$, and the update injects noise into $B$; stop before that, which the step test at L8 does.
- L6: computing the update with $s^Ts$ that underflows gives an infinite correction. Scale the variables so that $x$ is of order 1.
- L8: a small step proves little far from a root, and the residual can still be large; check $\|F(x)\|$ against the expected accuracy.

## Implementations

## History

Charles George Broyden introduced the method in 1965 in Mathematics of Computation, proposing two rank-one updates, now called the good and the bad Broyden methods, and testing them on problems that included the tridiagonal function above. Its local superlinear convergence was proved by Broyden, Dennis and Moré in 1973, and Dennis and Moré's 1974 characterization of superlinear convergence gave the standard tool for analysing such updates. Gay proved finite termination on linear systems in 1979. The same least change idea led to the DFP and BFGS updates of unconstrained optimization.

## References
