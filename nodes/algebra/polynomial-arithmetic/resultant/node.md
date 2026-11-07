---
tag: X1SNNP
kind: definition
slug: resultant
name: Resultant
aliases:
- Sylvester resultant
- resultant of polynomials
- eliminant
area: algebra/polynomial-arithmetic
level: advanced
summary: Determinant of the Sylvester matrix; zero exactly when two polynomials share a common root.
prereqs: [polynomial-gcd, determinant]
see_also: [sylvester-matrix, subresultant, discriminant, subresultant-gcd, polynomial-extended-euclidean-algorithm, hadamard-bound, cylindrical-algebraic-decomposition, vieta-formulas]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 6.3, The resultant (p. 152; the Sylvester matrix, the gcd criterion, and the resultant as a combination s f + t g)
  - book: isbn:9780387556406
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138, Springer, 1993
    locator: Section 3.3.2, Resultants and Discriminants
  - book: isbn:9780387953854
    title: Serge Lang, Algebra, revised third edition, Graduate Texts in Mathematics 211, Springer, 2002
    locator: Chapter IV, Section 8, The resultant (the determinant and the product over the roots)
  - paper: doi:10.1080/14786444008649995
    title: J. J. Sylvester, A method of determining by mere inspection the derivatives from two equations of any degree, Philosophical Magazine 16, 1840
    locator: pp. 132 to 135
---

The resultant of two polynomials is one element of the coefficient ring, the determinant of their [Sylvester matrix](/sylvester-matrix/), that is zero exactly when the two polynomials have a common factor of positive degree. Over an algebraically closed field this means a common root. It is a polynomial in the coefficients, so it eliminates the variable: for polynomials in $x$ and $y$, the resultant with respect to $x$ is a polynomial in $y$ whose roots include the $y$-coordinates of the common zeros. It can be computed by the Euclidean algorithm without finding any root, and it is the starting point of [subresultants](/subresultant/), [discriminants](/discriminant/) and elimination theory.

## Definition

Let $R$ be a commutative ring, and let

$$f = \sum_{i=0}^{m} a_i x^i, \qquad g = \sum_{j=0}^{n} b_j x^j \in R[x]$$

with $m, n \ge 0$ and $m + n \ge 1$. The integers $m$ and $n$ are the *formal degrees*; usually $a_m \ne 0$ and $b_n \ne 0$, so they are the degrees.

**Sylvester matrix.** $\operatorname{Syl}(f, g)$ is the $(m + n) \times (m + n)$ matrix whose first $n$ rows hold the coefficients $a_m, a_{m-1}, \ldots, a_0$ of $f$, shifted one column to the right in each row, and whose last $m$ rows hold $b_n, \ldots, b_0$, shifted the same way. Row $i$ of the first block, for $i = 0, \ldots, n - 1$, lists the coefficients of $x^{n - 1 - i} f$ from $x^{m + n - 1}$ down to $x^0$, and row $j$ of the second block lists those of $x^{m - 1 - j} g$.

**Resultant.** $\operatorname{Res}(f, g) = \operatorname{Res}_{m, n}(f, g) = \det \operatorname{Syl}(f, g) \in R$.

For $f = x^2 - 3x + 2$ and $g = x^2 + 1$, with $m = n = 2$:

$$\operatorname{Syl}(f, g) = \begin{pmatrix} 1 & -3 & 2 & 0 \\ 0 & 1 & -3 & 2 \\ 1 & 0 & 1 & 0 \\ 0 & 1 & 0 & 1 \end{pmatrix}, \qquad \operatorname{Res}(f, g) = 10.$$

**Basic properties.** Let $a_m \ne 0$ and $b_n \ne 0$.

