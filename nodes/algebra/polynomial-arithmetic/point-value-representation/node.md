---
tag: T0CK84
kind: data-structure
slug: point-value-representation
name: Point-value representation
aliases:
- point-value form
- evaluation form
- value representation
area: algebra/polynomial-arithmetic
level: core
summary: Stores the values of the polynomial at n distinct points; multiplication becomes pointwise.
implements: [polynomial]
model: blum-shub-smale-machine
complexity:
  vars: {n: the number of points}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
prereqs: [polynomial, dense-polynomial-representation, factor-theorem, horner-rule]
see_also: [evaluation-interpolation-paradigm, fft-polynomial-multiplication, lagrange-interpolation, newton-interpolation, interpolating-polynomial-uniqueness, fast-interpolation, chinese-remainder-theorem, vandermonde-matrix]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 5.2, Evaluation and interpolation; Section 5.4, Chinese Remainder Algorithm (interpolation as Chinese remaindering modulo x - u_i); Section 10.2, Fast interpolation
  - book: isbn:9780262046305
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, fourth edition, MIT Press, 2022
    locator: Section 30.1, Representing polynomials (the point-value representation, uniqueness of interpolation, and pointwise addition and multiplication)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6.4, Evaluation of polynomials (interpolation, Newton's divided differences and Lagrange's formula)
  - paper: doi:10.1137/S0036144502417715
    title: Jean-Paul Berrut and Lloyd N. Trefethen, Barycentric Lagrange interpolation, SIAM Review 46(3) (2004), 501 to 517
    locator: the barycentric formula, the weights, and their O(n) evaluation
---

The point-value representation stores a [polynomial](/polynomial/) of degree less than $n$ as its values at $n$ fixed distinct points $u_0, \ldots, u_{n-1}$. Over a field, interpolation makes this a one-to-one correspondence, so the list of values is a complete description. Addition and multiplication act on each value separately and cost $n$ field operations, against $\Theta(n^2)$ for schoolbook multiplication in the [coefficient form](/dense-polynomial-representation/). The price is paid at the borders: converting from coefficients is multipoint evaluation and converting back is interpolation, and both take $\Theta(n \log n)$ at roots of unity by the [FFT](/fft-polynomial-multiplication/) and $O(M(n) \log n)$ at general points.

## In plain words

A straight line is fixed by two of its points, and a parabola by three. In the same way, a polynomial of degree less than n is fixed by its values at n different numbers. So instead of the coefficients, we can store the n values.

In this form, adding two polynomials means adding the values at each point, and multiplying means multiplying the values at each point. Each takes one step per point. But a product has a higher degree than its factors, so there must be enough points for the product. To get the coefficients back, or a value at a new number, we must rebuild the polynomial from its values. This step is called interpolation, and it costs more.

## The abstract type

The representation implements the [polynomial](/polynomial/) abstract type over a field $F$, restricted to polynomials of degree less than $n$, where $n$ is fixed in advance. It gives `add`, `sub`, scalar multiplication, `mul` when the degree of the product stays below $n$, a zero test, an equality test, evaluation at a new point, and conversion to and from coefficients. It does not give the degree or division with remainder directly; both need conversion to coefficients first.

Costs are counted in field operations in the algebraic complexity model, the [Blum-Shub-Smale machine](/blum-shub-smale-machine/) over $F$: each addition, subtraction, multiplication, division and zero test costs 1. Over a commutative ring $R$ that is not a field, the representation still works if every difference $u_i - u_j$ with $i \ne j$ is a unit of $R$. For $R = \mathbb{Z}/m\mathbb{Z}$ this means that the points are distinct modulo every prime factor of $m$.

## Representation

Fix $n \ge 1$ and distinct points $U = (u_0, \ldots, u_{n-1})$ in $F$. A value is a list $y = [y_0, \ldots, y_{n-1}]$ in $F^n$. It stands for the unique polynomial $\operatorname{val}(y) \in F[x]$ with $\deg \operatorname{val}(y) < n$ and $\operatorname{val}(y)(u_i) = y_i$ for each $i$. By Lagrange's formula,

