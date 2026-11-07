---
tag: 6ZJDDQ
kind: definition
slug: primitive-polynomial
name: Primitive polynomial
aliases:
- Content and primitive part
- content and primitive part
- primitive polynomial
- content of a polynomial
area: algebra/polynomial-arithmetic
level: core
summary: Integer polynomial whose coefficients have gcd 1; the content is the gcd of the coefficients.
prereqs: [polynomial-ring, greatest-common-divisor]
see_also: [gauss-lemma, polynomial-gcd, primitive-prs, subresultant-gcd, polynomial-factorization-over-integers, eisenstein-criterion, pseudo-division, monic-polynomial]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 6.2, Gauß' lemma (p. 147; content, primitive part and the normal form in R[x] for a UFD R), and Section 6.12, Pseudodivision and primitive Euclidean Algorithms (p. 190)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6.1, Division of Polynomials (content, primitive part, and Gauss's lemma over a unique factorization domain)
  - book: isbn:9780471433347
    title: David S. Dummit and Richard M. Foote, Abstract Algebra, third edition, Wiley, 2004
    locator: Section 9.3, Polynomial rings that are unique factorization domains (Gauss's lemma and its corollaries)
---

A polynomial with integer coefficients is primitive when the greatest common divisor of its coefficients is $1$, and that gcd is the content of the polynomial. Every nonzero $f \in \mathbb{Z}[x]$ splits as $f = \operatorname{cont}(f) \cdot \operatorname{pp}(f)$ into its content and a primitive part, and the same holds over every unique factorization domain. The split separates the integer part of a problem from the polynomial part. By [Gauss's lemma](/gauss-lemma/), the product of primitive polynomials is primitive, which links factorization and gcds in $\mathbb{Z}[x]$ to those in $\mathbb{Q}[x]$.

## Definition

Let $R$ be a unique factorization domain, for example $\mathbb{Z}$, $F[y]$ for a field $F$, or $\mathbb{Z}[y_1, \ldots, y_k]$. Gcds in $R$ exist and are unique up to a unit factor. We fix a normal form: over $\mathbb{Z}$ the positive one, over $F[y]$ the monic one.

**Content.** For $f = \sum_{i=0}^{n} a_i x^i \in R[x]$ with $f \ne 0$, the *content* is

$$\operatorname{cont}(f) = \pm \gcd(a_0, a_1, \ldots, a_n),$$

with the sign (or unit) chosen so that the leading coefficient of $f / \operatorname{cont}(f)$ is normal; over $\mathbb{Z}$, the sign of $\operatorname{cont}(f)$ is the sign of $\operatorname{lc}(f)$. By convention $\operatorname{cont}(0) = 0$.

**Primitive.** $f \ne 0$ is *primitive* when $\gcd(a_0, \ldots, a_n)$ is a unit of $R$, that is $1$ over $\mathbb{Z}$.

**Primitive part.** For $f \ne 0$, $\operatorname{pp}(f) = f / \operatorname{cont}(f)$. It lies in $R[x]$, it is primitive, and its leading coefficient is normal. By convention $\operatorname{pp}(0) = 0$.

**Basic facts.**

1. $f = \operatorname{cont}(f) \cdot \operatorname{pp}(f)$, and this is the only way to write $f = c\, g$ with $c \in R$ and $g \in R[x]$ primitive with a normal leading coefficient. *Proof.* If $f = c g$ with $g$ primitive, the gcd of the coefficients of $f$ is $c$ times the gcd of those of $g$, up to a unit, so $c$ and $\operatorname{cont}(f)$ agree up to a unit; the normal leading coefficient fixes the unit. $\square$
2. **Primitive over $\mathbb{Q}$.** Every nonzero $f \in \mathbb{Q}[x]$ is $f = c \cdot g$ with $c \in \mathbb{Q}$ and $g \in \mathbb{Z}[x]$ primitive with $\operatorname{lc}(g) > 0$, in exactly one way. *Proof.* Multiply by a common denominator $d$, so that $d f \in \mathbb{Z}[x]$, and take $c = \operatorname{cont}(d f) / d$ and $g = \operatorname{pp}(d f)$. If $c g = c' g'$, clear the denominators of $c$ and $c'$ and apply fact 1. $\square$ The same holds for the field of fractions of any UFD.
3. **Gauss's lemma.** If $f, g \in R[x]$ are primitive, so is $f g$. Hence $\operatorname{cont}(f g) = \operatorname{cont}(f) \operatorname{cont}(g)$ and $\operatorname{pp}(f g) = \operatorname{pp}(f) \operatorname{pp}(g)$. *Proof for $R = \mathbb{Z}$.* Assume a prime $p$ divides every coefficient of $f g$. Reduce modulo $p$: $\bar f \bar g = 0$ in $\mathbb{F}_p[x]$. Since $\mathbb{F}_p[x]$ is an integral domain, $\bar f = 0$ or $\bar g = 0$, so $p$ divides all coefficients of $f$ or of $g$, against primitivity. For a general UFD, replace $p$ by a prime element $\pi$ and $\mathbb{F}_p$ by the domain $R/(\pi)$. $\square$ See [Gauss's lemma](/gauss-lemma/) for the consequences.
4. **A test by reduction.** $f \in \mathbb{Z}[x]$ is primitive exactly when $f \bmod p \ne 0$ for every prime $p$.
5. **Monic implies primitive.** A monic polynomial has a coefficient equal to $1$, so it is primitive.

**Computing.** $\operatorname{cont}(f)$ takes $n$ gcds in $R$, folded from left to right, and the fold can stop as soon as the gcd is a unit. Over $\mathbb{Z}$ the fold takes $O(n + \log \max_i |a_i|)$ Euclidean division steps in total, since the running gcd only shrinks (see [gcd of an array](/gcd-of-array/)). The primitive part then takes $n + 1$ exact divisions.

## Examples and non-examples

- $f = 6x^2 + 10x + 4$ has $\operatorname{cont}(f) = 2$ and $\operatorname{pp}(f) = 3x^2 + 5x + 2$. It is not primitive.
- $2x + 3$ is primitive, although no coefficient is $\pm 1$: $\gcd(2, 3) = 1$.
- $-4x^2 - 6$ has $\operatorname{cont} = -2$ with the sign convention, and $\operatorname{pp} = 2x^2 + 3$.
- Constants: $5$ has content $5$ and primitive part $1$. The constant $1$ is primitive. The zero polynomial is not primitive.
- **Over $\mathbb{Q}$.** $\tfrac12 x^2 + \tfrac13 x + 1 = \tfrac16 (3x^2 + 2x + 6)$, so its rational content is $1/6$ and its primitive part is $3x^2 + 2x + 6$.
- **Gauss's lemma at work.** $(2x + 1)(3x + 2) = 6x^2 + 7x + 2$ is primitive, as the lemma says. For $(2x + 2)(3x + 3) = 6x^2 + 12x + 6$, the content is $6 = 2 \cdot 3$, the product of the contents.
- **Several variables.** In $\mathbb{Z}[y][x]$, $f = (y^2 - 1)\, x + (y - 1)$ has content $y - 1$ as a polynomial in $x$ with coefficients in $\mathbb{Z}[y]$, and primitive part $(y + 1)\, x + 1$. Recursive gcd algorithms for several variables use this content.
- **Over a field.** In $F[x]$, every nonzero polynomial is primitive, since every nonzero coefficient is a unit. The notion matters only over rings that are not fields.

## Related definitions

- **Gauss's lemma.** The product of primitive polynomials is primitive; so a primitive $f \in \mathbb{Z}[x]$ of positive degree is irreducible in $\mathbb{Z}[x]$ exactly when it is [irreducible](/irreducible-polynomial/) in $\mathbb{Q}[x]$. See [Gauss's lemma](/gauss-lemma/).
- **Gcd through contents.** $\gcd(f, g) = \gcd(\operatorname{cont} f, \operatorname{cont} g) \cdot \gcd(\operatorname{pp} f, \operatorname{pp} g)$ in $R[x]$; see [polynomial GCD](/polynomial-gcd/).
- **Primitive remainder sequences.** The [primitive PRS](/primitive-prs/) replaces each [pseudo-remainder](/pseudo-division/) by its primitive part, which keeps the coefficients as small as possible at the price of a content computation per step.
- **Factoring over $\mathbb{Z}$.** [Factoring in $\mathbb{Z}[x]$](/polynomial-factorization-over-integers/) splits $f$ into the factorization of the integer $\operatorname{cont}(f)$ and the factorization of the primitive polynomial $\operatorname{pp}(f)$.
- **Monic polynomial.** A stronger normalization, with leading coefficient $1$; see [monic polynomial](/monic-polynomial/). Over a field, the monic associate of a polynomial plays the role of the primitive part.
- **A different meaning over finite fields.** In coding theory and for [linear feedback shift registers](/linear-feedback-shift-register/), a *primitive polynomial* over $\mathbb{F}_q$ is an irreducible polynomial of degree $k$ whose roots generate the multiplicative group of $\mathbb{F}_{q^k}$, so its root is a [primitive root](/primitive-root/) of the field. This is a different notion with the same name.

## References
