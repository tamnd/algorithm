---
tag: W59BSG
kind: theorem
slug: factor-theorem
name: Factor theorem
aliases:
- root factor theorem
area: algebra/polynomial-arithmetic
level: intro
summary: X - a divides f exactly when f(a) = 0.
prereqs: [polynomial, monic-polynomial]
see_also: [polynomial-remainder-theorem, horner-rule, irreducible-polynomial, multiplicity-of-roots, interpolating-polynomial-uniqueness, schwartz-zippel-lemma, rational-root-theorem, polynomial-root-finding]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 2.4, Division with remainder (division by a monic polynomial); Section 5.2, Evaluation and interpolation (evaluation at u is the remainder modulo x - u); Section 25.3, Polynomials and fields
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition, Cambridge University Press, 2009
    locator: Section 7.2, Polynomial rings (polynomial evaluation, roots, and the bound on the number of roots over an integral domain)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6.4, Evaluation of polynomials (Horner's rule computes the quotient by x - x0 as a by-product)
  - book: isbn:9780471433347
    title: David S. Dummit and Richard M. Foote, Abstract Algebra, third edition, Wiley, 2004
    locator: Section 9.5, Polynomial rings over fields II (a polynomial of degree n over a field has at most n roots)
---

The factor theorem says that a value $a$ is a root of a polynomial $f$ exactly when $x - a$ divides $f$. It holds over every commutative ring, and the quotient comes out of [Horner's rule](/horner-rule/) at no extra cost. Its main consequence is that over an integral domain a nonzero polynomial of degree $n$ has at most $n$ roots, which is the basis of polynomial interpolation, polynomial identity testing, and root finding by deflation.

## Statement

Let $R$ be a commutative ring with $1$, let $f = \sum_{k=0}^{n} f_k x^k \in R[x]$ and let $a \in R$.

**Theorem (remainder and factor theorem).** There is exactly one $q \in R[x]$ with

$$f = (x - a)\, q + f(a).$$

If $\deg f = n \ge 1$, then $\deg q = n - 1$, $\operatorname{lc}(q) = \operatorname{lc}(f)$, and the coefficients of $q = \sum_{k=0}^{n-1} q_k x^k$ are given by $q_{n-1} = f_n$ and $q_{k-1} = f_k + a\, q_k$ for $k = n-1, \ldots, 1$, with $f(a) = f_0 + a\, q_0$. In particular, $x - a$ divides $f$ in $R[x]$ if and only if $f(a) = 0$.

**Corollary (root bound).** Let $D$ be an integral domain and $f \in D[x]$ nonzero of degree $n$. If $a_1, \ldots, a_k \in D$ are distinct roots of $f$, then $(x - a_1) \cdots (x - a_k)$ divides $f$. Hence $f$ has at most $n$ roots in $D$.

## In plain words

Take a polynomial and a number. Divide the polynomial by "x minus the number". The remainder is a constant, and it is exactly the value of the polynomial at that number. So the division leaves nothing behind exactly when the number is a root. The same steps that compute the value also produce the quotient. When the coefficients come from a ring with no zero divisors, such as the integers or any field, each root splits off one factor, and the degree goes down by one each time. So a polynomial of degree n cannot have more than n roots.

## Proof

*Existence.* For each $k \ge 1$ the identity

$$x^k - a^k = (x - a)(x^{k-1} + a x^{k-2} + \cdots + a^{k-2} x + a^{k-1})$$

holds in $R[x]$: expand the right side, and all terms cancel in pairs except $x^k$ and $-a^k$. This uses only commutativity of $R$. Multiply by $f_k$ and sum over $k$:

$$f - f(a) = \sum_{k=1}^{n} f_k (x^k - a^k) = (x - a) \sum_{k=1}^{n} f_k \sum_{j=0}^{k-1} a^{k-1-j} x^j.$$

Call the last sum $q$. Then $f = (x - a) q + f(a)$.

*The coefficients of $q$.* Compare coefficients in $f = (x - a) q + r$ with $r \in R$ and $q = \sum_{k=0}^{n-1} q_k x^k$. The coefficient of $x^n$ gives $f_n = q_{n-1}$. For $1 \le k \le n - 1$ the coefficient of $x^k$ gives $f_k = q_{k-1} - a q_k$, so $q_{k-1} = f_k + a q_k$. The constant term gives $f_0 = r - a q_0$, so $r = f_0 + a q_0$. Unrolling this recurrence gives $r = f_0 + a(f_1 + a(f_2 + \cdots + a f_n))$, which is $f(a)$ written in Horner form. So $q$ and $r = f(a)$ are exactly the intermediate values and the final value of Horner's rule. Since $q_{n-1} = f_n \ne 0$, $\deg q = n - 1$.

*Uniqueness.* Suppose $(x - a) q + f(a) = (x - a) q' + f(a)$. Then $(x - a)(q - q') = 0$. The polynomial $x - a$ is [monic](/monic-polynomial/), and a monic polynomial is not a zero divisor: if $h \ne 0$ then the top coefficient of $(x - a) h$ is $\operatorname{lc}(h) \ne 0$. So $q = q'$.

*Divisibility.* If $f(a) = 0$, then $f = (x - a) q$. Conversely, if $f = (x - a) g$ for some $g \in R[x]$, then evaluation at $a$ is a ring homomorphism $R[x] \to R$ (this uses commutativity), so $f(a) = (a - a) g(a) = 0$.

*Root bound.* Induction on $k$. For $k = 0$ the product is $1$. Suppose $f = (x - a_1) \cdots (x - a_{k-1})\, g$ for some $g \in D[x]$. Evaluate at $a_k$: $0 = f(a_k) = \prod_{i<k} (a_k - a_i) \cdot g(a_k)$. Each factor $a_k - a_i$ is nonzero because the roots are distinct, and $D$ has no zero divisors, so $g(a_k) = 0$. By the theorem, $g = (x - a_k) g'$, which gives the claim for $k$. Over an integral domain, $\deg(uv) = \deg u + \deg v$, so the degree $k$ of the product of linear factors is at most $\deg f = n$. $\blacksquare$

## Consequences

- **Interpolation is unique.** Over an integral domain, two polynomials of degree less than $n$ that agree at $n$ distinct points are equal, because their difference has degree less than $n$ and $n$ roots. This is the uniqueness half of [polynomial interpolation](/interpolating-polynomial-uniqueness/), and it is why the [point-value representation](/point-value-representation/) of a polynomial is faithful.
- **Polynomials and functions.** Over an infinite integral domain, a polynomial that vanishes at every point is zero. So two polynomials that define the same function are equal. Over a finite field $\mathbb{F}_q$ this fails: $x^q - x$ vanishes at every point of $\mathbb{F}_q$, since it has $q$ roots there, and it is not zero.
- **Identity testing.** A nonzero polynomial of degree $n$ over a field vanishes at no more than $n$ points of a finite set $S$. A random point of $S$ is a root with probability at most $n/|S|$. The multivariate form is the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/), used for [polynomial identity testing](/polynomial-identity-testing/).
- **Deflation.** After a root $a$ is found, numerical and exact [root finders](/polynomial-root-finding/) continue with the quotient $q$, which has degree $n - 1$. Horner's rule gives $q$ at the cost of evaluating $f(a)$.
- **Multiple roots.** $(x - a)^2$ divides $f$ exactly when $f(a) = 0$ and $f'(a) = 0$. Apply the theorem to $f$ and then to $q$, and use $f' = q + (x - a) q'$, so that $f'(a) = q(a)$. See [multiplicity of roots](/multiplicity-of-roots/).
- **Irreducibility in low degree.** Over a field, a polynomial of degree 2 or 3 is [irreducible](/irreducible-polynomial/) exactly when it has no root.
- **Remainder modulo many points.** The remainder of $f$ modulo $x - a$ is $f(a)$. Evaluating at many points is therefore computing many remainders, and [fast multipoint evaluation](/fast-multipoint-evaluation/) does this with a tree of products of the moduli $x - a_i$.

