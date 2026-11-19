---
tag: 36CQFZ
kind: technique
slug: large-eddy-simulation
name: Large eddy simulation
aliases:
- LES
area: scientific-computing/incompressible-flow-and-turbulence
level: core
summary: Resolves the large turbulent eddies on the grid and models the effect of the filtered small scales by a subgrid model.
model: real-ram
history:
  year: 1963
  people: [Joseph Smagorinsky, Douglas Lilly, James Deardorff, Massimo Germano, Parviz Moin]
  note: Smagorinsky introduced the subgrid eddy viscosity for weather models in 1963, and Lilly tied its constant to the Kolmogorov spectrum. Deardorff ran the first engineering LES, of channel flow, in 1970, and Germano, Piomelli, Moin and Cabot made the model coefficient dynamic in 1991.
prereqs: [kolmogorov-1941-theory, navier-stokes-equations]
see_also: [smagorinsky-model, dynamic-subgrid-model, direct-numerical-simulation, kolmogorov-1941-theory, reynolds-averaged-navier-stokes, wall-functions, spectral-methods, convolution]
sources:
  - book: isbn:9780521598866
    title: Stephen B. Pope, Turbulent Flows, Cambridge University Press, 2000
    locator: Chapter 13 (13.1 to 13.3 filtering and the filtered equations, 13.4 the Smagorinsky model, 13.5 LES in wavenumber space, 13.6 further residual-stress models, 13.7 discussion)
  - paper: "J. Smagorinsky, General circulation experiments with the primitive equations, I. The basic experiment, Monthly Weather Review 91(3), 1963, 99-164"
    locator: the nonlinear lateral viscosity proportional to the grid size squared times the deformation
  - paper: doi:10.1017/S0022112070000691
    title: James W. Deardorff, A numerical study of three-dimensional turbulent channel flow at large Reynolds numbers, Journal of Fluid Mechanics 41(2), 1970, 453-480
    locator: the first large eddy simulation of a wall-bounded flow, with the Smagorinsky model
  - paper: doi:10.1063/1.857955
    title: Massimo Germano, Ugo Piomelli, Parviz Moin and William H. Cabot, A dynamic subgrid-scale eddy viscosity model, Physics of Fluids A 3(7), 1991, 1760-1765
    locator: the computation of the model coefficient from the resolved field
---

Large eddy simulation (LES) is a method for turbulent flow that computes the large eddies directly from spatially filtered [Navier-Stokes equations](/navier-stokes-equations/) on a grid of spacing $\Delta$, and represents the effect of the smaller, filtered-out eddies by a subgrid model. It sits between [direct numerical simulation](/direct-numerical-simulation/), which resolves every scale, and [RANS](/reynolds-averaged-navier-stokes/), which resolves none. The [Kolmogorov 1941 theory](/kolmogorov-1941-theory/) is the basis for putting the filter in the inertial range, where the small scales are close to universal, and the [Smagorinsky model](/smagorinsky-model/) and the [dynamic subgrid model](/dynamic-subgrid-model/) are the standard eddy viscosity models for those scales.

## In plain words

In a turbulent flow the big eddies carry most of the energy and depend on the shape of the flow, while the small eddies look much the same in every flow. Large eddy simulation uses this. It smooths the flow over a small region, about the size of a grid cell, and computes the smoothed flow exactly. The big eddies are thus resolved in full. The small eddies are not computed; their main effect, draining energy from the big ones, is added by a simple model. This costs far less than following every eddy, because the grid only needs to be fine enough for the big ones. It still costs much more than computing only the average flow, but it gives the unsteady motion, which an average cannot give.

## When it applies

- The flow has large unsteady eddies that matter: free shear layers, jets, wakes, separated flows, mixing, combustion, aeroacoustic noise, or the atmospheric boundary layer.
- The Reynolds number is too high for [DNS](/direct-numerical-simulation/), but the grid can resolve the energy-containing eddies. A common rule of thumb is to resolve at least 80 percent of the turbulent kinetic energy.
- The filter width $\Delta$ lies in the inertial range, $\eta \ll \Delta \ll L$, where $\eta$ is the Kolmogorov scale and $L$ the size of the large eddies.
- Near walls the energy-containing eddies scale with the viscous length $\nu/u_\tau$, so resolving them costs nearly as much as DNS. At high Reynolds numbers the near-wall layer is often modeled instead, by a wall model like the [wall functions](/wall-functions/) of RANS.

## The template

**Filter.** For a filter kernel $G_\Delta$ with integral one, the filtered velocity is the [convolution](/convolution/)
$$\bar u(x) = \int G_\Delta(r)\, u(x - r)\, dr.$$
Common kernels are the box (top hat) of width $\Delta$, the Gaussian, and the sharp spectral cutoff at $k_c = \pi/\Delta$. Often the filter is not applied explicitly: the grid and the scheme act as the filter, and $\Delta$ is taken as the cell size or $(\Delta x\,\Delta y\,\Delta z)^{1/3}$.

**Filtered equations.** If the filter commutes with derivatives (true for a uniform filter width),
$$\frac{\partial \bar u_i}{\partial x_i} = 0, \qquad \frac{\partial \bar u_i}{\partial t} + \frac{\partial(\bar u_i\bar u_j)}{\partial x_j} = -\frac{1}{\rho}\frac{\partial \bar p}{\partial x_i} + \nu\nabla^2\bar u_i - \frac{\partial \tau_{ij}}{\partial x_j},$$
with the subgrid stress $\tau_{ij} = \overline{u_i u_j} - \bar u_i\bar u_j$. These are exact; $\tau_{ij}$ is the unknown, and it plays the role of the Reynolds stress in RANS.

