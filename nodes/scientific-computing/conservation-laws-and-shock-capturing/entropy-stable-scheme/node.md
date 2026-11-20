---
tag: 0A1T0M
kind: technique
slug: entropy-stable-scheme
name: Entropy stable schemes
aliases:
- entropy conservative flux
area: scientific-computing/conservation-laws-and-shock-capturing
level: research
summary: "Schemes whose flux is an entropy conservative flux in Tadmor's sense plus dissipation in the entropy variables, so the discrete solution obeys an entropy inequality for every mesh."
prereqs: [hyperbolic-conservation-law, lax-entropy-condition, finite-volume-method]
see_also: [summation-by-parts-operators, discontinuous-galerkin-method, rusanov-flux, roe-solver, harten-hyman-entropy-fix, weno-scheme, euler-equations-of-gas-dynamics, burgers-equation]
sources:
  - paper: "Eitan Tadmor, The numerical viscosity of entropy stable schemes for systems of conservation laws. I, Mathematics of Computation 49(179) (1987) 91-103"
    locator: entropy conservative fluxes, the comparison of numerical viscosities, entropy stability of three-point schemes
  - paper: "Eitan Tadmor, Entropy stability theory for difference approximations of nonlinear conservation laws and related time-dependent problems, Acta Numerica 12 (2003) 451-512"
    locator: the survey of the theory, entropy variables, the path integral form of the entropy conservative flux
  - paper: doi:10.1137/110836961
    title: Ulrik S. Fjordholm, Siddhartha Mishra and Eitan Tadmor, Arbitrarily high-order accurate entropy stable essentially nonoscillatory schemes for systems of conservation laws, SIAM Journal on Numerical Analysis 50(2) (2012) 544-573
    locator: high-order entropy conservative fluxes, the sign property of ENO reconstruction, the TeCNO schemes
  - paper: doi:10.1016/j.jcp.2009.04.021
    title: "Farzad Ismail and Philip L. Roe, Affordable, entropy-consistent Euler flux functions II: entropy production at shocks, Journal of Computational Physics 228(15) (2009) 5410-5436"
    locator: an entropy conservative flux for the Euler equations in closed form, with logarithmic means
---

An entropy stable scheme is a conservative scheme for a hyperbolic system $u_t + f(u)_x = 0$ that satisfies a discrete form of the entropy inequality $U(u)_t + q(u)_x \le 0$ on every mesh, not only in the limit. The construction, due to Tadmor (1987), has two parts. The first is an entropy conservative two-point flux $F^*$, defined by the condition $(v_R - v_L)\cdot F^* = \psi_R - \psi_L$, where $v = U'(u)$ are the entropy variables and $\psi = v\cdot f - q$ is the entropy potential. With $F^*$ the semi-discrete scheme conserves the total entropy exactly. The second part adds dissipation in the entropy variables, $F = F^* - \tfrac12 D(v_R - v_L)$ with $D$ symmetric positive semidefinite, which makes the total entropy decrease at a known rate. The same idea, with [summation-by-parts](/summation-by-parts-operators/) operators, gives entropy stable [DG](/discontinuous-galerkin-method/) and spectral element methods of high order.

## In plain words

Physical flows with shocks lose a quantity called entropy (in the mathematical sign convention used here) and never gain it. Many good schemes can still gain it in rare cases and then compute a wrong solution or blow up. An entropy stable scheme is built so that this cannot happen. First it uses a special flux between two cells, chosen so that the scheme moves entropy around without creating or destroying any. That flux alone is too clean: at a shock it produces large wiggles, because the entropy has nowhere to go. So a second, small term is added that can only remove entropy, and that is largest where neighbouring cells differ the most. The result is a scheme whose entropy is guaranteed to go down, with a rate you can compute.

## When it applies

- The system has a convex entropy $U(u)$ with entropy flux $q(u)$, $q' = U'f'$. Most systems from physics have one: the Euler equations ($U = -\rho s/(\gamma - 1)$ with $s$ the specific entropy), the [shallow water equations](/shallow-water-equations/) (the total energy), MHD and the scalar laws ($U = u^2/2$ for Burgers).
- The scheme is in conservation form, so it can be written with face fluxes.
- You want robustness that does not depend on tuning: under-resolved turbulence, long runs, strong shocks, high order schemes that are unstable because of aliasing.

Entropy stability is a semi-discrete property. A fully discrete scheme keeps it only with an entropy stable time integrator; with explicit Runge-Kutta methods the error in the entropy is $O(\Delta t^{p})$ and is usually much smaller than the dissipation.

## The template