$$\operatorname{val}(y) = \sum_{i=0}^{n-1} y_i \prod_{j \ne i} \frac{x - u_j}{u_i - u_j}.$$

**Why this is a representation.** The map $\operatorname{ev}_U : f \mapsto (f(u_0), \ldots, f(u_{n-1}))$ from the polynomials of degree less than $n$ to $F^n$ is a bijection. It is onto because Lagrange's formula gives a preimage of each $y$, and it is one-to-one because a nonzero polynomial of degree less than $n$ has fewer than $n$ roots, by the [factor theorem](/factor-theorem/). In matrix terms, $\operatorname{ev}_U$ is multiplication by the [Vandermonde matrix](/vandermonde-matrix/) $V = (u_i^j)$, and $\det V = \prod_{i<j} (u_j - u_i) \ne 0$. There is no normalization invariant: every list in $F^n$ is valid, and two values are equal exactly when the lists are equal.

**Barycentric weights.** For evaluation at new points we store, once per point set, the weights $w_i = 1 / \prod_{j \ne i} (u_i - u_j)$. They depend only on $U$, not on the polynomial.

**The ring structure.** The map $\operatorname{ev}_U : F[x] \to F^n$ is a ring homomorphism with kernel generated by $m(x) = \prod_i (x - u_i)$. So $F^n$ is isomorphic to $F[x]/(m)$, by the [Chinese remainder theorem](/chinese-remainder-theorem/) for the coprime moduli $x - u_i$. Pointwise multiplication is therefore multiplication modulo $m$. It equals ordinary multiplication exactly when the product has degree less than $n$.

## Operations

```pseudo id=main
WEIGHTS(U)                             ▷ once per point set; U = (u_0, ..., u_{n−1}) distinct
L1  for i ← 0 to n − 1 do
L2      p ← Π_{j ≠ i} (u_i − u_j)
L3      w[i] ← p⁻¹

ADD(y, z)
L4  return [y[i] + z[i] for i ← 0 to n − 1]

MUL(y, z)                              ▷ represents the product only if deg f + deg g < n
L5  return [y[i] · z[i] for i ← 0 to n − 1]

EVALUATE-AT(y, t)                      ▷ barycentric formula, needs the weights w
L6  if t = u_k for some k then return y[k]
L7  ℓ ← Π_{j} (t − u_j)
L8  return ℓ · Σ_i w[i] · y[i] / (t − u_i)

TO-COEFFICIENTS(y)                     ▷ Newton's divided differences
L9  d ← a copy of y
L10 for k ← 1 to n − 1 do for i ← n − 1 down to k do d[i] ← (d[i] − d[i − 1]) / (u_i − u_{i−k})
L11 c ← [d[n − 1]]
L12 for i ← n − 2 down to 0 do c ← c · (x − u_i) + d[i]
L13 return c with its zero top entries removed
```

