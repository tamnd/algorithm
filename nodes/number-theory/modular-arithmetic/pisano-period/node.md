---
tag: B3XJ1S
kind: concept
slug: pisano-period
name: Pisano period
area: number-theory/modular-arithmetic
level: core
summary: The length π(m) of the cycle after which the Fibonacci numbers taken modulo m repeat; it is at most 6m and divides p − 1 or 2(p + 1) for most primes p.
prereqs: [fibonacci-numbers, congruence]
see_also: [fibonacci-fast-doubling, matrix-fibonacci, matrix-exponentiation, multiplicative-order, quadratic-reciprocity, cycle-detection, chinese-remainder-theorem]
sources:
  - paper: "D. D. Wall, Fibonacci series modulo m, The American Mathematical Monthly 67(6), 1960"
    locator: pages 525 to 532 (periodicity, the lcm rule, the bounds for prime moduli and the question whether π(p^2) = π(p) can hold)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.8, Fibonacci Numbers (the closed form with the golden ratio and the identities used here)
  - url: "https://oeis.org/A001175"
    locator: OEIS A001175, Pisano periods (values of π(m) and the listed properties)
  - url: "https://en.wikipedia.org/wiki/Pisano_period"
    locator: Wikipedia, Pisano period (the properties, the bound π(m) ≤ 6m and Wall's question)
---

The Pisano period $\pi(m)$ is the period of the [Fibonacci numbers](/fibonacci-numbers/) modulo $m$: the least $k \ge 1$ with $F_k \equiv 0$ and $F_{k+1} \equiv 1 \pmod m$. The sequence modulo $m$ is purely periodic, and $\pi(m) \le 6m$ for all $m$. For a prime $p \equiv \pm 1 \pmod{10}$, $\pi(p)$ divides $p - 1$; for $p \equiv \pm 3 \pmod{10}$ it divides $2(p + 1)$, results that come from [quadratic reciprocity](/quadratic-reciprocity/) and the order of the golden ratio in a finite field. A practical use is that $F_n \bmod m = F_{n \bmod \pi(m)} \bmod m$, which reduces a huge index before any computation.

## In plain words

Write down the Fibonacci numbers, where each number is the sum of the two before it, but keep only the remainder after division by a fixed number. The remainders are small, so the same pair of neighbours must show up again. From that point the whole list repeats, because each pair fixes the next number. The list also runs backwards, so the repeat goes all the way back to the start, 0 and 1. The length of this cycle is the Pisano period. For the last digit, the cycle has 60 steps. So to get the last digit of a Fibonacci number with a huge position, you can shrink the position to its remainder by 60 first.

## The idea

**Periodicity.** Modulo $m$ there are $m^2$ pairs $(F_n \bmod m, F_{n+1} \bmod m)$, so two of the first $m^2 + 1$ pairs are equal. The step $(x, y) \mapsto (y, x + y)$ has the inverse $(x, y) \mapsto (y - x, x)$, so it is a permutation of the finite set of pairs, and every orbit is a pure cycle. Hence the pair $(0, 1)$ comes back, and $\pi(m)$ is the length of its cycle. In matrix form, $\pi(m)$ is the [multiplicative order](/multiplicative-order/) of $Q = \begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}$ in the group of invertible $2 \times 2$ matrices modulo $m$, since $Q^n = \begin{pmatrix} F_{n+1} & F_n \\ F_n & F_{n-1} \end{pmatrix}$.

**Reducing the index.** Since the sequence repeats, $F_n \equiv F_{n \bmod \pi(m)} \pmod m$, and more generally $F_a \equiv F_b \pmod m$ when $a \equiv b \pmod{\pi(m)}$.

**Several moduli.** For coprime $m$ and $n$, by the [Chinese remainder theorem](/chinese-remainder-theorem/) a pair repeats modulo $mn$ exactly when it repeats modulo both, so $\pi(mn) = \operatorname{lcm}(\pi(m), \pi(n))$. More generally $\pi(\operatorname{lcm}(m, n)) = \operatorname{lcm}(\pi(m), \pi(n))$. So $\pi$ is determined by its values at prime powers.

**Prime moduli.** By the closed form, $F_n = (\varphi^n - \psi^n)/(\varphi - \psi)$, where $\varphi$ and $\psi$ are the roots of $x^2 - x - 1$, with $\varphi \psi = -1$ and $(\varphi - \psi)^2 = 5$. Let $p \ne 2, 5$ be prime.

- If $p \equiv \pm 1 \pmod{10}$, then 5 is a [quadratic residue](/quadratic-residue/) modulo $p$ by quadratic reciprocity, so $\varphi$ and $\psi$ lie in $\mathbb{Z}_p^*$. Both have orders dividing $p - 1$, so $\pi(p) \mid p - 1$.
- If $p \equiv \pm 3 \pmod{10}$, then 5 is a nonresidue, $\varphi$ and $\psi$ lie in the field with $p^2$ elements, and the Frobenius map sends $\varphi$ to $\varphi^p = \psi$. So $\varphi^{p+1} = \varphi \psi = -1$ and $\varphi^{2(p+1)} = 1$, and $\pi(p) \mid 2(p + 1)$. In this case $\pi(p)$ does not divide $p + 1$.
- For the small primes, $\pi(2) = 3$ and $\pi(5) = 20$.

