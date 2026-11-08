---
tag: 7HKDM9
kind: technique
slug: von-neumann-stability-analysis
name: Von Neumann stability analysis
aliases:
- Fourier stability analysis
- von Neumann analysis
- amplification factor analysis
area: numerical/differential-equations
level: advanced
summary: "Test the ℓ2 stability of a linear constant-coefficient scheme by inserting a Fourier mode and checking that its amplification factor satisfies |g(θ)| <= 1 + CΔt for all θ."
prereqs: [finite-difference-method, discrete-fourier-transform, heat-equation, advection-equation]
see_also: [lax-equivalence-theorem, courant-friedrichs-lewy-condition, ftcs-method, upwind-scheme, lax-wendroff-method, crank-nicolson-method, stability-region, total-variation-diminishing]
sources:
  - book: isbn:9780898715675
    title: John C. Strikwerda, Finite Difference Schemes and Partial Differential Equations, second edition, SIAM, 2004
    locator: Chapter 2 (analysis of finite difference schemes; Fourier analysis, von Neumann analysis, the stability theorem for one-step schemes), Chapter 4 (multistep schemes, the amplification polynomial and the leapfrog scheme), Chapter 7 (systems and the Kreiss matrix theorem)
  - book: isbn:9780898716290
    title: Randall J. LeVeque, Finite Difference Methods for Ordinary and Partial Differential Equations, SIAM, 2007
    locator: Chapter 9 (diffusion equations; von Neumann analysis of FTCS and Crank-Nicolson), Chapter 10 (advection equations; von Neumann analysis of upwind, Lax-Friedrichs and Lax-Wendroff, modified equations and dispersion)
  - book: isbn:9780521607933
    title: K. W. Morton and D. F. Mayers, Numerical Solution of Partial Differential Equations, second edition, Cambridge University Press, 2005
    locator: Chapter 2 (parabolic equations in one dimension; Fourier analysis of the error), Chapter 4 (hyperbolic equations; amplification factors, dispersion), Chapter 5 (consistency, convergence and stability)
  - paper: doi:10.1002/cpa.3160090206
    title: Peter D. Lax and Robert D. Richtmyer, Survey of the stability of linear finite difference equations, Communications on Pure and Applied Mathematics 9 (1956) 267-293
    locator: the equivalence theorem and the Fourier criterion for constant-coefficient schemes
  - paper: "John Crank and Phyllis Nicolson, A practical method for numerical evaluation of solutions of partial differential equations of the heat-conduction type, Mathematical Proceedings of the Cambridge Philosophical Society 43 (1947) 50-67"
    locator: early published use of the Fourier stability argument attributed to von Neumann; doi:10.1017/S0305004100023197
  - paper: "George G. O'Brien, Morton A. Hyman and Sidney Kaplan, A study of the numerical solution of partial differential equations, Journal of Mathematics and Physics 29 (1951) 223-251"
    locator: systematic exposition of the von Neumann method; doi:10.1002/sapm1950291223
---

Von Neumann stability analysis decides whether a linear finite difference scheme with constant coefficients is stable, by asking what the scheme does to a single Fourier mode. Insert $U_j^n = g^n e^{ij\theta}$ into the scheme; the scheme maps the mode to a multiple of itself, and the multiplier $g(\theta)$ is the **amplification factor**. If $|g(\theta)| \le 1 + C\Delta t$ for every frequency $\theta \in [-\pi, \pi]$, the scheme is stable in the discrete $\ell^2$ norm; if not, some mode grows exponentially. Together with consistency and the [Lax equivalence theorem](/lax-equivalence-theorem/), this gives convergence. It is the tool that produces the classical conditions $\kappa\Delta t/\Delta x^2 \le \frac{1}{2}$ for the [FTCS](/ftcs-method/) heat scheme and $|a|\Delta t/\Delta x \le 1$ for the [upwind](/upwind-scheme/) and [Lax-Wendroff](/lax-wendroff-method/) schemes.

## In plain words

Any grid function is a sum of waves, from the smoothest one to the sawtooth that flips sign at every grid point. A linear scheme with the same formula at every point treats each wave separately: one step multiplies the wave by a number that depends only on its frequency. If none of these numbers is bigger than 1 in size (up to a tiny allowance), no wave can grow, and the scheme is stable. If even one of them is bigger than 1, that wave will grow by the same factor every step, and rounding errors alone will eventually seed it.

