---
tag: 7BZW23
kind: problem
slug: advection-equation
name: Advection equation
aliases:
- linear transport equation
- linear advection equation
- one-way wave equation
area: numerical/differential-equations
level: core
summary: The hyperbolic PDE u_t + a u_x = 0, whose solution u(x, t) = u_0(x - a t) moves the initial profile at speed a. The basic test problem for schemes for hyperbolic equations.
model: real-ram
prereqs: [pde-classification]
see_also: [courant-friedrichs-lewy-condition, upwind-scheme, lax-wendroff-method, lax-friedrichs-scheme, method-of-characteristics, burgers-equation, finite-volume-method, flux-limiter-methods]
sources:
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 10 (advection equations and hyperbolic systems; method of lines, Lax-Wendroff, upwind, von Neumann analysis, the CFL condition, modified equations)
  - book: isbn:9780521009249
    title: Randall J. LeVeque, Finite Volume Methods for Hyperbolic Problems, Cambridge University Press, 2002
    locator: Chapter 2 (the advection equation and its characteristics), Chapter 4 (finite volume methods), Chapter 6 (high-resolution methods, limiters) and Chapter 8 (convergence, accuracy and stability)
  - book: isbn:9780521734905
    title: Arieh Iserles, A First Course in the Numerical Analysis of Differential Equations, second edition, Cambridge University Press, 2009
    locator: Chapter 17, Sections 17.1 and 17.2 (why the advection equation, finite differences for it)
  - book: isbn:9780898715675
    title: John C. Strikwerda, Finite Difference Schemes and Partial Differential Equations, second edition, SIAM, 2004
    locator: Chapter 1 (the one-way wave equation, its schemes and the CFL condition)
  - paper: "S. K. Godunov, A difference method for numerical calculation of discontinuous solutions of the equations of hydrodynamics, Matematicheskii Sbornik 47(89) (1959) 271-306 (in Russian)"
    locator: the theorem that linear monotone schemes are at most first order accurate
---

The advection equation $u_t + a u_x = 0$ describes a quantity $u(x, t)$ that is carried along at a constant speed $a$ without changing shape. Its solution is $u(x, t) = u_0(x - at)$, so the problem is trivial to solve exactly, and this is why it is the standard test problem for numerical schemes for hyperbolic equations: every error a scheme makes, smearing, wiggles, wrong speed or blow-up, is visible against the exact answer. The [CFL condition](/courant-friedrichs-lewy-condition/), [upwind differencing](/upwind-scheme/), the [Lax-Wendroff method](/lax-wendroff-method/), numerical diffusion and dispersion, and flux limiters were all first understood on this equation.

## In plain words

Think of a wind that blows at a constant speed along a straight road, carrying a cloud of smoke. The smoke does not spread or change; the whole cloud just moves. That is what the equation says. To find the smoke at a later time, you take the picture at the start and shift it by the distance the wind travels. A computer that only knows the values on a grid has to rebuild this shift from neighbouring values. If it looks in the wrong direction, or takes too large a time step, the result explodes. If it uses too simple a rule, the cloud slowly blurs. If it uses a more accurate rule, sharp edges grow small ripples. Choosing between these failures is the central problem of computing waves and flows.

## Definition

**Notation.** $u(x, t)$ is the unknown, $\Delta x$ and $\Delta t$ are the mesh widths, $U_j^n \approx u(x_j, t_n)$ with $x_j = j\Delta x$ and $t_n = n\Delta t$, and $\nu = a\Delta t/\Delta x$ is the Courant number.

**Cauchy problem.** Given $a \in \mathbb{R}$ and $u_0 : \mathbb{R} \to \mathbb{R}$, find $u$ with
$$u_t + a u_x = 0 \quad (x \in \mathbb{R},\ t > 0), \qquad u(x, 0) = u_0(x).$$
If $u_0 \in C^1$, the unique $C^1$ solution is $u(x, t) = u_0(x - at)$: along each characteristic line $x = x_0 + at$, $\frac{d}{dt}u(x_0 + at, t) = au_x + u_t = 0$, so $u$ is constant there, and every point $(x, t)$ lies on exactly one such line. For less regular $u_0$, such as a step, the same formula defines the weak solution.

