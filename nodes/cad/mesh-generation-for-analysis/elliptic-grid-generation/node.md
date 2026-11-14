---
tag: EEEWVA
kind: algorithm
slug: elliptic-grid-generation
name: Elliptic grid generation
aliases:
- Winslow grid generation
- Thompson-Thames-Mastin method
area: cad/mesh-generation-for-analysis
level: advanced
summary: Computes a structured grid by solving Laplace or Poisson equations for the computational coordinates; the continuous map never folds, and control functions set the spacing.
solves: [structured-grid-generation]
model: real-ram
complexity:
  vars: {n: the number of grid points (M + 1)(N + 1)}
  time: {per_sweep: O(n), gauss_seidel_model: O(n^2), sor_model: O(n^(3/2))}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1966
  people: [Alan M. Winslow, Joe F. Thompson, Frank C. Thames, C. Wayne Mastin]
  note: Winslow made meshes whose lines are level curves of harmonic functions in 1966. Thompson, Thames and Mastin added control functions and general bodies in 1974.
prereqs: [transfinite-interpolation-grid, poisson-equation, successive-over-relaxation]
see_also: [structured-grid-generation, gauss-seidel-method, laplacian-smoothing, scaled-jacobian, tutte-embedding, multigrid-method, finite-difference-method, mesh-untangling]
sources:
  - paper: doi:10.1016/0021-9991(66)90001-5
    title: Alan M. Winslow, Numerical solution of the quasilinear Poisson equation in a nonuniform triangle mesh, Journal of Computational Physics 1(2), 1966, 149 to 172
    locator: the mesh whose lines are equipotentials, obtained by solving the inverted Laplace equations for the coordinates (general locator)
  - paper: doi:10.1016/0021-9991(74)90114-4
    title: Joe F. Thompson, Frank C. Thames and C. Wayne Mastin, Automatic numerical generation of body-fitted curvilinear coordinate system for field containing any number of arbitrary two-dimensional bodies, Journal of Computational Physics 15(3), 1974, 299 to 319
    locator: the Poisson system with control functions for the computational coordinates, its transformed form, and its solution by point successive over-relaxation (general locator)
  - book: isbn:9780444009852
    title: Joe F. Thompson, Z. U. A. Warsi and C. Wayne Mastin, Numerical Grid Generation, Foundations and Applications, North-Holland, 1985
    locator: the chapters on elliptic generation systems (general locator)
  - book: isbn:9780521641210
    title: Peter Duren, Harmonic Mappings in the Plane, Cambridge Tracts in Mathematics 156, Cambridge University Press, 2004
    locator: the chapter Harmonic Mappings onto Convex Regions, the Radó-Kneser-Choquet theorem on p. 29 and Choquet's proof on p. 31
---

Elliptic grid generation makes a structured grid inside a block by asking that the computational coordinates $\xi$ and $\eta$ be harmonic functions of the physical coordinates, or solutions of a Poisson equation with chosen right-hand sides. The equations are inverted, so that the unknowns are the physical positions $x(\xi, \eta)$ of the grid points, and solved by finite differences and an iteration such as [successive over-relaxation](/successive-over-relaxation/), starting from a [transfinite interpolation](/transfinite-interpolation-grid/) grid. The grids are smooth. For the Laplace case, the continuous map is one to one on any domain bounded by a Jordan curve, by the Radó-Kneser-Choquet theorem. The discrete grid does not inherit this guarantee, so it must still be checked.

## In plain words

Think of the grid lines of one family as lines of equal temperature in a metal plate. Hold one side of the plate at one temperature and the opposite side at another, and the heat spreads evenly between them. Lines of equal temperature never cross, and they bend smoothly around dents in the plate. Do the same with the other two sides, and the two families of lines form the grid.

To compute this, the program moves each inner grid point toward a weighted average of its neighbours. It does this again and again until the points stop moving. Extra terms can pull the lines closer to a wall, where a flow solver needs small cells.

The smooth lines of the exact solution never cross. The computed grid is only close to them, so a program still checks every cell.

## The problem

This is [structured grid generation](/structured-grid-generation/) for one block. The input is four sides given as point lists, as for transfinite interpolation: the bottom $B_0, \ldots, B_M$, the top $T_0, \ldots, T_M$, the left $L_0, \ldots, L_N$ and the right $R_0, \ldots, R_N$, with common corners. Optional inputs are control functions $P_{ij}, Q_{ij}$, a relaxation factor $0 < \omega < 2$, a tolerance and a maximum number of sweeps. The output is a grid $x_{ij}$ with the given boundary points that satisfies the discrete equations below to the tolerance, and a flag that says whether it converged. A grid is valid if every cell is a strictly convex counterclockwise quadrilateral.