The analysis turns a question about a huge matrix into a short formula in one variable $\theta$. The dangerous frequency is often the highest one, $\theta = \pi$, the sawtooth that the PDE barely has but the grid can hold.

## When it applies

- **Linear, constant-coefficient schemes.** The difference operator must have the same coefficients at every grid point, so that Fourier modes are eigenvectors. Variable or nonlinear coefficients need the frozen-coefficient heuristic of the Variations section.
- **No boundaries, or periodic ones.** The analysis is exact on the whole line $\mathbb{Z}$ or on a periodic grid. Boundary conditions can add instabilities that the analysis cannot see.
- **The $\ell^2$ norm.** Parseval's identity turns the discrete $\ell^2$ norm $\|U\|_{2,\Delta x} = (\Delta x\sum_j|U_j|^2)^{1/2}$ into the $L^2$ norm of the Fourier transform. The test says nothing directly about the max norm, a maximum principle or total variation.
- **Refinement along a path.** Stability means $\|U^n\| \le K\|U^0\|$ for $0 \le n\Delta t \le T$ as $\Delta t, \Delta x \to 0$ with a fixed relation, such as a fixed Courant number $\nu = a\Delta t/\Delta x$ or a fixed $\mu = \kappa\Delta t/\Delta x^2$.

## The template

```pseudo id=main
VON-NEUMANN(scheme)                    ▷ linear, constant coefficients, periodic or on Z
L1  freeze coefficients and drop the boundary conditions
L2  substitute U_j^n = g^n e^(i j θ) (a vector amplitude for systems or for several time levels)
L3  divide out g^n e^(i j θ): get g(θ), or the amplification matrix G(θ) with U^(n+1) = G(θ) U^n
L4  compute M(Δt) = max over θ in [−π, π] of |g(θ)| (or of ‖G(θ)^n‖ for matrices)
L5  if M(Δt) <= 1 + CΔt for small Δt then report stable in ℓ2
L6  else report the unstable θ and solve M <= 1 for the admissible ratio (ν or μ)
```

The holes are the scheme, the refinement path (which ratio is held fixed) and, for matrices, the bound used in line L4.

**Why it works (proved for one-step scalar schemes).** On $\mathbb{Z}$, define $\hat U(\theta) = \frac{\Delta x}{\sqrt{2\pi}}\sum_j U_j e^{-ij\theta}$. A scheme $U_j^{n+1} = \sum_k c_k U_{j+k}^n$ (explicit) or $\sum_k d_k U^{n+1}_{j+k} = \sum_k c_k U_{j+k}^n$ (implicit) gives $\hat U^{n+1}(\theta) = g(\theta)\hat U^n(\theta)$ with $g = \sum c_k e^{ik\theta}/\sum d_k e^{ik\theta}$. Parseval's identity gives

$$\|U^n\|_{2,\Delta x} = \|g^n\hat U^0\|_{L^2(-\pi, \pi)} \le \max_\theta|g(\theta)|^n\,\|U^0\|_{2,\Delta x}.$$

If $|g| \le 1 + C\Delta t$, then $|g|^n \le e^{CT}$ for $n\Delta t \le T$: stable. Conversely, if $|g(\theta_0)| > 1 + C\Delta t$ for every $C$ along the refinement path, initial data concentrated near $\theta_0$ grow without bound. This is the stability theorem of Chapter 2 of Strikwerda's book. When $g$ does not depend on $\Delta t$ separately (as for the schemes below with $\nu$ or $\mu$ fixed), the condition reduces to $\max_\theta|g| \le 1$.

**Systems and multilevel schemes (necessary only).** For a scheme with several time levels or a system, $G(\theta)$ is a matrix and stability requires $\|G(\theta)^n\| \le K$. The spectral radius condition $\rho(G(\theta)) \le 1 + C\Delta t$ is necessary. It is also sufficient when $G(\theta)$ is normal, or more generally under the Kreiss matrix theorem; a Jordan block on the unit circle gives linear growth $\|G^n\| \sim n$ although every eigenvalue has modulus 1.

## Classic examples

