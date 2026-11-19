---
tag: Y6ETTZ
kind: model
slug: dynamic-subgrid-model
name: Dynamic subgrid model
aliases:
- dynamic Smagorinsky model
- Germano dynamic model
area: scientific-computing/incompressible-flow-and-turbulence
level: advanced
summary: "Computes the Smagorinsky coefficient locally from the resolved field by test filtering and the Germano identity, with the least squares fit of Lilly."
model: real-ram
history:
  year: 1991
  people: [Massimo Germano, Ugo Piomelli, Parviz Moin, William Cabot, Douglas Lilly]
  note: Germano, Piomelli, Moin and Cabot proposed the dynamic procedure in 1991 at the Stanford Center for Turbulence Research. Lilly replaced their contraction with a least squares fit in 1992, and Meneveau, Lund and Cabot averaged along fluid paths in 1996.
prereqs: [smagorinsky-model]
see_also: [smagorinsky-model, large-eddy-simulation, least-squares-problem, kolmogorov-1941-theory, direct-numerical-simulation, convolution, boussinesq-eddy-viscosity]
sources:
  - paper: doi:10.1063/1.857955
    title: Massimo Germano, Ugo Piomelli, Parviz Moin and William H. Cabot, A dynamic subgrid-scale eddy viscosity model, Physics of Fluids A 3(7), 1991, 1760-1765
    locator: the test filter, the identity for the resolved stress, the coefficient from the contraction with the strain rate, and the LES of channel flow and transition
  - paper: doi:10.1063/1.858280
    title: D. K. Lilly, A proposed modification of the Germano subgrid-scale closure method, Physics of Fluids A 4(3), 1992, 633-635
    locator: the least squares estimate of the coefficient
  - paper: "C. Meneveau, T. S. Lund and W. H. Cabot, A Lagrangian dynamic subgrid-scale model of turbulence, Journal of Fluid Mechanics 319, 1996, 353-385"
    locator: averaging the numerator and denominator along fluid pathlines for flows with no homogeneous direction
  - book: isbn:9780521598866
    title: Stephen B. Pope, Turbulent Flows, Cambridge University Press, 2000
    locator: Section 13.6.1 (the dynamic model)
---

The dynamic subgrid model is a procedure for [large eddy simulation](/large-eddy-simulation/) that computes the coefficient of the [Smagorinsky model](/smagorinsky-model/) at each place and time from the resolved velocity field, instead of fixing it in advance. It filters the resolved field a second time with a coarser test filter, uses the Germano identity to relate the subgrid stresses at the two filter widths to a stress that can be computed exactly, and fits the coefficient by least squares, as Lilly proposed. The [Kolmogorov 1941 theory](/kolmogorov-1941-theory/) justifies the key assumption, that the coefficient is the same at both widths when both lie in the inertial range. The model needs no fitted constant, turns itself off in laminar regions and near walls, and gives results closer to [DNS](/direct-numerical-simulation/) data than the constant-coefficient model.

## The machine

**Unknowns.** The filtered velocity $\bar u_i$ of the LES on a grid with filter width $\Delta$, and a coefficient field $C(x, t) = C_s^2$.

**Two filters.** The grid filter (bar) has width $\Delta$. The test filter (hat) has width $\hat\Delta = \alpha\Delta$, usually with $\alpha = 2$, and is applied explicitly to resolved quantities, for example by the discrete [convolution](/convolution/) $\hat f_i = (f_{i-1} + 2f_i + f_{i+1})/4$ in each direction.

**Stresses.**

- Subgrid stress at the grid level: $\tau_{ij} = \overline{u_iu_j} - \bar u_i\bar u_j$ (unknown).
- Subgrid stress at the test level: $T_{ij} = \widehat{\overline{u_iu_j}} - \hat{\bar u}_i\hat{\bar u}_j$ (unknown).
- Resolved stress: $L_{ij} = \widehat{\bar u_i\bar u_j} - \hat{\bar u}_i\hat{\bar u}_j$ (computable from $\bar u$).

**Germano identity (exact).** $L_{ij} = T_{ij} - \hat\tau_{ij}$. The terms $\widehat{\overline{u_iu_j}}$ cancel when $\hat\tau_{ij}$ is subtracted from $T_{ij}$.

**Model at both levels.** Use the Smagorinsky form with the same $C$:
$$\tau_{ij} - \tfrac{1}{3}\tau_{kk}\delta_{ij} = -2C\Delta^2|\bar S|\bar S_{ij}, \qquad T_{ij} - \tfrac{1}{3}T_{kk}\delta_{ij} = -2C\hat\Delta^2|\hat{\bar S}|\hat{\bar S}_{ij},$$
where $\hat{\bar S}_{ij}$ is the strain rate of $\hat{\bar u}$. If $C$ varies slowly enough to be taken out of the test filter, the identity becomes
$$L_{ij}^d = 2C M_{ij}, \qquad M_{ij} = \Delta^2\widehat{|\bar S|\bar S_{ij}} - \hat\Delta^2|\hat{\bar S}|\hat{\bar S}_{ij},$$
with $L_{ij}^d$ the traceless part of $L_{ij}$. These are five independent equations (in 3D) for one unknown.

