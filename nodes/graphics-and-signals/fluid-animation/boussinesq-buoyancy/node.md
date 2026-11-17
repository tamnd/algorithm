---
tag: QV9FZM
kind: model
slug: boussinesq-buoyancy
name: Boussinesq buoyancy
aliases:
- Boussinesq approximation
area: graphics-and-signals/fluid-animation
level: core
summary: "Model the lift of hot gas and the weight of smoke by an upward force linear in temperature and smoke density, in a flow that keeps one constant density."
prereqs: [navier-stokes-equations, stable-fluids]
see_also: [fluid-simulation-for-animation, vorticity-confinement, fire-simulation, mac-grid, heat-equation, advection-equation, poisson-equation, chorin-projection-method]
sources:
  - paper: doi:10.1145/383259.383260
    title: "Ronald Fedkiw, Jos Stam and Henrik Wann Jensen, Visual simulation of smoke, Proceedings of SIGGRAPH 2001, 15-22"
    locator: "section 2 (the incompressible Euler equations 1 and 2, the advection of T and of the smoke density, equations 6 and 7, and the buoyancy force, equation 8), section 4 (forces at the voxel centers, added before the advection)"
  - paper: doi:10.1086/146849
    title: "Edward A. Spiegel and George Veronis, On the Boussinesq approximation for a compressible fluid, The Astrophysical Journal 131, 442, 1960"
    locator: the conditions under which the density can be kept constant except in the gravity term
  - paper: doi:10.1145/566570.566643
    title: "Duc Quang Nguyen, Ronald Fedkiw and Henrik Wann Jensen, Physically based modeling and animation of fire, ACM Transactions on Graphics 21(3), 721-728, 2002 (SIGGRAPH 2002)"
    locator: "section 4, equation 14 (the temperature term alone), and section 6 (the constant 0.15 m/(K s^2))"
  - book: isbn:9781482232837
    title: "Robert Bridson, Fluid Simulation for Computer Graphics, second edition, CRC Press, 2015"
    locator: the chapter Smoke (temperature and smoke concentration, buoyancy)
---

Boussinesq buoyancy is the force that makes hot smoke rise in most smoke solvers for animation. Fedkiw, Stam and Jensen (2001) write it as

$$\mathbf f_{buoy} = \big(-\alpha\, s + \beta\, (T - T_{amb})\big)\, \hat{\mathbf y},$$

where $s$ is the smoke density, $T$ the temperature, $T_{amb}$ the temperature of the surrounding air, $\hat{\mathbf y}$ the unit vector up, and $\alpha, \beta \ge 0$ two constants. The paper writes $\rho$ for the smoke density and $\mathbf z$ for the up vector; this page uses $s$ so that $\rho$ can stay the density of the air. The flow itself keeps one constant density and stays incompressible. The change of density that heat and smoke cause enters only through this force, which is the idea of Boussinesq: keep the density difference where gravity acts on it, and nowhere else. The model is an empirical approximation. It is close to the physics only for small differences of temperature and density, and graphics uses it with $\alpha$ and $\beta$ tuned by eye, often far outside that range.

## The machine

**The quantities.** On a domain with walls, the state is the velocity $\mathbf u$ (m/s), the pressure $p$ (Pa), the temperature $T$ (K) and the smoke density $s$. The air has the constant density $\rho_0$ (kg/m³). The smoke density is in kg/m³ of soot, or a concentration without units, as the user chooses; $\alpha$ takes the matching units.

**The equations.** With the force above,

$$\nabla \cdot \mathbf u = 0, \qquad \frac{\partial \mathbf u}{\partial t} + (\mathbf u \cdot \nabla)\, \mathbf u = -\frac{1}{\rho_0} \nabla p + \mathbf f_{buoy} + \mathbf f_{other},$$

$$\frac{\partial T}{\partial t} + (\mathbf u \cdot \nabla)\, T = 0, \qquad \frac{\partial s}{\partial t} + (\mathbf u \cdot \nabla)\, s = 0.$$

The last two are the paper's equations 6 and 7: $T$ and $s$ are carried by the flow and do not act on it except through $\mathbf f_{buoy}$. Here $p$ is the pressure minus the hydrostatic pressure of the ambient air. The paper uses the inviscid form of the [Navier-Stokes equations](/navier-stokes-equations/); $\mathbf f_{other}$ holds, for example, [vorticity confinement](/vorticity-confinement/).

**The parameters.**

