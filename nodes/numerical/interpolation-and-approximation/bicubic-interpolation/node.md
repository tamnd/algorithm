---
tag: 4YZAGC
kind: algorithm
slug: bicubic-interpolation
name: Bicubic interpolation
aliases:
- Bicubic spline interpolation
- bicubic convolution
- Keys cubic convolution
- tensor-product Catmull-Rom interpolation
area: numerical/interpolation-and-approximation
level: core
summary: Interpolate on a rectangular grid by a cubic Hermite rule in x and in y, with slopes from three-point differences, using the 4 by 4 neighbourhood. C^1, exact on biquadratics, third order.
solves: [interpolation-problem]
model: real-ram
complexity:
  vars: {m: "the number of grid lines in x", n: "the number of grid lines in y", h: "the largest cell side"}
  time: {per_point: Θ(log m + log n)}
  space: {extra: Θ(1)}
  flops: {per_point_uniform: "71"}
properties: {deterministic: true, recursive: false, local: true, smoothness: C1, exact_on: "polynomials of degree at most 2 in each variable"}
history:
  year: 1981
  people: [James C. Ferguson, Steven A. Coons, Edwin Catmull, Raphael Rom, Robert G. Keys]
  note: Bicubic patches with corner values, slopes and twists were used in CAD from the 1960s; Keys (1981) analyzed the cubic convolution kernel with a = -1/2 and showed it is third order.
prereqs: [cubic-hermite-spline, bilinear-interpolation]
see_also: [catmull-rom-spline, tensor-product-interpolation, cubic-spline-interpolation, image-resampling, tensor-product-surface, separable-filter, sinc-interpolation, nearest-neighbor-interpolation]
sources:
  - paper: doi:10.1109/TASSP.1981.1163711
    title: "Robert G. Keys, Cubic convolution interpolation for digital image processing, IEEE Transactions on Acoustics, Speech, and Signal Processing 29(6) (1981) 1153-1160"
    locator: the kernel with a = -1/2, its third-order accuracy and the boundary rule
  - book: isbn:9780521880688
    title: William H. Press, Saul A. Teukolsky, William T. Vetterling and Brian P. Flannery, Numerical Recipes, third edition, Cambridge University Press, 2007
    locator: Section 3.6, Interpolation on a grid in multidimensions (bicubic interpolation from values, gradients and cross derivatives; bicubic spline)
  - book: isbn:9780387953663
    title: Carl de Boor, A Practical Guide to Splines, revised edition, Springer, 2001
    locator: Chapter XVII, Surface approximation by tensor products
  - paper: "Edwin Catmull and Raphael Rom, A class of local interpolating splines, in Computer Aided Geometric Design, R. E. Barnhill and R. F. Riesenfeld (eds.), Academic Press, 1974, 317-326"
    locator: local cubic interpolation with slopes from neighbouring points
  - paper: "Don P. Mitchell and Arun N. Netravali, Reconstruction filters in computer graphics, Computer Graphics (SIGGRAPH 88 Proceedings) 22(4) (1988) 221-228"
    locator: the two-parameter family of cubic filters containing the Catmull-Rom (Keys a = -1/2) kernel
---

Bicubic interpolation estimates a function of two variables from values on a rectangular grid, using the $4 \times 4$ block of grid values around the point. On each axis it uses a one-dimensional rule: the [cubic Hermite spline](/cubic-hermite-spline/) whose slope at each node is the slope of the parabola through that node and its two neighbours. The bicubic value is the tensor product of the two rules: interpolate four rows in one direction, then the four results in the other. The result is $C^1$, exact on polynomials of degree at most 2 in each variable, and third-order accurate. On a uniform grid it is exactly Keys's cubic convolution with $a = -1/2$, the "bicubic" filter of image software, and it is the tensor product of [Catmull-Rom](/catmull-rom-spline/) interpolation. The name also covers two relatives treated under Variants: bicubic Hermite patches with given derivatives, and the bicubic (tensor-product) cubic spline.

## In plain words

[Bilinear interpolation](/bilinear-interpolation/) looks at the 4 grid values around a point and blends them, which gives a surface with creases along the grid lines. Bicubic interpolation looks a little further, at the 16 values in a 4 by 4 block, and fits a smooth cubic curve through each row of four. Then it fits one more smooth curve through the four row results. The extra points tell it which way the surface is sloping at each grid point, so neighbouring cells meet without creases. The price is four times as many values per point, and the result can overshoot a little near sudden jumps, because some of the weights are negative.

