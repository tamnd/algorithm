---
tag: XDMCM0
kind: technique
slug: collocation-method
name: Collocation methods
aliases:
- orthogonal collocation
- collocation
- piecewise polynomial collocation
area: numerical/differential-equations
level: advanced
summary: Approximate the solution by a polynomial on each step and require the equation to hold exactly at chosen points. For ODEs this gives implicit Runge-Kutta methods such as Gauss and Radau IIA.
prereqs: [bvp-boundary-value-problem, butcher-tableau, polynomial-interpolation]
see_also: [gauss-legendre-runge-kutta, radau-iia-methods, butcher-order-conditions, gaussian-quadrature, spectral-methods, galerkin-method, shooting-method, dense-output]
sources:
  - book: isbn:9783540566700
    title: Ernst Hairer, Syvert P. Nørsett and Gerhard Wanner, Solving Ordinary Differential Equations I, Nonstiff Problems, second revised edition, Springer, 1993
    locator: Section II.7 (implicit Runge-Kutta methods, collocation methods, the order theorem for collocation and the error of the collocation polynomial, simplifying assumptions)
  - book: isbn:9783540604525
    title: Ernst Hairer and Gerhard Wanner, Solving Ordinary Differential Equations II, Stiff and Differential-Algebraic Problems, second revised edition, Springer, 1996
    locator: Section IV.5 (Gauss, Radau and Lobatto methods as collocation methods) and Section IV.15 (order reduction for stiff problems)
  - book: isbn:9780898713541
    title: Uri M. Ascher, Robert M. M. Mattheij and Robert D. Russell, Numerical Solution of Boundary Value Problems for Ordinary Differential Equations, SIAM, 1995
    locator: Chapter 5 (finite difference methods, including collocation for first order systems and higher order equations, superconvergence at mesh points)
  - book: isbn:9780898714128
    title: Uri M. Ascher and Linda R. Petzold, Computer Methods for Ordinary Differential Equations and Differential-Algebraic Equations, SIAM, 1998
    locator: Chapter 4 (implicit Runge-Kutta and collocation methods) and Chapter 8 (finite difference and collocation methods for boundary value problems)
  - paper: "C. de Boor and B. Swartz, Collocation at Gaussian points, SIAM Journal on Numerical Analysis 10 (1973) 582-606"
    locator: the error of piecewise polynomial collocation at Gauss points for boundary value problems, superconvergence at the mesh points
  - paper: "K. Wright, Some relationships between implicit Runge-Kutta, collocation and Lanczos τ methods, and their stability properties, BIT 10 (1970) 217-227"
    locator: the equivalence of collocation and implicit Runge-Kutta methods
---

## In plain words

You want a function that satisfies a differential equation, but you can only handle simple functions, such as polynomials. Collocation picks a polynomial with a few free coefficients and demands that the equation hold exactly at the same number of chosen points. Between those points the equation is only nearly satisfied. With good points, the error is far smaller than the number of points suggests. For time stepping, this produces the strongest implicit Runge-Kutta methods. For boundary value problems, it gives a smooth approximate solution on the whole interval, and many standard solvers work this way.

## When it applies