On a periodic grid with cells $C_j$ of width $\Delta x$ and averages $u_j$, write $v_j = U'(u_j)$ and $\psi_j = v_j\cdot f(u_j) - q(u_j)$.

```pseudo id=main
ENTROPY-STABLE-SCHEME(u, Δx)
L1  choose a convex entropy pair (U, q); set v ← U'(u) and ψ ← v·f(u) - q(u)
L2  pick an entropy conservative flux F* with (v_R - v_L)·F* = ψ_R - ψ_L
L3  F_(j+1/2) ← F*(u_j, u_(j+1)) - ½ D_(j+1/2) (v_(j+1) - v_j),  D symmetric, D ≥ 0
L4  du_j/dt ← -(F_(j+1/2) - F_(j-1/2)) / Δx; advance in time with an SSP Runge-Kutta method
```

The key identity is discrete summation by parts. On a periodic grid,

$$\frac{d}{dt}\sum_j U(u_j)\,\Delta x = \sum_j v_j\cdot\frac{du_j}{dt}\,\Delta x = \sum_j (v_{j+1} - v_j)\cdot F_{j+1/2}.$$

With $F = F^*$ each term is $\psi_{j+1} - \psi_j$, and the sum telescopes to $0$. With the dissipation of L3 the sum is $-\tfrac12\sum_j (v_{j+1} - v_j)^{T}D_{j+1/2}(v_{j+1} - v_j) \le 0$ (theorem). On a nonperiodic grid the boundary terms remain, and boundary conditions must be chosen so they have the right sign.

Tadmor's path integral gives one entropy conservative flux for any system: $F^* = \int_0^1 f\big(u(v_L + \theta(v_R - v_L))\big)\,d\theta$. It is exact but needs quadrature, so practical schemes use closed forms such as the Ismail-Roe flux for the Euler equations, built from logarithmic means of the density and of $\rho/p$. A common choice for $D$ is the largest wave speed times the matrix $\partial u/\partial v$, a Rusanov-type dissipation, or a Roe-type matrix $R|\Lambda|R^T$ with scaled eigenvectors.

## Classic examples

