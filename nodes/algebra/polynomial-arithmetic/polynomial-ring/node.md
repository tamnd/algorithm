---
tag: 0SMTJV
kind: definition
slug: polynomial-ring
name: Polynomial ring
aliases:
- ring of polynomials
- R[x]
area: algebra/polynomial-arithmetic
level: intro
summary: The ring R[x] of polynomials over a coefficient ring R, with coefficientwise addition and convolution multiplication.
prereqs: []
see_also: [polynomial, polynomial-degree, monic-polynomial, polynomial-multiplication, polynomial-division, euclidean-domain, irreducible-polynomial, dense-polynomial-representation]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 2.2, Representation and addition of polynomials (pp. 32 to 34), and Section 25.2, Rings
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6, Polynomial Arithmetic (the introduction, on polynomials over a commutative ring)
  - book: isbn:9780471433347
    title: David S. Dummit and Richard M. Foote, Abstract Algebra, third edition, Wiley, 2004
    locator: Section 7.2, Examples, polynomial rings; Section 9.1, Polynomial rings, definitions and basic properties
  - paper: doi:10.1007/BF01178683
    title: David G. Cantor and Erich Kaltofen, On fast multiplication of polynomials over arbitrary algebras, Acta Informatica 28(7), 1991
    locator: pp. 693 to 701 (the bound of O(n log n log log n) ring operations)
---

The polynomial ring $R[x]$ over a commutative ring $R$ is the set of finite formal sums $a_0 + a_1 x + \cdots + a_n x^n$ with $a_i \in R$, with addition coefficient by coefficient and multiplication by the [convolution](/convolution/) of the coefficient sequences. It is the home of every algorithm of this area: [multiplication](/polynomial-multiplication/), [division with remainder](/polynomial-division/), [gcd](/polynomial-gcd/) and factorization all compute in $R[x]$. Its properties depend on $R$: when $R$ is a field, $R[x]$ has division with remainder and is a [Euclidean domain](/euclidean-domain/); when $R$ has zero divisors, degrees can drop under multiplication.

## Definition

Let $R$ be a commutative ring with $1$.

**Polynomials.** A *polynomial* over $R$ in the indeterminate $x$ is a sequence $(a_0, a_1, a_2, \ldots)$ of elements of $R$ such that only finitely many $a_i$ are nonzero. We write it as

$$f = \sum_{i \ge 0} a_i x^i = a_0 + a_1 x + \cdots + a_n x^n,$$

where $n$ is any index with $a_i = 0$ for all $i > n$. The element $a_i$ is the *coefficient* of $x^i$ in $f$. Two polynomials are equal when all their coefficients are equal. The *zero polynomial* $0$ has all coefficients $0$.

**Operations.** For $f = \sum a_i x^i$ and $g = \sum b_j x^j$,

$$f + g = \sum_{k \ge 0} (a_k + b_k)\, x^k, \qquad f \cdot g = \sum_{k \ge 0} c_k x^k \quad\text{with}\quad c_k = \sum_{i + j = k} a_i b_j .$$

Each $c_k$ is a finite sum of $k + 1$ terms, and $c_k = 0$ when $k > \deg f + \deg g$, so $f \cdot g$ is again a polynomial. With these operations, $R[x]$ is a commutative ring. Its zero is the zero polynomial and its one is the constant $1$. The map $a \mapsto (a, 0, 0, \ldots)$ embeds $R$ in $R[x]$ as the *constant polynomials*, and $x$ is the sequence $(0, 1, 0, 0, \ldots)$. Associativity of the product follows from $\sum_{i + j + l = k} a_i b_j c_l$ being the coefficient of $x^k$ in both $(fg)h$ and $f(gh)$.

**Degree.** For $f \ne 0$, the *degree* $\deg f$ is the largest $i$ with $a_i \ne 0$, and $\operatorname{lc}(f) = a_{\deg f}$ is the *leading coefficient*. The zero polynomial has degree $-\infty$ by convention. See [degree of a polynomial](/polynomial-degree/).

**Evaluation.** For $r \in R$, the map $f \mapsto f(r) = \sum a_i r^i$ is a ring homomorphism $R[x] \to R$. More generally, for each ring homomorphism $\varphi : R \to S$ to a commutative ring $S$ and each $s \in S$, there is exactly one ring homomorphism $R[x] \to S$ that extends $\varphi$ and sends $x$ to $s$. This is the *universal property* of $R[x]$.

**Several variables.** $R[x_1, \ldots, x_m]$ is defined by induction as $R[x_1, \ldots, x_{m-1}][x_m]$. Its elements are finite sums of terms $a\, x_1^{e_1} \cdots x_m^{e_m}$.

**Conventions of this area.** On the pages of this area, $R$ is a commutative ring with $1$, and a page says when $R$ must be a field (written $F$) or an integral domain. A polynomial has degree $n$, so it has $n + 1$ coefficients. $M(n)$ is the number of operations in $R$ to multiply two polynomials of degree less than $n$: $M(n) = O(n^2)$ for the school method, $O(n^{\log_2 3})$ for [Karatsuba](/karatsuba-multiplication/), and $O(n \log n \log \log n)$ over any ring by the method of Cantor and Kaltofen. Costs count operations in $R$ (additions, subtractions, multiplications, and divisions by units or in a field), with each operation at unit cost, unless the page says that it counts word or bit operations.

### Basic facts

