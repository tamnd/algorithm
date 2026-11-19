---
tag: 7VRC33
kind: algorithm
slug: front-tracking-method
name: Front tracking method
aliases:
- Unverdi-Tryggvason method
area: scientific-computing/incompressible-flow-and-turbulence
level: advanced
summary: Represents the interface by a moving surface mesh that carries surface tension and is coupled to a fixed grid for the flow.
solves: [navier-stokes-equations]
model: real-ram
complexity:
  vars: {M: "the number of front points", N: "the number of grid cells along each side", K: "the number of time steps", S: "the cost of one step of the grid flow solver"}
  time: {worst: "Θ(K (M + S))"}
  space: {extra: "Θ(M + N^2)"}
properties: {deterministic: true, sharp_interface: true, lagrangian_interface: true, zero_net_tension_force: true, conserves_volume: "approximately", topology_changes: "need extra work"}
history:
  year: 1992
  people: [Salih O. Unverdi, Gretar Tryggvason]
  note: "Unverdi and Tryggvason (1992) moved a connected front of marker points through a fixed grid and linked the two with the smoothed delta functions of the immersed boundary method of Peskin. Tryggvason and co-workers (2001) reviewed the method and its uses."
prereqs: [navier-stokes-equations, immersed-boundary-method, chorin-projection-method]
see_also: [volume-of-fluid-method, piecewise-linear-interface-calculation, level-set-method, continuum-surface-force, particle-level-set, marker-and-cell-method, ghost-fluid-method, shoelace-formula]
sources:
  - paper: doi:10.1016/0021-9991(92)90307-K
    title: "Salih O. Unverdi and Gretar Tryggvason, A front-tracking method for viscous, incompressible, multi-fluid flows, Journal of Computational Physics 100 (1992) 25-37"
    locator: "the front of connected marker points, the transfer between front and grid, and the indicator function"
  - paper: doi:10.1006/jcph.2001.6726
    title: "G. Tryggvason, B. Bunner, A. Esmaeeli, D. Juric, N. Al-Rawahi, W. Tauber, J. Han, S. Nas and Y.-J. Jan, A front-tracking method for the computations of multiphase flow, Journal of Computational Physics 169 (2001) 708-759"
    locator: "the surface tension on front elements, the restructuring of the front and the validation tests"
  - paper: doi:10.1017/S0962492902000077
    title: "Charles S. Peskin, The immersed boundary method, Acta Numerica 11 (2002) 479-517"
    locator: "the construction of the 4-point delta function from its moment conditions"
---

The front tracking method computes flows of two fluids, such as bubbles in a liquid, by keeping two separate meshes: a fixed grid on which the [Navier-Stokes equations](/navier-stokes-equations/) are solved, and a moving mesh of connected points that is the interface itself (a curve in 2D, a triangulated surface in 3D). The interface points move with the fluid velocity, interpolated from the grid. In return, the interface computes the surface tension from its own geometry and spreads it onto the grid as a force, with the smoothed delta function of the [immersed boundary method](/immersed-boundary-method/). Since the interface is explicit, its position, normal and curvature are known to high accuracy, and the interface stays sharp. The price is bookkeeping: the front must be refined as it stretches, and drops that merge or break up need special treatment.

## In plain words

Imagine a bubble rising in water, drawn as a ring of beads joined by threads. The water is computed on a fixed grid of squares, as usual. In each step, every thread pulls on the beads at its two ends with a force equal to the surface tension, so a curved ring is pulled inward, harder where it bends more. These pulls are passed to the nearby grid squares as forces on the water. The flow solver then finds the new water velocity. Each bead reads the velocity from the nearby grid squares and moves with it. When threads become too long, a new bead is put in the middle; when beads come too close, one is taken out. The beads always show exactly where the bubble surface is.

## The problem

Solve the incompressible Navier-Stokes equations for two immiscible fluids separated by a moving interface $\Gamma$, with density $\rho$ and viscosity $\mu$ that jump across $\Gamma$, and a surface tension force $\sigma\kappa n$ concentrated on $\Gamma$, where $\sigma$ is the surface tension coefficient, $\kappa$ the curvature and $n$ the normal. In the one-fluid form used by front tracking this is

$$\rho(\partial_tu + u \cdot \nabla u) = -\nabla p + \nabla \cdot \mu(\nabla u + \nabla u^T) + \int_\Gamma\sigma\kappa n\,\delta(x - X(s))\,ds, \qquad \nabla \cdot u = 0,$$

and the interface moves with the fluid, $dX/dt = u(X)$. The output is the velocity on the grid and the position of the interface after $K$ steps. On this page the grid is $N \times N$ cell centers of spacing $h = 1/N$ in the periodic unit square, and the front is a closed polygon $X_1, \dots, X_M$ in counterclockwise order.

## The algorithm