## The problem

The input is grid coordinates $x_0, \ldots, x_m$ and $y_0, \ldots, y_n$ (distinct on each axis, in any order), a table $f_{ij} = f(x_i, y_j)$ and a point $(x, y)$. After sorting the axes with the table, the output is $p(x, y) = (S_x \otimes S_y) f$, where $S$ on one axis is this operator on data $(x_k, y_k)$:

- the slope at node $k$ is $d_k = $ the derivative at $x_k$ of the parabola through $x_{k-1}, x_k, x_{k+1}$ for an interior node, through $x_0, x_1, x_2$ for $k = 0$, and through the last three nodes for $k = m$ (with only two nodes, the slope of the chord);
- on $[x_k, x_{k+1}]$, $S$ is the cubic with values $y_k, y_{k+1}$ and slopes $d_k, d_{k+1}$.

Outside the grid the end cubics are extended; with a single coordinate on an axis, $p$ is constant in that direction.

Since $d_k$ is a linear combination of three data values, $S(t) = \sum_k w_k(t) y_k$ with at most four nonzero weights, on the nodes $k - 1, \ldots, k + 2$ for $t$ in cell $k$ (fewer near the ends). Then
$$p(x, y) = \sum_a \sum_b w_a(x)\, w_b(y)\, f_{ab},$$
a weighted sum over the $4 \times 4$ block. On a uniform grid with $s = (t - x_k)/h$, the interior weights are Keys's
$$w_{k-1} = \frac{-s^3 + 2s^2 - s}{2}, \quad w_k = \frac{3s^3 - 5s^2 + 2}{2}, \quad w_{k+1} = \frac{-3s^3 + 4s^2 + s}{2}, \quad w_{k+2} = \frac{s^3 - s^2}{2}.$$

Notation on the interpolation and approximation pages: $f$ is the function, $p$ the interpolant, $h$ the largest cell side. Costs are arithmetic operations on the [real RAM](/real-ram/).

## The algorithm

```pseudo id=main
BICUBIC(x[0 .. m], y[0 .. n], f, X, Y)        ▷ both axes increasing, m, n ≥ 1
L1  i ← the index with x[i] ≤ X < x[i+1], clamped to 0 .. m − 1   ▷ binary search
L2  j ← the index with y[j] ≤ Y < y[j+1], clamped to 0 .. n − 1
L3  (A, α) ← the nodes i − 1 .. i + 2 that exist and the weights of the 1-D rule at X
L4  (B, β) ← the nodes j − 1 .. j + 2 that exist and the weights of the 1-D rule at Y
L5  for each a in A: r[a] ← Σ over b in B of β[b]·f[a][b]   ▷ interpolate the rows in y
L6  return Σ over a in A of α[a]·r[a]                    ▷ then interpolate in x
```

The weights in L3 come from the Hermite basis on $[x_i, x_{i+1}]$: with $\sigma = (X - x_i)/h_i$, $h_{00} = (1 + 2\sigma)(1 - \sigma)^2$, $h_{10} = \sigma(1 - \sigma)^2$, $h_{01} = \sigma^2(3 - 2\sigma)$, $h_{11} = \sigma^2(\sigma - 1)$, the rule is $h_{00} y_i + h_i h_{10} d_i + h_{01} y_{i+1} + h_i h_{11} d_{i+1}$, and substituting the three-point formulas for $d_i, d_{i+1}$ gives the four weights. The order of the two directions does not matter in exact arithmetic.

## Example

Take $x_a = a$, $y_b = b$ for $a, b = 0, \ldots, 3$, data $f_{ab} = a^2 + b$, and the point $(1.5, 1.5)$, the centre of the middle cell. All slopes are central differences, and at $s = 1/2$ the weights on each axis are $(-\frac{1}{16}, \frac{9}{16}, \frac{9}{16}, -\frac{1}{16})$.

- L5: each row $a$ gives $r_a = a^2 + (-\frac{1}{16} \cdot 0 + \frac{9}{16} \cdot 1 + \frac{9}{16} \cdot 2 - \frac{1}{16} \cdot 3) = a^2 + 1.5$.
- L6: $-\frac{1}{16}(0 + 1.5) + \frac{9}{16}(1 + 1.5) + \frac{9}{16}(4 + 1.5) - \frac{1}{16}(9 + 1.5) = 3.75$.

