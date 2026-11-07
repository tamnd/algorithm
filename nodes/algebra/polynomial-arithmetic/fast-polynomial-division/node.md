---
tag: X5VM5A
kind: algorithm
slug: fast-polynomial-division
name: Fast polynomial division
aliases:
- Newton division of polynomials
- division with remainder by Newton iteration
area: algebra/polynomial-arithmetic
level: advanced
summary: Computes the quotient by inverting the reversed divisor with Newton iteration, in multiplication time.
solves: [polynomial-division]
model: blum-shub-smale-machine
complexity:
  vars: {n: the degree of the dividend a, m: the degree of the divisor b, M: the cost function M(n) of multiplying two polynomials of degree less than n}
  time: {worst: O(M(n)), best: O(M(n))}
  space: {extra: O(n)}
  ring_operations: {worst: 4M(n - m + 1) + M(m) + o(M(n)) + O(n)}
properties: {deterministic: true, in_place: false, recursive: false, online: false}
history:
  year: 1972
  people: [Malte Sieveking, Robert T. Moenck, Allan Borodin, Volker Strassen]
  note: Newton inversion of power series (Sieveking 1972, Kung 1974) gave division with remainder of polynomials in O(M(n)) ring operations, used by Moenck and Borodin and by Strassen for fast evaluation and interpolation.
prereqs: [newton-power-series-inversion, dense-polynomial-representation, newton-iteration]
see_also: [polynomial-division, polynomial-long-division, pseudo-division, power-series-inversion, fft-polynomial-multiplication, fast-multipoint-evaluation, newton-raphson-division, barrett-reduction]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 9.1, Division with remainder using Newton iteration
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 4.2.4, Newton's method for formal power series; Section 2.4.1, Barrett's algorithm (the integer analogue with a precomputed inverse)
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition, Cambridge University Press, 2009
    locator: Section 17.6, Faster polynomial arithmetic
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.6.1, Division of polynomials (the schoolbook algorithm that this one replaces)
---

Fast polynomial division computes the quotient and remainder of $a$ divided by $b$ with a constant number of polynomial multiplications. It reverses the coefficient lists, so that the quotient becomes a truncated power series, and gets it from one [Newton inversion](/newton-power-series-inversion/) of the reversed divisor and one product. The remainder then costs one more product. With FFT multiplication this divides in $O(n \log n)$ ring operations instead of the $\Theta((n - m + 1) m)$ of [long division](/polynomial-long-division/).

Notation: $R$ is a commutative ring with $1$, a polynomial is the list of its coefficients with the constant term first, $n = \deg a$, $m = \deg b$, and $M(k)$ is the cost of multiplying two polynomials of degree less than $k$ over $R$. We assume that $M(k)/k$ is nondecreasing and that multiplying a polynomial with $k$ coefficients by one with at most $k$ coefficients costs at most $M(k)$. Costs count ring operations of $R$ in the algebraic complexity model. $R$ need not be a field, but the leading coefficient of $b$ must be a unit.

## In plain words

Long division of polynomials works from the top coefficient down and costs about the product of the two degrees. The fast method turns the polynomials upside down by reading their coefficients in reverse order. After this turn, the quotient is the first few terms of a fraction of two power series. The reciprocal of the turned divisor comes from Newton's method, which costs about three multiplications. One more multiplication gives the turned quotient, and turning it back gives the quotient. The remainder is the dividend minus the quotient times the divisor, and only its low part is needed, which costs one small multiplication. So division is as fast as multiplication, up to a small constant factor.

## The problem

**Input:** polynomials $a, b \in R[x]$ with $b \ne 0$ and $\operatorname{lc}(b)$ a unit of $R$.

**Output:** the unique $q, r \in R[x]$ with $a = qb + r$ and $\deg r < \deg b$ (where $\deg 0 = -\infty$).

