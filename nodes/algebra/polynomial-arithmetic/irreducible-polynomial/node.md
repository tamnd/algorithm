---
tag: H562FR
kind: definition
slug: irreducible-polynomial
name: Irreducible polynomial
aliases:
- prime polynomial
area: algebra/polynomial-arithmetic
level: intro
summary: Non-constant polynomial that admits no factorisation into two non-constant polynomials.
prereqs: [polynomial, monic-polynomial]
see_also: [primitive-polynomial, factor-theorem, eisenstein-criterion, gauss-lemma, polynomial-irreducibility-testing, rabin-irreducibility-test, polynomial-factorization-over-finite-fields, square-free-polynomial]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 14.1, Factorization of polynomials; Section 14.2, Distinct-degree factorization (the product of all monic irreducible polynomials whose degree divides d); Section 14.9, Testing irreducibility; Section 25.3, Polynomials and fields
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition, Cambridge University Press, 2009
    locator: Section 16.3, Unique factorization of polynomials; Section 20.1, Tests for and constructing irreducible polynomials
  - book: isbn:9780471433347
    title: David S. Dummit and Richard M. Foote, Abstract Algebra, third edition, Wiley, 2004
    locator: Section 9.3, Polynomial rings that are unique factorization domains; Section 9.4, Irreducibility criteria
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6.2, Factorization of polynomials
---

An irreducible polynomial is a polynomial that cannot be written as a product of two polynomials of smaller degree, in the same way that a prime number cannot be written as a product of two smaller numbers. Over a field, every nonconstant polynomial is a constant times a product of [monic](/monic-polynomial/) irreducible polynomials, and these factors are unique up to order. Irreducibility depends on the coefficient ring: $x^2 + 1$ is irreducible over $\mathbb{Q}$ and $\mathbb{R}$, but it splits over $\mathbb{C}$ and over $\mathbb{F}_2$ and $\mathbb{F}_5$.

## Definition

**Over a field.** Let $F$ be a field. A polynomial $f \in F[x]$ is **irreducible over $F$** when $\deg f \ge 1$ and there are no $g, h \in F[x]$ with $f = gh$, $\deg g \ge 1$ and $\deg h \ge 1$. Equivalently, every factorization $f = gh$ in $F[x]$ has $g$ or $h$ a nonzero constant. A nonconstant polynomial that is not irreducible is **reducible**. Constants are neither irreducible nor reducible: the zero polynomial is excluded, and the nonzero constants are the units of $F[x]$.

