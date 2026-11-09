---
tag: R6JAK0
kind: technique
slug: quasi-newton-method
name: Quasi-Newton method
aliases:
- secant-type methods
- variable metric methods
- secant methods for minimization
area: optimization/gradient-methods
level: advanced
summary: "Replace the Hessian in Newton's step by a matrix updated from gradient differences so that B_(k+1) s_k = y_k. Each step costs O(n^2) and no second derivatives; the local rate is superlinear."
prereqs: [gradient-descent, newton-method-for-systems, secant-method, wolfe-conditions, positive-definite-matrix]
see_also: [bfgs, limited-memory-bfgs, broyden-method, secant-method, newton-method-for-systems, nonlinear-conjugate-gradient, wolfe-conditions, sherman-morrison-formula]
sources:
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006
    locator: Chapter 6, Quasi-Newton methods (the secant equation, BFGS, DFP, SR1 and the Broyden class), and Section 3.3, Rate of convergence (the Dennis-Moré characterization of superlinear convergence)
  - book: isbn:9780898713640
    title: John E. Dennis Jr. and Robert B. Schnabel, Numerical Methods for Unconstrained Optimization and Nonlinear Equations, SIAM, 1996
    locator: Chapters 8 and 9 (secant methods for systems of equations and for unconstrained minimization)
  - paper: doi:10.1137/0801001
    title: William C. Davidon, Variable metric method for minimization, SIAM Journal on Optimization 1(1), 1991 (a reprint of the 1959 Argonne National Laboratory report)
    locator: pages 1 to 17
  - paper: doi:10.1093/comjnl/6.2.163
    title: Roger Fletcher and Michael J. D. Powell, A rapidly convergent descent method for minimization, The Computer Journal 6(2), 1963
    locator: pages 163 to 168 (the DFP update)
  - paper: doi:10.1090/S0025-5718-1965-0198670-6
    title: Charles G. Broyden, A class of methods for solving nonlinear simultaneous equations, Mathematics of Computation 19(92), 1965
    locator: pages 577 to 593
  - paper: doi:10.1090/S0025-5718-1974-0343581-1
    title: John E. Dennis Jr. and Jorge J. Moré, A characterization of superlinear convergence and its application to quasi-Newton methods, Mathematics of Computation 28(126), 1974
    locator: pages 549 to 560
  - paper: doi:10.1137/1019005
    title: John E. Dennis Jr. and Jorge J. Moré, Quasi-Newton methods, motivation and theory, SIAM Review 19(1), 1977
    locator: pages 46 to 89
---

A quasi-Newton method is a line search method whose search direction is $d_k = -H_k\nabla f(x_k)$, where $H_k$ is a symmetric matrix that stands in for the inverse Hessian $\nabla^2f(x_k)^{-1}$ of Newton's method. After each step, $H_k$ gets a low-rank update built from the step $s_k = x_{k+1} - x_k$ and the gradient change $y_k = \nabla f(x_{k+1}) - \nabla f(x_k)$, so that the new matrix satisfies the *secant equation* $H_{k+1}y_k = s_k$, or $B_{k+1}s_k = y_k$ for $B = H^{-1}$. The method needs only gradients, one step costs $O(n^2)$ in place of the $O(n^3)$ of a Newton solve, and near a minimizer with a positive definite Hessian it converges superlinearly. [BFGS](/bfgs/) is the main example, and [L-BFGS](/limited-memory-bfgs/) is its form for large $n$.

## In plain words

Newton's method knows the exact curvature of the function at each point and jumps to the bottom of the bowl that has this curvature. Computing that curvature is expensive, and often there is no formula for it.

A quasi-Newton method learns the curvature as it goes. After each step it compares the slope at the new point with the slope at the old point. The change in slope over the length of the step says how strongly the function bends in that direction. The method corrects its guess of the curvature so that the guess agrees with this measurement, and keeps the rest of the guess as it was.

At first the guess is poor and the steps are like those of plain downhill walking. After some steps the guess is good in the directions that matter, and the steps become almost as good as Newton's.

## When it applies

- $f : \mathbb{R}^n \to \mathbb{R}$ is smooth, and $\nabla f$ is available, but the Hessian is not available or is too expensive.
- $n$ is small enough to store an $n \times n$ matrix, a few thousand variables at most. For larger $n$, keep only the last few pairs $(s, y)$, as in [L-BFGS](/limited-memory-bfgs/).
- The step satisfies the curvature condition $y_k^\top s_k > 0$. A line search with the [Wolfe conditions](/wolfe-conditions/) ensures it, because the second Wolfe condition gives $y_k^\top s_k \ge (c_2 - 1)\alpha_k\nabla f(x_k)^\top d_k > 0$. For a strictly convex $f$ it holds for every step.
- The fast local rate needs a minimizer $x^*$ with $\nabla^2f(x^*)$ positive definite and $\nabla^2f$ continuous near $x^*$.

