---
tag: HJ49HP
kind: definition
slug: boundary-conditions
name: Dirichlet and Neumann boundary conditions
aliases:
- Dirichlet condition
- Neumann condition
- Robin condition
- boundary conditions
area: numerical/differential-equations
level: intro
summary: Conditions on the boundary of the domain of a differential equation. Dirichlet fixes the value of u, Neumann fixes the normal derivative, Robin fixes a combination of the two.
prereqs: [bvp-boundary-value-problem]
see_also: [poisson-equation, heat-equation, sturm-liouville-problem, finite-difference-method, finite-element-method, shooting-method, advection-equation, pde-classification]
sources:
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 2, Section 2.2 (boundary conditions), Section 2.12 (Neumann boundary conditions, the ghost point and the one-sided formula) and Section 2.13 (existence and uniqueness, the solvability condition)
  - book: isbn:9780521734905
    title: Arieh Iserles, A First Course in the Numerical Analysis of Differential Equations, second edition, Cambridge University Press, 2009
    locator: Chapter 8 (finite difference schemes for the Poisson equation with Dirichlet conditions) and Chapter 16 (the diffusion equation with boundary conditions)
  - book: isbn:9780898713541
    title: Uri M. Ascher, Robert M. M. Mattheij and Robert D. Russell, Numerical Solution of Boundary Value Problems for Ordinary Differential Equations, SIAM Classics in Applied Mathematics 13, 1995
    locator: Chapter 1 (boundary value problems and the form of their boundary conditions) and Chapter 3 (existence and uniqueness theory)
---

A boundary condition is an equation that the solution $u$ of a differential equation must satisfy on the boundary of its domain. A Dirichlet condition fixes the value of $u$, a Neumann condition fixes the derivative of $u$ in the direction of the outward normal, and a Robin condition fixes a linear combination of the two. Together with the differential equation they form a [boundary value problem](/bvp-boundary-value-problem/), and the choice of condition decides whether the problem has a solution, whether it is unique, and how a [finite difference](/finite-difference-method/) or [finite element](/finite-element-method/) scheme must treat the boundary.

## Definition

Let $\Omega \subset \mathbb{R}^m$ be a bounded open set with a piecewise smooth boundary $\partial\Omega$ and outward unit normal $\mathbf{n}$. Let $u$ be defined on the closure of $\Omega$, and write $\partial u/\partial n = \mathbf{n} \cdot \nabla u$ for the outward normal derivative. Let $\Gamma \subseteq \partial\Omega$ and let $g$ be a given function on $\Gamma$.

- A **Dirichlet condition** on $\Gamma$ is $u = g$ on $\Gamma$.
- A **Neumann condition** on $\Gamma$ is $\partial u / \partial n = g$ on $\Gamma$.
- A **Robin condition** on $\Gamma$ is $\alpha u + \beta\, \partial u/\partial n = g$ on $\Gamma$, with given functions $\alpha, \beta$ that are not both zero at any point.
- A condition is **homogeneous** if $g = 0$.
- The conditions are **mixed** when different parts of $\partial\Omega$ carry conditions of different types.

In one dimension, $\Omega = (a, b)$ and $\partial\Omega = \{a, b\}$. The outward normal is $-1$ at $a$ and $+1$ at $b$, so the Neumann condition at $a$ reads $-u'(a) = g(a)$; most books write it as $u'(a) = \sigma_a$ instead, and this page does the same. A **periodic condition** $u(a) = u(b)$, $u'(a) = u'(b)$ couples the two ends and is none of the three types above.

For a time-dependent problem in $u(x, t)$ on $\Omega \times (0, T]$, the conditions hold on $\partial\Omega$ for each $t > 0$, and an initial condition $u(x, 0) = u_0(x)$ is added. For a hyperbolic equation such as the [advection equation](/advection-equation/) $u_t + c\, u_x = 0$ on $(a, b)$, a condition may be given only where the characteristics enter the domain: at $x = a$ when $c > 0$, and at $x = b$ when $c < 0$.

**Two facts for the one-dimensional model problem** $-u'' = f$ on $(0, 1)$, with $f$ continuous.

1. *Pure Neumann conditions need a compatibility condition and leave a free constant.* With $u'(0) = \sigma_0$ and $u'(1) = \sigma_1$, a $C^2$ solution exists if and only if $\int_0^1 f\,dx = \sigma_0 - \sigma_1$, and any two solutions differ by a constant. Proof: integrating $-u'' = f$ gives $u'(0) - u'(1) = \int_0^1 f\,dx$, so the condition is necessary. If it holds, $u(x) = c + \sigma_0 x - \int_0^x (x - s) f(s)\,ds$ has $u'' = -f$, $u'(0) = \sigma_0$ and $u'(1) = \sigma_0 - \int_0^1 f\,ds = \sigma_1$, for each constant $c$. The difference $w$ of two solutions has $w'' = 0$ and $w'(0) = 0$, so $w$ is constant.
2. *A Dirichlet condition at one end, or a Robin condition with the right sign, gives uniqueness.* Take the homogeneous conditions $-u'(0) + \kappa_0 u(0) = 0$ and $u'(1) + \kappa_1 u(1) = 0$ with $\kappa_0, \kappa_1 \ge 0$ not both zero; these are $\partial u/\partial n + \kappa u = 0$ in outward-normal form. If $-u'' = 0$, multiply by $u$ and integrate by parts: $0 = \int_0^1 (u')^2\,dx - u'(1)u(1) + u'(0)u(0) = \int_0^1 (u')^2\,dx + \kappa_1 u(1)^2 + \kappa_0 u(0)^2$. Each term is at least 0, so $u' = 0$ and $u$ is a constant $c$ with $(\kappa_0 + \kappa_1)c^2 = 0$, so $u = 0$. A Dirichlet condition $u(0) = 0$ gives the same conclusion directly from $u' = 0$. With $\kappa$ of the wrong sign uniqueness can fail.