- **Initial value problems** $y' = f(t, y)$, $y(t_0) = y_0$, $y \in \mathbb{R}^d$, where an implicit one-step method of high order or good stability is needed, for example stiff problems.
- **Boundary value problems** $y' = f(t, y)$ on $[a, b]$ with $g(y(a), y(b)) = 0$, and higher order equations, where [shooting](/shooting-method/) is unstable or a continuous solution is wanted.
- **PDEs and integral equations**, with global polynomials at Chebyshev or Legendre points ([spectral collocation](/spectral-methods/)), or with piecewise polynomials.
- It needs: $f$ smooth enough for the order claimed, distinct collocation points, and a way to solve the resulting nonlinear system, usually [Newton's method](/newton-method-for-systems/).

## The template

On a step $[t_n, t_n + h]$ choose distinct numbers $c_1, \dots, c_s$ in $[0, 1]$. Let $\ell_j$ be the Lagrange basis polynomials of degree $s - 1$ for these points.

```pseudo id=template
COLLOCATE(f, mesh t_0 < … < t_N, c_1, …, c_s, side conditions)
L1  on each [t_n, t_{n+1}] take an unknown polynomial u_n of degree ≤ s with values in R^d
L2  for each n and each i: require u_n′(t_n + c_i h_n) = f(t_n + c_i h_n, u_n(t_n + c_i h_n))
L3  for 0 < n < N: require u_n(t_n) = u_{n−1}(t_n)                 ▷ continuity
L4  require the side conditions: u_0(t_0) = y_0 (IVP) or g(u(a), u(b)) = 0 (BVP)
L5  solve the algebraic system by Newton's method                  ▷ for an IVP, one step at a time
L6  estimate the error, refine the mesh where it is large, and repeat if needed
L7  return the piecewise polynomial u
```

There are $(s + 1)dN$ unknowns. Lines L2 to L4 give $sdN$ collocation equations, $(N - 1)d$ continuity equations and $d$ side conditions, so the counts match.

**Collocation is an implicit Runge-Kutta method.** For one step from $(t_0, y_0)$, write $k_j = u'(t_0 + c_jh)$. Since $u'$ has degree $s - 1$, it equals its interpolant: $u'(t_0 + \tau h) = \sum_jk_j\ell_j(\tau)$. Integrating from 0,
$$u(t_0 + c_ih) = y_0 + h\sum_ja_{ij}k_j, \qquad u(t_0 + h) = y_0 + h\sum_jb_jk_j, \qquad a_{ij} = \int_0^{c_i}\ell_j(\tau)\,d\tau,\quad b_j = \int_0^1\ell_j(\tau)\,d\tau.$$
Condition L2 says $k_i = f(t_0 + c_ih, u(t_0 + c_ih))$. These are exactly the stage equations of the Runge-Kutta method with [tableau](/butcher-tableau/) $(A, b, c)$. Conversely, the stages of that method define $u$ by the same formula. So the two are the same method, and $u$ is a built-in [dense output](/dense-output/).

**Order (HNW I, Section II.7).** Let the quadrature rule $\int_0^1\varphi \approx \sum_jb_j\varphi(c_j)$ have order $p$, that is, be exact for polynomials of degree below $p$. Then $p \le 2s$, and:

1. The collocation method satisfies Butcher's simplifying condition $C(s)$: $\sum_ja_{ij}c_j^{k-1} = c_i^k/k$ for $k \le s$, because interpolation reproduces $\tau^{k-1}$ exactly. This is the stage order $s$.
2. It satisfies $B(p)$ by the choice of $b$. With $C(s)$, distinct $c_j$ and all $b_j \ne 0$, $B(p)$ implies $D(p - s)$.
3. Butcher's theorem on simplifying assumptions (see [order conditions](/butcher-order-conditions/)), with $\eta = s$ and $\zeta = p - s$, then gives order $p$ at the mesh points. Interpolatory quadrature always has $p \ge s$. Hairer, Nørsett and Wanner prove the order $p$ without the condition $b_j \ne 0$, by a different argument.
4. Between mesh points, $u(t) - y(t) = O(h^{s+1})$ and $u^{(k)}(t) - y^{(k)}(t) = O(h^{s+1-k})$ on a step, for smooth $f$.

So the mesh values are superconvergent: order up to $2s$, while the polynomial itself has order $s + 1$.

**Cost.** Each step of an IVP solves a nonlinear system of size $sd$. A Newton iteration with the Jacobian $J$ of $f$ costs one Jacobian, $s$ evaluations of $f$ per iteration, and one LU factorization of the $sd \times sd$ matrix $I - hA \otimes J$. That is $\Theta(s^3d^3)$ done directly, and less with the eigenvalue tricks used by Radau5. For a BVP, the global system is almost block diagonal, with $N$ blocks, and it can be solved in $\Theta(N(sd)^3)$ operations.

## Classic examples

The tableaux below were computed from the points $c$ with exact `Fraction` arithmetic.

- **One point.** $c = (1)$ gives [backward Euler](/backward-euler-method/), order 1. $c = (\tfrac12)$ gives the implicit midpoint rule, order 2, which is the one-stage Gauss method.
- **Trapezoidal rule.** $c = (0, 1)$ gives $A = \begin{pmatrix}0 & 0\\ \tfrac12 & \tfrac12\end{pmatrix}$ and $b = (\tfrac12, \tfrac12)$. This is the trapezoidal rule, the two-stage Lobatto IIIA method, of order 2.
- **Gauss methods.** The $s$ Gauss-Legendre points give quadrature order $2s$, the maximum. These are the [Gauss methods](/gauss-legendre-runge-kutta/), A-stable and symmetric, with $R(z)$ the $(s, s)$ Padé approximation of $e^z$. For $s = 2$, $c = \tfrac12 \mp \tfrac{\sqrt3}6$, and $R(-1) = 7/19 = 0.368421$, which the computed tableau reproduces.
- **Radau IIA.** The Radau points with $c_s = 1$ give order $2s - 1$. For $s = 2$, $c = (\tfrac13, 1)$ gives $A = \begin{pmatrix}\tfrac5{12} & -\tfrac1{12}\\ \tfrac34 & \tfrac14\end{pmatrix}$ and $b = (\tfrac34, \tfrac14)$, of order 3. These are the [Radau IIA methods](/radau-iia-methods/). They are L-stable, and the code Radau5 uses $s = 3$.
- **Lobatto IIIA.** The Lobatto points with $c_1 = 0$ and $c_s = 1$ give order $2s - 2$. For $s = 3$, $c = (0, \tfrac12, 1)$ gives Simpson's weights $b = (\tfrac16, \tfrac23, \tfrac16)$ and order 4. MATLAB's bvp4c solves boundary value problems with this formula, as a collocation method with a continuous $C^1$ solution.
- **Piecewise Gauss collocation for BVPs.** COLSYS and COLNEW use collocation at Gauss points with adaptive meshes. For a first order system and $s$ points, de Boor and Swartz showed an error of $O(h^{2s})$ at the mesh points and $O(h^{s+1})$ uniformly.
- **Orthogonal collocation.** In chemical engineering, collocation at the zeros of orthogonal polynomials (Gauss or Radau points) is used for reactor and diffusion models. That is where the name comes from.

**Superconvergence, observed.** For the two-stage Gauss method on $y' = -y$, $y(0) = 1$ over $[0, 1]$ with $N$ steps:

| $N$ | max error at mesh points | ratio, $\log_2$ | max error of $u$ at $t_n + h/4$ | ratio, $\log_2$ |
|---|---|---|---|---|
| 5 | $8.1946 \cdot 10^{-7}$ | | $5.4563 \cdot 10^{-5}$ | |
| 10 | $5.1125 \cdot 10^{-8}$ | 4.00 | $7.2965 \cdot 10^{-6}$ | 2.90 |
| 20 | $3.1939 \cdot 10^{-9}$ | 4.00 | $9.4366 \cdot 10^{-7}$ | 2.95 |
| 40 | $1.9959 \cdot 10^{-10}$ | 4.00 | $1.1999 \cdot 10^{-7}$ | 2.98 |

The mesh values have order $2s = 4$, and the polynomial between them has order $s + 1 = 3$. At the midpoint $t_n + h/2$ the observed order was 4 in the same run, an extra effect of the symmetric points that the theorem above does not claim.

## Variations

- **Spectral collocation.** One global polynomial of high degree at Chebyshev or Legendre-Gauss-Lobatto points. It converges faster than any power of $1/s$ for analytic solutions. See [spectral methods](/spectral-methods/) and [Chebyshev nodes](/chebyshev-nodes/).
- **Higher order equations.** For $y^{(m)} = f(t, y, \dots, y^{(m-1)})$, collocate directly with piecewise polynomials of degree $s + m - 1$ that are $C^{m-1}$ at the mesh points, instead of rewriting the equation as a first order system. This is the setting of de Boor and Swartz and of COLSYS.
- **Perturbed and discontinuous collocation.** Relaxing the conditions describes larger families of implicit Runge-Kutta methods, including Lobatto IIIB and IIIC.
- **Multistep collocation.** The polynomial also interpolates past values. This gives linear multistep and general linear methods.
- **Differential-algebraic, delay and integral equations.** Radau IIA collocation is the standard method for index 1 to 3 DAEs. Collocation in piecewise polynomial spaces is also the main method for Volterra integral equations.
- **Relation to Galerkin methods.** Collocation is a [Galerkin](/galerkin-method/)-type method in which the test functions are point evaluations. Some Galerkin methods in time, with suitable quadrature, give the same discrete equations.

## Pitfalls

- **Dense values are less accurate than mesh values.** The polynomial between mesh points has only order $s + 1$, as the table shows. Do not report $2s$ for interpolated output.
- **Stiff order reduction.** For stiff problems the observed order often drops towards the stage order $s$ or $s + 1$ (HW II, Section IV.15). The Gauss methods are hit harder than Radau IIA.
- **Damping at infinity.** Gauss methods have $|R(\infty)| = 1$ and Lobatto IIIA has $R(-\infty) = -1$ for $s = 2$, so stiff components are not damped and can oscillate. Use Radau IIA when strong damping is needed.
- **Poor points.** Equally spaced points of high degree lead to the [Runge phenomenon](/runge-phenomenon/) and to negative quadrature weights. For $c = (\tfrac14, \tfrac12, \tfrac34)$ the weights are $(\tfrac23, -\tfrac13, \tfrac23)$, and the order is only 4 for three stages, against 6 for Gauss.
- **Nonlinear solves.** The system has size $sd$ per step, or $(s + 1)dN$ for a BVP. Newton's method needs a good starting guess. For BVPs, continuation in a parameter is often needed.
- **Points must be distinct**, or the interpolation in the template is not defined.

## Exercises

1. Show that one point $c_1 = \theta$ gives $y_1 = y_0 + hf(t_0 + \theta h, Y)$ with $Y = y_0 + \theta hf(t_0 + \theta h, Y)$, and that the order is 2 for $\theta = \tfrac12$ and 1 otherwise.
2. Compute the tableau for $c = (\tfrac13, 1)$ and check that it is Radau IIA of order 3, using the order conditions up to order 3.
3. Prove that every collocation method satisfies $C(s)$.
4. Show that the stability function of the collocation method with $c = (0, 1)$ is $R(z) = (1 + z/2)/(1 - z/2)$.
5. Find the order of the collocation method with $c = (\tfrac14, \tfrac12, \tfrac34)$. (Answer: 4, because the symmetric rule is exact for cubics but not for $\tau^4$.)
6. For $u'' = 0$ on $[0, 1]$ with $u(0) = 0$ and $u(1) = 1$, show that piecewise collocation of any order reproduces $u = t$ exactly. Then explain why this check finds sign errors in the continuity equations of a BVP code.

## References
