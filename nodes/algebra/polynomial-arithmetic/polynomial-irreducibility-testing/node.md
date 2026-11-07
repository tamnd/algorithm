---
tag: EGMQCP
kind: problem
slug: polynomial-irreducibility-testing
name: Polynomial irreducibility testing
aliases:
- irreducibility test
- testing irreducibility of polynomials
area: algebra/polynomial-arithmetic
level: advanced
summary: Decide whether a given polynomial is irreducible over a field. Over finite fields and over Q this takes polynomial time; over some computable fields it is undecidable.
model: blum-shub-smale-machine
complexity:
  vars: {n: the degree of f, q: the number of elements of the finite field, M: the cost function M(n) of multiplying two polynomials of degree less than n}
  time: {worst: O(n M(n) log q)}
prereqs: [irreducible-polynomial, polynomial-ring]
see_also: [irreducible-polynomial, rabin-irreducibility-test, eisenstein-criterion, gauss-lemma, polynomial-factorization-over-finite-fields, polynomial-factorization-over-integers, distinct-degree-factorization, lll-algorithm]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 14.9, Testing irreducibility and constructing irreducible polynomials; Chapter 16 for factoring over Q with lattice reduction
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6.2, Factorization of Polynomials
  - paper: doi:10.1137/0209024
    title: Michael O. Rabin, Probabilistic algorithms in finite fields, SIAM Journal on Computing 9(2), 1980
    locator: pp. 273 to 280
  - paper: doi:10.1109/SFCS.1981.37
    title: Michael Ben-Or, Probabilistic algorithms in finite fields, 22nd Annual Symposium on Foundations of Computer Science, 1981
    locator: pp. 394 to 398
  - paper: doi:10.1007/BF01457454
    title: Arjen K. Lenstra, Hendrik W. Lenstra Jr. and László Lovász, Factoring polynomials with rational coefficients, Mathematische Annalen 261(4), 1982
    locator: pp. 515 to 534
  - paper: doi:10.1098/rsta.1956.0003
    title: Albrecht Fröhlich and John C. Shepherdson, Effective procedures in field theory, Philosophical Transactions of the Royal Society of London A 248, 1956
    locator: pp. 407 to 432
  - paper: doi:10.1145/800205.806338
    title: Barry M. Trager, Algebraic factoring and rational function integration, SYMSAC 1976
    locator: pp. 219 to 226
---