Subtraction and scalar multiplication are pointwise like ADD. The zero test is "all $y_i = 0$". Conversion from the coefficient list $a$ is $y_i = a(u_i)$ for each $i$, by [Horner's rule](/horner-rule/). To change to a larger point set, which a product of high degree needs, convert to coefficients and evaluate at the new points (`extend` in the code).

Line L10 computes the divided differences: after round $k$, $d[i]$ is the leading coefficient of the polynomial of degree at most $k$ that interpolates the values at $u_{i-k}, \ldots, u_i$. At the end, $d[k]$ is the coefficient of the Newton form

$$f = d_0 + d_1 (x - u_0) + d_2 (x - u_0)(x - u_1) + \cdots + d_{n-1} (x - u_0) \cdots (x - u_{n-2}),$$

and line L12 expands it from the inside out, as in Horner's rule. Line L8 is the barycentric form of Lagrange's formula, $f(t) = \ell(t) \sum_i \frac{w_i y_i}{t - u_i}$ with $\ell(t) = \prod_j (t - u_j)$, which follows by factoring $\ell(t)$ out of each Lagrange basis polynomial.

## Example

Over $\mathbb{Q}$, take $n = 3$ points $U = (0, 1, 2)$, $f = 1 + 2x$ and $g = 3 - x$. Then $\deg f + \deg g = 2 < 3$, so three points suffice for the product.

| point $u_i$ | $f(u_i)$ | $g(u_i)$ | MUL: $y_i z_i$ |
|---|---|---|---|
| 0 | 1 | 3 | 3 |
| 1 | 3 | 2 | 6 |
| 2 | 5 | 1 | 5 |

**Back to coefficients.** TO-COEFFICIENTS$([3, 6, 5])$: line L9 sets $d = [3, 6, 5]$. Round $k = 1$ sets $d_2 = (5 - 6)/(2 - 1) = -1$ and $d_1 = (6 - 3)/(1 - 0) = 3$, so $d = [3, 3, -1]$. Round $k = 2$ sets $d_2 = (-1 - 3)/(2 - 0) = -2$, so $d = [3, 3, -2]$. The Newton form is $3 + 3x - 2x(x - 1)$. Lines L11 and L12 expand it: $c = -2$, then $c = -2(x - 1) + 3 = -2x + 5$, then $c = (-2x + 5)(x - 0) + 3 = -2x^2 + 5x + 3$. Indeed $(1 + 2x)(3 - x) = 3 + 5x - 2x^2$.

**At a new point.** The weights are $w_0 = 1/((0-1)(0-2)) = \tfrac12$, $w_1 = 1/((1-0)(1-2)) = -1$ and $w_2 = 1/((2-0)(2-1)) = \tfrac12$. At $t = 3$, $\ell(3) = 3 \cdot 2 \cdot 1 = 6$ and $\sum_i w_i y_i/(3 - u_i) = \tfrac{3/2}{3} - \tfrac{6}{2} + \tfrac{5/2}{1} = \tfrac12 - 3 + \tfrac52 = 0$. So the product is $0$ at $3$, which agrees with $g(3) = 0$.

**Too few points.** With $U = (0, 1)$, the polynomial $x$ has the values $[0, 1]$, and MUL gives $[0, 1]$ again, which is the representation of $x$, not of $x^2$. The pointwise product is $x^2 \bmod x(x - 1) = x$.

## Correctness

Each operation returns the representation of the right polynomial, under the stated degree condition for MUL. ADD and MUL are correct because evaluation at $u_i$ is a ring homomorphism, and the result has degree less than $n$ (for MUL by the hypothesis), so it is the unique interpolant of the new values. EVALUATE-AT is the barycentric form of Lagrange's formula. TO-COEFFICIENTS is correct by the recurrence of divided differences, which comes from the uniqueness of interpolation. The proofs are in the proof file.

## Complexity

All costs are field operations in the algebraic complexity model, for $n$ points. The front matter states the cost of ADD and MUL. The bounds in the table are proved; the crossovers between the methods in the last rows are observed in practice and depend on the field and the machine.

| operation | field operations | notes |
|---|---|---|
| `add`, `sub`, scalar multiple | $n$ | pointwise |
| `mul` | $n$ | needs $\deg f + \deg g < n$ |
| zero test, equality | $n$ | no normalization needed |
| weights for a point set | $O(n^2)$, or $O(M(n) \log n)$ | once per point set; $O(n)$ at roots of unity, where $w_i = u_i / n$ |
| evaluate at a new point | $O(n)$ with the weights | about $5n$ operations, $n$ of them divisions |
| from coefficients | $O(n^2)$ by Horner; $O(M(n) \log n)$ by [fast multipoint evaluation](/fast-multipoint-evaluation/); $O(n \log n)$ at roots of unity by the FFT | |
| to coefficients | $O(n^2)$ by divided differences; $O(M(n) \log n)$ by [fast interpolation](/fast-interpolation/); $O(n \log n)$ at roots of unity by the inverse FFT | |
| space | $n$ values, plus $n$ weights per point set | |

TO-COEFFICIENTS runs the inner step of line L10 $\sum_{k=1}^{n-1} (n - k) = n(n-1)/2$ times, with one subtraction, one subtraction of points and one division each, and line L12 costs $O(i)$ for the $i$-th step, so $O(n^2)$ in total. The point differences $u_i - u_{i-k}$ do not depend on the values, so they can be inverted once per point set.

## Variants

- **Roots of unity.** If $F$ contains a primitive $n$-th [root of unity](/roots-of-unity/) $\omega$, choose $u_i = \omega^i$. Conversion in both directions is the [discrete Fourier transform](/fast-fourier-transform/) and its inverse, in $O(n \log n)$. Over $\mathbb{Z}/p\mathbb{Z}$ with $p = 998244353 = 119 \cdot 2^{23} + 1$ this is the [number-theoretic transform](/number-theoretic-transform/). This is the representation inside [FFT multiplication](/fft-polynomial-multiplication/).
- **Integer points.** $u_i = i$, as in [Toom-Cook multiplication](/toom-cook-multiplication/), which also uses the point at infinity (the leading coefficient). The weights are $w_i = (-1)^{n-1-i} / (i!\,(n-1-i)!)$, so the field must have characteristic $0$ or at least $n$.
- **Chebyshev points.** Over $\mathbb{R}$, values at Chebyshev points with the barycentric formula are numerically stable for very high degree, and this is the representation of the Chebfun system (Berrut and Trefethen).
- **Residues modulo general moduli.** Replace $x - u_i$ by pairwise coprime polynomials $m_i$ and store $f \bmod m_i$. This is the Chinese remainder representation, and the point-value form is its case of linear moduli (von zur Gathen and Gerhard, Section 5.4).
- **Values of integer polynomials modulo primes.** For $f \in \mathbb{Z}[x]$, store $f \bmod p_j$ for several primes. This is the same idea applied to the coefficients instead of the variable, and it is the base of [modular methods](/modular-methods/).
- **Multivariate grids.** For polynomials in $k$ variables with $\deg_{x_i} < d_i$, store the values on a grid $U_1 \times \cdots \times U_k$ with $|U_i| = d_i$.

## When to use it

Use the point-value form inside an algorithm that does several multiplications or additions in a row and then converts back once, as in the [evaluation-interpolation paradigm](/evaluation-interpolation-paradigm/): a product of many polynomials, a determinant of a polynomial matrix, or a resultant. Choose the number of points from a bound on the degree of the final result. Use the coefficient form when the degree changes in ways that are hard to bound, when division with remainder is needed, or when the polynomial is sparse.

## Pitfalls

- **Too few points.** MUL is correct only when $\deg f + \deg g < n$. Otherwise the result is the product modulo $\prod (x - u_i)$, and no error is reported. Plan the number of points for the final degree, or extend the point set before each product.
- **Repeated points.** If $u_i = u_j$ for $i \ne j$, the weights and the divided differences divide by zero. Over $\mathbb{Z}/p\mathbb{Z}$ there are only $p$ distinct points, so polynomials of degree $p$ or more cannot be stored this way over $\mathbb{F}_p$; use an extension field or the coefficient form.
- **The degree is hidden.** The list $[4, 4, 4, 4]$ is the constant $4$, and $[0, 0, 0, 0]$ is zero, but in general the degree is known only after interpolation. Code that needs the leading coefficient must convert first.
- **Different point sets.** Two lists can be added or multiplied only if they use the same points in the same order. Keep the point set with the values, or fix it globally.
- **Numerical instability.** Over $\mathbb{R}$ with equally spaced points, the Vandermonde matrix is very badly conditioned, and the Newton and monomial coefficients lose many digits for degree above about 20. Use Chebyshev points and the barycentric formula, or roots of unity.
- **Mistaking the field one for the integer one.** In generic code, a product over an empty set or a starting value of `1` can be a machine integer, and `1 / p` then gives a floating point number. The implementation below builds the field's one from the points.

## Implementations

## History

Lagrange's interpolation formula appeared in 1795, and Waring had published it in 1779. Newton's divided differences are older, from his work on finite differences in the late 17th century. The view of polynomial arithmetic as arithmetic on values, with conversion by the FFT, became central to computer algebra after the fast Fourier transform of Cooley and Tukey (1965) and its use for fast polynomial multiplication. Textbooks such as Cormen, Leiserson, Rivest and Stein present the point-value form as the second of the two standard representations of a polynomial. The barycentric formula was popularized for numerical work by Berrut and Trefethen in 2004.

## References