1. **Root formula.** If $f = a_m \prod_{i=1}^{m} (x - \alpha_i)$ and $g = b_n \prod_{j=1}^{n} (x - \beta_j)$ over a field that contains the roots, then
$$\operatorname{Res}(f, g) = a_m^{n} b_n^{m} \prod_{i, j} (\alpha_i - \beta_j) = a_m^{n} \prod_{i} g(\alpha_i) = (-1)^{mn}\, b_n^{m} \prod_{j} f(\beta_j).$$
The three forms agree, because $g(\alpha_i) = b_n \prod_j (\alpha_i - \beta_j)$ and $f(\beta_j) = a_m \prod_i (\beta_j - \alpha_i)$. That the determinant equals the first form is proved with generic roots in Lang, Chapter IV, Section 8, and stated in Cohen, Section 3.3.2.
2. **Common factors.** If $R = F$ is a field, $\operatorname{Res}(f, g) = 0$ exactly when $\deg \gcd(f, g) \ge 1$. *Proof.* Let $P_k$ be the space of polynomials of degree less than $k$. The linear map $\varphi(s, t) = s f + t g$ from $P_n \times P_m$ to $P_{m+n}$ has the matrix $\operatorname{Syl}(f, g)$, up to transposition, in the bases of monomials. If $h = \gcd(f, g)$ has degree $\ge 1$, then $s = g/h$ and $t = -f/h$ give $\varphi(s, t) = 0$ with $s \ne 0$, so $\varphi$ is singular and the determinant is $0$. Conversely, if $\varphi(s, t) = 0$ with $(s, t) \ne (0, 0)$, then $s f = -t g$, so $f \mid t g$ with $\deg t < m = \deg f$. If $\gcd(f, g) = 1$, then $f \mid t$, so $t = 0$, then $s f = 0$ and $s = 0$, a contradiction. $\square$ Over an integral domain $R$, apply this in the fraction field.
3. **A combination of $f$ and $g$.** There are $s, t \in R[x]$ with $\deg s < n$, $\deg t < m$ and $s f + t g = \operatorname{Res}(f, g)$. *Proof.* In $\operatorname{Syl}(f, g)$, add $x^{m + n - 1 - k}$ times column $k$ to the last column, for each $k < m + n - 1$. The determinant does not change, and the last column now holds the polynomials $x^{n - 1 - i} f$ and $x^{m - 1 - j} g$. Expand along this column: the result is $s f + t g$, with $s$ and $t$ sums of cofactors times powers of $x$, of the stated degrees. $\square$ For the example above, $(3x + 1) f + (8 - 3x) g = 10$.
4. **Symmetry and products.** $\operatorname{Res}(g, f) = (-1)^{mn} \operatorname{Res}(f, g)$, since moving the $m$ rows of $g$ above the $n$ rows of $f$ takes $mn$ row swaps. $\operatorname{Res}(f, g h) = \operatorname{Res}(f, g) \operatorname{Res}(f, h)$, by the form $a_m^{n} \prod_i g(\alpha_i)$ of the root formula.
5. **Euclidean reduction.** If $R = F$ is a field, $n \ge 1$ and $r = f \operatorname{rem} g \ne 0$, then $\operatorname{Res}(f, g) = (-1)^{mn}\, b_n^{\,m - \deg r} \operatorname{Res}(g, r)$. *Proof.* By the root formula, $\operatorname{Res}(g, f) = b_n^{m} \prod_j f(\beta_j)$, and $f(\beta_j) = r(\beta_j)$ since $g(\beta_j) = 0$. So $\operatorname{Res}(g, f) = b_n^{m - \deg r} \cdot b_n^{\deg r} \prod_j r(\beta_j) = b_n^{m - \deg r} \operatorname{Res}(g, r)$, and property 4 gives the sign. $\square$ If $r = 0$, then $g \mid f$ and $\operatorname{Res}(f, g) = 0$ for $n \ge 1$. Together with $\operatorname{Res}(f, b_0) = b_0^{m}$ for a constant $g = b_0$, this computes the resultant by the [Euclidean algorithm](/polynomial-euclidean-algorithm/).
6. **Size over $\mathbb{Z}$.** If $f, g \in \mathbb{Z}[x]$, then $|\operatorname{Res}(f, g)| \le \|f\|_2^{\,n}\, \|g\|_2^{\,m}$, where $\|f\|_2$ is the Euclidean norm of the coefficient vector. This is the [Hadamard bound](/hadamard-bound/) applied to the rows of $\operatorname{Syl}(f, g)$: each of the $n$ rows of the first block has norm $\|f\|_2$, and each of the $m$ others has norm $\|g\|_2$.

**Computing.** Over a field, property 5 gives $\operatorname{Res}(f, g)$ in $O(mn + m)$ operations by the Euclidean algorithm, and the fast Euclidean algorithm gives $O(M(N) \log N)$ operations when $m, n \le N$ (von zur Gathen and Gerhard, Chapter 11). Over $\mathbb{Z}$, compute it modulo several primes and combine by the [Chinese remainder theorem](/chinese-remainder-theorem/), with property 6 to choose how many primes, or use the [subresultant algorithm](/subresultant-gcd/), which works over any integral domain without fractions.

## Examples and non-examples

All values below were checked with a script that computes the Sylvester determinant with exact fractions.

