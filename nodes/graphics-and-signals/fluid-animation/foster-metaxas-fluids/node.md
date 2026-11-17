---
tag: NBGCFG
kind: algorithm
slug: foster-metaxas-fluids
name: Foster-Metaxas liquid animation
aliases:
- realistic animation of liquids
area: graphics-and-signals/fluid-animation
level: advanced
summary: Animate liquids by explicit finite differences of the Navier-Stokes equations on a MAC grid, a cell-by-cell pressure iteration and marker particles for the surface.
solves: [fluid-simulation-for-animation]
model: real-ram
complexity:
  vars: {g: "the number of grid cells", m: "the number of marker particles", k: "the number of pressure sweeps"}
  time: {velocity: "Θ(g)", pressure: "O(g k)", markers: "Θ(m)", step: "O(g k + m)"}
  space: {extra: "Θ(g + m)"}
properties: {deterministic: true, exact: false, unconditionally_stable: false, explicit: true}
history:
  year: 1996
  people: [Nick Foster, Dimitri Metaxas]
  note: Foster and Metaxas brought the marker-and-cell method of computational fluid dynamics into computer animation, with free surfaces, obstacles and control of the liquid by the animator.
prereqs: [mac-grid, marker-and-cell-method, navier-stokes-equations, finite-difference-method]
see_also: [stable-fluids, successive-over-relaxation, courant-friedrichs-lewy-condition, chorin-projection-method, level-set-method, particle-level-set, fluid-implicit-particle, volume-of-fluid-method]
sources:
  - paper: doi:10.1006/gmip.1996.0039
    title: "Nick Foster and Dimitri Metaxas, Realistic animation of liquids, Graphical Models and Image Processing 58(5), 471-483, 1996"
    locator: "Section 3 (the grid, equations 2 to 10 and the boundary rules), Section 4.1 (markers), Section 6 (the algorithm) and Section 8 (examples)"
  - paper: doi:10.1063/1.1761178
    title: "Francis H. Harlow and J. Eddie Welch, Numerical calculation of time-dependent viscous incompressible flow of fluid with free surface, The Physics of Fluids 8(12), 2182-2189, 1965"
    locator: "the marker-and-cell method: the staggered grid and the marker particles"
  - paper: doi:10.1145/383259.383261
    title: "Nick Foster and Ronald Fedkiw, Practical animation of liquids, SIGGRAPH 2001, 23-30"
    locator: "the later solver with semi-Lagrangian advection and a level set with particles"
---

The Foster-Metaxas method (1996) is an early full 3D Navier-Stokes solver for liquids in computer animation. It brought the [marker-and-cell method](/marker-and-cell-method/) of Harlow and Welch from engineering into graphics. It stores the velocity on a [MAC grid](/mac-grid/), moves it by explicit finite differences, removes the divergence by a cell-by-cell pressure iteration, and tracks the liquid with massless marker particles. Special rules set the velocity at the free surface. The method is explicit, so its time step must stay small. That limit is the main thing that [stable fluids](/stable-fluids/) removed three years later.

## In plain words

The space is cut into a grid of boxes. Small markers float in the liquid and show where it is. A box with markers next to an empty box is on the surface.

Each step does four things. First it changes the speed of the liquid on each box wall: the flow carries speed along, gravity pulls down, pressure pushes from high to low, and friction evens out the speeds. Next it visits each full box in turn and fixes its walls. If more liquid flows out than in, the box lowers its pressure and its walls let less out, and if more flows in, it does the opposite. It repeats the visits until every full box is balanced. Then simple rules set the walls of the surface boxes. Last, each marker moves with the local speed.

The steps must be short, or the numbers grow out of control.

## The problem

Animate a liquid with a free surface in a box with walls. The liquid moves by the incompressible [Navier-Stokes equations](/navier-stokes-equations/), written with the kinematic pressure $p$ (pressure divided by density), as in the paper:

$$\frac{\partial \mathbf u}{\partial t} = -(\mathbf u \cdot \nabla)\mathbf u - \nabla p + \nu \nabla^2 \mathbf u + \mathbf g, \qquad \nabla \cdot \mathbf u = 0.$$

Above the liquid is air at a fixed pressure, taken as 0. At each frame the animator needs the shape of the liquid, for rendering. Small details of the flow matter less than a plausible shape, so this is a case of [fluid simulation for animation](/fluid-simulation-for-animation/).

