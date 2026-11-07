---
tag: N9QH16
kind: problem
slug: polynomial-gcd
name: Polynomial GCD
aliases:
- greatest common divisor of polynomials
- polynomial greatest common divisor
area: algebra/polynomial-arithmetic
level: core
summary: Compute the monic greatest common divisor of two polynomials over a field.
model: blum-shub-smale-machine
complexity:
  vars: {n: the larger of the degrees of f and g, M: the multiplication time (M(k) field operations to multiply two polynomials of degree less than k)}
  time: {worst: O(M(n) log n)}
prereqs: [polynomial-division, greatest-common-divisor, euclidean-domain]
see_also: [polynomial-euclidean-algorithm, polynomial-extended-euclidean-algorithm, half-gcd, subresultant-gcd, brown-modular-gcd, heuristic-gcd, resultant, square-free-polynomial]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 3, The Euclidean Algorithm (Sections 3.2 to 3.4, pp. 47 to 61); Chapter 6, Modular algorithms and interpolation (Sections 6.1 to 6.4 and 6.10 to 6.12); Section 11.1, Fast Euclidean Algorithm (p. 313)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6.1, Division of Polynomials (Euclid's algorithm for polynomials, the growth of the coefficients over the rationals, and the subresultant and modular methods)
  - book: isbn:9780792392590
    title: Keith O. Geddes, Stephen R. Czapor and George Labahn, Algorithms for Computer Algebra, Kluwer, 1992
    locator: Chapter 7, Polynomial GCD Computation
---

The polynomial GCD problem asks for the greatest common divisor of two polynomials $f$ and $g$: the common divisor $h$ that every other common divisor divides. Over a field $F$ the gcd is unique once it is made monic, and the [Euclidean algorithm](/polynomial-euclidean-algorithm/) computes it with $O(n^2)$ operations in $F$, or $O(M(n) \log n)$ with the [half-gcd](/half-gcd/) method. Over $\mathbb{Z}$ the arithmetic count hides the real difficulty, the growth of the coefficients, and the methods of choice are the [subresultant](/subresultant-gcd/) and [modular](/brown-modular-gcd/) algorithms. The gcd is the step behind square-free factorization, the simplification of rational functions and the inverses in $F[x]/(m)$.

## In plain words

Two polynomials can share a factor, the way the numbers 12 and 18 share the factor 6. The greatest common divisor is the largest shared factor. With fractions, or with arithmetic modulo a prime, you find it as for whole numbers: divide one by the other, keep the remainder, and repeat with the divisor and the remainder until the remainder is zero. The last divisor is the answer, after you scale it so that its top coefficient is one.

With whole-number coefficients the same method works on paper, but the fractions that appear on the way become very long, even when the answer is one. Good programs avoid this. They compute the answer modulo several primes and put the results together, or they use a careful variant that removes common factors of the coefficients at each step.

## Definition

**Over a field.** Let $F$ be a field and $f, g \in F[x]$. A polynomial $h$ is a *greatest common divisor* of $f$ and $g$ when $h \mid f$, $h \mid g$, and every common divisor of $f$ and $g$ divides $h$.

**Input.** $f, g \in F[x]$, given by their coefficients.

**Output.** The gcd $h = \gcd(f, g)$, normalized to be monic, with $\gcd(0, 0) = 0$.

**Existence and uniqueness.** $F[x]$ is a [Euclidean domain](/euclidean-domain/) with the degree as the size, because [division with remainder](/polynomial-division/) by any nonzero $g$ exists. So the ideal $(f, g) = \{ sf + tg \}$ is principal: if $(f, g) \ne 0$, let $h$ be a nonzero element of least degree in it, and divide $f$ by $h$; the remainder is in the ideal and has degree less than $\deg h$, so it is $0$, and similarly for $g$. Then $h \mid f$, $h \mid g$, and $h = sf + tg$, so every common divisor divides $h$. If $h$ and $h'$ are both gcds, each divides the other, so $h' = c h$ for a unit $c \in F^{\times}$. Exactly one of them is monic. $\square$

**Over a unique factorization domain.** Over $\mathbb{Z}$, or over $R[x]$ for a UFD $R$, the gcd exists by unique factorization and is unique up to a unit; over $\mathbb{Z}$ it is made unique by a positive leading coefficient. By [Gauss's lemma](/gauss-lemma/),

$$\gcd(f, g) = \gcd(\operatorname{cont} f, \operatorname{cont} g) \cdot \gcd(\operatorname{pp} f, \operatorname{pp} g),$$

where $\operatorname{cont}$ and $\operatorname{pp}$ are the content and the [primitive part](/primitive-polynomial/). The gcd over $\mathbb{Q}$ is the gcd over $\mathbb{Z}$ divided by its leading coefficient.

**Cost.** Field operations at unit cost, as in [polynomial ring](/polynomial-ring/), with $M(n)$ the cost of multiplying two polynomials of degree less than $n$. Over $\mathbb{Z}$ the cost is counted in word operations, with the degree and the size of the coefficients as parameters.

## Variants

- **Gcd with cofactors.** Also return $f / h$ and $g / h$, for example to reduce a rational function $f/g$ to lowest terms.
- **Extended gcd.** Return $s, t$ with $sf + tg = h$: the [extended Euclidean algorithm](/polynomial-extended-euclidean-algorithm/). It gives inverses modulo $m$ in $F[x]/(m)$ and Bézout coefficients for [Hensel lifting](/hensel-lifting/).
- **Gcd over $\mathbb{Z}$ or $\mathbb{Q}$.** The same problem with exact integer coefficients, where the bit cost matters.
- **Gcd over a ring that is not a domain.** Over $\mathbb{Z}/n\mathbb{Z}$ with composite $n$, the ring of coefficients has zero divisors, and the Euclidean algorithm can meet a leading coefficient that is not a unit. Then it stops, and the gcd of that coefficient with $n$ is a factor of $n$.
- **Multivariate gcd.** For $f, g \in F[x_1, \ldots, x_k]$, by recursion on the variables, by evaluation and interpolation (Brown), or by sparse interpolation (Zippel; see [Zippel's sparse interpolation](/zippel-sparse-interpolation/)).
- **Many polynomials.** $\gcd(f_1, \ldots, f_k)$ by folding, or by one gcd of $f_1$ with a random linear combination of the others.
- **Decision version.** Is $\gcd(f, g) = 1$? Over a field, with $\operatorname{lc}(f) \ne 0$ and $\operatorname{lc}(g) \ne 0$, this holds exactly when the [resultant](/resultant/) $\operatorname{res}(f, g)$ is nonzero.
- **Approximate gcd.** With floating-point coefficients, find a nearby pair of polynomials with a nontrivial gcd. This is a different, numerical problem.

## Examples

- **Over $\mathbb{Q}$.** $f = x^4 + 2x^3 - x - 2 = (x^3 - 1)(x + 2)$ and $g = x^4 + 3x^3 - x - 3 = (x^3 - 1)(x + 3)$. Then $g - f = x^3 - 1$ is the first remainder, and $f \operatorname{rem} (x^3 - 1) = 0$, so $\gcd(f, g) = x^3 - 1$.
- **Over $\mathbb{F}_2$.** $\gcd(x^4 + x, x^2 + 1) = x + 1$, since $x^4 + x = x(x + 1)(x^2 + x + 1)$ and $x^2 + 1 = (x + 1)^2$.
- **Over $\mathbb{Z}$ and over $\mathbb{Q}$.** For $f = 6x^2 + 12x + 6 = 6(x + 1)^2$ and $g = 4x^2 - 4 = 4(x - 1)(x + 1)$, the gcd in $\mathbb{Z}[x]$ is $2(x + 1) = 2x + 2$, and the monic gcd in $\mathbb{Q}[x]$ is $x + 1$.
- **Coefficient growth.** Knuth's example in Section 4.6.1 takes $f = x^8 + x^6 - 3x^4 - 3x^3 + 8x^2 + 2x - 5$ and $g = 3x^6 + 5x^4 - 4x^2 - 9x + 21$. The remainders over $\mathbb{Q}$ are

$$-\tfrac{5}{9} x^4 + \tfrac{1}{9} x^2 - \tfrac{1}{3}, \qquad -\tfrac{117}{25} x^2 - 9x + \tfrac{441}{25}, \qquad \tfrac{233150}{19773} x - \tfrac{102500}{6591}, \qquad -\tfrac{1288744821}{543589225},$$

so $\gcd(f, g) = 1$, but the last numbers have ten digits although the inputs have one.

## Known algorithms

| algorithm | cost | notes |
|---|---|---|
| [Euclidean algorithm](/polynomial-euclidean-algorithm/) over $F$ | $O(\deg f \cdot \deg g)$ field operations | simple; best for small degrees |
| [Fast Euclidean algorithm](/half-gcd/) (half-gcd) | $O(M(n) \log n)$ field operations | von zur Gathen and Gerhard, Section 11.1 |
| [Primitive PRS](/primitive-prs/) over $\mathbb{Z}$ | polynomial bit cost, with a gcd of the coefficients at each step | the smallest coefficients, the most content computations |
| [Subresultant gcd](/subresultant-gcd/) over a domain | $O(n^2)$ operations in the domain, with exact divisions | coefficients bounded by subresultants, so polynomial size |
| [Modular gcd](/brown-modular-gcd/) (Brown, Collins) | polynomial bit cost; the method of choice in practice | gcds modulo primes, combined by the Chinese remainder theorem; von zur Gathen and Gerhard, Section 6.4 |
| [Heuristic gcd](/heuristic-gcd/) | one integer gcd per trial | evaluates at a large integer; fast for small degrees |

The costs over a field are proved. The ranking of the methods over $\mathbb{Z}$ is observed in practice: modular methods are the default in computer algebra systems, and the heuristic gcd is fast for dense polynomials of moderate degree.

## Bounds

- **Upper bound over a field.** $O(M(n) \log n)$ operations, so $O(n \log^2 n \log\log n)$ over any field and $O(n \log^2 n)$ with FFT-based multiplication.
- **Classical bound.** The Euclidean algorithm on $\deg f = m \ge \deg g = n$ uses at most $(2n + 1)(m + n + 1)$ field operations and $n + 1$ inversions, which is $O(mn)$; the proof is on the page of the [Euclidean algorithm](/polynomial-euclidean-algorithm/), and von zur Gathen and Gerhard, Section 3.3, give a finer count.
- **Coefficient size over $\mathbb{Z}$.** The coefficients of $\gcd(f, g)$ in $\mathbb{Z}[x]$ are bounded through the Mignotte bound on the factors of $f$ (von zur Gathen and Gerhard, Section 6.6), and the subresultants bound those of the intermediate results. So all good methods run in time polynomial in the degree and the bit size of the coefficients.
- **Lower bound.** $\Omega(n)$, since the answer depends on every coefficient.

## Reductions

- **Gcd to division.** The Euclidean algorithm is a sequence of [divisions with remainder](/polynomial-division/).
- **Gcd to linear algebra.** $\deg \gcd(f, g) = \deg f + \deg g - \operatorname{rank} S$, where $S$ is the [Sylvester matrix](/sylvester-matrix/) of $f$ and $g$. In particular $\gcd(f, g) = 1$ exactly when $\operatorname{res}(f, g) = \det S \ne 0$.
- **Lcm from gcd.** $\operatorname{lcm}(f, g) = f g / \gcd(f, g)$, up to a unit; see [least common multiple](/least-common-multiple/).
- **Repeated factors to gcd.** Over a field of characteristic $0$, $f / \gcd(f, f')$ is the [square-free](/square-free-polynomial/) part of $f$.
- **Rational reconstruction and Padé approximation.** Running the extended Euclidean algorithm on $m$ and $u$ and stopping halfway gives a [Padé approximation](/pade-approximation/), and the [Berlekamp-Massey](/berlekamp-massey/) algorithm is the same computation for linear recurrences.

## Applications

- [Square-free factorization](/square-free-factorization/), the first step of every factoring algorithm.
- Root finding and factoring over $\mathbb{F}_q$: $\gcd(f, x^q - x)$ is the product of the distinct linear factors of $f$, and [distinct-degree factorization](/distinct-degree-factorization/) takes $\gcd(f, x^{q^i} - x)$ for $i = 1, 2, \ldots$.
- Inverses in $F[x]/(m)$, so arithmetic in finite fields $\mathbb{F}_{p^k}$.
- Simplification of rational functions in computer algebra, and [partial fraction decomposition](/partial-fraction-decomposition/).
- [Reed-Solomon decoding](/reed-solomon-decoding/) by the extended Euclidean algorithm.
- Testing whether two polynomials share a root, and computing multiple roots.

## References
