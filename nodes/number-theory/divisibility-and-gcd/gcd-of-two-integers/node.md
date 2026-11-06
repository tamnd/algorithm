---
tag: 5P4E29
kind: problem
slug: gcd-of-two-integers
name: GCD of two integers
aliases:
- two-number GCD
area: number-theory/divisibility-and-gcd
level: intro
summary: Compute gcd(a, b) for given integers a and b.
prereqs: [greatest-common-divisor, divisibility]
see_also: [euclidean-algorithm, binary-gcd, lehmers-gcd, half-gcd, extended-euclidean-algorithm, gcd-of-array, lames-theorem, polynomial-gcd]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.2, Greatest common divisor (Euclid's algorithm, the GCD recursion theorem, Lamé's theorem and the extended algorithm)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.5.2, The Greatest Common Divisor (Euclid's algorithm, the binary gcd, Lehmer's method for large numbers), and Section 4.5.3, Analysis of Euclid's Algorithm
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 1.6, Greatest common divisor (1.6.1 Naive GCD, 1.6.2 Extended GCD, 1.6.3 Half binary GCD, divide and conquer GCD)
  - paper: doi:10.1090/S0025-5718-07-02017-0
    title: Niels Möller, On Schönhage's algorithm and subquadratic integer gcd computation, Mathematics of Computation 77 (2008)
    locator: pages 589 to 607 (the subquadratic algorithms and their running time O(n (log n)^2 log log n))
---

The GCD of two integers is the problem of computing the [greatest common divisor](/greatest-common-divisor/) $\gcd(a, b)$ of two given integers. It is one of the oldest problems with a known algorithm: the [Euclidean algorithm](/euclidean-algorithm/) solves it with $O(\log \min(|a|, |b|))$ divisions, and needs no factoring. For numbers with $n$ bits, the classical methods take $O(n^2)$ bit operations, and the [half-GCD](/half-gcd/) method takes $O(M(n) \log n)$, where $M(n)$ is the cost of multiplying two $n$-bit numbers. Fractions, [modular inverses](/modular-inverse/), RSA key generation and many other tasks call it as a subroutine.

## In plain words

You are given two whole numbers and must find the largest number that divides both. Trying every candidate is slow for large numbers, and splitting both numbers into primes is even slower. The classical trick is that the answer does not change when you replace the larger number by its remainder after division by the smaller one. The numbers shrink fast, and when one of them becomes zero, the other one is the answer. Even numbers with hundreds of digits take only a few hundred such steps.

## Definition

**Input.** Two integers $a$ and $b$. Either may be negative or zero.

**Output.** The integer $g = \gcd(a, b) \ge 0$: the largest integer that divides both $a$ and $b$ when they are not both zero, and $g = 0$ when $a = b = 0$. Equivalently, $g \ge 0$, $g \mid a$, $g \mid b$, and every common divisor of $a$ and $b$ divides $g$.

**Cost models.** Two models are in use, and a bound must say which one it uses.

- **Word-sized inputs.** On the [word RAM](/word-ram/) with $|a|, |b| < 2^w$, each arithmetic operation, including division with remainder, costs one unit. The cost is the number of steps.
- **Arbitrary precision.** The inputs have $n$ bits each, $n = \lceil \lg(\max(|a|, |b|) + 1) \rceil$, and the cost is the number of bit operations (or word operations on $n/w$-word numbers). $M(n)$ denotes the cost of multiplying two $n$-bit integers: $O(n^2)$ by the schoolbook method, $O(n^{1.585})$ by [Karatsuba](/karatsuba-multiplication/), and $O(n \log n)$ by [Harvey and van der Hoeven](/harvey-van-der-hoeven-multiplication/).

## Variants