## The template

```pseudo id=main
QUASI-NEWTON(f, ∇f, x₀, H₀, UPDATE, ε)
L1  x ← x₀; g ← ∇f(x); H ← H₀                      ▷ often H₀ = I
L2  while ‖g‖ > ε do
L3      d ← −H g
L4      α ← a step along d that satisfies the Wolfe conditions, trying α = 1 first
L5      s ← α d; x ← x + s; g⁺ ← ∇f(x); y ← g⁺ − g
L6      H ← UPDATE(H, s, y)                          ▷ symmetric, with H y = s
L7      g ← g⁺
L8  return x
```

The holes are the start $H_0$, the line search of line L4 and the rule UPDATE of line L6. The update is a rank-one or rank-two correction, so it costs $O(n^2)$, and line L3 costs $O(n^2)$. One iteration costs $O(n^2)$ plus the values of $f$ and $\nabla f$ in the line search, and the memory is $O(n^2)$.

**Why the secant equation.** By the fundamental theorem of calculus, $y_k = \bar{A}_ks_k$ with $\bar{A}_k = \int_0^1\nabla^2f(x_k + ts_k)\,dt$, the average Hessian along the step. So the secant equation $B_{k+1}s_k = y_k$ asks $B_{k+1}$ to act on $s_k$ as the true curvature did. In one dimension it fixes $B_{k+1} = y_k/s_k$, and the method is the [secant method](/secant-method/) applied to $f'$. In $n$ dimensions the equation fixes only $n$ of the $n(n+1)/2$ entries of a symmetric matrix, and each method chooses the rest by asking for the smallest change to $B_k$ or $H_k$ in some weighted norm.

**Why trying α = 1 matters.** The Newton step has $\alpha = 1$. The fast local rate needs the method to take unit steps near $x^*$, so the line search must try $\alpha = 1$ first and accept it when it passes. With $c_1 < \frac12$ the Armijo test accepts the unit step near $x^*$ once $H_k$ is accurate enough along $d_k$ (Nocedal and Wright, Section 3.3).

**Superlinear rate (Dennis and Moré).** Let $f$ be twice continuously differentiable, let $x_{k+1} = x_k + d_k$ with $d_k = -H_k\nabla f(x_k)$ (unit steps) and $B_k = H_k^{-1}$, and let $x_k \to x^*$ with $\nabla f(x^*) = 0$ and $\nabla^2f(x^*)$ positive definite, $x_k \ne x^*$. Then $\|x_{k+1} - x^*\| = o(\|x_k - x^*\|)$ if and only if
$$\lim_{k\to\infty}\frac{\|(B_k - \nabla^2f(x^*))d_k\|}{\|d_k\|} = 0.$$
So the matrices need not converge to the Hessian; they need to be right only along the steps taken. *Proof of the "if" part.* Let $A_k = \nabla^2f(x_k)$, $e_k = x_k - x^*$, and let $d^N_k = -A_k^{-1}\nabla f(x_k)$ be the Newton step, defined for large $k$. Since $\nabla f(x_k) = \int_0^1\nabla^2f(x^* + te_k)\,dt\;e_k$, we get $e_k + d^N_k = A_k^{-1}\int_0^1\left(A_k - \nabla^2f(x^* + te_k)\right)dt\;e_k = o(\|e_k\|)$ by the continuity of $\nabla^2f$. Also $d_k - d^N_k = A_k^{-1}(A_kd_k + \nabla f(x_k)) = A_k^{-1}(A_k - B_k)d_k$, and $A_k \to \nabla^2f(x^*)$, so the condition gives $\|d_k - d^N_k\| = o(\|d_k\|)$. Hence $\|e_{k+1}\| = \|e_k + d_k\| \le \|e_k + d^N_k\| + \|d_k - d^N_k\| = o(\|e_k\|) + o(\|d_k\|)$. Since $\|d_k\| \le \|e_{k+1}\| + \|e_k\|$, the term $o(\|d_k\|)$ is at most $\frac12\|e_{k+1}\| + o(\|e_k\|)$ for large $k$, and so $\|e_{k+1}\| = o(\|e_k\|)$. $\square$ Dennis and Moré also prove the converse.