- **A linear factor.** $\operatorname{Res}(x - a, g) = g(a)$, by the root formula with $m = 1$ and $a_1 = 1$. For $g = x^3 - 2x^2 + 3$ and $a = 5$ this is $78$.
- **No common root.** For $f = (x - 1)(x - 2)$ and $g = x^2 + 1$, $\operatorname{Res}(f, g) = g(1)\, g(2) = 2 \cdot 5 = 10$, as the matrix above gives.
- **A common root.** For $f = (x - 1)(x - 2)$ and $g = x^2 - 1 = (x - 1)(x + 1)$, $\operatorname{Res}(f, g) = 0$, and $\gcd(f, g) = x - 1$.
- **A quadratic and its derivative.** For $f = a x^2 + b x + c$ with $a \ne 0$, $\operatorname{Res}(f, f') = a\, f'(\alpha_1) f'(\alpha_2) = -a\,(b^2 - 4ac)$, since $f'(\alpha_{1,2}) = 2a\alpha_{1,2} + b = \pm \sqrt{b^2 - 4ac}$. So the [discriminant](/discriminant/) $b^2 - 4ac$ is a resultant up to the factor $-a$. For $3x^2 + 5x + 2$ the resultant is $-3$.
- **Elimination.** For $f = x^2 + y^2 - 1$ and $g = x - y$, as polynomials in $x$ over $R = \mathbb{Q}[y]$, $\operatorname{Res}_x(f, g) = (-1)^{2 \cdot 1} \cdot 1^{2} \cdot f(y) = 2y^2 - 1$. Its roots $y = \pm 1/\sqrt{2}$ are the $y$-coordinates of the two points where the line meets the circle.
- **Over $\mathbb{Z}$, a nonzero resultant need not be a unit.** $\operatorname{Res}(x^2 + 1, x^3 - x - 1) = 5$. Over $\mathbb{Q}$ the two polynomials are coprime, but over $\mathbb{F}_5$ they have the common root $2$: $2^2 + 1 = 5$ and $8 - 2 - 1 = 5$. In general, if a prime $p$ divides neither $a_m$ nor $b_n$, then $\operatorname{Res}(f, g) \bmod p$ is the resultant of $f \bmod p$ and $g \bmod p$, since the determinant commutes with reduction. So by property 2, $p$ divides $\operatorname{Res}(f, g)$ exactly when $f$ and $g$ have a common factor modulo $p$.
- **Non-example: vanishing leading coefficients.** With formal degrees, if $a_m = b_n = 0$, the first column of $\operatorname{Syl}(f, g)$ is zero and $\operatorname{Res}_{m, n}(f, g) = 0$, whether or not $f$ and $g$ have a common factor. When the coefficients are specialized, for example $y \mapsto y_0$ in an elimination, property 2 holds only at the points where $a_m$ or $b_n$ stays nonzero.

## Related definitions

- **Sylvester matrix.** The matrix of the map $(s, t) \mapsto s f + t g$; see [Sylvester matrix](/sylvester-matrix/).
- **Subresultants.** Determinants of submatrices of $\operatorname{Syl}(f, g)$ obtained by deleting rows and columns. For $k < n$, the $k$-th principal subresultant coefficient is nonzero exactly when $k$ is the degree of a remainder in the Euclidean algorithm (von zur Gathen and Gerhard, Section 11.2), and the $0$-th is the resultant. See [subresultant](/subresultant/) and the [subresultant gcd algorithm](/subresultant-gcd/).
- **Discriminant.** $\operatorname{disc}(f) = (-1)^{m(m-1)/2} a_m^{-1} \operatorname{Res}(f, f')$, which is zero exactly when $f$ has a repeated root; see [discriminant](/discriminant/).
- **Bézout coefficients.** Property 3 is a scaled form of the identity $s f + t g = \gcd(f, g)$ of the [extended Euclidean algorithm](/polynomial-extended-euclidean-algorithm/). When $\gcd(f, g) = 1$ over a field, the $s$ and $t$ of property 3 are $\operatorname{Res}(f, g)$ times the unique Bézout coefficients of degrees less than $n$ and $m$.
- **Elimination and geometry.** Resultants project the common zeros of polynomials in several variables to fewer variables. This is a step of [cylindrical algebraic decomposition](/cylindrical-algebraic-decomposition/) and of methods for solving polynomial systems.
- **Symmetric functions.** The root formula expresses the resultant through the roots, and [Vieta's formulas](/vieta-formulas/) express the symmetric functions of the roots through the coefficients, which explains why the resultant is a polynomial in the coefficients.

## References
