---
tag: 8ZDJKH
kind: problem
slug: lcm-of-integers
name: LCM of integers
aliases:
- lcm of an array
- lcm of many integers
area: number-theory/divisibility-and-gcd
level: intro
summary: Compute the least common multiple of two or more integers.
prereqs: [least-common-multiple, greatest-common-divisor, gcd-lcm-identity]
see_also: [gcd-of-two-integers, gcd-of-array, euclidean-algorithm, chinese-remainder-theorem, carmichael-function, permutation-cycles]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.5.2, The Greatest Common Divisor (the least common multiple and its relation to the gcd)
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 4.1, Divisibility, and Section 4.2, Primes (lcm as the maximum of the prime exponents)
  - paper: "M. Nair, On Chebyshev-type inequalities for primes, American Mathematical Monthly 89 (1982)"
    locator: pages 126 to 129 (lcm(1, 2, ..., n) is at least 2^n for n at least 7)
---

The LCM of integers is the problem of computing the [least common multiple](/least-common-multiple/) of a list of integers: the smallest positive integer that each of them divides, or 0 if one of them is 0. The standard method folds the two-number formula $\operatorname{lcm}(x, y) = |x| / \gcd(x, y) \cdot |y|$ over the list, so it costs one [gcd](/gcd-of-two-integers/) and one exact division per number. The answer can be much larger than the inputs: $\operatorname{lcm}(1, 2, \ldots, n)$ grows like $e^{n}$, so with 64-bit integers the fold overflows already for the numbers 1 to 43.

## In plain words

Several machines start together, and each one repeats its cycle every so many seconds. You want to know when they all start a cycle together again. That moment is the least common multiple of the cycle lengths. Two lengths are easy: divide one by their largest common divisor and multiply by the other. For a longer list, combine the first two, then combine the result with the third, and so on. The answer can grow very fast, so on a computer you must watch for numbers that no longer fit in a machine word.

## Definition

**Input.** Integers $a_1, \ldots, a_k$ with $k \ge 1$.

**Output.** $L = \operatorname{lcm}(a_1, \ldots, a_k)$: if all $a_i \ne 0$, the least positive integer with $a_i \mid L$ for each $i$; if some $a_i = 0$, then $L = 0$. Signs do not matter: $L = \operatorname{lcm}(|a_1|, \ldots, |a_k|)$. Equivalently, $L \ge 0$, each $a_i$ divides $L$, and $L$ divides every common multiple of the $a_i$.

**Cost models.** On the [word RAM](/word-ram/) each operation on a word costs one unit, but the answer may not fit in a word, so a word-sized solution must detect overflow. With arbitrary precision, let $n_i$ be the bit length of $a_i$ and $B = \sum_i n_i$; the answer has at most $B$ bits, and costs are counted in bit operations.

## Variants

- **Two numbers.** $\operatorname{lcm}(a, b) = |a| / \gcd(a, b) \cdot |b|$, by the [GCD and LCM identity](/gcd-lcm-identity/).
- **The first $n$ integers.** $\operatorname{lcm}(1, \ldots, n) = \prod_{p \le n} p^{\lfloor \log_p n \rfloor}$: each prime $p \le n$ appears with the largest power that is at most $n$.
- **The lcm modulo a prime.** When the true lcm is too large, contests ask for it modulo $m$. The fold cannot be done modulo $m$, because it divides by a gcd of the true values. The correct method factors each $a_i$, keeps the maximum exponent of each prime, and multiplies the prime powers modulo $m$.
- **Range queries.** The lcm of a subarray, with updates. The answer grows quickly, so this is usually asked modulo a prime, with the prime exponents kept in a segment tree.

## Examples

- $\operatorname{lcm}(4, 6, 10) = 60$ and $\operatorname{lcm}(12, 18, 30) = 180$.
- $\operatorname{lcm}(3, 0, 5) = 0$ and $\operatorname{lcm}(-4, 6) = 12$.
- $\operatorname{lcm}(2^3, 2^7, 2^5) = 2^7 = 128$: for powers of one prime the lcm is the largest.
- $\operatorname{lcm}(2, 3, 4, 5, 6) = 60$.
- $\operatorname{lcm}(1, \ldots, 20) = 232792560 = 2^4 \cdot 3^2 \cdot 5 \cdot 7 \cdot 11 \cdot 13 \cdot 17 \cdot 19$.
- $\operatorname{lcm}(1, \ldots, 42) = 219060189739591200 < 2^{63}$, but $\operatorname{lcm}(1, \ldots, 43) = 9419588158802421600 > 2^{63}$, so a signed 64-bit fold overflows at 43.
- $\operatorname{lcm}(1, \ldots, 100)$ has 136 bits.