## The algorithm

The paper's Section 6 lists nine steps: set up the obstacles and the liquid, set the initial pressure and velocity, and then loop over labeling the cells, setting the boundary values, computing the new velocity, iterating the pressure, fixing the surface cells and moving the markers. This page shows the loop in 2D with square cells and free-slip walls, as in the paper's examples. The paper is in 3D with $\delta x$, $\delta y$ and $\delta z$ allowed to differ, and it also has obstacle cells inside the grid.

```pseudo id=main
FOSTER-METAXAS-STEP(u, v, p, markers, dt)
L1  label each cell EMPTY if it has no marker, SURFACE if it has an EMPTY neighbor, else FULL
L2  on each u face with a liquid side: u~ <- u + dt (-d(u^2)/dx - d(uv)/dy - dp/dx + nu lap u + g_x)
L3  on each v face with a liquid side: v~ <- v + dt (-d(uv)/dx - d(v^2)/dy - dp/dy + nu lap v + g_y)
L4  repeat: for each FULL cell c in a fixed order:
L5      D <- -(divergence of c); dp <- beta D with beta = beta0 dx^2 / (4 dt)
L6      add (dt / dx) dp to the outward velocity of each face of c not on a wall; p_c <- p_c + dp
L7  until |divergence| < eps in every FULL cell
L8  on each SURFACE cell, set the faces toward EMPTY cells by the free surface rules
L9  move each marker: x <- x + dt U(x), with U interpolated from the four nearest faces
```

**Labels (L1).** The paper calls this step 3 and adds a fourth label for obstacle cells. A cell with no marker is EMPTY. A cell with a marker next to an EMPTY cell is SURFACE. Every other cell with a marker is FULL.

**Velocity (L2, L3).** These are equation 2 of the paper: one forward Euler step with central differences, in conservative form ($\partial u^2 / \partial x$ instead of $u\, \partial u / \partial x$). A value that the grid does not store, such as $u$ at a cell center, is the average of its two neighbors, and the square of a quantity is the square of that average. The pressure of a SURFACE or EMPTY cell is the air pressure 0. At a free-slip wall, the normal velocity is 0, and a tangential velocity outside the wall copies the one inside. The paper also allows no-slip walls, where the outside value is the negative of the inside one.

**Pressure (L4 to L7).** These are equations 5 to 9. $D$ is the "missing mass" of the cell. One update moves all open faces of the cell by the same amount, in the direction that cancels the divergence. With $\beta_0 = 1$, an interior cell ends exactly balanced, but the update changes the divergence of its neighbors. So the paper sweeps over all FULL cells until the largest divergence is below $\varepsilon$, and it chooses $\beta_0$ in $[1, 2]$ to speed this up. This is [successive over-relaxation](/successive-over-relaxation/) on the pressure Poisson equation, and $\beta_0$ is the relaxation factor. The paper reports 3 to 6 sweeps on average in its examples with $\beta_0 = 1.7$ and $\varepsilon = 0.0001$, starting each step from the old pressure.

**Surface (L8).** These are the rules of Section 3.2.3. A SURFACE cell with one face toward an EMPTY cell sets that face so that the divergence of the cell is 0 (equation 10). With two such faces on different axes, each copies the face opposite it. With three, the face opposite the liquid copies, and the other two keep the value from equation 2, so they follow gravity. In 3D a surface cell has 64 cases. The paper does not state the 2D case of two open faces on the same axis, which is a column one cell wide. The code of this page moves both by the same amount so that the divergence is 0.

**Markers (L9).** The paper interpolates the velocity at a marker by area weighting of the four nearest values, which is [bilinear interpolation](/bilinear-interpolation/), and moves the marker by forward Euler. The markers carry no mass and do not take part in the velocity computation.

## Example

**One cell update by hand.** Take an interior FULL cell with $\Delta x = 0.1$ m and $\Delta t = 0.01$ s. Its faces have $u_{\text{left}} = 0.2$, $u_{\text{right}} = 0.5$, $v_{\text{bottom}} = 0.1$ and $v_{\text{top}} = 0$, all in m/s. The divergence is $(0.5 - 0.2 + 0 - 0.1)/0.1 = 2$ per second, so $D = -2$. With $\beta_0 = 1$, $\beta = 0.1^2 / (4 \cdot 0.01) = 0.25$ m²/s, so $\delta p = -0.5$ m²/s², and each outward velocity changes by $(0.01/0.1)(-0.5) = -0.05$ m/s:

