---
tag: XS6424
kind: model
slug: smagorinsky-model
name: Smagorinsky model
aliases:
- Smagorinsky subgrid model
area: scientific-computing/incompressible-flow-and-turbulence
level: core
summary: "A subgrid eddy viscosity equal to (C_s Delta)^2 times the magnitude of the resolved strain rate tensor."
model: real-ram
history:
  year: 1963
  people: [Joseph Smagorinsky, Douglas Lilly, James Deardorff]
  note: Smagorinsky used the nonlinear viscosity in a general circulation model of the atmosphere in 1963. Lilly derived the constant from the Kolmogorov spectrum in 1967, and Deardorff used the model in the first LES of channel flow in 1970 with a smaller constant.
prereqs: [large-eddy-simulation]
see_also: [large-eddy-simulation, dynamic-subgrid-model, kolmogorov-1941-theory, mixing-length-model, boussinesq-eddy-viscosity, direct-numerical-simulation, finite-difference-method]
sources:
  - paper: "J. Smagorinsky, General circulation experiments with the primitive equations, I. The basic experiment, Monthly Weather Review 91(3), 1963, 99-164"
    locator: the lateral eddy viscosity proportional to the square of the grid size times the magnitude of the deformation
  - paper: "D. K. Lilly, The representation of small-scale turbulence in numerical simulation experiments, Proceedings of the IBM Scientific Computing Symposium on Environmental Sciences, Yorktown Heights, 1966, IBM Form 320-1951, 1967, 195-210"
    locator: the estimate of the constant from the inertial range spectrum
  - paper: doi:10.1017/S0022112070000691
    title: James W. Deardorff, A numerical study of three-dimensional turbulent channel flow at large Reynolds numbers, Journal of Fluid Mechanics 41(2), 1970, 453-480
    locator: the model in channel flow and the smaller value of the constant needed there
  - book: isbn:9780521598866
    title: Stephen B. Pope, Turbulent Flows, Cambridge University Press, 2000
    locator: Section 13.4 (the Smagorinsky model, 13.4.2 the behavior in the inertial subrange, 13.4.5 near-wall resolution)
---

The Smagorinsky model is a subgrid-scale closure for [large eddy simulation](/large-eddy-simulation/) that sets the eddy viscosity of the unresolved scales to $\nu_r = (C_s\Delta)^2|\bar S|$, where $\Delta$ is the filter width, $|\bar S|$ is the magnitude of the resolved strain rate and $C_s$ is a constant. It is a [mixing length model](/mixing-length-model/) for the subgrid scales, with the length set by the grid instead of the wall distance. The [Kolmogorov 1941 theory](/kolmogorov-1941-theory/) gives Lilly's estimate $C_s \approx 0.17$; shear flows need about 0.1, and the [dynamic subgrid model](/dynamic-subgrid-model/) computes the coefficient from the resolved field instead. As $\Delta$ shrinks toward the Kolmogorov scale, the model fades and LES approaches [direct numerical simulation](/direct-numerical-simulation/).

## The machine

**Unknowns.** The filtered velocity $\bar u_i$ and pressure $\bar p$ of the LES equations, on a grid with filter width $\Delta$ (m). The subgrid stress is $\tau_{ij} = \overline{u_i u_j} - \bar u_i\bar u_j$.

**Closure.** With the resolved strain rate $\bar S_{ij} = \frac{1}{2}(\partial\bar u_i/\partial x_j + \partial\bar u_j/\partial x_i)$ (1/s),
$$\tau_{ij} - \frac{1}{3}\tau_{kk}\delta_{ij} = -2\nu_r\bar S_{ij}, \qquad \nu_r = (C_s\Delta)^2|\bar S|, \qquad |\bar S| = \sqrt{2\bar S_{ij}\bar S_{ij}}.$$
The trace $\tau_{kk}$ is absorbed into the filtered pressure. This is the [Boussinesq form](/boussinesq-eddy-viscosity/) with the velocity scale $C_s\Delta|\bar S|$ and length scale $C_s\Delta$.

**Parameters.**

- $C_s$. Lilly's estimate from the K41 spectrum is $C_s = \frac{1}{\pi}\left(\frac{2}{3C_K}\right)^{3/4}$, about 0.17 for $C_K = 1.5$ (derived below, given the measured Kolmogorov constant $C_K$). In practice it is fitted: about 0.1 in channel flow and other shear flows, after Deardorff.
- $\Delta$. A choice tied to the grid, usually the cell size or $(\Delta x\,\Delta y\,\Delta z)^{1/3}$ on anisotropic grids.
- Near walls, $C_s\Delta$ is often multiplied by a van Driest factor $1 - e^{-y^+/A^+}$ with $A^+ \approx 26$, a rule borrowed from the mixing length model.

**Procedure on a periodic 2D grid.** With central differences of second order,

```pseudo id=main
SMAGORINSKY-2D(u, v, Δx, Δy, C_s, Δ)
L1  for each grid point (i, j), indices taken modulo the grid size:
L2      S11 ← (u[i+1,j] - u[i-1,j]) / (2Δx); S22 ← (v[i,j+1] - v[i,j-1]) / (2Δy)
L3      S12 ← ((u[i,j+1] - u[i,j-1]) / (2Δy) + (v[i+1,j] - v[i-1,j]) / (2Δx)) / 2
L4      |S| ← sqrt(2 (S11^2 + S22^2 + 2 S12^2))
L5      ν_r[i,j] ← (C_s Δ)^2 |S|
L6  return ν_r
```

