---
tag: EBMDJ7
kind: algorithm
slug: polynomial-euclidean-algorithm
name: Polynomial Euclidean algorithm
aliases:
- Euclid's algorithm for polynomials
- Euclidean algorithm for polynomials
area: algebra/polynomial-arithmetic
level: core
summary: Computes the gcd of two polynomials by repeated remainders; quadratic in the degree over a field.
solves: [polynomial-gcd]
model: blum-shub-smale-machine
complexity:
  vars: {m: the larger of the degrees of f and g, n: the smaller of the degrees of f and g}
  time: {worst: O(m n + m)}
  space: {extra: O(m)}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [polynomial-gcd, polynomial-long-division, euclidean-algorithm]
see_also: [polynomial-extended-euclidean-algorithm, half-gcd, subresultant-gcd, brown-modular-gcd, primitive-prs, euclidean-algorithm, resultant, lames-theorem]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 3.2, The Extended Euclidean Algorithm (p. 47), and Section 3.3, Cost analysis for Z and F[x] (p. 51)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6.1, Division of Polynomials (Euclid's algorithm over a field, its history, and the growth of the coefficients)
  - book: isbn:9780792392590
    title: Keith O. Geddes, Stephen R. Czapor and George Labahn, Algorithms for Computer Algebra, Kluwer, 1992
    locator: Chapter 7, Polynomial GCD Computation (the Euclidean algorithm and polynomial remainder sequences)
---

The polynomial Euclidean algorithm computes the [gcd](/polynomial-gcd/) of two polynomials $f$ and $g$ over a field $F$ by replacing the pair $(f, g)$ with $(g, f \operatorname{rem} g)$ until the second polynomial is zero. The last nonzero remainder, made monic, is the gcd. It is the same method as the [Euclidean algorithm](/euclidean-algorithm/) for integers, with the degree in place of the absolute value. With [long division](/polynomial-long-division/) for each step, it uses at most $(2n + 1)(m + n + 1)$ operations in $F$ for $\deg f = m \ge \deg g = n$, so $O(n^2)$ when $m = O(n)$.

## In plain words

Any polynomial that divides two polynomials also divides the remainder of one by the other, and the other way round. So you can replace the larger one by that remainder without changing the common divisors. The remainder has a smaller degree, so the pair gets smaller at each round.

When the remainder is zero, the last divisor divides the polynomial before it. It is then a divisor of both, and every common divisor divides it. It is the greatest common divisor. Scale it so that its top coefficient is one, and the answer is unique.

The method needs exact division by top coefficients, so the coefficients must come from a field, such as the fractions or the integers modulo a prime.

## The problem

Given a field $F$ and $f, g \in F[x]$, compute the monic $h = \gcd(f, g)$, with $\gcd(0, 0) = 0$. Polynomials are stored as dense coefficient arrays, lowest degree first. See [polynomial GCD](/polynomial-gcd/) for the existence and uniqueness of $h$ and for the problem over $\mathbb{Z}$.

## The algorithm

```pseudo id=main
EUCLID(f, g)                          ▷ f, g in F[x], F a field
L1  r_0 ← f; r_1 ← g, both with zero top coefficients stripped
L2  while r_1 ≠ 0 do
L3      (r_0, r_1) ← (r_1, r_0 rem r_1)   ▷ remainder of long division
L4  if r_0 = 0 then return 0          ▷ only when f = g = 0
L5  u ← lc(r_0)^(−1)
L6  return u · r_0                     ▷ the monic gcd
```

Line L3 uses the remainder part of [long division](/polynomial-long-division/), which needs only that $\operatorname{lc}(r_1)$ is a unit; over a field every nonzero element is one. If $\deg f < \deg g$, the first pass of line L3 only swaps the two polynomials, since then $f \operatorname{rem} g = f$. Lines L5 and L6 normalize the result. Without them, the algorithm returns a gcd that is correct up to a nonzero constant factor.

The sequence $r_0 = f, r_1 = g, r_2, \ldots, r_\ell, r_{\ell+1} = 0$ of the values of $r_1$ is the *remainder sequence* of $f$ and $g$. Its degrees $\deg r_1 > \deg r_2 > \cdots > \deg r_\ell$ strictly decrease.

## Example

Over $\mathbb{Q}$, take $f = x^4 - 1$ and $g = x^3 + 2x^2 + 2x + 1$.

| step | $r_0$ | $r_1$ | quotient | new remainder |
|---|---|---|---|---|
| 1 | $x^4 - 1$ | $x^3 + 2x^2 + 2x + 1$ | $x - 2$ | $2x^2 + 3x + 1$ |
| 2 | $x^3 + 2x^2 + 2x + 1$ | $2x^2 + 3x + 1$ | $\tfrac12 x + \tfrac14$ | $\tfrac34 x + \tfrac34$ |
| 3 | $2x^2 + 3x + 1$ | $\tfrac34 x + \tfrac34$ | $\tfrac83 x + \tfrac43$ | $0$ |

The last nonzero remainder is $\tfrac34 (x + 1)$, so $\gcd(f, g) = x + 1$. This agrees with the factorizations $f = (x - 1)(x + 1)(x^2 + 1)$ and $g = (x + 1)(x^2 + x + 1)$. Over $\mathbb{F}_7$ the same inputs give the remainders $2x^2 + 3x + 1$ and $6x + 6$, and again the gcd $x + 1$.

## Correctness

Two facts give correctness; the full proof is below.

1. **The common divisors do not change.** If $r_2 = r_0 - q r_1$, then a polynomial divides $r_0$ and $r_1$ exactly when it divides $r_1$ and $r_2$. So line L3 keeps the [invariant](/loop-invariant/) that the common divisors of $(r_0, r_1)$ are the common divisors of $(f, g)$.
2. **The loop stops.** Each pass of line L3 replaces $\deg r_1$ by a smaller degree, or by $-\infty$ when the remainder is $0$. A strictly decreasing sequence of degrees $\ge 0$ is finite.

When the loop stops, $r_1 = 0$, and the common divisors of $(r_0, 0)$ are the divisors of $r_0$. So $r_0$ is a common divisor of $f$ and $g$ that every common divisor divides, and lines L5 and L6 make it monic.

## Complexity

The cost counts field operations at unit cost, as in [polynomial ring](/polynomial-ring/). Let $n_0 = m = \deg f \ge n_1 = n = \deg g \ge 0$ and $n_i = \deg r_i$.

- **Number of divisions.** The degrees $n_1 > n_2 > \cdots > n_\ell \ge 0$ are distinct, so $\ell \le n + 1$.
- **Cost of the divisions.** Dividing $r_{i-1}$ by $r_i$ costs at most $(2n_i + 1)(n_{i-1} - n_i + 1)$ operations and one inversion (see [long division](/polynomial-long-division/)). Since $n_i \le n$ and the sum telescopes,

$$\sum_{i=1}^{\ell} (2 n_i + 1)(n_{i-1} - n_i + 1) \le (2n + 1)\,(m - n_\ell + \ell) \le (2n + 1)(m + n + 1).$$

- **Normalization.** $n_\ell + 1 \le n + 1$ multiplications and one inversion.
- **Total.** At most $(2n + 1)(m + n + 1) + n + 1$ operations and $n + 2$ inversions, which is $O(mn + m)$. In the *normal* case, where every degree after the first drops by exactly one, the first division costs about $2n(m - n)$ and each later one about $4 n_i$, which sums to about $2n(m - n) + 2n^2 = 2mn$ operations. Von zur Gathen and Gerhard (Section 3.3) count the extended version in detail.
- **Space.** $O(m)$ for the two current remainders.
- **Over $\mathbb{Q}$.** The count above is the number of operations on fractions, not their bit cost. The fractions in the remainder sequence can grow fast, as in Knuth's example on the [polynomial GCD](/polynomial-gcd/) page, where one-digit inputs give a ten-digit last remainder. For $\mathbb{Z}[x]$ and $\mathbb{Q}[x]$ use the [subresultant](/subresultant-gcd/) or [modular](/brown-modular-gcd/) algorithm.

The operation counts are proved. The relative speed of this algorithm, the half-gcd and the modular methods on real inputs is observed by measurement.

## Properties

- **Deterministic and exact** over any field with exact arithmetic.
- **The remainder sequence is unique.** Over a field, the remainders $r_i$ are determined by $f$ and $g$, because each remainder is unique. Variants that scale the $r_i$ differ only by constant factors.
- **Degrees of the remainders.** The degrees $n_2, \ldots, n_\ell$ are the indices $j < n$ at which the $j$-th [subresultant](/subresultant/) of $f$ and $g$ is nonzero (von zur Gathen and Gerhard, Section 11.2). This links the algorithm to the [resultant](/resultant/).
- **Not in place.** It needs a copy of the two current remainders; the quotients are not stored.

## Variants and improvements

- **Extended Euclidean algorithm.** Keep $s_i, t_i$ with $s_i f + t_i g = r_i$: the [extended Euclidean algorithm](/polynomial-extended-euclidean-algorithm/), which gives Bézout coefficients and inverses modulo a polynomial.
- **Monic remainders.** Make each $r_i$ monic. This changes the $r_i$ only by constants and keeps the numbers smaller in some cases; von zur Gathen and Gerhard use this normalization in Section 3.2.
- **Fast Euclidean algorithm.** Compute the quotients from the top coefficients only, by divide and conquer, in $O(M(n) \log n)$ operations: [half-gcd](/half-gcd/), von zur Gathen and Gerhard, Section 11.1.
- **Over an integral domain.** Replace the remainder by the [pseudo-remainder](/pseudo-division/) and remove a known factor at each step: the [primitive PRS](/primitive-prs/) and the [subresultant PRS](/subresultant-prs/) avoid fractions.
- **Modular gcd.** Run the algorithm over $\mathbb{F}_p$ for several primes and combine: [Brown's modular gcd](/brown-modular-gcd/).

## When to use it

Use it over finite fields and other fields with constant-cost arithmetic, for degrees up to a few hundred, where its simple loop beats the half-gcd. Use it as the base case of the half-gcd. Do not use it over $\mathbb{Q}$ for large inputs: the intermediate fractions grow, and a modular or subresultant method is much faster in practice.

## Pitfalls

- **Zero top coefficients.** A remainder computed in place can keep zero top coefficients. Then its "leading coefficient" is $0$ and the next division fails. Strip after each remainder.
- **Integer coefficients.** Over $\mathbb{Z}$, the division in line L3 is not defined unless the leading coefficient is $\pm 1$. Convert to $\mathbb{Q}$, or use pseudo-division.
- **Floating-point coefficients.** A remainder that should be $0$ comes out as a tiny nonzero polynomial, and the algorithm returns $1$ for polynomials with a common root. The exact gcd is not continuous in the coefficients; an approximate gcd needs a different, numerical method.
- **Forgetting the normalization.** Without lines L5 and L6, the result is correct only up to a constant, and two runs on scaled inputs give different answers.
- **The case $f = g = 0$.** There is no leading coefficient to invert. Return $0$.

## Implementations

## History

Knuth, Section 4.6.1, credits Simon Stevin with the first use of Euclid's algorithm for polynomials, in 1585. The growth of the coefficients over $\mathbb{Q}$ led to the polynomial remainder sequences of Collins and of Brown and Traub in the 1960s and 1970s, which Knuth also describes in Section 4.6.1.

## References
