---
tag: PVT0RQ
kind: definition
slug: monic-polynomial
name: Monic polynomial
aliases:
- normalized polynomial
area: algebra/polynomial-arithmetic
level: intro
summary: A polynomial whose leading coefficient is 1; used to normalise results of division and gcd.
prereqs: [polynomial]
see_also: [polynomial-degree, irreducible-polynomial, primitive-polynomial, polynomial-gcd, polynomial-long-division, minimal-polynomial-algebraic-element, characteristic-polynomial, rational-root-theorem]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 2.4, Division with remainder (division by a polynomial whose leading coefficient is a unit); Section 3.4, (Non-)Uniqueness of the gcd (the normal form, monic over a field); Section 25.3, Polynomials and fields
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6, Polynomial arithmetic (the definition of a monic polynomial), and Section 4.6.1, Division of polynomials
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition, Cambridge University Press, 2009
    locator: Section 7.2, Polynomial rings (leading coefficient, monic polynomials, division with remainder)
---

A monic polynomial is a nonzero [polynomial](/polynomial/) whose leading coefficient is $1$. Over a field, every nonzero polynomial is a nonzero constant times exactly one monic polynomial, so "monic" is the standard way to pick one representative among the polynomials that differ by a unit factor. The gcd, the minimal polynomial and the characteristic polynomial are monic by convention. Division with remainder by a monic polynomial needs no division of coefficients, so it works over every commutative ring.

## Definition

Let $R$ be a commutative ring with $1 \ne 0$. A polynomial $f = \sum_{i=0}^{n} f_i x^i \in R[x]$ with $f_n \ne 0$ has [degree](/polynomial-degree/) $n$ and leading coefficient $\operatorname{lc}(f) = f_n$. The polynomial $f$ is **monic** when $f \ne 0$ and $\operatorname{lc}(f) = 1$, that is

$$f = x^n + f_{n-1} x^{n-1} + \cdots + f_1 x + f_0 \qquad (n \ge 0,\ f_i \in R).$$

The zero polynomial is not monic, and the constant $1$ is the only monic polynomial of degree $0$.

**Monic associate.** Let $F$ be a field and $f \in F[x]$ nonzero. The polynomial $\operatorname{monic}(f) = \operatorname{lc}(f)^{-1} f$ is monic, and $f = \operatorname{lc}(f) \cdot \operatorname{monic}(f)$. It is the only monic polynomial of the form $c f$ with $c \in F$: if $c f$ is monic then $c \operatorname{lc}(f) = 1$, so $c = \operatorname{lc}(f)^{-1}$. Since the units of $F[x]$ are the nonzero constants, each class of associates of nonzero polynomials holds exactly one monic polynomial. Over a ring that is not a field, such as $\mathbb{Z}$, a polynomial like $2x + 1$ has no monic associate, and the normal form is instead the [primitive](/primitive-polynomial/) polynomial with positive leading coefficient.

**Basic properties.** For monic $f, g \in R[x]$:

1. **Products.** $fg$ is monic and $\deg(fg) = \deg f + \deg g$. The coefficient of $x^{\deg f + \deg g}$ in $fg$ is $\operatorname{lc}(f)\operatorname{lc}(g) = 1 \cdot 1 = 1$, and no higher power occurs. This holds over every ring, even one with zero divisors, because $1 \cdot 1 \ne 0$. For the same reason a monic polynomial is never a zero divisor in $R[x]$: if $h \ne 0$ then $\operatorname{lc}(f h) = \operatorname{lc}(h) \ne 0$.
2. **Division with remainder.** For each $a \in R[x]$ there are unique $q, r \in R[x]$ with $a = q f + r$ and $\deg r < \deg f$. The [long division](/polynomial-long-division/) loop subtracts $c\, x^{k} f$ with $c$ the current top coefficient of $a$; since $\operatorname{lc}(f) = 1$, the new top coefficient is $c - c \cdot 1 = 0$ and no inverse is needed. Uniqueness follows from item 1: if $q f + r = q' f + r'$ with $q \ne q'$, then $(q - q') f$ has degree at least $\deg f$, while $r' - r$ has degree less than $\deg f$.
3. **Counting.** Over a finite field $\mathbb{F}_q$ there are exactly $q^n$ monic polynomials of degree $n$, one for each choice of $f_0, \ldots, f_{n-1}$.

## Examples and non-examples

- $x^2 - 3x + 2 = (x - 1)(x - 2)$ is monic over $\mathbb{Z}$, and so are both factors, as item 1 requires.
- Division by the monic $x^2 + x + 1$ over $\mathbb{Z}$: $x^3 + 2x + 5 = (x - 1)(x^2 + x + 1) + (2x + 6)$. All coefficients stay integers.
- $2x + 1 \in \mathbb{Z}[x]$ is **not** monic, and dividing $x$ by it needs the fraction $1/2$: over $\mathbb{Q}$, $x = \tfrac{1}{2}(2x + 1) - \tfrac{1}{2}$. Its monic associate over $\mathbb{Q}$ is $x + \tfrac{1}{2}$.
- The polynomial $3x^2 + x$ over $\mathbb{Z}/3\mathbb{Z}$ equals $x$, because $3 = 0$ there. It is monic of degree $1$. A program that stores the coefficient list $[0, 1, 3]$ without reducing it and without removing the top zero would report the wrong degree and the wrong leading coefficient.
- The zero polynomial is not monic. The constant $5 \in \mathbb{Q}[x]$ is not monic, and its monic associate is $1$.
- Over $\mathbb{Z}/4\mathbb{Z}$, $x^2 + 2x$ is monic, while $2x^2 + x$ is not, and it has no monic associate because $2$ is not a unit. Its product with itself is $4x^4 + 4x^3 + x^2 = x^2$, so the degree of a product of non-monic polynomials can drop.
- Over $\mathbb{F}_2$ there are $2^2 = 4$ monic polynomials of degree 2: $x^2$, $x^2 + 1$, $x^2 + x$ and $x^2 + x + 1$.

## Related definitions

- [Polynomial](/polynomial/) and [degree](/polynomial-degree/): the leading coefficient is defined through the degree.
- [Primitive polynomial](/primitive-polynomial/): the normal form over $\mathbb{Z}$ and other unique factorization domains, where the content takes the place of the leading coefficient.
- [Irreducible polynomial](/irreducible-polynomial/): factorization over a field is written as $\operatorname{lc}(f)$ times a product of monic irreducible polynomials, and this form is unique.
- [Polynomial gcd](/polynomial-gcd/): over a field, "the" gcd means the monic one, and the [Euclidean algorithm](/polynomial-euclidean-algorithm/) returns it after a final division by the leading coefficient.
- [Minimal polynomial](/minimal-polynomial-algebraic-element/) and [characteristic polynomial](/characteristic-polynomial/): both are monic by definition.
- [Rational root theorem](/rational-root-theorem/): a rational root of a monic polynomial with integer coefficients is an integer.

## References
