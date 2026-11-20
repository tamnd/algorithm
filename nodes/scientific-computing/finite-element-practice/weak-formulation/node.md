---
tag: MNAD6Y
kind: definition
slug: weak-formulation
name: Weak formulation
aliases:
- variational formulation of a boundary value problem
area: scientific-computing/finite-element-practice
level: intro
summary: Restates a boundary value problem as finding u in a function space with a(u, v) = l(v) for all test functions v, which needs fewer derivatives.
prereqs: [poisson-equation, boundary-conditions]
see_also: [sobolev-space, lax-milgram-theorem, galerkin-method, finite-element-method, finite-element-assembly, euler-lagrange-equation, nitsche-method, weak-solution-of-conservation-law]
sources:
  - book: isbn:9780387759333
    title: Susanne C. Brenner and L. Ridgway Scott, The Mathematical Theory of Finite Element Methods, third edition, Springer, 2008
    locator: Chapter 0 (the one-dimensional variational formulation) and Chapter 2 (variational formulation of elliptic boundary value problems, natural and essential boundary conditions)
  - book: isbn:9780821849743
    title: Lawrence C. Evans, Partial Differential Equations, second edition, Graduate Studies in Mathematics 19, American Mathematical Society, 2010
    locator: Chapter 6, Section 6.1 (weak solutions of second-order elliptic equations)
  - book: isbn:9780898715149
    title: Philippe G. Ciarlet, The Finite Element Method for Elliptic Problems, SIAM Classics in Applied Mathematics 40, 2002
    locator: Chapter 1 (abstract variational problems and examples of elliptic boundary value problems)
---

A weak formulation of a boundary value problem asks for a function $u$ in a function space $V$ such that $a(u, v) = l(v)$ for every test function $v$ in $V$. You get it when you multiply the differential equation by $v$, integrate over the domain and move one derivative from $u$ to $v$ by integration by parts. The weak form needs only first derivatives of $u$ for a second-order equation, so it has solutions where the classical problem has none, for example at material interfaces. It is the start of the [Galerkin method](/galerkin-method/) and of the [finite element method](/finite-element-method/), which replace $V$ by a finite-dimensional subspace.

## Definition

**Model problem.** Let $\Omega \subset \mathbb{R}^d$ be a bounded domain with Lipschitz boundary $\partial\Omega = \overline{\Gamma_D} \cup \overline{\Gamma_N}$, and let $n$ be the unit outward normal. The strong form is

$$-\nabla \cdot (\kappa \nabla u) = f \ \text{in } \Omega, \qquad u = g_D \ \text{on } \Gamma_D, \qquad \kappa \frac{\partial u}{\partial n} = g_N \ \text{on } \Gamma_N,$$

with a coefficient $\kappa(x)$ that satisfies $0 < \kappa_0 \le \kappa(x) \le \kappa_1$.

**Derivation.** Multiply the equation by a test function $v$ with $v = 0$ on $\Gamma_D$ and integrate over $\Omega$. Green's formula $\int_\Omega -\nabla\cdot(\kappa\nabla u)\, v = \int_\Omega \kappa \nabla u \cdot \nabla v - \int_{\partial\Omega} \kappa \frac{\partial u}{\partial n} v$ moves one derivative to $v$. The boundary integral is zero on $\Gamma_D$ because $v = 0$ there, and it is $\int_{\Gamma_N} g_N v$ on $\Gamma_N$. The result is

$$a(u, v) = \int_\Omega \kappa \nabla u \cdot \nabla v \, dx, \qquad l(v) = \int_\Omega f v \, dx + \int_{\Gamma_N} g_N v \, ds.$$

**Weak formulation.** Let $V = \{v \in H^1(\Omega) : v = 0 \text{ on } \Gamma_D\}$, a closed subspace of the [Sobolev space](/sobolev-space/) $H^1(\Omega)$, and let $u_D \in H^1(\Omega)$ be any function with $u_D = g_D$ on $\Gamma_D$. The weak problem is: find $u \in u_D + V$ such that

$$a(u, v) = l(v) \quad \text{for all } v \in V.$$

A function $u$ with this property is a *weak solution*. In the abstract form, $V$ is a Hilbert space, $a : V \times V \to \mathbb{R}$ is a bounded bilinear form and $l : V \to \mathbb{R}$ is a bounded linear functional. The [Lax-Milgram theorem](/lax-milgram-theorem/) gives existence and uniqueness when $a$ is also coercive. For the model problem with $|\Gamma_D| > 0$ this holds with $M = \kappa_1$ and $\alpha = \kappa_0 / (1 + C_P^2)$, where $C_P$ is the Poincaré constant.

**Two kinds of boundary conditions.** A condition that you build into the space, such as $u = g_D$, is *essential*. A condition that comes out of the integration by parts, such as $\kappa\,\partial u/\partial n = g_N$, is *natural*: it appears only in $l$, and the weak solution satisfies it automatically.

**Strong and weak solutions.** Every classical solution $u \in C^2(\overline\Omega)$ is a weak solution: the derivation above is a proof. If a weak solution is in $H^2(\Omega)$, then integration by parts in the other direction gives $\int_\Omega (-\nabla\cdot(\kappa\nabla u) - f)v = 0$ for all smooth $v$ with compact support, so the equation holds almost everywhere, and the Neumann condition follows next.

