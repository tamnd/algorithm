---
tag: FJGR38
kind: model
slug: k-epsilon-model
name: "k-epsilon turbulence model"
aliases:
- standard k-epsilon model
area: scientific-computing/incompressible-flow-and-turbulence
level: core
summary: "Two transport equations, for turbulent kinetic energy k and its dissipation rate epsilon, give the eddy viscosity C k^2/epsilon."
model: real-ram
history:
  year: 1972
  people: [William P. Jones, Brian Launder, Dudley Brian Spalding, B. I. Sharma]
  note: Jones and Launder published the two-equation model with low Reynolds number terms in 1972. Launder and Sharma gave the constants now called standard in 1974, and Launder and Spalding paired the model with wall functions the same year.
prereqs: [boussinesq-eddy-viscosity]
see_also: [boussinesq-eddy-viscosity, k-omega-model, k-omega-sst-model, wall-functions, mixing-length-model, reynolds-averaged-navier-stokes, kolmogorov-1941-theory, classical-runge-kutta-4]
sources:
  - paper: doi:10.1016/0017-9310(72)90076-2
    title: W. P. Jones and B. E. Launder, The prediction of laminarization with a two-equation model of turbulence, International Journal of Heat and Mass Transfer 15(2), 1972, 301-314
    locator: the transport equations for k and epsilon, with damping terms for low Reynolds numbers
  - paper: doi:10.1016/0094-4548(74)90150-7
    title: B. E. Launder and B. I. Sharma, Application of the energy-dissipation model of turbulence to the calculation of flow near a spinning disc, Letters in Heat and Mass Transfer 1(2), 1974, 131-137
    locator: the standard constants C_mu = 0.09, C_1 = 1.44, C_2 = 1.92, sigma_k = 1.0, sigma_eps = 1.3
  - paper: doi:10.1016/0045-7825(74)90029-2
    title: B. E. Launder and D. B. Spalding, The numerical computation of turbulent flows, Computer Methods in Applied Mechanics and Engineering 3(2), 1974, 269-289
    locator: the model with its constants and the wall functions used with it
  - book: isbn:9780521598866
    title: Stephen B. Pope, Turbulent Flows, Cambridge University Press, 2000
    locator: Section 5.4.6 (grid turbulence), Section 10.3 (turbulent kinetic energy models) and Section 10.4 (the k-epsilon model, 10.4.2 the model equation for epsilon)
  - book: isbn:9781928729082
    title: David C. Wilcox, Turbulence Modeling for CFD, third edition, DCW Industries, 2006
    locator: Chapter 4 (two-equation models, the k-epsilon model and its closure coefficients)
---

The k-epsilon model is a two-equation closure of the [Reynolds-averaged Navier-Stokes equations](/reynolds-averaged-navier-stokes/) that solves transport equations for the turbulent kinetic energy $k$ and its dissipation rate $\varepsilon$, and sets the eddy viscosity to $\nu_t = C_\mu k^2/\varepsilon$. It uses the [Boussinesq hypothesis](/boussinesq-eddy-viscosity/) for the stresses, and, unlike the [mixing length model](/mixing-length-model/), it needs no prescribed length. Its five constants are fitted to simple flows. The [k-omega model](/k-omega-model/) carries $\omega = \varepsilon/(C_\mu k)$ instead and handles walls better, the [SST model](/k-omega-sst-model/) blends the two, and the standard form is used with [wall functions](/wall-functions/) because it is poor in the viscous sublayer.

## The machine

**Unknowns.** The mean velocity $U_i$ and pressure $P$, plus two scalar fields: $k$ (m^2/s^2) and $\varepsilon$ (m^2/s^3). The kinematic viscosity is $\nu$ (m^2/s).

**Equations.** With the Boussinesq stresses and the production $\mathcal P = 2\nu_t S_{ij}S_{ij}$,
$$\nu_t = C_\mu \frac{k^2}{\varepsilon},$$
$$\frac{Dk}{Dt} = \mathcal P - \varepsilon + \nabla\cdot\left[\left(\nu + \frac{\nu_t}{\sigma_k}\right)\nabla k\right],$$
$$\frac{D\varepsilon}{Dt} = C_1 \frac{\varepsilon}{k}\mathcal P - C_2 \frac{\varepsilon^2}{k} + \nabla\cdot\left[\left(\nu + \frac{\nu_t}{\sigma_\varepsilon}\right)\nabla\varepsilon\right],$$
where $D/Dt$ is the derivative following the mean flow.

**Parameters.** The standard constants of Launder and Sharma (1974) are all fitted, not derived:

| constant | value | fitted to |
|---|---|---|
| $C_\mu$ | 0.09 | the ratio $-\langle u'v' \rangle/k \approx 0.3$ measured in shear layers in equilibrium, which the model gives as $\sqrt{C_\mu}$ |
| $C_2$ | 1.92 | the decay of grid turbulence |
| $C_1$ | 1.44 | the growth of shear flows, chiefly homogeneous shear and free shear layers |
| $\sigma_k$ | 1.0 | a choice of order one |
| $\sigma_\varepsilon$ | 1.3 | the log law, through the relation for $\kappa$ below |

The $k$ equation is the exact one with its unclosed terms modeled by gradient diffusion. The $\varepsilon$ equation is a model built to look like the $k$ equation, not a model of the exact $\varepsilon$ equation term by term (Pope 10.4.2).

**Near walls.** The standard model is not valid in the viscous sublayer. It is used with [wall functions](/wall-functions/) that set $k$ and $\varepsilon$ at the first grid point, or in low Reynolds number forms with damping functions, such as the original Jones and Launder model.

