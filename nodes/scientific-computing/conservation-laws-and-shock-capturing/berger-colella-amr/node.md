---
tag: 64KT6D
kind: algorithm
slug: berger-colella-amr
name: Berger-Colella adaptive mesh refinement
aliases:
- Berger-Oliger AMR
- block-structured AMR
area: scientific-computing/conservation-laws-and-shock-capturing
level: advanced
summary: Covers regions that need resolution by nested finer grid patches, subcycled in time, with flux corrections at coarse-fine boundaries to keep conservation.
solves: [advection-equation, euler-equations-of-gas-dynamics]
model: real-ram
complexity:
  vars: {W: "the cell updates in one coarse step, the sum over levels l of r^l times the number of cells on level l", M: "the number of cells on all levels"}
  time: {worst: "Θ(W)"}
  space: {extra: "Θ(M)"}
properties: {deterministic: true, explicit: true, conservative: true, subcycling: true, adaptive: true}
history:
  year: 1989
  people: [M. J. Berger, J. Oliger, P. Colella]
  note: Berger and Oliger (1984) introduced the recursive hierarchy of refined patches with subcycling in time. Berger and Colella (1989) made it conservative with flux registers and refluxing, and used it for shock waves in gas dynamics.
prereqs: [adaptive-mesh-refinement, finite-volume-method, courant-friedrichs-lewy-condition]
see_also: [upwind-scheme, godunov-method, muscl-scheme, quadtree, octree, space-filling-curve, adaptive-finite-element-method, multigrid-method]
sources:
  - paper: doi:10.1016/0021-9991(89)90035-1
    title: M. J. Berger and P. Colella, Local adaptive mesh refinement for shock hydrodynamics, Journal of Computational Physics 82(1) (1989) 64-84
    locator: the grid hierarchy with proper nesting, the conservative flux correction at coarse-fine boundaries, the integration algorithm with subcycling
  - paper: "Marsha J. Berger and Joseph Oliger, Adaptive mesh refinement for hyperbolic partial differential equations, Journal of Computational Physics 53(3) (1984) 484-512"
    locator: the recursive time step on a hierarchy of nested grids, regridding from an error estimate
---

Berger-Colella adaptive mesh refinement (AMR) is a way to run an explicit [finite volume](/finite-volume-method/) scheme for a conservation law on a hierarchy of grids. Level 0 covers the domain. Each finer level $l + 1$ is a union of rectangular patches, each with cells $r$ times smaller than those of level $l$, placed only where an error indicator is large, such as near shocks and fronts. Each level takes $r$ time steps of size $\Delta t_l/r$ for each step of the level below, so every level runs at the same Courant number. At a face between a coarse cell and a fine patch, the coarse scheme and the fine scheme compute different fluxes. A flux register stores both, and after the fine steps a refluxing step corrects the coarse cell next to the patch, so the composite scheme conserves mass, momentum and energy exactly. Berger and Oliger (1984) introduced the hierarchy and the subcycling. Berger and Colella (1989) added the refluxing and the proper nesting that make it a conservative shock-capturing method. Libraries such as Chombo, AMReX and SAMRAI use this design.

## In plain words

A fine grid everywhere is expensive, and a shock or a flame front usually takes only a small part of the domain. So the method puts small fine grids on top of a coarse one, only where the solution has sharp features, and it moves them with those features. A fine grid takes several small time steps while the coarse grid takes one large step. Where a fine grid meets the coarse grid, the two grids calculate a different amount of material that crosses their common edge. The method records both amounts and, after the fine steps, corrects the coarse cell next to the edge, so that no material is created or lost.

## The problem

Solve a hyperbolic conservation law $u_t + f(u)_x = 0$ with a conservative explicit scheme $u_i \leftarrow u_i - \frac{\Delta t}{\Delta x}(F_{i+1/2} - F_{i-1/2})$ to a given accuracy, with far fewer cells than a uniform grid at the finest resolution. The composite solution must be conservative: on a periodic domain the sum of $u\,\Delta x$ over the finest cells that cover each point must stay constant. The [Lax-Wendroff theorem](/lax-wendroff-theorem/) needs conservation to get correct shock speeds.

## The algorithm

The hierarchy has levels $0, \dots, L$ with $\Delta x_l = \Delta x_0/r^l$ and $\Delta t_l = \Delta t_0/r^l$. A patch of level $l + 1$ covers whole cells of level $l$. A cell of level $l$ under a patch of level $l + 1$ is covered. Proper nesting means that every patch of level $l + 1$ is inside level $l$ with at least one level-$l$ cell between them. One coarse step is $\text{ADVANCE}(0, 0)$:

```pseudo id=main
ADVANCE(l, θ)
L1  fill the ghost cells of each level-l patch from a level-l patch, else from level l-1 at (1-θ) old + θ new
L2  for each level-l patch do save u as old; compute the fluxes F; u_i ← u_i - (Δt_l/Δx_l)(F_(i+1/2) - F_(i-1/2))
L3  if l > 0 then add Δt_l F at the two ends of each patch to the fine flux register R
L4  if l < L then keep C ← Δt_l F at the faces where level-(l+1) patches start or end
L5      for k ← 0 to r-1 do ADVANCE(l+1, k/r)
L6      at each such face correct the uncovered level-l cell next to it by ∓(R - C)/Δx_l
L7      replace each covered level-l cell by the mean of its r fine cells
REGRID (every K coarse steps)
L8  for l ← 0 to L-1 do tag level-l cells with large |Δu|, add a buffer, keep only properly nested cells
L9      make level-(l+1) patches from runs of tagged cells; fill them from old level-(l+1) data, else from level l
```

The sign in L6 is minus for the cell to the left of a patch and plus for the cell to the right. L7 is called average down. After L7 the covered cells hold the fine averages, so level 0 alone gives the composite total.

## Example

**One face by hand.** Take $u_t + u_x = 0$ on $[0, 1)$, periodic, with 8 coarse cells, $r = 2$, $\Delta t_0 = \tfrac1{16}$ (Courant number $\tfrac12$ on both levels), and $u = 1$ for $x < \tfrac9{16}$, else $0$, sampled at cell centres. Tagging the cells next to jumps (with no buffer) gives the patches over coarse cells 3 and 4 and over coarse cells 7 and 0. The fine values over coarse cells 3 and 4 are $1, 1, 1, 0$. Coarse cell 4 holds their mean $\tfrac12$ and coarse cell 5 holds $0$. At face 5, the right end of the first patch:

- coarse flux: $C = \Delta t_0\,u_4 = \tfrac1{16}\cdot\tfrac12 = \tfrac1{32}$, and the coarse step gives $u_5 = 0 - \tfrac12(0 - \tfrac12) = \tfrac14$;
- first fine step: the last fine cell holds $0$, so the flux is $0$, and the cell becomes $0 - \tfrac12(0 - 1) = \tfrac12$;
- second fine step: the flux is $\tfrac12$, so $R = \tfrac1{32}(0 + \tfrac12) = \tfrac1{64}$;
- refluxing: $u_5 \leftarrow \tfrac14 + (R - C)/\Delta x_0 = \tfrac14 + (\tfrac1{64} - \tfrac1{32})\cdot 8 = \tfrac18$.

The amount $\tfrac18\cdot\tfrac18 = \tfrac1{64}$ in cell 5 is now exactly what left the fine patch. Without refluxing cell 5 holds $\tfrac14$, which is $\tfrac1{64}$ of extra mass, and the total $\tfrac9{16}$ is not kept. The tests check these numbers in exact rational arithmetic.

**Accuracy and cost (measurement).** $u_0 = e^{-200(x - 0.3)^2}$, 32 cells on level 0, $r = 2$, Courant number $\tfrac12$, $T = 0.25$, tags where a neighbour differs by more than 0.02, buffer 2, regrid every step. $L^1$ error against the exact solution at the cell centres:

| method | finest $\Delta x$ | cells at $T$ | $L^1$ error |
|---|---|---|---|
| uniform, 32 cells | 1/32 | 32 | 5.551e-2 |
| AMR, levels 0 and 1 | 1/64 | 49 | 3.482e-2 |
| uniform, 64 cells | 1/64 | 64 | 3.482e-2 |
| AMR, levels 0 to 2 | 1/128 | 73 | 1.995e-2 |
| uniform, 128 cells | 1/128 | 128 | 1.995e-2 |