**FTCS for the heat equation.** For $u_t = \kappa u_{xx}$ and $U_j^{n+1} = U_j^n + \mu(U_{j+1}^n - 2U_j^n + U_{j-1}^n)$ with $\mu = \kappa\Delta t/\Delta x^2$, line L3 gives $g(\theta) = 1 - 4\mu\sin^2(\theta/2)$. The minimum is $1 - 4\mu$ at $\theta = \pi$, so the scheme is stable exactly when $\mu \le \frac{1}{2}$. With $M = 20$ intervals on $[0, 1]$, homogeneous Dirichlet conditions and the triangle $u_0 = \min(x, 1 - x)$, the max-norm errors against the Fourier series solution are (observed):

| $\mu$ | $g(\pi)$ | $t \approx 0.06$ | $t \approx 0.25$ | $t \approx 1$ |
|---|---|---|---|---|
| 0.40 | -0.60 | 1.5e-4 | 2.1e-4 | 3.1e-6 |
| 0.50 | -1.00 | 1.5e-3 | 4.8e-4 | 9.1e-7 |
| 0.51 | -1.04 | 9.8e-3 | 0.56 | 6.4e6 |
| 0.55 | -1.20 | 13 | 1.8e12 | 6.3e56 |

A 2% change in the time step decides between a correct answer and $10^6$.

**Advection schemes.** For $u_t + au_x = 0$ with $\nu = a\Delta t/\Delta x$ and $s = \sin^2(\theta/2)$:

| scheme | $g(\theta)$ | $\lvert g\rvert^2$ | stable for |
|---|---|---|---|
| FTCS (centered) | $1 - i\nu\sin\theta$ | $1 + \nu^2\sin^2\theta$ | never |
| upwind ($a > 0$) | $1 - \nu(1 - e^{-i\theta})$ | $1 - 4\nu(1 - \nu)s$ | $0 \le \nu \le 1$ |
| Lax-Friedrichs | $\cos\theta - i\nu\sin\theta$ | $\cos^2\theta + \nu^2\sin^2\theta$ | $\lvert\nu\rvert \le 1$ |
| Lax-Wendroff | $1 - i\nu\sin\theta - 2\nu^2 s$ | $1 - 4\nu^2(1 - \nu^2)s^2$ | $\lvert\nu\rvert \le 1$ |

A numerical maximization of $|g|$ over 2001 values of $\theta$ gives $\max|g| = 1.118$ for centered FTCS at $\nu = 0.5$, $1.2$ for upwind at $\nu = 1.1$ (and $2.0$ at $\nu = -0.5$, the wrong upwind direction), $1.1$ for Lax-Friedrichs and $1.42$ for Lax-Wendroff at $\nu = 1.1$. Running upwind on a Gaussian with 100 cells gives a maximum of $0.858$ after 200 steps at $\nu = 0.9$ and $4.56 \times 10^3$ at $\nu = 1.1$. The stability limits coincide with the [CFL condition](/courant-friedrichs-lewy-condition/) for these schemes, but the analysis also shows that centered FTCS is unstable although it satisfies CFL for $|\nu| \le 1$.

**Implicit schemes.** [Crank-Nicolson](/crank-nicolson-method/) for the heat equation gives $g = (1 - 2\mu s)/(1 + 2\mu s)$ and backward Euler $g = 1/(1 + 4\mu s)$; both satisfy $|g| \le 1$ for every $\mu > 0$, so they are unconditionally stable. At $\theta = \pi$ and large $\mu$, Crank-Nicolson has $g \to -1$ (for $\mu = 1$, $g = -1/3$), so sawtooth errors decay slowly and change sign each step, the PDE form of the lack of [L-stability](/l-stability/).

**Leapfrog (two levels).** $U_j^{n+1} = U_j^{n-1} - \nu(U_{j+1}^n - U_{j-1}^n)$ gives $g^2 + 2i\nu\sin\theta\,g - 1 = 0$. For $|\nu| < 1$ both roots have $|g| = 1$ and are distinct: stable, with no damping. At $\nu = 1.1$ the larger root reaches $1.558$. At $\nu = 1$ the roots coincide at $\theta = \pi/2$ and the amplification matrix is a Jordan block: starting the $\theta = \pi/2$ mode with a $10^{-3}$ error in the second level, the amplitude is $1.005$ after 100 steps, $1.41$ after 1000 and $10.05$ after 10000 (observed), the linear growth predicted for a Jordan block.

