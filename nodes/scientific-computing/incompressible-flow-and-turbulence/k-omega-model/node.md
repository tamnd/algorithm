---
tag: XZPQV1
kind: model
slug: k-omega-model
name: Wilcox k-omega model
aliases:
- k-omega turbulence model
area: scientific-computing/incompressible-flow-and-turbulence
level: core
summary: "Two transport equations, for turbulent kinetic energy and the specific dissipation rate omega, accurate near walls with no damping functions."
model: real-ram
history:
  year: 1988
  people: [Andrey Kolmogorov, Philip Saffman, David C. Wilcox]
  note: Kolmogorov proposed a model with an equation for a frequency of the energy-containing eddies in 1942, and Saffman a similar one in 1970. Wilcox gave the form and constants of the standard model in 1988 and revised it in 1998 and 2006.
prereqs: [boussinesq-eddy-viscosity]
see_also: [k-epsilon-model, k-omega-sst-model, boussinesq-eddy-viscosity, spalart-allmaras-model, wall-functions, mixing-length-model, reynolds-averaged-navier-stokes]
sources:
  - paper: doi:10.2514/3.10041
    title: David C. Wilcox, Reassessment of the scale-determining equation for advanced turbulence models, AIAA Journal 26(11), 1988, 1299-1310
    locator: the k-omega equations with alpha = 5/9, beta = 3/40, beta* = 9/100, sigma = sigma* = 1/2, and the near-wall solution
  - book: isbn:9781928729082
    title: David C. Wilcox, Turbulence Modeling for CFD, third edition, DCW Industries, 2006
    locator: Chapter 4 (two-equation models, the k-omega model, its closure coefficients, the 2006 version and its free shear flow results)
  - book: isbn:9780521598866
    title: Stephen B. Pope, Turbulent Flows, Cambridge University Press, 2000
    locator: Section 10.5.1 (the k-omega model)
  - paper: doi:10.2514/3.11115
    title: F. R. Menter, Influence of freestream values on k-omega turbulence model predictions, AIAA Journal 30(6), 1992, 1657-1659
    locator: the dependence of the results on the value of omega in the free stream
  - paper: doi:10.2514/1.36541
    title: David C. Wilcox, Formulation of the k-omega turbulence model revisited, AIAA Journal 46(11), 2008, 2823-2838
    locator: the 2006 version with cross diffusion and a stress limiter
---

The Wilcox k-omega model is a two-equation closure of the [Reynolds-averaged Navier-Stokes equations](/reynolds-averaged-navier-stokes/) that solves transport equations for the turbulent kinetic energy $k$ and the specific dissipation rate $\omega$, and sets the eddy viscosity to $\nu_t = k/\omega$. Like the [k-epsilon model](/k-epsilon-model/) it uses the [Boussinesq hypothesis](/boussinesq-eddy-viscosity/), but its $\omega$ equation has a simple exact solution near a wall, so it can be integrated through the viscous sublayer without damping functions or [wall functions](/wall-functions/). Its known weakness is a dependence on the value of $\omega$ in the free stream, which the [SST model](/k-omega-sst-model/) removes by switching to k-epsilon away from walls. The [Spalart-Allmaras model](/spalart-allmaras-model/) is the one-equation alternative for the same aerodynamic flows.

## The machine

**Unknowns.** The mean velocity and pressure, plus $k$ (m^2/s^2) and $\omega$ (1/s). The dissipation rate is $\varepsilon = \beta^* k\omega$, so $\omega$ is a rate of dissipation per unit energy, or an inverse time scale of the large eddies.

**Equations (1988 form).** With the production $\mathcal P = 2\nu_t S_{ij}S_{ij}$,
$$\nu_t = \frac{k}{\omega},$$
$$\frac{Dk}{Dt} = \mathcal P - \beta^* k\omega + \nabla\cdot\left[(\nu + \sigma^*\nu_t)\nabla k\right],$$
$$\frac{D\omega}{Dt} = \alpha\frac{\omega}{k}\mathcal P - \beta\omega^2 + \nabla\cdot\left[(\nu + \sigma\nu_t)\nabla\omega\right].$$

**Parameters.** The constants are $\alpha = 5/9$, $\beta = 3/40$, $\beta^* = 9/100$ and $\sigma = \sigma^* = 1/2$. All are fitted, with these targets:

- $\beta^* = 0.09$ plays the role of $C_\mu$ and gives $-\langle u'v' \rangle/k = \sqrt{\beta^*} = 0.3$ in equilibrium shear layers;
- the ratio $\beta^*/\beta = 1.2$ is the decay exponent of grid turbulence (derived below);
- $\alpha$ is then tied to the von Karman constant by the log-layer relation below;
- $\sigma$ and $\sigma^*$ are chosen of order one and tuned against boundary layer data.

