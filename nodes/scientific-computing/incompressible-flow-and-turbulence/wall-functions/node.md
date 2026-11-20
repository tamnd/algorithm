---
tag: 7MSEKR
kind: technique
slug: wall-functions
name: Wall functions
aliases:
- log-law wall function
area: scientific-computing/incompressible-flow-and-turbulence
level: core
summary: "Replace the resolution of the thin near-wall layer by the logarithmic law of the wall, which gives the wall shear stress from the first cell velocity."
model: real-ram
history:
  year: 1974
  people: [Brian Launder, Dudley Brian Spalding, Theodore von Karman, Ludwig Prandtl]
  note: The log law of the wall goes back to Prandtl and von Karman around 1930. Launder and Spalding made it a boundary condition for the k-epsilon model in 1974, and Spalding had given a single formula for the whole inner layer in 1961.
prereqs: [mixing-length-model, k-epsilon-model]
see_also: [k-epsilon-model, mixing-length-model, k-omega-model, reynolds-averaged-navier-stokes, boundary-conditions, newton-raphson-method, bisection-method, large-eddy-simulation]
sources:
  - paper: doi:10.1016/0045-7825(74)90029-2
    title: B. E. Launder and D. B. Spalding, The numerical computation of turbulent flows, Computer Methods in Applied Mechanics and Engineering 3(2), 1974, 269-289
    locator: the wall functions for the momentum, k and epsilon equations, with u* = C_mu^(1/4) k^(1/2)
  - paper: doi:10.1115/1.3641728
    title: D. B. Spalding, A single formula for the law of the wall, Journal of Applied Mechanics 28(3), 1961, 455-458
    locator: the formula for y+ as a function of u+ that covers the sublayer, the buffer layer and the log layer
  - book: isbn:9780521598866
    title: Stephen B. Pope, Turbulent Flows, Cambridge University Press, 2000
    locator: Section 7.1.4 (mean velocity profiles, the viscous sublayer and the log law), Section 7.3 (boundary layers) and Section 11.7.6 (wall functions)
  - book: isbn:9781928729082
    title: David C. Wilcox, Turbulence Modeling for CFD, third edition, DCW Industries, 2006
    locator: Chapter 4 (two-equation models, the surface boundary conditions and wall functions)
---

Wall functions are boundary conditions for turbulence models that replace the resolution of the viscous sublayer and the buffer layer next to a wall by the logarithmic law of the wall: from the mean velocity at the first grid point they give the wall shear stress and the values of the turbulence variables there. They close the gap between the [Reynolds-averaged Navier-Stokes equations](/reynolds-averaged-navier-stokes/) with a [Boussinesq](/boussinesq-eddy-viscosity/) closure and the wall, mostly for the [k-epsilon model](/k-epsilon-model/), which is not valid in the sublayer. The log law they impose is the one the [mixing length model](/mixing-length-model/) predicts, with constants fitted to measurements. The [k-omega](/k-omega-model/), [SST](/k-omega-sst-model/) and [Spalart-Allmaras](/spalart-allmaras-model/) models can instead be integrated to the wall on a fine grid.

## In plain words

Right next to a wall, the flow changes very fast over a very thin layer. Resolving that layer would need many tiny cells, often more than the rest of the domain. Measurements show that the velocity in this layer follows a nearly universal profile, once distance and speed are scaled by the wall friction. A wall function uses that profile as a shortcut. The first grid point is placed outside the thin layer. Its velocity and its distance from the wall are fed into the known profile, which is solved for the friction at the wall. That friction is then applied as a force on the flow. The same profile also gives the turbulence level at the first point. The shortcut is good when the flow is attached and calm along the wall, and poor where it separates.

## When it applies

- The wall-adjacent cell center is in the log layer. Wall units are $y^+ = u_\tau y/\nu$, $u^+ = U/u_\tau$, with $u_\tau = \sqrt{\tau_w/\rho}$, $\nu$ the kinematic viscosity (m^2/s) and $\tau_w$ the wall shear stress (Pa). The usual range for the first point is $30 \lesssim y^+ \lesssim 300$; this is a rule of thumb, and the upper limit grows with the Reynolds number because the log layer reaches out to about a tenth or a fifth of the boundary layer thickness.
- The near-wall flow is close to local equilibrium: production of turbulence about equal to dissipation, a weak pressure gradient, and no separation in the cell.
- The Reynolds number is high, so that the log layer is wide enough to hold the first point.
- It does not apply where $\tau_w$ changes sign (separation and reattachment), in strong pressure gradients, in low Reynolds number or transitional flows, or where wall heat transfer must be accurate.

