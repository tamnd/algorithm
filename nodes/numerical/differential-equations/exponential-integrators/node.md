---
tag: 4R98K0
kind: algorithm
slug: exponential-integrators
name: Exponential integrators
aliases:
- exponential time differencing
- ETD methods
- exponential Runge-Kutta methods
- exponential Euler method
area: numerical/differential-equations
level: research
summary: "Methods for y' = Ay + g(t, y) that integrate the stiff linear part exactly with e^(hA) and the φ-functions and treat only g explicitly. Exponential Euler has order 1, ETD2RK order 2."
solves: [stiff-ode-problem, ode-initial-value-problem]
model: real-ram
complexity:
  vars: {N: "the number of steps, ⌈(T - t_0)/h⌉", d: "the dimension of y", s: "the number of squarings, about log_2 of the norm of hA", q: "the number of Taylor terms, at most 40 and about 13 in practice", C: "the cost of one evaluation of g"}
  time: {worst: "Θ((q + s) d^3 + N (C + d^2))"}
  space: {extra: "Θ(d^2)"}
  evaluations: {worst: "2 N"}
properties: {deterministic: true, implicit: false, one_step: true, order: "2", stiff_order: "2", exact_for_linear_part: true, preserves_equilibria: true}
history:
  year: 1960
  people: [John Certaine, J. Douglas Lawson, Steven M. Cox, Paul C. Matthews, Marlis Hochbruck, Alexander Ostermann]
  note: Certaine (1960) and Lawson (1967) built multistep and Runge-Kutta methods around the exponential of the linear part; Cox and Matthews (2002) popularized exponential time differencing (ETD2RK, ETDRK4) for stiff PDEs, and Hochbruck and Ostermann (2005) derived the stiff order conditions.
prereqs: [stiff-ode-problem, runge-kutta-methods, method-of-lines]
see_also: [rosenbrock-methods, operator-splitting, spectral-methods, arnoldi-iteration, pade-approximation, heuns-method, heat-equation, gronwall-inequality]
sources:
  - paper: doi:10.1017/S0962492910000048
    title: Marlis Hochbruck and Alexander Ostermann, Exponential integrators, Acta Numerica 19 (2010) 209-286
    locator: Section 2 (exponential Runge-Kutta methods, the exponential Euler method, stiff order conditions and convergence for parabolic problems), Section 4 (computing products of φ-functions with vectors)
  - paper: doi:10.1006/jcph.2002.6995
    title: S. M. Cox and P. C. Matthews, Exponential time differencing for stiff systems, Journal of Computational Physics 176 (2002) 430-455
    locator: the first-order ETD scheme, the two-stage ETD2RK scheme and the fourth-order ETDRK4 scheme
  - paper: doi:10.1137/S1064827502410633
    title: Aly-Khan Kassam and Lloyd N. Trefethen, Fourth-order time-stepping for stiff PDEs, SIAM Journal on Scientific Computing 26(4) (2005) 1214-1233
    locator: cancellation in the φ-functions and their evaluation by contour integrals
  - book: isbn:9780898716467
    title: Nicholas J. Higham, Functions of Matrices, Theory and Computation, SIAM, 2008
    locator: Chapter 10 (the matrix exponential, scaling and squaring, the φ-functions via an augmented matrix)
---

Exponential integrators solve semilinear systems $y' = Ay + g(t, y)$, where the matrix $A$ carries the stiffness (for instance a discretized diffusion operator) and $g$ is a mild nonlinearity. They treat the linear part exactly through the matrix exponential $e^{hA}$ and the related functions $\varphi_1(z) = (e^z - 1)/z$, $\varphi_2(z) = (e^z - 1 - z)/z^2$, and approximate only $g$. The simplest is the exponential Euler method $y_{n+1} = e^{hA}y_n + h\varphi_1(hA)g(t_n, y_n)$; the two-stage ETD2RK method of Cox and Matthews adds a correction with $\varphi_2$ and has order 2. The methods are explicit in $g$, need no Newton iteration, and are stable for steps far beyond the explicit stability limit, with error constants that, for smooth solutions and $\|e^{tA}\| \le 1$, do not depend on $\|A\|$.

## In plain words