**Well-posedness.** For every $p \in [1, \infty]$, $\|u(\cdot, t)\|_{L^p} = \|u_0\|_{L^p}$, and the solution map is linear, so $\|u(\cdot, t) - v(\cdot, t)\|_{L^p} = \|u_0 - v_0\|_{L^p}$. Small changes in the data give equally small changes in the solution.

**Boundary and periodic problems.** On $[0, L]$ with $a > 0$, a [boundary condition](/boundary-conditions/) $u(0, t) = g(t)$ is given at the inflow end only. With periodic conditions $u(0, t) = u(L, t)$ the profile leaves at one end and returns at the other, and at $t = L/|a|$ the exact solution equals $u_0$ again, which gives an easy error check.

**The computational task.** Given $u_0$ (and inflow data), $a$, a final time $T$ and a mesh, compute $U_j^N$ with $t_N = T$, and measure the error in a stated norm, usually the discrete $L^1$ norm $\Delta x\sum_j |U_j^N - u(x_j, T)|$, the discrete $L^2$ norm, or the max norm.

## Variants

- **Variable coefficients.** $u_t + a(x, t)u_x = 0$ (advective form): $u$ is constant along curves with $dx/dt = a(x, t)$. The conservative form $u_t + (a(x, t)u)_x = 0$ conserves $\int u\,dx$ instead. The two differ when $a$ depends on $x$.
- **Several dimensions.** $u_t + \mathbf{b}\cdot\nabla u = 0$ with a velocity field $\mathbf{b}$; it moves the [level sets](/level-set-method/) of $u$ with the flow.
- **Linear hyperbolic systems.** $u_t + Bu_x = 0$ with $B$ diagonalizable with real eigenvalues; see Reductions.
- **Advection-diffusion.** $u_t + au_x = \kappa u_{xx}$. For small $\kappa$ (large Péclet number $|a|L/\kappa$) the schemes for pure advection are the relevant ones.
- **Nonlinear advection.** [Burgers' equation](/burgers-equation/) $u_t + uu_x = 0$, where the speed depends on $u$ and shocks form.

## Examples

**Exact solutions.** With $a = 1$ and $u_0(x) = e^{-100(x - 0.3)^2}$, the solution at $t = 0.4$ is $e^{-100(x - 0.7)^2}$, the same pulse moved by $0.4$.

**Smooth data, two schemes.** Take $a = 1$, $u_0 = \sin 2\pi x$ on $[0, 1]$ with periodic boundary, $\nu = 0.5$, and $T = 0.5$. The $L^1$ errors are:

| $\Delta x$ | upwind | Lax-Wendroff |
|---|---|---|
| 1/100 | 0.030648 | 0.00098687 |
| 1/200 | 0.015515 | 0.00024673 |
| 1/400 | 0.0078057 | 0.000061685 |
| 1/800 | 0.0039149 | 0.000015421 |

The ratios tend to 2 and to 4: first order and second order, as the truncation errors predict.

**Discontinuous data.** With the step $u_0 = 1$ on $[0.25, 0.5)$ and $0$ elsewhere, under the same settings the $L^1$ error of upwind falls by $1.413$ per halving of $\Delta x$ (from $0.0796$ at $\Delta x = 1/100$ to $0.0282$ at $1/800$), close to $\sqrt{2}$, an observed order of $1/2$. Upwind keeps the solution in $[0, 1]$ but smears the step over a width that grows like $\sqrt{\Delta x\, T}$. Lax-Wendroff falls by about $1.51$ per halving (observed order about $0.6$), and its solution overshoots to $1.24$ and undershoots to $-0.24$ at $\Delta x = 1/800$. These are observed rates; the known asymptotic rates for such linear schemes on a step are $1/2$ for first-order and $2/3$ for second-order schemes (LeVeque, Finite Volume Methods, Chapter 8).

## Known algorithms

- **[Upwind scheme](/upwind-scheme/).** $U_j^{n+1} = U_j^n - \nu(U_j^n - U_{j-1}^n)$ for $a > 0$. First order, stable for $0 \le \nu \le 1$, monotone. Its modified equation $u_t + au_x = \tfrac{a\Delta x}{2}(1 - \nu)u_{xx}$ shows the numerical diffusion.
- **[Lax-Friedrichs scheme](/lax-friedrichs-scheme/).** First order, stable for $|\nu| \le 1$, more diffusive than upwind.
- **[Lax-Wendroff method](/lax-wendroff-method/).** Second order, stable for $|\nu| \le 1$; its leading error is dispersive, $\tfrac{a\Delta x^2}{6}(\nu^2 - 1)u_{xxx}$, which makes wiggles behind steep fronts.
- **Leapfrog and Beam-Warming.** Second order, with the stability ranges $|\nu| \le 1$ and $0 \le \nu \le 2$.
- **[Method of lines](/method-of-lines/).** Discretize in space only and use an ODE solver such as RK3 or [RK4](/classical-runge-kutta-4/); the time step must put $\Delta t$ times the eigenvalues of the space operator inside the [stability region](/absolute-stability/).
- **High-resolution [finite volume methods](/finite-volume-method/).** [Flux limiters](/flux-limiter-methods/) that are [total variation diminishing](/total-variation-diminishing/), and [WENO](/weno-scheme/) reconstructions, give second or higher order on smooth parts without oscillations at jumps.
- **Semi-Lagrangian methods.** Follow the characteristic back from each grid point and interpolate; they allow $|\nu| > 1$.
- **[Spectral methods](/spectral-methods/).** For periodic smooth data, Fourier differentiation is exponentially accurate in space.

## Bounds

- **CFL condition.** An explicit scheme with stencil $x_{j-l}, \dots, x_{j+r}$ can converge only if $-r \le \nu \le l$ ([CFL condition](/courant-friedrichs-lewy-condition/), proved there).
- **Godunov's theorem (1959).** A linear scheme that is monotone (maps monotone data to monotone data) is at most first order accurate. So second order and freedom from oscillations need a nonlinear scheme, such as a limiter.
- **Cost.** An explicit scheme on $N = L/\Delta x$ cells with $\nu$ fixed takes $T|a|/(\nu\Delta x)$ steps of $\Theta(N)$ operations, so $\Theta(N^2)$ operations in one dimension to reach a fixed $T$; in $m$ dimensions with $N$ cells per direction, $\Theta(N^{m+1})$.
- **Accuracy.** For smooth solutions a stable scheme of order $p$ has error $O(\Delta x^p)$ at fixed $\nu$ (by the [Lax equivalence theorem](/lax-equivalence-theorem/) and the truncation error). For discontinuous data the rates fall as described in Examples.

## Reductions

- **Hyperbolic systems to scalar equations.** If $B = R\Lambda R^{-1}$ with real eigenvalues, then $w = R^{-1}u$ satisfies $w_t + \Lambda w_x = 0$, which is $m$ independent advection equations with speeds $\lambda_p$.
- **The wave equation.** $u_{tt} = c^2u_{xx}$ with $v = u_t$, $w = cu_x$ is the system $v_t = cw_x$, $w_t = cv_x$; the combinations $v \pm w$ satisfy advection equations with speeds $\mp c$.
- **To an ODE system.** The method of lines turns the equation into $U' = -\tfrac{a}{\Delta x}DU$ with a difference matrix $D$, an [initial value problem](/ode-initial-value-problem/) in $\mathbb{R}^N$.
- **From the [method of characteristics](/method-of-characteristics/).** Any first-order linear PDE reduces along its characteristics to ODEs.

## Applications

- Transport of a passive tracer (pollutant, temperature, moisture) by a known wind or current, the core step of weather and ocean models.
- Moving interfaces in the [level set method](/level-set-method/).
- The linearization of the Euler equations of gas dynamics and of shallow water flow, which is a system of advection equations for small disturbances.
- The test case for new schemes for conservation laws, before they are applied to [Burgers' equation](/burgers-equation/) and the Euler equations.

## References