Irreducibility testing asks whether a polynomial $f$ of degree $n \ge 1$ over a field $F$ is [irreducible](/irreducible-polynomial/): whether it has no factorization $f = gh$ into two polynomials of smaller degree. The answer depends on the field: $x^2 + 1$ is irreducible over $\mathbb{Q}$ and $\mathbb{R}$ but not over $\mathbb{C}$ or $\mathbb{F}_5$. Over a finite field $\mathbb{F}_q$, [Rabin's test](/rabin-irreducibility-test/) decides it deterministically in $O(n\, M(n) \log q)$ field operations, and over $\mathbb{Q}$ it is decidable in polynomial time by lattice reduction. Over some fields that are computable in the usual sense, no algorithm can decide it.

## In plain words

A polynomial is irreducible when it cannot be written as a product of two polynomials of lower degree. Prime numbers play the same part among the integers. The question has no single answer for a polynomial alone: the allowed coefficients matter, because a polynomial that cannot be split with rational coefficients can perhaps be split with real or complex ones.

For coefficients in a finite field there are fast and exact tests that never find the factors. For rational coefficients there are quick tests that can only prove irreducibility in good cases, and complete methods that come from factoring. For some unusual fields no method can answer the question at all.

## Definition

Let $F$ be a field. A polynomial $f \in F[x]$ is *irreducible* if $\deg f \ge 1$ and $f = gh$ with $g, h \in F[x]$ implies that $g$ or $h$ is a constant. Constants, including $0$, are not irreducible: nonzero constants are units.

**Problem.** Given $f \in F[x]$ of degree $n$, decide whether $f$ is irreducible over $F$.

The input must be given in a form that the algorithm can compute with: elements of a finite field, rational numbers, or elements of a number field written in a basis. For a ring that is not a field, such as $\mathbb{Z}$, the definition changes: $2x + 2 = 2(x + 1)$ is reducible in $\mathbb{Z}[x]$ because $2$ is not a unit, but $2x + 2$ is irreducible in $\mathbb{Q}[x]$. By [Gauss's lemma](/gauss-lemma/), a [primitive](/primitive-polynomial/) $f \in \mathbb{Z}[x]$ of degree at least $1$ is irreducible in $\mathbb{Z}[x]$ exactly when it is irreducible in $\mathbb{Q}[x]$.

**Cost model.** Over $\mathbb{F}_q$ we count field operations at unit cost, in the algebraic model of the [Blum-Shub-Smale machine](/blum-shub-smale-machine/), and $M(n)$ is the cost of multiplying two polynomials of degree less than $n$. Over $\mathbb{Q}$, coefficients grow, so costs are bit operations in the input size: the degree $n$ and the maximal coefficient length.

## Variants

- **Over $\mathbb{C}$.** By the fundamental theorem of algebra, $f$ is irreducible exactly when $n = 1$.
- **Over $\mathbb{R}$.** $f$ is irreducible exactly when $n = 1$, or $n = 2$ and $f = ax^2 + bx + c$ has $b^2 - 4ac < 0$. Non-real complex roots come in conjugate pairs, so every real polynomial is a product of such factors.
- **Over a finite field $\mathbb{F}_q$.** Decidable in polynomial time, deterministically, with Rabin's or Ben-Or's test.
- **Over $\mathbb{Q}$ and $\mathbb{Z}$.** Decidable by factoring; there are also cheap sufficient tests.
- **Over a number field $\mathbb{Q}(\alpha)$.** Trager (1976) reduces factoring, and so testing, to factoring a norm over $\mathbb{Q}$.
- **Over a general computable field.** Fröhlich and Shepherdson (1956) gave fields whose arithmetic is computable but over which no algorithm decides irreducibility of polynomials.
- **Absolute irreducibility.** Over $\mathbb{Q}$ or $\mathbb{F}_q$, one may also ask whether $f$, usually multivariate, stays irreducible over the algebraic closure. This is a different problem.

## Examples

A script checked the finite-field claims below with the implementation of [Rabin's test](/rabin-irreducibility-test/).

- **The same polynomial over different fields.** $x^2 + 1$ is irreducible over $\mathbb{Q}$, $\mathbb{R}$ and $\mathbb{F}_3$, since it has no root there and has degree $2$. It is reducible over $\mathbb{C}$, as $(x - i)(x + i)$; over $\mathbb{F}_5$, as $(x - 2)(x + 2)$; and over $\mathbb{F}_2$, as $(x + 1)^2$.
- **A finite field.** $x^4 + x + 1$ is irreducible over $\mathbb{F}_2$; Rabin's test checks it in four squarings modulo $f$, as on its page.
- **Eisenstein's criterion.** $x^3 - 2$ is irreducible over $\mathbb{Q}$ by the [Eisenstein criterion](/eisenstein-criterion/) at the prime $2$. It is also irreducible over $\mathbb{F}_7$, because $2$ is not a cube modulo $7$, and reducible over $\mathbb{F}_5$, where $3^3 = 27 \equiv 2$.
- **Reduction modulo a prime.** $x^3 + x + 1$ is irreducible over $\mathbb{F}_2$, so it is irreducible over $\mathbb{Q}$, by the criterion below.
- **A polynomial that is reducible modulo every prime.** $x^4 + 1$ is irreducible over $\mathbb{Q}$: $f(x + 1) = x^4 + 4x^3 + 6x^2 + 4x + 2$ is Eisenstein at $2$. But it is reducible over every $\mathbb{F}_p$. Over $\mathbb{F}_2$ it is $(x + 1)^4$. For odd $p$, $8 \mid p^2 - 1$, and every root $\alpha$ satisfies $\alpha^8 = 1$, so $\alpha^{p^2} = \alpha$; the polynomial is square-free, as $\gcd(f, 4x^3) = 1$, so it divides $x^{p^2} - x$ and all its irreducible factors have degree $1$ or $2$. So the test modulo a prime can never prove $x^4 + 1$ irreducible. The script confirms the reducibility for all primes below $200$.
- **The derivative may vanish.** Over $\mathbb{F}_p(t)$, $x^p - t$ is irreducible, by Eisenstein at $t$, although its derivative is $0$.

## Known algorithms

**Over finite fields.**

- **[Rabin's test](/rabin-irreducibility-test/)** (1980). $f$ of degree $n$ is irreducible exactly when $x^{q^n} \equiv x \pmod f$ and $\gcd(x^{q^{n/r}} - x, f) = 1$ for each prime $r \mid n$. Cost $O(n\, M(n) \log q)$ field operations.
- **Ben-Or's test** (1981). Check $\gcd(x^{q^i} - x, f) = 1$ for $i = 1, \ldots, \lfloor n/2 \rfloor$, stopping at the first failure. Same worst case; faster on random inputs, which usually have a small factor.
- **Berlekamp's matrix.** For square-free $f$, the number of irreducible factors equals the dimension of the kernel of $Q - I$, where $Q$ is the matrix of the map $g \mapsto g^q \bmod f$. So $f$ is irreducible exactly when it is square-free and $Q - I$ has rank $n - 1$. Building $Q$ and using [Gaussian elimination](/gaussian-elimination/) costs $O(n^3)$ field operations plus the powering. See [Berlekamp factorization](/berlekamp-factorization/) and Knuth, Section 4.6.2.
- **[Distinct-degree factorization](/distinct-degree-factorization/).** It finds the product of the irreducible factors of each degree; $f$ is irreducible when all of them sit in degree $n$.

**Over $\mathbb{Q}$ and $\mathbb{Z}$.**

- **Sufficient criteria.** The [Eisenstein criterion](/eisenstein-criterion/), also after a substitution $x \mapsto x + a$. The *reduction criterion*: if $f \in \mathbb{Z}[x]$ is primitive, $p \nmid \operatorname{lc}(f)$, and $f \bmod p$ is irreducible over $\mathbb{F}_p$, then $f$ is irreducible over $\mathbb{Q}$. Proof: a factorization $f = gh$ in $\mathbb{Z}[x]$ with $\deg g, \deg h \ge 1$, which exists by Gauss's lemma if $f$ is reducible over $\mathbb{Q}$, has $p \nmid \operatorname{lc}(g) \operatorname{lc}(h)$, so it gives a factorization modulo $p$ with the same degrees. Degree information from several primes also helps: if the factor degrees modulo different primes have no common partial sum, except $0$ and $n$, then $f$ is irreducible.
- **Complete methods by factoring.** The [Zassenhaus algorithm](/zassenhaus-algorithm/) factors modulo $p$, lifts with [Hensel lifting](/hensel-lifting/), and tries subsets of the lifted factors; it is fast in practice but exponential in the worst case. Lenstra, Lenstra and Lovász (1982) replaced the subset search by the [LLL lattice reduction](/lll-algorithm/) and gave the first polynomial-time algorithm, so irreducibility over $\mathbb{Q}$ is decidable in polynomial time. See [factorization over the integers](/polynomial-factorization-over-integers/).
- **Kronecker's method** tries all possible factors by interpolation; it is finite but exponential. See [Kronecker's factorization method](/kronecker-factorization-method/).

## Bounds

- **Finite fields, upper bound.** $O(n\, M(n) \log q)$ field operations, deterministic, by Rabin's test. This is proved. Methods that compute the Frobenius powers by modular composition, following von zur Gathen and Shoup (1992), reduce the dependence on $n$; see [polynomial composition](/polynomial-composition/).
- **Finite fields, lower bound.** $\Omega(n)$ in general, as the answer depends on every coefficient. No better lower bound is known in the algebraic model.
- **Over $\mathbb{Q}$.** Polynomial in $n$ and in the coefficient length, by Lenstra, Lenstra and Lovász (1982). This is proved.
- **Over general computable fields.** Undecidable for some fields, by Fröhlich and Shepherdson (1956).

## Reductions

- **Testing reduces to factoring.** $f$ is irreducible exactly when its factorization has one factor of multiplicity one. Over $\mathbb{F}_q$, testing is cheaper than factoring: it needs no randomness and no equal-degree splitting.
- **Over $\mathbb{Z}$ to over $\mathbb{Q}$.** By Gauss's lemma, $f \in \mathbb{Z}[x]$ of degree at least $1$ is irreducible in $\mathbb{Z}[x]$ exactly when it is primitive and irreducible in $\mathbb{Q}[x]$.
- **Square-freeness first.** An irreducible polynomial over a perfect field, such as $\mathbb{Q}$ or $\mathbb{F}_q$, is square-free, so $\gcd(f, f') \ne 1$ already proves reducibility there; see [square-free factorization](/square-free-factorization/).
- **Construction reduces to testing.** To find an irreducible polynomial of degree $n$ over $\mathbb{F}_q$, test random monic candidates; about one in $n$ is irreducible, so $O(n)$ tests are expected.

## Applications

- **Building finite fields.** $\mathbb{F}_{p^n}$ is $\mathbb{F}_p[x]/(f)$ for an irreducible $f$ of degree $n$; this needs a tested $f$.
- **Coding theory and pseudorandom sequences.** Cyclic codes and [linear feedback shift registers](/linear-feedback-shift-register/) use irreducible and primitive polynomials over $\mathbb{F}_2$.
- **Cryptography.** Binary field arithmetic and some lattice and code-based schemes use a fixed irreducible modulus.
- **Computer algebra.** Factoring algorithms test the factors they produce, and simplifiers test whether an algebraic number is given by its minimal polynomial.

## References
