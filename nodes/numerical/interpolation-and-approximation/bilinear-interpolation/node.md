---
tag: 15TKW4
kind: algorithm
slug: bilinear-interpolation
name: Bilinear interpolation
aliases:
- bilinear interpolant
- Q1 interpolation
area: numerical/interpolation-and-approximation
level: core
summary: Interpolate on a rectangular grid by linear interpolation in x, then in y, inside the cell around the point. Continuous, exact on a + bx + cy + dxy, error O(h^2), 17 operations per point.
solves: [interpolation-problem]
model: real-ram
complexity:
  vars: {m: "the number of grid lines in x", n: "the number of grid lines in y", h: "the largest cell side"}
  time: {per_point: Θ(log m + log n)}
  space: {extra: Θ(1)}
  flops: {per_point: "17"}
properties: {deterministic: true, recursive: false, local: true, smoothness: C0, exact_on: "span of 1, x, y, xy"}
history:
  year: 1964
  people: [Milton Abramowitz, Irene A. Stegun, Lance Williams]
  note: Two-way interpolation in printed tables is much older; the four-point bivariate formula is listed in Abramowitz and Stegun (1964), and bilinear texture filtering became standard in graphics in the 1980s.
prereqs: [piecewise-linear-interpolation, interpolation-problem]
see_also: [bicubic-interpolation, tensor-product-interpolation, nearest-neighbor-interpolation, bilinear-filtering, texture-mapping, mipmap, image-resampling, scattered-data-interpolation]
sources:
  - book: isbn:9780486612720
    title: Milton Abramowitz and Irene A. Stegun (eds.), Handbook of Mathematical Functions, Dover, 1965 reprint of the 1964 NBS edition
    locator: Section 25.2, bivariate interpolation, formula 25.2.66 (four-point formula)
  - book: isbn:9780387953663
    title: Carl de Boor, A Practical Guide to Splines, revised edition, Springer, 2001
    locator: Chapter XVII, Surface approximation by tensor products
  - book: isbn:9780521880688
    title: William H. Press, Saul A. Teukolsky, William T. Vetterling and Brian P. Flannery, Numerical Recipes, third edition, Cambridge University Press, 2007
    locator: Section 3.6, Interpolation on a grid in multidimensions (bilinear interpolation)
  - paper: "Paul S. Heckbert, Survey of texture mapping, IEEE Computer Graphics and Applications 6(11) (1986) 56-67"
    locator: texture filtering, bilinear interpolation of texels
  - paper: "Lance Williams, Pyramidal parametrics, Computer Graphics (SIGGRAPH 83 Proceedings) 17(3) (1983) 1-11"
    locator: mipmaps with bilinear interpolation within a level and linear interpolation between levels
---

Bilinear interpolation estimates a function of two variables from its values on a rectangular grid. It finds the grid cell that contains the point, interpolates linearly along the two horizontal edges of the cell, and then linearly between the two results. The interpolant on each cell is $c_0 + c_1 x + c_2 y + c_3 xy$: linear along every line parallel to an axis, but curved (a saddle) along diagonals. It is continuous across cells, exact for functions of that form, and for smooth $f$ has error at most $\frac{h_x^2}{8}\|f_{xx}\|_\infty + \frac{h_y^2}{8}\|f_{yy}\|_\infty$. In graphics the same operation on texture images is called bilinear filtering.

## In plain words

You know the height of a surface at the corners of a square, and you want the height at a point inside. First walk along the bottom edge: the height there is a weighted average of the two bottom corners, with more weight on the closer corner. Do the same along the top edge. Then move up from the bottom point to the top point and take a weighted average again.

The result is an average of the four corners. Each corner's weight is the area of the rectangle on the opposite side of the point, so closer corners count more. On a grid of many squares, you do this in whichever square contains the point. Neighboring squares agree along their shared edge, so the surface has no jumps, but it can have creases along grid lines.

## The problem

The input is grid coordinates $x_0, \ldots, x_m$ and $y_0, \ldots, y_n$ (distinct on each axis, in any order), a table $f_{ij} = f(x_i, y_j)$, and a point $(x, y)$. After sorting both axes with the table, the output is $p(x, y)$, where $p$ is continuous, and on each cell $R_{ij} = [x_i, x_{i+1}] \times [y_j, y_{j+1}]$ it lies in $Q_1 = \operatorname{span}\{1, x, y, xy\}$ and matches $f$ at the four corners. Outside the grid the end cell is extended. With a single coordinate on an axis, $p$ is taken constant in that direction.

On one cell, with $u = (x - x_i)/(x_{i+1} - x_i)$ and $v = (y - y_j)/(y_{j+1} - y_j)$,
$$p = (1 - u)(1 - v) f_{i,j} + u(1 - v) f_{i+1,j} + (1 - u) v f_{i,j+1} + u v f_{i+1,j+1}.$$
This $p$ is the only element of $Q_1$ with these corner values: the four conditions form a linear system whose determinant is nonzero for any rectangle, since an element of $Q_1$ that vanishes at the corners is linear and zero on each edge, and then zero on every vertical segment.

