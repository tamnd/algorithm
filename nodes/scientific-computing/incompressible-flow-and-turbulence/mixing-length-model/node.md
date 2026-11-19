---
tag: QA49H0
kind: model
slug: mixing-length-model
name: Prandtl mixing length model
aliases:
- mixing length model
area: scientific-computing/incompressible-flow-and-turbulence
level: intro
summary: An algebraic eddy viscosity equal to the square of a mixing length times the magnitude of the mean velocity gradient.
model: real-ram
history:
  year: 1925
  people: [Ludwig Prandtl, Theodore von Karman, Edward R. van Driest]
  note: Prandtl proposed the mixing length in 1925 by analogy with the mean free path of a gas. Von Karman and Prandtl derived the logarithmic law of the wall in the early 1930s, and van Driest added the damping factor near the wall in 1956.
prereqs: [boussinesq-eddy-viscosity]
see_also: [boussinesq-eddy-viscosity, wall-functions, k-epsilon-model, spalart-allmaras-model, smagorinsky-model, reynolds-averaged-navier-stokes, trapezoidal-rule]
sources:
  - paper: doi:10.1002/zamm.19250050212
    title: Ludwig Prandtl, Bericht über Untersuchungen zur ausgebildeten Turbulenz, Zeitschrift für Angewandte Mathematik und Mechanik 5(2), 1925, 136-139
    locator: the mixing length and the eddy viscosity proportional to its square times the velocity gradient
  - paper: doi:10.2514/8.3713
    title: E. R. van Driest, On turbulent flow near a wall, Journal of the Aeronautical Sciences 23(11), 1956, 1007-1011
    locator: the exponential damping factor with the constant A+ = 26
  - book: isbn:9780521598866
    title: Stephen B. Pope, Turbulent Flows, Cambridge University Press, 2000
    locator: Section 7.1.4 (mean velocity profiles and the log law), Section 7.1.7 (lengthscales and the mixing length) and Section 10.2.2 (the mixing-length model)
  - book: isbn:9781928729082
    title: David C. Wilcox, Turbulence Modeling for CFD, third edition, DCW Industries, 2006
    locator: Chapter 3 (algebraic models, the mixing length and the van Driest damping)
---

The Prandtl mixing length model is an algebraic turbulence closure that sets the eddy viscosity to $\nu_t = \ell_m^2 |dU/dy|$, where $\ell_m$ is a prescribed mixing length and $dU/dy$ is the mean velocity gradient. It is the simplest way to apply the [Boussinesq hypothesis](/boussinesq-eddy-viscosity/) to the [Reynolds-averaged Navier-Stokes equations](/reynolds-averaged-navier-stokes/): it needs no extra transport equation, only a rule for $\ell_m$, such as $\ell_m = \kappa y$ near a wall. The [k-epsilon](/k-epsilon-model/), [k-omega](/k-omega-model/), [SST](/k-omega-sst-model/) and [Spalart-Allmaras](/spalart-allmaras-model/) models replace the prescribed length by transported quantities. The model predicts the logarithmic law of the wall, which [wall functions](/wall-functions/) then use.

## The machine

**Setting.** A thin shear flow with mean velocity $U(y)$ along a wall at $y = 0$, kinematic viscosity $\nu$ (m^2/s), and total shear stress $\tau(y)$ per unit density. The wall stress is $\tau_w$, the friction velocity is $u_\tau = \sqrt{\tau_w/\rho}$, and wall units are $y^+ = u_\tau y / \nu$, $U^+ = U/u_\tau$, $\tau^+ = \tau/(\rho u_\tau^2)$.

**Closure.** The Reynolds shear stress is
$$-\langle u'v' \rangle = \nu_t \frac{dU}{dy}, \qquad \nu_t = \ell_m^2 \left|\frac{dU}{dy}\right|.$$

**Mixing length.** The model needs a rule for $\ell_m$. Near a wall:

- $\ell_m = \kappa y$, with the von Karman constant $\kappa \approx 0.41$;
- with van Driest damping, $\ell_m = \kappa y\left(1 - e^{-y^+/A^+}\right)$, with $A^+ = 26$, which makes $\nu_t$ fall off like $y^4$ near the wall instead of $y^2$.

In the outer part of a boundary layer, or in a free shear flow such as a jet or a wake, $\ell_m$ is a fixed fraction of the local layer width.

**Parameters.** $\kappa$ and $A^+$ are fitted to measured mean velocity profiles; the outer fraction is fitted per flow type. What is derived: the form $\ell^2|dU/dy|$ follows from dimensional reasoning once one length is given, and the log law follows from the model with no further input.

**Equation in wall units.** In the layer near a wall the mean momentum balance reduces to $(\nu + \nu_t)\, dU/dy = \tau$, or
$$(1 + \ell^{+2} |g|)\, g = \tau^+, \qquad g = \frac{dU^+}{dy^+}.$$
This is a quadratic in $g$ with one root of the sign of $\tau^+$:
$$g = \frac{2\tau^+}{1 + \sqrt{1 + 4\ell^{+2}|\tau^+|}}.$$
This form avoids the loss of digits of the textbook root $(-1 + \sqrt{\cdots})/(2\ell^{+2})$ when $\ell^+$ is small. Integrating $g$ from the wall with $U^+(0) = 0$ gives the profile. For a constant stress layer $\tau^+ = 1$; for a channel of half-height $\delta$, the exact balance of the [RANS](/reynolds-averaged-navier-stokes/) page gives $\tau^+ = 1 - y^+/Re_\tau$ with $Re_\tau = u_\tau \delta/\nu$.

