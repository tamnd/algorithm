---
tag: SYEY5V
kind: technique
slug: rhie-chow-interpolation
name: Rhie-Chow interpolation
aliases:
- momentum interpolation
area: scientific-computing/incompressible-flow-and-turbulence
level: advanced
summary: "Interpolates face velocities on a collocated grid with a pressure-gradient correction, which removes checkerboard pressure modes."
model: real-ram
prereqs: [finite-volume-method, simple-algorithm, navier-stokes-equations]
see_also: [marker-and-cell-method, mac-grid, piso-algorithm, inf-sup-condition, taylor-hood-element, artificial-compressibility-method, chorin-projection-method]
sources:
  - paper: doi:10.2514/3.8284
    title: C. M. Rhie and W. L. Chow, Numerical study of the turbulent flow past an airfoil with trailing edge separation, AIAA Journal 21(11) (1983) 1525-1532
    locator: the momentum interpolation of face velocities on a nonstaggered grid
  - paper: doi:10.1080/10407788808913607
    title: S. Majumdar, Role of underrelaxation in momentum interpolation for calculation of flow with nonstaggered grids, Numerical Heat Transfer 13(1) (1988) 125-132
    locator: the dependence of the converged solution on the under-relaxation factor and its removal
  - book: isbn:9783319996912
    title: Joel H. Ferziger, Milovan Perić and Robert L. Street, Computational Methods for Fluid Dynamics, 4th edition, Springer, 2020
    locator: pressure-velocity coupling on colocated grids
---

Rhie-Chow interpolation, also called momentum interpolation, computes the velocity on the faces of a collocated finite volume grid, where all unknowns sit at the cell centers. Simple linear interpolation of the cell velocities lets a pressure field that alternates from cell to cell, the checkerboard, pass through the continuity equation unseen, because the central pressure difference over two cells does not see it. Rhie and Chow (1983) built the face velocity from the discrete momentum equation instead: the face velocity is the interpolated velocity without its pressure gradient, plus a pressure gradient taken directly across the face. The two gradients differ only for rough pressure fields, so the change is small for smooth flow, but it couples neighboring cells and removes the checkerboard. It made collocated grids practical for [SIMPLE](/simple-algorithm/) type solvers on general meshes, and it is widely used in collocated finite volume codes. A known defect is that the converged result can depend on the under-relaxation factor and the time step; Majumdar (1988) showed how to remove the dependence on under-relaxation.

## In plain words

Store the pressure and the velocity at the center of each cell. To know how much fluid passes between two cells you need the velocity on the wall between them. The easy guess is the average of the two neighboring velocities. But each cell velocity was pushed by a pressure difference that skips over the cell itself and compares the cells on both sides. A pressure that goes high, low, high, low then pushes nothing anywhere, and the solver cannot remove it. Rhie and Chow take the average velocity, remove the push that came from the skipping pressure difference, and put back the push from the pressure on the two sides of this very wall. For smooth pressure this changes almost nothing. For the high, low pattern it gives a strong push, so the pattern is removed.

## When it applies

- **Collocated grids.** All variables at cell centers, as on unstructured and curvilinear meshes, where a staggered grid like the [MAC grid](/mac-grid/) is hard to build.
- **Pressure-based solvers.** SIMPLE, [PISO](/piso-algorithm/) and their relatives, which build a pressure or pressure-correction equation from the face mass fluxes.
- **Low-order equal-order discretizations.** The checkerboard is the finite volume form of the instability that equal-order finite elements show when they fail the [inf-sup condition](/inf-sup-condition/); Rhie-Chow plays the role of a pressure stabilization.

## The template

**Notation.** In the momentum equation of cell $P$, discretized and under-relaxed,

$$a_P u_P = \sum_{nb} a_{nb} u_{nb} + b_P - V_P (\nabla p)_P, \qquad \hat u_P = \frac{\sum_{nb} a_{nb} u_{nb} + b_P}{a_P}, \qquad d_P = \frac{V_P}{a_P},$$

so $u_P = \hat u_P - d_P(\nabla p)_P$, where $(\nabla p)_P$ is the central gradient over the two neighbors. For a face $f$ between cells $P$ and $E$ at distance $h$, write $\overline{x}_f$ for linear interpolation. **The Rhie-Chow face velocity** is

$$u_f = \overline{\hat u}_f - \overline{d}_f\,\frac{p_E - p_P}{h} = \overline{u}_f - \overline{d}_f\left(\frac{p_E - p_P}{h} - \overline{\nabla p}_f\right).$$