| symbol | meaning | units | range |
|---|---|---|---|
| $\beta$ | lift per kelvin above ambient | m/(s² K) | $\beta \ge 0$; $g / T_{amb} \approx 0.033$ for an ideal gas at 300 K |
| $\alpha$ | weight per unit of smoke | m/s² per unit of $s$ | $\alpha \ge 0$; $g / \rho_0 \approx 8.2$ m⁴/(kg s²) for soot in kg/m³ in air |
| $T_{amb}$ | ambient temperature | K | $T_{amb} > 0$ |
| $s$, $T$ | smoke density, temperature | as above | $s \ge 0$; the force is zero at $s = 0$, $T = T_{amb}$ |

The paper calls $\alpha$ and $\beta$ two positive constants with units that make the equation meaningful. Nguyen, Fedkiw and Jensen (2002) keep only the temperature term for fire. They write $\alpha$ for its coefficient and use $0.15$ m/(K s²), about five times the ideal gas value.

**Where the linear law comes from.** Start from $\rho\, D\mathbf u / Dt = -\nabla p_{full} - \rho g \hat{\mathbf y}$, and write $\rho = \rho_0 + \rho'$ and $p_{full} = p_0 + p$ with $\nabla p_0 = -\rho_0 g \hat{\mathbf y}$, the hydrostatic pressure of the air at rest. Keep $\rho'$ only in the gravity term and divide by $\rho_0$:

$$\frac{D\mathbf u}{Dt} = -\frac{1}{\rho_0} \nabla p - g\, \frac{\rho'}{\rho_0}\, \hat{\mathbf y}.$$

A density that falls linearly with temperature, $\rho' = -\rho_0 \beta_T (T - T_{amb})$, gives the term $g \beta_T (T - T_{amb})$, so $\beta = g \beta_T$. For an ideal gas at fixed pressure, $\rho \propto 1/T$, and the slope at $T_{amb}$ is $\beta_T = 1/T_{amb}$. Soot of mass $s$ per unit volume adds about $\rho' = s$, if the volume of the soot itself is neglected, which gives $\alpha = g / \rho_0$.

**The standing assumptions.**

1. The density differences are small, $|\rho'| \ll \rho_0$, so the inertia on the left uses $\rho_0$.
2. The density depends linearly on $T$ and $s$.
3. The flow is slow compared with sound, so it is incompressible and the gas does not expand as it heats.
4. The air far away is at rest, at the uniform temperature $T_{amb}$, in hydrostatic balance.
5. Heat and smoke do not diffuse, cool or decay. Solvers for animation often add such terms by hand; they are not part of the force.

**On a MAC grid.** $T$ and $s$ live at the cell centers of a [MAC grid](/mac-grid/) and the force is vertical, so it is added to the $v$ faces, each with the mean of the two cells below and above it. Then the solver advects and projects, as in [stable fluids](/stable-fluids/).

```pseudo id=main
SMOKE-STEP(u, s, T, Δt)
L1  f(s, T) = -α s + β (T - T_amb)                ▷ upward acceleration
L2  for each v face: s_f, T_f ← means of the two cells below and above
L3      v ← v + Δt f(s_f, T_f)
L4  advect u, s and T by u
L5  project u                                       ▷ removes the part of f that is a gradient
```

Lines L2 and L3 cost $\Theta(n)$ on a grid of $n$ cells, small next to the pressure solve of line L5.

## What it counts

The model predicts the acceleration that differences of temperature and smoke from the ambient air give to the flow: hot gas rises, smoke sinks, and the pressure pushes the rest of the fluid out of the way. Not all of the force makes motion. The projection removes the part that is a gradient, and a force that depends only on the height is a gradient. What drives the flow is the change of the force along the horizontal. Take the curl of the momentum equation in 2D, with $\omega = \partial v / \partial x - \partial u / \partial y$:

$$\frac{D\omega}{Dt} = \frac{\partial f_y}{\partial x} = \beta\, \frac{\partial T}{\partial x} - \alpha\, \frac{\partial s}{\partial x}.$$

So the model makes rotation where hot and cold gas sit side by side. A hot blob gets a pair of opposite swirls, one on each side, that carry it up through its center and bring cooler gas down at its sides. This is the rolling rise of smoke.

The model does not predict the expansion of gas as it heats, because the flow keeps one density. It does not predict pressure waves or sound, the real rise speed of very hot gas, the cooling of the gas, or the detail below the grid scale. It also says nothing on how the solver keeps the swirls; numerical dissipation removes them, and [vorticity confinement](/vorticity-confinement/) is the usual remedy.

## Relation to other models

- **The full Navier-Stokes equations.** The [Navier-Stokes equations](/navier-stokes-equations/) for a gas let the density vary everywhere. The buoyancy model keeps it constant except in gravity. A variable density solve keeps $\rho$ in the pressure equation as well, at a higher cost.
- **The ideal gas.** The exact density difference of an ideal gas at fixed pressure, as a fraction of $\rho_{amb}$, is $(T - T_{amb}) / T$. The model replaces it by its tangent $(T - T_{amb}) / T_{amb}$ at $T_{amb}$. The error is computed below.
- **Fire.** The [fire method](/fire-simulation/) of Nguyen, Fedkiw and Jensen (2002) uses the temperature term alone. It models the expansion that this model leaves out by a jump of the velocity at the burning surface, not by buoyancy.
- **Convection with diffusion.** With viscosity and the diffusion of the [heat equation](/heat-equation/) added to the equation of $T$, the same model gives the classic equations of Rayleigh-Bénard convection in fluid dynamics.
- **Pure advection.** Without the force, $T$ and $s$ follow the [advection equation](/advection-equation/) and do not change the flow at all. They are then only dye.

## Known results in the model

**A layered fluid stays at rest (proved).** If $T$ and $s$ depend only on the height $y$, then $\mathbf f_{buoy} = f(y) \hat{\mathbf y} = \nabla F$ with $F(y) = \int f\, dy$. The pressure $p = \rho_0 F$ balances it, and $\mathbf u = 0$ stays a solution. This holds for hot gas above and for hot gas below. On a MAC grid it holds exactly: the force on each row of $v$ faces is the difference of a potential between the rows of cells, so the [Chorin projection](/chorin-projection-method/) removes it. The tests check $|\mathbf u| < 10^{-12}$ after one force step and one projection, for a uniform $T$ of 400 K and for both linear layerings. The layering with hot gas below is a state of rest, but the vorticity equation above shows that any horizontal difference of $T$ in it starts a rotation; in physics this is the onset of convection.

**The linear law against the ideal gas (proved by algebra).** The ratio of the model force $\beta (T - T_{amb})$, with $\beta = g / T_{amb}$, to $g (\rho_{amb} - \rho) / \rho_{amb} = g (T - T_{amb}) / T$ is $T / T_{amb}$. For $T_{amb} = 300$ K:

| $T$ (K) | 303 | 330 | 600 | 2000 |
|---|---|---|---|---|
| model force (m/s²) | 0.098 | 0.981 | 9.81 | 55.6 |
| ideal gas, $g (T - T_{amb}) / T$ (m/s²) | 0.097 | 0.892 | 4.91 | 8.34 |
| ratio | 1.01 | 1.1 | 2.0 | 6.67 |

So the linear law is within 1% for a difference of 3 K and off by a factor of 2 at 600 K. Hot smoke and fire are far outside the range of the derivation, and in that range $\beta$ is a tuning value, not a property of the gas.

**No net flow through a horizontal line (proved).** In a closed box the projected velocity has zero divergence and zero normal velocity at the walls. By the divergence theorem on the part of the box below any height, the net flow up through that height is zero. So the rise of hot gas is always paid for by a sinking of other gas. The tests check that the sum of $v$ over each row of faces is below $10^{-10}$ after a hot blob gets one kick.

**A hot blob, one step (measured).** On a $16 \times 24$ grid with $\Delta x = 1/16$ m and walls, a Gaussian blob with $\sigma = 0.1$ m and a peak 300 K above ambient, centered at $(0.5, 0.4)$ m, with $\beta = 0.0327$ m/(s² K) and $\Delta t = 0.05$ s, the face at the center of the blob gets the kick $\Delta t\, \beta\, (T_f - T_{amb}) = 0.418$ m/s. After the projection it moves at $0.198$ m/s up. The projection removes more than half of the kick, which is the pressure pushing back. The velocity next to the side walls points down. The field is the mirror image of itself about the vertical line through the blob.

**A hot blob, several steps (measured).** With the same setup and only the force, semi-Lagrangian advection and projection, the height of the center of the excess temperature was

| step | 0 | 4 | 8 | 12 |
|---|---|---|---|---|
| height (m) | 0.400 | 0.449 | 0.549 | 0.666 |
| peak $T$ (K) | 600 | 539 | 486 | 441 |

The blob speeds up as it rises. The model has no diffusion of heat, so the fall of the peak comes from the interpolation in the advection, not from the model.

**Heavy smoke sinks (measured).** A blob of smoke at ambient temperature with $\alpha = 0.5$ gets a downward velocity at its center and an upward one at the side walls, the mirror of the hot blob.

## References