Many problems mix a fast, simple part with a slow, complicated one. Heat spreading on a fine grid is fast and simple; a chemical reaction on top of it is slow but nonlinear. Ordinary explicit methods must take tiny steps because of the fast part, even when nothing interesting happens on that time scale. An exponential integrator solves the fast simple part exactly, using a precomputed matrix that says how the linear system evolves over one step. It approximates only the slow part, in the way an ordinary explicit method would. So the step size is set by the slow part, not by the fast one. The price is computing that matrix (or its effect on vectors) once per step size.

## The problem

Given a matrix $A \in \mathbb{R}^{d \times d}$, a function $g : [t_0, T] \times \mathbb{R}^d \to \mathbb{R}^d$ and $y_0$, approximate the solution of the semilinear [initial value problem](/ode-initial-value-problem/) $y' = Ay + g(t, y)$, $y(t_0) = y_0$, at $T$. The interesting case is a [stiff problem](/stiff-ode-problem/): $\|A\|$ is large (the stiff part), while $g$ is Lipschitz with a moderate constant $L$ and the exact solution is smooth. The exact solution satisfies the variation-of-constants formula

$$y(t_n + h) = e^{hA}y(t_n) + \int_0^he^{(h - \sigma)A}g\big(t_n + \sigma, y(t_n + \sigma)\big)\,d\sigma,$$

and exponential integrators are quadrature rules for this integral in which only $g$ is approximated. With $\varphi_0(z) = e^z$ and $\varphi_k(z) = \int_0^1e^{(1-\theta)z}\frac{\theta^{k-1}}{(k-1)!}\,d\theta = \sum_{j \ge 0}\frac{z^j}{(j+k)!}$, one has $\int_0^he^{(h-\sigma)A}d\sigma = h\varphi_1(hA)$ and $\int_0^he^{(h-\sigma)A}\frac{\sigma}{h}d\sigma = h\varphi_2(hA)$.

## The algorithm

```pseudo id=main
ETD2RK(A, g, t0, y0, T, h)
L1  N ← max(1, ⌈(T − t0)/h − δ⌉); k ← (T − t0)/N        ▷ equal steps, so the matrices are computed once
L2  [E P1 P2] ← first block row of exp(W), W = [[kA, I, 0], [0, 0, I], [0, 0, 0]]   ▷ E = e^(kA), P_j = φ_j(kA)
L3  for n ← 0 to N − 1 do
L4      G ← g(t_n, y_n)
L5      a ← E y_n + k P1 G                                 ▷ exponential Euler predictor
L6      D ← g(t_n + k, a) − G
L7      y_(n+1) ← a + k P2 D                               ▷ second-order correction
L8  return y_N
```

Line L2 obtains all three matrices from one exponential of a $3d \times 3d$ block matrix: the first block row of $W^j$ is $[Z^j, Z^{j-1}, Z^{j-2}]$ for $Z = kA$ and $j \ge 2$, so the series for $e^W$ has $\varphi_1(Z)$ and $\varphi_2(Z)$ in its top right blocks. The exponential is computed by scaling and squaring: divide $W$ by $2^s$ until its 1-norm is at most $\tfrac12$, sum the Taylor series until the terms are below $10^{-18}$, and square $s$ times. Evaluating $\varphi_1, \varphi_2$ by their closed forms instead would cancel catastrophically for small $\|Z\|$. Stopping after line L5 gives the exponential Euler method.

The steps are equal so that line L2 runs once. Methods that change the step must recompute the matrices, or, for large sparse $A$, compute only the products $\varphi_j(kA)v$ by Krylov ([Arnoldi](/arnoldi-iteration/)) approximations.

## Example

**One step by hand.** $y' = -4y + t$, $y(0) = 1$, one step $h = \tfrac12$. Here $z = hA = -2$, $e^{-2} = 0.135335$, $\varphi_1(-2) = 0.432332$, $\varphi_2(-2) = 0.283834$.

- L4: $G = g(0) = 0$.
- L5: $a = 0.135335 \cdot 1 + \tfrac12 \cdot 0.432332 \cdot 0 = 0.135335$.
- L6: $D = g(\tfrac12) - 0 = \tfrac12$.
- L7: $y_1 = 0.135335 + \tfrac12 \cdot 0.283834 \cdot \tfrac12 = 0.206294$.

The exact value is $y(\tfrac12) = \tfrac{17}{16}e^{-2} + \tfrac18 - \tfrac1{16} = 0.206294$: ETD2RK is exact when $g$ is affine in $t$ and independent of $y$. Explicit Euler with the same step sits on its stability boundary ($y_1 = 1 + \tfrac12(-4) = -1$).