```pseudo id=main
FRONT-TRACKING(X, u, Δt, K)
L1  for k ← 1 to K
L2      F_k ← σ (t_{k+1/2} - t_{k-1/2}) for every front point k   ▷ surface tension
L3      f ← Σ_k F_k δ_h(x - X_k)                                  ▷ spread to the grid
L4      u ← FLOW-STEP(u, f, Δt)                                   ▷ ρ and μ from the front
L5      U_k ← Σ_ij u_ij δ_h(x_ij - X_k) h²                        ▷ interpolate to the front
L6      X_k ← X_k + Δt U_k                                        ▷ midpoint rule in the code
L7      split elements longer than l_max, drop points closer than l_min
L8  return X, u
```

**Surface tension (line L2).** With $t_{k+1/2}$ the unit tangent of the element from $X_k$ to $X_{k+1}$, the force on point $k$ is $\sigma(t_{k+1/2} - t_{k-1/2})$: each element pulls its two end points toward each other with the tension $\sigma$. Since $dt/ds = \kappa n$, this is the integral of $\sigma\kappa n$ over the half elements on both sides of the point. This is the form described by Tryggvason and co-workers (2001), and its forces on a closed front add up to exactly zero.

**Front to grid and back (lines L3 and L5).** The smoothed delta function is $\delta_h(x, y) = \phi(x/h)\phi(y/h)/h^2$ with Peskin's 4-point kernel

$$\phi(r) = \tfrac18\bigl(3 - 2|r| + \sqrt{1 + 4|r| - 4r^2}\bigr) \text{ for } |r| \le 1, \qquad \phi(r) = \tfrac18\bigl(5 - 2|r| - \sqrt{-7 + 12|r| - 4r^2}\bigr) \text{ for } 1 \le |r| \le 2,$$

and $\phi = 0$ beyond. The same weights are used in both directions, so spreading and interpolation are adjoint, and each front point touches a block of $4 \times 4$ grid points.

**The flow step (line L4).** Any grid solver can be used; Unverdi and Tryggvason used a conservative finite difference method on a fixed grid, and a projection method on a staggered grid, as in the [MAC method](/marker-and-cell-method/), is the usual choice. The density and viscosity on the grid come from an indicator function $I$, which is 1 in one fluid and 0 in the other. To find it, the jump of $I$ times the normal is spread from the front like a force, giving a grid approximation $G$ of $\nabla I$, and the Poisson equation $\nabla^2I = \nabla \cdot G$ is solved. The code on this page takes the flow step as a parameter, and the tests use a prescribed velocity, so they check the front part of the method on its own.

**Restructuring (line L7).** In a stretching flow the elements grow, and in a compressing flow they shrink. The code splits each element longer than $l_{\max}$ into equal parts and then drops points that are closer than $l_{\min}$ to the previous kept point. In 3D the front is a triangulation, and the same job is done by splitting, collapsing and flipping edges.

## Example

**A corner, by hand.** For the unit square with corners $(0, 0), (1, 0), (1, 1), (0, 1)$ and $\sigma = 1$, the point $(1, 0)$ has $t_{k-1/2} = (1, 0)$ and $t_{k+1/2} = (0, 1)$, so its force is $(-1, 1)$, pointing into the square with length $\sqrt2 = 2\sin(\pi/4)$. The four forces add up to zero. For a regular polygon with $M$ points on a circle of radius $R$, each force has length $2\sigma\sin(\pi/M)$ and points to the center; divided by the element length $2R\sin(\pi/M)$ it is $\sigma/R$, the force per length of the Young-Laplace law.

**The Laplace pressure jump.** In a drop at rest the pressure balances the surface tension, $\nabla p = f$, so the jump of $p$ across the interface is the integral of the spread force across it. In 2D the exact jump is $\sigma/R$. For a circle of radius $R = 0.25$ centered on a cell center, with $\sigma = 1$, integrating $f_x$ along the grid row through the center gave:

| $N$ | $M$ | front spacing / $h$ | $\Delta p\,R/\sigma$ |
|---|---|---|---|
| 32 | 64 | 0.79 | 1.0155 |
| 32 | 128 | 0.39 | 0.9989 |
| 64 | 128 | 0.79 | 1.0159 |
| 64 | 256 | 0.39 | 0.9990 |

The error depends on the front spacing compared with $h$, not on $h$ itself: with about two front points per grid cell, the jump is within 0.1%. In all cases the total spread force was zero to $10^{-16}$.

**Advection.** A circle of radius 0.15 at $(0.5, 0.75)$ with 64 points turns once in the prescribed rotation $u = -2\pi(y - \frac12)$, $v = 2\pi(x - \frac12)$, interpolated from a $32 \times 32$ grid. Since the kernel reproduces linear fields, only the time step matters:

| steps | 50 | 100 | 200 |
|---|---|---|---|
| max point error | 0.0066 | 0.0017 | 0.00041 |
| area change | $3.1 \cdot 10^{-3}$ | $3.9 \cdot 10^{-4}$ | $4.9 \cdot 10^{-5}$ |

The point error falls as $\Delta t^2$, as for the midpoint rule. The area is not kept exactly: the front has no built-in volume conservation, which is the main difference from the [volume of fluid method](/volume-of-fluid-method/). In the shear flow $u = y - \frac12$, a circle of radius 0.2 with 40 points was stretched for $t = 2$ with $l_{\min} = 0.01$ and $l_{\max} = 0.03$. The first restructuring split every element into two, and the front ended with 110 points, all elements between 0.013 and 0.027 long. No point was dropped, so the area stayed the same to $3 \cdot 10^{-15}$.

