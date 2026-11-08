---
tag: DVHW5Q
kind: problem
slug: bvp-boundary-value-problem
name: Boundary value problem
aliases:
- two-point boundary value problem
- BVP
area: numerical/differential-equations
level: intro
summary: Find a solution of an ODE on an interval that satisfies conditions at both ends (or at several points), instead of conditions at one starting point.
model: real-ram
prereqs: [ode-initial-value-problem]
see_also: [boundary-conditions, shooting-method, finite-difference-method, collocation-method, sturm-liouville-problem, poisson-equation, newton-method-for-systems, thomas-algorithm]
sources:
  - book: isbn:9780898713541
    title: Uri M. Ascher, Robert M. M. Mattheij and Robert D. Russell, Numerical Solution of Boundary Value Problems for Ordinary Differential Equations, SIAM Classics in Applied Mathematics 13, 1995
    locator: Chapter 1 (examples), Chapter 3 (existence, uniqueness and conditioning), Chapter 4 (shooting and multiple shooting), Chapter 5 (finite difference and collocation methods)
  - book: "Herbert B. Keller, Numerical Methods for Two-Point Boundary-Value Problems, Blaisdell, 1968"
    locator: Chapter 1 (existence and uniqueness for u'' = f(x, u, u')), Chapter 2 (shooting), Chapter 3 (finite difference methods)
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 2 (steady states and boundary value problems, centered differences, stability and convergence, nonlinear problems with Newton's method)
  - book: isbn:9780898714128
    title: Uri M. Ascher and Linda R. Petzold, Computer Methods for Ordinary Differential Equations and Differential-Algebraic Equations, SIAM, 1998
    locator: Chapter 6 (boundary value problem theory), Chapter 7 (shooting), Chapter 8 (finite difference methods for boundary value problems)
---

A boundary value problem (BVP) asks for a solution of an ordinary differential equation on an interval $[a, b]$ that satisfies [boundary conditions](/boundary-conditions/) at both ends, or at several points. Unlike the [initial value problem](/ode-initial-value-problem/), the data do not fix a starting state, so a solution cannot be built by marching from one end, and existence and uniqueness are no longer automatic. The standard methods are [shooting](/shooting-method/), which reduces the problem to root finding over initial value problems, and global methods ([finite differences](/finite-difference-method/), [collocation](/collocation-method/), finite elements), which turn it into one large sparse system of equations.

## In plain words

In an initial value problem you know where you start and how you move, and you only need to follow the motion. In a boundary value problem you know part of the state at the start and part of it at the end. Think of a cannon that must hit a target: you know where the ball starts and where it must land, but not the angle. You can guess the angle, fire, see where the ball lands, and correct the guess. Or you can describe the whole flight path at once as many unknown points and require that each piece of the path obeys the equation and that the two ends are right. Some problems of this kind have no solution, some have exactly one, and some have several.

## Definition

**General two-point BVP.** Given $f : [a, b] \times \mathbb{R}^d \to \mathbb{R}^d$ and $g : \mathbb{R}^d \times \mathbb{R}^d \to \mathbb{R}^d$, find $y \in C^1([a, b]; \mathbb{R}^d)$ with
$$y'(x) = f(x, y(x)) \quad (a \le x \le b), \qquad g(y(a), y(b)) = 0.$$
The $d$ conditions in $g$ replace the $d$ initial values of an initial value problem.

**Linear BVP.** $y' = A(x) y + q(x)$ with $B_a y(a) + B_b y(b) = \beta$, where $A$ and $q$ are continuous and $B_a, B_b$ are $d \times d$ matrices. The conditions are *separated* when each row of $[B_a \; B_b]$ involves only $y(a)$ or only $y(b)$.

**Second-order scalar form.** $u'' = f(x, u, u')$ on $(a, b)$ with two conditions such as $u(a) = \alpha$, $u(b) = \beta$. With $y = (u, u')$ it is the case $d = 2$ of the general form.

The output is the function $y$, or in practice its values on a mesh $a = x_0 < x_1 < \dots < x_N = b$, or a piecewise polynomial that approximates it to a requested tolerance.

**Theorem (linear BVPs).** Let $Y(x)$ be the fundamental matrix of $Y' = A(x) Y$, $Y(a) = I$. The linear BVP has exactly one solution for each $q$ and $\beta$ if and only if $Q = B_a + B_b Y(b)$ is nonsingular.

*Proof.* Each solution of the differential equation has the form $y(x) = Y(x) s + v(x)$, where $s = y(a)$ and $v$ solves $v' = Av + q$, $v(a) = 0$. Both $Y$ and $v$ exist on all of $[a, b]$ because the equation is linear with continuous coefficients. The boundary condition becomes $B_a s + B_b (Y(b) s + v(b)) = \beta$, that is $Q s = \beta - B_b v(b)$. If $Q$ is nonsingular this linear system has exactly one $s$, so the BVP has exactly one solution. If $Q$ is singular, take $q = 0$: then $v = 0$, and for $\beta = 0$ each nonzero $s$ in the null space of $Q$ gives a second solution besides $y = 0$. $\square$

**Theorem (Keller, 1968, Chapter 1).** Let $f(x, u, p)$ be continuous on $[a, b] \times \mathbb{R}^2$ with continuous partial derivatives that satisfy $\partial f/\partial u > 0$ and $|\partial f/\partial p| \le M$. Then $u'' = f(x, u, u')$ with the separated conditions $a_0 u(a) - a_1 u'(a) = \alpha$, $b_0 u(b) + b_1 u'(b) = \beta$, where $a_0 a_1 \ge 0$, $b_0 b_1 \ge 0$, $|a_0| + |a_1| > 0$, $|b_0| + |b_1| > 0$ and $|a_0| + |b_0| > 0$, has exactly one solution. This page states the theorem without proof.

## Variants

- **Multipoint problems.** Conditions at interior points as well as at the ends.
- **Eigenvalue problems.** Find $\lambda$ and $u \ne 0$ with $-(pu')' + qu = \lambda w u$ and homogeneous conditions; this is the [Sturm-Liouville problem](/sturm-liouville-problem/).
- **Problems with unknown parameters or an unknown endpoint.** A free boundary $b$ or a parameter is added as an unknown with $p' = 0$, and one more boundary condition is added for each unknown.
- **Singular problems and infinite intervals.** The coefficients blow up at an end, or $b = \infty$ (the Blasius boundary layer equation). They are reduced to a finite interval with asymptotic boundary conditions.
- **Singularly perturbed problems.** $\varepsilon u'' + u' = f$ with small $\varepsilon > 0$ has a boundary layer of width $O(\varepsilon)$, which needs a nonuniform mesh.
- **Elliptic PDE problems.** The [Poisson equation](/poisson-equation/) on a domain with conditions on its boundary is the multidimensional analogue.

## Examples

**One solution, none, or infinitely many.** For $u'' = -u$: with $u(0) = 0$, $u(\pi/2) = 1$, the only solution is $u = \sin x$. With $u(0) = 0$, $u(\pi) = 1$ there is none, since every solution with $u(0) = 0$ is $c\sin x$ and vanishes at $\pi$. With $u(0) = 0$, $u(\pi) = 0$, every $c \sin x$ is a solution. In the linear theorem, $Y(\pi)$ maps $(u, u')(0)$ to $(u, u')(\pi)$, and $Q$ is singular exactly in the second and third cases.

**Two solutions of a nonlinear problem (Bratu).** $u'' + \lambda e^u = 0$ on $(0, 1)$, $u(0) = u(1) = 0$, has the solutions
$$u(x) = -2 \ln\frac{\cosh((x - 1/2)\theta/2)}{\cosh(\theta/4)}, \qquad \theta = \sqrt{2\lambda}\, \cosh(\theta/4).$$
For $\lambda = 1$ the equation for $\theta$ has the two roots $\theta = 1.51716$ and $\theta = 10.93870$, with maximum values $u(1/2) = 0.14054$ and $4.09147$. Two solutions exist for $0 < \lambda < \lambda^* = 3.513831$, one for $\lambda = \lambda^*$, and none for $\lambda > \lambda^*$. Here $\partial f/\partial u = -\lambda e^u < 0$, so Keller's theorem does not apply, which is consistent with the lack of uniqueness.

**Finite differences on Bratu.** With $h = 1/N$ and the centered formula $(u_{i-1} - 2u_i + u_{i+1})/h^2 + \lambda e^{u_i} = 0$ at the interior points, Newton's method started at $u = 0$ solves the tridiagonal nonlinear system. For $\lambda = 1$ it finds the lower solution, and the [Thomas algorithm](/thomas-algorithm/) does each linear solve in $O(N)$ operations. The value at $x = 1/2$ is $0.140763$ for $N = 8$, $0.140595$ for $N = 16$ and $0.140553$ for $N = 32$; the errors $2.23 \cdot 10^{-4}$, $5.57 \cdot 10^{-5}$ and $1.39 \cdot 10^{-5}$ fall by a factor of 4 per halving of $h$. To find the upper solution, Newton's method needs a start near it, or continuation in $\lambda$ around the turning point.

**Sensitivity of shooting.** For $u'' = 100u$, $u(0) = 1$, $u(1) = e^{-10}$, the solution is $e^{-10x}$. Shooting with $u'(0) = s$ gives $u(1) = \cosh 10 + s \sinh(10)/10$, so an error $\varepsilon$ in $s$ becomes an error of $1101.3\,\varepsilon$ at $x = 1$. With $u'' = 400u$ the factor is $\sinh(20)/20 = 1.21 \cdot 10^7$. The BVP itself is well conditioned in both cases; only the method is sensitive.

## Known algorithms

- **[Shooting method](/shooting-method/).** Guess the missing initial values $s$, solve the initial value problem, and solve $g(s, y(b; s)) = 0$ for $s$ with [Newton's method](/newton-method-for-systems/). Simple and reuses adaptive IVP codes, but the error can grow like $e^{L(b-a)}$.
- **Multiple shooting.** Shoot on $M$ subintervals and add continuity conditions at the joints. The growth per subinterval falls to about $e^{L(b-a)/M}$, at the price of a larger, block-structured system.
- **[Finite difference methods](/finite-difference-method/).** Replace derivatives by differences on a mesh and solve the resulting banded or almost block diagonal system, with Newton's method for nonlinear problems. The centered scheme has order 2; deferred corrections or Richardson extrapolation raise it.
- **[Collocation methods](/collocation-method/).** Seek a piecewise polynomial that satisfies the equation at Gauss or Lobatto points in each mesh interval. COLSYS and COLNEW use Gauss collocation, and MATLAB's bvp4c uses three-stage Lobatto IIIA collocation, with adaptive mesh selection.
- **[Finite element](/finite-element-method/) and [Galerkin](/galerkin-method/) methods.** Use the weak form, which is natural for self-adjoint problems.
- **[Spectral methods](/spectral-methods/).** Chebyshev collocation on the whole interval, with exponential convergence for analytic solutions.

## Bounds

For a linear second-order problem discretized with $N$ points and a three-point formula, the system is tridiagonal and costs $\Theta(N)$ operations; for a first-order system of dimension $d$ the one-step schemes give an almost block diagonal matrix that costs $O(N d^3)$ per solve. A nonlinear problem multiplies this by the number of Newton iterations. Every method reads the data at each mesh point, so $\Omega(N)$ is a trivial lower bound.

The accuracy depends on the smoothness of $y$. For the centered scheme on $-u'' + c(x) u = f$ with $c \ge 0$, Dirichlet conditions and $u \in C^4$, the max-norm error is $O(h^2)$ (LeVeque, Chapter 2). For a first-order system, collocation at $k$ Gauss points per interval has error $O(h^{2k})$ at the mesh points and $O(h^{k+1})$ between them, for smooth enough solutions (Ascher, Mattheij and Russell, Chapter 5).

The conditioning of the problem is measured by a stability constant $\kappa$, the norm of the solution operator from the data $(q, \beta)$ to $y$ (Ascher, Mattheij and Russell, Chapter 3). A well-conditioned BVP can have exponentially growing and decaying modes at the same time, as in the shooting example above; global methods and multiple shooting keep the error near $\kappa$ times the local error, while simple shooting can lose a factor of $e^{L(b-a)}$.

## Reductions

- **BVP to root finding.** Shooting defines $F(s) = g(s, y(b; s))$, where $y(\cdot\,; s)$ solves the IVP with $y(a) = s$. The BVP solutions correspond one to one to the roots of $F$.
- **BVP to an algebraic system.** Any discretization on a mesh turns it into a system of $(N+1)d$ equations in $(N+1)d$ unknowns.
- **Eigenvalue problems and parameters to standard form.** Add $\lambda' = 0$ and a normalization condition such as $u'(a) = 1$. An unknown endpoint $b$ becomes a parameter by the change of variable $x = a + (b - a)\xi$, $\xi \in [0, 1]$.
- **Higher order to first order.** An equation of order $m$ becomes a system of dimension $m$ with the derivatives as new unknowns.

## Applications

- Deflection of beams ($u'''' = f$ with conditions on $u$ and $u''$ or $u'$ at each end) and steady heat conduction in a rod.
- Boundary layers in fluid mechanics, such as the Blasius equation $f''' + \tfrac{1}{2} f f'' = 0$ on $[0, \infty)$.
- Combustion and chemical reactors: the Bratu (Gelfand) problem above models thermal ignition.
- Optimal control: Pontryagin's maximum principle gives a BVP for the state and the costate, with conditions at the start and at the end time.
- Periodic orbits of autonomous systems, with the unknown period as a parameter and $y(0) = y(T)$.

## References
