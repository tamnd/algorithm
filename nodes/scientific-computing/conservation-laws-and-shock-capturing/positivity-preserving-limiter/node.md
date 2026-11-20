---
tag: YD4710
kind: technique
slug: positivity-preserving-limiter
name: Positivity-preserving limiter
aliases:
- Zhang-Shu limiter
area: scientific-computing/conservation-laws-and-shock-capturing
level: research
summary: "Scales a high-order polynomial toward its cell mean so that density and pressure stay positive at the quadrature points. Keeps the mean and high order; positive means need a CFL condition."
prereqs: [discontinuous-galerkin-method, euler-equations-of-gas-dynamics, strong-stability-preserving-runge-kutta]
see_also: [runge-kutta-discontinuous-galerkin, weno-scheme, gauss-lobatto-quadrature, lax-friedrichs-scheme, hll-riemann-solver, entropy-stable-scheme, well-balanced-scheme, flux-limiter-methods]
sources:
  - paper: "Xiangxiong Zhang and Chi-Wang Shu, On maximum-principle-satisfying high order schemes for scalar conservation laws, Journal of Computational Physics 229(9) (2010) 3091-3120"
    locator: the scaling limiter for the bounds of a scalar law, the convex decomposition of the cell mean with Gauss-Lobatto points, the CFL condition, the accuracy of the limiter
  - paper: "Xiangxiong Zhang and Chi-Wang Shu, On positivity-preserving high order discontinuous Galerkin schemes for compressible Euler equations on rectangular meshes, Journal of Computational Physics 229(23) (2010) 8918-8934"
    locator: the limiter for density and pressure, the convex set of admissible states, the extension to two dimensions
  - paper: "Sigal Gottlieb, Chi-Wang Shu and Eitan Tadmor, Strong stability-preserving high-order time discretization methods, SIAM Review 43(1) (2001) 89-112"
    locator: SSP Runge-Kutta methods as convex combinations of forward Euler steps
---

The positivity-preserving limiter of Zhang and Shu keeps the density and pressure of a high-order scheme for the [Euler equations](/euler-equations-of-gas-dynamics/) positive, and for a scalar law keeps the solution within the bounds of the initial data, without losing high order for smooth solutions. In each cell it replaces the polynomial $u_h$ by $\bar u + \theta(u_h - \bar u)$, where $\bar u$ is the cell mean and $\theta \in [0, 1]$ is the largest factor for which the values at a set of quadrature points are admissible. The mean does not change, so the scheme stays conservative. The limiter alone does not make the scheme positive. The other half of the method is a theorem: if the values at the Gauss-Lobatto points of every cell are admissible, then one forward Euler step of the cell means is a convex combination of first-order positive steps, and so the new means are admissible under a reduced CFL condition. [SSP Runge-Kutta](/strong-stability-preserving-runge-kutta/) time stepping, with the limiter after every stage, carries this to high order in time.

## In plain words

A gas cannot have negative density or negative pressure, but high-order schemes can produce such values near vacuum or at strong shocks, and then the program stops. This limiter fixes the problem one cell at a time. It keeps the cell's average, which is the part that carries the conservation law, and shrinks the shape of the polynomial toward that average, just enough that the density and pressure are positive at the points the scheme uses. If the shape was already fine, nothing changes. A separate argument shows that if the points in every cell are positive, then the averages after a small enough time step are positive too. So the two parts together keep the whole computation physical.

## When it applies

- A scheme that updates cell means conservatively from point values at cell faces: [DG](/discontinuous-galerkin-method/), finite volume [WENO](/weno-scheme/), and other reconstructions.
- A first-order scheme that keeps the admissible set $G$ under a CFL condition, used as the building block in the proof. Lax-Friedrichs, HLL and Godunov fluxes are positive for the Euler equations; the Roe flux is not.
- An admissible set $G$ that is convex. For a scalar law, $G = [m, M]$, the range of the initial data. For the Euler equations, $G = \{\rho > 0,\ p > 0\}$, which is convex because $p = (\gamma - 1)(E - m^2/(2\rho))$ is a concave function of the conserved variables where $\rho > 0$.
- Problems near vacuum or with very strong shocks: blast waves, jets with high Mach numbers, rarefactions into near vacuum, and the [shallow water equations](/shallow-water-equations/) with wetting and drying, where the water depth must stay nonnegative.

