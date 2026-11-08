---
tag: T2RXGZ
kind: problem
slug: wave-equation
name: Wave equation
aliases:
- one-dimensional wave equation
- vibrating string equation
area: numerical/differential-equations
level: intro
summary: "The hyperbolic PDE u_tt = c^2 u_xx. Energy is conserved and signals move at speed c. The leapfrog scheme has error O(Δx^2 + Δt^2) and is stable for Courant numbers up to 1."
model: real-ram
prereqs: [pde-classification, boundary-conditions, finite-differences]
see_also: [advection-equation, courant-friedrichs-lewy-condition, von-neumann-stability-analysis, lax-equivalence-theorem, verlet-integration, method-of-characteristics, method-of-lines, heat-equation]
sources:
  - book: isbn:9780821849743
    title: Lawrence C. Evans, Partial Differential Equations, second edition, American Mathematical Society, 2010
    locator: Section 2.4 (the wave equation, d'Alembert's formula, energy methods and finite propagation speed)
  - book: isbn:9780898715675
    title: John C. Strikwerda, Finite Difference Schemes and Partial Differential Equations, second edition, SIAM, 2004
    locator: Chapter 8 (second-order equations, the leapfrog scheme for the wave equation and its stability)
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 10 (advection equations and hyperbolic systems, the CFL condition)
  - paper: doi:10.1007/BF01448839
    title: Richard Courant, Kurt Friedrichs and Hans Lewy, Über die partiellen Differenzengleichungen der mathematischen Physik, Mathematische Annalen 100 (1928) 32-74
    locator: the difference scheme for the wave equation and the domain of dependence condition
---

The wave equation $u_{tt} = c^2 u_{xx}$ is the model [hyperbolic](/pde-classification/) partial differential equation. It describes a vibrating string, sound in a pipe and, in several dimensions, sound and light. Its solutions keep their energy and move at the finite speed $c$. The standard numerical method, the leapfrog scheme, is stable exactly when the [Courant number](/courant-friedrichs-lewy-condition/) is at most 1.

## In plain words

Pluck a guitar string. The bump splits in two halves, one runs to the left and one to the right, both at the same speed. At the fixed ends they reflect and come back upside down. The string keeps its energy and only moves it around.

A computer stores the height of the string at many points and updates all of them in small time steps. Each new height uses the two previous heights at that point and the heights of its two neighbours. This works only if a time step is short enough that a wave cannot pass more than one grid point in one step. If the step is a little too long, tiny rounding errors grow very fast and the numbers explode. If the step is shorter, the waves travel a little too slowly on the grid, which shows as small ripples behind sharp fronts.

## Definition

**Notation.** The unknown is $u(x, t)$ and $c > 0$ is the wave speed. The mesh widths are $\Delta x = \ell / M$ and $\Delta t$, the grid points are $x_j = j \Delta x$ and $t_n = n \Delta t$, and $U_j^n \approx u(x_j, t_n)$. The Courant number is $\nu = c\, \Delta t / \Delta x$. Errors are measured in the max norm over the grid points at a fixed time.

**The initial-boundary value problem.** Given $u_0$ and $v_0$ on $[0, \ell]$, find $u$ with

$$u_{tt} = c^2 u_{xx} \quad (0 < x < \ell,\ t > 0), \qquad u(x, 0) = u_0(x), \quad u_t(x, 0) = v_0(x), \qquad u(0, t) = u(\ell, t) = 0.$$

The equation is second order in time, so it needs two initial conditions: the shape and the velocity.

**d'Alembert's formula.** On the whole line, with $u_0 \in C^2$ and $v_0 \in C^1$, the unique solution is

$$u(x, t) = \frac{u_0(x - ct) + u_0(x + ct)}{2} + \frac{1}{2c}\int_{x - ct}^{x + ct} v_0(s)\, ds$$

(Evans, Section 2.4.1). Each solution is a sum $F(x - ct) + G(x + ct)$ of a wave to the right and a wave to the left. The value at $(x, t)$ depends only on the data in the interval $[x - ct, x + ct]$, its domain of dependence. For the string with fixed ends, extend $u_0$ and $v_0$ to odd functions of period $2\ell$ and use the same formula.

**Fourier series.** With $u_0 = \sum_k a_k \sin(k\pi x/\ell)$ and $v_0 = 0$, the solution is $u = \sum_k a_k \cos(k\pi c t/\ell) \sin(k\pi x/\ell)$. No mode decays: unlike the [heat equation](/heat-equation/), the wave equation does not smooth its data. A corner in $u_0$ stays a corner for all time.

**Energy.** For a smooth solution with fixed ends, $E(t) = \int_0^\ell \left(u_t^2 + c^2 u_x^2\right) dx$ is constant. *Proof.* $E'(t) = 2\int_0^\ell (u_t u_{tt} + c^2 u_x u_{xt})\, dx = 2\int_0^\ell u_t (u_{tt} - c^2 u_{xx})\, dx + 2c^2 [u_x u_t]_0^\ell = 0$, after an integration by parts, because $u_t = 0$ at both ends. $\square$ Applied to the difference of two solutions, this proves uniqueness.