**A stiff reaction-diffusion problem.** The Chafee-Infante equation $u_t = u_{xx} + 20(u - u^3)$ on $(0, 1)$ with $u = 0$ at both ends, discretized with 15 interior points ($\Delta x = \tfrac1{16}$, so $A$ is the second difference matrix with eigenvalues down to $-1014$), $u_0(x) = 0.1\sin\pi x$, $T = 0.25$. Errors in the maximum norm against an RK4 reference with $h = \tfrac1{2000}$:

| $h$ | 0.05 | 0.025 | 0.0125 | 0.00625 | 0.003125 | 0.0015625 |
|---|---|---|---|---|---|---|
| ETD2RK | $4.35 \times 10^{-2}$ | $1.29 \times 10^{-2}$ | $3.61 \times 10^{-3}$ | $9.62 \times 10^{-4}$ | $2.49 \times 10^{-4}$ | $6.35 \times 10^{-5}$ |
| observed order | | 1.75 | 1.84 | 1.91 | 1.95 | 1.97 |
| exponential Euler | $2.00 \times 10^{-1}$ | $9.53 \times 10^{-2}$ | $4.38 \times 10^{-2}$ | $2.07 \times 10^{-2}$ | $1.00 \times 10^{-2}$ | $4.94 \times 10^{-3}$ |

Classical RK4 is unstable here for $h$ above about $2.7 \times 10^{-3}$ (it overflows at $h = 0.01$), while ETD2RK is stable at every step size; the error, not stability, decides the step.

**Stiffness-independent error.** For $y' = \lambda(y - \sin t) + \cos t$, $y(0) = 1$, on $[0, 2]$, the ETD2RK error satisfies $|y_N - y(2)| \le 0.1h^2$ for all $h = 2^{-3}, \ldots, 2^{-8}$ and all $\lambda \in \{-10^2, -10^4, -10^6\}$.

## Correctness

The proof file shows four things.

1. **Line L2 is correct:** the first block row of $\exp(W)$ is $[e^Z, \varphi_1(Z), \varphi_2(Z)]$, by the power formula above.
2. **Exactness.** ETD2RK reproduces the exact solution when $g(t, y) = c_0 + c_1t$ (variation of constants with a linear integrand), and both methods keep every equilibrium $y^*$ of $Ay + g(y) = 0$ fixed, for every step size.
3. **Quadrature form.** ETD2RK replaces $g(t_n + \sigma, y(t_n + \sigma))$ in the variation-of-constants integral by the linear interpolant between $g(t_n, y_n)$ and $g(t_{n+1}, a)$; exponential Euler replaces it by the constant $g(t_n, y_n)$.
4. **Stiff convergence (proved).** If $\|e^{tA}\| \le 1$ for $t \ge 0$ (for example $A$ symmetric negative semidefinite in the 2-norm), $g$ is Lipschitz in $y$ with constant $L$, and $F(t) = g(t, y(t))$ has bounded first and second derivatives along the exact solution, then exponential Euler has global error $\le C_1h$ and ETD2RK $\le C_2h^2$, with $C_1, C_2$ depending on $L$, $T - t_0$ and the bounds on $F', F''$, but not on $\|A\|$.

For parabolic problems with unbounded $A$ (analytic semigroups), the general stiff order theory is due to Hochbruck and Ostermann (2005; survey 2010, Section 2); that part is cited.

## Complexity

Line L2 multiplies $3d \times 3d$ matrices $q + s$ times, where $s \approx \log_2(2\|kA\|_1)$ squarings and $q$ Taylor terms (about 13 in double precision): $\Theta((q + s)d^3)$ once. Each step evaluates $g$ twice and does three matrix-vector products, $\Theta(C + d^2)$, so the total is $\Theta((q + s)d^3 + N(C + d^2))$ time and $\Theta(d^2)$ extra space for the three matrices, in the [real RAM](/real-ram/) model. Exponential Euler needs $N$ evaluations of $g$ and two products per step.

For large sparse $A$ (a PDE in several dimensions), dense $d \times d$ matrices are out of the question; Krylov methods compute $\varphi_j(kA)v$ with a few dozen sparse products per step, and for diagonal $A$ (Fourier spectral methods for periodic problems) the $\varphi_j$ are applied entrywise at $O(d)$ cost.

