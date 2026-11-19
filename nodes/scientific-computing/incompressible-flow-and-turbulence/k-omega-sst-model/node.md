---
tag: 9699ZX
kind: model
slug: k-omega-sst-model
name: k-omega SST model
aliases:
- shear stress transport model
- Menter SST model
area: scientific-computing/incompressible-flow-and-turbulence
level: advanced
summary: "Blends k-omega near walls with k-epsilon in the free stream and limits the shear stress; the common model for separated flows."
model: real-ram
history:
  year: 1994
  people: [Florian Menter, Peter Bradshaw]
  note: Menter combined the Wilcox k-omega model near walls with a transformed k-epsilon model away from them, and limited the eddy viscosity with Bradshaw's observation that the shear stress in a boundary layer is close to 0.3 times k. The 1994 paper also gave the baseline (BSL) model without the limiter.
prereqs: [k-omega-model, k-epsilon-model]
see_also: [k-omega-model, k-epsilon-model, spalart-allmaras-model, boussinesq-eddy-viscosity, wall-functions, reynolds-averaged-navier-stokes, large-eddy-simulation]
sources:
  - paper: doi:10.2514/3.12149
    title: Florian R. Menter, Two-equation eddy-viscosity turbulence models for engineering applications, AIAA Journal 32(8), 1994, 1598-1605
    locator: the BSL and SST models, the blending functions F1 and F2, the limiter with a1 = 0.31, and the two sets of constants
  - paper: "F. R. Menter, M. Kuntz and R. Langtry, Ten years of industrial experience with the SST turbulence model, in K. Hanjalic, Y. Nagano and M. Tummers (eds.), Turbulence, Heat and Mass Transfer 4, Begell House, 2003, 625-632"
    locator: the strain-rate form of the limiter and the production limiter used in later codes
  - paper: "P. Bradshaw, D. H. Ferriss and N. P. Atwell, Calculation of boundary-layer development using the turbulent energy equation, Journal of Fluid Mechanics 28(3), 1967, 593-616"
    locator: the assumption that the shear stress is a fixed fraction of the turbulent kinetic energy
  - book: isbn:9781928729082
    title: David C. Wilcox, Turbulence Modeling for CFD, third edition, DCW Industries, 2006
    locator: Chapter 4 (two-equation models, including the discussion of the SST model and of stress limiters)
---

The k-omega SST (shear stress transport) model of Menter is a two-equation closure of the [Reynolds-averaged Navier-Stokes equations](/reynolds-averaged-navier-stokes/) that uses the [Wilcox k-omega model](/k-omega-model/) near walls and the [k-epsilon model](/k-epsilon-model/), rewritten in terms of $\omega$, away from them, with a smooth blending function between the two. It also limits the eddy viscosity so that the shear stress in a boundary layer cannot exceed $a_1 k$, which improves its predictions of separation. It is a [Boussinesq](/boussinesq-eddy-viscosity/) closure like its two parents and like the one-equation [Spalart-Allmaras model](/spalart-allmaras-model/), and it is normally integrated to the wall rather than used with [wall functions](/wall-functions/).

## The machine

**Unknowns.** The mean flow, $k$ (m^2/s^2) and $\omega$ (1/s), and the distance $d$ (m) to the nearest wall, which the blending functions need.

**Equations.** With $\mathcal P = 2\nu_t S_{ij}S_{ij}$,
$$\frac{Dk}{Dt} = \mathcal P - \beta^* k\omega + \nabla\cdot\left[(\nu + \sigma_k\nu_t)\nabla k\right],$$
$$\frac{D\omega}{Dt} = \frac{\gamma}{\nu_t}\mathcal P - \beta\omega^2 + \nabla\cdot\left[(\nu + \sigma_\omega\nu_t)\nabla\omega\right] + 2(1 - F_1)\frac{\sigma_{\omega 2}}{\omega}\nabla k\cdot\nabla\omega.$$
The last term is the cross diffusion that appears when the k-epsilon model is rewritten in $\omega$; the factor $1 - F_1$ switches it off near walls.

**Blending.** Each constant $\phi$ in the $\omega$ equation is $\phi = F_1\phi_1 + (1 - F_1)\phi_2$, where set 1 is k-omega and set 2 is transformed k-epsilon. The function is
$$F_1 = \tanh(\arg_1^4), \qquad \arg_1 = \min\left(\max\left(\frac{\sqrt k}{\beta^*\omega d}, \frac{500\nu}{d^2\omega}\right), \frac{4\sigma_{\omega 2}k}{CD_{k\omega}d^2}\right),$$
with $CD_{k\omega} = \max\left(2\sigma_{\omega 2}\frac{1}{\omega}\nabla k\cdot\nabla\omega, 10^{-20}\right)$. It is near one in the inner part of a boundary layer and goes to zero toward its edge and in the free stream.

