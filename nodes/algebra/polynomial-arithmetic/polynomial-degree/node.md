---
tag: TREG4V
kind: concept
slug: polynomial-degree
name: Degree of a polynomial
aliases:
- degree
- leading coefficient
- leading term
area: algebra/polynomial-arithmetic
level: intro
summary: Highest power with nonzero coefficient; it bounds the work and the number of roots.
prereqs: [polynomial-ring]
see_also: [polynomial-ring, monic-polynomial, polynomial-division, polynomial-euclidean-algorithm, factor-theorem, dense-polynomial-representation, polynomial-composition, vieta-formulas]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 2.2, Representation and addition of polynomials (degree and leading coefficient), and Section 9.1, Division with remainder using Newton iteration (the reversal of a polynomial)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6, Polynomial Arithmetic (the definitions of degree, leading coefficient and monic)
  - book: isbn:9780471433347
    title: David S. Dummit and Richard M. Foote, Abstract Algebra, third edition, Wiley, 2004
    locator: Section 9.1, Polynomial rings, definitions and basic properties (the degree of a product over an integral domain)
---

The degree of a nonzero polynomial $f = a_0 + a_1 x + \cdots + a_n x^n$ over a commutative ring $R$ is the largest index $n$ with $a_n \ne 0$, and its leading coefficient is $a_n$. The degree is the size measure of [polynomial arithmetic](/polynomial-ring/): a polynomial of degree $n$ has $n + 1$ coefficients, the costs of all algorithms are stated in it, and [division with remainder](/polynomial-division/) and the [Euclidean algorithm](/polynomial-euclidean-algorithm/) terminate because the degree drops. Over an integral domain it also bounds the number of roots.

## In plain words

A polynomial is a list of numbers, one for each power of the unknown. The degree is the highest power whose number is not zero, and that number is the leading coefficient. It tells you how long the list really is, once you remove the zeros at the top end.

Most work on polynomials is measured by the degree. Adding two polynomials takes work in proportion to the degree, and the school method of multiplying takes work in proportion to its square. When you divide one polynomial by another, each step removes the top term, so the degree goes down until the remainder is smaller than the divisor. The degree also limits how many times the graph of the polynomial can cross zero.

## The idea

Let $f = \sum_{i \ge 0} a_i x^i \in R[x]$.

**Definitions.**

- For $f \ne 0$, $\deg f = \max\{\, i : a_i \ne 0 \,\}$, the *leading coefficient* is $\operatorname{lc}(f) = a_{\deg f}$, and the *leading term* is $a_{\deg f} x^{\deg f}$. A polynomial with $\operatorname{lc}(f) = 1$ is [monic](/monic-polynomial/).
- For $f = 0$, there is no nonzero coefficient. We set $\deg 0 = -\infty$, with $-\infty < n$ and $-\infty + n = -\infty$ for each integer $n$. Some texts and programs use $-1$ instead. The value $-\infty$ makes rules 2 and 3 below true with no exception; the value $-1$ does not (for example $\deg(0 \cdot x) = -1 \ne -1 + 1$).
- A *constant* is a polynomial of degree at most $0$. A polynomial of degree $1$, $2$, $3$ is *linear*, *quadratic*, *cubic*.
- In a program, a [dense representation](/dense-polynomial-representation/) stores $a_0, \ldots, a_n$. It is *normalized* when the last stored coefficient is nonzero, and then $\deg f$ is the length minus $1$. A result of a subtraction or of arithmetic modulo $m$ can have zero top coefficients, so a program must strip them before it reads the degree.

**Rules.** Let $f, g$ be nonzero.

1. **Sum.** $\deg(f + g) \le \max(\deg f, \deg g)$, with equality when $\deg f \ne \deg g$. The top coefficients can cancel when the degrees are equal. *Proof.* Each coefficient of $f + g$ above $\max(\deg f, \deg g)$ is $0 + 0$. If $\deg f > \deg g$, the coefficient of $x^{\deg f}$ in $f + g$ is $\operatorname{lc}(f) + 0 \ne 0$. $\square$
2. **Product.** $\deg(fg) \le \deg f + \deg g$, and the coefficient of $x^{\deg f + \deg g}$ in $fg$ is $\operatorname{lc}(f)\operatorname{lc}(g)$. So $\deg(fg) = \deg f + \deg g$ when $R$ is an integral domain, or when one of the two leading coefficients is a unit. The proof is fact 1 of [polynomial ring](/polynomial-ring/).
3. **Quotient and remainder.** If $f = qg + r$ with $\deg r < \deg g$ and $\operatorname{lc}(g)$ a unit, then $\deg q = \deg f - \deg g$ when $\deg f \ge \deg g$, and $q = 0$ otherwise. *Proof.* $\deg(qg) = \deg q + \deg g$ by rule 2, since $\operatorname{lc}(g)$ is a unit. If $q \ne 0$, then $\deg(qg) \ge \deg g > \deg r$, so $\deg f = \deg(qg + r) = \deg q + \deg g$ by rule 1. If $q = 0$, then $\deg f = \deg r < \deg g$. $\square$
4. **Composition.** If $R$ is an integral domain and $\deg g \ge 1$, then $\deg f(g) = \deg f \cdot \deg g$. *Proof.* Write $n = \deg f$. By rule 2, $\deg(a_i g^i) = i \deg g$ for each $a_i \ne 0$, and these are distinct for distinct $i$. The term $i = n$ has the largest degree $n \deg g$, so by rule 1 it is the degree of the sum. $\square$
5. **Derivative.** The formal derivative $f' = \sum_{i \ge 1} i a_i x^{i-1}$ has $\deg f' \le \deg f - 1$, with equality when $(\deg f) \cdot \operatorname{lc}(f) \ne 0$ in $R$. Over a field of characteristic $p$ the degree can drop further, and $f'$ can be $0$ for a polynomial that is not constant.
6. **Roots.** If $R$ is an integral domain and $f \ne 0$, then $f$ has at most $\deg f$ roots in $R$. *Proof.* By induction on $\deg f$. A constant $f \ne 0$ has no root. If $f(a) = 0$, then the [factor theorem](/factor-theorem/) gives $f = (x - a)h$ with $\deg h = \deg f - 1$ by rule 3. For a root $b \ne a$, $0 = (b - a) h(b)$ and $b - a \ne 0$, so $h(b) = 0$ because $R$ has no zero divisors. So the roots of $f$ other than $a$ are roots of $h$, and there are at most $\deg f - 1$ of them. $\square$