| face | left $u$ | right $u$ | bottom $v$ | top $v$ | divergence (1/s) | $\frac12 \sum w^2$ |
|---|---|---|---|---|---|---|
| before | 0.20 | 0.50 | 0.10 | 0.00 | 2 | 0.150 |
| after | 0.25 | 0.45 | 0.15 | -0.05 | 0 | 0.145 |

The cell is balanced, and the energy drops by $0.005$, which is $F^2 / (2 n) = 0.2^2 / 8$ with the net outflow $F = 0.2$ m/s and $n = 4$ open faces. With $\beta_0 = 1.7$ the update overshoots, to a divergence of $-1.4$, but over a sweep it moves the error away faster.

**The effect of $\beta_0$, measured.** A random velocity in a closed box full of liquid, from `random.Random(1)`, $\Delta t = 0.01$ s, reduced to $\varepsilon = 10^{-4}$:

| grid | $\beta_0 = 1$ | $1.5$ | $1.7$ | $1.9$ |
|---|---|---|---|---|
| 8 by 8 | 139 | 65 | 47 | 77 |
| 16 by 16 | 402 | 155 | 83 | 102 |

The best $\beta_0$ is near 1.7 here, and the count grows with the grid. The paper's small counts probably come from starting each step at the old pressure, where the velocity is already nearly balanced. The still pool below shows the same effect.

**A still pool and a dam break, measured.** A pool 6 cells deep in a 12 by 12 box, with 4 markers per cell, $\Delta t = 0.005$ s and $\varepsilon = 10^{-8}$, stays at rest for 40 steps: the largest velocity is $2.5 \times 10^{-10}$ m/s. The first step needs 134 sweeps to build the hydrostatic pressure, and from the third step on no sweep is needed. A column of water 0.25 m wide and 0.5 m tall in a 0.8 m box (16 by 16 cells, 200 markers, $\Delta t = 0.004$ s, $\varepsilon = 10^{-4}$) collapses. Its front moves from 0.25 m to 0.30 m after 20 steps, 0.46 m after 40 steps and 0.66 m after 60 steps. Each step takes 34 to 53 sweeps, and the CFL number stays below 0.25.

## Correctness

The claims are about the discrete step. They are proved in [proofs/correctness.md](proofs/correctness.md).

1. **One cell update.** It multiplies the divergence of the cell by $1 - \beta_0 n_c / 4$, where $n_c$ is the number of faces not on a wall. It lowers the kinetic energy by $\frac{F^2}{2 n_c} \omega (2 - \omega)$, with $\omega = \beta_0 n_c / 4$, so for $\beta_0 \le 2$ the energy never increases.
2. **The pressure iteration is the projection.** For $0 < \beta_0 < 2$, the sweeps converge linearly to the orthogonal projection of the velocity onto the fields with zero divergence in every FULL cell. That is the same velocity as the projection of the shared helper `macgrid.py` with FULL cells as FLUID and the other cells as AIR. If each group of FULL cells touches the surface, the pressures are also the same.
3. **Surface rules.** A SURFACE cell with one or two faces toward EMPTY cells ends with zero divergence.
4. **Rest.** A pool at rest with the hydrostatic pressure stays at rest.
5. **Step limit.** In a linear model, the explicit viscous term is stable in 2D only for $\nu \Delta t / \Delta x^2 \le \frac14$. Central advection with viscosity in 1D is stable if and only if $c^2 \le 2r \le 1$, and without viscosity it grows a little at every step size.

The tests check each claim: the update formula on every cell of a random field, the match with the helper in a closed box and with a free surface, the surface rules, the hydrostatic pressure, the still pool, the viscous limit through the full code, and the dam break.

## Complexity

Let $g$ be the number of cells and $m$ the number of markers. Labels, the new velocity, the surface rules and the extra velocity layer cost $\Theta(g)$, and the markers cost $\Theta(m)$. One pressure sweep costs $\Theta(g)$, so the iteration costs $O(g k)$ for $k$ sweeps. From a cold start on an $N$ by $N$ grid, $k$ grows with $N$, about as $N^2$ for $\beta_0 = 1$ and as $N$ at the best $\beta_0$, which are the rates of Gauss-Seidel and optimal SOR on the Poisson equation. The extra space is $\Theta(g + m)$.