## The template

Let $\hat x_1 < \dots < \hat x_N$ be the Gauss-Lobatto points of cell $C_j$, with weights $\hat w_\alpha$ that add to 1, chosen with $2N - 3 \ge k$ so that the rule is exact for the polynomials of degree $k$. Then $\hat x_1$ and $\hat x_N$ are the cell faces. Let $S_j$ be these points, together with the Gauss points used by the flux and volume terms.

```pseudo id=main
POSITIVITY-LIMITER(u_h, ε)                     ▷ applied after every SSP stage
L1  for each cell j with mean ū = (ρ̄, m̄, Ē) do
L2      ρ_min ← min over x in S_j of ρ_h(x)
L3      θ₁ ← min(1, (ρ̄ - ε) / (ρ̄ - ρ_min));  ρ̂ ← ρ̄ + θ₁ (ρ_h - ρ̄)
L4      for each x in S_j with p(û(x)) < ε: t_x ← the root in [0, 1] of p((1 - t) ū + t û(x)) = ε
L5      θ₂ ← min(1, min_x t_x)
L6      u_h ← ū + θ₂ (û - ū)                   ▷ the mean is unchanged
```

Here $\varepsilon$ is a small positive number with $\bar\rho > \varepsilon$ and $p(\bar u) > \varepsilon$, for example $\min(10^{-13}, \bar\rho, p(\bar u))$. For a scalar law with bounds $m \le u \le M$ the limiter is one step: $\theta = \min\big(1, \frac{M - \bar u}{M_j - \bar u}, \frac{\bar u - m}{\bar u - m_j}\big)$, with $M_j$ and $m_j$ the largest and smallest values of $u_h$ on $S_j$.

**Why the means stay admissible (theorem).** In one dimension, write the forward Euler step of the means with $\lambda = \Delta t/\Delta x$ and use the quadrature $\bar u_j = \sum_\alpha \hat w_\alpha u_\alpha$, with $u_\alpha = u_h(\hat x_\alpha)$, so $u_1 = u^+_{j-1/2}$ and $u_N = u^-_{j+1/2}$:

$$\bar u_j^{n+1} = \sum_{\alpha=2}^{N-1}\hat w_\alpha u_\alpha + \hat w_N\Big[u_N - \tfrac{\lambda}{\hat w_N}\big(F(u_N, u^+_{j+1/2}) - F(u_1, u_N)\big)\Big] + \hat w_1\Big[u_1 - \tfrac{\lambda}{\hat w_1}\big(F(u_1, u_N) - F(u^-_{j-1/2}, u_1)\big)\Big].$$

The term $F(u_1, u_N)$ is added and subtracted. Each bracket is one step of the first-order scheme with flux $F$ and ratio $\lambda/\hat w_1$ (here $\hat w_1 = \hat w_N$), applied to three admissible states. If that scheme keeps $G$ for $\lambda a \le c_0$, then each bracket is in $G$ when $\lambda a \le \hat w_1 c_0$. The point values $u_\alpha$ are in $G$ after the limiter, so $\bar u_j^{n+1}$ is a convex combination of points of $G$ and lies in $G$. For $k = 2$ with $N = 3$ points, $\hat w_1 = \tfrac16$. An SSP Runge-Kutta stage is a convex combination of such steps, so the result holds for the full step, with the limiter after each stage.

**Accuracy.** For a smooth solution whose values stay away from the bounds, $\theta = 1$ on fine grids and the limiter does nothing. Where it does act, Zhang and Shu show that the change $|\bar u + \theta(u_h - \bar u) - u_h|$ is of the same order as the error of $u_h$, so the order of accuracy is kept.

## Classic examples

