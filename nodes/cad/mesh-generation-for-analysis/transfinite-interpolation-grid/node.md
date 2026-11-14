---
tag: FNVCY2
kind: algorithm
slug: transfinite-interpolation-grid
name: Transfinite interpolation grid generation
aliases:
- algebraic grid generation
- Gordon-Hall method
area: cad/mesh-generation-for-analysis
level: core
summary: Gordon and Hall's algebraic grid that blends the boundary curves of a block by a Boolean sum of linear interpolants, the basis of mapped meshing.
solves: [structured-grid-generation]
model: real-ram
complexity:
  vars: {M: the number of cells along the first parameter, N: the number of cells along the second parameter}
  time: {worst: O(M N)}
  space: {extra: O(M N)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1973
  people: [William J. Gordon, Charles A. Hall]
  note: Gordon described the Boolean sum of interpolation projectors in 1971. Gordon and Hall applied it to curvilinear coordinates and mesh generation in 1973.
prereqs: [coons-patch, bilinear-interpolation, structured-grid-generation]
see_also: [elliptic-grid-generation, mesh-generation, scaled-jacobian, orientation-test, tensor-product-surface, hexahedral-mesh-generation, finite-element-method, mesh-quality-measures]
sources:
  - paper: doi:10.1002/nme.1620070405
    title: William J. Gordon and Charles A. Hall, Construction of curvilinear co-ordinate systems and applications to mesh generation, International Journal for Numerical Methods in Engineering 7(4), 1973, 461 to 477
    locator: the transfinite interpolation of the boundary of a block by Boolean sums and its use for grids in two and three dimensions (general locator)
  - paper: doi:10.1137/0708019
    title: William J. Gordon, Blending-function methods of bivariate and multivariate interpolation and approximation, SIAM Journal on Numerical Analysis 8(1), 1971, 158 to 177
    locator: the interpolation projectors, their Boolean sum, and the interpolation of a function on the whole boundary of a rectangle
  - book: isbn:9780444009852
    title: Joe F. Thompson, Z. U. A. Warsi and C. Wayne Mastin, Numerical Grid Generation, Foundations and Applications, North-Holland, 1985
    locator: the chapter on algebraic generation systems (general locator)
---

Transfinite interpolation (TFI) makes a structured grid inside a block with four curved sides. It adds the linear interpolation between the left and right sides to the linear interpolation between the bottom and top sides, and subtracts the bilinear interpolation of the four corners. The grid matches every given boundary point exactly, costs a constant number of operations per point, and has no iteration. It does not guarantee a valid grid: on a strongly curved or concave side the grid lines can cross, so every TFI grid must be checked, and many are then smoothed by [elliptic grid generation](/elliptic-grid-generation/).

## In plain words

Take a region with four sides, like a bent rectangle. Each side has a row of points on it, and opposite sides have the same number of points. We want a net of grid lines inside that joins each point to the matching point on the opposite side.

Draw straight lines from each left point to its right partner, and from each bottom point to its top partner. Each of these two families of lines matches two of the sides but misses the other two. Add the two families and subtract a simple correction made from the four corners, and the result matches all four sides.

The method is fast and direct. It looks only at the sides, so a deep dent in one side can push the inner lines over each other. A good program always checks the grid cells after it builds them.

## The problem

This is [structured grid generation](/structured-grid-generation/) for one block. The input is four sides given as point lists: the bottom $B_0, \ldots, B_M$ and top $T_0, \ldots, T_M$, the left $L_0, \ldots, L_N$ and right $R_0, \ldots, R_N$, with $M, N \ge 1$. The sides must meet at four common corners:

$$B_0 = L_0 = P_{00}, \quad B_M = R_0 = P_{10}, \quad T_0 = L_N = P_{01}, \quad T_M = R_N = P_{11}.$$

The input also gives parameter values $0 = u_0 < \cdots < u_M = 1$ and $0 = v_0 < \cdots < v_N = 1$, which are $i/M$ and $j/N$ by default. The output is the grid $x_{ij}$, $0 \le i \le M$, $0 \le j \le N$, with $x_{i0} = B_i$, $x_{iN} = T_i$, $x_{0j} = L_j$ and $x_{Mj} = R_j$. Cell $(i, j)$ is the quadrilateral $x_{ij}, x_{i+1,j}, x_{i+1,j+1}, x_{i,j+1}$. A grid is valid if every cell is a strictly convex counterclockwise quadrilateral.

## The algorithm

ORIENT2D$(a, b, c) = (b_x - a_x)(c_y - a_y) - (b_y - a_y)(c_x - a_x)$ is the [orientation test](/orientation-test/). CHECK uses it to test the corner Jacobians of each cell, as on the [scaled Jacobian](/scaled-jacobian/) page.

```pseudo id=main
TFI(B, T, L, R, u, v)
L1  if B_0 ≠ L_0 or B_M ≠ R_0 or T_0 ≠ L_N or T_M ≠ R_N then error
L2  P00 ← B_0; P10 ← B_M; P01 ← T_0; P11 ← T_M
L3  for i ← 0 to M do
L4      for j ← 0 to N do
L5          U ← (1 − u_i) L_j + u_i R_j                   ▷ matches left and right
L6          V ← (1 − v_j) B_i + v_j T_i                   ▷ matches bottom and top
L7          C ← (1 − v_j)((1 − u_i) P00 + u_i P10) + v_j((1 − u_i) P01 + u_i P11)
L8          x_ij ← U + V − C
L9  return x

CHECK(x)
L10 for each cell with corners q_0 = x_ij, q_1 = x_{i+1,j}, q_2 = x_{i+1,j+1}, q_3 = x_{i,j+1} do
L11     if ORIENT2D(q_{k−1}, q_k, q_{k+1}) ≤ 0 for some k = 0..3 then return false
L12 return true
```

The grid is the [Coons patch](/coons-patch/) of the sides, sampled at the parameters. In the language of projectors, let $P_u$ interpolate linearly between the left and right sides and $P_v$ between the bottom and top sides. Then $U = P_u$, $V = P_v$, $C = P_u P_v$, and TFI is the Boolean sum

$$P_u \oplus P_v = P_u + P_v - P_u P_v.$$

Points can have any dimension, so the same code makes a grid on a surface patch in 3D from its four boundary curves. In 3D, a block with six faces uses three projectors and

$$P_u \oplus P_v \oplus P_w = P_u + P_v + P_w - P_u P_v - P_v P_w - P_w P_u + P_u P_v P_w,$$

which reads the six faces, subtracts the linear interpolants of the twelve edges and adds back the trilinear interpolant of the eight corners. It reproduces all six faces by the same argument.

## Example

Take a quarter of the annulus between the circles of radii 1 and 2, with $M = N = 2$. The bottom side is the segment $(1, 0), (3/2, 0), (2, 0)$, the top side is $(0, 1), (0, 3/2), (0, 2)$, the left side is the inner arc $(1, 0), (3/5, 4/5), (0, 1)$, and the right side is the outer arc $(2, 0), (6/5, 8/5), (0, 2)$. The arc points are exact rational points on the circles.

| step | value at $i = j = 1$, $u = v = 1/2$ |
|---|---|
| L5, $U$ | $\tfrac12 (3/5, 4/5) + \tfrac12 (6/5, 8/5) = (9/10, 6/5)$ |
| L6, $V$ | $\tfrac12 (3/2, 0) + \tfrac12 (0, 3/2) = (3/4, 3/4)$ |
| L7, $C$ | the average of the four corners, $(3/4, 3/4)$ |
| L8, $x_{11}$ | $(9/10, 6/5)$, which lies on the circle of radius $3/2$ |

The points on the sides come out equal to the input, as the proof says. The four cells have the corner values $(2/5, 3/5, 3/5, 2/5)$, $(3/10, 9/20, 9/20, 3/10)$, $(3/5, 4/5, 4/5, 3/5)$ and $(9/20, 3/5, 3/5, 9/20)$, all positive, so CHECK returns true.

**A grid that folds.** Take the unit square, but replace the bottom side by the hook polyline $(0, 0) \to (3/5, 1/5) \to (2/5, 2/5) \to (1, 0)$, which goes right, turns back to the left, and then goes down to $(1, 0)$. The domain is still a simple polygon. Sample the hook at $u = i/6$ and the straight sides at $v = j/4$. Near the hook, the grid line $j = 1$ follows the turn back: its points at $i = 2, 3, 4$ are $(8/15, 2/5)$, $(1/2, 19/40)$ and $(7/15, 11/20)$. Cells $(2, 0)$ and $(3, 0)$ have all four corner values negative, for example $-1/75$, $-7/400$, $-7/1200$, $-1/600$, so they are turned over. Cells $(2, 1)$ and $(3, 1)$ have mixed signs, so they are not convex. CHECK returns false. A finer grid does not help, because the continuous TFI map itself folds there.

## Correctness

The proof is by substitution. On the bottom side $v = 0$, so $V$ is the bottom point and the corner conditions make $U$ and $C$ the same linear interpolation between $P_{00}$ and $P_{10}$, which cancels. The other three sides are the same. In projector form, $I - P_u \oplus P_v = (I - P_u)(I - P_v)$, and the projectors commute, so the error vanishes where either factor vanishes, which is the whole boundary. The same identity shows that data from a bilinear map $a + bu + cv + e\,uv$ are reproduced exactly, so a parallelogram or any convex quadrilateral with evenly spaced straight sides gives its bilinear grid. With int or Fraction input every value is exact. The full proof is below.

The algorithm only interpolates. Its output is valid exactly when CHECK returns true, and the example above shows that this can fail for a simple domain.

## Complexity

The inner loop runs $(M + 1)(N + 1)$ times, and each iteration does a constant number of operations per coordinate, so the time is $O(MN)$ and the space for the grid is $O(MN)$. CHECK does $4MN$ orientation tests. In 3D, a block of $M \times N \times P$ cells takes $O(MNP)$ time. No linear system is solved, which is why TFI is the usual first grid and the starting point of iterative methods.

## Properties

- **Exact on the boundary.** Every given side point is reproduced, in exact arithmetic exactly.
- **Bilinear precision.** Data from any map that is linear in each parameter are reproduced.
- **Local in the data.** A change of one side point that is not a corner changes only the grid line that starts at it. A change of a corner changes the whole grid.
- **No validity guarantee.** Concave or strongly curved sides can fold the grid.
- **Inherits the spacing of the sides.** Points clustered on a side stay clustered along the grid lines that leave it, and the clustering fades linearly to the opposite side.
- **Explicit and parallel.** Each grid point is computed on its own.

## Variants and improvements

- **Other blending functions.** The linear functions $1 - u$ and $u$ can be replaced by other functions with the same values at 0 and 1, for example the stretching functions that cluster grid lines near a wall. Cubic Hermite blending also uses the derivatives across the sides, which lets the grid lines leave a side at right angles.
- **Arc length parameters.** If $u_i$ is the normalized arc length of the bottom side and it differs from that of the top side, the parameters can be blended between the two, so that each side keeps its own spacing.
- **Three dimensions.** The Boolean sum of three projectors fills a block from its six faces, and is the core of mapped hexahedral meshing and of [hexahedral mesh generation](/hexahedral-mesh-generation/) by blocks.
- **Elliptic smoothing.** TFI gives the initial grid of [elliptic grid generation](/elliptic-grid-generation/), which then iterates to a smooth grid. The continuous harmonic map behind that method does not fold on any domain bounded by a Jordan curve, but its discrete grid has no such proof.

## When to use it

Use TFI for a block whose sides are close to straight or gently curved, when speed matters, and as the initial grid for an elliptic or optimization method. It is the standard way to fill the blocks of a multiblock grid and to place interior points of high order elements with curved sides. Use an [elliptic grid](/elliptic-grid-generation/) or another smoothing step when the block has concave sides or when smooth spacing is needed, and use an unstructured method such as [advancing front mesh generation](/advancing-front-mesh-generation/) when the domain does not split into four-sided blocks.

## Pitfalls

- **Corners that do not match.** If two sides meet at different points, the grid does not close. L1 rejects this input; with floats, compare with a tolerance or share the corner objects.
- **Unchecked folding.** A folded cell has a negative Jacobian and breaks a finite element or finite volume solver. Always run CHECK, with exact orientation signs if the points are close.
- **Opposite sides with different spacing.** If the bottom points cluster to the left and the top points to the right, the grid lines are strongly skewed, and cells can fail CHECK even in a convex quadrilateral. The tests of [elliptic grid generation](/elliptic-grid-generation/) find this for 5 of 25 convex quadrilaterals with random spacing on the sides.
- **Degenerate blocks.** A triangle given as a block with one side of zero length has cells of zero area along that side, and CHECK returns false there.

## Implementations

## History

Steven Coons introduced the bilinearly blended patch for surfaces in the 1960s. William Gordon described interpolation projectors and their Boolean sums in general in 1971. The word transfinite means that the interpolant matches a function on whole curves or surfaces, not only at finitely many points. In 1973 Gordon and Hall used it to build curvilinear coordinate systems and meshes for numerical methods. It became the standard algebraic method of the numerical grid generation books of the 1980s, and it remains the default way to fill structured blocks.

## References