A trace of the fold on $(4, 6, 10)$: start with $L = 4$; $\gcd(4, 6) = 2$, so $L = 4/2 \cdot 6 = 12$; $\gcd(12, 10) = 2$, so $L = 12/2 \cdot 10 = 60$.

## Known algorithms

**Fold with the gcd.** Set $L \leftarrow |a_1|$. For $i = 2, \ldots, k$: if $L = 0$ or $a_i = 0$, set $L \leftarrow 0$; else set $L \leftarrow (L / \gcd(L, a_i)) \cdot |a_i|$. Return $L$.

*Correctness.* By induction on $i$, $L = \operatorname{lcm}(a_1, \ldots, a_i)$ after step $i$. The step uses $\operatorname{lcm}(a_1, \ldots, a_i) = \operatorname{lcm}(\operatorname{lcm}(a_1, \ldots, a_{i-1}), a_i)$, which holds because both sides are the nonnegative integer that divides exactly the common multiples of $a_1, \ldots, a_i$ (the divisibility form of the definition), and then the two-number identity.

*Cost.* On the word RAM, $k - 1$ gcd computations of $O(w)$ steps each when no overflow occurs, so $O(k w)$ time. With arbitrary precision and schoolbook arithmetic, step $i$ costs $O(|L| \cdot n_i + n_i^2)$ bit operations: one reduction $L \bmod a_i$, a gcd of two numbers of at most $n_i$ bits by the [Euclidean algorithm](/euclidean-algorithm/), one exact division and one multiplication. Since $|L| \le B$, the sum over $i$ is $O(B^2)$.

**Through the factorizations.** If the $a_i$ are small, factor each one, for example with a [smallest prime factor table](/smallest-prime-factor-table/), and take the largest exponent of each prime. This is the method for the lcm modulo a prime.

**The first $n$ integers.** Sieve the primes up to $n$ with the [sieve of Eratosthenes](/sieve-of-eratosthenes/) and multiply $p^{\lfloor \log_p n \rfloor}$ over them.

## Bounds

- **Size of the answer.** $L \le \prod_i |a_i|$, so $L$ has at most $B$ bits. Equality holds when the $a_i$ are pairwise [coprime](/coprime-integers/). Writing the answer needs $\Omega(\log L)$ bit operations, so $\Omega(B)$ in the worst case.
- **Growth of $\operatorname{lcm}(1, \ldots, n)$.** $\ln \operatorname{lcm}(1, \ldots, n) = \sum_{p^j \le n} \ln p$, which is Chebyshev's function $\psi(n)$. By the [prime number theorem](/prime-number-theorem/), $\psi(n) \sim n$, so $\operatorname{lcm}(1, \ldots, n) = e^{(1 + o(1)) n}$. For $n = 1000$, $\ln \operatorname{lcm}(1, \ldots, n) / n \approx 0.997$. Nair proved the elementary bound $\operatorname{lcm}(1, \ldots, n) \ge 2^n$ for $n \ge 7$.
- **Overflow.** On the word RAM, test $L / g > \lfloor (2^{w-1} - 1) / |a_i| \rfloor$ before the multiplication to detect overflow.

## Reductions

- **To the gcd.** Each step of the fold is one gcd and one exact division, so the problem reduces to $k - 1$ instances of the [GCD of two integers](/gcd-of-two-integers/).
- **Dual of the gcd of an array.** The [GCD of an array](/gcd-of-array/) is the same fold with the gcd, and with exponents it takes the minimum where the lcm takes the maximum.

## Applications

- **Periods.** Events with periods $a_1, \ldots, a_k$ coincide again after $\operatorname{lcm}(a_1, \ldots, a_k)$ steps. The order of a permutation is the lcm of its [cycle](/permutation-cycles/) lengths: a permutation with cycles of lengths 3, 4 and 5 has order 60.
- **Common denominators.** The least common denominator of fractions in lowest terms is the lcm of their denominators.
- **Chinese remainder theorem.** A system of congruences $x \equiv r_i \pmod{m_i}$ that is consistent has a unique solution modulo $\operatorname{lcm}(m_1, \ldots, m_k)$; see the [Chinese remainder theorem](/chinese-remainder-theorem/).
- **Group exponents.** The [Carmichael function](/carmichael-function/) $\lambda(n)$ is the lcm of $\lambda$ over the prime powers of $n$.

## References
