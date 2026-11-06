---
tag: TEHDMW
kind: problem
slug: reducing-fractions
name: Reducing fractions to lowest terms
aliases:
- lowest terms
- canonical fraction
area: number-theory/divisibility-and-gcd
level: intro
summary: Divide numerator and denominator of a/b by gcd(a, b).
prereqs: [greatest-common-divisor, coprime-integers]
see_also: [gcd-of-two-integers, euclidean-algorithm, least-common-multiple, gcd-lcm-identity, stern-brocot-tree, continued-fraction, farey-sequence]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.5.1, Fractions (lowest terms, and the rules for the product and the sum of two reduced fractions with small gcds)
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 4.5, Relative Primality (fractions in lowest terms and the Stern-Brocot tree)
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Section 10.5, The representation of an irreducible rational fraction by a simple continued fraction
---

Reducing a fraction $a/b$ to lowest terms means finding the integers $p$ and $q$ with $p/q = a/b$, $q > 0$ and $\gcd(p, q) = 1$. The pair exists and is unique, and it is $p = \operatorname{sign}(b)\, a/g$, $q = |b|/g$ with $g = \gcd(a, b)$. So the cost is one [gcd](/gcd-of-two-integers/) and two exact divisions. Exact rational arithmetic does this after each operation, because it keeps the numbers small, makes equal fractions equal as pairs, and lets fractions be hashed and compared by their parts.

## In plain words

Twelve eighteenths, six ninths and two thirds are the same amount written in different ways. The shortest way is the one where the top and the bottom have no common factor left. To get it, find the largest number that divides both the top and the bottom, and divide both by it. Then make the bottom positive by moving any minus sign to the top. Every fraction has exactly one such shortest form, so two fractions are equal exactly when their shortest forms are the same.

## Definition

**Input.** Integers $a$ and $b$ with $b \ne 0$.

**Output.** The integers $p$ and $q$ with

$$\frac{p}{q} = \frac{a}{b}, \qquad q \ge 1, \qquad \gcd(p, q) = 1.$$

This is the **reduced form** or **lowest terms** of $a/b$. For $a = 0$ it is $0/1$.

**Existence and uniqueness.** Let $g = \gcd(a, b) \ge 1$ and $\sigma = 1$ if $b > 0$, $\sigma = -1$ if $b < 0$. Then $p = \sigma a / g$ and $q = \sigma b / g = |b|/g$ are integers, $q \ge 1$, $p/q = a/b$, and $\gcd(p, q) = \gcd(a/g, b/g) = 1$ (see the [greatest common divisor](/greatest-common-divisor/) page). For uniqueness, let $p/q = p'/q'$ with $q, q' \ge 1$ and $\gcd(p, q) = \gcd(p', q') = 1$. Then $p q' = p' q$, so $q \mid p q'$; since $\gcd(q, p) = 1$, Gauss's lemma gives $q \mid q'$. In the same way $q' \mid q$, and both are positive, so $q = q'$ and then $p = p'$. $\square$