**First-order form.** With $w = (u_t, c\,u_x)$ the equation becomes $w_t = A w_x$ with $A = \begin{pmatrix} 0 & c \\ c & 0 \end{pmatrix}$. The eigenvalues of $A$ are $\pm c$, so the system is hyperbolic, and the characteristic variables $u_t \pm c\, u_x$ each solve an [advection equation](/advection-equation/).

**The leapfrog scheme.** Replace both second derivatives by central differences:

$$U_j^{n+1} = 2U_j^n - U_j^{n-1} + \nu^2 \left(U_{j+1}^n - 2U_j^n + U_{j-1}^n\right), \qquad 1 \le j \le M - 1,$$

with $U_0^n = U_M^n = 0$. The first step uses the Taylor expansion $u(x, \Delta t) \approx u_0 + \Delta t\, v_0 + \frac12 \Delta t^2 c^2 u_0''$, that is $U_j^1 = U_j^0 + \Delta t\, v_0(x_j) + \frac{\nu^2}{2}(U_{j+1}^0 - 2U_j^0 + U_{j-1}^0)$. Each step costs $O(M)$ operations. This scheme is the [Störmer-Verlet method](/verlet-integration/) applied to the semi-discrete system $U'' = c^2 \Delta x^{-2} \delta^2 U$.

**The computational task.** Given $u_0$, $v_0$, $c$, $\ell$, $T$ and a mesh, compute $U^N$ with $t_N = T$, and report the error in a stated norm.

## Variants