This is the problem of [polynomial division](/polynomial-division/). Existence and uniqueness need only that $\operatorname{lc}(b)$ is a unit: if $qb + r = q'b + r'$, then $(q - q')b = r' - r$, and since $\operatorname{lc}(b)$ is not a zero divisor, the left side has degree at least $m$ unless $q = q'$. When $\operatorname{lc}(b)$ is not a unit, as for $2x + 1$ over $\mathbb{Z}$, use [pseudo-division](/pseudo-division/) or work over the fraction field.

## The algorithm

For a polynomial $f$ of degree at most $k$, the reversal is $\operatorname{rev}_k(f) = x^k f(1/x)$: the same coefficients in the opposite order. Substitute $1/x$ in $a = qb + r$ and multiply by $x^n$:

$$\operatorname{rev}_n(a) = \operatorname{rev}_{n-m}(q)\, \operatorname{rev}_m(b) + x^{n-m+1} \operatorname{rev}_{m-1}(r).$$

The constant term of $\operatorname{rev}_m(b)$ is $\operatorname{lc}(b)$, a unit, so $\operatorname{rev}_m(b)$ is invertible modulo $x^k$ for $k = n - m + 1$, and

$$\operatorname{rev}_{n-m}(q) \equiv \operatorname{rev}_n(a)\, \operatorname{rev}_m(b)^{-1} \pmod{x^{n-m+1}}.$$

Since $\deg q = n - m$, the left side has fewer than $k$ coefficients, so this congruence determines $q$. The remainder is $r = a - qb$, and because $\deg r < m$ it is enough to compute $a - qb$ modulo $x^m$.

```pseudo id=main
FAST-DIVMOD(a, b)                    ▷ b ≠ 0, lc(b) a unit
L1  remove zero entries at the top of a and b; n ← deg a, m ← deg b
L2  if n < m then return (0, a)
L3  k ← n − m + 1
L4  h ← NEWTON-INVERSE(rev_m(b), k)       ▷ rev_m(b) · h ≡ 1 mod x^k
L5  s ← rev_n(a) mod x^k
L6  t ← s · h mod x^k                      ▷ t = rev_{n−m}(q)
L7  q ← rev_{n−m}(t)
L8  u ← q · b mod x^m                      ▷ only the low m coefficients
L9  r ← (a mod x^m) − u
L10 return (q, r)
```

NEWTON-INVERSE is the algorithm of [Newton power series inversion](/newton-power-series-inversion/). Line L1 matters: the reversal uses the true degree, so zero entries at the top of the input lists must go first. Lines L5 and L6 use only the top $k$ coefficients of $a$; the lower ones enter only through line L9. If $m = 0$, then $b$ is a unit constant, the remainder is $0$, and lines L8 and L9 are skipped.

When many dividends share one divisor $b$, as in [fast multipoint evaluation](/fast-multipoint-evaluation/) or in arithmetic modulo $b$, line L4 is done once, for the largest $k$ needed, and the rest costs two products per division. The implementation accepts such a precomputed inverse.

## Example

Divide $a = x^5 + 2x^4 + 3x^3 + 4x^2 + 5x + 6$ by $b = x^2 + x + 1$ over $\mathbb{Z}$. Here $n = 5$, $m = 2$, $k = 4$, and the lists are $a = [6, 5, 4, 3, 2, 1]$ and $b = [1, 1, 1]$.

**Line L4.** $\operatorname{rev}_2(b) = 1 + x + x^2$. The Newton inversion climbs the precisions $1, 2, 4$:

| precision | $d = \operatorname{rev}(b) \cdot g \bmod x^{m'}$ | correction | $g$ |
|---|---|---|---|
| 1 | | | $[1]$ |
| 2 | $[1, 1]$ | $[-1]$ | $[1, -1]$ |
| 4 | $[1, 0, 0, -1]$ | $[0, 1]$ | $[1, -1, 0, 1]$ |

So $h = 1 - x + x^3$. Check: $(1 + x + x^2)(1 - x + x^3) = 1 + x^4 + x^5 \equiv 1 \pmod{x^4}$.

**Lines L5 to L7.** $\operatorname{rev}_5(a) = [1, 2, 3, 4, 5, 6]$, so $s = [1, 2, 3, 4]$. The product $s \cdot h$ modulo $x^4$ is $[1, 2 - 1, 3 - 2, 4 - 3 + 1] = [1, 1, 1, 2]$. Reversed, $q = [2, 1, 1, 1]$, that is $q = x^3 + x^2 + x + 2$.

**Lines L8 and L9.** $q \cdot b \bmod x^2 = [2, 1] \cdot [1, 1] \bmod x^2 = [2, 3]$, and $r = [6 - 2, 5 - 3] = [4, 2]$, that is $r = 2x + 4$.

Check: $(x^3 + x^2 + x + 2)(x^2 + x + 1) + 2x + 4 = x^5 + 2x^4 + 3x^3 + 4x^2 + 5x + 6$. A script confirms the table and the result.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). In short: the reversal identity above holds because each term of $a = qb + r$ is multiplied by $x^n$ after the substitution $x \mapsto 1/x$, and $x^n r(1/x) = x^{n-m+1} \cdot x^{m-1} r(1/x)$ with $\deg r \le m - 1$. Reducing modulo $x^k$ removes the remainder term. The inverse from line L4 is correct by the correctness theorem of Newton inversion, so line L6 gives $\operatorname{rev}_{n-m}(q)$ exactly, because both sides have fewer than $k$ coefficients. For the remainder, $a - qb$ has degree less than $m$, so it equals its reduction modulo $x^m$, which lines L8 and L9 compute.

## Complexity

All bounds count ring operations in the algebraic complexity model and are proved under the assumptions on $M$ stated above. Let $k = n - m + 1$.

- **Line L4.** Newton inversion to precision $k$ costs at most $3M(k) + 2\lceil \log_2 k \rceil M(k)/k + O(k)$, plus one inversion of $\operatorname{lc}(b)$.
- **Line L6.** Two polynomials with $k$ coefficients: at most $M(k)$.
- **Line L8.** At most $\min(k, m)$ by $m$ coefficients, only the low $m$ coefficients kept: at most $M(m)$.
- **Lines L1, L5, L7 and L9.** $O(n)$.

So the total is at most $4M(n - m + 1) + M(m) + o(M(n)) + O(n)$, and at most $M(n - m + 1) + M(m) + O(n)$ when the inverse is precomputed. Since $M(k)/k$ is nondecreasing, $M(k) + M(m) \le M(k + m) = M(n + 1)$, so the total is at most $4M(n + 1) + o(M(n)) + O(n)$, which is $O(M(n))$. Von zur Gathen and Gerhard, Section 9.1, prove a bound of the same form.

**Space.** $O(n)$ ring elements, plus the space of the multiplication.

| multiplication | $M(n)$ | division of degree $2m$ by degree $m$ |
|---|---|---|
| schoolbook | $\Theta(n^2)$ | $\Theta(m^2)$; long division has the same order and a smaller constant |
| Karatsuba | $O(n^{\log_2 3})$ | $O(m^{\log_2 3})$ |
| FFT over a ring with suitable roots of unity | $O(n \log n)$ | $O(m \log m)$ |

**In practice (observed).** Long division costs about $(n - m + 1)(m + 1)$ multiplications and as many additions, with very small overhead. The fast method wins only when both $n - m$ and $m$ are large. If $n - m$ is small, long division is linear in $m$ and is the better choice. If $m$ is small, long division is linear in $n$. Crossover sizes depend on the ring, the multiplication used and the machine; libraries such as NTL and FLINT switch from long division to Newton division above a threshold tuned for each ring.

## Properties

- **Exact.** No rounding: over $\mathbb{Z}$ with a divisor whose leading coefficient is $\pm 1$, and over $\mathbb{Z}/m\mathbb{Z}$ or $\mathbb{Q}$, the result equals that of long division.
- **Only one inversion in $R$.** The only division in $R$ is the inverse of $\operatorname{lc}(b)$, at the start of the Newton inversion.
- **Reusable precomputation.** The inverse of $\operatorname{rev}_m(b)$ modulo $x^k$ serves every dividend of degree less than $m + k$.
- **Generic in the multiplication.** Any multiplication algorithm can be used; the bound follows that of the multiplication.
- **Not in place.** It needs $O(n)$ extra ring elements.

## Variants and improvements

- **Quotient only, or remainder only.** If only $q$ is needed, skip lines L8 and L9. If only $r$ is needed and $b$ is fixed, precompute the inverse; then each remainder costs $M(k) + M(m) + O(n)$.
- **Barrett-style reduction modulo $b$.** For arithmetic in $R[x]/(b)$, products have degree at most $2m - 2$, so $k = m - 1$, and one precomputed inverse of length $m - 1$ serves all reductions. This is the polynomial form of [Barrett reduction](/barrett-reduction/).
- **Middle product and transform reuse.** With FFT multiplication, the transform of $b$ and of the precomputed inverse can be stored, and line L8 can be replaced by a cyclic product of any length $N \ge m$, because $r = (a - qb) \bmod (x^N - 1)$ when $\deg r < N$. Brent and Zimmermann discuss such savings for the integer case.
- **Unbalanced divisions.** When $n$ is much larger than $2m$, split $a$ into blocks of $m$ coefficients and divide block by block from the top, with one precomputed inverse of length $m$; this costs $O((n/m) M(m))$.
- **Integers.** The same reversal idea gives fast [integer division](/integer-division/) by [Newton-Raphson division](/newton-raphson-division/), but there carries require a correction step at the end.

## When to use it

Use fast division when the divisor and the quotient both have large degree and a fast multiplication is available, for example inside [fast multipoint evaluation](/fast-multipoint-evaluation/) and [fast interpolation](/fast-interpolation/), the half-gcd algorithm, and repeated reduction modulo a fixed polynomial (modular exponentiation in $R[x]/(b)$, as in [distinct-degree factorization](/distinct-degree-factorization/)). For small degrees, or when one of $n - m$ and $m$ is small, use [long division](/polynomial-long-division/). When the leading coefficient of $b$ is not a unit, use [pseudo-division](/pseudo-division/).

## Pitfalls

- **Reversal with the wrong degree.** If the input list of $a$ or $b$ has zero entries at the top, reversing the list without removing them uses the wrong degree and gives a wrong quotient. Normalize first.
- **A leading coefficient that is not a unit.** Over $\mathbb{Z}$, $b = 2x + 1$ has no inverse of $\operatorname{rev}(b)$ with integer coefficients. The implementation raises an error.
- **The wrong precision.** The quotient needs precision $n - m + 1$, not $n$ or $n + 1$. Inverting to precision $n$ is correct but wastes work, which is large when $m$ is close to $n$.
- **Full product for the remainder.** Computing $qb$ in full costs $M(n)$; only the low $m$ coefficients are needed.
- **A short precomputed inverse.** An inverse computed for a smaller $k$ gives a wrong quotient without any error. The implementation checks the length.

## Implementations

## History

The reversal identity and Newton inversion together reduce division with remainder to multiplication. Sieveking in 1972 and Kung in 1974 showed that the reciprocal of a power series costs a constant times one multiplication. Moenck and Borodin, and Strassen, used division in $O(M(n))$ operations as the basic step of fast evaluation at many points, fast interpolation and fast Chinese remaindering in the early 1970s. The standard textbook treatment, with the reversal and the bound used on this page, is in von zur Gathen and Gerhard, Section 9.1.

## References