**Dispersion.** The argument of $g$ gives the numerical phase speed. For Lax-Wendroff at $\nu = 0.5$ the ratio of numerical to exact phase speed is $0.981$, $0.928$, $0.749$ at $\theta = \pi/8, \pi/4, \pi/2$, with $|g| = 0.9995$, $0.9919$, $0.9014$: short waves lag and are damped, which is the origin of the trailing oscillations behind a jump.

## Variations

- **Several space dimensions.** Use $e^{i(j\theta_1 + k\theta_2)}$. FTCS in two dimensions gives $g = 1 - 4\mu_x\sin^2(\theta_1/2) - 4\mu_y\sin^2(\theta_2/2)$, stable iff $\mu_x + \mu_y \le \frac{1}{2}$.
- **Semi-discretization.** For the [method of lines](/method-of-lines/), the Fourier symbol of the spatial operator gives the eigenvalues $\lambda(\theta)$ of the ODE system; the time integrator is stable when all $\Delta t\,\lambda(\theta)$ lie in its [stability region](/stability-region/) (exactly so for normal operators such as periodic differences).
- **Frozen coefficients.** For variable coefficients, require the von Neumann condition at every frozen value. This is a heuristic; Kreiss and Strang proved it is sufficient for dissipative schemes with smooth coefficients, and it can fail for nondissipative ones.
- **Nonlinear schemes.** Linearize about a smooth solution. This explains why nonlinear schemes such as limited or [TVD](/total-variation-diminishing/) schemes need different tools near shocks.
- **Boundaries.** The Godunov-Ryabenkii condition and the Gustafsson-Kreiss-Sundström (GKS) normal mode analysis extend the Fourier test to initial-boundary value problems.
- **The energy method** proves stability in a norm directly by summation by parts, and also covers variable coefficients and boundaries.

## Pitfalls

- **Smooth test data can hide an instability.** With $u_0 = \sin\pi x$ and $\mu = 0.51$ the FTCS error is still $1.8 \times 10^{-6}$ after 800 steps, because only rounding seeds the sawtooth mode; after 1200 steps it is $3.5 \times 10^{-3}$ and after 1600 steps it is 179. A test that passes is not a stability proof.
- **Checking only small $\theta$.** The unstable mode is usually at $\theta = \pi$ or near it; a Taylor expansion of $g$ for small $\theta$ checks accuracy, not stability.
- **Eigenvalues are not enough for matrices.** For systems and multilevel schemes, $\rho(G) \le 1$ is necessary only, as the leapfrog Jordan block shows.
- **$\ell^2$ stability is not monotonicity.** Lax-Wendroff is $\ell^2$ stable for $|\nu| \le 1$ but overshoots discontinuities by more than 20%; positivity and maximum principles need other criteria.
- **Fixing the wrong ratio.** Stability depends on the refinement path. Hyperbolic schemes are analyzed with $\Delta t/\Delta x$ fixed, parabolic ones with $\Delta t/\Delta x^2$ fixed; mixing them up changes the answer.
- **Allowing $1 + C\Delta t$.** The condition allows $|g|$ slightly above 1 for problems whose solutions grow, such as $u_t = u_{xx} + u$; demanding $|g| \le 1$ wrongly rejects such schemes.

## Exercises

1. Show that the Beam-Warming scheme has $|g|^2 = 1 - 4\nu(1 - \nu)^2(2 - \nu)s^2$ with $s = \sin^2(\theta/2)$, and deduce that it is stable for $0 \le \nu \le 2$.
2. For the $\theta$-method $U^{n+1} - U^n = \mu\big(\vartheta\delta^2U^{n+1} + (1 - \vartheta)\delta^2U^n\big)$ with $\delta^2U_j = U_{j+1} - 2U_j + U_{j-1}$, prove that it is unconditionally stable for $\vartheta \ge \frac{1}{2}$ and stable iff $\mu(1 - 2\vartheta) \le \frac{1}{2}$ otherwise.
3. Derive the amplification matrix of the leapfrog scheme and show that it is not uniformly power bounded at $\nu = 1$.
4. Show that the DuFort-Frankel scheme for the heat equation is unconditionally stable in the von Neumann sense, and explain why it is still not convergent unless $\Delta t/\Delta x \to 0$.

## References