Lines L2 and L3 are [finite differences](/finite-difference-method/) with error $O(\Delta x^2)$, and L4 counts $S_{12}$ and $S_{21}$ once each. The cost is a constant number of operations per point, $O(N)$ for $N$ points in the real RAM. In 3D the same lines run over the nine velocity derivatives.

## What it counts

The model gives the subgrid eddy viscosity $\nu_r$, the modeled subgrid stress, and the subgrid dissipation $\varepsilon_{sgs} = -\tau_{ij}\bar S_{ij} = \nu_r|\bar S|^2$: the rate at which resolved kinetic energy is drained into the unresolved scales. Inside an LES it fixes the resolved field, and with it every statistic the LES reports.

## Relation to other models

- **Mixing length.** It is Prandtl's [mixing length model](/mixing-length-model/) with $\ell = C_s\Delta$ and $|dU/dy|$ replaced by $|\bar S|$; in a pure shear $dU/dy$, $|\bar S| = |dU/dy|$ and the two have the same form.
- **Dynamic model.** The [dynamic model](/dynamic-subgrid-model/) keeps the form and computes $(C_s)^2$ in space and time from a second, coarser test filter. It removes the need to fit $C_s$ and lets the viscosity vanish in laminar regions and near walls.
- **RANS models.** RANS eddy viscosities such as the [k-epsilon model](/k-epsilon-model/) model all of the turbulence and are far larger; the Smagorinsky viscosity models only the part below the grid scale and goes to zero as $\Delta \to 0$.
- **Other subgrid models.** Scale-similarity and mixed models, and models designed to vanish in pure shear and near walls, are the main alternatives in LES.

## Known results in the model

**Lilly's constant (derived under stated assumptions).** Assume a sharp spectral cutoff at $k_c = \pi/\Delta$ inside an inertial range with $E(k) = C_K\varepsilon^{2/3}k^{-5/3}$, and replace $\langle|\bar S|^3\rangle$ by $\langle|\bar S|^2\rangle^{3/2}$. The resolved strain is $\langle|\bar S|^2\rangle = 2\int_0^{k_c}k^2E(k)\,dk = \frac{3}{2}C_K\varepsilon^{2/3}k_c^{4/3}$. Setting the mean model dissipation equal to $\varepsilon$ gives
$$\varepsilon = (C_s\Delta)^2\left(\tfrac{3}{2}C_K\right)^{3/2}\varepsilon\, k_c^2 \quad\Longrightarrow\quad C_s = \frac{1}{\pi}\left(\frac{2}{3C_K}\right)^{3/4}.$$
For $C_K = 1.5$, $2/(3 \times 1.5) = 0.4444$, its 3/4 power is 0.5443, and $C_s = 0.173$; for $C_K = 1.6$, $C_s = 0.165$. The tests check both. The value depends on the filter and on the approximation of the third moment, so it is an estimate.

**No backscatter (theorem in the model).** $\varepsilon_{sgs} = \nu_r|\bar S|^2 \ge 0$ at every point, because $\nu_r \ge 0$. Energy can only go from the resolved scales to the subgrid ones. Filtered DNS data show local backscatter, energy going the other way in parts of the flow, which the model cannot represent (measurement).

**Strain cases by hand.** A pure shear $\partial\bar u/\partial y = \gamma$ has $|\bar S| = \gamma$. A plane strain $\partial\bar u/\partial x = a$, $\partial\bar v/\partial y = -a$ has $|\bar S| = 2a$. A solid-body rotation has $\bar S_{ij} = 0$, so $\nu_r = 0$. In SI units, with $\Delta = 1$ cm, $|\bar S| = 50$ 1/s and $C_s = 0.1$, $\nu_r = (0.001)^2 \times 50 = 5 \times 10^{-5}$ m^2/s, about three times the viscosity of air.

**Taylor-Green field (exact, checked by the tests).** For $u = -\cos x\sin y$, $v = \sin x\cos y$ on $[0, 2\pi)^2$, $\bar S_{11} = \sin x\sin y = -\bar S_{22}$ and $\bar S_{12} = 0$, so $|\bar S| = 2|\sin x\sin y|$. A central difference of $\sin$ on spacing $h$ gives exactly $\cos$ times $\sin(h)/h$, so on a uniform grid the computed $|\bar S|$ is exactly $\frac{\sin h}{h}$ times the true one. With 32 points, $h = 0.19635$ and $\sin(h)/h = 0.993587$. At $x = y = \pi/2$ with $C_s = 0.17$ and $\Delta = h$, $\nu_r = (0.17 \times 0.19635)^2 \times 2 \times 0.993587 = 2.214 \times 10^{-3}$ in the units of the box.

**Known defects (measurement and theorem).** In a laminar shear flow the model gives $\nu_r = (C_s\Delta)^2\gamma > 0$, so it damps disturbances that should grow in transition. At a wall $|\bar S|$ is largest while the true subgrid stress goes to zero, so without damping it gives too much viscosity there. Point by point, the modeled stress correlates poorly with the exact one in filtered DNS data, even when the mean dissipation is right. The best fitted $C_s$ differs from flow to flow: near 0.17 to 0.2 in isotropic turbulence and near 0.1 in channel flow.

## References
