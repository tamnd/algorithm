---
tag: 7P964K
kind: problem
slug: structured-grid-generation
name: Structured grid generation
aliases:
- body-fitted grid generation
- mapped meshing
area: cad/mesh-generation-for-analysis
level: core
summary: Map a logically rectangular grid onto a physical domain so grid lines follow the boundaries, as finite difference, finite volume and mapped element solvers need.
prereqs: [mesh-generation, bilinear-interpolation]
see_also: [transfinite-interpolation-grid, elliptic-grid-generation, hexahedral-mesh-generation, scaled-jacobian, mesh-quality-measures, finite-difference-method, finite-volume-method, advancing-front-mesh-generation]
sources:
  - book: isbn:9780444009852
    title: Joe F. Thompson, Z. U. A. Warsi and C. Wayne Mastin, Numerical Grid Generation, Foundations and Applications, North-Holland, 1985
    locator: the chapters on boundary-conforming coordinate systems, algebraic generation, elliptic generation and hyperbolic generation (general locator)
  - book: isbn:9780849326875
    title: Joe F. Thompson, Bharat K. Soni and Nigel P. Weatherill (editors), Handbook of Grid Generation, CRC Press, 1999
    locator: the part on structured grids, with algebraic, elliptic and hyperbolic methods, multiblock grids and grid quality (general locator)
  - paper: doi:10.1002/nme.1620070405
    title: William J. Gordon and Charles A. Hall, Construction of curvilinear co-ordinate systems and applications to mesh generation, International Journal for Numerical Methods in Engineering 7(4), 1973, 461 to 477
    locator: transfinite interpolation as an algebraic grid generator (general locator)
  - paper: doi:10.1016/0021-9991(74)90114-4
    title: Joe F. Thompson, Frank C. Thames and C. Wayne Mastin, Automatic numerical generation of body-fitted curvilinear coordinate system for field containing any number of arbitrary two-dimensional bodies, Journal of Computational Physics 15(3), 1974, 299 to 319
    locator: elliptic generation of body-fitted coordinates with control functions (general locator)
  - paper: doi:10.1137/0901031
    title: Joseph L. Steger and Denny S. Chaussee, Generation of body-fitted coordinates using hyperbolic partial differential equations, SIAM Journal on Scientific and Statistical Computing 1(4), 1980, 431 to 437
    locator: hyperbolic marching grid generation from a body surface (general locator)
---

Structured grid generation asks for a grid of points $x_{ij}$, indexed like the cells of a rectangle, that fills a physical domain so that the outer grid lines lie on its boundary. Every interior point has four neighbours, so a solver can store the grid as an array and use the same difference formulas everywhere. The grid must not fold, and its cells should be close to square and change size smoothly. The problem is easy for domains that look like a deformed rectangle and hard for complex shapes, which must first be cut into such blocks.

## In plain words

Take a sheet of graph paper and stretch it, without tearing or folding, so that its four edges lie on the four sides of a region, such as the space around a wing. The lines of the paper now follow the shape of the region. A computer can do its calculations on the stretched paper as if it were still a plain square, because each small square still has the same neighbours.

The hard parts are to choose where the lines go inside, so that no small square turns over or becomes very thin, and to cut a complicated region into pieces that each look like a stretched square.

## Definition

**Input (2D, one block).** A domain $\Omega$ in the plane bounded by a closed curve, with four marked points on it that split it into four sides, called bottom, right, top and left, in counterclockwise order. Points on the sides: $M + 1$ on the bottom and top and $N + 1$ on the left and right, so that the sides share their end points at the four corners.

**Output.** Points $x_{ij}$ for $0 \le i \le M$ and $0 \le j \le N$ such that $x_{i0}$, $x_{iN}$, $x_{0j}$ and $x_{Mj}$ are the given boundary points, and every cell, the quadrilateral

$$Q_{ij} = (x_{ij},\ x_{i+1,j},\ x_{i+1,j+1},\ x_{i,j+1}),$$

is **valid**: its four corner values, the cross products of the two edges at each corner,

$$\det(x_{i+1,j} - x_{ij},\ x_{i,j+1} - x_{ij})$$

and the three like it, are all positive. So each cell is a strictly convex counterclockwise quadrilateral.

**Why the corner values.** Map the unit square onto a cell by the bilinear map $X(s, t) = a + b s + c t + d s t$. Then $X_s = b + d t$ and $X_t = c + d s$, so

$$\det(X_s, X_t) = \det(b, c) + s \det(b, d) + t \det(d, c),$$

because $\det(d, d) = 0$. The Jacobian is an affine function of $(s, t)$, so it is positive on the whole square if and only if it is positive at the four corners, and at each corner it equals the corner value. Validity is therefore exact and local, and the [scaled Jacobian](/scaled-jacobian/) is these corner values divided by the edge lengths.

**Continuous form.** Find a homeomorphism $x$ from the unit square onto $\overline{\Omega}$ that takes the sides to the sides, is smooth inside, and has $\det(x_u, x_v) > 0$. The grid is then $x_{ij} = x(u_i, v_j)$ for increasing parameters $u_i$ and $v_j$.