The total cost to a fixed time $T$ is the cost per step times $T / \Delta t$, and the explicit step bounds $\Delta t$ by both $\Delta x / |\mathbf u|_{\max}$ and about $\Delta x^2 / (4 \nu)$. Halving $\Delta x$ in 3D multiplies the cells by 8 and at least halves $\Delta t$.

## Properties

- **Explicit.** The velocity step is forward Euler. It needs the CFL limit of the paper's equation 3 and a viscous limit, so it is not unconditionally stable.
- **Exact projection in the limit.** The iteration converges to the same divergence-free field as a direct Poisson solve. With a finite $\varepsilon$ it stops early, so each FULL cell keeps a divergence up to $\varepsilon$.
- **Less numerical diffusion than semi-Lagrangian advection.** Central differences do not smooth the flow the way interpolation does, so small swirls last longer, as long as the step is stable.
- **Volume is not conserved exactly.** The liquid is the set of cells with a marker, and that set can grow or shrink as markers spread or bunch.
- **Local and simple.** Each part touches a cell and its neighbors only, which made it practical on the hardware of 1996.

## Variants and improvements

- **Obstacles, inflow and outflow.** The paper's Section 3.2 sets the boundary values for obstacle cells inside the grid, with free-slip or no-slip walls, and for sources and sinks of liquid.
- **Control.** Section 7 lets the animator steer the liquid through inflow and outflow and through a time history of pressure applied at the surface.
- **Hot gas.** Foster and Metaxas (1997) used the same kind of solver for a hot, turbulent gas.
- **Semi-Lagrangian liquids.** Foster and Fedkiw (2001) replaced the explicit advection by the semi-Lagrangian step of [stable fluids](/stable-fluids/), and the markers by a [level set](/level-set-method/) corrected with particles. This led to the [particle level set](/particle-level-set/) method.
- **Direct pressure solves.** Later solvers replace the sweeps by conjugate gradients or [multigrid](/multigrid-method/) on the same 5-point system.
- **Particle velocities.** [PIC](/particle-in-cell/) and [FLIP](/fluid-implicit-particle/) give the markers a velocity of their own and use them for the advection too.

## When to use it

Use it to study the history of liquid animation, or as a small explicit solver where the time step is already small for another reason, such as fast contact or high viscosity in a short shot. Its central differences keep more detail than a first order semi-Lagrangian step at the same grid size.

For most new work, use a semi-Lagrangian or particle-grid solver with a level set or particles for the surface. They allow large steps and give a smoother surface than marker cells.

## Pitfalls

- **Too large a step.** Equation 3 keeps the CFL number below 1, but the viscous term needs $\nu \Delta t / \Delta x^2 \le \frac14$ in 2D (and $\frac16$ in 3D), and central advection needs viscosity or a small step. Check all limits each step.
- **Too few sweeps.** A loose $\varepsilon$ leaves divergence, which shows as liquid that gains or loses volume.
- **$\beta_0$ out of range.** For $\beta_0 > 2$ an interior cell update can increase the energy, and the iteration can diverge. At $\beta_0 = 2$ an interior update only flips the sign of the divergence.
- **The surface pressure.** The pressure of a SURFACE cell is the air pressure. A FULL cell next to it sees the surface at the center of the SURFACE cell, half a cell away from where the markers may be.
- **Blocky surface.** Marker cells give a surface made of whole cells. Render a smooth surface built from the markers, not the cell labels.
- **Empty faces.** Markers near the surface read faces that the solver did not set. Give those faces a value, for example by one layer of extrapolation as the code here does.
- **Run-to-run cost.** The number of sweeps depends on the flow, so the cost per frame is not fixed.

## Implementations

## History

Harlow and Welch published the marker-and-cell method in 1965 at Los Alamos, with the staggered grid and marker particles for a free surface. In 1996 Nick Foster and Dimitri Metaxas adapted it for computer animation in "Realistic animation of liquids" (the title of the paper, which is the alias of this page). They added obstacles inside the grid and control by the animator, with examples such as a jet of water and a falling drop. Their 1997 SIGGRAPH paper used a similar solver for hot gas. Stam's stable fluids (1999) removed the explicit step limit, and Foster and Fedkiw (2001) combined that idea with a level set to build the liquid solvers that graphics has used since.

## References