## Correctness

The [proof file](proofs/correctness/) shows four exact facts. The forces of line L2 on a closed front have zero sum and zero torque, because each element pulls its two end points with equal and opposite forces along the element. Peskin's kernel has $\sum_j\phi(r - j) = 1$ and $\sum_j(r - j)\phi(r - j) = 0$ for every $r$. So spreading keeps the total force and the total torque, and the grid flow gets no net momentum or angular momentum from surface tension, while interpolation is exact for linear velocity fields. Splitting elements does not change the front. The accuracy of the coupled method, with a real flow solver, is a matter of measurement; Tryggvason and co-workers (2001) report the tests.

## Complexity

Lines L2, L3, L5 and L6 cost $\Theta(M)$, with a constant of 16 grid points per front point for each transfer. Restructuring costs $\Theta(M)$. So a step costs $\Theta(M + S)$, where $S$ is the cost of the flow step, and a run $\Theta(K(M + S))$. With $M = \Theta(N)$ points on a 2D grid, the front is cheap compared with the grid solve: a fast Poisson solver gives $S = \Theta(N^2\log N)$ in 2D. Memory is $\Theta(M + N^2)$. The indicator function needs one more Poisson solve per step.

## Properties

- **Sharp interface.** The fluid properties jump over a few grid cells, set by the width of $\delta_h$, and the interface position is known to the accuracy of the front points, not of the grid.
- **Accurate curvature.** The surface tension comes from the front geometry, which is smooth, so the force is much less noisy than curvature computed from volume fractions.
- **Zero net force from surface tension**, exactly, as the proof shows. This rules out the self-propulsion of a drop by its own surface tension.
- **Volume is kept only approximately.** The enclosed area changes with the time-stepping error and with each dropped point, as the advection table shows. Long runs correct it.
- **Topology changes are not automatic.** Two drops that touch do not merge until the code finds the close fronts and reconnects them.

## Variants and improvements

- **Level contour reconstruction.** Shin and Juric rebuild the front from a contour of the indicator function every few steps, which makes merging and breakup automatic in 3D and removes most of the restructuring code.
- **Mass correction.** Codes move the front points a little along the normal after each step to restore the volume of each drop.
- **Hybrid methods.** The front can be combined with a [level set](/level-set-method/) or with the [volume of fluid method](/volume-of-fluid-method/), using the front for curvature and the other method for topology and conservation.
- **Other force forms.** Surface tension can be computed per element with the curvature of a fitted curve, which is more accurate for coarse fronts but no longer sums to exactly zero.
- **Front tracking for shocks.** In compressible gas dynamics, front tracking of Glimm and co-workers follows shocks and contact discontinuities as moving curves. It has the same name but solves the jump conditions at the front, not a one-fluid equation.

## When to use it

Use front tracking for flows where the interface shape and the surface tension must be very accurate and the topology does not change often: rising bubbles, drops in shear, deformable cells and capsules, and flows with surfactants that live on the interface. It is also the natural choice when quantities are carried on the interface, because the front points can store them. For flows with much breakup and merging, such as atomization, the [volume of fluid method](/volume-of-fluid-method/) or a [level set](/level-set-method/) is simpler. For surface tension on those methods, see the [continuum surface force](/continuum-surface-force/) model.

## Pitfalls

- **Unresolved front.** With front points much farther apart than $h$, the spread force has gaps; the Laplace table shows 1.6% error at 0.79 points per cell. Keep the front spacing near $h/2$ to $h$.
- **Over-refined front.** Front points much closer than $h/4$ add work and give short elements whose tangents are noisy. Drop them, as line L7 does.
- **Volume drift.** The front is not conservative. Monitor the volume of each drop and correct it.
- **Merging and breakup.** Two fronts that come within a few grid cells interact through the smoothed fields, but do not join. Decide when they should, and reconnect them.
- **Periodic wrap.** The moment identities of the kernel use the true coordinates of the grid points. When a front crosses a periodic boundary, shift the coordinates before spreading.
- **Parasitic currents.** Even with exact force balance, the pressure on the grid cannot balance a smoothed force exactly, so a drop at rest shows small spurious velocities. They are much smaller than with curvature from volume fractions, but they are there.

## Implementations

## History

The immersed boundary method of Peskin, built in the 1970s for heart valves, gave the idea of a Lagrangian structure that spreads its forces onto a fixed grid with a smoothed delta function. Unverdi and Tryggvason (1992) used this idea for the interface between two fluids, with a front of connected points, an indicator function found from the front, and the one-fluid Navier-Stokes equations on a fixed grid. Tryggvason and co-workers developed the method for bubbly flows, boiling, solidification and flows with surfactants, and their review (Tryggvason et al. 2001) describes it in detail. Peskin (2002) reviewed the immersed boundary method and the construction of its delta functions.

## References