**Worked example.** Take $f = 2x^3 - 6x^2 + 2x - 1$ over $\mathbb{Z}$ and $a = 3$. The recurrence gives $q_2 = 2$, $q_1 = -6 + 3 \cdot 2 = 0$, $q_0 = 2 + 3 \cdot 0 = 2$ and $f(3) = -1 + 3 \cdot 2 = 5$. So $f = (x - 3)(2x^2 + 2) + 5$, and $x - 3$ does not divide $f$. For $f = x^3 - 6x^2 + 11x - 6$ and $a = 1$ the recurrence gives $q = x^2 - 5x + 6$ and remainder $0$, so $f = (x - 1)(x^2 - 5x + 6) = (x - 1)(x - 2)(x - 3)$.

## Tightness

- **The root bound is attained.** $(x - a_1) \cdots (x - a_n)$ with distinct $a_i$ has degree $n$ and exactly $n$ roots in any integral domain that contains $n$ distinct elements.
- **The integral domain hypothesis is needed for the root bound.** Over $\mathbb{Z}/8\mathbb{Z}$, $x^2 - 1$ has the four roots $1, 3, 5, 7$, and $x^2 - 1 = (x - 1)(x + 1) = (x - 3)(x - 5)$, so factorization into linear factors is not unique. Over $\mathbb{Z}/6\mathbb{Z}$, $x^2 - x$ has the four roots $0, 1, 3, 4$. The proof breaks where it cancels $\prod (a_k - a_i)$: in $\mathbb{Z}/8\mathbb{Z}$, $(3 - 1) \cdot g(3) = 2 \cdot 4 = 0$ with $g = x + 1$ and $g(3) = 4 \ne 0$. The factor theorem itself still holds there: each single root $a$ gives a factor $x - a$.
- **Commutativity is needed.** In the quaternions, $x^2 + 1$ has infinitely many roots, for example $i$, $j$ and $k$. Evaluation is not a ring homomorphism in a noncommutative ring, so the divisibility step fails.
- **The zero polynomial is excluded.** It vanishes everywhere and has no degree in $\mathbb{N}$.

## History

The statement that $x - a$ divides a polynomial equation with root $a$ appears in Book III of Descartes' La Geometrie (1637), and the factor theorem is often named after him for this reason. Lagrange proved in 1768 that a polynomial congruence of degree $n$ modulo a prime $p$ has at most $n$ solutions, which is the root bound over the field $\mathbb{Z}/p\mathbb{Z}$. The modern form, for polynomials over an arbitrary commutative ring with the root bound over integral domains, is standard in algebra texts such as Dummit and Foote and in computer algebra texts such as von zur Gathen and Gerhard.

## References
