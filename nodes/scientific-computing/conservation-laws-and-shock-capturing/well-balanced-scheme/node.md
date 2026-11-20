---
tag: DMAAHD
kind: technique
slug: well-balanced-scheme
name: Well-balanced schemes
aliases:
- hydrostatic reconstruction
area: scientific-computing/conservation-laws-and-shock-capturing
level: advanced
summary: "Schemes for balance laws that keep a family of steady states exactly, such as the lake at rest over a varying bottom, by discretizing flux gradient and source term so that they cancel."
model: floating-point-model
prereqs: [shallow-water-equations, finite-volume-method, godunov-method]
see_also: [positivity-preserving-limiter, rusanov-flux, hll-riemann-solver, euler-equations-of-gas-dynamics, discontinuous-galerkin-method, kurganov-tadmor-scheme, entropy-stable-scheme, hyperbolic-conservation-law]
sources:
  - paper: "Alfredo Bermúdez and M. Elena Vázquez, Upwind methods for hyperbolic conservation laws with source terms, Computers and Fluids 23(8) (1994) 1049-1071"
    locator: the upwind treatment of the source term and the exact conservation property (C-property) for the lake at rest
  - paper: doi:10.1137/S1064827503431090
    title: Emmanuel Audusse, François Bouchut, Marie-Odile Bristeau, Rupert Klein and Benoît Perthame, A fast and stable well-balanced scheme with hydrostatic reconstruction for shallow water flows, SIAM Journal on Scientific Computing 25(6) (2004) 2050-2065
    locator: the hydrostatic reconstruction, the proof that it keeps the lake at rest and nonnegative depths, the second-order extension
  - paper: "J. M. Greenberg and A. Y. LeRoux, A well-balanced scheme for the numerical processing of source terms in hyperbolic equations, SIAM Journal on Numerical Analysis 33(1) (1996) 1-16"
    locator: the name well-balanced and the treatment of the source at the cell faces
  - book: isbn:9780521009249
    title: Randall J. LeVeque, Finite Volume Methods for Hyperbolic Problems, Cambridge University Press, 2002
    locator: Chapter 17 (source terms and balance laws, quasi-steady problems)
---

A well-balanced scheme is a scheme for a balance law $u_t + f(u)_x = S(u, x)$ that keeps a chosen family of steady states $f(u)_x = S(u, x)$ exactly at the discrete level, not only up to the truncation error. The standard case is the [shallow water equations](/shallow-water-equations/) over a bottom $z(x)$, $h_t + (hu)_x = 0$ and $(hu)_t + (hu^2 + \tfrac12gh^2)_x = -ghz_x$, with the lake at rest $u = 0$, $h + z = \text{const}$. In that state the pressure gradient $(\tfrac12gh^2)_x$ and the bottom force $-ghz_x$ cancel. If they are discretized separately, their truncation errors do not cancel, and the scheme makes currents of size $O(\Delta x)$ in still water. These currents are often larger than the waves one wants to compute, such as a tsunami of 1 m over an ocean 4 km deep. Bermúdez and Vázquez (1994) called the exact preservation of the lake at rest the C-property, and Greenberg and LeRoux (1996) introduced the name well-balanced. The hydrostatic reconstruction of Audusse et al. (2004) is a simple and widely used way to make any positive finite volume solver well balanced, including at wet-dry fronts.

## In plain words

In a lake at rest over an uneven bottom, the water pushes sideways because it is deeper in some places, and the slope of the bottom pushes back by the same amount. Nothing moves. A computer program computes these two pushes with two different formulas, and the small errors in each formula do not cancel, so the program makes the still water flow. A well-balanced scheme computes the two pushes together, in a way that makes them cancel exactly when the water surface is flat. Then still water stays still, to the last digit of the computer arithmetic, and small real waves on top of it are not hidden by false currents.

## When it applies

- A hyperbolic system with a source term whose steady states are important or long-lived: shallow water over a bottom, gas in a gravitational field (hydrostatic atmospheres and stars), flow in a duct of varying area, chemical kinetics with equilibria.
- The perturbations to compute are small compared with the truncation error of the balance: tides, tsunamis, stellar oscillations, flood waves over complex topography.
- Long runs, where a spurious current of size $O(\Delta x)$ builds up into a false steady flow.
- Problems with dry regions, where the scheme must also keep $h \ge 0$, so the well-balanced method must work with a positive solver.