**Subgrid model.** An eddy viscosity model, in the spirit of the [Boussinesq hypothesis](/boussinesq-eddy-viscosity/), sets the anisotropic part of $\tau_{ij}$ to $-2\nu_r\bar S_{ij}$, with $\bar S_{ij}$ the resolved strain rate. The [Smagorinsky model](/smagorinsky-model/) takes $\nu_r = (C_s\Delta)^2|\bar S|$; the [dynamic model](/dynamic-subgrid-model/) computes $C_s$ from the resolved field.

**Steps.**

1. Choose $\Delta$ from an estimate of the integral scale $L$, so that the energy-containing eddies span many cells, and check that $\Delta$ is in the inertial range.
2. Discretize with a scheme of low numerical dissipation: central or energy-conserving finite differences or finite volumes, or [spectral methods](/spectral-methods/) in simple domains. A strongly upwind scheme adds numerical dissipation that can exceed the model.
3. Advance in time with a step that keeps the Courant number $Co$ well below one, and enforce $\nabla\cdot\bar u = 0$ by a projection.
4. Supply unsteady inflow turbulence (recycled, synthetic or from a precursor run) and suitable wall treatment.
5. Run past the start-up transient, then collect statistics over many large-eddy times.
6. Check sensitivity to $\Delta$: the resolved fraction of $k$ and the statistics of interest should not change much on a finer grid.

## Classic examples

**A box filter by hand.** On a periodic grid take the samples $u = (0, 2, 0, 2)$ and the discrete filter $\bar u_i = (u_{i-1} + 2u_i + u_{i+1})/4$. Then $\bar u = (1, 1, 1, 1)$: the filter removes the shortest wave entirely. The squares are $u^2 = (0, 4, 0, 4)$, so $\overline{u^2} = (2, 2, 2, 2)$, and the subgrid stress is
$$\tau = \overline{u^2} - \bar u^2 = 2 - 1 = 1,$$
exactly the energy of the removed wave. For a filter with nonnegative weights, $\tau_{ii} \ge 0$ always, which is a theorem: it is a weighted variance. The transfer function of this filter is $\cos^2(kh/2)$ for grid spacing $h$, which is zero at the shortest wave $kh = \pi$.

**Energy left to the model (by K41).** With the spectrum $E(k) = C\varepsilon^{2/3}k^{-5/3}$ beyond a cutoff $k_c$ in the inertial range, the subgrid kinetic energy is $\int_{k_c}^\infty E\,dk = \frac{3}{2}C\varepsilon^{2/3}k_c^{-2/3}$. Halving $\Delta$ doubles $k_c$ and divides the subgrid energy by $2^{2/3} = 1.59$. So refining the grid shifts energy to the resolved field only slowly; this is a prediction from the spectrum, not a measurement.

**Channel flow.** Deardorff (1970) computed a channel with the Smagorinsky model on a grid of 6720 points and found that a smaller coefficient than in isotropic turbulence was needed, an early sign that the constant is not universal.

**Weather and climate.** Smagorinsky's 1963 general circulation model used the eddy viscosity for the lateral mixing that the coarse grid could not resolve, and atmospheric boundary layer LES with the same type of model is a standard tool in meteorology.

## Variations

- **Explicit and implicit filtering.** Explicit filtering applies a filter of known shape at each step, separating the filter from the grid. Implicit LES uses no model at all and lets the numerical dissipation of the scheme play the role of the subgrid stress.
- **Subgrid models.** Besides [Smagorinsky](/smagorinsky-model/) and the [dynamic model](/dynamic-subgrid-model/), there are scale-similarity models that estimate $\tau_{ij}$ from the resolved field filtered twice, mixed models that add an eddy viscosity to them, and models built to vanish in pure shear or solid-body rotation near walls.
- **Wall-modeled LES.** Resolve the outer flow and model the inner layer with a wall stress law, which makes the cost at high Reynolds number grow much more slowly.
- **Hybrid RANS and LES.** Detached eddy simulation uses a RANS model such as [Spalart-Allmaras](/spalart-allmaras-model/) or [SST](/k-omega-sst-model/) in attached boundary layers and LES in separated regions.

## Pitfalls

- **Numerical dissipation.** Upwind or low-order schemes damp the smallest resolved eddies more than the subgrid model, so the model has little effect and the results depend on the scheme.
- **No grid convergence in the usual sense.** Refining the grid changes the problem: as $\Delta \to \eta$ LES tends to DNS. Report $\Delta$ and the resolved fraction of the energy, not a single "converged" answer.
- **Commutation errors.** On stretched grids the filter width varies and the filter does not commute exactly with derivatives.
- **Near-wall resolution.** A grid that is fine enough far from walls can be far too coarse near them, where a constant-coefficient Smagorinsky model also gives too much viscosity.
- **Inflow.** A smooth mean inflow profile with no fluctuations takes a long distance to become turbulent.
- **Comparing with experiment.** LES statistics are of the filtered field. Resolved stresses must be compared with measured ones with the subgrid part added or estimated.

## Exercises

1. Apply the filter $\bar u_i = (u_{i-1} + 2u_i + u_{i+1})/4$ to the periodic samples $u = (1, 1, 1, 1)$ and to $u = (1, -1, 1, -1)$. (Answer: $(1, 1, 1, 1)$ and $(0, 0, 0, 0)$.)
2. With the K41 spectrum, by what factor must $\Delta$ shrink to cut the subgrid energy in half? (Answer: $k_c$ must grow by $2^{3/2} = 2.83$.)

## References
