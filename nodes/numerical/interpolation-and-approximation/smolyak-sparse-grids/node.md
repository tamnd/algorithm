---
tag: Y27RRZ
kind: algorithm
slug: smolyak-sparse-grids
name: Smolyak sparse grid interpolation
aliases:
- Sparse grid interpolation
- Smolyak construction
- Smolyak algorithm
- Combination technique
area: numerical/interpolation-and-approximation
level: research
summary: Interpolates a function of d variables by a signed sum of small tensor-product interpolants. It needs O(2^L L^(d-1)) points instead of (2^L+1)^d, and pays off for smooth, nearly separable functions.
solves: [multivariate-interpolation]
model: real-ram
complexity:
  vars: {N: the number of sparse grid points, d: the dimension, L: the level, T: the total number of points of the component tensor grids}
  time: {fit: Θ(N), evaluate: Θ(d T)}
  space: {extra: Θ(N d)}
  flops: {evaluate: "3 d T"}
properties: {deterministic: true, recursive: false, interpolates_with_nested_nodes: true, linear_in_data: true, exact_on_total_degree_L: true}
history:
  year: 1963
  people: [Sergey A. Smolyak]
  note: Smolyak (1963) built quadrature and interpolation formulas for tensor product classes from one-dimensional ones; the method was revived for interpolation, PDEs and uncertainty quantification from the 1990s.
prereqs: [tensor-product-interpolation, polynomial-interpolation]
see_also: [sparse-grid-quadrature, curse-of-dimensionality, chebyshev-interpolation, clenshaw-curtis-quadrature, multivariate-interpolation, lebesgue-constant, monte-carlo-integration, scattered-data-interpolation]
sources:
  - paper: "Sergey A. Smolyak, Quadrature and interpolation formulas for tensor products of certain classes of functions, Soviet Mathematics Doklady 4 (1963) 240-243"
    locator: the construction from differences of one-dimensional formulas
  - paper: "Volker Barthelmann, Erich Novak and Klaus Ritter, High dimensional polynomial interpolation on sparse grids, Advances in Computational Mathematics 12 (2000) 273-288"
    locator: the combination formula, interpolation with nested nodes, polynomial exactness and error bounds for Chebyshev extrema
  - paper: "Grzegorz W. Wasilkowski and Henryk Woźniakowski, Explicit cost bounds of algorithms for multivariate tensor product problems, Journal of Complexity 11 (1995) 1-56"
    locator: the combination formula for Smolyak's algorithm and cost bounds
  - paper: "Hans-Joachim Bungartz and Michael Griebel, Sparse grids, Acta Numerica 13 (2004) 147-269"
    locator: hierarchical bases, point counts and approximation orders for piecewise linear sparse grids, the combination technique
  - paper: "Lloyd N. Trefethen, Cubature, approximation, and isotropy in the hypercube, SIAM Review 59 (2017) 469-491"
    locator: the comparison of sparse, tensor and total degree approximation and the effect of rotations
---

Smolyak's construction builds an interpolant in $d$ variables from one-dimensional interpolation rules without using the full tensor grid. Instead of interpolating on a product grid with $n$ points in every direction, it adds up many coarse tensor-product interpolants, each fine in a few directions and coarse in the others, with signed integer weights. The resulting sparse grid has $O(2^L L^{d-1})$ points at level $L$, where the full grid has $(2^L + 1)^d$, and for functions with bounded mixed derivatives it loses only logarithmic factors in accuracy. It is a standard tool in uncertainty quantification, high-dimensional PDEs and surrogate modelling, but it is not a cure for every high-dimensional function.

## In plain words

To sample a function of many inputs on a full grid, every combination of input values is needed, and the count explodes: ten points per input in ten inputs is ten billion samples.

Smolyak's idea is that the fine detail in one input rarely needs fine detail in all the others at once. So it builds many small grids, each detailed in only a few inputs, and combines their interpolants with plus and minus signs so that the double-counted parts cancel. The union of these grids, the sparse grid, has far fewer points.

This works well when the function is smooth and its inputs interact weakly. When the important behaviour runs along a diagonal, the savings shrink or vanish.

## The problem

