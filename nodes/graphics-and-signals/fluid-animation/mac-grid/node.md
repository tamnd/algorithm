---
tag: NKCN2S
kind: data-structure
slug: mac-grid
name: MAC grid
aliases:
- marker-and-cell grid
- staggered grid
area: graphics-and-signals/fluid-animation
level: core
summary: A fluid grid with pressure at cell centers and each velocity component on the faces normal to it. Divergence and gradient become compact central differences with no checkerboard null space.
model: real-ram
complexity:
  vars: {g: the number of grid cells, k: the number of conjugate gradient iterations}
  time: {sample: O(1), divergence: Θ(g), gradient_update: Θ(g), poisson_build: Θ(g), pressure_solve: O(g k)}
  space: {total: Θ(g)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 1965
  people: [Francis H. Harlow, J. Eddie Welch]
  note: Harlow and Welch put pressure at cell centers and velocity components on cell faces in their marker-and-cell method at Los Alamos. Foster and Metaxas (1996) brought the layout to computer animation.
prereqs: [poisson-equation, finite-difference-method, bilinear-interpolation]
see_also: [marker-and-cell-method, stable-fluids, chorin-projection-method, helmholtz-hodge-decomposition, finite-volume-method, conjugate-gradient-method, multigrid-method, particle-in-cell]
sources:
  - paper: doi:10.1063/1.1761178
    title: "Francis H. Harlow and J. Eddie Welch, Numerical calculation of time-dependent viscous incompressible flow of fluid with free surface, Physics of Fluids 8(12), 1965, 2182-2189"
    locator: the finite difference mesh with the pressure at cell centers and the velocity components on the cell faces
  - book: isbn:9781482232837
    title: "Robert Bridson, Fluid Simulation for Computer Graphics, second edition, CRC Press, 2015"
    locator: "the chapter Overview of Numerical Simulation (section Grids) and the chapter Making Fluids Incompressible (the discrete pressure gradient, the discrete divergence, the pressure equations and the compatibility condition)"
  - paper: doi:10.1006/gmip.1996.0039
    title: "Nick Foster and Dimitri Metaxas, Realistic animation of liquids, Graphical Models and Image Processing 58(5), 1996, 471-483"
    locator: Section 3.1, the staggered velocities at face centers and the pressure at cell centers
  - paper: doi:10.1145/383259.383260
    title: "Ronald Fedkiw, Jos Stam and Henrik Wann Jensen, Visual simulation of smoke, SIGGRAPH 2001, 15-22"
    locator: Section 4, the staggered grid and the sampling of the velocity at cell faces
---

A MAC grid is the standard layout of a grid fluid solver in computer animation. Pressure and other scalars live at the centers of the cells. The x component of the velocity lives at the centers of the cell faces whose normal is x, and the y component at the centers of the faces whose normal is y. With this layout, the divergence of a cell and the pressure gradient across a face both use the two nearest values only. The discrete Laplacian that they make has no checkerboard null space, which is the main reason for the layout. This page fixes the layout for all grid fluid pages of the encyclopedia. The shared helper `macgrid.py` implements it, and the [marker-and-cell method](/marker-and-cell-method/) of 1965 is the full solver from which the name comes.

## In plain words

Think of a tiled floor with water on it. Water crosses from tile to tile at the edges, so a MAC grid measures the flow on each edge. It keeps the pressure in the middle of each tile.

To find the net flow out of a tile, add its four edge values with signs. To find how pressure pushes water across an edge, take the difference of the two tiles on its sides.

If you kept all values in the tile centers, you would have to average neighbors to get edge values. Then a pressure that goes up and down from tile to tile, like a chessboard, gives no push at all, and the solver cannot see it. On a MAC grid that pattern pushes hard, so it cannot hide.

## The abstract type

A MAC grid stores a discrete velocity field and the scalar fields of a fluid on a uniform grid, and gives these operations:

- SAMPLE$(q, x, y)$: the value of a stored field at any point, by [bilinear interpolation](/bilinear-interpolation/). The velocity at a point needs one sample of $u$ and one of $v$.
- DIVERGENCE: the net outflow of each cell divided by its area.
- GRADIENT-UPDATE$(p)$: subtract $\frac{\Delta t}{\rho}$ times the discrete pressure gradient from the velocity on each face.
- POISSON-SYSTEM: the sparse symmetric matrix $A$ and the right side $b$ of the pressure equation over the FLUID cells, so that the velocity after GRADIENT-UPDATE has zero divergence.

PROJECT is POISSON-SYSTEM, a linear solve and GRADIENT-UPDATE. ADVECT moves a field along the velocity; it is the subject of [stable fluids](/stable-fluids/) and its relatives. The helper has both.

## Representation

The grid has $n_x$ by $n_y$ square cells of side $\Delta x$. The index $i$ counts in $x$ and $j$ counts in $y$, so $i$ is not an image row.

- $p[i][j]$ is at $((i + \tfrac12)\Delta x, (j + \tfrac12)\Delta x)$ for $0 \le i < n_x$, $0 \le j < n_y$. Smoke density, temperature and other scalars use the same points.
- $u[i][j]$ is at $(i\,\Delta x, (j + \tfrac12)\Delta x)$ for $0 \le i \le n_x$: the left face of cell $(i, j)$. There are $(n_x + 1)\,n_y$ values.
- $v[i][j]$ is at $((i + \tfrac12)\Delta x, j\,\Delta x)$ for $0 \le j \le n_y$: the bottom face of cell $(i, j)$. There are $n_x\,(n_y + 1)$ values.
- $label[i][j] \in \{\text{FLUID}, \text{SOLID}, \text{AIR}\}$. A cell outside the grid counts as SOLID, so the border of the domain is a wall.

In 3D, add $w[i][j][k]$ at $((i + \tfrac12)\Delta x, (j + \tfrac12)\Delta x, k\,\Delta x)$. All the code here is 2D.

A uniform field with offsets $(o_x, o_y)$ has $q[a][b]$ at $((a + o_x)\Delta x, (b + o_y)\Delta x)$. The offsets are $(\tfrac12, \tfrac12)$ for $p$, $(0, \tfrac12)$ for $u$ and $(\tfrac12, 0)$ for $v$. One sampling routine with the offsets as arguments serves all three, which removes a common source of half-cell bugs.

The boundary rules are part of the representation:

- **(S) Solid faces.** On a face with a SOLID cell on at least one side, the velocity is the normal velocity of the solid there, which is zero for a fixed wall. The pressure update does not change it.
- **(A) Air cells.** In an AIR cell, $p = 0$. This is the free surface condition with the pressure measured from the air pressure.

The layout is one of several staggered layouts. In atmospheric modeling it is called the Arakawa C grid, while the B and E grids place the two components together at other points. "Marker-and-cell grid" names the layout after the method that introduced it; the method also moves marker particles, which the grid does not need.

## Operations

```pseudo id=main
SAMPLE(q, x, y, ox, oy)                     ▷ q[a][b] at ((a + ox) dx, (b + oy) dx), size na by nb
L1  fx <- clamp(x/dx - ox, 0, na - 1); fy <- clamp(y/dx - oy, 0, nb - 1)
L2  a <- min(floor(fx), na - 2); b <- min(floor(fy), nb - 2); s <- fx - a; t <- fy - b
L3  return (1-s)(1-t) q[a][b] + (1-s) t q[a][b+1] + s (1-t) q[a+1][b] + s t q[a+1][b+1]

DIVERGENCE(u, v)
L4  for each cell (i, j): d[i][j] <- (u[i+1][j] - u[i][j] + v[i][j+1] - v[i][j]) / dx

GRADIENT-UPDATE(u, v, p, label, dt, rho)    ▷ p = 0 in AIR cells
L5  for each inner u face (i, j), 1 <= i <= nx - 1, with no SOLID side and a FLUID side do
L6      u[i][j] <- u[i][j] - dt / (rho dx) (p[i][j] - p[i-1][j])
L7  the same for each inner v face (i, j), 1 <= j <= ny - 1, with p[i][j] - p[i][j-1]

POISSON-ROW(i, j)                           ▷ cell (i, j) is FLUID; its row is k
L8  for each neighbor c of (i, j) that is not SOLID: A[k][k] <- A[k][k] + 1
L9      if c is FLUID then A[k][c] <- A[k][c] - 1
L10 b[k] <- -(rho dx / dt) (u[i+1][j] - u[i][j] + v[i][j+1] - v[i][j])
```

Lines L1 and L2 clamp the point to the box of the sample points, so a query outside the grid returns the value at the nearest border sample. The weights at line L3 are nonnegative and sum to 1.

Line L4 is the [finite volume](/finite-volume-method/) form of the divergence: the flux through each face of the cell, with the outward sign, over the cell area. In the interior it is also the central difference of $u$ and $v$ over one cell, which is second order accurate at the cell center.

Lines L5 to L7 update only faces between two cells that are not SOLID, with at least one FLUID side. Faces between two AIR cells keep their values, and faces on a solid keep the solid velocity, rule (S). The difference at line L6 is a central difference at the face center over one cell, again second order.

Lines L8 to L10 build the equations $A\,p = b$ that make the updated divergence zero. A SOLID neighbor adds nothing, because rule (S) fixes its face. An AIR neighbor adds 1 to the diagonal only, because its pressure is 0. A FLUID neighbor adds 1 to the diagonal and $-1$ off the diagonal. With $\Delta x = 1$ this is the 5-point Laplacian with a minus sign, with Neumann rows at walls and Dirichlet rows at air. Solve it by [conjugate gradients](/conjugate-gradient-method/) (the helper), by [multigrid](/multigrid-method/), or by a dense method for small tests.

## Example

**Divergence.** Take $n_x = 2$, $n_y = 1$, $\Delta x = 0.5$ m, $u = (0, 1, 3)$ m/s on the three vertical faces and $v[0] = (0, 2)$, $v[1] = (1, 1)$ m/s on the bottom and top faces of the two cells. Line L4 gives

| cell | $u$ right minus left | $v$ top minus bottom | divergence (1/s) |
|---|---|---|---|
| (0, 0) | 1 - 0 = 1 | 2 - 0 = 2 | 3 / 0.5 = 6 |
| (1, 0) | 3 - 1 = 2 | 1 - 1 = 0 | 2 / 0.5 = 4 |

**One projection by hand.** A 2 by 2 box with walls, $\Delta x = \Delta t = \rho = 1$, and one nonzero face: $u[1][0] = 1$, the face between cells (0, 0) and (1, 0). The divergence is $1$ in cell (0, 0) and $-1$ in cell (1, 0). Each cell has two walls and two FLUID neighbors, so each row of $A$ has 2 on the diagonal and $-1$ twice. In the cell order (0, 0), (0, 1), (1, 0), (1, 1),

$$A = \begin{pmatrix} 2 & -1 & -1 & 0 \\ -1 & 2 & 0 & -1 \\ -1 & 0 & 2 & -1 \\ 0 & -1 & -1 & 2 \end{pmatrix}, \qquad b = (-1, 0, 1, 0).$$

$A$ is singular, because the box is closed: adding a constant to $p$ changes nothing. The entries of $b$ sum to zero, so the system is consistent. The solution with mean zero is $p = (-\tfrac38, -\tfrac18, \tfrac38, \tfrac18)$. Lines L5 to L7 then give

| face | before | pressure difference | after |
|---|---|---|---|
| $u[1][0]$ | 1 | 3/8 - (-3/8) = 3/4 | 1/4 |
| $u[1][1]$ | 0 | 1/8 - (-1/8) = 1/4 | -1/4 |
| $v[0][1]$ | 0 | -1/8 - (-3/8) = 1/4 | -1/4 |
| $v[1][1]$ | 0 | 1/8 - 3/8 = -1/4 | 1/4 |

Every cell now has zero divergence. The single jet became a loop that turns counterclockwise with speed $\tfrac14$ on each inner face. The kinetic energy $\tfrac12 \sum$ (velocity squared) dropped from $\tfrac12$ to $\tfrac18$.

**A larger box.** The helper on a 16 by 16 box with $\Delta x = 1/16$ m, $\Delta t = 0.01$ s, $\rho = 1000$ kg/m^3 (per unit depth), and random face velocities in $[-1, 1]$ m/s from `random.Random(4)`: the largest cell divergence goes from 55.40 1/s to $4.2 \times 10^{-11}$ 1/s after 74 conjugate gradient iterations with the tolerance $10^{-12}$, and the kinetic energy goes from 350.00 J to 161.63 J. On a 32 by 32 grid ($\Delta x = 1/32$ m, seed 5) the solve takes 153 iterations, about twice as many for twice the side, as the condition number predicts. The iteration counts are measurements.

**The checkerboard.** On a periodic 4 by 4 grid, the MAC Laplacian has a null space of dimension 1: the constants. The Laplacian made from the central difference gradient and divergence on a collocated grid has a null space of dimension 4, and the checkerboard $(-1)^{i+j}$ is in it. The MAC Laplacian maps the checkerboard to $-8$ times itself, the eigenvalue of largest size, so the pressure solve sees this mode and removes the divergence it causes. The test file checks both counts by exact elimination for $n = 4$ and $n = 6$.

## Correctness

The correctness claims are identities of the discrete operators. They hold exactly in rational arithmetic, and the tests check them with `fractions.Fraction`.

1. SAMPLE reproduces every affine function exactly, and its value lies between the smallest and the largest of the four values it uses. The weights are products of numbers in $[0, 1]$ that sum to 1.
2. Let $D$ be DIVERGENCE and $G$ the gradient of lines L5 to L7 without the factor $\Delta t / \rho$. Then $-\Delta x^2\,D\,G = A$ on the FLUID cells, so after GRADIENT-UPDATE with the solution of $A\,p = b$ the divergence of every FLUID cell is zero.
3. $A$ is symmetric and positive semidefinite. Its null space is spanned by the indicator vectors of the connected FLUID regions that touch no AIR cell. For each such region, the system is consistent if and only if the sum of $b$ over the region is zero, which is the discrete compatibility condition: the net flux through the solid boundary of a closed region must be zero.
4. With fixed walls, the projection is the orthogonal projection onto the divergence-free fields in the inner product $\sum u^2 + \sum v^2$. It never increases the kinetic energy.
5. On a periodic $n$ by $n$ grid, the null space of the MAC Laplacian is the constants. For even $n$, the collocated central difference Laplacian has a null space of dimension 4.

The proofs, by summation by parts and by discrete Fourier modes, are in [proofs/correctness.md](proofs/correctness.md).

## Complexity

Let $g = n_x n_y$ be the number of cells. The grid stores $g$ pressures, $(n_x + 1) n_y + n_x (n_y + 1) = 2g + n_x + n_y$ face velocities and $g$ labels, so the space is $\Theta(g)$, plus $\Theta(g)$ per extra scalar field.

SAMPLE costs $O(1)$. DIVERGENCE, GRADIENT-UPDATE and the assembly of $A$ and $b$ cost $\Theta(g)$, because each cell and face does a constant amount of work. $A$ has at most 5 nonzeros per row.

The solve dominates. One conjugate gradient iteration costs $\Theta(g)$. On an $N$ by $N$ grid the condition number of $A$ grows as $N^2$, so plain conjugate gradients need $O(N)$ iterations for a fixed reduction of the error, which is $O(g^{3/2})$ in total in 2D. Multigrid reaches a fixed reduction in $O(g)$. The measured counts above (74 and 153) fit the $O(N)$ estimate.

## Variants

- **3D.** The same layout with a third component $w$ on the faces normal to $z$. Every statement above holds with 7-point stencils.
- **Collocated grids.** All components at cell centers. Simpler to advect, but the central difference projection has the checkerboard null space. Stam's [stable fluids](/stable-fluids/) used a cell-centered grid, and computational fluid dynamics codes with collocated grids add a correction to the face fluxes (the Rhie-Chow interpolation) to remove the checkerboard.
- **Cut cells and fractional weights.** Faces partly covered by a solid get a weight between 0 and 1 in the pressure equation. See [variational solid-fluid coupling](/variational-solid-fluid-coupling/).
- **Free surface at sub-cell accuracy.** The [ghost fluid method](/ghost-fluid-method/) puts $p = 0$ at the interpolated surface position instead of the AIR cell center.
- **Sparse and adaptive grids.** Store only tiles near the fluid, or refine with an octree. The face placement stays the same inside each tile or cell.
- **Particles on a MAC grid.** [Particle-in-cell](/particle-in-cell/), [FLIP](/fluid-implicit-particle/) and [APIC](/affine-particle-in-cell/) carry velocity on particles and use the MAC grid only for the projection.

## When to use it

Use a MAC grid for any incompressible grid fluid with a pressure projection: smoke, fire, liquids with a level set or particles, and the grid part of hybrid particle methods. It gives the most compact and robust pressure equation, and the boundary conditions are simple to state on faces.

A collocated grid is easier when the main work is advection of many vector quantities, or when the code also runs other solvers that expect values at the same points. For compressible flow with shocks, the [finite volume method](/finite-volume-method/) with collocated cell averages and Riemann solvers is the usual choice.

## Pitfalls

- **Off by half a cell.** $u$ has $n_x + 1$ columns and $v$ has $n_y + 1$ rows. Sampling $u$ with the offsets of $p$ shifts the whole velocity field by half a cell. Use one sampling routine with explicit offsets.
- **Velocity at a cell center.** It is the average of the two $u$ faces and the two $v$ faces. Do not take $u[i][j]$ as the velocity of cell $(i, j)$.
- **Boundaries before the divergence.** Set the solid face velocities, rule (S), before computing $b$. Otherwise the right side contains flow through walls, and the closed system can become inconsistent.
- **The singular closed box.** With walls on all sides, $A$ is singular. Remove the mean of $b$ over each closed region and fix the free constant of $p$, for example by removing its mean. The helper does both. A floating point $b$ with a small nonzero sum makes plain conjugate gradients stall.
- **AIR is not SOLID.** An AIR neighbor adds 1 to the diagonal; a SOLID neighbor adds nothing. Mixing them up gives a free surface that acts like a wall, or a wall that leaks.
- **Faces between AIR cells.** The projection does not touch them, but advection reads them. Extrapolate the fluid velocity into a few layers of AIR faces before advection.
- **Units of $b$.** The right side at line L10 has the factor $\rho\,\Delta x / \Delta t$. Code that solves for $p\,\Delta t / \rho$ instead must use the same scale in GRADIENT-UPDATE.

## Implementations

## History

Harlow and Welch (1965) introduced the layout at Los Alamos as the grid of their marker-and-cell method for incompressible flow with a free surface: pressure at cell centers, velocity components on the faces, and marker particles to track the liquid. In meteorology the same layout became known as the C grid in Arakawa's classification of staggered grids. Foster and Metaxas (1996) used it for the first liquid animations in computer graphics, with marker particles and an explicit solver. Stam (1999) used a cell-centered grid in stable fluids, and Fedkiw, Stam and Jensen (2001) went back to the staggered layout of Foster and Metaxas for smoke. Since then the MAC grid is the default of grid fluid solvers in animation, and Bridson's book builds every grid method on it.

## References
