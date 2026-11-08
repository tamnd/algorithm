---
tag: EFCPNY
kind: problem
slug: burgers-equation
name: Burgers' equation
aliases:
- Bateman-Burgers equation
- inviscid Burgers equation
- viscous Burgers equation
area: numerical/differential-equations
level: advanced
summary: The PDE u_t + (u^2/2)_x = ν u_xx. With ν = 0 smooth data break into shocks in finite time, so it is the standard model problem for nonlinear conservation laws.
model: real-ram
prereqs: [advection-equation, method-of-characteristics]
see_also: [riemann-problem, godunov-method, finite-volume-method, lax-friedrichs-scheme, flux-limiter-methods, weno-scheme, heat-equation, navier-stokes-equations]
sources:
  - book: isbn:9780521009249
    title: Randall J. LeVeque, Finite Volume Methods for Hyperbolic Problems, Cambridge University Press, 2002
    locator: Chapter 11 (nonlinear scalar conservation laws, Burgers' equation, shocks, rarefaction waves, the Rankine-Hugoniot and entropy conditions) and Chapter 12 (finite volume methods for nonlinear scalar conservation laws, Godunov's method, the entropy fix, the Lax-Wendroff theorem, nonconservative methods)
  - book: isbn:9780821849743
    title: Lawrence C. Evans, Partial Differential Equations, second edition, American Mathematical Society, 2010
    locator: Section 3.4 (conservation laws, integral solutions, the Lax-Oleinik formula, entropy solutions and their uniqueness) and Section 4.4 (the Hopf-Cole transformation)
  - paper: "J. M. Burgers, A mathematical model illustrating the theory of turbulence, Advances in Applied Mechanics 1 (1948) 171-199"
    locator: the equation as a model of turbulence
  - paper: "E. Hopf, The partial differential equation u_t + u u_x = μ u_xx, Communications on Pure and Applied Mathematics 3 (1950) 201-230"
    locator: the transformation to the heat equation, the explicit solution and the limit of vanishing viscosity
  - paper: "J. D. Cole, On a quasi-linear parabolic equation occurring in aerodynamics, Quarterly of Applied Mathematics 9 (1951) 225-236"
    locator: the same transformation, found independently
  - paper: "P. Lax and B. Wendroff, Systems of conservation laws, Communications on Pure and Applied Mathematics 13 (1960) 217-237"
    locator: the theorem that limits of conservative consistent schemes are weak solutions
  - paper: "A. Harten, J. M. Hyman and P. D. Lax, On finite-difference approximations and entropy conditions for shocks, Communications on Pure and Applied Mathematics 29 (1976) 297-322"
    locator: monotone schemes satisfy the entropy condition and are at most first order accurate
---

Burgers' equation $u_t + uu_x = \nu u_{xx}$ is the simplest PDE that combines nonlinear transport with diffusion. Without viscosity ($\nu = 0$), it is the scalar conservation law $u_t + (u^2/2)_x = 0$. Each value of $u$ moves at speed $u$, so faster parts catch up with slower parts, the profile steepens, and after a finite time it contains a jump, a shock. From then on the equation holds only in a weak sense. Weak solutions are not unique, and an extra entropy condition selects the physical one. These effects appear in gas dynamics, traffic flow and every other system of conservation laws. Burgers' equation shows them in their simplest form, and it has exact solutions to test against. So it is the standard test problem for shock-capturing schemes such as the [Godunov method](/godunov-method/).

## In plain words

Picture cars on a one-lane road where each car keeps its own speed. If faster cars are behind slower ones, the gaps close and the cars bunch up. In the equation, the bunching continues until the profile has a vertical front. At that moment the smooth description breaks down, and the front moves on as a jump whose speed is fixed by how much "stuff" must be conserved. If the faster cars are in front instead, the gaps open and the profile spreads out smoothly. A small amount of viscosity turns the jump into a steep but smooth front. A numerical method must move the jump at the right speed, keep it sharp, and never create jumps that spread instead of steepen.

## Definition

**Notation.** $u(x, t)$ is the unknown, $\Delta x$ and $\Delta t$ are the mesh widths, $U_j^n$ approximates the average of $u(\cdot, t_n)$ over the cell $[x_{j-1/2}, x_{j+1/2}]$, $t_n = n\Delta t$, and $\lambda = \Delta t/\Delta x$. The Courant number is $\lambda\max_j|U_j^n|$. The flux is $f(u) = u^2/2$. Errors are measured in the discrete $L^1$ norm $\Delta x\sum_j|U_j^N - u(x_j, T)|$, which is the natural norm for conservation laws.

