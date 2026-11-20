---
tag: A8MSVS
kind: technique
slug: adaptive-mesh-refinement
name: Adaptive mesh refinement
aliases:
- adaptive grid refinement
area: scientific-computing/conservation-laws-and-shock-capturing
level: core
summary: Refines the grid during a run where an error indicator is large and coarsens it where the solution is smooth.
model: real-ram
prereqs: [finite-volume-method, quadtree]
see_also: [berger-colella-amr, adaptive-finite-element-method, octree, multigrid-method, richardson-extrapolation, adaptive-quadrature, z-order-curve, domain-decomposition]
sources:
  - paper: "Marsha J. Berger and Joseph Oliger, Adaptive mesh refinement for hyperbolic partial differential equations, Journal of Computational Physics 53(3) (1984) 484-512"
    locator: the hierarchy of nested rotated grids, the Richardson error estimate for tagging, regridding and subcycling in time
  - paper: doi:10.1016/0021-9991(89)90035-1
    title: Marsha J. Berger and Phillip Colella, Local adaptive mesh refinement for shock hydrodynamics, Journal of Computational Physics 82(1) (1989) 64-84
    locator: aligned patches on a hierarchy of levels, the conservative flux correction at coarse-fine faces, tagging and buffer zones
---

Adaptive mesh refinement (AMR) changes the grid while a computation runs. An error indicator is computed in every cell. Cells where it is large are tagged and replaced by finer cells, and fine cells where it is small are merged back. The solver then works on this mixed grid. Shocks, fronts, vortices and boundary layers often fill a small part of the domain, so AMR can reach the accuracy of a uniform fine grid with a small fraction of its cells. The method needs three parts: an error indicator, a data structure for the refined grid (patches, a [quadtree](/quadtree/) or [octree](/octree/) of cells, or a refined finite element mesh), and rules for moving data between levels without losing conservation or accuracy. Berger and Oliger (1984) introduced block-structured AMR for hyperbolic equations, and Berger and Colella (1989) made it conservative for shock hydrodynamics; that method has its own page, [Berger-Colella AMR](/berger-colella-amr/).

## In plain words

A grid with small cells everywhere is accurate but slow. Most of a flow is often smooth and needs only large cells, while a few places, such as a shock wave or the edge of a flame, need small ones. Adaptive refinement looks at the solution from time to time and finds the places where it changes quickly. It puts small cells there and large cells everywhere else. When the shock moves on, the small cells follow it and the old ones are merged back. The program must pass values between large and small cells carefully, so that no mass or energy is lost at the borders.

## When it applies

- Solutions with features that are much smaller than the domain: shocks, contact discontinuities, flame fronts, interfaces, singularities at corners, gravitational collapse.
- Features that move or appear during the run, so a fixed graded mesh would need to be fine everywhere they can go.
- An error indicator is available and cheap: gradients or jumps, a [Richardson](/richardson-extrapolation/) comparison of two grids, or an a posteriori residual estimate.
- The solver can work on a non-uniform grid, with interpolation at the borders between levels.

It is not worth it when the solution is uniformly rough (fully developed turbulence fills the domain), or when the overhead of regridding and of the borders between levels is larger than the savings.

## The template

```pseudo id=main
AMR-RUN(u, T)
L1  while t < T do
L2      if it is time to regrid then
L3          compute an error indicator η_C for every cell C on every level
L4          tag the cells with η_C > tol, and add a buffer of b cells around them
L5          cover the tagged cells with finer cells, keeping the levels properly nested
L6          fill new fine cells by conservative interpolation, and remove fine cells no longer tagged
L7      advance all levels to t + Δt, the finer levels with smaller steps
L8      average the fine values onto the coarse cells they cover, and correct the coarse fluxes at the borders
```

**Walk-through.** L3 measures where the grid is too coarse. L4 turns the measure into a set of cells, and the buffer makes sure that a moving feature does not leave the fine region before the next regrid. L5 builds the new grid: a set of rectangular patches in block-structured AMR, new children in a tree, or bisected elements in finite elements. Proper nesting means that each fine cell lies inside the next coarser level, at least one coarse cell away from its border, so that the border data always comes from the next level. L6 moves the solution to the new grid; conservative interpolation keeps the integral of each conserved quantity. L7 advances the levels. For explicit hyperbolic schemes the CFL condition lets a level with cells $r$ times smaller take $r$ steps per coarse step, so each level works at its own stable step. L8 makes the levels agree again: the coarse cells under a fine region take the average of the fine values, and the coarse cells next to a fine region replace their face flux by the sum of the fine fluxes. Without that flux correction, mass is not conserved.