This equals $1.5^2 + 1.5$: the rule reproduces the quadratic exactly, while [bilinear interpolation](/bilinear-interpolation/) gives $(1 + 4)/2 + 1.5 = 4$. If one value is changed, $f_{1,2}$ from 3 to 4, the result rises by the product of its weights, $\frac{9}{16} \cdot \frac{9}{16} = \frac{81}{256}$. A corner value of the block has weight $\frac{1}{256}$; the edge values of the block have negative weights $-\frac{9}{256}$.

**Convergence for $f = \sin(2x)\, e^{y}$ on $[0, 1]^2$** with an $n \times n$ uniform grid, maximum error on $120 \times 120$ sample points (computed in double precision):

| $n$ | whole square | on $[0.25, 0.75]^2$ |
|---|---|---|
| 4 | 1.95e-2 | 4.54e-3 |
| 8 | 2.65e-3 | 5.25e-4 |
| 16 | 3.36e-4 | 6.22e-5 |
| 32 | 4.17e-5 | 7.40e-6 |

The error drops by about 8 per halving of $h$: third order, against second order for bilinear interpolation. The error is a few times larger near the edges, where the slopes are one-sided.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The steps are these.

1. *The one-dimensional rule interpolates and is $C^1$.* On each cell it is the cubic with the prescribed end values and slopes, so it matches $y_k$ at every node. The slope $d_k$ at a node depends only on $k$ (the same three nodes are used by both cells that share $x_k$), so the two cubics meeting at $x_k$ have the same value and slope.
2. *It is exact on quadratics.* If $y_k = q(x_k)$ with $\deg q \le 2$, the parabola through any three nodes is $q$, so $d_k = q'(x_k)$, and the cubic Hermite interpolant of $q$ on a cell is $q$ itself.
3. *Lines L3 to L6 compute the tensor product.* Expanding the double sum gives $p = \sum_a \sum_b w_a(X) w_b(Y) f_{ab}$, which is $S_x$ applied to the results of $S_y$ on each row. It matches $f_{ij}$ at grid points, is $C^1$ in each variable, and reproduces every $x^a y^b$ with $a, b \le 2$ because $S_x \otimes S_y (x^a y^b) = (S_x x^a)(S_y y^b)$.
4. *It is a bicubic Hermite patch.* On each cell $p$ is the bicubic polynomial with corner values $f$, slopes $D_x f$, $D_y f$ and twist $D_x D_y f$, where $D$ is the three-point slope operator. Two patches sharing an edge share these data along it, so $p$ is $C^1$ as a function of two variables.