AMR gets the error of the uniform fine grid with 57% of its cells, because the pulse stays inside the refined region and the coarse cells see only $u \approx 0$. With a box profile, 16 coarse cells and two finer levels, the total mass is $\tfrac{13}{64}$ exactly after 14 coarse steps with refluxing. Without refluxing it is off by $4.3\times10^{-3}$, that is 2%.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It shows two facts. First, proper nesting makes every ghost value in L1 and every cell in L6 exist. Second, with refluxing, one call $\text{ADVANCE}(l, \theta)$ changes the mass of each level-$l$ patch only by the level-$l$ fluxes at its two ends, so the composite mass is conserved exactly. Regridding also conserves mass, because it fills new fine cells either from old fine cells or with the value of the parent cell. When level 1 covers the whole domain, the method is the uniform fine scheme with $r$ steps per coarse step. When $L = 0$, it is the single-grid scheme.

## Complexity

One coarse step does $r^l$ steps on level $l$, so the work is $\Theta(\sum_l r^l N_l)$ flux evaluations, where $N_l$ is the number of cells on level $l$. A uniform grid at the finest level does $r^L$ steps on $r^L N_0$ cells, so the gain is large when the fine levels cover a small fraction of the domain. Regridding costs $\Theta(\sum_l N_l)$ in one dimension, plus the cost of clustering the tagged cells into rectangles in two and three dimensions. The flux registers take memory proportional to the number of coarse-fine faces. The reference code finds the patch of a cell by a linear search over the patches of its level, which is simple but slow when there are many patches. Production codes keep an index map or a box tree.

## Properties

- Conservative to rounding error (exactly in rational arithmetic), with refluxing.
- Every level runs at the same Courant number, so the time step is not limited by the finest cells.
- First order in time at coarse-fine boundaries with linear interpolation in time for the ghost cells. Second-order schemes need second-order interpolation in space and time to keep their order there.
- Explicit and local: each patch is a uniform grid, so a fast uniform-grid kernel runs on it.
- The hierarchy changes during the run, so the number of cells changes with the solution.

## Variants and improvements

- **Berger-Oliger.** The 1984 method allows rotated patches and does not correct the fluxes, so it is not conservative.
- **Clustering.** In two and three dimensions the tagged cells are grouped into rectangles with an efficiency threshold, usually by the method of Berger and Rigoutsos (1991), which splits boxes at holes and inflection points of tag signatures.
- **Without subcycling.** All levels take the finest time step. Refluxing becomes simpler, and the code becomes slower by a factor near $r^L$ on the coarse levels.
- **Runge-Kutta time stepping.** The flux register sums the stage fluxes with the weights of the Runge-Kutta method, so the corrected coarse flux matches the fine one.
- **Tree-based AMR.** A [quadtree](/quadtree/) or an [octree](/octree/) refines single cells instead of patches, and a [space-filling curve](/space-filling-curve/) distributes the leaves over processors. The refluxing idea is the same.
- **Elliptic AMR.** A composite Poisson solve couples the levels with [multigrid](/multigrid-method/) and the same flux matching at coarse-fine faces.

## When to use it

Use it for explicit shock-capturing on structured grids when the features that need resolution (shocks, contact discontinuities, flame fronts, collapsing clouds) cover a small part of the domain and move. It is the standard method in astrophysics, combustion and compressible flow codes. For problems where most of the domain needs the fine grid, a uniform grid is simpler and faster. For complex geometry, unstructured mesh adaptation or [adaptive finite elements](/adaptive-finite-element-method/) fit better.

## Pitfalls

- **Forgetting the reflux.** The scheme still looks correct but loses or creates mass at every coarse-fine face, and shock speeds become wrong.
- **Breaking proper nesting.** If a level-$(l+2)$ patch touches the edge of level $l + 1$, its ghost cells come from the wrong level and the reflux corrects a covered cell.
- **Ghost values without time interpolation.** Using the new coarse value for all subcycles is first order and can make reflections at the patch edge.
- **Regridding that interpolates non-conservatively.** New fine cells must have the parent value as their mean. Linear interpolation needs a limited, conservative slope.
- **Tags too close to the patch edge.** Without a buffer the feature leaves the fine patch between regrids. The buffer must be at least the distance the feature moves between regrids.
- **Small patches.** Many small patches mean many ghost cells and much overhead. Clustering trades a few extra cells for fewer, larger boxes.

## Implementations

## History

Marsha Berger and Joseph Oliger (1984) gave AMR for hyperbolic equations: a recursive hierarchy of patches, which can be rotated, with subcycling and regridding from an error estimate. Berger and Colella (1989) restricted the patches to be aligned with the coarse grid, introduced proper nesting and the conservative flux correction, and computed shock reflection problems for the Euler equations. The patch-based design became the basis of most block-structured AMR codes in astrophysics, combustion and plasma physics.

## References