**Over an integral domain.** Let $D$ be an integral domain, for example $\mathbb{Z}$. A polynomial $f \in D[x]$ is irreducible in $D[x]$ when $f$ is nonzero, not a unit, and every factorization $f = gh$ in $D[x]$ has $g$ or $h$ a unit of $D$. This is the general definition of an irreducible element of a ring. Over a field it is the definition above, because the units of $F[x]$ are the nonzero constants. Over $\mathbb{Z}$ the two notions differ, because a nonunit constant such as $2$ is a valid factor: $2x + 2 = 2(x + 1)$ is reducible in $\mathbb{Z}[x]$ and irreducible in $\mathbb{Q}[x]$, and the prime $3$ is irreducible as a constant polynomial in $\mathbb{Z}[x]$. By [Gauss's lemma](/gauss-lemma/), a nonconstant $f \in \mathbb{Z}[x]$ is irreducible in $\mathbb{Z}[x]$ exactly when it is [primitive](/primitive-polynomial/) and irreducible in $\mathbb{Q}[x]$. On these pages, "irreducible" without a ring means irreducible over the field of coefficients at hand.

**Facts used by the algorithms.** Let $F$ be a field.

1. **Degree 1.** Every polynomial of degree 1 is irreducible, because the degrees of the factors would have to add to 1.
2. **Degree 2 and 3.** A polynomial $f$ of degree 2 or 3 is reducible exactly when it has a root in $F$. A factorization into two nonconstant factors of total degree 2 or 3 must contain a factor of degree 1, and by the [factor theorem](/factor-theorem/) a factor $x - a$ exists exactly when $f(a) = 0$. This fails from degree 4 on: $x^4 + 4 = (x^2 + 2x + 2)(x^2 - 2x + 2)$ has no rational root and is reducible over $\mathbb{Q}$.
3. **Unique factorization.** Each nonzero $f \in F[x]$ is $f = \operatorname{lc}(f)\, p_1^{e_1} \cdots p_k^{e_k}$ with distinct monic irreducible $p_i$ and $e_i \ge 1$, and this form is unique up to the order of the factors. The reason is that $F[x]$ is a Euclidean domain, so an irreducible $p$ that divides $gh$ divides $g$ or $h$.
4. **Quotient field.** The ring $F[x]/(f)$ is a field exactly when $f$ is irreducible. This is how finite fields $\mathbb{F}_{q^n}$ are built: take an irreducible $f \in \mathbb{F}_q[x]$ of degree $n$.
5. **Counting over a finite field.** Let $I_q(n)$ be the number of monic irreducible polynomials of degree $n$ in $\mathbb{F}_q[x]$. The polynomial $x^{q^n} - x$ is the product of all monic irreducible polynomials whose degree divides $n$, each once. Comparing degrees gives $q^n = \sum_{d \mid n} d\, I_q(d)$, and Mobius inversion gives
$$I_q(n) = \frac{1}{n} \sum_{d \mid n} \mu(d)\, q^{n/d}, \qquad \frac{q^n}{n} - \frac{2 q^{n/2}}{n} \le I_q(n) \le \frac{q^n}{n}.$$
So about one monic polynomial in $n$ of degree $n$ is irreducible. A random search for an irreducible polynomial therefore needs about $n$ trials on average, each with an [irreducibility test](/rabin-irreducibility-test/).

## Examples and non-examples

- $x^2 + 1$ is irreducible over $\mathbb{Q}$, $\mathbb{R}$ and $\mathbb{F}_3$, since it has no root there (fact 2). It is reducible over $\mathbb{C}$ as $(x - i)(x + i)$, over $\mathbb{F}_2$ as $(x + 1)^2$, and over $\mathbb{F}_5$ as $(x - 2)(x - 3)$.
- $x^2 - 2$ is irreducible over $\mathbb{Q}$, because $\sqrt 2$ is irrational, and reducible over $\mathbb{R}$ as $(x - \sqrt 2)(x + \sqrt 2)$.
- $x^2 + x + 1$ and $x^3 + x + 1$ are irreducible over $\mathbb{F}_2$: neither has $0$ or $1$ as a root. The second one defines the field $\mathbb{F}_8 = \mathbb{F}_2[x]/(x^3 + x + 1)$.
- $x^4 + 1$ is irreducible over $\mathbb{Q}$ (substitute $x + 1$ for $x$ and apply the [Eisenstein criterion](/eisenstein-criterion/) with $p = 2$), but it is reducible modulo every prime $p$. So reduction modulo one prime cannot prove that every polynomial is irreducible over $\mathbb{Z}$.
- $x^4 + 4$ has no rational root and is still reducible over $\mathbb{Q}$, as shown in fact 2.
- $2x + 2$ is reducible in $\mathbb{Z}[x]$ and irreducible in $\mathbb{Q}[x]$.
- Counts over $\mathbb{F}_2$: $I_2(1), \ldots, I_2(5) = 2, 1, 2, 3, 6$. Over $\mathbb{F}_3$: $I_3(1), I_3(2), I_3(3) = 3, 3, 8$. The formula of fact 5 gives the same numbers, for example $I_2(4) = (2^4 - 2^2)/4 = 3$.
- Constants are not irreducible. The zero polynomial is not irreducible.

## Related definitions

- [Monic polynomial](/monic-polynomial/): the factors in the unique factorization over a field are chosen monic.
- [Primitive polynomial](/primitive-polynomial/) and [Gauss's lemma](/gauss-lemma/): they connect irreducibility over $\mathbb{Z}$ and over $\mathbb{Q}$.
- [Square-free polynomial](/square-free-polynomial/): a polynomial whose factorization has all $e_i = 1$.
- [Eisenstein criterion](/eisenstein-criterion/): a sufficient condition for irreducibility over $\mathbb{Q}$.
- [Polynomial irreducibility testing](/polynomial-irreducibility-testing/) and [Rabin's test](/rabin-irreducibility-test/): the decision problem and an algorithm for it over finite fields.
- [Factorization over finite fields](/polynomial-factorization-over-finite-fields/) and [over the integers](/polynomial-factorization-over-integers/): the problems of finding the irreducible factors.
- [Prime number](/prime-number/): the analogue in $\mathbb{Z}$.

## References