**Quality.** Among valid grids, the user wants cells near the boundary of a given size, angles near $90°$ (small skew), bounded aspect ratio, and a small size ratio between neighbouring cells. These goals are measured by the [mesh quality measures](/mesh-quality-measures/), and they often conflict.

## Variants

- **Three dimensions.** The input is a solid with six marked faces, and the output is $x_{ijk}$ with valid hexahedral cells. The trilinear Jacobian is not affine, so the corner test is necessary but no longer sufficient.
- **Surface grids.** The grid lies on a curved surface, usually in the parameter plane of a [tensor product surface](/tensor-product-surface/).
- **Grid topologies around a body.** An O-grid wraps around a body, with one index periodic. A C-grid wraps around the body and continues along the wake. An H-grid keeps four sides with the body inside one of them.
- **Multiblock grids.** A complex domain is cut into four-sided blocks in 2D or six-sided blocks in 3D, each gridded on its own, with matching points on shared faces. Choosing the blocks is the hard part, and it is usually done by hand or from a medial axis, as in [medial axis decomposition meshing](/medial-axis-decomposition-meshing/).
- **Overset grids.** Blocks overlap instead of matching, and the solver interpolates between them.
- **Orthogonal and conformal grids.** All grid lines meet at right angles. In 2D a conformal map onto a rectangle gives such a grid, but a domain with four marked points can be mapped conformally only onto a rectangle of one aspect ratio, its conformal modulus, so the boundary point distribution cannot be chosen freely.
- **Adaptive grids.** Points move to follow features of the solution, by control functions or by a sizing rule like a [mesh sizing function](/mesh-sizing-function/).
- **Boundary layer grids.** Very thin cells next to a wall, grown outward. See [boundary layer mesh generation](/boundary-layer-mesh-generation/).

## Examples

**Convex quadrilateral, uniform spacing.** Let the domain be the quadrilateral with corners $A = (0,0)$, $B = (4,0)$, $C = (3,3)$, $D = (0,2)$, and put the midpoint on each side, so $M = N = 2$. [Transfinite interpolation](/transfinite-interpolation-grid/) places the single interior point at $(7/4, 5/4)$, the average of the four corners. The 16 corner values of the four cells are all positive, between $3/2$ and $3$, so the grid is valid. At $A$ the corner value is $2 = \tfrac14 \det(B - A, D - A)$, as Theorem 2 below says.

**Annulus sector.** For the region $1 \le r \le 2$, $0 \le \theta \le \pi/2$, the polar grid $x_{ij} = r_j (\cos\theta_i, \sin\theta_i)$ with $r_j$ and $\theta_i$ increasing is valid: each cell is an isosceles trapezoid in counterclockwise order. Its grid lines, the circles and the rays, meet at right angles. The [elliptic grid generation](/elliptic-grid-generation/) page compares TFI and the elliptic method with an exact conformal grid of an annulus sector.

**Folding.** Let the bottom side double back on itself, with an inner angle of about $349°$ at one corner of the bottom polyline. Both TFI and the elliptic method, with the same boundary points, give grids with folded cells next to that corner. The worked numbers are on the two algorithm pages.

**Non-example.** If a marked corner has an inner angle of $180°$ or more, no valid grid with those corners exists, by Theorem 3 below. An L-shaped domain is therefore gridded as one block only if its reflex corner is not a marked corner; a reflex point in the middle of a side is allowed.

## Known algorithms

- **Algebraic (transfinite interpolation).** [Transfinite interpolation](/transfinite-interpolation-grid/) blends the four sides with the formula of the [Coons patch](/coons-patch/). It reproduces the boundary exactly, costs $O(MN)$, and has no guarantee against folding.
- **Elliptic.** The [elliptic method](/elliptic-grid-generation/) solves the Laplace or Poisson equations for the computational coordinates, iterated with [Gauss-Seidel](/gauss-seidel-method/), [SOR](/successive-over-relaxation/) or a [multigrid method](/multigrid-method/). The continuous map never folds, the grid is smooth, and control functions set the spacing.
- **Hyperbolic.** Steger and Chaussee (1980) march outward from a body surface, one layer at a time, solving equations for orthogonality and cell area. It is fast and gives orthogonal grids near walls, but the outer boundary cannot be prescribed.
- **Conformal mapping.** Exact orthogonal grids for 2D domains, with the limits above.
- **Repair.** A grid with folded cells is repaired by [mesh untangling](/mesh-untangling/) and improved by [optimization-based smoothing](/optimization-based-mesh-smoothing/) or [Laplacian smoothing](/laplacian-smoothing/).

## Bounds

**Theorem 1 (time).** A grid has $(M + 1)(N + 1)$ points, so any method needs $\Omega(MN)$ time, and TFI reaches this. The validity check costs $O(MN)$ exact [orientation tests](/orientation-test/), one per cell corner, by the affine Jacobian fact of the Definition. An elliptic solve costs $O(MN)$ per sweep, times the number of sweeps.

