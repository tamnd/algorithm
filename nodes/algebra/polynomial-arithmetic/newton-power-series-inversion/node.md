---
tag: 8P4715
kind: algorithm
slug: newton-power-series-inversion
name: Newton power series inversion
aliases:
- power series reciprocal by Newton iteration
- Sieveking-Kung algorithm
area: algebra/polynomial-arithmetic
level: advanced
summary: Inverts a power series by the iteration g <- g(2 - fg) that doubles the precision each step.
solves: [power-series-inversion]
model: blum-shub-smale-machine
complexity:
  vars: {n: the number of coefficients of the inverse that are computed, M: the cost function M(n) of multiplying two polynomials of degree less than n}
  time: {worst: O(M(n)), best: O(M(n))}
  space: {extra: O(n)}
  ring_operations: {worst: 3M(n) + o(M(n))}
properties: {deterministic: true, in_place: false, recursive: false, online: false}
history:
  year: 1972
  people: [Malte Sieveking, H. T. Kung]
  note: Sieveking (1972) and Kung (1974) showed that the reciprocal of a power series costs a constant times one multiplication, using Newton iteration.
prereqs: [newton-iteration, dense-polynomial-representation, fft-polynomial-multiplication]
see_also: [fast-polynomial-division, power-series-inversion, newton-raphson-division, karatsuba-multiplication, linear-recurrence-nth-term, bostan-mori-algorithm, hensel-lifting, polynomial-multiplication]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 9.1, Division with remainder using Newton iteration (inversion of power series by Newton iteration and its cost of 3M(n) + O(n))
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 4.2.4, Newton's method for formal power series; Section 3.3.2, The middle product
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition, Cambridge University Press, 2009
    locator: Section 17.6, Faster polynomial arithmetic (inverting power series by Newton iteration, used for fast division with remainder)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.7, Manipulation of power series
---

Newton power series inversion computes the first $n$ coefficients of $1/f$ for a power series $f$ whose constant term is a unit. It starts from $g = 1/f_0$ and applies the step $g \leftarrow g(2 - fg)$, which doubles the number of correct coefficients each time. With a fast multiplication the total cost is at most about three multiplications of size $n$, so inversion, and with it [division with remainder](/fast-polynomial-division/), is as fast as multiplication up to a constant factor.

Notation: $R$ is a commutative ring with $1$, power series are lists of coefficients with the constant term first, and $M(n)$ is the cost of multiplying two polynomials of degree less than $n$ over $R$. We assume $M(n)/n$ is nondecreasing. Costs count ring operations of $R$ in the algebraic complexity model.

## In plain words

The reciprocal of a power series is the series that multiplies with it to give exactly 1. The coefficients can be found one at a time, but that costs a number of steps that grows with the square of the number of coefficients. Newton's method finds them faster. Start with the reciprocal of the first coefficient, which is correct to one term. Multiply the series by the guess and look at how far the product is from 1. Use this error to correct the guess. The correction makes the guess right to twice as many terms. After about log n rounds, all n terms are right, and the last round does most of the work.

## The problem

**Input:** a list $f = [f_0, f_1, \ldots]$ of elements of $R$ with $f_0$ a unit of $R$, and an integer $n \ge 0$.

**Output:** the list $[g_0, \ldots, g_{n-1}]$ such that $f g \equiv 1 \pmod{x^n}$, where $f = \sum_k f_k x^k$ and $g = \sum_{k<n} g_k x^k$.

The inverse exists and is unique modulo $x^n$ exactly when $f_0$ is a unit: the coefficient of $x^0$ in $fg$ is $f_0 g_0$, and for $k \ge 1$ the coefficient of $x^k$ gives $g_k = -f_0^{-1} \sum_{j=1}^{k} f_j g_{k-j}$, the naive recurrence with $\Theta(n^2)$ operations. This is the problem [power series inversion](/power-series-inversion/).

## The algorithm

Let $k_0 = n$ and $k_{i+1} = \lceil k_i / 2 \rceil$ until $k_s = 1$. The algorithm climbs the precisions $1 = k_s < k_{s-1} < \cdots < k_0 = n$. At precision $m$ it keeps $g$ with $fg \equiv 1 \pmod{x^m}$. To go to precision $m' \le 2m$ it computes the error $e = 1 - fg$, which is divisible by $x^m$, and adds $g e$. Since $e$ starts at $x^m$, only its coefficients $m$ to $m' - 1$ are needed, and only the coefficients $0$ to $m' - m - 1$ of the correction $g \cdot (e / x^m)$.

```pseudo id=main
NEWTON-INVERSE(f, n)                       ▷ f_0 a unit, n ≥ 1
L1  g ← [f_0^{−1}]
L2  m ← 1
L3  for m' in PRECISIONS(n) after the first entry do   ▷ m < m' ≤ 2m
L4      d ← (f mod x^{m'}) · g  mod x^{m'}             ▷ d ≡ 1 mod x^m
L5      t ← −(d_m + d_{m+1} x + ⋯ + d_{m'−1} x^{m'−m−1})
L6      c ← g · t  mod x^{m'−m}
L7      g ← g + x^m · c;  m ← m'
L8  return g
```