The continuous equations, with $\xi$ and $\eta$ the indices $i$ and $j$ seen as continuous variables, are

$$\alpha\, x_{\xi\xi} - 2 \beta\, x_{\xi\eta} + \gamma\, x_{\eta\eta} + J^2 (P\, x_\xi + Q\, x_\eta) = 0,$$
$$\alpha = |x_\eta|^2, \quad \beta = x_\xi \cdot x_\eta, \quad \gamma = |x_\xi|^2, \quad J = \det(x_\xi, x_\eta),$$

for both coordinates of $x = (x, y)$. They are equivalent, where $J \ne 0$, to $\xi_{xx} + \xi_{yy} = P$ and $\eta_{xx} + \eta_{yy} = Q$. With $P = Q = 0$ this is Winslow's method. Thompson, Thames and Mastin introduced the control functions $P$ and $Q$.

## The algorithm

ORIENT2D is the [orientation test](/orientation-test/). CHECK converts each stored float to a Fraction without rounding, so its signs are exact for the points as stored.

```pseudo id=main
ELLIPTIC-GRID(B, T, L, R, P, Q, ω, tol, K)
L1  x ← TFI(B, T, L, R)                                 ▷ the sides stay fixed from here on
L2  for k ← 1 to K do
L3      for i ← 1 to M − 1 do
L4          for j ← 1 to N − 1 do
L5              x_ξ ← (x_{i+1,j} − x_{i−1,j})/2;  x_η ← (x_{i,j+1} − x_{i,j−1})/2
L6              α ← |x_η|²;  β ← x_ξ · x_η;  γ ← |x_ξ|²;  J ← det(x_ξ, x_η)
L7              X ← (x_{i+1,j+1} − x_{i+1,j−1} − x_{i−1,j+1} + x_{i−1,j−1})/4
L8              G ← [α(x_{i+1,j} + x_{i−1,j}) + γ(x_{i,j+1} + x_{i,j−1}) − 2βX + J²(P_ij x_ξ + Q_ij x_η)] / (2(α + γ))
L9              x_ij ← x_ij + ω (G − x_ij)
L10     r ← max over inner points of |G_ij(x) − x_ij|      ▷ L5 to L8 on the new grid
L11     if r < tol then return (x, converged)
L12 return (x, not converged)

CHECK(x)
L13 for each cell with corners q_0 = x_ij, q_1 = x_{i+1,j}, q_2 = x_{i+1,j+1}, q_3 = x_{i,j+1} do
L14     if ORIENT2D(q_{k−1}, q_k, q_{k+1}) ≤ 0 for some k = 0..3 then return false
L15 return true
```

L5 to L7 are central differences with unit index spacing. L8 solves the discrete equation at $(i, j)$ for $x_{ij}$, with the neighbours and the coefficients fixed. With $\omega = 1$ this is a nonlinear [Gauss-Seidel method](/gauss-seidel-method/), and with $1 < \omega < 2$ it is point SOR. The coefficients are recomputed at each point from the newest values, so the iteration is a Picard iteration on a nonlinear system. L10 measures the residual of every equation, divided by $2(\alpha + \gamma)$, on the grid after the sweep.

## Example

**One inner point.** Take the trapezoid with corners $(0, 0)$, $(4, 0)$, $(2, 2)$, $(0, 2)$ and $M = N = 2$, with the side midpoints $(2, 0)$, $(1, 2)$, $(0, 1)$ and $(3, 1)$. TFI puts the inner point at $(3/2, 1)$. With one inner point, L5 to L8 use only boundary points, so one sweep with $\omega = 1$ gives the solution.

| step | value |
|---|---|
| L5 | $x_\xi = ((3, 1) - (0, 1))/2 = (3/2, 0)$, $x_\eta = ((1, 2) - (2, 0))/2 = (-1/2, 1)$ |
| L6 | $\alpha = 5/4$, $\beta = -3/4$, $\gamma = 9/4$, $J = 3/2$ |
| L7 | $X = ((2, 2) - (4, 0) - (0, 2) + (0, 0))/4 = (-1/2, 0)$ |
| L8 | $G = \big[\tfrac54 (3, 2) + \tfrac94 (3, 2) - 2 (-\tfrac34)(-\tfrac12, 0)\big] / 7 = (39/28, 1)$ |
| L10 | $r = 0$ after the sweep, so L11 returns |