Notation on the interpolation and approximation pages: $f$ is the function, $p$ the interpolant, $h_x = \max_i (x_{i+1} - x_i)$ and $h_y = \max_j (y_{j+1} - y_j)$. Costs are arithmetic operations on the [real RAM](/real-ram/).

## The algorithm

```pseudo id=main
BILINEAR(x[0 .. m], y[0 .. n], f, X, Y)        ▷ both axes increasing, m, n ≥ 1
L1  i ← the index with x[i] ≤ X < x[i+1], clamped to 0 .. m − 1   ▷ binary search
L2  j ← the index with y[j] ≤ Y < y[j+1], clamped to 0 .. n − 1
L3  u ← (X − x[i]) / (x[i+1] − x[i])
L4  v ← (Y − y[j]) / (y[j+1] − y[j])
L5  a ← (1 − u)·f[i][j] + u·f[i+1][j]            ▷ along the edge y = y[j]
L6  b ← (1 − u)·f[i][j+1] + u·f[i+1][j+1]        ▷ along the edge y = y[j+1]
L7  return (1 − v)·a + v·b
```

Interpolating first in $y$ and then in $x$ gives the same value in exact arithmetic, because both orders expand to the four-term formula above. Unsorted axes are sorted once with the table in $O(m \log m + n \log n)$ plus the cost of permuting the table.

## Example

Take the unit square with $f_{00} = 1$, $f_{10} = 3$, $f_{01} = 2$, $f_{11} = 6$ (the first index is $x$), and the point $(1/4, 1/2)$, so $u = 1/4$, $v = 1/2$.

- L5: $a = \frac34 \cdot 1 + \frac14 \cdot 3 = 1.5$.
- L6: $b = \frac34 \cdot 2 + \frac14 \cdot 6 = 3$.
- L7: $p = \frac12 \cdot 1.5 + \frac12 \cdot 3 = 2.25$.

The four weights are $\frac38, \frac18, \frac38, \frac18$, which sum to 1, and $\frac38 + \frac38 + \frac34 + \frac34 = 2.25$.

**The saddle.** With corners $f_{00} = f_{11} = 0$ and $f_{10} = f_{01} = 1$, the interpolant is $p = u + v - 2uv$. Along the diagonal $u = v = t$ it is $2t - 2t^2$, a parabola with value $1/2$ at the center: bilinear interpolation is not linear. Splitting the square into two triangles and interpolating linearly on each would give $0$ or $1$ at the center, depending on which diagonal is chosen.

**Convergence for $f = e^{x + y}$ on $[0, 1]^2$** with an $n \times n$ grid of equal cells, maximum error on a fine grid (computed in double precision) against the bound $2 \cdot \frac{h^2}{8} e^2$:

| $n$ | max error | bound |
|---|---|---|
| 4 | 9.07e-2 | 1.15e-1 |
| 8 | 2.53e-2 | 2.89e-2 |
| 16 | 6.68e-3 | 7.22e-3 |
| 32 | 1.72e-3 | 1.80e-3 |
| 64 | 4.36e-4 | 4.51e-4 |

The error drops by 4 per halving of $h$ and approaches the bound, which is sharp (see Correctness).

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The steps are these.

1. *The cell.* Lines L1 and L2 find a cell $[x_i, x_{i+1}] \times [y_j, y_{j+1}]$ containing the point (or the nearest end cell for points outside the grid).
2. *Corner values.* At a corner, $u$ and $v$ are each 0 or 1, and L5 to L7 return that corner's value. This holds in floating point too: at $X = x_i$ the numerator of $u$ is exactly 0, at $X = x_{i+1}$ the numerator and denominator are the same rounded number, so $u = 1$ exactly, and the weights $1 - u$, $u$ are then exactly $0$ and $1$.
3. *Form.* L5 and L6 are linear in $u$, and L7 is linear in $v$, so the result is $c_0 + c_1 u + c_2 v + c_3 uv$, which lies in $Q_1$ since $u$ and $v$ are affine in $x$ and $y$. By uniqueness it is the $Q_1$ interpolant.
4. *Continuity.* On a shared vertical edge $x = x_{i+1}$, both cells give $(1 - v) f_{i+1,j} + v f_{i+1,j+1}$, which depends only on the two shared corners. The same holds for horizontal edges, so $p$ is continuous.

**Error bound (proved).** Let $R$ be a cell with sides $h_x$, $h_y$, and suppose $f_{xx}$ and $f_{yy}$ exist and are continuous on $R$. Then for $(x, y) \in R$,
$$|f(x, y) - p(x, y)| \le \frac{h_x^2}{8} \max_R |f_{xx}| + \frac{h_y^2}{8} \max_R |f_{yy}|.$$
Write $I_x$ and $I_y$ for linear interpolation in one variable. Then $p = I_x I_y f$ and $f - p = (f - I_x f) + I_x (f - I_y f)$. The first term is bounded by the one-dimensional bound $\frac{h_x^2}{8}\max|f_{xx}|$ ([piecewise linear interpolation](/piecewise-linear-interpolation/)), and $I_x$ takes convex combinations, so the second is at most $\frac{h_y^2}{8}\max|f_{yy}|$. The bound needs no mixed derivative, because $xy$ is reproduced. For $f = x^2$ it is attained at the middle of each cell, so the constant $1/8$ cannot be lowered.