Notation on the interpolation pages: $f : [-1, 1]^d \to \mathbb{R}$; for each level $i \ge 1$, $X^i$ is a set of $m(i)$ one-dimensional nodes with $m(1) = 1$ and $m(i) = 2^{i-1} + 1$, nested ($X^i \subset X^{i+1}$), here the Chebyshev extrema $-\cos(\pi j/(m(i) - 1))$ (Clenshaw-Curtis points) with $X^1 = \{0\}$; $U^i$ is polynomial interpolation on $X^i$, $U^0 = 0$ and $\Delta^i = U^i - U^{i-1}$; multi-indices $\mathbf{i} = (i_1, \ldots, i_d)$ have entries $\ge 1$ and $|\mathbf{i}| = i_1 + \cdots + i_d$; $q = d + L$ for the level $L \ge 0$.

**Smolyak's operator.**
$$A(q, d) = \sum_{|\mathbf{i}| \le q} \Delta^{i_1} \otimes \cdots \otimes \Delta^{i_d} = \sum_{q - d + 1 \le |\mathbf{i}| \le q} (-1)^{q - |\mathbf{i}|} \binom{d - 1}{q - |\mathbf{i}|}\, U^{i_1} \otimes \cdots \otimes U^{i_d}.$$
The first form shows the idea: keep the tensor products of detail operators whose levels add up to at most $q$, a simplex of levels instead of a cube. The second, the **combination formula**, shows how to compute it from ordinary [tensor-product interpolants](/tensor-product-interpolation/). The **sparse grid** is $H(q, d) = \bigcup_{|\mathbf{i}| = q} X^{i_1} \times \cdots \times X^{i_d}$, which contains all points the operator uses.

## The algorithm

```pseudo id=main
SMOLYAK(f, d, L, t)
L1  for every multi-index i ≥ 1 with max(d, L + 1) ≤ |i| ≤ d + L:
L2      c_i ← (−1)^(d+L−|i|) · binom(d − 1, d + L − |i|)
L3      sample f on X^(i_1) × ... × X^(i_d), reusing values at points already sampled
L4      s ← s + c_i · (U^(i_1) ⊗ ... ⊗ U^(i_d) f)(t)
L5  return s
```

The implementation stores each node by its exact position $j/(m - 1)$ in $[0, 1]$, so nested nodes are recognized exactly and $f$ is evaluated once per sparse grid point; with equally spaced nodes ($2k - 1$) it runs in exact rational arithmetic for tests. Each tensor interpolant at $t$ is a sum over its grid of products of one-dimensional Lagrange weights.

## Example

**Small grids.** For $d = 2$, $L = 1$ ($q = 3$) the combination formula is
$$A(3, 2) = U^2 \otimes U^1 + U^1 \otimes U^2 - U^1 \otimes U^1,$$
a three-point rule along the $x$ axis plus a three-point rule along the $y$ axis minus their shared centre value: the sparse grid is the cross of 5 points $(0,0), (\pm1, 0), (0, \pm1)$, exact on $1, x, y, x^2, y^2$ but not on $xy$. The numbers of points:

| $L$ | 0 | 1 | 2 | 3 | 4 | full grid at $L = 4$ |
|---|---|---|---|---|---|---|
| $d = 2$ | 1 | 5 | 13 | 29 | 65 | 289 |
| $d = 4$ | 1 | 9 | 41 | 137 | 401 | 83521 |
| $d = 10$ | 1 | 21 | 221 | 1581 | 8801 | $2.0 \times 10^{12}$ |

**Accuracy at equal cost.** Maximum error at 60 random points (seed 3) in $[-1, 1]^d$, against a full Chebyshev tensor grid with about the same number of points $n^d$:

| $f$ | $d$ | $L$ | sparse points | sparse error | tensor points | tensor error |
|---|---|---|---|---|---|---|
| $e^{-\lVert x \rVert^2/2}$ | 2 | 6 | 321 | $9.6 \times 10^{-10}$ | $18^2 = 324$ | $1.2 \times 10^{-13}$ |
| | 4 | 5 | 1105 | $9.5 \times 10^{-5}$ | $6^4 = 1296$ | $2.0 \times 10^{-3}$ |
| | 8 | 4 | 3937 | $1.8 \times 10^{-2}$ | $3^8 = 6561$ | $6.7 \times 10^{-2}$ |
| $\cos(x_1 + \cdots + x_d)$ | 2 | 6 | 321 | $3.0 \times 10^{-11}$ | 324 | $1.7 \times 10^{-15}$ |
| | 4 | 5 | 1105 | $6.3 \times 10^{-3}$ | 1296 | $1.6 \times 10^{-4}$ |
| $1/(1.5 + \bar{x})$, $\bar{x}$ the mean | 4 | 5 | 1105 | $8.8 \times 10^{-4}$ | 1296 | $1.3 \times 10^{-5}$ |
| | 8 | 3 | 849 | $1.9 \times 10^{-3}$ | $2^8 = 256$ | $6.9 \times 10^{-2}$ |

In two dimensions the full grid wins. For the separable Gaussian the sparse grid wins clearly from $d = 4$ on. For the ridge functions $\cos(\sum x_j)$ and $1/(1.5 + \bar x)$, whose variation runs along the diagonal, the full grid is better at $d = 4$; only at $d = 8$, where a comparable full grid has 2 points per direction, does the sparse grid help. These are observations for these functions, consistent with Trefethen's (2017) analysis of anisotropy.

## Correctness

Three facts make the algorithm correct; the proof file proves them.

- **The combination formula equals the difference form.** Expanding each $\Delta^{i} = U^{i} - U^{i-1}$ and collecting the coefficient of $U^{k_1} \otimes \cdots \otimes U^{k_d}$ gives $\sum_{r=0}^{q - |\mathbf{k}|} (-1)^r \binom{d}{r}$, which equals $(-1)^{q - |\mathbf{k}|} \binom{d-1}{q - |\mathbf{k}|}$ when $q - |\mathbf{k}| \le d - 1$ and $0$ otherwise.
- **Polynomial exactness.** If $\deg g_j \le m(k_j) - 1$ for some $\mathbf{k}$ with $|\mathbf{k}| \le q$, then $A(q, d)(g_1 \otimes \cdots \otimes g_d) = g_1 \otimes \cdots \otimes g_d$, because $\Delta^i g_j = 0$ for $i > k_j$ and the remaining differences telescope. In particular $A(q, d)$ reproduces every polynomial of total degree at most $L$, and many of higher degree.
- **Interpolation.** With nested nodes, $A(q, d) f$ equals $f$ at every point of the sparse grid $H(q, d)$, because $\Delta^i g$ vanishes on $X^{i-1}$.

## Complexity

- **Points (proved).** For fixed $d$, $|H(q, d)| = \Theta(2^L L^{d-1})$ as $L \to \infty$, against $(2^L + 1)^d$ for the full grid with the same finest resolution. The constant grows quickly with $d$; the table shows the actual counts.
- **Fit:** one evaluation of $f$ per sparse grid point, $N$ in all; usually the evaluations of $f$ dominate everything else.
- **Evaluation:** the combination form costs $\Theta(d T)$ per point, where $T$ is the total size of the component grids, plus $O(d\, m^2)$ for the one-dimensional weights. $T$ is a small multiple of $N$ in practice ($T/N$ was 2.6 to 4.8 for the cases in the table; observed, not a bound). Converting once to a hierarchical or Chebyshev coefficient form gives evaluation in $O(N d)$ independent of the component grids.
- **Space:** $\Theta(N d)$ for the points and values.

## Properties

- **Error bound (proved, Barthelmann, Novak and Ritter 2000).** For Chebyshev extrema and $f$ with continuous mixed derivatives $\partial^{\alpha} f$, $\alpha_j \le k$, $\|f - A(q, d) f\|_\infty \le c_{d,k}\, N^{-k} (\log N)^{(k+2)(d-1)+1}$ times a norm of those derivatives. A full tensor grid with $N$ points gives only about $N^{-k/d}$ for functions with $k$ derivatives in each variable. The constant $c_{d,k}$ is not small, so the bound is asymptotic.
- **Piecewise linear sparse grids (proved, Bungartz and Griebel).** With hat functions instead of polynomials, the error is $O(h^2 |\log_2 h|^{d-1})$ in the maximum norm for $f$ with bounded mixed second derivatives, $h = 2^{-L}$, using $O(h^{-1} |\log_2 h|^{d-1})$ points.
- **Stability.** The operator norm is at most $\sum_{\mathbf{i}} |c_{\mathbf{i}}| \prod_j \Lambda_{m(i_j)}$, with $\Lambda_m$ the one-dimensional [Lebesgue constant](/lebesgue-constant/); for Chebyshev nodes this grows only polylogarithmically in $N$ for fixed $d$. With equispaced nodes it grows exponentially and the method is useless beyond small levels.
- **Linear in $f$**, and **interpolatory** with nested nodes. Without nesting the formula still defines an approximation, but it needs more points and does not interpolate.
- **Not rotation invariant.** The space favours functions that are sums of terms each depending strongly on few coordinates; ridge functions along diagonals are approximated much worse than their axis-aligned versions.