1. **Degree of a product.** For nonzero $f, g$, $\deg(fg) \le \deg f + \deg g$, and the coefficient of $x^{\deg f + \deg g}$ in $fg$ is $\operatorname{lc}(f)\operatorname{lc}(g)$. So equality holds exactly when $\operatorname{lc}(f)\operatorname{lc}(g) \ne 0$. *Proof.* In $c_k = \sum_{i+j=k} a_i b_j$ with $k > \deg f + \deg g$, each term has $i > \deg f$ or $j > \deg g$, so it is $0$. For $k = \deg f + \deg g$, the only term that can be nonzero is $a_{\deg f} b_{\deg g}$. $\square$
2. **Integral domains.** $R[x]$ is an integral domain if and only if $R$ is. *Proof.* If $R$ is a domain and $f, g \ne 0$, then $\operatorname{lc}(f)\operatorname{lc}(g) \ne 0$, so $fg \ne 0$ by fact 1. If $R$ has $ab = 0$ with $a, b \ne 0$, the constants $a$ and $b$ are zero divisors in $R[x]$. $\square$
3. **Units.** If $R$ is an integral domain, the units of $R[x]$ are the units of $R$. *Proof.* If $fg = 1$, then $\deg f + \deg g = 0$ by fact 1, so $f$ and $g$ are constants with product $1$. $\square$
4. **Division by a monic polynomial.** For $f, g \in R[x]$ with $\operatorname{lc}(g)$ a unit of $R$, there are unique $q, r$ with $f = qg + r$ and $\deg r < \deg g$. This is [polynomial division](/polynomial-division/).
5. **Fields.** If $F$ is a field, $F[x]$ is a [Euclidean domain](/euclidean-domain/) with the degree as Euclidean function. So it is a principal ideal domain and a unique factorization domain, and the [Euclidean algorithm](/polynomial-euclidean-algorithm/) computes gcds in it.
6. **Unique factorization over a UFD.** If $R$ is a unique factorization domain, so is $R[x]$. This is a consequence of [Gauss's lemma](/gauss-lemma/). For example $\mathbb{Z}[x]$ is a UFD.

## Examples and non-examples

- **A product in $\mathbb{Z}[x]$.** $(1 + 2x)(3 - x + x^2) = 3 + 5x - x^2 + 2x^3$. The coefficients are $c_0 = 1 \cdot 3$, $c_1 = 1 \cdot (-1) + 2 \cdot 3 = 5$, $c_2 = 1 \cdot 1 + 2 \cdot (-1) = -1$ and $c_3 = 2 \cdot 1 = 2$. The degree is $1 + 2 = 3$, as fact 1 says for a domain.
- **The degree drops over $\mathbb{Z}/6\mathbb{Z}$.** $(1 + 2x)(1 + 3x) = 1 + 5x + 6x^2 = 1 + 5x$, because $2 \cdot 3 = 0$ in $\mathbb{Z}/6\mathbb{Z}$. The product of two polynomials of degree $1$ has degree $1$.
- **A unit of degree 1.** Over $\mathbb{Z}/4\mathbb{Z}$, $(1 + 2x)^2 = 1 + 4x + 4x^2 = 1$. So $1 + 2x$ is a unit of $(\mathbb{Z}/4\mathbb{Z})[x]$, and fact 3 fails when $R$ is not a domain.
- **A polynomial is not a function.** Over $\mathbb{F}_3 = \mathbb{Z}/3\mathbb{Z}$, the polynomial $x^3 - x = 2x + x^3$ is not zero, but its value at each of $0, 1, 2$ is $0$, by [Fermat's little theorem](/fermat-little-theorem/). Two different polynomials can define the same function on a finite ring. Over an infinite integral domain this cannot happen, because a nonzero polynomial of degree $n$ has at most $n$ roots.
- **$\mathbb{Z}[x]$ is not a principal ideal domain.** The ideal $(2, x)$ of the polynomials with even constant term is not generated by one polynomial. A generator $d$ would divide $2$, so $d = \pm 1$ or $\pm 2$; $\pm 1 \notin (2, x)$ and $\pm 2$ does not divide $x$. So fact 5 needs a field.
- **Non-example: Laurent polynomials.** $x^{-1} + 1 + x$ is not in $R[x]$: exponents are nonnegative. The Laurent polynomials form the larger ring $R[x, x^{-1}]$.
- **Non-example: power series.** $1 + x + x^2 + \cdots$ has infinitely many nonzero coefficients, so it is not a polynomial. It lies in the ring $R[[x]]$ of formal power series, where it is the inverse of $1 - x$; see [power series inversion](/power-series-inversion/).

## Related definitions

- [Polynomial](/polynomial/): the abstract type that the representations implement.
- [Degree of a polynomial](/polynomial-degree/) and [monic polynomial](/monic-polynomial/): the leading term and its normalization.
- [Dense representation](/dense-polynomial-representation/) and [sparse representation](/sparse-polynomial-representation/): how a program stores an element of $R[x]$.
- [Polynomial multiplication](/polynomial-multiplication/) and [polynomial division](/polynomial-division/): the two basic operations and their costs.
- [Euclidean domain](/euclidean-domain/): the structure of $F[x]$ over a field.
- [Irreducible polynomial](/irreducible-polynomial/) and [primitive polynomial](/primitive-polynomial/): the building blocks of factorization in $F[x]$ and $\mathbb{Z}[x]$.
- [Point-value representation](/point-value-representation/): a polynomial of degree less than $n$ over a field is fixed by its values at $n$ distinct points.

## References
