---
tag: 50J7BS
kind: concept
slug: tensor-product-interpolation
name: Tensor-product interpolation
aliases:
- Tensor-product grid interpolation
- Tensor-product interpolant
- Interpolation on Cartesian grids
area: numerical/interpolation-and-approximation
level: advanced
summary: Builds multivariate interpolants by combining one-dimensional rules along each coordinate. Works on Cartesian grids, multiplies Lebesgue constants, and needs n^d points.
prereqs: [multivariate-interpolation, lagrange-interpolation]
see_also: [bilinear-interpolation, bicubic-interpolation, smolyak-sparse-grids, chebyshev-interpolation, b-spline, lebesgue-constant, curse-of-dimensionality, image-resampling]
sources:
  - book: isbn:9780387953663
    title: Carl de Boor, A Practical Guide to Splines, revised edition, Springer, 2001
    locator: Chapter XVII, Surface approximation by tensor products (the tensor-product of linear interpolation schemes and its evaluation)
  - paper: "William J. Gordon, Blending-function methods of bivariate and multivariate interpolation and approximation, SIAM Journal on Numerical Analysis 8 (1971) 158-177"
    locator: tensor products and Boolean sums of univariate projectors
  - paper: "Hans-Joachim Bungartz and Michael Griebel, Sparse grids, Acta Numerica 13 (2004) 147-269"
    locator: full grids, their cost and error, and the hierarchical decomposition that leads to sparse grids
  - paper: "Alex Townsend and Lloyd N. Trefethen, An extension of Chebfun to two dimensions, SIAM Journal on Scientific Computing 35(6) (2013) C495-C518"
    locator: tensor-product Chebyshev grids compared with low-rank approximation
  - book: isbn:9781611975932
    title: Lloyd N. Trefethen, Approximation Theory and Approximation Practice, extended edition, SIAM, 2019
    locator: Chapter 15, Lebesgue constants (the one-dimensional factors of the tensor-product Lebesgue constant)
---

Tensor-product interpolation builds an interpolant in several variables out of interpolants in one variable. The data sit on a Cartesian grid $X_1 \times \cdots \times X_d$; one interpolates along the first coordinate for every fixed value of the others, then along the second, and so on. The result does not depend on the order, it reproduces every function that the one-dimensional rules reproduce in each variable separately, and its accuracy and stability follow directly from the one-dimensional theory. The price is the number of grid points, which is the product of the one-dimensional counts.

## In plain words

Suppose you know a function's values at the crossings of a street grid. To estimate it somewhere between the crossings, first estimate it along each north-south street at your east-west position, using the values on that street. Then estimate along your own east-west line, using those new values. Doing the streets in the other order gives the same answer.

Every good method on a line can be used this way, and it inherits that method's accuracy. The catch is cost: ten points per direction means a hundred in two dimensions, a thousand in three, and ten billion in ten.

## The idea

Notation on the interpolation pages: on $[-1, 1]^d$ (or a box), the grid is $X_1 \times \cdots \times X_d$ with $X_k = \{x^{(k)}_0, \ldots, x^{(k)}_{n_k}\}$; $f_{i_1 \ldots i_d} = f(x^{(1)}_{i_1}, \ldots, x^{(d)}_{i_d})$; $\ell^{(k)}_i$ are the one-dimensional cardinal functions ($\ell^{(k)}_i(x^{(k)}_j) = \delta_{ij}$), for example Lagrange polynomials or cardinal splines; $\Lambda^{(k)}$ is the one-dimensional Lebesgue constant.

**The interpolant.**
$$s(x_1, \ldots, x_d) = \sum_{i_1 = 0}^{n_1} \cdots \sum_{i_d = 0}^{n_d} f_{i_1 \ldots i_d}\, \ell^{(1)}_{i_1}(x_1) \cdots \ell^{(d)}_{i_d}(x_d).$$
Its cardinal functions are products, so $s$ interpolates at every grid point. In operator form $s = (P_1 \otimes \cdots \otimes P_d) f = P_1 P_2 \cdots P_d f$, where $P_k$ interpolates in variable $k$ with the others fixed. The $P_k$ commute, which is why the order does not matter.

**What it reproduces.** If each $P_k$ reproduces a space $V_k$ (for polynomial interpolation, $\mathcal{P}_{n_k}$), the tensor product reproduces $V_1 \otimes \cdots \otimes V_d$: for polynomials, the space $\mathcal{Q}_n$ of polynomials of degree at most $n_k$ in each variable $x_k$, including the mixed term $x_1^{n_1} \cdots x_d^{n_d}$ of total degree $\sum n_k$.

**Stability.** The Lebesgue constant is multiplicative: $\|P_1 \cdots P_d\| = \prod_k \Lambda^{(k)}$ in the maximum norm, since the sum of absolute values of the product cardinal functions factors.

