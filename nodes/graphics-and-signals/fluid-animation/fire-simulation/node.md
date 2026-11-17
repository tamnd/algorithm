---
tag: QHWFYD
kind: algorithm
slug: fire-simulation
name: Nguyen-Fedkiw-Jensen fire
aliases:
- physically based fire animation
area: graphics-and-signals/fluid-animation
level: advanced
summary: "Animate fire with a level set for the thin blue core that moves with the fuel plus a flame speed, and two incompressible flows, fuel and hot products, joined by jump conditions at the core."
solves: [fluid-simulation-for-animation]
model: real-ram
complexity:
  vars: {n: "the number of grid cells", s: "the number of level set substeps per step", k: "the number of conjugate gradient iterations of the pressure solve"}
  time: {level_set: "Θ(s n)", pressure: "O(n k)", redistance: "O(n log n)", step: "O(s n + n log n + n k)"}
  space: {extra: "Θ(n)"}
properties: {deterministic: true, exact: false, unconditionally_stable: false, conservative: false}
history:
  year: 2002
  people: [Duc Quang Nguyen, Ronald Fedkiw, Henrik Wann Jensen]
  note: Nguyen, Fedkiw and Jensen brought the thin flame model of combustion to animation, with the ghost fluid method for the jumps and blackbody rendering.
prereqs: [stable-fluids, mac-grid, level-set-method, ghost-fluid-method, boussinesq-buoyancy, vorticity-confinement]
see_also: [fluid-simulation-for-animation, navier-stokes-equations, fast-marching-method, poisson-equation, conjugate-gradient-method, upwind-scheme, signed-distance-function, particle-level-set]
sources:
  - paper: doi:10.1145/566570.566643
    title: "Duc Quang Nguyen, Ronald Fedkiw and Henrik Wann Jensen, Physically based modeling and animation of fire, ACM Transactions on Graphics 21(3), 721-728, 2002 (SIGGRAPH 2002)"
    locator: "sections 3.1 to 3.3 (blue core, equation 1; jump conditions, equations 2 and 3; solid fuels, equations 4 and 5), section 4 (level set, equations 6 and 7; ghost velocities, equations 12 and 13; buoyancy and vorticity confinement, equations 14 and 15; temperature, equations 16 and 17), section 6 (the constants)"
  - paper: doi:10.1006/jcph.2001.6812
    title: "Duc Q. Nguyen, Ronald P. Fedkiw and Myungjoo Kang, A boundary condition capturing method for incompressible flame discontinuities, Journal of Computational Physics 172, 71-98, 2001"
    locator: the pressure solve with the jump conditions, which the fire paper refers to
  - paper: doi:10.1006/jcph.1999.6236
    title: "Ronald P. Fedkiw, Tariq Aslam, Barry Merriman and Stanley Osher, A non-oscillatory Eulerian approach to interfaces in multimaterial flows (the ghost fluid method), Journal of Computational Physics 152, 457-492, 1999"
    locator: the ghost fluid method
  - paper: doi:10.1016/0021-9991(88)90002-2
    title: "Stanley Osher and James A. Sethian, Fronts propagating with curvature-dependent speed: algorithms based on Hamilton-Jacobi formulations, Journal of Computational Physics 79(1), 12-49, 1988"
    locator: the level set method
---

The fire method of Nguyen, Fedkiw and Jensen (2002) animates flames from gas or solid fuel on a grid. It uses the thin flame model from combustion science: the reaction happens on a surface, the blue core, that separates the gaseous fuel from the hot products. A [level set](/level-set-method/) tracks this surface, and the surface moves with the fuel plus a flame speed $S$ into the fuel. The fuel and the products are two incompressible flows with different densities. Where they meet, conservation of mass and momentum gives a jump in the normal velocity and in the pressure. The [ghost fluid method](/ghost-fluid-method/) carries these jumps through the advection and the pressure solve. The jump in velocity is the expansion of the gas as it burns, and the paper shows that it makes the flames look fuller. Buoyancy, [vorticity confinement](/vorticity-confinement/) and a temperature model for the color complete the method. The name "physically based" means that the method uses physical quantities and states its approximations, not that the result is accurate.

## In plain words

A gas flame has a thin blue sheet where the fuel burns. Inside it is fuel, outside are hot gases.

The method keeps a number in every grid cell that says how far the cell is from the sheet, and on which side. Each step, the sheet moves with the fuel flow and also eats into the fuel at a fixed speed.