## Classic examples

- [Berger-Colella AMR](/berger-colella-amr/): rectangular patches on levels refined by a ratio $r$, subcycling in time and a flux register at the borders. It is the basis of block-structured codes for gas dynamics and astrophysics.
- [Adaptive finite element method](/adaptive-finite-element-method/): the loop solve, estimate, mark, refine with an a posteriori error estimator and bisection of the marked elements, with proofs of convergence at the optimal rate for elliptic problems.
- [Quadtree](/quadtree/) and [octree](/octree/) grids: each cell splits into 4 or 8 children. Tree codes keep a 2:1 balance between neighbours and store the leaves in the order of a [space-filling curve](/z-order-curve/), which makes load balancing on parallel machines simple.
- [Adaptive quadrature](/adaptive-quadrature/): the same idea in one dimension for integrals. An interval is split when two rules disagree, which is a Richardson error estimate.

**Tagging by hand.** Take 8 cells with $u = (0, 0, 0, 0.1, 0.9, 1, 1, 1)$, the indicator $\eta_i = |u_{i+1} - u_{i-1}|/2$ in the interior cells, a tolerance $0.3$, a buffer of 1 cell and a ratio $r = 2$. The indicators of cells 1 to 6 are $0, 0.05, 0.45, 0.45, 0.05, 0$. Cells 3 and 4 are tagged, the buffer adds cells 2 and 5, and the fine level covers coarse cells 2 to 5 with fine cells 4 to 11. If the front moves by one coarse cell before the next regrid, it is still inside the fine region.

**Savings (measurement).** On the [Berger-Colella](/berger-colella-amr/) page, a square pulse advected by a first-order upwind scheme with 32 coarse cells has the error 5.55e-2. One level of refinement with ratio 2 gives 3.48e-2 with 49 cells, the same error as a uniform grid of 64 cells. Two levels give 2.00e-2 with 73 cells, the same as 128 uniform cells. Without the flux correction at the borders, the total mass drifts by 2%.

## Variations

- **Block-structured AMR.** Refined rectangles of many cells each, as in Berger-Oliger and Berger-Colella. Each patch is a plain array, so existing single-grid solvers run on it with little change.
- **Tree-based (cell-by-cell) AMR.** Each cell can split on its own, which follows features closely with fewer extra cells, at the cost of indirect addressing. Forests of octrees scale to very large parallel runs.
- **h, p and hp refinement.** In finite elements, $h$ makes elements smaller, $p$ raises the polynomial degree, and $hp$ chooses between them by the local smoothness. It converges exponentially for problems with corner singularities.
- **r refinement (moving meshes).** The number of cells is fixed, and the nodes move towards the features by a mesh equation.
- **Anisotropic refinement.** Cells are refined in one direction only, for boundary layers and shocks aligned with the grid.
- **Refinement in time only.** Local time stepping keeps the grid but lets small cells take smaller steps.

## Pitfalls

- **A non-conservative border.** If the coarse cell next to a fine region uses its own flux, mass and energy are lost or created at the border. Correct the coarse flux with the sum of the fine fluxes.
- **No buffer.** A shock that moves out of the fine region between two regrids is computed on the coarse grid, and the gain is lost. The buffer must cover the distance that features move between regrids.
- **An indicator that sees only gradients.** Tagging on $|\nabla u|$ refines every steep but harmless region and can miss errors that are smooth but large. A Richardson or residual estimate measures the error itself.
- **Bad interpolation to new fine cells.** Interpolation that is not conservative, or not limited, makes new oscillations at each regrid.
- **Reflections at the borders.** Waves can partly reflect where the cell size jumps. Use a refinement ratio of 2 or 4, and keep the borders away from the waves that matter.
- **Load imbalance.** On parallel machines the fine cells move with the features. Repartition the work after each regrid.

## Exercises

1. Explain why a cell with size $h/r$ can take time steps of $\Delta t/r$, and count the cell updates of one coarse step on a hierarchy with $N_\ell$ cells on level $\ell$.
2. For a one-dimensional conservative scheme with one fine patch, show that replacing the coarse flux at each border face by the time average of the fine fluxes makes the total mass constant.
3. Design a Richardson error indicator for a second-order scheme: compare two steps of size $\Delta t$ on a grid with one step of size $2\Delta t$ on the same grid coarsened by 2, and find the factor that turns the difference into an estimate of the error.

## References
