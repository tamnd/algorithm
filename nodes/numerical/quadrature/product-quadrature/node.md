---
tag: W907MC
kind: technique
slug: product-quadrature
name: Product quadrature
aliases:
- tensor-product quadrature
- iterated quadrature
- product rule
- tensor product rule
area: numerical/quadrature
level: core
summary: Apply a one-dimensional rule in each coordinate; the cost grows exponentially with dimension.
prereqs: [multidimensional-integration, quadrature-rule]
see_also: [cubature-rule, gauss-legendre-quadrature, tensor-product-interpolation, sparse-grid-quadrature, monte-carlo-integration, curse-of-dimensionality, gauss-hermite-quadrature, kronecker-product]
sources:
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Section 5.6, Cartesian products and product rules; Section 5.8, Compound rules (in several dimensions)
  - book: "A. H. Stroud, Approximate Calculation of Multiple Integrals, Prentice-Hall, 1971"
    locator: Chapter 2, Product formulas (including conical product rules for the simplex)
  - paper: doi:10.1017/S0962492904000182
    title: Hans-Joachim Bungartz and Michael Griebel, Sparse grids, Acta Numerica 13, 2004, 147-269
    locator: Section 3 (the cost of full tensor product grids against sparse grids)
---

Product quadrature integrates over a box $[a_1, b_1] \times \cdots \times [a_s, b_s]$ by applying a one-dimensional [quadrature rule](/quadrature-rule/) in each coordinate. With rules $R_k$ of $n_k$ nodes, the product rule has $N = n_1 \cdots n_s$ nodes, the grid of all combinations, and weights equal to products of one-dimensional weights. It is the same as integrating one variable at a time with the inner integrals done numerically. It inherits accuracy and stability from its factors, but its cost grows like $n^s$, so it is the standard method in two or three dimensions and useless beyond about six.

## In plain words

To find the volume under a surface over a rectangle, first pick the points you would use along the $x$ side and along the $y$ side, and use every pair as a sample point. Each sample gets a weight: its $x$ weight times its $y$ weight. Add up weight times height.

This is the same as doing the inner integral along $y$ for each fixed $x$ with the one-dimensional rule, then integrating those results along $x$. Whatever the one-dimensional rule is good at, the product rule is good at too. The price is the number of points: ten points per direction is a hundred in two dimensions, a thousand in three and ten billion in ten. That growth is the curse of dimensionality.

## When it applies

- The region is a box, or a smooth map of one: a disc in polar coordinates, a triangle by the collapsed map $(u, v) \mapsto (u, (1 - u) v)$, a ball in spherical coordinates. The Jacobian of the map then joins the integrand or the weight.
- The dimension is small, $s \le 3$ in general and up to about 6 for very smooth integrands with few points per direction.
- The integrand is smooth in each variable, or has a known weight that factors, $w(x) = w_1(x_1) \cdots w_s(x_s)$, such as a Gaussian density, for which each factor gets its own Gauss rule.
- The data are already on a grid, for example values on a rectangular mesh.

## The template

```pseudo id=main
PRODUCT-RULE(f, RULE_1, ..., RULE_s)         ▷ RULE_k = nodes x^(k)_1..x^(k)_n_k, weights w^(k)_1..w^(k)_n_k on [a_k, b_k]
L1  total ← 0
L2  for each (i_1, ..., i_s) with 1 ≤ i_k ≤ n_k do
L3      x ← (x^(1)_i_1, ..., x^(s)_i_s)
L4      W ← w^(1)_i_1 · w^(2)_i_2 · ... · w^(s)_i_s
L5      total ← total + W · f(x)
L6  return total
```

The holes are the one-dimensional rules $\mathrm{RULE}_k$, one per coordinate: [Gauss-Legendre](/gauss-legendre-quadrature/), [Clenshaw-Curtis](/clenshaw-curtis-quadrature/), a composite [Simpson](/simpsons-rule/) or [trapezoidal](/trapezoidal-rule/) rule, or a Gauss rule for a weight. In operator form the rule is $Q = R_1 \otimes R_2 \otimes \cdots \otimes R_s$: the weights form the [Kronecker product](/kronecker-product/) of the weight vectors. Iterated evaluation, applying $R_s$ to each line in direction $s$, then $R_{s-1}$, and so on, gives the same sum with $O(N)$ operations.

**Exactness.** Let $R_k$ be exact for polynomials of degree at most $d_k$ in $x_k$. Then $Q$ is exact for every monomial $x_1^{\alpha_1} \cdots x_s^{\alpha_s}$ with $\alpha_k \le d_k$ for all $k$, and so for the tensor space spanned by them. *Proof.* For such a monomial both the integral (by Fubini) and the rule factor: $Q(x^\alpha) = \prod_k R_k(x_k^{\alpha_k}) = \prod_k \int_{a_k}^{b_k} x_k^{\alpha_k}\,dx_k = \int_B x^\alpha\,dx$. Linearity extends this to the span. $\square$ In particular $Q$ has total degree of exactness $\min_k d_k$, and no more in general: $x_k^{d_k + 1}$ fails.

**Error.** Write $I_k$ for the exact integral in coordinate $k$ and $E_k = I_k - R_k$. The telescoping identity

$$I_1 \otimes \cdots \otimes I_s - R_1 \otimes \cdots \otimes R_s = \sum_{k=1}^{s} R_1 \otimes \cdots \otimes R_{k-1} \otimes E_k \otimes I_{k+1} \otimes \cdots \otimes I_s$$