The point moves from $x = 1.5$ to $x = 39/28 \approx 1.393$, a shift of $3/28$ to the left. The term $-2\beta X$ is the whole difference: without it, the point would stay at $(3/2, 1)$.

**A conformal map as an oracle.** Take the sector of an annulus with the grid points $x_{ij} = e^{\kappa i} (\cos \kappa j, \sin \kappa j)$ on the sides, with $\kappa = \pi / (2N)$ and $M = N$. The map $(\xi, \eta) \mapsto e^{\kappa \xi} (\cos \kappa \eta, \sin \kappa \eta)$ is conformal, so $\xi$ and $\eta$ are harmonic and this map is the exact continuous solution. The largest distance of the converged grid from it is $0.0345$, $0.0088$, $0.0023$ and $0.00057$ for $N = 4, 8, 16, 32$, so the error falls by a factor of about 4 when the grid is refined, as expected for central differences. The TFI start is wrong by about $0.21$ at every resolution.

**A grid that converges and is still not valid.** Take the unit square with the bottom side replaced by the hook $(0, 0) \to (3/5, 1/5) \to (2/5, 2/5) \to (1, 0)$, the domain of the folding example of the [transfinite interpolation page](/transfinite-interpolation-grid/), with $M = 6$ and $N = 4$. The boundary angle at $(2/5, 2/5)$ is about $349°$. The TFI start has two cells turned over. ELLIPTIC-GRID with $\omega = 1.5$ converges to a residual below $10^{-12}$ in 43 sweeps. No cell is turned over anymore, but two cells next to the hook have one or two negative corner values, so CHECK returns false. Grids of $12 \times 8$ and $24 \times 16$ cells on the same domain also fail CHECK near the hook.

**Convex quadrilaterals.** On 25 random convex quadrilaterals with random point spacing on the sides and 6 to 12 cells per direction, 5 of the TFI starts fail CHECK, and every converged elliptic grid passes it. This is what the tests observe, not a theorem.

## Correctness

The procedure keeps the boundary points, because it writes only inner points, and it stops after at most $K$ sweeps. When it reports convergence, every discrete equation holds with a residual below $2(\alpha + \gamma)$ times the tolerance. If the sides are evenly spaced samples of an affine map, the TFI start already solves the equations, so the method reproduces parallelograms.

The reason elliptic grids do not fold is a theorem about the continuous map.

**Theorem (Radó-Kneser-Choquet).** Let $\Omega$ be a bounded convex domain whose boundary is a Jordan curve $\Gamma$, and let $\varphi$ be a homeomorphism of the unit circle onto $\Gamma$. Then the harmonic extension of $\varphi$ to the unit disk is a one-to-one map of the disk onto $\Omega$ with nonvanishing Jacobian.

Duren proves it in the chapter "Harmonic Mappings onto Convex Regions" of his book. The idea of Kneser's proof is that a linear combination $a F_1 + b F_2 - c$ of the two coordinate functions changes sign at most twice on the circle, because a line cuts a convex curve at most twice. A critical point would need four sign changes, so the gradients of $F_1$ and $F_2$ are independent everywhere.

Winslow's map $(\xi, \eta)$ goes from the physical domain $\Omega$ to the rectangle $R$ of indices, and the theorem needs the target to be convex. $R$ is convex. A conformal map of the disk onto $\Omega$, which exists by the Riemann mapping theorem and extends to the boundary by Carathéodory's theorem, carries the theorem from the disk to $\Omega$. So for any domain bounded by a Jordan curve, convex or not, $(\xi, \eta)$ is one to one with nonvanishing Jacobian, and its inverse, the grid map, has grid lines that never cross. If instead $x$ and $y$ were made harmonic in $\xi$ and $\eta$, the target would be $\Omega$, and the map could fold on a non-convex domain. Control functions $P, Q \ne 0$ also leave the theorem behind.

The discrete grid inherits only part of this. Its equations are a finite difference approximation with coefficients that depend on the solution, and they have no maximum principle of the kind the proof needs. If discrete solutions converge to the continuous map, cells away from the boundary are positive on fine enough grids. Near the boundary, and at a reentrant corner, nothing is guaranteed, and the hook example shows a converged grid that fails CHECK. The full proofs are below.

## Complexity