**Wall boundary condition.** At a smooth wall $k = 0$. Near the wall the $\omega$ equation reduces to $\nu\, d^2\omega/dy^2 = \beta\omega^2$, which has the exact solution $\omega = 6\nu/(\beta y^2)$. So $\omega$ is infinite at the wall. Codes impose the asymptotic form at the first cell or set a large finite wall value; a common rule, from Menter, is $\omega_w = 10 \cdot 6\nu/(\beta\,\Delta y_1^2)$ with $\Delta y_1$ the first cell height, and a first cell at $y^+ \lesssim 1$.

**Free-stream value.** Outside a boundary layer $k$ and $\omega$ must be given small positive values, and the 1988 model is sensitive to the value of $\omega$ chosen there.

**Later versions.** Wilcox's 2006 version adds a cross-diffusion term $\sigma_d (1/\omega)\nabla k\cdot\nabla\omega$ (only when it is positive), a stress limiter in $\nu_t$ with $C_{lim} = 7/8$, and new constants, among them $\alpha = 13/25$, $\beta_0 = 0.0708$, $\sigma^* = 3/5$ and $\sigma_d = 1/8$. These reduce the free-stream sensitivity and improve free shear flows. A page or code must say which version it uses.

## What it counts

The model gives the mean flow, $k$, $\omega$, $\varepsilon = \beta^* k\omega$, the eddy viscosity and the Boussinesq stresses. Because it can be integrated to the wall, it also gives the wall shear stress and the heat flux directly, without the assumption of a log layer at the first cell.

## Relation to other models

- **k-epsilon.** Substituting $\varepsilon = \beta^* k\omega$ into the [k-epsilon model](/k-epsilon-model/) gives an $\omega$ equation with an extra cross-diffusion term proportional to $\frac{1}{\omega}\nabla k\cdot\nabla\omega$, plus some changes in the diffusion terms. The two models differ by this term and by their constants, which is why k-omega is better near walls and k-epsilon is less sensitive to free-stream values.
- **SST.** The [SST model](/k-omega-sst-model/) blends the two with a function that is one near walls and zero far away, and adds a limiter on the shear stress.
- **Mixing length.** In the log layer the model gives $\nu_t = \kappa u_\tau y$, the [mixing length](/mixing-length-model/) result.
- **Boussinesq.** As a [Boussinesq](/boussinesq-eddy-viscosity/) closure it shares the limits of all eddy viscosity models.
- **Wall functions.** It can also be run with [wall functions](/wall-functions/) on coarse grids, with $\omega$ at the first cell set to $u_\tau/(\sqrt{\beta^*}\kappa y)$.

## Known results in the model

**Decay of homogeneous turbulence (exact in the model).** With no mean gradient, $dk/dt = -\beta^* k\omega$ and $d\omega/dt = -\beta\omega^2$. The second equation gives $\omega = \omega_0/(1 + \beta\omega_0 t)$, and then the first gives
$$k = k_0\,(1 + \beta\omega_0 t)^{-\beta^*/\beta}.$$
So $k$ decays like $t^{-1.2}$ at late times. By hand: with $k_0 = 1$ m^2/s^2 and $\omega_0 = 10$ 1/s, at $t = 1/(\beta\omega_0) = 1.333$ s, $\omega = 5$ 1/s and $k = 2^{-1.2} = 0.435$ m^2/s^2. The 2006 constants give the exponent $0.09/0.0708 = 1.27$.

**Log layer (exact in the model).** In a constant-stress layer with $U = (u_\tau/\kappa)\ln y + \text{const}$, the model has the solution
$$k = \frac{u_\tau^2}{\sqrt{\beta^*}}, \qquad \omega = \frac{u_\tau}{\sqrt{\beta^*}\,\kappa y}, \qquad \nu_t = \kappa u_\tau y,$$
provided $\alpha = \beta/\beta^* - \sigma\kappa^2/\sqrt{\beta^*}$. With $\kappa = 0.41$ this gives $\alpha = 0.8333 - 0.5 \times 0.1681/0.3 = 0.553$, close to the chosen 5/9; conversely, $\alpha = 5/9$ implies $\kappa = 0.408$.

**Near-wall solution (exact in the model).** $\omega = 6\nu/(\beta y^2)$ satisfies $\nu\,\omega'' = \beta\omega^2$: with $\omega = A y^{-2}$, $\omega'' = 6A y^{-4}$, so $6\nu A = \beta A^2$ and $A = 6\nu/\beta = 80\nu$. In air ($\nu = 1.5 \times 10^{-5}$ m^2/s) at $y = 10^{-5}$ m this is $\omega = 1.2 \times 10^7$ 1/s.

**Agreement with experiment (measurement).** For boundary layers in adverse pressure gradients, the k-omega model predicts skin friction and separation better than the standard k-epsilon model in the comparisons collected by Wilcox. Menter showed that for free shear flows and for the edge of boundary layers, the results of the 1988 model change markedly with the free-stream value of $\omega$. Both are measured or computed findings for this set of constants.

## References