**Decaying turbulence.** In homogeneous turbulence with no mean gradient, $\mathcal P = 0$ and the diffusion terms vanish, which leaves two ordinary differential equations. The procedure below integrates them with the [classical Runge-Kutta method](/classical-runge-kutta-4/).

```pseudo id=main
K-EPSILON-DECAY(k_0, ε_0, T, m, C_2)
L1  h ← T / m; (k, ε) ← (k_0, ε_0)
L2  f(k, ε) = (-ε, -C_2 ε^2 / k)
L3  for step ← 1 to m:
L4      a ← f(k, ε); b ← f((k, ε) + h a / 2); c ← f((k, ε) + h b / 2); d ← f((k, ε) + h c)
L5      (k, ε) ← (k, ε) + h (a + 2b + 2c + d) / 6
L6  return k, ε
```

Each step costs four evaluations of $f$, and the error at a fixed $T$ falls like $h^4$. In a full flow solver the two equations are discretized like the momentum equations, usually by the [finite volume method](/finite-volume-method/) with upwind convection, and the source terms are treated implicitly to keep $k$ and $\varepsilon$ positive.

## What it counts

The model gives the mean flow, $k$, $\varepsilon$, the eddy viscosity and the Reynolds stresses in the Boussinesq form. From $k$ and $\varepsilon$ it gives a turbulence time scale $k/\varepsilon$ and length scale $k^{3/2}/\varepsilon$, which are useful for mixing, heat transfer and combustion models.

## Relation to other models

- **Closure hypothesis.** It is a [Boussinesq](/boussinesq-eddy-viscosity/) closure, so it shares its limits: equal normal stresses in simple shear and no stress anisotropy.
- **Mixing length.** In an equilibrium log layer the model gives $\nu_t = \kappa u_\tau y$, which is the [mixing length model](/mixing-length-model/) with $\ell_m = \kappa y$.
- **k-omega.** The substitution $\omega = \varepsilon/(C_\mu k)$ turns the model into a k-omega model with an extra cross-diffusion term. The [Wilcox k-omega model](/k-omega-model/) drops that term.
- **SST.** The [SST model](/k-omega-sst-model/) uses k-omega near walls and the transformed k-epsilon model away from them, and limits the shear stress.
- **Variants.** The RNG k-epsilon model changes the constants and adds a strain-dependent term to the $\varepsilon$ equation, and realizable k-epsilon models make $C_\mu$ depend on the strain so that the normal stresses stay nonnegative.
- **K41.** The [Kolmogorov theory](/kolmogorov-1941-theory/) says that $\varepsilon$ is set by the large eddies and passed down the cascade, which is why $\varepsilon$, not a viscous quantity, is the second variable.

## Known results in the model

**Eddy viscosity by hand.** With $k = 1$ m^2/s^2 and $\varepsilon = 10$ m^2/s^3, $\nu_t = 0.09 \times 1/10 = 0.009$ m^2/s.

**Decay of homogeneous turbulence (exact in the model).** The decay equations $dk/dt = -\varepsilon$ and $d\varepsilon/dt = -C_2\varepsilon^2/k$ have the solution
$$k = k_0\left(1 + \frac{t}{t_0}\right)^{-n}, \qquad \varepsilon = \varepsilon_0\left(1 + \frac{t}{t_0}\right)^{-n-1}, \qquad n = \frac{1}{C_2 - 1}, \quad t_0 = \frac{n k_0}{\varepsilon_0}.$$
Check by substitution: the first equation gives $\varepsilon_0 = n k_0/t_0$, and the second gives $(n + 1)/t_0 = C_2\varepsilon_0/k_0 = C_2 n/t_0$, so $n + 1 = C_2 n$. With $C_2 = 1.92$, $n = 1.087$. Starting from $k_0 = 1$ and $\varepsilon_0 = 1$, $t_0 = 1.087$ s and $k(t_0) = 2^{-1.087} = 0.471$ m^2/s^2. The tests check the RK4 solution against this formula and its fourth-order convergence. Measured decay exponents in grid turbulence are of the same size, a little above 1 (Pope 5.4.6), which is how $C_2$ was chosen: the agreement is a fit.

**Log layer (exact in the model).** In a constant-stress layer with production equal to dissipation and $U = (u_\tau/\kappa)\ln y + \text{const}$, the model has the solution $k = u_\tau^2/\sqrt{C_\mu}$, $\varepsilon = u_\tau^3/(\kappa y)$ and $\nu_t = \kappa u_\tau y$, provided
$$\kappa^2 = \sigma_\varepsilon\sqrt{C_\mu}\,(C_2 - C_1).$$
With the standard constants, $\sqrt{0.09} = 0.3$ and $k/u_\tau^2 = 3.33$, and $\kappa^2 = 1.3 \times 0.3 \times 0.48 = 0.1872$, so $\kappa = 0.433$. This is close to the measured 0.41 but not equal: the constants are a compromise among several flows. With $u_\tau = 0.5$ m/s at $y = 0.01$ m and $\kappa = 0.41$, $k = 0.833$ m^2/s^2, $\varepsilon = 30.5$ m^2/s^3 and $\nu_t = 0.00205$ m^2/s.

**Agreement with experiment (measurement).** The model gives good spreading rates for plane free shear layers and reasonable results for attached boundary layers in weak pressure gradients. Measurements show known failures: it predicts too much $k$ near stagnation points, the wrong spreading rate for the round jet compared with the plane jet, and too much skin friction and delayed separation in adverse pressure gradients. These are measured shortcomings of the fitted model, not of the averaged equations.

## References