**Theorem 2 (TFI is valid for matched spacing on a convex quadrilateral).** Let $A, B, C, D$ be a strictly convex counterclockwise quadrilateral. Let $0 = u_0 < \dots < u_M = 1$ and $0 = v_0 < \dots < v_N = 1$, and put the boundary points at the same fractions on opposite sides: $x_{i0} = (1 - u_i)A + u_i B$, $x_{iN} = (1 - u_i)D + u_i C$, $x_{0j} = (1 - v_j)A + v_j D$, $x_{Mj} = (1 - v_j)B + v_j C$. Then the TFI grid with parameters $u_i$ and $v_j$ is valid.

*Proof.* Let $X(u, v) = (1-u)(1-v)A + u(1-v)B + uvC + (1-u)vD$, the bilinear map of the quadrilateral. The three terms of TFI at $(u_i, v_j)$ are the interpolation between $x_{0j}$ and $x_{Mj}$ at $u_i$, the interpolation between $x_{i0}$ and $x_{iN}$ at $v_j$, and the bilinear interpolation of the corners. With these boundary points each of the three is $X(u_i, v_j)$, so TFI gives $x_{ij} = X(u_i, v_j)$. The map $Y(s, t) = X(u_i + s\,\Delta u, v_j + t\,\Delta v)$, with $\Delta u = u_{i+1} - u_i$ and $\Delta v = v_{j+1} - v_j$, is bilinear with corners the corners of the cell $Q_{ij}$, and it is linear along each edge of the unit square. So the edge vectors at a corner are the partial derivatives of $Y$ there, and each corner value of $Q_{ij}$ equals $\Delta u\,\Delta v \det(X_u, X_v)$ at that corner. By the Definition, $\det(X_u, X_v)$ is affine on the unit square, and at its corners it equals $\det(B - A, D - A)$, $\det(C - B, A - B)$, $\det(D - C, B - C)$ and $\det(A - D, C - D)$, the corner values of $ABCD$, which are positive because it is strictly convex and counterclockwise. An affine function that is positive at the four corners of a square is positive on all of it. So every corner value of every cell is positive. $\blacksquare$

Without matched spacing the theorem fails: on the TFI page, 5 of 25 convex quadrilaterals with random spacing give folded TFI grids.

**Theorem 3 (a necessary condition).** If a valid grid exists, then the boundary turns left strictly at each of the four marked corners, that is, the inner angle there is strictly between $0°$ and $180°$.

*Proof.* The corner value of the cell $Q_{00}$ at $x_{00}$ is $\det(x_{10} - x_{00},\ x_{01} - x_{00})$. Both points are given boundary points, the neighbours of the corner along the bottom and the left side. This number is the orientation of the boundary at the corner, and it is positive exactly when the boundary turns left there. The other three corners are the same. $\blacksquare$

**Continuous existence.** For every domain bounded by a Jordan curve with four marked points, a homeomorphism of the unit square onto it that takes sides to sides exists, by the Riemann mapping theorem and Carathéodory's extension. The elliptic method gives one that is smooth with positive Jacobian inside, by the theorem of Radó, Kneser and Choquet; the proof and its limits are on the [elliptic grid generation](/elliptic-grid-generation/) page. A discrete grid with fixed boundary points does not inherit this guarantee, as the folding example shows.

## Reductions

- **To surface patches.** Algebraic grid generation is the same problem as filling a four-sided patch from its boundary curves, and TFI is the [Coons patch](/coons-patch/) formula applied in the plane.
- **To an elliptic boundary value problem.** Elliptic generation reduces the problem to a nonlinear system on the grid points, solved by the relaxation and multigrid methods of numerical linear algebra.
- **To general meshing.** A multiblock structured grid is a quadrilateral mesh in 2D or a hexahedral mesh in 3D with a block structure, so it is a special case of [hexahedral mesh generation](/hexahedral-mesh-generation/), and it can be made by [hexahedral sweeping](/hexahedral-sweeping/) when the solid is a swept shape. The general [mesh generation](/mesh-generation/) problem asks for a triangulation of a domain whose triangles have bounded angles and sizes. Unstructured methods such as [Delaunay refinement](/delaunay-refinement/) and the [advancing front method](/advancing-front-mesh-generation/) solve it for any shape, at the cost of an irregular data structure.

## Applications

- **Computational fluid dynamics.** Finite difference and [finite volume](/finite-volume-method/) solvers on body-fitted multiblock grids around wings, turbine blades and vehicles, where the regular structure gives fast and accurate solvers and thin cells near walls.
- **Finite difference methods.** The [finite difference method](/finite-difference-method/) needs a logically rectangular grid, and a body-fitted map carries a curved domain to a rectangle.
- **Mapped meshing in finite element tools.** Preprocessors for the [finite element method](/finite-element-method/) mesh four-sided faces and swept solids with mapped quadrilaterals and hexahedra.
- **Ocean and weather models.** Curvilinear grids that follow coastlines or the sphere.
- **Domain decomposition.** The blocks of a multiblock grid give a natural split for [domain decomposition](/domain-decomposition/) on parallel computers.

## References