PRECISIONS$(n)$ is the list $1 = k_s, k_{s-1}, \ldots, k_0 = n$ defined above. For $n = 8$ it is $1, 2, 4, 8$, and for $n = 5$ it is $1, 2, 3, 5$. Computing the list from the top avoids a last step that overshoots $n$ by almost a factor of 2.

Lines L4 to L7 are the Newton step $g \leftarrow g + g(1 - fg) = g(2 - fg)$ written so that no multiplication produces coefficients that are known in advance. The products in lines L4 and L6 can use any multiplication algorithm; the implementation passes it as a parameter and uses Karatsuba multiplication by default.

## Example

Invert $f = 1 - x - x^2$ over $\mathbb{Z}$ to precision $n = 8$. The precisions are $1, 2, 4, 8$.

| line | $m \to m'$ | $d = fg \bmod x^{m'}$ | $t$ | $c = gt \bmod x^{m'-m}$ | new $g$ |
|---|---|---|---|---|---|
| L1 | $1$ | | | | $[1]$ |
| L4 to L7 | $1 \to 2$ | $[1, -1]$ | $[1]$ | $[1]$ | $[1, 1]$ |
| L4 to L7 | $2 \to 4$ | $[1, 0, -2, -1]$ | $[2, 1]$ | $[2, 3]$ | $[1, 1, 2, 3]$ |
| L4 to L7 | $4 \to 8$ | $[1, 0, 0, 0, -5, -3, 0, 0]$ | $[5, 3, 0, 0]$ | $[5, 8, 13, 21]$ | $[1, 1, 2, 3, 5, 8, 13, 21]$ |

At each step the first $m$ entries of $d$ are $1, 0, \ldots, 0$, as the invariant says, and the next entries are the error. The result is the Fibonacci numbers, since $1/(1 - x - x^2) = \sum_k F_{k+1} x^k$. The test file checks this result, the precision lists, and the identity $fg \equiv 1 \pmod{x^n}$ for random inputs.

## Correctness

**Invariant.** At the start of each iteration of line L3, with the current $m$, $g$ has $m$ coefficients and $fg \equiv 1 \pmod{x^m}$.

*Initialization.* After line L1, $f g \equiv f_0 f_0^{-1} = 1 \pmod x$, and $m = 1$.

*Maintenance.* Let $m < m' \le 2m$; this holds because $m = \lceil m'/2 \rceil$. Let $e = 1 - fg \bmod x^{m'}$. By the invariant, $e = x^m \tilde e$ with $\tilde e = t$ from line L5, since $d = 1 - e$. The new $g$ is $g_{\text{new}} = g + x^m (g t \bmod x^{m'-m}) \equiv g + g e \pmod{x^{m'}}$. Then

$$1 - f g_{\text{new}} \equiv 1 - fg(1 + e) = (1 - fg) - fg\, e \equiv e - (1 - e) e = e^2 \pmod{x^{m'}}.$$

Since $e^2$ is divisible by $x^{2m}$ and $2m \ge m'$, $f g_{\text{new}} \equiv 1 \pmod{x^{m'}}$.

*Termination.* The last precision is $n$, so line L8 returns $g$ with $fg \equiv 1 \pmod{x^n}$, and by uniqueness it is the inverse. The full proof, with the precision list and the cost bound, is in the proof file.

## Complexity

All bounds count ring operations in the algebraic complexity model and are proved, assuming $M(n)/n$ is nondecreasing.

**One step.** For the step from $m$ to $m'$, line L4 multiplies a polynomial with $m'$ coefficients by one with $m$ coefficients, at most $M(m')$. Line L6 multiplies $m$ by $m' - m \le m$ coefficients, at most $M(m)$, and we only need the low $m' - m$ coefficients of the result. Lines L5 and L7 cost $O(m')$.

**Total.** By induction, $k_i \le n/2^i + 1$, since $\lceil k/2 \rceil \le (k + 1)/2$. With $M(k) \le (k/n) M(n)$ for $k \le n$,

$$\sum_{i<s} M(k_i) \le \frac{M(n)}{n} \sum_{i<s} \Bigl(\frac{n}{2^i} + 1\Bigr) \le 2M(n) + s\, \frac{M(n)}{n},$$

and the products of line L6 add at most half of this. With $s = \lceil \log_2 n \rceil$ the total is at most $3M(n) + O(M(n) \log n / n) + O(n)$, that is $3M(n) + o(M(n))$ for every multiplication with $M(n) = O(n^{1+\epsilon})$. This is the bound of von zur Gathen and Gerhard, Section 9.1.

**Space.** $O(n)$ ring elements for $g$, $d$, $t$ and $c$, plus the space of the multiplication.

| multiplication | $M(n)$ | inversion to precision $n$ |
|---|---|---|
| schoolbook | $\Theta(n^2)$ | $\Theta(n^2)$; the naive recurrence is simpler and about as fast |
| Karatsuba | $O(n^{\log_2 3})$ | $O(n^{\log_2 3})$ |
| FFT over a ring with suitable roots of unity | $O(n \log n)$ | $O(n \log n)$ |
| Cantor-Kaltofen, any ring | $O(n \log n \log\log n)$ | $O(n \log n \log\log n)$ |

**In practice (observed).** With FFT multiplication, implementations reuse the transform of $g$ in lines L4 and L6, and use the fact that the low half of $d$ is known, which is the middle product of Brent and Zimmermann, Section 3.3.2. This lowers the cost to roughly $2M(n)$ or less. Below some size, which depends on the ring and the machine and is in the tens to hundreds of coefficients, the naive $\Theta(n^2)$ recurrence is faster.

## Properties

- **Exact.** No rounding: over $\mathbb{Z}$, $\mathbb{Z}/m\mathbb{Z}$ or $\mathbb{Q}$ the result is the exact inverse.
- **Integer inputs stay integer.** Over $\mathbb{Z}$ with $f_0 = \pm 1$, every intermediate value is an integer. No division is used except $f_0^{-1}$.
- **Prefix stable.** The first $m$ coefficients never change after they are computed, so the result for precision $n$ is a prefix of the result for every larger precision.
- **Self-correcting.** If $g$ is wrong at precision $m$ but right at precision $\lceil m/2 \rceil$, one step still gives the correct result at precision $m$. This is how the inverse is refreshed inside other Newton iterations.
- **Not online.** Computing $g_k$ needs $f_0, \ldots, f_k$ only, but the algorithm computes blocks of coefficients at a time; for coefficient-by-coefficient output, use relaxed (online) multiplication instead.

## Variants and improvements

- **Division of series.** $a/f \bmod x^n$ is $a$ times the inverse. Karp and Markstein's trick folds the last multiplication by $a$ into the last Newton step, which saves about one product.
- **Polynomial division.** For $a = qb + r$, the reversed quotient is the reversed $a$ times the inverse of the reversed $b$ modulo $x^{\deg a - \deg b + 1}$. This is [fast polynomial division](/fast-polynomial-division/).
- **Higher order steps.** With $e = 1 - fg$, the step $g \leftarrow g(1 + e + e^2)$ triples the precision, since $1 - fg(1 + e + e^2) = e^3$.
- **Middle product.** Line L4 only needs coefficients $m$ to $m' - 1$ of $fg$. The transposed form of multiplication computes exactly these at about the cost of one product of size $m$, not $m'$.
- **Over $\mathbb{Z}$ and $\mathbb{Q}$.** If $f_0$ is not $\pm 1$, the inverse has denominators that are powers of $f_0$. One can work modulo a prime $p$ or modulo $p^k$ and lift, or compute $f_0^{n} / f$ over $\mathbb{Z}$ to keep integers.
- **Integers and reals.** The same step $y \leftarrow y(2 - ay)$ gives reciprocals of integers and of floating point numbers ([Newton-Raphson division](/newton-raphson-division/)), but there the precision is in digits and rounding must be handled.

## When to use it

Use Newton inversion when the precision $n$ is large enough that fast multiplication beats the schoolbook product, and as the inner step of fast division, of fast [multipoint evaluation](/fast-multipoint-evaluation/) and [interpolation](/fast-interpolation/), and of logarithms and exponentials of power series. For small $n$, or when only schoolbook multiplication is available, the naive recurrence is as fast and simpler. For linear recurrences with constant coefficients, where the inverse of a fixed polynomial is wanted at one far index, use [Bostan-Mori](/bostan-mori-algorithm/) instead.

## Pitfalls

- **A constant term that is not a unit.** Over $\mathbb{Z}$, $1/(2 + x)$ is not a power series with integer coefficients. The implementation raises an error instead of returning floats or wrong integers.
- **Using the full product.** Computing $g(2 - fg)$ with full products of length $2m'$ and truncating at the end doubles the cost and gives no extra precision.
- **Precisions that double from 1.** For $n = 2^k + 1$, doubling from $1$ ends at precision $2^{k+1}$, almost twice $n$, and the last step costs almost twice as much as needed. Use the list $\lceil n/2^i \rceil$.
- **Floating point coefficients.** Over $\mathbb{R}$, errors can grow with each step when $f$ has a root of small modulus, because the inverse then has coefficients that grow geometrically.
- **Zero entries at the top of the input.** The input list is a series truncated at some point; trailing zeros are valid and change nothing. A normalization routine for polynomials is not needed here, but it must not reject a list like $[1, 2, 0, 0]$.

## Implementations

## History

The step $g \leftarrow g(2 - fg)$ is Newton's method for $1/g - f = 0$, used for reciprocals of numbers on early computers without a divide instruction. Sieveking in 1972 and Kung in 1974 showed that it gives the reciprocal of a power series at a constant times the cost of one multiplication, which made fast division of polynomials possible. Moenck and Borodin, and later Strassen, used this in fast algorithms for division, evaluation and interpolation in the 1970s. The precise constant $3M(n)$ is the standard textbook bound in von zur Gathen and Gerhard, and Brent and Zimmermann and later work on the middle product reduced the constant for FFT-based multiplication.

## References