**Inviscid Cauchy problem.** Given $u_0 \in L^\infty(\mathbb{R})$, find $u$ with
$$u_t + \big(\tfrac12u^2\big)_x = 0, \quad x \in \mathbb{R},\ t > 0, \qquad u(x, 0) = u_0(x).$$

- **Classical solutions.** If $u_0$ is $C^1$ and bounded with bounded derivative, then $u(x, t) = u_0(\xi)$ where $x = \xi + u_0(\xi)t$. This defines $u$ as long as $\xi \mapsto \xi + u_0(\xi)t$ is increasing, that is for $t < T_b = -1/\min u_0'$ if $\min u_0' < 0$, and for all $t$ otherwise. At $T_b$ the characteristics cross and $u_x$ becomes infinite. This is the [method of characteristics](/method-of-characteristics/).
- **Weak solutions.** $u \in L^\infty$ is a weak solution if $\int_0^\infty\int(u\varphi_t + \tfrac12u^2\varphi_x)\,dx\,dt + \int u_0\varphi(x, 0)\,dx = 0$ for every $C^1$ test function $\varphi$ with compact support in $\mathbb{R} \times [0, \infty)$.
- **Rankine-Hugoniot condition.** A piecewise smooth weak solution with a jump from $u_L$ to $u_R$ along $x = \xi(t)$ must have $\xi'(t) = s = \frac{f(u_L) - f(u_R)}{u_L - u_R} = \frac{u_L + u_R}2$.
- **Entropy condition.** A jump is admissible only if $u_L > u_R$ (Lax's condition for convex $f$). For piecewise smooth solutions this is equivalent to the entropy inequality $(\tfrac12u^2)_t + (\tfrac13u^3)_x \le 0$ in the sense of distributions, for the entropy $\eta = u^2/2$ with entropy flux $q = u^3/3$. In general, Kružkov's definition asks for the inequality for every convex entropy. Kružkov (1970) proved that the entropy solution exists and is unique for $u_0 \in L^\infty$. It is also the limit of the viscous solutions as $\nu \to 0$.

**Viscous problem.** For $\nu > 0$, $u_t + uu_x = \nu u_{xx}$ has a unique smooth solution for bounded $u_0$, given explicitly by the Hopf-Cole formula (see Reductions).

**Properties of the entropy solution.** The integral $\int u\,dx$ is conserved. The solution satisfies $\min u_0 \le u \le \max u_0$, its total variation does not increase, and two solutions satisfy the $L^1$ contraction $\|u(\cdot, t) - v(\cdot, t)\|_{L^1} \le \|u_0 - v_0\|_{L^1}$.

**The computational task.** Given $u_0$, $T$ and a mesh, compute $U_j^N$ with $t_N = T$ that approximates the entropy solution (or the viscous solution), and report the $L^1$ error.

## Variants

- **Viscous Burgers' equation**, $\nu > 0$. Shocks become smooth fronts whose width is proportional to $\nu/(u_L - u_R)$. When $\nu$ is much smaller than $\Delta x$, numerical schemes face the same problems as for $\nu = 0$.
- **Riemann problem.** $u_0 = u_L$ for $x < 0$ and $u_R$ for $x > 0$. See the [Riemann problem](/riemann-problem/). It is the building block of Godunov-type schemes.
- **Periodic problem** on $[0, L)$, often with $u_0 = \sin$, which forms a shock at a known time.
- **General scalar conservation laws** $u_t + f(u)_x = 0$ with convex $f$. They behave like Burgers' equation, with $s = [f]/[u]$ and the condition $f'(u_L) > s > f'(u_R)$.
- **Nonconservative form.** $u_t + uu_x = 0$ is the same equation for smooth solutions, and so is $(u^2)_t + (\tfrac23u^3)_x = 0$. For shocks they differ: the second conservation law gives the speed $\tfrac23(u_L^2 + u_Lu_R + u_R^2)/(u_L + u_R)$, which is $\tfrac23$ instead of $\tfrac12$ for $u_L = 1$, $u_R = 0$. The conserved quantity must be part of the problem statement.
- **Forced and stochastic Burgers' equation**, and the Burgers equation in several dimensions, $u_t + (u \cdot \nabla)u = \nu\Delta u$, a model for the [Navier-Stokes equations](/navier-stokes-equations/) without pressure.

## Examples

**Shock.** $u_L = 1$, $u_R = 0$. The entropy solution is the jump moving at $s = \tfrac12$: $u = 1$ for $x < t/2$ and $0$ otherwise.

**Rarefaction.** $u_L = 0$, $u_R = 1$. The jump violates the entropy condition. The entropy solution is the fan $u = 0$ for $x < 0$, $u = x/t$ for $0 \le x \le t$, and $u = 1$ for $x > t$. The jump moving at speed $\tfrac12$ is also a weak solution, but not an admissible one.

**Breaking of a sine wave.** For $u_0 = \sin x$ with period $2\pi$, $\min u_0' = -1$, so $T_b = 1$. The steepest point is $x = \pi$. The data are odd about $\pi$, so for $t > 1$ a shock with $u_L = -u_R$ stands still at $x = \pi$, and its strength decays as the two sides drain into it.

**Viscous travelling wave.** For $u_L > u_R$, $s = (u_L + u_R)/2$ and $\delta = u_L - u_R$,
$$u(x, t) = s - \frac\delta2\tanh\Big(\frac{\delta(x - st)}{4\nu}\Big)$$
solves the viscous equation. It tends to the entropy shock as $\nu \to 0$. A finite difference check at one point with $\nu = 0.05$ gives a residual of $6 \cdot 10^{-8}$. It also comes from the Hopf-Cole formula with $\varphi = 1 + e^{-(x - t/2)/(2\nu)}$ for $u_L = 1$, $u_R = 0$.

**Schemes on Riemann problems.** On $[-1, 1]$ with $\lambda = 0.5$, $T = 0.5$, and $M$ cells ($\Delta x = 2/M$), the $L^1$ errors are (computed):

| data | scheme | $M = 100$ | $200$ | $400$ | $800$ | last ratio, $\log_2$ |
|---|---|---|---|---|---|---|
| shock $(1, 0)$ | Godunov | $1.329 \cdot 10^{-2}$ | $4.727 \cdot 10^{-3}$ | $2.364 \cdot 10^{-3}$ | $1.182 \cdot 10^{-3}$ | 1.00 |
| shock $(1, 0)$ | Lax-Friedrichs | $4.929 \cdot 10^{-2}$ | $2.677 \cdot 10^{-2}$ | $1.280 \cdot 10^{-2}$ | $6.401 \cdot 10^{-3}$ | 1.00 |
| rarefaction $(0, 1)$ | Godunov | $2.372 \cdot 10^{-2}$ | $1.455 \cdot 10^{-2}$ | $8.702 \cdot 10^{-3}$ | $5.094 \cdot 10^{-3}$ | 0.77 |
| transonic $(-1, 1)$ | Godunov | $4.744 \cdot 10^{-2}$ | $2.910 \cdot 10^{-2}$ | $1.740 \cdot 10^{-2}$ | $1.019 \cdot 10^{-2}$ | 0.77 |
| transonic $(-1, 1)$ | Roe, no entropy fix | $0.5$ | $0.5$ | $0.5$ | $0.5$ | 0 |

Two failures are worth a closer look. First, the Roe flux without an entropy fix keeps the initial jump from $-1$ to $1$ as a stationary expansion shock, because both one-sided fluxes equal $\tfrac12$. The scheme is conservative and consistent, and it converges, but to a weak solution that violates the entropy condition. Second, the nonconservative upwind scheme $U_j^{n+1} = U_j^n - \lambda U_j^n(U_j^n - U_{j-1}^n)$ applied to the shock $(1, 0)$ never moves the jump. At the first cell with $U_j = 0$ the update is zero. With $M = 200$ the jump is still at $x = 0$ at $T = 1$, while the true shock is at $x = 0.5$.

## Known algorithms

- **[Godunov's method](/godunov-method/).** It uses the exact Riemann solution at each cell interface. For Burgers' equation the interface flux has the closed form $F(u_L, u_R) = \max\big(f(\max(u_L, 0)), f(\min(u_R, 0))\big)$. It is monotone, first order, and stable for Courant number at most 1.
- **[Lax-Friedrichs](/lax-friedrichs-scheme/)** and its local variant (Rusanov). They are simpler and monotone, but more diffusive, as the table shows.
- **Roe's linearized solver with an entropy fix** (Harten), and the Engquist-Osher flux, which is monotone and needs no fix.
- **High-resolution schemes.** MUSCL reconstruction with [flux limiters](/flux-limiter-methods/), [TVD](/total-variation-diminishing/) schemes, and [WENO](/weno-scheme/) schemes give second or higher order in smooth regions and sharp shocks without large oscillations.
- **[Lax-Wendroff](/lax-wendroff-method/) and MacCormack.** They are second order, but oscillate near shocks.
- **Viscous problems.** The [method of lines](/method-of-lines/) with centred differences or [spectral methods](/spectral-methods/), an implicit or IMEX time stepper for the diffusion, or [operator splitting](/operator-splitting/) between transport and diffusion. The Hopf-Cole formula gives reference solutions.
- **Exact formulas.** For piecewise constant or piecewise linear data, front tracking or the Lax-Oleinik formula give the entropy solution exactly, up to the solution of scalar equations.

## Bounds

- **Lax-Wendroff theorem (1960).** If a conservative scheme with a consistent numerical flux converges boundedly almost everywhere as $\Delta x, \Delta t \to 0$, the limit is a weak solution. This is proved. It does not say that the limit is the entropy solution, as the Roe example shows.
- **Nonconservative schemes** can converge to functions with wrong shock speeds, or not converge to any weak solution. The upwind example above is the simplest case.
- **Monotone schemes.** Conservative monotone schemes (Godunov, Lax-Friedrichs, Engquist-Osher) converge to the entropy solution under the CFL condition (Harten, Hyman and Lax 1976; Crandall and Majda 1980). They are at most first order accurate in smooth regions. For data of bounded variation, Kuznetsov's theory gives an $L^1$ error bound of order $\Delta x^{1/2}$. For a single shock the observed order is 1, as in the table, and for rarefactions it is between $\tfrac12$ and 1.
- **CFL condition.** An explicit scheme needs $\lambda\max|u| \le 1$ (or less, depending on the scheme). See the [CFL condition](/courant-friedrichs-lewy-condition/).

## Reductions

- **Hopf-Cole transformation (Hopf 1950, Cole 1951).** If $\varphi > 0$ solves the [heat equation](/heat-equation/) $\varphi_t = \nu\varphi_{xx}$, then $u = -2\nu\varphi_x/\varphi$ solves the viscous Burgers' equation. With $U_0(y) = \int_0^yu_0$,
$$\varphi(x, t) = \frac1{\sqrt{4\pi\nu t}}\int_{\mathbb{R}}\exp\Big(-\frac{(x - y)^2}{4\nu t} - \frac{U_0(y)}{2\nu}\Big)dy.$$
So the viscous problem reduces to a linear one and has an explicit solution.
- **Lax-Oleinik formula.** Letting $\nu \to 0$ in the Hopf-Cole formula with Laplace's method gives the entropy solution $u(x, t) = (x - y^*)/t$, where $y^*$ minimizes $(x - y)^2/(2t) + U_0(y)$ (Evans, Section 3.4). The inviscid problem reduces to a minimization for each $(x, t)$.
- **Characteristics.** Before $T_b$, computing $u(x, t)$ reduces to solving $x = \xi + u_0(\xi)t$ for $\xi$.
- **Traffic flow.** The Lighthill-Whitham-Richards model $\rho_t + (\rho(1 - \rho))_x = 0$ becomes $u_t + uu_x = 0$ with $u = 1 - 2\rho$ for smooth solutions. Since $u$ is an affine function of $\rho$, the shock speeds also agree.
- **Other convex laws.** For smooth solutions of $v_t + f(v)_x = 0$, $u = f'(v)$ satisfies Burgers' equation. For shocks this map does not preserve the Rankine-Hugoniot condition unless $f$ is quadratic.

## Applications

- The standard test problem for shock-capturing schemes: every new flux, limiter or reconstruction is first tried on Burgers' Riemann problems and on the breaking sine wave.
- Burgers (1948) proposed it as a one-dimensional model of turbulence. It is still used for studies of decaying turbulence and of the inviscid limit.
- A model for weak shocks in gas dynamics, for kinematic waves in traffic flow, and for the steepening of nonlinear acoustic waves.
- A test for the convection term in solvers for the Navier-Stokes equations, and a benchmark for model reduction, data assimilation and learned solvers, because exact solutions are known.

## References