Hot gas is lighter than fuel, so the same mass takes more room. The gas must leave the sheet faster than the fuel arrives, and the pressure drops across the sheet. The method keeps two flows, one for the fuel and one for the hot gas, and links them at the sheet with these two rules. Then the hot gas rises, cools and changes color from white to yellow to red.

## The problem

Given a domain with walls, fuel injectors and open boundaries, animate the fuel, the blue core and the hot products. The input is the fuel density $\rho_f$, the product density $\rho_h < \rho_f$, the flame speed $S$ of the fuel, and the temperatures $T_{air}$, $T_{ign}$ and $T_{max}$. Speeds are low compared with sound, so both gases are treated as incompressible, which avoids the small time steps of a compressible solver. The output each frame is the velocity, the level set $\varphi$ and the temperature $T$, which a renderer turns into the color of a blackbody.

**The jump conditions.** Let $\varphi > 0$ in the fuel, and let $V$ be the normal velocity along the normal that points from the fuel to the products. The front moves at $D = V_f - S$: the fuel crosses it at the speed $S$. Conservation of mass and momentum across the front (the paper's equations 2 and 3) are

$$\rho_h (V_h - D) = \rho_f (V_f - D), \qquad \rho_h (V_h - D)^2 + p_h = \rho_f (V_f - D)^2 + p_f,$$

and they give

$$V_h = V_f + \left(\frac{\rho_f}{\rho_h} - 1\right) S, \qquad p_h = p_f - \left(\frac{\rho_f}{\rho_h} - 1\right) \rho_f S^2.$$

The tangential velocity is the same on both sides. The paper writes $\mathbf n = \nabla \varphi / |\nabla \varphi|$, which points into the fuel, for the motion of the level set, and the jump formulas hold with $V$ measured along $-\mathbf n$.

## The algorithm

Let $J = (\rho_f / \rho_h - 1) S$ and $P = (\rho_f / \rho_h - 1) \rho_f S^2$. Velocities live on the faces of a [MAC grid](/mac-grid/), and $\varphi$, $p$ and $T$ in the cells.

```pseudo id=main
FIRE-STEP(φ, u, T, Δt)
L1  w <- u_f + S n at each cell, with n = ∇φ / |∇φ| by central differences and u_f the fuel velocity
L2  φ <- φ - Δt (w · ∇φ) by upwind differences, in substeps that keep |w| Δt / Δx at most 1/2; then redistance φ
L3  form the fuel and the product velocity on every face: on the other side, add or subtract J m (ghost values)
L4  advect each velocity field by itself; each face keeps the field of the material that is at the face now
L5  advect T by the product velocity with the ghost value T_max in the fuel; set T_ign in the fuel; apply the cooling
L6  v <- v + Δt α (T - T_air) on the vertical faces
L7  solve ∇·(∇p / ρ) = ∇·u* / Δt with the pressure jump P across the front, by the ghost fluid method
L8  u <- u* - Δt ∇p / ρ, with the same jump
```

**The level set (L1, L2).** The front moves with $\mathbf w = \mathbf u_f + S \mathbf n$, so $\varphi_t = -\mathbf w \cdot \nabla \varphi$ (the paper's equation 6). The paper solves it with first order upwind differences (its equation 7). In the products, $\mathbf u_f$ is the ghost fuel velocity of line L3. The paper takes the incompressible step about five times larger than the CFL limit of the level set, and moves $\varphi$ in substeps, which cuts the number of pressure solves by about five. It keeps $\varphi$ close to a signed distance with the [fast marching method](/fast-marching-method/). Without this, $\varphi$ gets steep in the products, the upwind gradient grows, and the front eats the fuel too fast. In a test of the code here without redistancing, the core of a nozzle flame grew and then burned away.

**Ghost velocities (L3, L4).** The paper's equations 12 and 13 give the product velocity in the fuel region: take the fuel velocity, keep its tangential part, and add $J$ to its normal part. The reverse gives the fuel velocity in the products. A semi-Lagrangian backtrace that crosses the front then reads the velocity of its own material, so the jump is not smeared. The code stores one value per face, the velocity of the material at the face, and makes the other one when it needs it.

**Temperature (L5).** The paper follows a reaction coordinate $Y$ with $Y_t = -(\mathbf u \cdot \nabla) Y - k$, so $1 - Y$ is the time since a gas element crossed the core, and maps it to a temperature curve that an animator can shape. For large flames it uses a ghost value instead: a backtrace that looks into the fuel reads $T_{max}$. Past the peak, $T$ cools by $-c_T ((T - T_{air}) / (T_{max} - T_{air}))^4$ (the paper's equation 17), which the code integrates exactly. A density for the smoke follows the same pattern.

**Forces (L6).** Buoyancy is $\alpha (T - T_{air})$ upward (equation 14), the temperature term of [Boussinesq buoyancy](/boussinesq-buoyancy/). Vorticity confinement $\varepsilon h (\mathbf N \times \boldsymbol\omega)$ (equation 15) adds back small swirls; the paper uses a different $\varepsilon$ for the fuel and the products. The code here leaves it out.

**Pressure (L7, L8).** Each gas has its own density, and the pressure jumps by $P$ at the front. In the equation of a cell, the pressure of a neighbor on the other side is replaced by its ghost value, the pressure plus or minus $P$. The known jump goes to the right side, and the matrix stays symmetric. The code gives a face that crosses the front the density $\hat\rho = \theta \rho_a + (1 - \theta) \rho_b$, where $\theta$ is the part of the face segment on the side of cell $a$, from the values of $\varphi$. The paper refers to Nguyen, Fedkiw and Kang (2001) for the details of its solver.

**Solid fuel.** A solid that burns is a fuel source. Mass conservation at its surface gives the gas speed $V_s + (\rho_s / \rho_f - 1) S$ (equation 5). The paper injects gas at this speed from the voxels on the surface of a burning object.

## Example

**The jumps by hand.** With $\rho_f = 1$ kg/m³, $\rho_h = 0.2$ kg/m³ and $S = 0.5$ m/s, $\rho_f / \rho_h - 1 = 4$. The products leave the core $J = 2$ m/s faster than the fuel arrives, and the pressure drops by $P = 4 \cdot 1 \cdot 0.25 = 1$ Pa. The paper uses $S = 0.5$ m/s for most of its examples and compares $\rho_h = 0.2$, $0.1$ and $0.05$ with $\rho_f = 1$ in its figure 7:

| $\rho_h$ (kg/m³) | $J$ (m/s) | $P$ (Pa) |
|---|---|---|
| 0.2 | 2.0 | 1.0 |
| 0.1 | 4.5 | 2.25 |
| 0.05 | 9.5 | 4.75 |

For the flamethrower of the paper's section 6, $S = 0.1$ m/s, $\rho_f = 1$ and $\rho_h = 0.01$, so $J = 9.9$ m/s while the fuel enters at 30 m/s.

**A planar flame, measured.** A channel of 16 by 3 cells of 5 cm has an injector at one end that pushes fuel at 0.5 m/s, and an open end. The front is 6.75 cells from the injector side. With the velocities of the table's first row, three steps of 0.02 s keep the front, the fuel speed 0.5 m/s and the product speed 2.5 m/s to $10^{-10}$, and the pressure is 1 Pa in the fuel and 0 in the products. This holds for fronts that face $+x$, $-x$ and $+y$. If the whole channel starts at 0.5 m/s, one step brings the products to 2.5 m/s. The pressure of that step also holds the impulse that accelerates them: 1 Pa per cell over the 8 product cells.

**A nozzle flame, measured.** A grid of 12 by 16 cells of 5 cm has a wall at the bottom with a nozzle 0.2 m wide that injects fuel at 1.5 m/s, and an open top. With $S = 0.5$ m/s, $\rho_h = 0.2$ and no buoyancy, after 25 steps of 0.02 s the core reaches 0.176 m above the nozzle. With $S = 0.75$ m/s it reaches only 0.023 m. The paper's equation 1, $v_f A_f = S A_S$, says the same: the core area that burns the injected fuel shrinks as $S$ grows. For a triangle in 2D, it gives the heights 0.283 m and 0.173 m. The simulated cores are shorter: the fuel does not move at one speed, and the grid has only 4 cells across the nozzle.

## Correctness

The claims are proved in [proofs/correctness.md](proofs/correctness.md).

1. **Jump conditions.** The formulas for $V_h$ and $p_h$ satisfy the conservation of mass and momentum exactly, and the tangential velocity does not jump.
2. **The front.** For a planar front in fuel at rest, the scheme moves the front at exactly $S$.
3. **The projection.** If each fluid region touches an open cell, the pressure system is symmetric positive definite, and after line L8 every cell has zero divergence when the faces are read in its own material.
4. **The planar flame.** The steady planar flame is an exact fixed point of the step, with the pressure jump $P$.
5. **The expansion.** In a channel, one step gives the fuel speed $S$ and the product speed $S + J$ from any start that is uniform across the channel.
6. **Temperature.** The cooling is integrated exactly, and $T$ stays in $[T_{air}, T_{max}]$.

These are statements about the discrete scheme. The model itself is an approximation: a real reaction zone has a thickness, $S$ depends on the mixture, and in a diffusion flame the burning rate depends on how the fuel mixes with air. The paper says that the thin flame model works well for visual work, not that it is exact.

## Complexity

Let $n$ be the number of cells. Lines L3 to L6 and L8 cost $\Theta(n)$. Line L2 costs $\Theta(n)$ per substep, and the number of substeps $s$ is about $\Delta t \max |\mathbf w| / (\Delta x / 2)$. Fast marching redistancing costs $O(n \log n)$; the brute force search in the code costs $\Theta(n c)$ for $c$ crossing points, which is good enough for the small test grids. The pressure solve of line L7 costs $O(n)$ per conjugate gradient iteration, and it is the most expensive part. Without a preconditioner, the number $k$ of iterations is $O(\sqrt{\kappa})$, and the density ratio raises the condition number $\kappa$. So one step costs $O(s n + n \log n + n k)$. The space is $\Theta(n)$.

## Properties

- **Two flows, one grid.** The fuel and the products each satisfy their own incompressible equations, and only the jump conditions couple them.
- **Sharp jumps.** Ghost values keep the velocity and pressure jumps at the front, without a smeared transition zone.
- **Volume is not conserved.** The front is a source of volume: the products need $\rho_f / \rho_h$ times the volume of the fuel they replace.
- **Not stable for every step.** The upwind level set step has a CFL limit, so it needs substeps. The flow part uses the semi-Lagrangian step of [stable fluids](/stable-fluids/).
- **Controllable.** $S$ sets the size of the core, $\rho_f / \rho_h$ sets the expansion, and the temperature curve and $\varepsilon$ are free for the artist.

## Variants and improvements

- **Solid fuels.** Inject gas from the surface of a burning object at the speed of equation 5, and turn this on or off per voxel to light or put out parts of the object.
- **Temperature curves.** Use the reaction coordinate $Y$ and a curve shaped by hand, or the $T_{max}$ ghost value for large flames.
- **Smoke.** Carry a soot density with the products; rendered by its absorption, it shows the smoke above the flame.
- **Rendering.** The paper ray marches the products as a participating medium, uses Planck's formula for the emitted spectrum, and maps it to RGB with a von Kries adaptation to the brightest color, so that the flame does not look too red.
- **Explosions and detonations.** These are fast and compressible, so a different solver is needed.

## When to use it

Use it for flames whose blue core and expansion matter: torches, burners, flamethrowers and burning objects at a scale where the grid resolves the core. For small flames in games, a texture or a particle system costs much less. For smoke without a reaction, use [stable fluids](/stable-fluids/) with [buoyancy](/boussinesq-buoyancy/) and leave out the level set.

## Pitfalls

- **The sign of the normal.** The jump formulas need the normal from the fuel to the products. With the normal $\nabla \varphi / |\nabla \varphi|$ of the level set, the signs flip. A wrong sign makes the products slower than the fuel.
- **No redistancing.** The upwind step then moves the front too fast where $\varphi$ is steep, and the core burns away.
- **A closed domain.** The front adds volume, so the pressure system of a closed box has no solution. Give the products an outlet.
- **Mixing the two velocities.** A backtrace from the products that lands in the fuel must read the ghost product velocity, not the fuel velocity. Otherwise the jump smears over a few cells.
- **Too large a level set step.** The level set has a CFL limit even though the flow step does not. Use substeps.
- **Buoyancy that is too strong.** With $\alpha = 0.15$ m/(K s²) as in the paper's section 6 and $T - T_{air}$ near 1700 K, the acceleration is over 250 m/s². On a coarse grid this can pull the core apart; in the nozzle test of this page, it shrinks the core to a few cells.

## Implementations

## History

Markstein (1964) first proposed the thin flame model in combustion science. Before 2002, fire in graphics used textured shapes, flame spread models, or a given velocity field that carried temperature and density with an advection-diffusion equation (Stam and Fiume 1995). Fedkiw, Aslam, Merriman and Osher (1999) introduced the ghost fluid method for jumps at interfaces in compressible flow, and Nguyen, Fedkiw and Kang (2001) used it for incompressible flames with the jump conditions. In 2002, Nguyen, Fedkiw and Jensen brought this solver to animation, together with the blue core, solid fuels, objects that catch fire, and blackbody rendering with chromatic adaptation.

## References