```pseudo id=main
MIXING-LENGTH-PROFILE(y_max, n, κ, A+, τ+(·))
L1  h ← y_max / n; U_0 ← 0
L2  for i ← 0 to n: y_i ← i h
L3      ℓ ← κ y_i (1 - exp(-y_i / A+))
L4      g_i ← 2 τ+(y_i) / (1 + sqrt(1 + 4 ℓ^2 |τ+(y_i)|))
L5  for i ← 1 to n:
L6      U_i ← U_(i-1) + h (g_(i-1) + g_i) / 2
L7  return y, U
```

Line L4 is the stable root of the local balance, and line L6 is the [trapezoidal rule](/trapezoidal-rule/), so the profile is second-order accurate in $h$ when $g$ is smooth. The cost is $O(n)$ operations in the real RAM.

## What it counts

The model gives the mean velocity profile $U(y)$, the eddy viscosity $\nu_t(y)$ and the Reynolds shear stress, and from the profile the skin friction: the relation between $u_\tau$ and the velocity at a given height or the bulk velocity. It gives no turbulent kinetic energy and no normal stresses.

## Relation to other models

- **Closure hypothesis.** The model is the [Boussinesq hypothesis](/boussinesq-eddy-viscosity/) with the velocity scale $\ell_m |dU/dy|$ and the length scale $\ell_m$.
- **Two-layer algebraic models.** The Cebeci-Smith and Baldwin-Lomax models use the damped mixing length near the wall and a different outer formula, and were standard in aerodynamics before one- and two-equation models.
- **Transport models.** The [k-epsilon model](/k-epsilon-model/) computes the length $k^{3/2}/\varepsilon$ instead of prescribing it, and in a log layer in equilibrium it reduces to a mixing length $\kappa y$. The [Spalart-Allmaras model](/spalart-allmaras-model/) carries the eddy viscosity itself.
- **Wall functions.** [Wall functions](/wall-functions/) take the log law that this model predicts and impose it as a boundary condition for the other models.
- **LES.** The [Smagorinsky model](/smagorinsky-model/) is a mixing length model for the subgrid scales, with $\ell = C_s \Delta$ set by the grid size and $|dU/dy|$ replaced by the magnitude of the resolved strain rate.

## Known results in the model

**Viscous sublayer (exact in the model).** As $y^+ \to 0$, $\ell^+ \to 0$ and $g \to \tau^+ = 1$, so $U^+ = y^+$ to first order.

**Log law (prediction of the model).** For $y^+ \gg 1$ with $\tau^+ = 1$ and $\ell^+ = \kappa y^+$, the viscous term is small and $(\kappa y^+ g)^2 = 1$, so
$$U^+ = \frac{1}{\kappa}\ln y^+ + B.$$
The slope $1/\kappa$ comes out of the model. The constant $B$ depends on what happens near the wall, where the model has no physics, so it must be fitted.

**Closed form with no damping (exact).** With $\ell^+ = \kappa y^+$ and $\tau^+ = 1$ the integral can be done:
$$U^+(y^+) = \frac{1}{\kappa}\operatorname{asinh}(2\kappa y^+) - \frac{\sqrt{1 + 4\kappa^2 y^{+2}} - 1}{2\kappa^2 y^+}.$$
For large $y^+$ it gives $B = (\ln(4\kappa) - 1)/\kappa = -1.232$ at $\kappa = 0.41$. Values to check with a calculator: $U^+(1) = 0.953$, $U^+(10) = 4.672$, $U^+(100) = 10.029$, $U^+(1000) = 15.619$. For example at $y^+ = 10$, $2\kappa y^+ = 8.2$ and $\operatorname{asinh}(8.2) = \ln(8.2 + \sqrt{68.24}) = 2.801$, so the first term is $2.801/0.41 = 6.832$; the second is $(\sqrt{68.24} - 1)/3.362 = 2.160$; and $U^+ = 4.672$.

**Van Driest damping (computed, checked by the tests).** With $A^+ = 26$ and $\kappa = 0.41$, numerical integration gives $U^+(5) = 4.88$, $U^+(10) = 8.42$, $U^+(30) = 13.19$, and $U^+ - \ln(y^+)/\kappa = 5.30$, $5.29$ and $5.28$ at $y^+ = 100$, $300$ and $1000$. So the damped model has $B \approx 5.28$. Measured values of $B$ are about 5.0 to 5.2, and the value 26 of $A^+$ was chosen to make the model fit them: the agreement is a fit, not a prediction.

**Eddy viscosity by hand.** In air, 1 cm from a wall where $dU/dy = 50$ 1/s, the undamped model gives $\ell_m = 0.41 \times 0.01 = 0.0041$ m and $\nu_t = 0.0041^2 \times 50 = 8.4 \times 10^{-4}$ m^2/s, about 56 times the molecular value $1.5 \times 10^{-5}$ m^2/s.

**Channel flow (computed).** With $\tau^+ = 1 - y^+/Re_\tau$ at $Re_\tau = 180$, the profile lies below the constant-stress one, and $\nu_t = 0$ at the centerline because $dU/dy = 0$ there. Measurements and [DNS](/direct-numerical-simulation/) show a finite eddy viscosity at the centerline, so this zero is a known defect of the model.

**Agreement with experiment (measurement).** For attached boundary layers in weak pressure gradients, mixing length models with fitted outer constants give skin friction close to measurements. They do poorly for separated flows and for flows whose turbulence is not in local equilibrium, because $\nu_t$ responds instantly to the local gradient.

## References