**Cost model.** On the [word RAM](/word-ram/) with word-sized $a$ and $b$, the gcd costs $O(\log \min(|a|, |b|))$ time and the divisions $O(1)$. With arbitrary precision and $n$-bit inputs, the gcd dominates: $O(n^2)$ bit operations with the [Euclidean algorithm](/euclidean-algorithm/) or [Lehmer's GCD](/lehmers-gcd/), $O(M(n) \log n)$ with the [half-GCD](/half-gcd/), and the two exact divisions cost $O(n^2)$ or $O(M(n))$.

## Variants

- **Reduce after an operation.** In rational arithmetic, the inputs are already reduced, which allows smaller gcds. For the product $(u/u')(v/v')$, let $d_1 = \gcd(u, v')$ and $d_2 = \gcd(u', v)$; then $\big((u/d_1)(v/d_2)\big) / \big((u'/d_2)(v'/d_1)\big)$ is already in lowest terms. For the sum $u/u' + v/v'$, let $d_1 = \gcd(u', v')$; if $d_1 = 1$, the result $(uv' + u'v)/(u'v')$ is reduced; otherwise let $t = u(v'/d_1) + v(u'/d_1)$ and $d_2 = \gcd(t, d_1)$, and the result is $(t/d_2)/\big((u'/d_1)(v'/d_2)\big)$. Knuth gives these rules in Section 4.5.1, crediting them to Henrici. The gcds are of smaller numbers than the gcd of the unreduced result.
- **Canonical direction vectors.** In geometry, the slope of the line through two lattice points is reduced to $(\Delta y/g, \Delta x/g)$ with a fixed sign rule, so that equal slopes hash to the same key.
- **Best approximations.** Given a real $x$ and a bound $N$, find the reduced $p/q$ with $q \le N$ closest to $x$. [Continued fractions](/continued-fraction/) and the [Stern-Brocot tree](/stern-brocot-tree/) solve it.
- **Counting reduced fractions.** The number of reduced fractions in $(0, 1]$ with denominator at most $N$ is $\sum_{q \le N} \varphi(q)$, the length of the [Farey sequence](/farey-sequence/) minus one.

## Examples

| $a/b$ | $\gcd(a, b)$ | lowest terms |
| --- | --- | --- |
| $462/1071$ | 21 | $22/51$ |
| $12/18$ | 6 | $2/3$ |
| $-6/-4$ | 2 | $3/2$ |
| $6/-4$ | 2 | $-3/2$ |
| $0/-7$ | 7 | $0/1$ |
| $2^{40}/2^{60}$ | $2^{40}$ | $1/2^{20}$ |
| $832040/1346269$ | 1 | $832040/1346269$ |

The last row is a ratio of consecutive Fibonacci numbers $F_{30}/F_{31}$, which is always in lowest terms. With the rules above, $(3/4)(10/9)$ uses $d_1 = \gcd(3, 9) = 3$ and $d_2 = \gcd(4, 10) = 2$ and gives $(1 \cdot 5)/(2 \cdot 3) = 5/6$; and $1/6 + 1/10$ uses $d_1 = 2$, $t = 1 \cdot 5 + 1 \cdot 3 = 8$, $d_2 = \gcd(8, 2) = 2$, and gives $4/(3 \cdot 5) = 4/15$.

## Known algorithms

- **Divide by the gcd.** Compute $g = \gcd(a, b)$ with any algorithm for the [GCD of two integers](/gcd-of-two-integers/): the [Euclidean algorithm](/euclidean-algorithm/), the [binary GCD](/binary-gcd/), [Lehmer's GCD](/lehmers-gcd/) or the [half-GCD](/half-gcd/). Then divide and fix the sign. The cost is that of the gcd.
- **Henrici's rules** for products and sums of reduced fractions, as above. They replace one gcd of the large result by gcds of the smaller inputs.
- **Through the factorization.** Cancelling common primes works for small hand examples, but [factoring](/integer-factorization/) is far slower than the gcd and is never used for this.

## Bounds

The problem is equivalent to computing the gcd, up to the cost of two exact divisions. In one direction, the algorithm above uses one gcd. In the other, from the reduced form $p/q$ of $a/b$ with $b > 0$, $\gcd(a, b) = b/q$. So the bounds of the [GCD of two integers](/gcd-of-two-integers/) apply: $O(\log \min(|a|, |b|))$ time on the word RAM, and between $\Omega(n)$ and $O(M(n) \log n)$ bit operations for $n$-bit numbers.

## Reductions

- **Gcd to reduction and back**, as in Bounds, with two exact divisions.
- **Equality of fractions.** $a/b = c/d$ if and only if the reduced forms are equal. Without reduction, the test $ad = bc$ also works and needs no gcd, but it doubles the size of the numbers.
- **Least common denominator.** For reduced fractions $p/q$ and $r/s$, the least common denominator is $\operatorname{lcm}(q, s)$; see the [GCD and LCM identity](/gcd-lcm-identity/).

## Applications

- **Exact rational arithmetic.** Python's `fractions.Fraction`, GMP's `mpq_t` and computer algebra systems keep each fraction in lowest terms with a positive denominator.
- **Hashing ratios and slopes.** Counting collinear points or grouping equal ratios uses the reduced pair as a key.
- **Continued fractions and the Stern-Brocot tree.** Each reduced positive fraction has a unique place in the [Stern-Brocot tree](/stern-brocot-tree/), and the Euclidean algorithm on $(p, q)$ produces its [continued fraction](/continued-fraction/).
- **Gear ratios and schedules.** A ratio of tooth counts or of periods is compared and simplified in lowest terms.

## References