## Complexity

Lines L1 and L2 are binary searches with about $\log_2 m + \log_2 n$ comparisons; on a uniform grid, the cell index is $\lfloor (X - x_0)/h_x \rfloor$ in $O(1)$, and when points arrive in order a moving pointer is $O(1)$ amortized. Lines L3 and L4 cost 3 operations each, forming $1 - u$ and $1 - v$ costs 2, and L5, L6 and L7 cost 3 each: 17 operations per point, with 2 divisions. On a uniform grid the divisions become multiplications by precomputed $1/h$. No setup and no extra space beyond the table are needed.

**Rounding.** For $X$ inside the cell, $0 \le u, v \le 1$ up to rounding, and each of L5 to L7 is a convex combination, so the computed value is the exact bilinear value of slightly perturbed corner data and perturbed $u, v$; the error is a small multiple of $u_{\text{mach}} \max |f_{ij}|$ over the four corners. No step can amplify errors, unlike high-degree polynomial interpolation.

## Properties

- **Local.** The value depends only on the four corners of the cell.
- **Exact on $Q_1$.** It reproduces $c_0 + c_1 x + c_2 y + c_3 xy$, in particular every affine function.
- **Maximum principle.** Inside the grid, the value lies between the smallest and largest of the four corner values, since the weights are nonnegative and sum to 1. There is no overshoot.
- **$C^0$ only.** The gradient jumps across grid lines, which shows as creases in surfaces and as a faint star or diamond pattern when images are enlarged a lot.
- **Separable.** It is the tensor product of one-dimensional linear interpolation; the order of the two directions does not matter.
- **Not rotation invariant.** It depends on the orientation of the grid; rotating the data by 45 degrees changes the interpolant.
- **Second-order accurate** for smooth $f$, as proved above.

## Variants and improvements

- **Trilinear and multilinear interpolation.** In $d$ dimensions use the $2^d$ corners of the cell and $2^d - 1$ one-dimensional interpolations. Trilinear interpolation is used for volume data and, between [mipmap](/mipmap/) levels, for textures.
- **Uniform grids.** Compute the cell index and fractions directly from $X/h$, which is the usual form in image processing and on GPUs ([bilinear filtering](/bilinear-filtering/)).
- **Bilinear quadrilaterals.** The map from the unit square to any quadrilateral by the same four-term formula is the Q1 finite element; finding $(u, v)$ for a given point then needs a quadratic equation.
- **Triangulation.** Split each cell along a diagonal and interpolate linearly on the triangles. This is linear on each triangle but depends on the choice of diagonal.
- **Smoother alternatives.** [Bicubic interpolation](/bicubic-interpolation/) uses 16 values and is $C^1$; [nearest-neighbor interpolation](/nearest-neighbor-interpolation/) is cheaper and discontinuous. For data not on a grid, see [scattered data interpolation](/scattered-data-interpolation/).

## When to use it

Use bilinear interpolation for fast, robust lookup in two-dimensional tables, for resampling images and textures at moderate scale factors, and as the default when the data may be rough and overshoot must not happen. It is the natural interpolant for data on a rectangular grid when second-order accuracy is enough. When the gradient must be continuous, or when the data are smooth and accuracy matters, use bicubic or tensor-product spline interpolation. When shrinking an image by a large factor, prefilter first (mipmaps or an area average); bilinear interpolation alone samples only four pixels and aliases.

## Pitfalls

- **Pixel centers.** In images, sample $(i, j)$ usually sits at $(i + 0.5, j + 0.5)$ in continuous coordinates; mixing the two conventions shifts the image by half a pixel.
- **The cheaper lerp is not exact at the far end.** Writing $a + u(b - a)$ saves two operations, but at $u = 1$ it returns $\mathrm{fl}(a + \mathrm{fl}(b - a))$, which can differ from $b$: with $a = 1$, $b = 10^{-17}$ it returns 0. The form $(1 - u)a + ub$ used here returns $b$ exactly at $u = 1$.
- **NaN and infinity spread.** In the four-weight form, a NaN or infinite corner gives NaN even when its weight is 0, because $0 \cdot \infty$ is NaN. Mask missing data before interpolating.
- **Extrapolation.** Outside the grid the end cell is extended, and the $xy$ term grows quickly; clamp the point to the grid if that is not wanted.
- **Not linear on diagonals.** Do not expect straight contour lines; the contours of a bilinear patch are hyperbolas.
- **Downsampling aliasing.** See When to use it.

## Implementations

## History

Interpolating in two-way tables by linear interpolation in each argument in turn was routine in the era of printed tables, and the four-point bivariate formula appears in Abramowitz and Stegun's Handbook (1964) together with its higher-order relatives. In finite element analysis the bilinear quadrilateral became one of the basic elements in the 1960s. In computer graphics, bilinear interpolation of texture samples, together with Lance Williams's mipmaps (1983), became the standard way to filter textures, and Heckbert's 1986 survey describes it; it is now built into GPU texture hardware.

## References