- [Godunov's method](/godunov-method/): its flux is an E-flux, so it is entropy stable, and it can be written as the entropy conservative flux plus a nonnegative dissipation (exercise 2).
- [Burgers' equation](/burgers-equation/): the simplest case, worked out below, with $v = u$ and a quadratic entropy conservative flux.
- [Shallow water equations](/shallow-water-equations/): the total energy is the entropy, and the entropy conservative flux uses arithmetic means only (exercise 1).
- [Euler equations](/euler-equations-of-gas-dynamics/): the Ismail-Roe flux with logarithmic means, plus matrix dissipation.
- [Discontinuous Galerkin method](/discontinuous-galerkin-method/): flux differencing with a two-point entropy conservative flux on Gauss-Lobatto nodes gives entropy stable DG of any order.

**Burgers' equation by hand.** For $f(u) = u^2/2$ take $U = u^2/2$, so $v = u$, $q = u^3/3$ and $\psi = u\cdot\tfrac{u^2}{2} - \tfrac{u^3}{3} = \tfrac{u^3}{6}$. The condition $(u_R - u_L)F^* = (u_R^3 - u_L^3)/6$ gives

$$F^*(u_L, u_R) = \frac{u_L^2 + u_Lu_R + u_R^2}{6},$$

which is also Tadmor's path integral $\int_0^1 \tfrac12(u_L + \theta(u_R - u_L))^2\,d\theta$. For $u_L = 1$, $u_R = 0$: $F^* = \tfrac16$, and indeed $(0 - 1)\cdot\tfrac16 = \tfrac{0 - 1}{6}$. With $D = \max(|u_L|, |u_R|) = 1$ the entropy stable flux is $\tfrac16 + \tfrac12 = \tfrac23$, and this face removes entropy at the rate $\tfrac12\cdot 1\cdot 1^2 = \tfrac12$. The arithmetic mean $\tfrac12(f(u_L) + f(u_R)) = \tfrac14$ is not entropy conservative: it does not satisfy the condition.

**A shock forms (measurement).** Burgers with $u_0 = \sin 2\pi x$ on $[0, 1]$, 100 cells, SSP-RK3 with $\Delta t = 0.2\,\Delta x$. A shock forms at $t = 1/(2\pi) \approx 0.16$. Total entropy $\sum_j \tfrac12 u_j^2\,\Delta x$, initially $0.25$, and the largest $|u_j|$:

| $t$ | EC: entropy | EC: $\max|u|$ | ES: entropy | ES: $\max|u|$ |
|---|---|---|---|---|
| 0.1 | 0.250000 | 0.9999 | 0.245215 | 0.9813 |
| 0.3 | 0.249998 | 1.8220 | 0.170048 | 0.9197 |
| 0.5 | 0.249997 | 1.5339 | 0.092046 | 0.7053 |

The entropy conservative scheme keeps the total entropy to about $3\times 10^{-6}$, the error of the time integrator, so after the shock it has no way to lose the entropy the exact solution loses, and it puts that energy into oscillations with values far outside the initial range. The entropy stable scheme decays as the exact solution does and keeps $|u| \le 1$. Before the shock, at $T = 0.2$ with $u_0 = \tfrac12 + \tfrac14\sin 2\pi x$ on 64 cells, the entropy error of the EC scheme with SSP-RK3 is $1.19\times 10^{-8}$, $1.49\times 10^{-9}$ and $1.86\times 10^{-10}$ for $\Delta t/\Delta x = 0.4, 0.2, 0.1$: a factor 8 per halving, third order in $\Delta t$.

**Euler equations.** Ismail and Roe (2009) give an entropy conservative flux for the Euler equations in closed form, with the entropy $U = -\rho s/(\gamma - 1)$. Adding a matrix dissipation built from the eigenvectors of the Jacobian, scaled so that $D = R|\Lambda|R^{T}$ acts on the entropy variables, gives an entropy stable flux that behaves like the Roe flux but has no entropy violating expansion shocks.

## Variations

- **TeCNO schemes** (Fjordholm, Mishra and Tadmor 2012). High-order entropy conservative fluxes made from linear combinations of two-point fluxes, plus dissipation applied to ENO reconstructions of the scaled entropy variables. The sign property of ENO makes the dissipation entropy stable at any order.
- **Entropy stable DG and spectral element methods.** Flux differencing with a two-point entropy conservative flux inside each element, written with [summation-by-parts](/summation-by-parts-operators/) operators on Gauss-Lobatto nodes, gives a discrete entropy inequality for any polynomial degree.
- **Kinetic energy preserving fluxes**, which also keep the discrete kinetic energy balance for the Euler equations and are popular in turbulence simulation.
- **Entropy stable time integration.** Relaxation Runge-Kutta methods change the step length slightly so that the fully discrete entropy satisfies the inequality too.
- **Entropy fixes** such as the [Harten-Hyman fix](/harten-hyman-entropy-fix/) for the Roe flux are a weaker, local remedy: they remove expansion shocks but do not give a global inequality.

## Pitfalls

- **Entropy conservative alone at shocks.** Without dissipation the scheme oscillates at every shock, as in the table. The EC flux is the base, not the scheme.
- **Dissipation in the wrong variables.** The dissipation must act on the jump of $v$ with a positive semidefinite matrix. Adding $-\tfrac12\lambda(u_R - u_L)$ in conserved variables is entropy stable for Burgers, where $v = u$, but not in general for systems.
- **Path integral by quadrature.** A crude quadrature of Tadmor's integral breaks the identity $(v_R - v_L)\cdot F^* = \psi_R - \psi_L$. Use a closed form, or enough points for the integrand.
- **Logarithmic means near equal states.** The Ismail-Roe flux uses $(a - b)/(\ln a - \ln b)$, which loses accuracy when $a \approx b$. Use the series expansion there.
- **Entropy stability is not positivity.** An entropy stable Euler scheme can still produce negative density or pressure near vacuum, where the entropy variables are not defined. Combine it with a [positivity-preserving limiter](/positivity-preserving-limiter/).
- **Expecting accuracy.** Entropy stability is a stability property. It does not make a first-order scheme accurate, and it does not prevent small oscillations of higher order schemes.

## Exercises

1. For the shallow water equations with entropy $U = \tfrac12 hu^2 + \tfrac12 gh^2$, compute $v$ and $\psi$ and check that $F^* = \big(\bar h\bar u,\ \bar h\bar u^2 + \tfrac{g}{2}\overline{h^2}\big)$, with bars for arithmetic means of the two states, is entropy conservative.
2. Show that for a scalar law with $U = u^2/2$ every flux of the form $F = F^* - \tfrac12 d\,(u_R - u_L)$ with $d \ge 0$ is entropy stable, and that Godunov's flux for Burgers is of this form with $d \ge 0$.
3. Prove that the semi-discrete entropy conservative scheme on a periodic grid also conserves $\sum_j u_j\,\Delta x$, and explain why both conservation laws together force oscillations after a shock forms.

## References