## Properties

- **Explicit in $g$.** No nonlinear equations, no Jacobians of $g$.
- **Exact for the linear part.** For $g = 0$ the method returns $e^{NkA}y_0$ up to the accuracy of the exponential: for a rotation, the norm is conserved to rounding.
- **No step size restriction from $A$.** For $\|e^{tA}\| \le 1$ the amplification of errors per step is at most $1 + O(kL)$, whatever $\|A\|$.
- **Preserves equilibria** exactly, unlike most Runge-Kutta methods applied to $y' = Ay + g$.
- **Order 2 (ETD2RK) and 1 (exponential Euler)**, with constants independent of the stiffness under the conditions above.
- **Reduces to Heun's method and Euler's method** when $A = 0$, since $\varphi_1(0) = 1$ and $\varphi_2(0) = \tfrac12$.

## Variants and improvements

- **Lawson methods** (integrating factor methods). Substitute $v = e^{-tA}y$ and apply any Runge-Kutta method to $v' = e^{-tA}g(t, e^{tA}v)$. Simple, but the order drops for stiff problems and equilibria are not preserved.
- **ETDRK4 and Krogstad's method.** Four-stage exponential Runge-Kutta methods of Cox and Matthews (2002) and Krogstad (2005); Kassam and Trefethen (2005) evaluate their $\varphi$-functions by contour integrals to avoid cancellation. Full stiff order 4 needs five stages (Hochbruck and Ostermann 2005).
- **Exponential multistep methods** (Certaine 1960, Nørsett 1969) and **exponential Rosenbrock methods**, which linearize $g$ at each step and put the Jacobian into the exponential, like [Rosenbrock methods](/rosenbrock-methods/) do for implicit Runge-Kutta.
- **Krylov and Leja approximations** of $\varphi_j(kA)v$ for large sparse $A$, with adaptive step size control.
- **Splitting.** [Operator splitting](/operator-splitting/) also uses $e^{kA}$, but alternates it with steps for $g$; exponential integrators avoid the splitting error.

## When to use it

Use exponential integrators for semilinear stiff problems where $A$ is known and its exponential (or its action on vectors) is cheap: Fourier spectral discretizations of reaction-diffusion, Kuramoto-Sivashinsky, nonlinear Schrödinger and KdV equations, and finite difference or finite element semidiscretizations of parabolic problems with a mild nonlinearity. When the stiffness sits in the nonlinear part, or the Jacobian changes a lot, implicit methods ([Radau IIA](/radau-iia-methods/), BDF) or exponential Rosenbrock methods are better.

## Pitfalls

- **Cancellation in the φ-functions.** $(e^z - 1 - z)/z^2$ evaluated directly keeps only about 6 correct digits at $|z| = 10^{-5}$ and none at $|z| = 10^{-8}$ (it returns $-0.61$ instead of $0.5$); use the series, the augmented matrix, or contour integrals.
- **Changing the step size.** Every new $k$ needs new $\varphi_j(kA)$; equal steps (line L1) or Krylov methods avoid repeated dense exponentials.
- **Taking the stiffness into $g$.** The method is only as good as the split: if $g$ contains stiff terms, the explicit treatment of $g$ restores a step size limit.
- **Non-normal $A$.** For strongly non-normal $A$, $\|e^{tA}\|$ can grow transiently even with stable eigenvalues, and the error constants grow with it.
- **Order claims from nonstiff theory.** A method of classical order $p$ can have lower stiff order; for example, Lawson methods and some four-stage ETD schemes lose order on parabolic problems.

## Implementations

## History

Certaine (1960) proposed multistep methods built on the exact solution of the linear part, and Lawson (1967) introduced generalized Runge-Kutta methods via the integrating factor. Nørsett (1969) developed exponential Adams methods. The approach was revived when Krylov methods made $\varphi_j(A)v$ affordable for large problems (Hochbruck and Lubich 1997) and when Cox and Matthews (2002) proposed exponential time differencing schemes, including ETD2RK and ETDRK4, for stiff PDEs; Kassam and Trefethen (2005) fixed their numerical evaluation. Hochbruck and Ostermann (2005) derived the stiff order conditions for exponential Runge-Kutta methods and surveyed the field in Acta Numerica in 2010.

## References