says that the total error is a sum of one-dimensional errors, each applied along one coordinate to a partly integrated function. If every $R_j$ has positive weights, $\|R_j\| = b_j - a_j$, and so

$$|E(f)| \le \sum_{k=1}^{s} \Big(\prod_{j \ne k} (b_j - a_j)\Big) \sup_{\text{lines in direction } k} |E_k(f \text{ on the line})|.$$

So the error is at most $s$ times the worst one-dimensional error on lines through the box. For a rule of order $p$ in each direction with $n$ points and $f$ with bounded derivatives of order $p$ in each variable, the error is $O(s\, n^{-p})$ with $N = n^s$ points, that is $O(N^{-p/s})$.

## Classic examples

- **Tensor Gauss-Legendre on a square.** [Gauss-Legendre](/gauss-legendre-quadrature/) with $n$ points per side, $N = n^2$. For $e^{x + y}$ on $[0, 1]^2$, with exact value $(e - 1)^2 = 2.9524924420$, the errors for $n = 1, \ldots, 5$ are $0.234$, $1.32 \times 10^{-3}$, $2.83 \times 10^{-6}$, $3.21 \times 10^{-9}$ and $2.25 \times 10^{-12}$. The 2-point product rule is exact for $x^3 y^3$, which has total degree 6, but fails on $x^4$, with error $-1/180$.
- **The curse of dimensionality.** The 3-point Gauss rule in each direction for $e^{x_1 + \cdots + x_s}$ on $[0, 1]^s$ has relative error $4.8 \times 10^{-7}$, $9.6 \times 10^{-7}$, $1.9 \times 10^{-6}$, $2.9 \times 10^{-6}$ and $3.8 \times 10^{-6}$ for $s = 1, 2, 4, 6, 8$, growing like $s$ times the one-dimensional error as the error formula says, while the number of points is $3, 9, 81, 729, 6561$. See the [curse of dimensionality](/curse-of-dimensionality/).
- **Gaussian expectations.** $\mathbb{E}[g(Z)]$ for a standard normal vector $Z$ in $\mathbb{R}^s$ factors into the weight $\prod_k e^{-x_k^2}$ after scaling, and the product of [Gauss-Hermite rules](/gauss-hermite-quadrature/) handles it; this is common in statistics and uncertainty quantification for small $s$.
- **Periodic integrands.** For $f$ periodic in every variable, the product of periodic [trapezoidal rules](/trapezoidal-rule/) converges geometrically in each direction and can be evaluated with a multidimensional [fast Fourier transform](/fast-fourier-transform/).
- **Finite elements.** Element integrals on quadrilaterals and hexahedra in the [finite element method](/finite-element-method/) use tensor Gauss rules on the reference square or cube.

## Variations

- **Different rules per direction.** Use more points where $f$ varies more. Anisotropic grids save work when some variables matter less.
- **Composite and adaptive products.** Split the box into sub-boxes and apply a product rule on each, refining where an error estimate is large; this is how most two- and three-dimensional adaptive integrators work.
- **Collapsed coordinates.** The Duffy map sends the square to a triangle with Jacobian $1 - u$, and a [Gauss-Jacobi rule](/gauss-jacobi-quadrature/) in $u$ absorbs that factor. Stroud's conical product rules do the same for simplices of any dimension.
- **Sparse grids.** The Smolyak combination of small product rules keeps most of the accuracy with far fewer points, $O(n (\log n)^{s-1})$ instead of $n^s$; see [sparse grid quadrature](/sparse-grid-quadrature/).
- **Non-product cubature.** Rules designed for total degree on a given region, such as those in Stroud's tables, need fewer points than a product rule of the same total degree; see [cubature rules](/cubature-rule/).
- **Product integration in one dimension.** The name is also used for rules for $\int k(x) f(x)\,dx$ that interpolate only $f$ and integrate the products $k \ell_i$ exactly, as in [Filon quadrature](/filon-quadrature/). That is a different technique.

## Pitfalls

- **Counting the cost.** $N = n^s$ grows fast: 10 points per direction in 10 dimensions is $10^{10}$ evaluations. Past $s \approx 5$, switch to [Monte Carlo](/monte-carlo-integration/), [quasi-Monte Carlo](/quasi-monte-carlo-integration/) or sparse grids.
- **Misreading the degree.** A product of degree-$d$ rules is exact for $x^\alpha$ with each $\alpha_k \le d$, not for every polynomial of total degree $s d$. Its total degree of exactness is only $d$.
- **Singularities on lines.** An integrand singular along a diagonal or a curve, such as $|x - y|^{-1/2}$, breaks the smoothness that each one-dimensional rule needs. Split the region along the singular set or change variables first.
- **Ignoring the Jacobian.** After mapping a disc or a triangle to a box, the Jacobian must be included in the integrand or the weight, and it can create an endpoint singularity that a Gauss-Jacobi rule should absorb.
- **Negative one-dimensional weights.** Products of rules with mixed-sign weights have $\sum |W| = \prod_k \sum_i |w^{(k)}_i|$, so the amplification of errors multiplies across dimensions.

## Exercises

1. Show that the product of positive rules is positive and that $\sum |W| = \prod_k (b_k - a_k)$, the volume of the box.
2. With the 2-point Gauss rule on $[0, 1]^2$, verify in exact arithmetic that $x^3 y^3$ is integrated exactly and $x^4$ and $x^4 y$ are not.
3. A product rule of order $p$ in each direction needs about $\tau^{-s/p}$ points for an error $\tau$. For $p = 4$ and $\tau = 10^{-6}$, find the dimension at which Monte Carlo with $\sigma = 1$ needs fewer points.

## References