- [Burgers' equation](/burgers-equation/) and other scalar laws: the limiter keeps the solution within the range of the initial data.
- [Discontinuous Galerkin method](/discontinuous-galerkin-method/): the limiter acts on the polynomial in each cell, checked at the Gauss-Lobatto and Gauss points.
- [WENO schemes](/weno-scheme/): the limiter acts on the reconstruction polynomial of each cell, with the same convex decomposition of the mean.
- [Euler equations](/euler-equations-of-gas-dynamics/): density first, then pressure, as in the template.
- [Shallow water equations](/shallow-water-equations/): the water depth stays nonnegative at wet-dry fronts.

**Density by hand.** A $P^1$ cell has $\rho_h(\xi) = 0.2 + 0.3\xi$ on $\xi \in [-1, 1]$, so $\bar\rho = 0.2$ and the left face value is $-0.1$. With $\varepsilon = 0$: $\theta_1 = \frac{0.2 - 0}{0.2 - (-0.1)} = \tfrac23$, and the limited density is $0.2 + 0.2\xi$, with face values $0$ and $0.4$ and the same mean.

**Pressure by hand.** With $\gamma = 1.4$, take a cell mean $\bar u = (\rho, m, E) = (1, 0, 2.5)$, which has $p = 0.4\cdot 2.5 = 1$, and a point value $\hat u = (0.5, 1.5, 1)$, which has $p = 0.4(1 - 1.5^2/(2\cdot 0.5)) = -0.5$. Along $(1 - t)\bar u + t\hat u = (1 - 0.5t,\ 1.5t,\ 2.5 - 1.5t)$ the condition $p = 0$ is $(2.5 - 1.5t)(2 - t) = 2.25t^2$, that is $0.75t^2 + 5.5t - 5 = 0$, with root $t = (\sqrt{45.25} - 5.5)/1.5 \approx 0.8179$. So $\theta_2 \le 0.818$ for this cell, and with $\theta_2 = 0.8179$ the point value becomes about $(0.591, 1.227, 1.273)$, which has $p \approx 0$. With $\varepsilon > 0$ the root is slightly smaller.

**Typical tests.** The Sedov blast wave, the Leblanc shock tube with a pressure ratio of $10^9$, and the double rarefaction into near vacuum. Without the limiter a high-order DG or WENO scheme produces negative pressure in the first few steps on these problems. With the limiter and the reduced CFL number they run to the end.

## Variations

- **Maximum-principle-satisfying limiter** for scalar laws (Zhang and Shu 2010), the same scaling with the bounds of the initial data.
- **Bound-preserving limiters for other systems:** nonnegative water depth for shallow water (combined with [well-balanced](/well-balanced-scheme/) reconstruction), positive density for multicomponent and reactive flows, and bounds on mass fractions.
- **Parametrized flux limiters**, which limit the high-order flux toward a positive low-order flux instead of limiting the polynomial, and so allow the standard CFL number.
- **Positivity-preserving entropy stable schemes**, which combine the limiter with an [entropy stable](/entropy-stable-scheme/) flux.
- **Two and three dimensions.** On rectangles, tensor products of Gauss and Gauss-Lobatto points give the convex decomposition, and the CFL condition is the sum over directions.

## Pitfalls

- **Limiter without the CFL condition.** The limiter keeps the point values of the current state admissible, but the next means are admissible only for $\lambda a \le \hat w_1 c_0$, which is several times smaller than the usual DG step. Without it, negative means can still appear.
- **A flux that is not positive.** The proof needs a first-order flux that keeps $G$. With the Roe flux the scheme can fail near vacuum even with the limiter.
- **Too few points in $S_j$.** Checking only the Gauss points of the volume integral is not enough. The Gauss-Lobatto points, including the faces, must be in the set.
- **Solving the pressure equation badly.** $p((1 - t)\bar u + t\hat u) = \varepsilon$ is a quadratic equation in $t$ for the Euler equations. Take the root in $[0, 1]$; a crude bisection with few steps can leave a negative pressure.
- **Using a fixed $\varepsilon$ larger than the mean.** If $\bar\rho < \varepsilon$, the formula for $\theta_1$ is negative. Choose $\varepsilon$ below the cell means.
- **Confusing positivity with entropy stability or oscillation control.** The limiter does not remove oscillations; a TVB or WENO limiter is still needed at shocks.

## Exercises

1. For a scalar law with bounds $[0, 1]$ and a $P^2$ cell with point values $0.1, -0.05, 0.4$ at the Lobatto points $-1, 0, 1$, compute the mean and $\theta$.
2. Show that $p(u) = (\gamma - 1)(E - m^2/(2\rho))$ is concave on $\{\rho > 0\}$, and conclude that $\{\rho > 0, p > 0\}$ is convex.
3. Show that the Lax-Friedrichs scheme keeps $G = \{\rho > 0, p > 0\}$ for the Euler equations when $\lambda\max(|u| + c) \le 1$, using the convexity of $G$ and the exact solution of the Riemann problem.

## References