- **Several dimensions.** $u_{tt} = c^2 \Delta u$. In three dimensions a sharp pulse stays sharp (Huygens' principle). In two dimensions it leaves a tail.
- **Variable speed.** $u_{tt} = (c(x)^2 u_x)_x$ or $\rho(x) u_{tt} = (\kappa(x) u_x)_x$, for waves in layered media. Waves reflect partly where $c$ jumps.
- **Damped and forced waves.** $u_{tt} + \gamma u_t = c^2 u_{xx} + g$. The damping makes the energy decrease.
- **Open boundaries.** On a truncated domain, absorbing or perfectly matched layers stop waves from reflecting at the artificial edge.
- **Helmholtz equation.** For time-harmonic waves $u = e^{-i\omega t} v(x)$, the wave equation becomes $-\Delta v - (\omega/c)^2 v = 0$, an indefinite relative of the [Poisson equation](/poisson-equation/).
- **Nonlinear waves.** The Klein-Gordon and sine-Gordon equations add a term $V'(u)$. They are [Hamiltonian systems](/hamiltonian-systems/) in infinite dimension, a standard use of [symplectic integrators](/symplectic-integrators/).

## Examples

**A standing wave.** Take $c = \ell = 1$, $u_0 = \sin(\pi x)$, $v_0 = 0$, so $u = \sin(\pi x)\cos(\pi t)$. Run the leapfrog scheme with $\nu = 0.5$ up to $T = 0.5$. For $M = 10, 20, 40, 80, 160$ the max errors are $4.852 \cdot 10^{-3}$, $1.212 \cdot 10^{-3}$, $3.028 \cdot 10^{-4}$, $7.570 \cdot 10^{-5}$ and $1.893 \cdot 10^{-5}$. The observed orders $\log_2$ of the ratios are $2.002$, $2.000$, $2.000$, $2.000$. At $T = 1$ the errors are far smaller ($4.7 \cdot 10^{-5}$ for $M = 10$) and fall by 16 at each halving. This is not a higher order: the error is mainly a phase error, and at $T = 1$ the exact solution is at a turning point, where a phase shift changes the value only to second order.

**The magic time step.** With $\nu = 1$ the leapfrog scheme is exact. The scheme becomes $U_j^{n+1} + U_j^{n-1} = U_{j+1}^n + U_{j-1}^n$. Each $F(x - ct)$ satisfies it on the grid, because $x_j - c t_{n+1} = x_{j-1} - c t_n$ and $x_j - c t_{n-1} = x_{j+1} - c t_n$ when $c \Delta t = \Delta x$. The same holds for each $G(x + ct)$. With $v_0 = 0$ the start step gives $U_j^1 = \frac12 (U_{j+1}^0 + U_{j-1}^0)$, which is d'Alembert's formula. So the errors are only rounding: $2.2 \cdot 10^{-16}$ for $M = 10$ above.

**A plucked string, just below and just above the limit.** Take $u_0(x) = \min(x, 1 - x)$, $v_0 = 0$, $M = 50$ and $T = 2$, one full period. The exact solution comes from d'Alembert's formula with the odd periodic extension.

| $\nu$ | steps | max error at $T$ | $\max_j |U_j^N|$ |
|---|---|---|---|
| 0.99 | 101 | $4.69 \cdot 10^{-3}$ | 0.495 |
| 1.00 | 100 | $4.4 \cdot 10^{-16}$ | 0.500 |
| 1.01 | 99 | $1.40 \cdot 10^{8}$ | $1.40 \cdot 10^{8}$ |

With $\nu = 0.99$ the corners of the profile spread into small ripples: the short waves travel too slowly. With $\nu = 1.01$ the shortest waves grow by a factor of about 1.33 per step, and after 99 steps the solution is destroyed. With $M = 100$ and $\nu = 1.01$ the result at $T = 2$ is $7.5 \cdot 10^{19}$.

## Known algorithms

- **Leapfrog (central in time and space).** Explicit, second order, three time levels, stable for $\nu \le 1$. The standard choice for constant or smooth coefficients.
- **[Method of lines](/method-of-lines/) with a symplectic integrator.** Discretize in space by finite differences, finite elements or [spectral methods](/spectral-methods/), then integrate $U'' = -K U$ with [Störmer-Verlet](/verlet-integration/). The energy error then stays bounded for long times.
- **Schemes for the first-order system.** [Lax-Wendroff](/lax-wendroff-method/), [upwind](/upwind-scheme/) on the characteristic variables, and [finite volume](/finite-volume-method/) methods. These handle discontinuous coefficients and are the base of methods for nonlinear hyperbolic systems.
- **Implicit schemes.** The $\theta$-scheme $U^{n+1} - 2U^n + U^{n-1} = \nu^2 \delta^2(\theta U^{n+1} + (1 - 2\theta) U^n + \theta U^{n-1})$ is unconditionally stable for $\theta \ge \frac14$. Each step solves a tridiagonal system. Implicit schemes are rarely worth the cost here, because accuracy already needs $\Delta t \sim \Delta x / c$.
- **Exact methods for special data.** For constant $c$ in one dimension, d'Alembert's formula or the [method of characteristics](/method-of-characteristics/) gives the solution directly.

## Bounds

- **Domain of dependence.** An explicit scheme that uses the neighbours $j \pm 1$ has a numerical domain of dependence of width $\Delta x$ per step. It can converge only if this contains the true domain of dependence, that is $\nu \le 1$ ([CFL condition](/courant-friedrichs-lewy-condition/), Courant, Friedrichs and Lewy 1928). This is a necessary condition for each explicit scheme with this stencil.
- **Von Neumann analysis.** Put $U_j^n = g^n e^{i k x_j}$ into the leapfrog scheme. Then $g + g^{-1} = 2 - 4\nu^2 \sin^2(k\Delta x/2)$. If $\nu \sin(k\Delta x/2) \le 1$, the two roots are $e^{\pm i\omega\Delta t}$ with $\sin(\omega\Delta t/2) = \nu\sin(k\Delta x/2)$, so $|g| = 1$. If $\nu\sin(k\Delta x/2) > 1$, one root is real with $|g| > 1$. For $s = \nu \sin(k\Delta x/2) = 1.01$ this root is $-1.3266$. So the scheme is stable for $\nu \le 1$ and unstable for $\nu > 1$ ([von Neumann analysis](/von-neumann-stability-analysis/)).
- **Discrete energy.** Multiply the scheme by $U_j^{n+1} - U_j^{n-1}$ and sum over $j$ by parts. This shows that $E^{n+1/2} = \sum_j (U_j^{n+1} - U_j^n)^2 + \nu^2 \sum_j (U_{j+1}^{n+1} - U_j^{n+1})(U_{j+1}^n - U_j^n)$ is the same for each $n$. For $\nu < 1$ it is a positive definite quadratic form, which gives a direct stability proof in the energy norm.
- **Convergence.** The truncation error is $O(\Delta t^2 + \Delta x^2)$ when $u \in C^4$. With stability for $\nu \le 1$ and the [Lax equivalence theorem](/lax-equivalence-theorem/), the scheme converges with order 2 at a fixed Courant number.
- **Dispersion.** For $\nu < 1$ the discrete phase speed $\omega/k$ is smaller than $c$ and decreases for shorter waves. A mode with $p$ points per wavelength has a relative phase error of order $p^{-2}$, so a second-order scheme needs many points per wavelength for long runs.

## Reductions

- **To two advection equations.** The characteristic variables $u_t \pm c\, u_x$ satisfy $r_t \mp c\, r_x = 0$. Schemes for the [advection equation](/advection-equation/) apply to each.
- **To an ODE system.** The [method of lines](/method-of-lines/) gives $U'' = -K U$ with a symmetric positive semidefinite $K$, a linear [Hamiltonian system](/hamiltonian-systems/) with the frequencies $\sqrt{\lambda_k(K)}$.
- **To an eigenproblem.** Separation of variables reduces the problem to the eigenfunctions of $-d^2/dx^2$, a [Sturm-Liouville problem](/sturm-liouville-problem/). With $c(x)$ variable, the eigenfunctions are no longer sines.

## Applications

- **Acoustics and seismics.** Sound propagation, seismic imaging and full waveform inversion solve wave equations in heterogeneous media with millions of unknowns.
- **Electromagnetics.** Each component of the electric and magnetic field in vacuum solves the wave equation. The Yee scheme for Maxwell's equations is a staggered leapfrog scheme.
- **Vibrations.** Strings, membranes and beams in mechanical and musical models.
- **A test problem.** Since the energy is conserved and the exact solution is known for many data, the wave equation tests long-time behaviour, dispersion and the CFL limit of new schemes.

## References