**Least squares (Lilly 1992).** Minimizing $\sum_{ij}(L_{ij}^d - 2CM_{ij})^2$ is a one-unknown [least squares problem](/least-squares-problem/) with solution
$$C = \frac{\langle L_{ij}M_{ij}\rangle}{2\langle M_{ij}M_{ij}\rangle}.$$
Germano and coworkers first contracted with $\bar S_{ij}$ instead; that denominator can vanish, and Lilly's form is now standard.

**Averaging and clipping (rules).** The pointwise $C$ swings widely and is often negative, and an LES that uses it directly becomes unstable. The brackets $\langle\cdot\rangle$ therefore denote an average: over homogeneous directions (planes parallel to the walls in a channel), over a small neighborhood, or along fluid pathlines with an exponential weight in the past (the Lagrangian model). The total viscosity is also clipped, $\nu + C\Delta^2|\bar S| \ge 0$. These are practical rules, not consequences of the identity.

**Parameters.** No model constant is fitted. The choices are the ratio $\alpha$ (2 is usual), the shape of the test filter, and the averaging. The assumption that $C$ is the same at $\Delta$ and $\hat\Delta$ is a hypothesis of scale invariance; scale-dependent variants drop it.

**Cost.** Each step needs the test filtering of $\bar u_i$, $\bar u_i\bar u_j$ and $|\bar S|\bar S_{ij}$, a few tens of extra filter operations per point. The work stays $O(N)$ per step in the real RAM, a modest multiple of the cost of the plain Smagorinsky model.

## What it counts

The model gives the coefficient field $C(x, t)$, the subgrid eddy viscosity $\nu_r = C\Delta^2|\bar S|$, the subgrid dissipation and, where $C < 0$ after averaging, a local transfer of energy from small to large scales (backscatter). Inside the LES it fixes the resolved flow and its statistics.

## Relation to other models

- **Smagorinsky.** It is the [Smagorinsky model](/smagorinsky-model/) with $C_s^2$ computed instead of fixed. The computed value is of the same size as the constants fitted by hand, smaller in shear flows than in isotropic turbulence, and near walls it drops to zero, which replaces the van Driest damping.
- **LES.** It is a subgrid model inside [large eddy simulation](/large-eddy-simulation/), and its test filter needs $\hat\Delta$ to lie in the inertial range too.
- **Other dynamic models.** The same procedure can fit the coefficient of any model with an unknown constant: mixed models with a scale-similarity part, other eddy viscosity forms, and models for scalar fluxes.
- **A priori tests.** The identity can be checked on filtered [DNS](/direct-numerical-simulation/) fields, where $\tau_{ij}$ is known exactly.

## Known results in the model

**The identity (theorem).** Expand: $T_{ij} - \hat\tau_{ij} = \left(\widehat{\overline{u_iu_j}} - \hat{\bar u}_i\hat{\bar u}_j\right) - \left(\widehat{\overline{u_iu_j}} - \widehat{\bar u_i\bar u_j}\right) = \widehat{\bar u_i\bar u_j} - \hat{\bar u}_i\hat{\bar u}_j = L_{ij}$. The test filter only needs to be linear. It holds for any field and any linear filter pair, so $L_{ij}$ is always computable.

**Resolved stress by hand.** On a periodic grid with resolved samples $\bar u = (0, 2, 0, 2)$ and the test filter $\hat f_i = (f_{i-1} + 2f_i + f_{i+1})/4$: $\hat{\bar u} = (1, 1, 1, 1)$, $\bar u^2 = (0, 4, 0, 4)$, $\widehat{\bar u^2} = (2, 2, 2, 2)$, so $L = 2 - 1 = 1$ at every point. If $\bar u$ is smooth at the scale $\hat\Delta$, for example constant, then $L = 0$ and so $C = 0$: the model switches off when there is no energy between the two filter widths, as in a laminar flow.

**Least squares by hand.** Suppose that after averaging the two-component data are $L^d = (0.02, 0.01)$ and $M = (0.5, 0.2)$ in consistent units. Then $\langle LM\rangle = 0.010 + 0.002 = 0.012$, $\langle MM\rangle = 0.25 + 0.04 = 0.29$, and
$$C = \frac{0.012}{2 \times 0.29} = 0.0207, \qquad C_s = \sqrt{0.0207} = 0.144.$$
With $2C = 0.041379$, the fit is $2CM = (0.020690, 0.008276)$ and the residual is $L^d - 2CM = (-0.000690, 0.001724)$. It is orthogonal to $M$, as least squares requires: $-0.000690 \times 0.5 + 0.001724 \times 0.2 = -0.000345 + 0.000345 = 0$.

**Channel flow and transition (measurement).** In the LES of Germano and coworkers, the computed coefficient went to zero at the wall with $\nu_r$ falling like $y^3$, close to the correct near-wall behavior, with no damping function. It was near zero in the laminar part of a transitional channel and grew as the flow became turbulent. Results with the model agreed better with DNS data than the constant-coefficient model. These are measured findings from those simulations.

**Instability without averaging (measurement).** In simulations, the pointwise coefficient takes large negative values over long times in some regions, which leads to growing energy and blow-up. This is why averaging and clipping are part of every practical version.

## References
