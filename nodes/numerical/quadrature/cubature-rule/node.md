---
tag: XN9G0S
kind: definition
slug: cubature-rule
name: Cubature rule
aliases:
- multidimensional quadrature rule
- cubature formula
- multivariate quadrature rule
area: numerical/quadrature
level: advanced
summary: A weighted sum of multivariate function values, exact for polynomials up to a given degree.
prereqs: [quadrature-rule, degree-of-precision]
see_also: [multidimensional-integration, product-quadrature, sparse-grid-quadrature, gaussian-quadrature, monte-carlo-integration, quasi-monte-carlo-integration, discrepancy, smolyak-sparse-grids]
sources:
  - book: "A. H. Stroud, Approximate Calculation of Multiple Integrals, Prentice-Hall, 1971"
    locator: Chapters 1 to 3 (definitions, invariance, product formulas, the lower bound on the number of points) and the tables of formulas for the square, triangle, cube and sphere, including Radon's degree 5 formula
  - paper: doi:10.1017/S0962492900002701
    title: "Ronald Cools, Constructing cubature formulae, the science behind the art, Acta Numerica 6 (1997) 1-54"
    locator: Sections 2 to 4 (the definition of degree, the lower bounds of Stroud and Möller, Tchakaloff's theorem)
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Chapter 5, Integration in two or more dimensions (product rules and rules of given degree)
  - paper: "Johann Radon, Zur mechanischen Kubatur, Monatshefte für Mathematik 52 (1948) 286-300"
    locator: the 7-point rule of degree 5 for the square and the construction from orthogonal polynomials
  - paper: "Vladimir Tchakaloff, Formules de cubatures mécaniques à coefficients non négatifs, Bulletin des Sciences Mathématiques 81 (1957) 123-134"
    locator: the existence of positive rules of degree d with at most dim P_d nodes
  - paper: "H. Michael Möller, Kubaturformeln mit minimaler Knotenzahl, Numerische Mathematik 25 (1976) 185-200"
    locator: the improved lower bound for centrally symmetric regions in the plane
  - paper: "Ronald Cools, An encyclopaedia of cubature formulas, Journal of Complexity 19 (2003) 445-453"
    locator: the online collection of known rules and their degrees
---

A cubature rule approximates an integral over a region in $\mathbb{R}^s$, $s \ge 2$, by a weighted sum of function values, $\sum_i w_if(x_i)$. It is the multivariate form of a [quadrature rule](/quadrature-rule/), and its main measure of quality is its *degree*: the largest $d$ such that it integrates every polynomial of total degree at most $d$ exactly, the analogue of the [degree of precision](/degree-of-precision/). Unlike the one-dimensional case, there is no universal recipe for optimal nodes: rules are built by products of one-dimensional rules, by symmetry and moment equations, or by sparse combinations, and the minimal number of nodes for a given degree is known only in special cases.

## Definition

**Notation.** As on all quadrature pages: $I(f) = \int f\,w$, a rule $Q_n(f) = \sum_{i=1}^n w_if(x_i)$ where $n$ counts nodes, $E_n = I - Q_n$, and $d$ the degree. Here $s \ge 1$ is the dimension, $\Omega \subset \mathbb{R}^s$ is a region (closure of an open set) and $w \ge 0$ is a weight function on $\Omega$ with $\int_\Omega w > 0$ and finite moments $\int_\Omega\lvert x^\alpha\rvert w$. For a multi-index $\alpha \in \mathbb{N}^s$, $x^\alpha = x_1^{\alpha_1}\cdots x_s^{\alpha_s}$ has total degree $\lvert\alpha\rvert = \alpha_1 + \cdots + \alpha_s$. $\mathcal{P}^s_k$ is the space of real polynomials in $s$ variables of total degree at most $k$, of dimension $\binom{s + k}{s}$.

A **cubature rule** for $I(f) = \int_\Omega f(x)\,w(x)\,dx$ is a linear functional
$$Q_n(f) = \sum_{i=1}^n w_if(x_i)$$
with distinct nodes $x_i \in \mathbb{R}^s$ and real weights $w_i \ne 0$. It has **degree** $d$ if
$$E_n(p) = 0 \text{ for all } p \in \mathcal{P}^s_d,\qquad\text{and}\qquad E_n(p) \ne 0 \text{ for some } p \in \mathcal{P}^s_{d+1}.$$
Since $E_n$ is linear, it suffices to check the $\binom{s + d}{s}$ monomials $x^\alpha$ with $\lvert\alpha\rvert \le d$, and to find one monomial of degree $d + 1$ that fails. For $s = 1$ this is a quadrature rule and its degree of precision.

**Qualities.** A rule is *positive* if all $w_i > 0$, *inside* if all $x_i \in \Omega$, and a *PI rule* (Stroud) if it is both. Positive rules of degree $d \ge 0$ have $\sum_i\lvert w_i\rvert = I(1)$, which bounds the effect of errors in the values $f(x_i)$; inside rules never evaluate $f$ where it may be undefined.

**Invariance.** An affine map $x = Ay + c$ with $A$ invertible preserves total degree, so a rule of degree $d$ for $\Omega$ maps to a rule of degree $d$ for $A^{-1}(\Omega - c)$, with weights multiplied by $\lvert\det A\rvert$ when $w = 1$. One rule for the standard square, triangle or simplex therefore serves for every parallelogram, triangle or simplex.

**Bounds on the number of nodes.** Let $\Omega$ have nonempty interior and $w > 0$ almost everywhere on it.

- *Lower bound (proved).* Every rule of degree $d$ has $n \ge \dim\mathcal{P}^s_{\lfloor d/2\rfloor} = \binom{s + \lfloor d/2\rfloor}{s}$. If $n$ were smaller, the $n$ linear conditions $p(x_i) = 0$ on $\mathcal{P}^s_{\lfloor d/2\rfloor}$ would have a nonzero solution $p$. Then $p^2 \in \mathcal{P}^s_d$, so $I(p^2) = Q_n(p^2) = 0$, which is impossible because a nonzero polynomial cannot vanish on a set of positive measure.
- *Möller's bound (cited).* For a centrally symmetric planar region and odd degree $d = 2k - 1$, $n \ge \binom{k + 1}{2} + \lfloor k/2\rfloor$: 4 nodes for $d = 3$, 7 for $d = 5$, 12 for $d = 7$ (Möller 1976).
- *Upper bound (cited).* Tchakaloff's theorem: for compact $\Omega$ there is a positive inside rule of degree $d$ with at most $\binom{s + d}{s}$ nodes (Tchakaloff 1957; Cools 1997, Section 4).

A rule that attains the lower bound is sometimes called *Gaussian*, by analogy with the one-dimensional case, where $\lfloor d/2\rfloor + 1 = n$ gives $d = 2n - 1$. In several variables such rules exist only for special regions, weights and degrees.

## Examples and non-examples

All identities below are checked in rational arithmetic. On the square $[-1, 1]^2$ the rules are symmetric under $x \mapsto -x$ and $y \mapsto -y$, so every monomial with an odd exponent integrates to $0$ on both sides, and only the squared coordinates enter, which are rational.

- **Product Gauss, $2 \times 2$, on the square.** Nodes $(\pm\frac{1}{\sqrt3}, \pm\frac{1}{\sqrt3})$, weights $1$. A product of two $k$-point [Gauss-Legendre](/gauss-legendre-quadrature/) rules integrates $x^ay^b$ exactly whenever $a, b \le 2k - 1$, so its total degree is $2k - 1$, here $3$. It fails at $y^4$: $I(y^4) = \frac45$, $Q(y^4) = \frac49$, $E = \frac{16}{45}$. With $n = 4$ nodes it meets Möller's bound for $d = 3$, so no rule of degree 3 on the square has fewer nodes. See [product quadrature](/product-quadrature/).
- **Radon's 7-point rule of degree 5 on the square.** The center with weight $\frac87$; $(0, \pm\sqrt{14/15})$ with weight $\frac{20}{63}$; $(\pm\sqrt{3/5}, \pm\sqrt{1/3})$ with weight $\frac59$. The weights sum to $4$, the area. It integrates $1, x^2, y^2, x^4, x^2y^2, y^4$ exactly and fails at degree 6, for example $E(y^6) = -\frac{128}{4725}$. The $3 \times 3$ product Gauss rule also has degree 5 but uses 9 nodes; Radon's rule meets Möller's bound of 7.
- **Edge-midpoint rule on a triangle.** On $T = \{x, y \ge 0,\ x + y \le 1\}$, area $\frac12$: nodes $(\frac12, 0)$, $(0, \frac12)$, $(\frac12, \frac12)$, weights $\frac16$. It is exact for $1, x, y, x^2, xy, y^2$ (for example $Q(xy) = \frac16\cdot\frac14 = \frac{1}{24} = I(xy)$) and fails at $x^3$: $I(x^3) = \frac{1}{20}$, $Q(x^3) = \frac{1}{24}$, $E = \frac{1}{120}$. So $d = 2$ with $n = 3 = \dim\mathcal{P}^2_1$, the lower bound: a Gaussian rule. By invariance it serves every triangle, as in finite element codes.
- **The centroid rule.** One node at the centroid with weight equal to the area has degree 1 on any convex region, and $n = 1$ is the lower bound for $d = 1$.
- **Sparse grids.** A [Smolyak sparse grid](/sparse-grid-quadrature/) built from nested one-dimensional rules is a cubature rule. Its degree in total-degree terms is modest, but it uses far fewer nodes than a full product in high dimension; its weights can be negative, so it is not positive.
- **Non-example: degree is not everything in high dimension.** A product of $k$-point rules in $s$ dimensions uses $k^s$ nodes; with $k = 5$ and $s = 10$ that is about $9.8$ million evaluations for degree 9. Degree-based rules are practical for small $s$; for large $s$, [Monte Carlo](/monte-carlo-integration/) and [quasi-Monte Carlo](/quasi-monte-carlo-integration/) methods are used instead.
- **Non-example: equal-weight point sets.** Monte Carlo and quasi-Monte Carlo rules $Q_n(f) = \frac{\operatorname{vol}\Omega}{n}\sum f(x_i)$ are cubature sums but generally have degree 0: they integrate constants exactly and $x_1$ only by accident. Their quality is measured by variance or by [discrepancy](/discrepancy/), not by degree.
- **Non-example: too few nodes.** No rule with 2 nodes has degree 2 on a region with interior in the plane: the lower bound is $\dim\mathcal{P}^2_1 = 3$. Indeed the line through the two nodes gives a $p \in \mathcal{P}^2_1$ with $Q(p^2) = 0 < I(p^2)$.

**Floating point.** For irrational nodes, such as Radon's, the computed rule has errors $E_n(x^\alpha)$ of the order of $u\sum_i\lvert w_i\rvert\,\lvert x_i^\alpha\rvert$ for $\lvert\alpha\rvert \le d$, with $u = 2^{-53}$; a numerical check of the degree must compare with this size, as in one dimension.

## Related definitions

- [Quadrature rule](/quadrature-rule/) and [degree of precision](/degree-of-precision/): the one-dimensional case, $s = 1$.
- [Multidimensional integration](/multidimensional-integration/): the problem that cubature rules solve, and the curse of dimensionality.
- [Product quadrature](/product-quadrature/): tensor products of one-dimensional rules, the simplest cubature rules.
- [Sparse grid quadrature](/sparse-grid-quadrature/): sums of small products that keep a total-degree exactness with fewer nodes.
- [Gaussian quadrature](/gaussian-quadrature/): the one-dimensional rules that attain the lower bound, which in several variables is rarely attainable.
- [Discrepancy](/discrepancy/) and [quasi-Monte Carlo integration](/quasi-monte-carlo-integration/): equal-weight rules judged by uniformity instead of degree.

## References