## The template

**Laws (fitted to measurement).** The viscous sublayer has $u^+ = y^+$ (exact as $y^+ \to 0$). The log layer has
$$u^+ = \frac{1}{\kappa}\ln y^+ + B, \qquad \kappa \approx 0.41, \quad B \approx 5.0 \text{ to } 5.2.$$
The form of the log law follows from matching arguments and from the mixing length model; $\kappa$ and $B$ are measured. The two laws cross at $y^+_c$ with $y^+_c = \ln(y^+_c)/\kappa + B$, which is $11.06$ for $\kappa = 0.41$ and $B = 5.2$.

**Friction velocity from the first point.** Given the tangential velocity $U_P$ at distance $y_P$, solve $U_P = u_\tau\, u^+(y_P u_\tau/\nu)$ for $u_\tau$. On the log branch $f(u) = u\left(\frac{1}{\kappa}\ln\frac{y_P u}{\nu} + B\right) - U_P$ is increasing and convex, so [Newton's method](/newton-raphson-method/) started from the laminar value converges after one overshoot.

```pseudo id=main
WALL-FUNCTION(U_P, y_P, ν, κ, B)
L1  y_c ← root of y = ln(y)/κ + B
L2  u ← sqrt(ν U_P / y_P)                       (laminar value)
L3  if y_P u / ν ≤ y_c: return u                 (first point in the sublayer)
L4  repeat
L5      s ← ln(y_P u / ν)/κ + B; f ← u s - U_P
L6      u ← u - f / (s + 1/κ)
L7  until |f| ≤ tol · U_P
L8  return u_τ = u, τ_w = ρ u^2
```

**Use in the solver.**

1. Apply $\tau_w$ as the shear force on the wall face of the first cell, in place of $\rho\nu\,\partial U/\partial y$ from the grid, which would be far too small.
2. For the [k-epsilon model](/k-epsilon-model/): set zero flux of $k$ through the wall, use the wall-function stress in the production term of the first cell, and fix $\varepsilon_P = u_\tau^3/(\kappa y_P)$. In equilibrium $k_P = u_\tau^2/\sqrt{C_\mu}$.
3. For the [k-omega model](/k-omega-model/): fix $\omega_P = u_\tau/(\sqrt{C_\mu}\kappa y_P)$.
4. Recompute $u_\tau$ every outer iteration of the flow solver, since $U_P$ changes.

**Launder-Spalding form.** Launder and Spalding take the velocity scale from $k_P$ instead: $u^* = C_\mu^{1/4}k_P^{1/2}$, $y^* = u^* y_P/\nu$, and
$$\frac{\tau_w}{\rho} = \frac{\kappa\, u^* U_P}{\ln(E y^*)}, \qquad E = e^{\kappa B}.$$
This needs no iteration, and $u^*$ stays positive at separation and reattachment points where $U_P$ and $u_\tau$ go to zero. In equilibrium $u^* = u_\tau$ and the two forms agree exactly, which the tests check.

## Classic examples

**Air over a plate (by hand).** Take $\nu = 1.5 \times 10^{-5}$ m^2/s, $\rho = 1.2$ kg/m^3, $U_P = 10$ m/s at $y_P = 1$ mm, with $\kappa = 0.41$ and $B = 5.2$. The Newton iterates are:

| step | $u$ (m/s) | $y^+$ | $f$ (m/s) |
|---|---|---|---|
| 0 | 0.387298 | 25.82 | -4.9149 |
| 1 | 0.702992 | 46.87 | 0.2522 |
| 2 | 0.688177 | 45.88 | 0.00038 |
| 3 | 0.688155 | 45.877 | 0.0 |

So $u_\tau = 0.6882$ m/s, $y^+ = 45.9$ (inside the 30 to 300 range), $\tau_w/\rho = 0.4736$ m^2/s^2 and $\tau_w = 0.568$ Pa. Check: $\ln(45.877)/0.41 + 5.2 = 14.532$ and $0.688155 \times 14.532 = 10.000$. The wall values for k-epsilon are $k_P = 0.4736/0.3 = 1.579$ m^2/s^2 and $\varepsilon_P = 0.6882^3/(0.41 \times 0.001) = 795$ m^2/s^3. The laminar value 0.387 m/s would give a wall stress 3.2 times too small.

**Spalding's law.** Spalding's formula
$$y^+ = u^+ + e^{-\kappa B}\left(e^{\kappa u^+} - 1 - \kappa u^+ - \frac{(\kappa u^+)^2}{2} - \frac{(\kappa u^+)^3}{6}\right)$$
gives $y^+$ as an increasing function of $u^+$ that is $u^+$ in the sublayer and tends to the log law far out, with a smooth buffer layer between. With $\kappa = 0.41$ and $B = 5.2$: $u^+(1) = 1.000$, $u^+(11) = 8.83$ (the two-law value is 11.00 from the linear law, since $11 < 11.06$; the log law alone gives 11.05), $u^+(30) = 12.79$ and $u^+(300) = 19.07$ against the log law's 19.11. Inverting it by [bisection](/bisection-method/) gives a wall function valid at any $y^+$.

## Variations

- **Scalable wall functions.** Use $\max(y^*, y^+_c)$ in place of $y^*$, so that a first point that falls into the sublayer is treated as if it sat at the crossover. This stops the results from getting worse when the grid is refined.
- **Automatic or blended wall treatment.** Blend the sublayer and log-law values of $\tau_w$ and $\omega$, or use Spalding's law, so the same boundary condition works for any $y^+$. SST codes often do this.
- **Rough walls.** Lower $B$ by a function $\Delta B(k_s^+)$ of the roughness height in wall units.
- **Thermal wall functions.** A log law for the temperature, with a turbulent Prandtl number near 0.85 and an extra term that depends on the molecular Prandtl number, gives the wall heat flux.
- **Non-equilibrium wall functions.** Include the pressure gradient and use $k_P$ from its own transport equation, to do better near separation.
- **Wall models for LES.** Wall-modeled [large eddy simulation](/large-eddy-simulation/) uses the same idea, with the instantaneous filtered velocity at the first point.

## Pitfalls

- **First point in the buffer layer.** For $5 \lesssim y^+ \lesssim 30$ neither the linear law nor the log law holds well, and the wall stress is in error.
- **Refining the grid makes it worse.** With standard wall functions, a finer near-wall grid pushes $y^+$ into the sublayer, where the log law is wrong. Wall functions are not grid-converged in the usual sense; use scalable or blended forms, or a low Reynolds number model.
- **Separation.** Where $U_P \to 0$ the log law gives $u_\tau \to 0$ and $\varepsilon_P \to 0$, while the real turbulence there is not small. The Launder-Spalding form with $u^*$ from $k_P$ avoids the zero but not the error.
- **Wrong production in the first cell.** Computing $\mathcal P$ from the grid velocity gradient in the first cell, instead of from $\tau_w$ and the log-law gradient $u_\tau/(\kappa y_P)$, gives too little $k$ there.
- **Using $y^+$ to choose the grid before the solution exists.** Estimate $u_\tau$ from a skin-friction correlation, then check $y^+$ after the run.

## Exercises

1. Water ($\nu = 10^{-6}$ m^2/s) has $u_\tau = 0.05$ m/s. Where must the first cell center be to lie at $y^+ = 50$? (Answer: $y = 50 \times 10^{-6}/0.05 = 1$ mm.)
2. For $\kappa = 0.41$ and $B = 5.2$, show that $y^+ = 11.06$ is where the linear law and the log law meet. (Answer: $\ln(11.06)/0.41 + 5.2 = 2.4034/0.41 + 5.2 = 11.06$.)
3. Show that the Launder-Spalding stress equals $\rho u_\tau^2$ when $k_P = u_\tau^2/\sqrt{C_\mu}$ and $U_P$ follows the log law. (Answer: then $u^* = u_\tau$, $y^* = y^+$, and $\kappa U_P/u_\tau = \ln y^+ + \kappa B = \ln(E y^+)$.)

## References