**Reversal.** For $n \ge \deg f$, the reversal $\operatorname{rev}_n(f) = x^n f(1/x) = \sum_{i=0}^{n} a_{n-i} x^i$ reads the coefficients backwards. It turns the leading coefficient into the constant term, so it turns a question about the top of $f$ into a question about the bottom. This is the base of [fast division](/fast-polynomial-division/) by [power series inversion](/power-series-inversion/).

**Degree as a size.** The input of an algorithm on polynomials of degree at most $n$ has $n + 1$ coefficients, so $n$ plays the role of the input size. Over $\mathbb{Z}$ or $\mathbb{Q}$ the coefficients also grow, and a bit cost needs both the degree and a bound on the size of the coefficients.

**Several variables.** In $R[x_1, \ldots, x_m]$, the *total degree* of a term $a\, x_1^{e_1} \cdots x_m^{e_m}$ is $e_1 + \cdots + e_m$, and the total degree of a polynomial is the largest total degree of its terms. The degree in one variable $x_i$ treats the other variables as coefficients.

## Examples

- $f = 7 - 2x + 3x^4$ has $\deg f = 4$, $\operatorname{lc}(f) = 3$ and leading term $3x^4$. It is not monic.
- **Cancellation in a sum.** $(x + x^2) + (1 - x^2) = 1 + x$. Both summands have degree $2$, and the sum has degree $1$.
- **A product over a ring with zero divisors.** In $(\mathbb{Z}/6\mathbb{Z})[x]$, $(1 + 2x)(1 + 3x) = 1 + 5x$, of degree $1$, not $2$, because $2 \cdot 3 = 0$.
- **Composition.** $f = x^2 + 1$ and $g = x^3 - x$ give $f(g) = x^6 - 2x^4 + x^2 + 1$, of degree $2 \cdot 3 = 6$.
- **Derivative in characteristic 3.** Over $\mathbb{F}_3$, $(x^3)' = 3x^2 = 0$. A polynomial of degree $3$ has derivative $0$. This is why [square-free factorization](/square-free-factorization/) over finite fields needs an extra step.
- **Too many roots over a ring that is not a domain.** Over $\mathbb{Z}/8\mathbb{Z}$, $x^2 - 1$ of degree $2$ has the four roots $1, 3, 5, 7$. Rule 6 needs an integral domain.
- **Reversal.** For $f = 2 + 3x + x^3$, $\operatorname{rev}_3(f) = 1 + 3x^2 + 2x^3$. The reversal with $n = 4$ is $x + 3x^3 + 2x^4$.
- **A stored list that is not normalized.** The list $[1, 2, 0, 0]$ stands for $1 + 2x$, of degree $1$, not $3$. A loop that divides by the "last" coefficient $0$ fails.

## Where it is used

- [Polynomial division](/polynomial-division/) and [long division](/polynomial-long-division/): each step lowers the degree of the remainder by at least one, and rule 3 gives the size of the quotient.
- [Polynomial Euclidean algorithm](/polynomial-euclidean-algorithm/): the degrees of the remainders strictly decrease, which bounds the number of steps by $\deg g + 1$.
- [Polynomial multiplication](/polynomial-multiplication/): the product of two polynomials of degree less than $n$ has degree less than $2n - 1$, so $2n - 1$ evaluation points suffice in the [evaluation-interpolation paradigm](/evaluation-interpolation-paradigm/).
- [Factor theorem](/factor-theorem/) and [Vieta's formulas](/vieta-formulas/): a monic polynomial of degree $n$ over a field with $n$ roots, counted with multiplicity, is the product of the $n$ linear factors.
- [Resultant](/resultant/): the size of the Sylvester matrix is $\deg f + \deg g$.
- [Fast polynomial division](/fast-polynomial-division/): the reversal turns division into power series inversion.
- [Square-free polynomial](/square-free-polynomial/): rule 5 decides when $\gcd(f, f')$ detects repeated factors.

## References