## The template

On cells $C_i$ with depth $h_i$, discharge $q_i = h_iu_i$ and bottom $z_i$, the hydrostatic reconstruction works as follows at each face $i + \tfrac12$, with any consistent flux $\mathcal F$ that keeps $h \ge 0$ (Rusanov, HLL, kinetic):

```pseudo id=main
HYDROSTATIC-RECONSTRUCTION-STEP(h, q, z, Δx, Δt, ℱ)
L1  for each face i+1/2 do z* ← max(z_i, z_(i+1))
L2      h*_L ← max(0, h_i + z_i - z*);  h*_R ← max(0, h_(i+1) + z_(i+1) - z*)
L3      F* ← ℱ((h*_L, h*_L u_i), (h*_R, h*_R u_(i+1)))
L4      F⁻ ← F* + (0, g/2 (h_i² - h*_L²));  F⁺ ← F* + (0, g/2 (h_(i+1)² - h*_R²))
L5  for each cell i do (h, q)_i ← (h, q)_i - (Δt/Δx)(F⁻_(i+1/2) - F⁺_(i-1/2))
```

**Walk-through.** L2 measures the depths from the higher of the two bottoms, so it reconstructs the water column that the two cells have in common. L3 evaluates the solver on these states. L4 gives each cell its own momentum flux: cell $i$ sees $F^-$ on its right face and cell $i + 1$ sees $F^+$ on its left face. The difference between $F^-$ and $F^+$ is the discrete bottom force at the face. The mass flux is the same on both sides, so mass is conserved exactly.

**Why the lake at rest is kept (theorem).** Let $u_i = 0$ and $h_i + z_i = \eta$ for every wet cell. If both cells at a face are wet and $\eta \ge z^*$, then $h^*_L = h^*_R = \eta - z^*$. The two reconstructed states are equal, so a consistent flux gives $F^* = (0, \tfrac g2 h^{*2})$ and $F^- = (0, \tfrac g2 h_i^2)$, $F^+ = (0, \tfrac g2 h_{i+1}^2)$. If one cell is dry with a bottom above $\eta$, both reconstructed depths are $0$, so $F^* = 0$ and again $F^- = (0, \tfrac g2 h_i^2)$. In every case cell $i$ sees $(0, \tfrac g2 h_i^2)$ on both of its faces, and its update is zero. In floating point the update is zero up to rounding, because $h_i + z_i - z^*$ and $\tfrac g2(h_i^2 - h^{*2}) + \tfrac g2h^{*2}$ are computed with rounding errors of a few units in the last place. Audusse et al. (2004) also prove that the scheme keeps $h \ge 0$ under the CFL condition of the solver and satisfies a semi-discrete entropy inequality.

## Classic examples