**Eddy viscosity with the limiter.**
$$\nu_t = \frac{a_1 k}{\max(a_1\omega, \Omega F_2)}, \qquad F_2 = \tanh(\arg_2^2), \qquad \arg_2 = \max\left(\frac{2\sqrt k}{\beta^*\omega d}, \frac{500\nu}{d^2\omega}\right),$$
where $\Omega$ is the magnitude of the vorticity in the 1994 paper; later versions use the strain rate magnitude instead. When $a_1\omega \ge \Omega F_2$, $\nu_t = k/\omega$ as in k-omega. When the mean shear is large compared with $\omega$, the limiter holds the shear stress $\nu_t\Omega$ at $a_1 k$. Later codes also cap the production in the $k$ equation at a multiple of $\beta^* k\omega$, often 10.

**Parameters.**

| constant | set 1 (k-omega) | set 2 (k-epsilon) |
|---|---|---|
| $\sigma_k$ | 0.85 | 1.0 |
| $\sigma_\omega$ | 0.5 | 0.856 |
| $\beta$ | 0.075 | 0.0828 |
| $\gamma$ | 0.5532 | 0.4404 |

with $\beta^* = 0.09$, $\kappa = 0.41$ and $a_1 = 0.31$. Which are fitted and which derived:

- Set 1 comes from the Wilcox model, with $\sigma_k$ changed from 0.5 to 0.85 by fitting; these are fitted.
- Set 2 is derived from the standard k-epsilon constants: $\beta_2 = \beta^*(C_2 - 1) = 0.09 \times 0.92 = 0.0828$, $\sigma_{k2} = \sigma_k = 1.0$, and $\sigma_{\omega 2} = 0.856$ is $1/\sigma_\varepsilon$ with $\sigma_\varepsilon = 1.168$, the value the k-epsilon log-layer relation needs for $\kappa = 0.41$.
- Both $\gamma$ values are derived from the log-layer relation $\gamma = \beta/\beta^* - \sigma_\omega\kappa^2/\sqrt{\beta^*}$.
- $a_1 = 0.31$ is fitted; it rests on Bradshaw's measured ratio $-\langle u'v' \rangle/k \approx 0.3$ in boundary layers.
- The 500, the powers in the tanh and the floor $10^{-20}$ are design choices.

## What it counts

The same outputs as the parent models: the mean flow, $k$, $\omega$, the eddy viscosity and the Boussinesq stresses, and, because it is integrated to the wall, the wall shear stress, the separation and reattachment points and the wall heat flux.

## Relation to other models

- **k-omega.** Near walls ($F_1 = 1$) and without the limiter, it is the [Wilcox model](/k-omega-model/) with $\sigma_k = 0.85$. It keeps the simple near-wall behavior $\omega \to 6\nu/(\beta_1 y^2)$.
- **k-epsilon.** Far from walls ($F_1 = 0$) it is the [k-epsilon model](/k-epsilon-model/) written in $\omega$, which removes the free-stream sensitivity of the 1988 k-omega model.
- **BSL.** The baseline model of the same paper has the blending but no limiter and $\sigma_{k1} = 0.5$.
- **Spalart-Allmaras.** The [Spalart-Allmaras model](/spalart-allmaras-model/) is the main one-equation competitor for external aerodynamics; SST gives a turbulence length scale, which SA does not.
- **Hybrid methods.** SST is often the RANS part of hybrid RANS and [LES](/large-eddy-simulation/) methods such as detached eddy simulation, where the length scale $\sqrt k/(\beta^*\omega)$ is replaced by a grid scale away from walls.

## Known results in the model

**The limiter by hand (exact arithmetic).** Take $k = 1$ m^2/s^2, $\omega = 10$ 1/s and $\Omega = 100$ 1/s with $F_2 = 1$. Then $a_1\omega = 3.1 < \Omega F_2 = 100$, so
$$\nu_t = \frac{0.31 \times 1}{100} = 0.0031\ \text{m}^2/\text{s}, \qquad \nu_t\Omega = 0.31 = a_1 k\ \text{m}^2/\text{s}^2.$$
The unlimited value $k/\omega = 0.1$ m^2/s would give a shear stress of 10 m^2/s^2, 32 times larger. In an adverse pressure gradient the production exceeds the dissipation, the unlimited model gives too much shear stress, and the boundary layer resists separation too much; the limiter brings the stress back to the measured ratio.

**Log-layer constants (exact in the model).** The values of $\gamma$ follow from $\kappa = 0.41$ and $\beta^* = 0.09$: $\gamma_1 = 0.075/0.09 - 0.5 \times 0.1681/0.3 = 0.8333 - 0.2802 = 0.5532$ and $\gamma_2 = 0.0828/0.09 - 0.856 \times 0.1681/0.3 = 0.9200 - 0.4796 = 0.4404$. Both sets therefore give the same log layer, so blending between them does not move it.

**Equivalence with k-epsilon (exact).** The relation $\beta_2 = \beta^*(C_2 - 1)$ makes the decay exponent of set 2 equal to that of k-epsilon: $\beta^*/\beta_2 = 1/(C_2 - 1) = 1.087$. Set 1 decays with exponent $\beta^*/\beta_1 = 1.2$.

**Agreement with experiment (measurement).** In Menter's comparisons, SST predicted adverse pressure gradient boundary layers and the separated flow over a backward-facing step and an airfoil near stall better than k-epsilon and the original k-omega model. It is now a default model in many commercial and open codes. These are measured comparisons for the chosen constants; the model still inherits the limits of the Boussinesq hypothesis in strongly curved, swirling or secondary flows.

## References