**Prime powers.** For every prime $p$, $\pi(p^k)$ divides $p^{k-1} \pi(p)$. In all cases computed so far, $\pi(p^k) = p^{k-1} \pi(p)$. Equality for all $k$ holds if and only if $\pi(p^2) \ne \pi(p)$; Wall asked in 1960 whether a prime with $\pi(p^2) = \pi(p)$ exists. Such primes are called Wall-Sun-Sun primes, and none is known.

**Other properties.** $\pi(m)$ is even for $m > 2$. $\pi(m) \le 6m$, with equality exactly for $m = 2 \cdot 5^k$, $k \ge 1$. The first index $\alpha(m) \ge 1$ with $m \mid F_{\alpha(m)}$, the rank of apparition, divides $\pi(m)$, and $\pi(m)/\alpha(m)$ is 1, 2 or 4; this ratio is the number of zeros in one period.

**Computing it.** For small $m$, run the recurrence from $(0, 1)$ until $(0, 1)$ comes back: at most $6m$ steps of $O(1)$ word operations, and $O(1)$ space. For large $m$ with a known factorization, compute $\pi(p)$ for each prime factor as the least divisor $d$ of $p - 1$ or $2(p + 1)$ with $Q^d \equiv I \pmod p$, using [fast doubling](/fibonacci-fast-doubling/) or [matrix exponentiation](/matrix-exponentiation/) and the same divisor-removal method as for the [multiplicative order](/multiplicative-order/). Then check the candidate $p^{k-1} \pi(p)$ for each prime power and combine with lcm. Without the factorization of $m$, no fast method is known. Generic [cycle detection](/cycle-detection/) is not needed: the cycle always passes through $(0, 1)$.

## Examples

**Modulo 2 and 3.** Modulo 2 the sequence is $0, 1, 1, 0, 1, 1, \ldots$, so $\pi(2) = 3$. Modulo 3 it is $0, 1, 1, 2, 0, 2, 2, 1, 0, 1, \ldots$, so $\pi(3) = 8$.

**Small values.** For $m = 1, \ldots, 15$:

| $m$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $\pi(m)$ | 1 | 3 | 8 | 6 | 20 | 24 | 16 | 12 | 24 | 60 | 10 | 24 | 28 | 48 | 40 |

The lcm rule: $\pi(12) = \operatorname{lcm}(\pi(4), \pi(3)) = \operatorname{lcm}(6, 8) = 24$, and $\pi(10) = \operatorname{lcm}(3, 20) = 60$.

**Prime moduli.** $11 \equiv 1 \pmod{10}$ and $\pi(11) = 10 = 11 - 1$; $29 \equiv -1 \pmod{10}$ and $\pi(29) = 14$, a proper divisor of 28. $7 \equiv -3 \pmod{10}$ and $\pi(7) = 16 = 2 \cdot 8$; $13 \equiv 3 \pmod{10}$ and $\pi(13) = 28 = 2 \cdot 14$.

**Prime powers.** $\pi(4) = 6 = 2 \cdot 3$, $\pi(9) = 24 = 3 \cdot 8$, $\pi(25) = 100 = 5 \cdot 20$, $\pi(49) = 112 = 7 \cdot 16$ and $\pi(121) = 110 = 11 \cdot 10$.

**Last digits.** $\pi(10) = 60$, $\pi(100) = 300$, $\pi(1000) = 1500$ and $\pi(10^4) = 15000$. To find the last digit of $F_{10^{18}}$: $10^{18} \bmod 60 = 40$, and $F_{40} = 102334155$, so the last digit is 5.

**The bound.** $\pi(10) = 60 = 6 \cdot 10$ and $\pi(50) = 300 = 6 \cdot 50$ reach the bound $6m$.

**Zeros per period.** Modulo 11, $\alpha = 10 = \pi$, one zero per period; modulo 3, $\alpha = 4$ and $\pi = 8$, two zeros; modulo 13, $\alpha = 7$ and $\pi = 28$, four zeros.

## Where it is used

- **Fibonacci numbers modulo m for huge indices.** Reduce $n$ modulo $\pi(m)$ first, then use [fast doubling](/fibonacci-fast-doubling/); this is a common step in programming contests. For a fixed small $m$, a table of one period answers every query in $O(1)$.
- **Nested recurrences.** To compute $F_{F_n} \bmod m$, compute $F_n \bmod \pi(m)$, then the outer value. The same idea applies to any linear recurrence and its period modulo $m$.
- **Primality and Lucas sequences.** The divisibility $F_{p - (5/p)} \equiv 0 \pmod p$ for primes $p \ne 2, 5$, which follows from the prime case above, is the basis of the Fibonacci and Lucas probable-prime tests.
- **Pseudorandom generators.** Lagged Fibonacci generators and other linear recurrences modulo $m$ are analysed through the period of the recurrence modulo prime powers.
- **Number theory.** Wall-Sun-Sun primes are linked to the first case of Fermat's last theorem, and searches for them use the computation of $\pi(p^2)$.

## References