The second form shows that it is linear interpolation plus a term that compares the compact pressure difference across the face with the interpolated cell gradients. On a uniform grid, for smooth $p$, a Taylor series gives $(p_E - p_P)/h - \overline{\nabla p}_f = -\tfrac{h^2}{4}\,p'''_f + O(h^4)$, so the change is of the order $d\,h^2$. In SIMPLE the face velocities, not the cell velocities, enter continuity, and the pressure correction equation becomes the compact Laplacian.

```pseudo id=main
SIMPLE-ITERATION-WITH-RHIE-CHOW(u, u_f, p)
L1  û_P ← (Σ a_nb u_nb + b_P) / a_P        ▷ relaxed momentum without the pressure
L2  u*_P ← û_P - d_P (∇p)_P                ▷ cell velocity
L3  u*_f ← avg(û)_f - d_f (p_E - p_P) / h  ▷ Rhie-Chow face velocity
L4  solve Σ_f d_f (p'_E - p'_P) / h · A_f = Σ_f u*_f A_f for p'
L5  u_f ← u*_f - d_f (p'_E - p'_P) / h; u ← u* - d (∇p')_P; p ← p + α_p p'
L6  return (u, u_f, p)
```

**Majumdar's correction.** With under-relaxation factor $\alpha$, the relaxed coefficients are $a_P/\alpha$, so $d = \alpha V/a_P$ and $\hat u$ contains $(1 - \alpha)u_P^{\text{old}}$. At a fixed point the cell velocities solve the steady equations for every $\alpha$, but the face velocity is $\overline{u}_f - \alpha\,(V/a_P)(\ldots)$, so its pressure term, and with it the converged pressure, depends on $\alpha$. Adding $(1 - \alpha)(u_f^{\text{old}} - \overline{u^{\text{old}}}_f)$ to $u^*_f$ in line L3 gives, at the fixed point, $\alpha(u_f - \overline{u}_f) = -\alpha(V/a_P)(\ldots)$, which is free of $\alpha$. The same algebra applies to a transient solver, where $a_P$ contains $V/\Delta t$ and $\hat u$ contains $u^n$: the plain formula makes the result depend on $\Delta t$, and its smoothing term vanishes as $\Delta t \to 0$.

## Classic examples

**The checkerboard by hand.** On a periodic 1D grid of width $h = 1$ with $a_P = V = 1$, let $p = (1, -1, 1, -1, \ldots)$. The central gradient $(p_{i+1} - p_{i-1})/2$ is 0 in every cell, so the cell velocities and linear face velocities do not change, and continuity cannot see this pressure. The compact difference across a face is $\pm 2$, so the Rhie-Chow face velocities change by $\mp 2$, alternating from face to face, and their divergence is $\pm 4$ in each cell. The test file checks in exact fractions that on 8 cells the continuity operator of linear interpolation has rank 6 (null space: constants and the checkerboard) and the Rhie-Chow operator has rank 7 (constants only).

**Relaxation dependence.** The 1D periodic model $c u - \nu u_{xx} = s - p_x$ with $c = 1$, $\nu = 0.01$ and $s = 1 + \sin 2\pi x + 0.5\sin 6\pi x$, solved by SIMPLE with $\alpha_p = 0.3$ to a tolerance of $10^{-12}$. The table gives the largest difference between the converged pressure and the one for $\alpha = 1$:

| cells | $\alpha = 0.7$, plain | $\alpha = 0.3$, plain | with Majumdar's term |
|---|---|---|---|
| 16 | 2.05e-3 | 5.20e-3 | below 1e-15 |
| 32 | 1.79e-4 | 4.21e-4 | below 1e-15 |
| 64 | 1.15e-5 | 2.69e-5 | below 2e-15 |

The face velocities are equal to 1 (the mean of $s$ divided by $c$) to $10^{-10}$ in every case, and the cell momentum equations hold. The dependence falls with the grid size: here about as $h^4$, because the viscous term makes $a_P$ grow like $1/h^2$, so $d$ is of order $h^2$ and the added term of order $h^4$. These are measurements from the implementation on this page.

## Variations

- **Majumdar's relaxation-independent form** (above), and similar terms that remove the time step dependence in transient solvers.
- **Different interpolations of $d$.** Linear or harmonic means of $d_P$ and $d_E$; on nonuniform and skewed grids the face gradient needs a non-orthogonal correction.
- **Body forces and sharp pressure jumps.** Buoyancy or surface tension forces at faces must be treated in the same way as the pressure gradient (a balanced force formulation), or spurious velocities appear.
- **Other pressure stabilizations.** Staggered grids avoid the problem from the start, and in finite elements, stable pairs such as the [Taylor-Hood element](/taylor-hood-element/) or pressure stabilized formulations do the same job.

## Pitfalls

- **Dependence on relaxation and time step.** With the plain formula the converged answer changes with $\alpha$ and $\Delta t$; the change is of the order of the discretization error, but it means that two runs of the same problem can disagree.
- **Small time steps.** Since $d$ scales like $\Delta t$ in transient runs, very small steps weaken the smoothing term and checkerboard modes can return.
- **Inconsistent $d$.** The $d$ used in the face velocity must be the one of the pressure correction equation, or mass is not conserved at convergence.
- **Forces other than pressure.** A body force that is interpolated linearly while the pressure is treated in the Rhie-Chow way breaks the balance between them in hydrostatic or capillary equilibrium.
- **Not a cure for everything.** It removes the checkerboard of the pressure; it does not fix the velocity checkerboard of central advection at high cell Reynolds number.

## Exercises

1. Show that the central cell gradient of $p_i = (-1)^i$ is zero, and that linear interpolation therefore gives a continuity equation with a two-dimensional null space on an even periodic grid.
2. Show that $(p_E - p_P)/h - \overline{\nabla p}_f = -\tfrac{h^2}{4}p'''_f + O(h^4)$ on a uniform grid.
3. Derive the face velocity at a fixed point of SIMPLE with under-relaxation $\alpha$, and show that Majumdar's term removes $\alpha$.
4. For a transient solver with $a_P = a_P^0 + V/\Delta t$, find how the plain Rhie-Chow face velocity at convergence of one step depends on $\Delta t$.

## References