## Variants and improvements

- **Sparse grid quadrature.** Integrating $A(q, d) f$ gives Smolyak cubature, built from one-dimensional rules such as [Clenshaw-Curtis](/clenshaw-curtis-quadrature/) or Gauss-Patterson; see [sparse grid quadrature](/sparse-grid-quadrature/).
- **Hierarchical (surplus) form.** Write the interpolant in a hierarchical basis; the coefficients (surpluses) measure local detail and drive adaptive refinement. Piecewise linear hat functions give the sparse grids of Zenger and of Bungartz and Griebel.
- **Combination technique** (Griebel, Schneider and Zenger 1992). The same signed sum, applied to solutions of PDEs on anisotropic full grids, which existing solvers can compute in parallel.
- **Dimension-adaptive and anisotropic grids** (Gerstner and Griebel). Choose the multi-index set greedily from estimated surpluses instead of a simplex, which helps when some variables matter more than others.
- **Slower growth rules.** Using $m(i) = 2i - 1$ or Leja sequences gives finer control of the number of points; Leja points are nested for every count.

## When to use it

Use Smolyak sparse grids for smooth functions of roughly 4 to 30 variables that are expensive to evaluate and whose variables interact weakly: parametric PDEs and uncertainty quantification with random inputs, surrogate models of simulations, and high-dimensional quadrature with smooth integrands. In 2 or 3 dimensions prefer full tensor-product or [Chebyshev interpolation](/chebyshev-interpolation/); for rough functions, or very high dimensions, prefer Monte Carlo or quasi-Monte Carlo, which do not depend on smoothness; for scattered data use [scattered data methods](/scattered-data-interpolation/).

## Pitfalls

- **Negative weights.** The combination coefficients alternate in sign, so the sum can amplify noise in $f$ and rounding; with noisy samples use regression on the same polynomial space instead.
- **Equispaced nodes.** Polynomial interpolation on nested equally spaced points has exponentially growing Lebesgue constants; use Chebyshev extrema, Leja points, or piecewise linear bases.
- **Ridge and rotated functions.** Accuracy depends on the coordinate system; a function that is easy along a diagonal can need many more points than a sparse grid offers. Check by rotating or by comparing with a tensor grid on a test case.
- **Discontinuities and kinks.** Global polynomials ring; use local hierarchical bases with adaptivity.
- **The curse is reduced, not removed.** The factor $L^{d-1}$ and the constants still grow with $d$, so "high dimensional" means tens of variables, not thousands (see [curse of dimensionality](/curse-of-dimensionality/)).
- **Counting points.** Reusing values at nested points is essential; a naive implementation that samples every component grid evaluates $f$ several times more often than necessary.

## Implementations

## History

Sergey Smolyak introduced the construction in 1963 for quadrature and interpolation of functions in tensor product classes, with the error bounds that motivate it. The idea was taken up in information-based complexity, where Wasilkowski and Woźniakowski (1995) gave the combination formula and explicit cost bounds, and in numerical PDEs, where Zenger (1991) introduced sparse grids of hat functions and Griebel, Schneider and Zenger (1992) the combination technique. Barthelmann, Novak and Ritter (2000) analysed polynomial interpolation on sparse grids of Chebyshev extrema, Gerstner and Griebel developed sparse grid quadrature and dimension adaptivity, and stochastic collocation methods from about 2005 made sparse grids a standard tool in uncertainty quantification. Trefethen (2017) pointed out that their advantage depends on the axis alignment of the function.

## References