**Energy form.** If $a$ is symmetric and $a(v, v) \ge 0$, then $u$ solves the weak problem if and only if it minimizes the energy $J(v) = \tfrac12 a(v, v) - l(v)$ over the same set. The reason is the identity $J(u + w) = J(u) + \bigl(a(u, w) - l(w)\bigr) + \tfrac12 a(w, w)$ for every $w \in V$. The strong equation is the [Euler-Lagrange equation](/euler-lagrange-equation/) of $J$.

## Examples and non-examples

**A smooth check.** Take $-u'' = 1$ on $(0, 1)$ with $u(0) = u(1) = 0$. The weak form is $\int_0^1 u'v'\,dx = \int_0^1 v\,dx$ for all $v \in H^1_0(0, 1)$, and the solution is $u = x(1-x)/2$. For the test function $v = x(1-x)$ the left side is $\int_0^1 (\tfrac12 - x)(1 - 2x)\,dx = \tfrac12\int_0^1 (1-2x)^2\,dx = \tfrac16$, and the right side is $\int_0^1 x(1-x)\,dx = \tfrac16$.

**A material interface.** Take $-(\kappa u')' = 0$ on $(0, 1)$ with $\kappa = 1$ on $(0, \tfrac12)$, $\kappa = 2$ on $(\tfrac12, 1)$, $u(0) = 0$ and $u(1) = 1$. No $C^2$ solution exists. The weak form makes the flux $\kappa u'$ a constant $c$, so $u' = c$ on the left half and $u' = c/2$ on the right half. Then $u(1) = c/2 + c/4 = 1$ gives $c = \tfrac43$, and $u = \tfrac43 x$ for $x \le \tfrac12$ and $u = \tfrac23 + \tfrac23(x - \tfrac12)$ for $x \ge \tfrac12$. The slope jumps from $\tfrac43$ to $\tfrac23$, but $\kappa u'$ stays continuous, which is the correct physics.

**A natural boundary condition.** Take $-u'' = 0$ on $(0, 1)$ with $u(0) = 0$ and $u'(1) = 1$. Here $V = \{v \in H^1(0,1) : v(0) = 0\}$ and $l(v) = v(1)$. The solution $u = x$ satisfies $\int_0^1 1 \cdot v'\,dx = v(1) - v(0) = v(1)$. The condition $u'(1) = 1$ is not in $V$. It is only in $l$.

**A point load in one dimension.** Take $-u'' = \delta_{1/2}$ with $u(0) = u(1) = 0$, so $l(v) = v(\tfrac12)$. The tent $u = x/2$ for $x \le \tfrac12$ and $u = (1 - x)/2$ for $x \ge \tfrac12$ is the weak solution: $\int_0^1 u'v' = \tfrac12 v(\tfrac12) + \tfrac12 v(\tfrac12) = v(\tfrac12)$. This $l$ is bounded on $H^1_0(0,1)$ because $|v(\tfrac12)| \le \tfrac12 |v|_1$ there.

**Non-example: a point load in two dimensions.** In $\Omega \subset \mathbb{R}^2$ the functional $l(v) = v(x_0)$ is not bounded on $H^1(\Omega)$, because $H^1$ functions in 2D need not be continuous. So $-\Delta u = \delta_{x_0}$ has no weak solution in $H^1$. Its solution behaves like $-\frac{1}{2\pi}\log|x - x_0|$, whose gradient is not square integrable near $x_0$.

**Non-example: a pure Neumann problem.** If $\Gamma_N = \partial\Omega$, the test function $v = 1$ gives $0 = \int_\Omega f + \int_{\partial\Omega} g_N$. Data that fails this condition has no weak solution, and when it holds the solution is unique only up to a constant. A unique solution comes from the space $V = \{v \in H^1(\Omega) : \int_\Omega v = 0\}$.

**Non-example: the wrong space.** The form $\int u'v' = \int fv$ posed on $C^1([0,1])$ functions with zero boundary values is not a weak formulation in the sense above. That space is not complete in the $H^1$ norm, so the Lax-Milgram argument fails, and for the interface example above it contains no solution.

## Related definitions

- **[Galerkin method](/galerkin-method/).** Pose the same weak form on a finite-dimensional subspace $V_h \subset V$. This gives a linear system $AU = b$ with $A_{ij} = a(\phi_j, \phi_i)$ and $b_i = l(\phi_i)$.
- **[Sobolev space](/sobolev-space/).** The spaces $H^1(\Omega)$ and $H^1_0(\Omega)$ where the weak form lives, with traces that give a meaning to boundary values.
- **Petrov-Galerkin formulation.** The trial space and the test space differ. Well-posedness then needs an [inf-sup condition](/inf-sup-condition/) in place of coercivity. [Streamline upwind Petrov-Galerkin](/streamline-upwind-petrov-galerkin/) is an example.
- **Mixed formulation.** The flux $\sigma = \kappa\nabla u$ is a second unknown, and the weak form becomes a saddle-point problem. See [mixed finite element method](/mixed-finite-element-method/).
- **Weakly imposed Dirichlet conditions.** [Nitsche's method](/nitsche-method/) puts $u = g_D$ into $a$ and $l$ instead of into $V$.
- **[Weak solution of a conservation law](/weak-solution-of-conservation-law/).** The same idea for first-order hyperbolic equations. There the test functions carry all the derivatives, and shocks are allowed.

## References