In $m$ dimensions the same argument with Green's identity shows that $-\Delta u = f$ in $\Omega$, $\partial u/\partial n = g$ on $\partial\Omega$ can have a solution only if $\int_\Omega f\,dx + \int_{\partial\Omega} g\,ds = 0$ (LeVeque, Section 2.13, treats the one-dimensional case).

## Examples and non-examples

**Examples.** For $u'' = 1$ on $(0, 1)$:

- Dirichlet at both ends, $u(0) = u(1) = 0$: the unique solution is $u(x) = x(x - 1)/2$.
- Dirichlet at $0$ and Neumann at $1$, $u(0) = 0$, $u'(1) = 0$: the unique solution is $u(x) = x^2/2 - x$.
- Robin at $1$, $u(0) = 0$, $u'(1) + u(1) = 0$: from $u = x^2/2 + cx$ the condition gives $1 + c + 1/2 + c = 0$, so $c = -3/4$ and $u(x) = x^2/2 - 3x/4$.

**Non-example (no solution).** $u'' = 1$ with $u'(0) = u'(1) = 0$. Here $f = -1$ in the form $-u'' = f$, so $\int_0^1 f\,dx = -1 \ne 0 = \sigma_0 - \sigma_1$ and fact 1 says that no solution exists. In physical terms: a rod with insulated ends and a steady heat source has no steady state.

**Non-example (not a boundary condition).** $u(0) = 0$, $u'(0) = 1$ gives two conditions at one point. That is an [initial value problem](/ode-initial-value-problem/), and the [shooting method](/shooting-method/) turns a boundary value problem into a sequence of such problems.

**Non-example (an ill-posed choice).** For $u_t + u_x = 0$ on $0 < x < 1$, information moves to the right. A Dirichlet condition at the outflow end $x = 1$, in addition to the one at $x = 0$, over-determines the problem: the value at $x = 1$ is already fixed by the data that arrive from the left.

**How a finite difference scheme treats the conditions.** Take $u'' = -\sin x$ on $(0, 1)$ with $u(0) = 0$ and $u'(1) = \cos 1$, so $u = \sin x$. Use the grid $x_i = ih$, $h = 1/N$, and the centered formula $(u_{i-1} - 2u_i + u_{i+1})/h^2 = f(x_i)$ at the interior points. The Dirichlet condition is used directly: $u_0 = 0$. The Neumann condition has two common forms.

- The one-sided formula $(u_N - u_{N-1})/h = \cos 1$ has local error $O(h)$, and it pulls the whole solution down to first order.
- A ghost point $u_{N+1}$ with $(u_{N+1} - u_{N-1})/(2h) = \cos 1$, used to remove $u_{N+1}$ from the centered equation at $x_N$, gives $(2u_{N-1} - 2u_N)/h^2 = f(x_N) - 2\cos(1)/h$ and keeps second order.

The maximum errors over the grid are:

| $N$ | one-sided | ghost point |
|---|---|---|
| 4 | 0.09797 | 0.007213 |
| 8 | 0.05079 | 0.001800 |
| 16 | 0.02585 | 0.0004499 |
| 32 | 0.01304 | 0.0001125 |

The first column halves when $h$ halves, the second falls by a factor of 4.

## Related definitions

- **Essential and natural conditions.** In the weak form used by the [finite element method](/finite-element-method/) and the [Galerkin method](/galerkin-method/), a Dirichlet condition must be built into the trial space (essential), while a Neumann or Robin condition enters through the boundary integral of the weak form (natural).
- **[Boundary value problem](/bvp-boundary-value-problem/).** A differential equation together with its boundary conditions. Separated conditions involve each end alone; non-separated ones, such as periodic conditions, couple the ends.
- **[Sturm-Liouville problem](/sturm-liouville-problem/).** An eigenvalue problem with homogeneous separated Robin conditions at both ends.
- **[Poisson equation](/poisson-equation/) and [heat equation](/heat-equation/).** The model elliptic and parabolic problems where these conditions are first met.
- **Inflow and outflow boundaries.** For hyperbolic problems the number of conditions at a boundary point equals the number of characteristics that enter the domain there; see [method of characteristics](/method-of-characteristics/) and [PDE classification](/pde-classification/).

## References