- **Extended GCD.** Also output integers $x$ and $y$ with $ax + by = g$ ([Bézout's identity](/bezouts-identity/)). The [extended Euclidean algorithm](/extended-euclidean-algorithm/) solves it at the same asymptotic cost. It gives [modular inverses](/modular-inverse/) and solves [linear Diophantine equations](/linear-diophantine-equation/).
- **Decision.** Decide whether $\gcd(a, b) = 1$, that is, whether $a$ and $b$ are [coprime](/coprime-integers/). No method is known that is faster than computing the gcd.
- **Many integers.** The [GCD of an array](/gcd-of-array/), the [GCD of all pairs](/all-pairs-gcd/) and [batch GCD](/batch-gcd/), which finds all shared factors among many numbers faster than pair by pair.
- **The least common multiple.** $\operatorname{lcm}(a, b) = |a| / \gcd(a, b) \cdot |b|$ by the [GCD and LCM identity](/gcd-lcm-identity/), so the [LCM of integers](/lcm-of-integers/) reduces to this problem.
- **Other rings.** The [polynomial GCD](/polynomial-gcd/) over a field, and the gcd in any [Euclidean domain](/euclidean-domain/), where the answer is unique only up to a unit.

## Examples

| $a$ | $b$ | $\gcd(a, b)$ | division steps of Euclid |
| --- | --- | --- | --- |
| 1071 | 462 | 21 | 3 |
| $-48$ | 18 | 6 | 3 |
| 0 | $-5$ | 5 | 1 |
| 0 | 0 | 0 | 0 |
| $2^{64}$ | $3 \cdot 2^{40}$ | $2^{40}$ | 2 |
| $10^{12} + 39$ | $10^{12} + 38$ | 1 | 2 |
| $F_{30} = 832040$ | $F_{31} = 1346269$ | 1 | 30 |

The steps count the divisions of the Euclidean algorithm on $(|a|, |b|)$ until the second number is 0. Consecutive [Fibonacci numbers](/fibonacci-numbers/) are the worst case for their size: all quotients are 1 except the last, and [Lamé's theorem](/lames-theorem/) shows that no smaller pair needs as many steps. Large inputs that differ by a small amount are easy: one division brings the second number down to the difference.

## Known algorithms

- [Euclidean algorithm](/euclidean-algorithm/): replace $(a, b)$ by $(b, a \bmod b)$. $O(\log \min(|a|, |b|))$ divisions; $O(n^2)$ bit operations.
- [Binary GCD](/binary-gcd/) (Stein's algorithm): uses only shifts, subtractions and parity tests. $O(n)$ iterations of $O(n)$ bit operations each, so $O(n^2)$; fast on word-sized inputs with a count-trailing-zeros instruction.
- [Lehmer's GCD](/lehmers-gcd/): runs the Euclidean steps on the leading words and applies them to the full numbers in one batch. $O(n^2)$ bit operations, with far fewer multiprecision operations.
- [Half-GCD](/half-gcd/) (Knuth and Schönhage): divide and conquer on the leading halves. $O(M(n) \log n)$ bit operations.
- [Extended Euclidean algorithm](/extended-euclidean-algorithm/): the Euclidean algorithm with the Bézout coefficients, $O(n^2)$ bit operations.

## Bounds

**Word-sized inputs.** The Euclidean algorithm makes at most about $\log_\varphi \min(|a|, |b|) + 2$ divisions, where $\varphi = (1 + \sqrt 5)/2$ ([Lamé's theorem](/lames-theorem/)). Each division costs $O(1)$ on the word RAM, so the time is $O(\log \min(|a|, |b|)) = O(w)$ in the worst case. The binary GCD also takes $O(w)$ iterations.

**Arbitrary precision, quadratic.** Let the Euclidean algorithm on $n$-bit inputs produce quotients $q_1, \ldots, q_k$. Schoolbook division of a number of at most $n$ bits by a smaller one, with quotient $q_i$, costs $O(n (1 + \lg q_i))$ bit operations. Since $r_{i-1} \ge q_i r_i$, the product $q_1 q_2 \cdots q_k$ is at most $|a|$, so $\sum_i \lg q_i \le n$, and $k = O(n)$. The total is $O(n (k + n)) = O(n^2)$ in the worst case (Knuth, Section 4.5.3).

**Arbitrary precision, subquadratic.** The half-GCD method computes the gcd in $O(M(n) \log n)$ bit operations. With $M(n) = O(n \log n)$ this is $O(n \log^2 n)$; with Schönhage and Strassen multiplication it is $O(n \log^2 n \log \log n)$, the bound in Möller's paper.

**Lower bounds.** Every algorithm must read its input, so $\Omega(n)$ bit operations are needed. No better general lower bound is known in the standard models, so the gap between $\Omega(n)$ and $O(M(n) \log n)$ is open. It is also not known whether the gcd of two $n$-bit integers can be computed by a parallel algorithm in polylogarithmic time with a polynomial number of processors (the question whether the problem is in NC).

## Reductions

- **To multiplication.** The half-GCD method reduces the gcd to $O(\log n)$ levels of multiplications, which is the source of the bound $O(M(n) \log n)$.
- **From the lcm and from fractions.** The [LCM of integers](/lcm-of-integers/) and [reducing fractions](/reducing-fractions/) take one gcd and one or two exact divisions.
- **From modular inversion.** $a$ has an inverse modulo $m$ if and only if $\gcd(a, m) = 1$; the extended gcd gives it.
- **Not through factoring.** The [fundamental theorem of arithmetic](/fundamental-theorem-of-arithmetic/) gives $\gcd(a, b)$ from the factorizations of $a$ and $b$, but [integer factorization](/integer-factorization/) is much harder than the gcd, so this route is never used to compute it.

## Applications

- **Exact rational arithmetic.** Each sum or product of fractions is reduced with a gcd ([reducing fractions](/reducing-fractions/)).
- **Modular arithmetic and cryptography.** [Modular inverses](/modular-inverse/), the [Chinese remainder theorem](/chinese-remainder-theorem/), and RSA key generation, where the public exponent must be coprime to $\varphi(N)$.
- **Finding shared factors.** If two RSA moduli share a prime, their gcd reveals it. [Batch GCD](/batch-gcd/) applies this to millions of keys at once.
- **Factoring algorithms.** [Pollard's rho](/pollard-rho/) and [Pollard's p minus 1](/pollard-p-minus-1/) method find a factor of $N$ as $\gcd(x, N)$ for a well-chosen $x$.
- **Periods and alignment.** Two cycles of lengths $a$ and $b$ realign after $\operatorname{lcm}(a, b)$ steps, and a rotation of an array of length $n$ by $k$ splits it into $\gcd(n, k)$ cycles.

## References