**Error bounds (proved for the 1-D rule on a uniform grid).** Let $f \in C^4$ on the interval. The cubic Hermite error with exact slopes is at most $\frac{h^4}{384}\|f^{(4)}\|_\infty$. The slope error at an interior node is $\frac{h^2}{6}|f'''(\xi)|$ and at an end node $\frac{h^2}{3}|f'''(\xi)|$, and a slope error $e$ changes the cubic by at most $\frac{h}{4}|e|$ (because $|h_{10}| + |h_{11}| = \sigma(1 - \sigma) \le 1/4$). So
$$\|f - S f\|_\infty \le \frac{h^4}{384}\|f^{(4)}\|_\infty + \frac{h^3}{12}\|f'''\|_\infty,$$
with $h^3/24$ in place of $h^3/12$ on cells away from the ends. In two variables, $f - p = (f - S_x f) + S_x(f - S_y f)$, and $\sum_k |w_k| = 1 + s(1 - s) \le \frac54$ on interior cells (proved; the end cells give the same maximum $\frac54$, computed), so the error is at most $E_x + \frac54 E_y$, where $E_x$ and $E_y$ are the one-dimensional bounds applied to $f$ along each direction. The rate $h^3$ cannot be improved in general, because the rule is not exact on cubics; the table shows it.

## Complexity

Lines L1 and L2 are binary searches with about $\log_2 m + \log_2 n$ comparisons, or $O(1)$ by direct indexing on a uniform grid. On a uniform grid with precomputed $1/h$, each axis needs 3 operations for $s$, 2 for $s^2$ and $s^3$, and 13 for the four weights (the last one as $1$ minus the other three): 18 per axis. Lines L5 and L6 cost $4 \cdot 7 + 7 = 35$ operations. The total is $2 \cdot 18 + 35 = 71$ per point. On a nonuniform grid the slope weights depend on the local spacings and the count roughly doubles, to about 130; they can be precomputed per grid line in $O(m + n)$ space. No setup is needed on a uniform grid. Resampling a whole image is separable: apply the 1-D rule to all rows, then to all columns, which costs about 8 multiplications per output pixel for the sums instead of 20.

**Rounding.** The weights sum to 1 and $\sum |w_a w_b| \le \frac{25}{16}$, so the computed value is accurate to a small multiple of $u \max |f_{ab}|$ over the block; nothing is amplified. At grid points $s = 0$ and the weights are exactly $(0, 1, 0, 0)$ on a uniform grid; on a nonuniform grid they are $1$ and $0$ up to rounding in the slope weights, which the implementation computes from differences.

## Properties

- **Local.** The value depends on the $4 \times 4$ block around the cell (fewer at the edges of the grid).
- **$C^1$, not $C^2$.** The second derivatives jump across grid lines.
- **Exact on $Q_2$**, the polynomials of degree at most 2 in each variable, and not exact on cubics.
- **Third order** for smooth $f$ (proved above, observed in the table).
- **Overshoot.** Some weights are negative. For step data $0, 0, 0, 1, 1, 1$ in one variable the rule dips to $-2/27 \approx -0.074$ before the step and rises to $1 + 2/27$ after it. In images this shows as a thin halo along edges.
- **Separable and linear** in the data.

## Variants and improvements

- **Keys's family.** The kernel with a free parameter $a$ (Keys 1981) and the two-parameter family of Mitchell and Netravali (1988) trade sharpness against ringing; only $a = -1/2$ (this rule) reproduces quadratics and is third order. Image programs sometimes use $a = -0.75$ for sharper results.
- **Bicubic Hermite patches with given derivatives.** When $f_x$, $f_y$ and $f_{xy}$ are known at the grid points, use them in place of the difference estimates; the patch has 16 coefficients per cell and is fourth order. This is the bicubic patch of Ferguson and Coons in geometric design and the routine of Numerical Recipes.
- **Bicubic spline.** Use [cubic spline interpolation](/cubic-spline-interpolation/) along each row and then each column. This is $C^2$ and fourth order but global: every grid value affects every output.
- **Monotone or limited slopes.** Replace the three-point slopes by limited ones, as in [Fritsch-Carlson](/fritsch-carlson-monotone-interpolation/), to suppress overshoot.
- **Higher-order kernels** such as Lanczos windows and, in the band-limited limit, [sinc interpolation](/sinc-interpolation/).

## When to use it

Use bicubic interpolation to resample images and smooth gridded fields when [bilinear interpolation](/bilinear-interpolation/) is too blurry or too creased, and as a fast $C^1$ interpolant for two-dimensional tables. Prefer Hermite patches when derivatives are known, and the bicubic spline when $C^2$ smoothness or fourth-order accuracy matters more than locality. When overshoot is unacceptable, for example for densities or probabilities, use bilinear interpolation or a limited variant. When shrinking images by large factors, prefilter first; any 16-point rule aliases.

## Pitfalls

- **Halos and negative values.** Negative weights produce overshoot near edges and can give negative output from nonnegative data; clamp when the range must be preserved.
- **Edges of the grid.** The 4-point stencil does not fit at the border. This implementation uses one-sided three-point slopes there, which on a uniform grid equals Keys's rule of extending the data by $f_{-1} = 3f_0 - 3f_1 + f_2$. Other choices (clamping, mirroring, periodic wrapping) give different values near the border.
- **Which "bicubic"?** Libraries use the name for this rule, for Keys's kernel with other values of $a$, for Hermite patches and for bicubic splines; their results differ.
- **Nonuniform grids.** Applying the uniform Keys weights to a nonuniform grid loses the quadratic reproduction; use the three-point slopes of the actual spacings, as here.
- **Pixel centres.** As with bilinear interpolation, mixing pixel-corner and pixel-centre coordinates shifts the result by half a pixel.

## Implementations

## History

Bicubic surface patches defined by corner values, slopes and cross derivatives (twists) were introduced in computer-aided design in the 1960s by James Ferguson at Boeing and Steven Coons at MIT. Catmull and Rom (1974) proposed local cubic interpolation with slopes taken from neighbouring points. For image processing, cubic convolution was used to resample satellite imagery in the 1970s, and Robert Keys (1981) analysed the one-parameter kernel, showed that $a = -1/2$ is the only choice that is third order, and gave the boundary rule. Mitchell and Netravali (1988) studied the wider family of cubic reconstruction filters for graphics. The rule is now the "bicubic" option of most image libraries.

## References