- [Shallow water equations](/shallow-water-equations/): the lake at rest over a bump and over an island, worked out below.
- [Euler equations](/euler-equations-of-gas-dynamics/) with gravity: the hydrostatic atmosphere $p_x = -\rho g$, kept by reconstructing $p$ relative to a local hydrostatic profile; this matters in astrophysics and weather codes.
- [Godunov's method](/godunov-method/) with an upwinded source: the approach of Bermúdez and Vázquez, which puts the source at the faces and splits it with the same upwinding as the flux.
- [Discontinuous Galerkin method](/discontinuous-galerkin-method/): high-order well-balanced DG uses the hydrostatic reconstruction at the faces and a matching quadrature of the source inside each cell.
- [Positivity-preserving limiter](/positivity-preserving-limiter/): with high-order schemes it keeps $h \ge 0$ at wet-dry fronts without breaking the balance.

**One face by hand.** Take $g = 9.81$, two cells with depths $h = (1, 0.5)$, bottoms $z = (0, 0.5)$ and no flow, so the surface is at 1 in both. Then $z^* = 0.5$ and $h^*_L = h^*_R = 0.5$, and the Rusanov flux of two equal states at rest is $F^* = (0, \tfrac g2\cdot 0.25) = (0, 1.22625)$. The left cell sees $F^- = (0, 1.22625 + 4.905\cdot 0.75) = (0, 4.905)$, which is $\tfrac g2 h_0^2$, and the right cell sees $F^+ = (0, 1.22625 + 0) = (0, 1.22625)$, which is $\tfrac g2 h_1^2$. With wall faces outside, both cells get zero updates. The plain Rusanov flux at the same face, with no reconstruction, has the mass flux $-\tfrac12 a(h_1 - h_0) = \tfrac12\sqrt{g}\cdot 0.5 \approx 0.783$, because its dissipation sees the jump in depth, and the scheme starts to move water.

**Lake at rest (measurement).** On $[0, 1]$ with walls, $g = 9.81$, surface level 1, forward Euler with Courant number 0.45, to $T = 0.5$. "Bump" is $z = 0.5e^{-50(x - 0.5)^2}$. "Island" is $z = \max(0, 1.2 - 40(x - 0.5)^2)$, which is dry for $|x - 0.5| < 0.071$. The naive scheme is the Rusanov flux with the centred source $-gh_i(z_{i+1} - z_{i-1})/(2\Delta x)$. Largest $|q|$ at $T$:

| cells | bump, naive | bump, hydrostatic | island, naive | island, hydrostatic |
|---|---|---|---|---|
| 50 | 1.020e-1 | 1.0e-15 | 4.231e-1 | 6.4e-16 |
| 100 | 4.874e-2 | 2.6e-15 | 1.985e-1 | 1.9e-16 |
| 200 | 2.303e-2 | 2.4e-15 | 9.718e-2 | 7.3e-16 |

The naive error is first order: it halves with $\Delta x$. The hydrostatic reconstruction keeps the lake at rest to rounding, with or without dry cells. With the naive scheme over the island, the largest error of the surface in the wet cells is 0.087, 0.039 and 0.021 for 50, 100 and 200 cells.

## Variations

- **Moving water equilibria.** The hydrostatic reconstruction keeps only $u = 0$. States with $hu = \text{const}$ and $\tfrac12u^2 + g(h + z) = \text{const}$ need reconstruction in those equilibrium variables.
- **Second and higher order.** Reconstruct $h + z$ (the surface) rather than $h$, then apply the hydrostatic step at the faces and add a centred source correction inside each cell.
- **Central-upwind schemes.** Well-balanced and positive versions of the [Kurganov-Tadmor](/kurganov-tadmor-scheme/) type schemes discretize the source to match the flux.
- **Wave-propagation methods.** LeVeque's quasi-steady approach puts the source into the Riemann problem at each face, so the source is balanced by a jump in the face states.
- **Entropy stable and well-balanced.** An energy conservative shallow water flux with a matching source discretization is both [entropy stable](/entropy-stable-scheme/) and well balanced.

## Pitfalls

- **Reconstructing $h$ instead of $h + z$.** A second-order slope limiter applied to $h$ breaks the balance. Reconstruct the surface elevation and recover $h$ from it.
- **Testing in exact arithmetic only.** The property holds to rounding in floating point. Check $|q|$ and $|h + z - \eta|$ against a tolerance of a few hundred ulps of $\tfrac g2h^2$, not against zero.
- **Dry cells.** Dividing by $h$ to get $u$ fails at $h = 0$. Set $u = 0$ for dry cells, or for $h$ below a small threshold.
- **Steep bottoms.** The hydrostatic reconstruction is consistent but can be inaccurate for large bottom jumps on coarse grids, because the reconstructed depths are clipped at 0.
- **Only one equilibrium.** A scheme balanced for the lake at rest is not balanced for steady flow over a bump; know which steady state matters for the problem.
- **Source at the cell centre with an upwind flux.** As the table shows, this standard approach makes spurious currents of order $\Delta x$, even though each part is consistent.

## Exercises

1. Show that the naive scheme of the table is consistent of first order, but that for the lake at rest its momentum update in a wet cell is $O(\Delta x)$ and not zero.
2. Show that the hydrostatic reconstruction keeps the total mass $\sum_i h_i\,\Delta x$ exactly on a grid with walls, in exact arithmetic.
3. For the Euler equations with gravity, $p_x = -\rho g$ with constant temperature gives $p = p_0e^{-x/H}$. Write a reconstruction that keeps this isothermal atmosphere exactly.

## References