Each sweep visits the $(M - 1)(N - 1)$ inner points with a constant amount of work, so it costs $O(n)$ time for $n$ grid points, and the grid needs $O(n)$ space. The number of sweeps has no proved bound, because the iteration is nonlinear. For the linear model problem, the Laplace equation on a square, Gauss-Seidel needs $O(n)$ sweeps for a fixed reduction of the error, and SOR with the best $\omega$ needs $O(\sqrt{n})$, so the totals are $O(n^2)$ and $O(n^{3/2})$. The elliptic iteration behaves about the same in practice: 41 to 94 sweeps to a residual below $10^{-12}$ for the random convex quadrilaterals above with $\omega = 1.5$. [Multigrid](/multigrid-method/) reaches $O(n)$ work for the linear problem and is used for large grids.

## Properties

- **Smooth.** Grid lines are smooth inside the domain, and spacing changes smoothly even when the boundary spacing jumps.
- **No folding in the continuous limit.** With $P = Q = 0$ the continuous map is one to one on every Jordan domain.
- **Boundary fixed.** The boundary points never move. Orthogonality at the boundary is not enforced unless the control functions are chosen for it.
- **Lines crowd at convex sides and spread at concave sides.** In the annulus sector, the circles of the exact solution have radii in geometric progression, so they are closer together near the inner circle, the convex side. A side that bends into the domain gets wider cells.
- **Reproduces affine grids.** A parallelogram with evenly spaced sides is a fixed point.
- **Iterative.** The result depends on the tolerance, and the run time on $\omega$ and the start.

## Variants and improvements

- **Control functions.** Thompson, Thames and Mastin chose $P$ and $Q$ as sums of exponential attraction terms toward given lines and points. Later methods compute $P$ and $Q$ on the boundary from the wanted spacing and angle of the first line of cells, and interpolate them inside.
- **Three dimensions.** The same idea with three harmonic coordinates gives grids of hexahedra. The Radó-Kneser-Choquet theorem has no analogue there: harmonic maps in 3D onto convex sets can fail to be one to one.
- **Other solvers.** Line SOR, alternating direction methods, [multigrid](/multigrid-method/) and Newton's method replace point SOR for large grids.
- **Variational methods.** The elliptic system is close to the Euler-Lagrange equations of smoothness functionals. Brackbill and Saltzman combined smoothness, orthogonality and size terms, and the grid follows from an optimization.
- **Unstructured smoothing.** On an unstructured mesh, [Laplacian smoothing](/laplacian-smoothing/) and the [Tutte embedding](/tutte-embedding/) are the discrete relatives. The Tutte embedding has a discrete guarantee of no folding, which the finite difference scheme lacks.

## When to use it

Use it when a smooth structured grid is needed on a block with curved sides, for example around an airfoil or inside a duct, and the TFI grid is too skewed or folds. Start from TFI, use $P = Q = 0$ first, and add control functions only when spacing near a wall matters. Check the cells after convergence with exact orientation signs. On a block with a sharp reentrant corner, split the block at the corner first. For domains that do not split into four-sided blocks, use an unstructured method such as [advancing front mesh generation](/advancing-front-mesh-generation/).

## Pitfalls

- **Trusting the theorem for the discrete grid.** The continuous map does not fold, but a coarse discrete grid near a reentrant corner can. Check every cell.
- **The wrong direction.** Solving Laplace equations for $x$ and $y$ in $(\xi, \eta)$, instead of the inverted equations, gives a map that can fold on a non-convex domain.
- **Strong control functions.** Large $P$ or $Q$ can push lines across each other; the theorem does not cover them.
- **Over-relaxation too large.** The iteration is nonlinear, and an $\omega$ near 2 can diverge or create a fold on the way. Start with $\omega$ between 1 and 1.5.
- **A folded start.** In the hook example the iteration removed the turned-over cells of the TFI start, but nothing guarantees this, and $\alpha + \gamma$ is zero where the start puts opposite neighbours of a point at the same place.

## Implementations

## History

Alan Winslow proposed in 1966 to make meshes whose lines are equipotentials, by solving the inverted Laplace equations for the coordinates of the mesh points. In 1974 Joe Thompson, Frank Thames and Wayne Mastin built a general method on this, with Poisson equations, control functions that attract lines toward chosen curves and points, and fields with several bodies, and it became known as the TTM method. The book by Thompson, Warsi and Mastin in 1985 made elliptic generation the standard way to smooth structured grids. The univalence of planar harmonic maps onto convex regions, the theorem that explains why the grids do not fold, was posed by Radó in 1926, proved by Kneser the same year, and proved again by Choquet in 1945.

## References