**Error.** Writing $f - P_1 P_2 f = (f - P_1 f) + P_1 (f - P_2 f)$ gives, in two variables,
$$\|f - P_1 P_2 f\|_\infty \le \|f - P_1 f\|_\infty + \Lambda^{(1)} \|f - P_2 f\|_\infty,$$
and by induction in $d$ variables. Each term is a one-dimensional interpolation error, taken uniformly over the other variables. So with Chebyshev points the error for an analytic $f$ decays geometrically in $n$, and for $f$ with $k$ derivatives in each variable like $n^{-k}$, up to the factor $\Lambda^{d-1}$.

**Cost.**

- Samples: $N = \prod_k (n_k + 1)$, that is $(n + 1)^d$.
- Setup: none for Lagrange or barycentric rules; for splines, solve the one-dimensional system along each grid line, $O(N)$ in total for banded systems.
- One evaluation: contract one coordinate at a time, $O(N)$ for global rules; for local rules (linear, cubic) only $2^d$ or $4^d$ cardinal functions are nonzero, so $O(2^d)$ or $O(4^d)$ ([bilinear](/bilinear-interpolation/), [bicubic](/bicubic-interpolation/)).
- On an output grid of $M^d$ points the contractions become matrix products. In 2D, $S = L_1 F L_2^{T}$ costs $O(M n^2 + M^2 n)$ instead of $O(M^2 n^2)$.

**Beyond full grids.** The exponential growth of $N$ with $d$ motivates sparse grids, which use Boolean sums $P_1 \oplus P_2 = P_1 + P_2 - P_1 P_2$ of coarse tensor products ([Smolyak sparse grids](/smolyak-sparse-grids/)), and low-rank approximations $f \approx \sum_{r=1}^{R} u_r(x) v_r(y)$, which keep the separable structure but choose the factors adaptively.

## Examples

**A small exact case.** On the grid $\{0, 1, 2\} \times \{0, 1\}$, use quadratic interpolation in $x$ and linear in $y$:
$$\ell_0(x) = \tfrac{(x - 1)(x - 2)}{2},\ \ell_1(x) = -x(x - 2),\ \ell_2(x) = \tfrac{x(x - 1)}{2}; \qquad m_0(y) = 1 - y,\ m_1(y) = y.$$
For $f(x, y) = x^2 y + 1$ the data are $f_{i0} = 1$ and $f_{i1} = 1 + i^2$, so $s = \sum_i \ell_i(x) \big[(1 - y) + y(1 + i^2)\big] = 1 + y \sum_i i^2 \ell_i(x) = 1 + x^2 y$: the function is in $\mathcal{P}_2 \otimes \mathcal{P}_1$ and is reproduced exactly. At $(0.5, 0.5)$ the six weights $\ell_i(0.5)\, m_j(0.5)$ are $0.1875, 0.375, -0.0625$ for each $j$, and they sum to 1.

**Lebesgue constants.** For Chebyshev points of the second kind the one-dimensional constants are $2.42$, $2.87$ and $3.31$ for $n = 10, 20, 40$; the 2D tensor products have $5.9$, $8.2$ and $11.0$, and in $d$ dimensions about $(\tfrac{2}{\pi} \log n)^d$. Small, but growing with $d$.

**Accuracy in 2D.** For $e^{x + 2y} \cos(xy)$ on $[-1, 1]^2$ the tensor Chebyshev interpolant has error $3.3 \times 10^{-7}$ at $n = 10$ and reaches rounding level, about $7 \times 10^{-15}$, at $n = 20$, as in one dimension. For $1/(1 + 25(x^2 + y^2))$ it needs $n = 80$, that is 6561 samples, for $10^{-7}$. See [multivariate interpolation](/multivariate-interpolation/) for the full table.

**Bilinear interpolation** is the case of two-point linear rules in each variable; on the unit square, $s(x, y) = f_{00}(1 - x)(1 - y) + f_{10}\, x (1 - y) + f_{01} (1 - x) y + f_{11}\, x y$, which is not linear along diagonals: it contains the $xy$ term.

## Where it is used

- Image and volume processing: [bilinear](/bilinear-interpolation/), [bicubic](/bicubic-interpolation/), trilinear and tensor B-spline resampling ([image resampling](/image-resampling/)).
- Spectral methods on boxes: tensor Chebyshev and Legendre grids for PDEs, and tensor Gauss quadrature.
- Tensor-product [B-splines](/b-spline/) and NURBS surfaces in geometric design, evaluated by de Boor's algorithm in each direction.
- Lookup tables in two to four variables in engineering and physics codes.
- The building blocks of sparse grids, and the reference against which their savings are measured.

## References