## Classic examples

With $\rho = 1/(y^\top s)$ and $r = y - Bs$:

- **BFGS** (Broyden, Fletcher, Goldfarb and Shanno, 1970). $H^+ = (I - \rho sy^\top)H(I - \rho ys^\top) + \rho ss^\top$. It keeps $H$ positive definite when $y^\top s > 0$, and it is the default choice. See [BFGS](/bfgs/).
- **DFP** (Davidon, Fletcher and Powell). $H^+ = H - \frac{Hyy^\top H}{y^\top Hy} + \rho ss^\top$. It is the BFGS formula with the roles of $(H, s, y)$ and $(B, y, s)$ exchanged. It also keeps positive definiteness, but it corrects bad curvature estimates more slowly than BFGS, and it is little used now.
- **SR1** (symmetric rank one). $B^+ = B + \frac{rr^\top}{r^\top s}$. It is the only symmetric rank-one update with $B^+s = y$, and it can produce indefinite matrices, which suits trust-region methods and nonconvex problems. Skip the update when $|r^\top s|$ is tiny compared with $\|r\|\|s\|$.
- **Broyden's method** for a system $F(x) = 0$. $B^+ = B + \frac{(y - Bs)s^\top}{s^\top s}$, the smallest change in the Frobenius norm with $B^+s = y$. The matrix is not symmetric. See [Broyden's method](/broyden-method/).
- **L-BFGS.** Keep only the last $m$ pairs $(s, y)$ and apply the BFGS inverse to a vector by the two-loop recursion in $O(mn)$ time. See [L-BFGS](/limited-memory-bfgs/).

## Variations

- **The Broyden class.** $B^+_\phi = (1 - \phi)B^+_{BFGS} + \phi B^+_{DFP}$. All its members satisfy the secant equation; with exact line searches on a strictly convex quadratic, the members with $\phi \ge 0$ produce the same iterates and terminate in at most $n$ steps (Nocedal and Wright, Chapter 6).
- **Direct or inverse form.** Update $B$ and solve $Bd = -g$ with a Cholesky factor that is updated in $O(n^2)$, or update $H$ and multiply. The inverse form is simpler; the factored direct form is more stable when $B$ is close to singular.
- **Scaling of $H_0$.** Before the first update, replace $H_0 = I$ by $\frac{y_0^\top s_0}{y_0^\top y_0}I$, which matches the size of the true curvature along the first step.
- **Damped updates.** When $y^\top s$ is too small or negative, as can happen in constrained or nonconvex problems, Powell's damping replaces $y$ by a combination of $y$ and $Bs$ that keeps positive definiteness.
- **Trust regions.** Use $B_k$ in a trust-region model in place of a line search. This is the usual setting for SR1.

## Pitfalls

- **Backtracking only.** The Armijo condition alone does not give $y^\top s > 0$. Then BFGS loses positive definiteness, $d$ may go uphill, and the division by $y^\top s$ can blow up. Use a Wolfe line search, or skip the update when $y^\top s \le 10^{-8}\|s\|\|y\|$.
- **No unit step.** A line search that never tries $\alpha = 1$, or that always shortens it, loses the superlinear rate.
- **Too many variables.** The $n \times n$ matrix costs $8n^2$ bytes in double precision and $O(n^2)$ time per step. For $n$ in the tens of thousands this is too much; use L-BFGS.
- **Nonconvex functions.** There are smooth nonconvex functions on which BFGS with a Wolfe line search, and even with exact line searches, does not reach a stationary point (Dai, 2002; Mascarenhas, 2004). Global convergence results for BFGS assume convexity.
- **Finite differences.** If the gradient is a finite difference approximation, $y$ is noisy for short steps, and the curvature estimate can be wrong.

## Exercises

1. Show that the BFGS and DFP inverse updates satisfy $H^+y = s$, and that the SR1 and Broyden updates satisfy $B^+s = y$.
2. Show that the second Wolfe condition implies $y_k^\top s_k > 0$.
3. Let $B$ be symmetric and $r^\top s \ne 0$. Prove that the SR1 update is the only symmetric matrix $B^+$ with $B^+ - B$ of rank one and $B^+s = y$.
4. Prove that if $H$ is positive definite and $y^\top s > 0$, the BFGS update $H^+$ is positive definite.
5. In one dimension, show that each update of this page gives $B^+ = y/s$, so the method is the secant method applied to $f'$.

## References
